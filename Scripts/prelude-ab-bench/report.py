#!/usr/bin/env python3
"""report.py <jobs.json> <outdir> <report.md> [vcs.csv] [--classes=classes.csv,...]

Summarises run.py's CSVs. A VC is *affected* when its resource counts under master and under
the PR differ for some seed. That includes VCs the change merely perturbs (their SMT is
reordered, not changed) and VCs that are nondeterministic across processes; the master2 (A/A)
and placebo rows measure those floors, and classify.py's classes.csv separates VCs whose SMT
contains the changed axiom. Costs are means over seeds. Verdicts are read at each job's own
limit (50M per VC for lit tests and synthetic programs, 5M for the standard library), though
the runs themselves used a much higher limit so that costs beyond it are measured.
"""
import collections, csv, glob, json, math, os, re, statistics as st, sys

CLASSES = [p for a in sys.argv[1:] if a.startswith("--classes=") for p in a.split("=", 1)[1].split(",") if p]
argv = [a for a in sys.argv if not a.startswith("--classes=")]
jobs_path, outdir, report_path = argv[1:4]
vcs_path = argv[4] if len(argv) > 4 else None
jobs = {j["id"]: j for j in json.load(open(jobs_path))}
esc = {j.replace("/", "__").replace(":", "--"): j for j in jobs}
PRE = ["master", "pr", "placebo"]


def dur(s):
    h, m, sec = s.split(":")
    return int(h) * 3600 + int(m) * 60 + float(sec)


data = collections.defaultdict(lambda: collections.defaultdict(dict))  # job -> prelude -> seed -> {vc: (outcome, ru, t)}
for path in glob.glob(os.path.join(outdir, "*.csv")):
    stem, p, s = os.path.basename(path)[:-4].rsplit("@", 2)
    if stem not in esc:  # a run of a job this report does not cover
        continue
    job = esc[stem]
    rows = {}
    for r in csv.DictReader(open(path)):
        rows[r["TestResult.DisplayName"]] = (r["TestResult.Outcome"], int(r["TestResult.ResourceCount"]),
                                             dur(r["TestResult.Duration"]))
    data[job][p][int(s)] = rows

seeds = sorted({s for j in data for p in data[j] for s in data[j][p]})
missing = [p for p in PRE if not any(p in data[j] for j in data)]
if missing:
    sys.exit(f"report.py needs runs under the {', '.join(PRE)} preludes; none for {', '.join(missing)}")


def verdict(outcome, ru, limit):
    if outcome == "Passed":
        return "ok" if ru <= limit else "over"
    if outcome in ("OutOfResource", "TimedOut"):
        return "over"
    return "error"


ALTS = sorted({p for j in data for p in data[j]} - set(PRE))
allrows, vcrows = [], []
for job in sorted(data):
    limit = jobs[job]["limit"]
    names = sorted({n for p in data[job] for s in data[job][p] for n in data[job][p][s]})
    for n in names:
        rec = {"job": job, "vc": n, "limit": limit}
        for p in PRE + ALTS:
            runs = [data[job][p][s].get(n) for s in seeds if s in data[job].get(p, {})]
            runs = [r for r in runs if r]
            rec[p] = runs
        if not all(rec[p] for p in PRE):
            continue
        rec["affected"] = [r[1] for r in rec["master"]] != [r[1] for r in rec["pr"]]
        allrows.append(rec)
        # master's UnionFind.dfy (Main not isolated) duplicates the PR's; it gets its own section
        if "-noiso" not in job:
            vcrows.append(rec)

aff = [r for r in vcrows if r["affected"]]
unaff = [r for r in vcrows if not r["affected"]]
placebo_diff_unaff = [r for r in unaff if [x[1] for x in r["master"]] != [x[1] for x in r["placebo"]]]


def mean_ru(runs): return st.mean(r[1] for r in runs)
def mean_t(runs): return st.mean(r[2] for r in runs)
def gm(xs): return math.exp(st.mean(math.log(x) for x in xs)) if xs else float("nan")
def pct(x): return f"{(x - 1) * 100:+.1f}%"


