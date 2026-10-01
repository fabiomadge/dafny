#!/usr/bin/env python3
"""screen.py <jobs.json> <outdir> [a b [aa]]: which programs does a prelude change reach?

Reads run.py output at seed 0 for two preludes (default master and pr). A VC is reached when
its resource counts differ; every other VC got identical SMT. Lists the reached programs, whether
they contain a map/imap comprehension themselves, and verdict changes at each job's limit. With
aa, a second run of a's prelude (such as master2), it also marks the jobs whose VCs differ between
two runs of the same input: their reach is no evidence."""
import collections, csv, glob, json, os, re, sys

jobs_path, outdir = sys.argv[1:3]
a, b = (sys.argv[3:5] if len(sys.argv) > 4 else ("master", "pr"))
aa = sys.argv[5] if len(sys.argv) > 5 else None
jobs = {j["id"]: j for j in json.load(open(jobs_path))}
esc = {j.replace("/", "__").replace(":", "--"): j for j in jobs}
COMP = re.compile(r"\bi?map\s+[A-Za-z_][\w'?]*\s*(?::|<-|\||,)")

res = collections.defaultdict(dict)
for path in glob.glob(os.path.join(outdir, "*.csv")):
    stem, p, s = os.path.basename(path)[:-4].rsplit("@", 2)
    if p in (a, b, aa) and s == "0" and stem in esc:
        res[esc[stem]][p] = {r["TestResult.DisplayName"]: (r["TestResult.Outcome"], int(r["TestResult.ResourceCount"]))
                             for r in csv.DictReader(open(path))}

def has_comp(job):
    files = [os.path.join(jobs[job]["cwd"], x) for x in jobs[job]["args"] if x.endswith(".dfy") and not x.startswith("-")]
    f = [x for x in jobs[job]["args"] if x.startswith("--filter-position=")]
    if f:  # a project: the filtered file
        files = [os.path.join(jobs[job]["cwd"], f[0].split("=", 1)[1])]
    return any(COMP.search(re.sub(r"//[^\n]*", "", open(x, encoding="utf-8-sig", errors="replace").read())) for x in files)

done = [j for j in res if a in res[j] and b in res[j]]
reached, noisy, total_vcs, flips = {}, {}, 0, []
differ = lambda x, y: [n for n in set(x) | set(y) if x.get(n, (None, -1))[1] != y.get(n, (None, -1))[1]]
for j in done:
    ra, rb = res[j][a], res[j][b]
    total_vcs += len(ra)
    if differ(ra, rb):
        reached[j] = differ(ra, rb)
    if aa in res[j] and differ(ra, res[j][aa]):
        noisy[j] = differ(ra, res[j][aa])
    lim = jobs[j]["limit"]
    ok = lambda r, n: n in r and r[n][0] == "Passed" and r[n][1] <= lim
    flips += [(j, n) for n in set(ra) | set(rb) if ok(ra, n) != ok(rb, n)]

print(f"{len(done)} jobs screened ({len(jobs) - len(done)} not run), {total_vcs} VCs; "
      f"{sum(map(len, reached.values()))} VCs in {len(reached)} jobs reached by {a} -> {b}")
for j in sorted(reached):
    notes = ("" if has_comp(j) else "   (no comprehension in its own source)") + \
            (f"   (A/A: {len(noisy[j])} VCs differ too)" if j in noisy else "")
    print(f"  {j}: {len(reached[j])} VCs{notes}")
if aa:
    print(f"{len(noisy)} jobs differ between two runs of {a} ({a} vs {aa}); "
          f"{len(set(reached) - set(noisy))} of the reached jobs do not")
print("verdict changes at each job's limit:", flips or "none")
