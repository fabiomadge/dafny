#!/usr/bin/env python3
"""run.py <jobs.json> <outdir> [--preludes master,pr,placebo] [--seeds 0,1,2,3,4] [--workers 28] [--solver z3]

Verifies every job under every prelude and random seed, one `dafny verify` per run, writing
one CSV of per-VC results per run. Seed 0 is Dafny's default; any other seed has Boogie rename
variables, reorder declarations and reseed the solver. Existing CSVs are kept, so an
interrupted run resumes.

(`dafny measure-complexity --mutations` would be the natural tool, but it crashes with Boogie
type errors on programs with key-expression map comprehensions, e.g. dafny0/Maps.dfy.)
"""
import argparse, concurrent.futures as cf, json, os, subprocess, time

HERE = os.path.dirname(os.path.abspath(__file__))
DFY = f"{HERE}/dafny.sh"
HEADER = "TestResult.DisplayName,TestResult.Outcome,TestResult.Duration,TestResult.ResourceCount\n"

ap = argparse.ArgumentParser()
ap.add_argument("jobs"); ap.add_argument("outdir")
ap.add_argument("--preludes", default="master,pr,placebo")
ap.add_argument("--seeds", default="0,1,2,3,4")
ap.add_argument("--workers", type=int, default=28)
ap.add_argument("--resource-limit", default="500e6")
ap.add_argument("--solver", default=None, help="SMT solver binary (default: the z3 next to Dafny)")
a = ap.parse_args()
a.outdir = os.path.abspath(a.outdir)  # dafny runs in each job's directory
os.makedirs(a.outdir, exist_ok=True)
jobs = json.load(open(a.jobs))
todo = []
for j in jobs:
    for p in a.preludes.split(","):
        for s in a.seeds.split(","):
            stem = j["id"].replace("/", "__").replace(":", "--") + f"@{p}@{s}"
            todo.append((j, p, int(s), os.path.join(a.outdir, stem)))
# Longest jobs first keeps the pool busy at the end.
todo.sort(key=lambda t: ("UnionFind" not in t[0]["id"], t[0]["kind"] != "std"))


def run(item):
    j, p, s, stem = item
    if os.path.exists(stem + ".csv"):
        return stem, "cached", 0.0
    cmd = ["bash", DFY, "verify", "--prelude", f"{HERE}/preludes/{p}.bpl",
           f"--resource-limit:{a.resource_limit}", "--verification-time-limit:300", "--cores:2",
           "--log-format", f"csv;LogFileName={stem}.csv.tmp"]
    if s:
        cmd += ["--boogie", f"/randomSeed:{s}"]
    if a.solver:
        cmd += ["--solver-path", a.solver]
    cmd += j["args"]
    t0 = time.time()
    r = subprocess.run(cmd, cwd=j["cwd"], capture_output=True, text=True)
    dt = time.time() - t0
    with open(stem + ".log", "w") as fh:
        fh.write(" ".join(cmd) + f"\nexit={r.returncode} wall={dt:.1f}s\n--- stdout\n{r.stdout[-20000:]}\n--- stderr\n{r.stderr[-20000:]}")
    if os.path.exists(stem + ".csv.tmp"):
        os.replace(stem + ".csv.tmp", stem + ".csv")
        return stem, f"exit={r.returncode}", dt
    open(stem + ".csv", "w").write(HEADER)  # nothing verified (e.g. a resolution-error test)
    return stem, f"no-csv exit={r.returncode}", dt


t0 = time.time()
with cf.ThreadPoolExecutor(a.workers) as ex:
    for i, (stem, status, dt) in enumerate(ex.map(run, todo), 1):
        if status != "cached":
            print(f"[{i}/{len(todo)} {time.time()-t0:6.0f}s] {os.path.basename(stem)} {status} {dt:.0f}s", flush=True)
print(f"done in {time.time()-t0:.0f}s")