out = []
w = out.append
w("# Map#Glue prelude A/B benchmark\n")
w(f"Seeds per (VC, prelude): {len(seeds)} ({', '.join(map(str, seeds))}; 0 is Dafny's default). "
  f"VCs: {len(vcrows)} in {len(data)} jobs; **{len(aff)} affected** (master and PR counts differ), "
  f"{len(unaff)} unaffected (identical counts under master and PR for every seed).")
w(f"Unaffected VCs whose counts differ under the placebo: {len(placebo_diff_unaff)}.\n")

import random
random.seed(6539)


def program(r):  # a program: a job without its resolver configuration
    return r["job"].split(":")[0]


def boot(rs, alt, n=2000, ref="master"):
    """Point estimates and 95% bootstrap intervals of the total-cost ratio, the geomean of per-VC
    ratios, and the geomean of per-program geomeans (each program weighs the same). Programs are
    resampled as units: the VCs of one program are not independent of each other."""
    by = collections.defaultdict(list)
    for r in rs:
        by[program(r)].append((max(mean_ru(r[ref]), 1), max(mean_ru(r[alt]), 1)))
    progs = list(by)
    stats = lambda sample: (sum(p for vs in sample for _, p in vs) / sum(m for vs in sample for m, _ in vs),
                            math.exp(st.mean(math.log(p / m) for vs in sample for m, p in vs)),
                            math.exp(st.mean(st.mean(math.log(p / m) for m, p in vs) for vs in sample)))
    point = stats([by[p] for p in progs])
    draws = [stats([by[random.choice(progs)] for _ in progs]) for _ in range(n)]
    cis = []
    for k in range(3):
        xs = sorted(d[k] for d in draws)
        cis.append(f"{pct(point[k])} [{pct(xs[int(0.025 * n)])}, {pct(xs[int(0.975 * n)])}]")
    return cis


def passing(r):  # a proof: passes under every prelude and seed
    return all(o == "Passed" for p in PRE for o, _, _ in r[p])


w("## Proof cost over affected VCs that pass everywhere\n")
w("Totals are sums of per-VC means over seeds. \"Per program\" averages each program's own VC geomean, so a\n"
  "program with hundreds of VCs weighs no more than one with two. Brackets are 95% bootstrap intervals that\n"
  "resample programs, not VCs.\n")
w("| group | programs | VCs | largest program | total PR/master | geomean over VCs | per program | placebo per program |")
w("|---|---:|---:|---|---|---|---|---|")
proofs = [r for r in aff if passing(r)]
kinds = sorted({jobs[r["job"]]["kind"] for r in proofs})
groups = [("all but synth", [r for r in proofs if jobs[r["job"]]["kind"] != "synth"])] + \
         [(k, [r for r in proofs if jobs[r["job"]]["kind"] == k]) for k in kinds]
for g, rs in groups:
    if not rs:
        continue
    count = collections.Counter(program(r) for r in rs)
    big, n_big = count.most_common(1)[0]
    tot, geo, per = boot(rs, "pr")
    w(f"| {g} | {len(count)} | {len(rs)} | {big} ({100 * n_big / len(rs):.0f}% of VCs) | {tot} | {geo} | {per} | "
      f"{boot(rs, 'placebo')[2]} |")

fails = [r for r in aff if not passing(r)]
w(f"\n{len(fails)} affected VCs fail (a verification error) in some run; their cost is the solver's search for a "
  "counterexample, reported separately:\n")
w("| job | VC | master mean (min..max) | PR mean (min..max) | placebo mean |")
w("|---|---|---|---|---|")
for r in sorted(fails, key=lambda r: -mean_ru(r["master"]))[:10]:
    rng = lambda runs: f"{mean_ru(runs)/1e6:.2f}M ({min(x[1] for x in runs)/1e6:.2f}..{max(x[1] for x in runs)/1e6:.2f})"
    w(f"| {r['job']} | {r['vc']} | {rng(r['master'])} | {rng(r['pr'])} | {mean_ru(r['placebo'])/1e6:.2f}M |")
groups = [("all", proofs)] + [(k, [r for r in proofs if jobs[r["job"]]["kind"] == k]) for k in ("lit", "std", "synth")]

