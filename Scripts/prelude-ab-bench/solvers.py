#!/usr/bin/env python3
"""solvers.py <jobs.json> <outdir> <ref> <alt> <report.md> [vcs.csv] [--seed 1] [--cap 60] [--kinds k1,k2]

Compares two variants of run.py --variants, typically two solvers, VC by VC: which VCs each proves
within the cap, how the other variant's failures end (an answer within the cap, or the cap), and how
long each takes on the VCs that both prove. Solvers count resources differently, so this compares
time, not resource counts. --kinds restricts the report to those job kinds.
"""
import argparse, collections, csv, glob, json, math, os, random, re, statistics as st

ap = argparse.ArgumentParser()
ap.add_argument("jobs"); ap.add_argument("outdir"); ap.add_argument("ref"); ap.add_argument("alt")
ap.add_argument("report"); ap.add_argument("vcs", nargs="?")
ap.add_argument("--seed", type=int, default=1)
ap.add_argument("--cap", type=float, default=60, help="the runs' per-VC time limit, in seconds")
ap.add_argument("--kinds", default=None)
a = ap.parse_args()
kinds = set(a.kinds.split(",")) if a.kinds else None
jobs = {j["id"]: j for j in json.load(open(a.jobs)) if not kinds or j["kind"] in kinds}
esc = {j.replace("/", "__").replace(":", "--"): j for j in jobs}
V = [a.ref, a.alt]
random.seed(6539)


def dur(s):
    h, m, sec = s.split(":")
    return int(h) * 3600 + int(m) * 60 + float(sec)


def load(job, v):
    """{(vc, k): (outcome, seconds)}, k numbering repeated names; None if the run left no CSV rows."""
    stem = os.path.join(a.outdir, job.replace("/", "__").replace(":", "--") + f"@{v}@{a.seed}")
    if not os.path.exists(stem + ".csv"):
        return None, None
    rows, seen = {}, collections.Counter()
    for r in csv.DictReader(open(stem + ".csv")):
        n = r["TestResult.DisplayName"]
        rows[(n, seen[n])] = (r["TestResult.Outcome"], dur(r["TestResult.Duration"]))
        seen[n] += 1
    log = open(stem + ".log", errors="replace").read() if os.path.exists(stem + ".log") else ""
    return rows, log


def verdict(o):
    if o is None:
        return "missing"
    outcome, t = o
    if outcome == "Passed" and t <= a.cap:
        return "proved"
    if outcome in ("TimedOut", "OutOfResource") or t >= 0.95 * a.cap:
        return "cap"
    return "failed"


PROVER_ERR = re.compile(r"Prover error: (.*)")
data, runs = {}, collections.defaultdict(collections.Counter)
errors = {v: collections.Counter() for v in V}
for job in sorted(jobs):
    loaded = {v: load(job, v) for v in V}
    if any(loaded[v][0] is None for v in V):
        continue
    for v in V:
        rows, log = loaded[v]
        m = re.search(r"^exit=(\S+)", log, re.M)
        code = m.group(1) if m else "?"
        runs[v]["no rows" if not rows else "ok" if code == "0" else f"exit {code}"] += 1
        for e in set(PROVER_ERR.findall(log)):
            errors[v][re.sub(r"<stdin>:\d+\.\d+", "<stdin>:L.C", e)[:120]] += 1
    data[job] = {v: loaded[v][0] for v in V}

recs = []
for job, d in data.items():
    for key in sorted(set(d[a.ref]) | set(d[a.alt])):
        recs.append({"job": job, "kind": jobs[job]["kind"], "vc": key[0], "k": key[1],
                     **{v: d[v].get(key) for v in V}, **{f"{v}_verdict": verdict(d[v].get(key)) for v in V}})


def program(job):
    return job.split(":")[0]


def gm(xs):
    return math.exp(st.mean(math.log(x) for x in xs)) if xs else float("nan")


def pct(x):
    return f"{(x - 1) * 100:+.0f}%" if abs(x - 1) >= 0.1 else f"{(x - 1) * 100:+.1f}%"


def ratio_stats(rs, n=2000):
    """Alt/ref time on VCs both prove: total, geomean over VCs, and per program (each program weighs the
    same), with 95% intervals that resample programs."""
    by = collections.defaultdict(lambda: [0.0, 0.0, 0.0, 0])
    for r in rs:
        t0, t1 = max(r[a.ref][1], 0.01), max(r[a.alt][1], 0.01)  # durations below 10 ms are noise
        x = by[program(r["job"])]
        x[0] += t0; x[1] += t1; x[2] += math.log(t1 / t0); x[3] += 1
    progs = list(by.values())
    if not progs:
        return ["-"] * 3
    f = lambda s: (sum(p[1] for p in s) / sum(p[0] for p in s), math.exp(sum(p[2] for p in s) / sum(p[3] for p in s)),
                   math.exp(st.mean(p[2] / p[3] for p in s)))
    point, draws = f(progs), [f([random.choice(progs) for _ in progs]) for _ in range(n)]
    out = []
    for k in range(3):
        xs = sorted(d[k] for d in draws)
        out.append(f"{pct(point[k])} [{pct(xs[int(0.025 * n)])}, {pct(xs[int(0.975 * n)])}]")
    return out


o = []
w = o.append
w(f"# {a.alt} against {a.ref}\n")
w(f"Seed {a.seed}, a per-VC time limit of {a.cap:g} s for both. {len(data)} jobs ran under both "
  f"({len({program(j) for j in data})} programs), {len(recs)} VCs.\n")
w("## Runs\n")
w("| variant | " + " | ".join(sorted({k for v in V for k in runs[v]})) + " |")
w("|---|" + "---:|" * len({k for v in V for k in runs[v]}))
for v in V:
    w(f"| {v} | " + " | ".join(str(runs[v][k]) for k in sorted({k for v in V for k in runs[v]})) + " |")
for v in V:
    if errors[v]:
        w(f"\nProver errors under {v} (runs that print each):\n")
        for e, c in errors[v].most_common(10):
            w(f"- {c}: `{e}`")
w("")

w("## Verdicts\n")
w(f"A VC is *proved* when it passes within {a.cap:g} s; *cap* means it ran out of time (or ran into the "
  f"limit); *failed* means the solver gave up within the limit; *missing* means the run reported no "
  f"result for it (it ended early).\n")
cats = ["proved", "failed", "cap", "missing"]
w(f"| {a.ref} \\ {a.alt} | " + " | ".join(cats) + " | total |")
w("|---|" + "---:|" * (len(cats) + 1))
for c0 in cats:
    row = [sum(1 for r in recs if r[f"{a.ref}_verdict"] == c0 and r[f"{a.alt}_verdict"] == c1) for c1 in cats]
    if sum(row):
        w(f"| {c0} | " + " | ".join(map(str, row)) + f" | {sum(row)} |")
w("")
w("| kind | programs | VCs | proved by both | only " + a.ref + " | only " + a.alt + " | neither | programs " + a.ref +
  " proves fully | of those, " + a.alt + " too |")
w("|---|---:|---:|---:|---:|---:|---:|---:|---:|")
for kind in sorted({r["kind"] for r in recs}) + ["all"]:
    rs = [r for r in recs if kind == "all" or r["kind"] == kind]
    p = lambda r, v: r[f"{v}_verdict"] == "proved"
    progs = collections.defaultdict(lambda: [True, True])
    for r in rs:
        progs[program(r["job"])][0] &= p(r, a.ref)
        progs[program(r["job"])][1] &= p(r, a.alt)
    full = [x for x in progs.values() if x[0]]
    w(f"| {kind} | {len(progs)} | {len(rs)} | {sum(p(r, a.ref) and p(r, a.alt) for r in rs)} | "
      f"{sum(p(r, a.ref) and not p(r, a.alt) for r in rs)} | {sum(p(r, a.alt) and not p(r, a.ref) for r in rs)} | "
      f"{sum(not p(r, a.ref) and not p(r, a.alt) for r in rs)} | {len(full)} | {sum(x[1] for x in full)} |")