# Per-seed totals: spread across seeds, per prelude
w("\n## Total proof RU per seed (affected VCs that pass everywhere)\n")
w("| prelude | " + " | ".join(f"seed {s}" for s in seeds) + " | mean | sd |")
w("|---|" + "---:|" * (len(seeds) + 2))
for p in PRE:
    tots = []
    for i, s in enumerate(seeds):
        tots.append(sum(r[p][i][1] for r in proofs if len(r[p]) > i))
    w(f"| {p} | " + " | ".join(f"{t/1e6:.1f}M" for t in tots) + f" | {st.mean(tots)/1e6:.1f}M | {st.pstdev(tots)/1e6:.1f}M |")

# Wall time
w("\n## Solver time over those proofs (sum of per-VC means, seconds)\n")
w("| group | master | PR | placebo |")
w("|---|---:|---:|---:|")
for g, rs in groups:
    if rs:
        w(f"| {g} | {sum(mean_t(r['master']) for r in rs):.1f} | {sum(mean_t(r['pr']) for r in rs):.1f} | {sum(mean_t(r['placebo']) for r in rs):.1f} |")

# Distribution of per-VC ratios
w("\n## Distribution of per-VC cost ratios over those proofs (mean over seeds)\n")
w("| ratio bucket | PR/master | placebo/master |")
w("|---|---:|---:|")
buckets = [(0, 0.5, "< 0.5x"), (0.5, 0.8, "0.5-0.8x"), (0.8, 0.95, "0.8-0.95x"), (0.95, 1.05, "0.95-1.05x"),
           (1.05, 1.25, "1.05-1.25x"), (1.25, 2, "1.25-2x"), (2, 4, "2-4x"), (4, 1e18, ">= 4x")]
for lo, hi, lab in buckets:
    c1 = sum(1 for r in proofs if lo <= mean_ru(r["pr"]) / max(mean_ru(r["master"]), 1) < hi)
    c2 = sum(1 for r in proofs if lo <= mean_ru(r["placebo"]) / max(mean_ru(r["master"]), 1) < hi)
    w(f"| {lab} | {c1} | {c2} |")

# Verdicts at the job's own limit
w("\n## Verdict changes at each job's limit (seeds passing out of %d)\n" % len(seeds))
w("| job | VC | limit | master ok | PR ok | placebo ok | master RU | PR RU |")
w("|---|---|---:|---:|---:|---:|---:|---:|")
flips = 0
for r in vcrows:
    oks = {p: sum(verdict(o, ru, r["limit"]) == "ok" for o, ru, _ in r[p]) for p in PRE}
    if oks["master"] != oks["pr"] or oks["master"] != oks["placebo"]:
        flips += 1
        w(f"| {r['job']} | {r['vc']} | {r['limit']/1e6:.0f}M | {oks['master']} | {oks['pr']} | {oks['placebo']} | "
          f"{mean_ru(r['master'])/1e6:.2f}M | {mean_ru(r['pr'])/1e6:.2f}M |")
if not flips:
    w("| (none) | | | | | | | |")

# Largest absolute changes
w("\n## Largest changes among those proofs (by |PR - master| mean RU)\n")
w("| job | VC | master | PR | PR/master | placebo | min..max master | min..max PR |")
w("|---|---|---:|---:|---:|---:|---|---|")
for r in sorted(proofs, key=lambda r: -abs(mean_ru(r["pr"]) - mean_ru(r["master"])))[:25]:
    mm, pp, pl = mean_ru(r["master"]), mean_ru(r["pr"]), mean_ru(r["placebo"])
    rng = lambda runs: f"{min(x[1] for x in runs)/1e6:.2f}..{max(x[1] for x in runs)/1e6:.2f}M"
    w(f"| {r['job']} | {r['vc']} | {mm/1e6:.2f}M | {pp/1e6:.2f}M | {pp/max(mm,1):.2f} | {pl/1e6:.2f}M | {rng(r['master'])} | {rng(r['pr'])} |")

# Per-job totals
w("\n## Per job (proofs among the affected VCs)\n")
w("| job | VCs | master | PR | PR vs master | placebo vs master |")
w("|---|---:|---:|---:|---:|---:|")
byjob = collections.defaultdict(list)
for r in proofs:
    byjob[r["job"]].append(r)