w("")

both = [r for r in recs if r[f"{a.ref}_verdict"] == "proved" and r[f"{a.alt}_verdict"] == "proved"]
w("## Time on the VCs both prove\n")
w(f"{a.alt}'s time over {a.ref}'s; per program averages each program's own geomean. Intervals resample programs.\n")
w("| kind | VCs | total | geomean over VCs | per program | " + a.alt + " faster |")
w("|---|---:|---|---|---|---:|")
for kind in sorted({r["kind"] for r in both}) + ["all"]:
    rs = [r for r in both if kind == "all" or r["kind"] == kind]
    tot, gv, gp = ratio_stats(rs)
    faster = sum(r[a.alt][1] < r[a.ref][1] for r in rs)
    w(f"| {kind} | {len(rs)} | {tot} | {gv} | {gp} | {faster / len(rs):.0%} |" if rs else f"| {kind} | 0 | | | | |")
w("")
ref_proved = [r for r in recs if r[f"{a.ref}_verdict"] == "proved"]
w(f"Of the {len(ref_proved)} VCs {a.ref} proves, the share each variant proves within a given time:\n")
w("| within | " + " | ".join(V) + " |")
w("|---|---:|---:|")
for t in (1, 5, 10, 30, a.cap):
    w(f"| {t:g} s | " + " | ".join(
        f"{sum(1 for r in ref_proved if r[v] and r[v][0] == 'Passed' and r[v][1] <= t) / max(len(ref_proved), 1):.1%}" for v in V) + " |")
w("")

only_alt = [r for r in recs if r[f"{a.alt}_verdict"] == "proved" and r[f"{a.ref}_verdict"] != "proved"]
w(f"## VCs only {a.alt} proves ({len(only_alt)})\n")
w(f"A VC that {a.ref} *fails* quickly and {a.alt} proves deserves a look: in a test that expects an error there, "
  f"it would mean that {a.alt} proves something false.\n")
w(f"| job | VC | {a.ref} | {a.alt} |")
w("|---|---|---|---|")
for r in sorted(only_alt, key=lambda r: (r[f'{a.ref}_verdict'], r["job"]))[:60]:
    w(f"| {r['job']} | {r['vc']} | {r[f'{a.ref}_verdict']} {r[a.ref][1] if r[a.ref] else 0:.1f} s | {r[a.alt][1]:.1f} s |")
w("")

only_ref = [r for r in recs if r[f"{a.ref}_verdict"] == "proved" and r[f"{a.alt}_verdict"] != "proved"]
w(f"## VCs only {a.ref} proves ({len(only_ref)}), by how {a.alt} ends\n")
w(f"| {a.alt} | VCs | median {a.ref} time | programs |")
w("|---|---:|---:|---:|")
for c in ("failed", "cap", "missing"):
    rs = [r for r in only_ref if r[f"{a.alt}_verdict"] == c]
    if rs:
        w(f"| {c} | {len(rs)} | {st.median(r[a.ref][1] for r in rs):.2f} s | {len({program(r['job']) for r in rs})} |")
w("")
w(f"Programs with the most such VCs:\n")
for job, n in collections.Counter(program(r["job"]) for r in only_ref).most_common(15):
    w(f"- {job}: {n}")
w("")
open(a.report, "w").write("\n".join(o) + "\n")

if a.vcs:
    with open(a.vcs, "w", newline="") as fh:
        cw = csv.writer(fh)
        cw.writerow(["job", "kind", "vc", "k"] + [f"{v}_{x}" for v in V for x in ("outcome", "seconds", "verdict")])
        for r in recs:
            cw.writerow([r["job"], r["kind"], r["vc"], r["k"]] + [x for v in V for x in (
                (r[v][0] if r[v] else ""), (f"{r[v][1]:.3f}" if r[v] else ""), r[f"{v}_verdict"])])
print(f"{len(data)} jobs, {len(recs)} VCs -> {a.report}")