for job in sorted(byjob, key=lambda j: -sum(mean_ru(r["master"]) for r in byjob[j])):
    rs = byjob[job]
    m = sum(mean_ru(r["master"]) for r in rs); p = sum(mean_ru(r["pr"]) for r in rs)
    pl = sum(mean_ru(r["placebo"]) for r in rs)
    w(f"| {job} | {len(rs)} | {m/1e6:.2f}M | {p/1e6:.2f}M | {pct(p/max(m,1))} | {pct(pl/max(m,1))} |")

# Synthetic scaling
syn = collections.defaultdict(dict)
for r in vcrows:
    mt = re.match(r"synth/(\w+)-(\d+)\.dfy", r["job"])
    if mt:
        fam, n = mt.group(1), int(mt.group(2))
        d = syn[fam].setdefault(n, {p: 0.0 for p in PRE})
        for p in PRE:
            d[p] += mean_ru(r[p])
if syn:
    sizes = sorted({n for f in syn for n in syn[f]})
    w("\n## Synthetic programs: total RU by size N (master / PR / placebo, mean over seeds)\n")
    w("| family | " + " | ".join(f"N={n}" for n in sizes) + " |")
    w("|---|" + "---|" * len(sizes))
    for fam in sorted(syn):
        cells = []
        for n in sizes:
            d = syn[fam].get(n)
            cells.append(f"{d['master']/1e6:.2f} / {d['pr']/1e6:.2f} / {d['placebo']/1e6:.2f}" if d else "")
        w(f"| {fam} | " + " | ".join(cells) + " |")

# master's UnionFind.dfy: Main as one VC
mains = [r for r in allrows if "-noiso" in r["job"] and r["vc"] == "Main (correctness)"]
if mains:
    w("\n## dafny4/UnionFind.dfy as on master (Main not isolated): Main's cost per seed\n")
    w("| resolver | prelude | " + " | ".join(f"seed {s}" for s in seeds) + " | over 50M |")
    w("|---|---|" + "---:|" * (len(seeds) + 1))
    for r in mains:
        for p in PRE + ALTS:
            if r[p]:
                w(f"| {r['job'].split(':')[-1]} | {p} | " + " | ".join(f"{x[1]/1e6:.1f}M" for x in r[p]) +
                  f" | {sum(x[1] > 50e6 for x in r[p])} |")

# Named comparisons: the noise floors first, then the change and its parts
COMPARISONS = [
    ("A/A: master2 vs master (same input, another process)", "master2", "master"),
    ("placebo vs master (the old axiom, rewritten)", "placebo", "master"),
    ("shape: pointwise vs master (the PR's quantifier without its guard)", "pointwise", "master"),
    ("guard: pr vs pointwise", "pr", "pointwise"),
    ("pr vs master", "pr", "master"),
    ("domguard vs master", "domguard", "master"),
    ("domguard vs pr", "domguard", "pr"),
]
present = {p for j in data for p in data[j]}
okn = lambda r, q: sum(verdict(o, ru, r["limit"]) == "ok" for o, ru, _ in r[q])
marker = {}
for path in CLASSES:
    for c in csv.DictReader(open(path)):
        if c["marker"] in ("True", "False"):
            marker[(c["job"], c["vc"])] = c["marker"] == "True"


def comparison_table(title, rs_all):
    cmps = [c for c in COMPARISONS if c[1] in present and c[2] in present]
    if not cmps or not rs_all:
        return
    w(f"\n## {title}\n")
    w("| comparison | programs | VCs | total | geomean over VCs | per program | verdict flips at limit |")
    w("|---|---:|---:|---|---|---|---:|")
    for lab, alt, ref in cmps:
        rs = [r for r in rs_all if r[alt] and r[ref]]
        if not rs:
            continue
        tot, geo, per = boot(rs, alt, ref=ref)
        flips = sum(1 for r in rs if len(r[alt]) == len(r[ref]) and okn(r, alt) != okn(r, ref))
        w(f"| {lab} | {len({program(r) for r in rs})} | {len(rs)} | {tot} | {geo} | {per} | {flips} |")


real = [r for r in proofs if jobs[r["job"]]["kind"] != "synth"]
comparison_table("Comparisons over the affected proofs (all but synth)", real)
if marker:
    known = [r for r in real if (r["job"], r["vc"]) in marker]
    comparison_table("... whose SMT contains the changed axiom (classify.py)", [r for r in known if marker[(r["job"], r["vc"])]])
    comparison_table("... whose SMT does not: a pure perturbation", [r for r in known if not marker[(r["job"], r["vc"])]])
    w(f"\n{len(real) - len(known)} of the {len(real)} affected proofs have no classification (unmapped or mixed log names).")
external = [r for r in real if jobs[r["job"]]["kind"] not in ("lit", "std")]
comparison_table("Comparisons over the external programs' affected proofs", external)

# Alternative encodings
if ALTS:
    w("\n## Alternative sound encodings, over the same proofs\n")
    w("restrict: elements defined everywhere, `$ArbitraryBoxValue` outside the domain. "
      "domguard: the PR's axiom guarded by `Map#Domain(Map#Glue(a, b, t))`. "
      "eager: the PR's axiom plus the trigger `{ Map#Glue(a, b, t), Set#IsMember(a, bx) }`.\n")
    w("| encoding | programs | VCs | total vs master | geomean over VCs vs master | per program vs master | per program vs PR | verdict flips vs master at limit |")
    w("|---|---:|---:|---|---|---|---|---:|")
    base = [r for r in proofs if jobs[r["job"]]["kind"] != "synth"]
    for alt in ["pr"] + ALTS:
        rs = [r for r in base if r[alt]]
        if not rs:
            continue
        tot, geo, per = boot(rs, alt)
        vs_pr = boot(rs, alt, ref="pr")[2] if alt != "pr" else ""
        okm = lambda r, q: sum(verdict(o, ru, r["limit"]) == "ok" for o, ru, _ in r[q])
        flips = sum(1 for r in allrows if len(r[alt]) == len(r["master"]) and "-noiso" not in r["job"]
                    and okm(r, alt) != okm(r, "master"))
        w(f"| {alt} | {len({program(r) for r in rs})} | {len(rs)} | {tot} | {geo} | {per} | {vs_pr} | {flips} |")
    for alt in ALTS:
        rs = [r for r in base if r[alt]]
        w(f"\n{alt}: largest differences from the PR\n")
        w("| job | VC | master | PR | " + alt + " |")
        w("|---|---|---:|---:|---:|")
        for r in sorted(rs, key=lambda r: -abs(mean_ru(r[alt]) - mean_ru(r["pr"])))[:6]:
            w(f"| {r['job']} | {r['vc']} | {mean_ru(r['master'])/1e6:.2f}M | {mean_ru(r['pr'])/1e6:.2f}M | {mean_ru(r[alt])/1e6:.2f}M |")
    syn2 = collections.defaultdict(dict)
    for r in vcrows:
        mt = re.match(r"synth/(\w+)-(\d+)\.dfy", r["job"])
        if mt and all(r[a] for a in ALTS):
            d = syn2[mt.group(1)].setdefault(int(mt.group(2)), collections.Counter())
            for q in ["master", "pr"] + ALTS:
                d[q] += mean_ru(r[q])
    if syn2:
        w("\nSynthetic programs at N=16 (total RU, mean over seeds):\n")
        w("| family | " + " | ".join(["master", "pr"] + ALTS) + " |")
        w("|---|" + "---:|" * (2 + len(ALTS)))
        for fam in sorted(syn2):
            d = syn2[fam].get(16)
            if d:
                w(f"| {fam} | " + " | ".join(f"{d[q]/1e6:.2f}M" for q in ["master", "pr"] + ALTS) + " |")

open(report_path, "w").write("\n".join(out) + "\n")
print("\n".join(out))

if vcs_path:
    with open(vcs_path, "w", newline="") as fh:
        cw = csv.writer(fh, lineterminator="\n")
        ps = PRE + ALTS
        cw.writerow(["job", "vc", "affected", "limit"] + [f"{p}_mean_ru" for p in ps] +
                    [f"{p}_ru_by_seed" for p in ps] + [f"{p}_outcomes" for p in ps] +
                    [f"{p}_seconds_by_seed" for p in ps])
        for r in allrows:
            cw.writerow([r["job"], r["vc"], r["affected"], int(r["limit"])] +
                        [round(mean_ru(r[p])) if r[p] else "" for p in ps] +
                        [" ".join(str(x[1]) for x in r[p]) for p in ps] +
                        [" ".join(x[0] for x in r[p]) for p in ps] +
                        [" ".join(f"{x[2]:.3f}" for x in r[p]) for p in ps])
