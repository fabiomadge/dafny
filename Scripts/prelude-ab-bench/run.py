#!/usr/bin/env python3
"""run.py <jobs.json> <outdir> [--preludes master,pr,placebo] [--seeds 0,1,2,3,4] [--workers 28] [--solver z3]
          [--variants variants.json] [--time-limit 300]

Verifies every job under every prelude and random seed, one `dafny verify` per run, writing
one CSV of per-VC results per run. Seed 0 is Dafny's default; any other seed has Boogie rename
variables, reorder declarations and reseed the solver. Existing CSVs are kept, so an
interrupted run resumes.

With --variants, each name in --preludes is a variant instead: a JSON object maps it to its own
"dll" (the Dafny build), "solver", "solver_options" (each passed as --solver-option) and, optionally,
"prelude" (default: the build's own). A job's variants run next to each other, under the same load.

(`dafny measure-complexity --mutations` would be the natural tool, but it crashes with Boogie
type errors on programs with key-expression map comprehensions, e.g. dafny0/Maps.dfy.)
"""
import argparse, concurrent.futures as cf, hashlib, json, os, subprocess, time
from corpus import run_limit

HERE = os.path.dirname(os.path.abspath(__file__))
DFY = f"{HERE}/dafny.sh"
HEADER = "TestResult.DisplayName,TestResult.Outcome,TestResult.Duration,TestResult.ResourceCount\n"

ap = argparse.ArgumentParser()
ap.add_argument("jobs"); ap.add_argument("outdir")
ap.add_argument("--preludes", default="master,pr,placebo")
ap.add_argument("--prelude-dir", default=f"{HERE}/preludes", help="where <prelude>.bpl is")
ap.add_argument("--seeds", default="0,1,2,3,4")
ap.add_argument("--workers", type=int, default=28)
ap.add_argument("--resource-limit", default="500e6")
ap.add_argument("--solver", default=None, help="SMT solver binary (default: the z3 next to Dafny)")
ap.add_argument("--run-timeout", type=float, default=3600, help="seconds before a whole dafny run is killed")
ap.add_argument("--variants", default=None, help="JSON: variant name -> dll, solver, solver_options, prelude")
ap.add_argument("--time-limit", type=int, default=300, help="--verification-time-limit, in seconds")
ap.add_argument("--solver-log-root", default=None,
                help="log each run's queries to <root>/<run id>/@PROC@.smt2; <root>/index.json maps run ids to runs. "
                     "Keep <root> short: Boogie shortens a log's name once its path reaches 180 characters")
a = ap.parse_args()
variants = json.load(open(a.variants)) if a.variants else None
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
if a.solver_log_root:
    os.makedirs(a.solver_log_root, exist_ok=True)
    index_path = os.path.join(a.solver_log_root, "index.json")
    index = json.load(open(index_path)) if os.path.exists(index_path) else {}
    index.update({hashlib.sha1(stem.encode()).hexdigest()[:12]: {"job": j["id"], "variant": p, "seed": s}
                  for j, p, s, stem in todo})
    json.dump(index, open(index_path, "w"), indent=0)


def run(item):
    j, p, s, stem = item
    if os.path.exists(stem + ".csv"):
        return stem, "cached", 0.0
    v = variants[p] if variants else {"prelude": os.path.join(a.prelude_dir, f"{p}.bpl"), "solver": a.solver}
    cmd = ["bash", DFY, "verify"] + (["--prelude", v["prelude"]] if v.get("prelude") else []) + [
           f"--resource-limit:{run_limit(j, a.resource_limit)}", f"--verification-time-limit:{a.time_limit}", "--cores:2",
           "--log-format", f"csv;LogFileName={stem}.csv.tmp"]
    if s:
        cmd += ["--boogie", f"/randomSeed:{s}"]
    if v.get("solver"):
        cmd += ["--solver-path", v["solver"]]
    for o in v.get("solver_options", []):
        cmd += ["--solver-option", o]
    if a.solver_log_root:
        d = os.path.join(a.solver_log_root, hashlib.sha1(stem.encode()).hexdigest()[:12])
        os.makedirs(d, exist_ok=True)
        cmd += ["--solver-log", os.path.join(d, "@PROC@.smt2")]
    cmd += j["args"]
    env = dict(os.environ, DAFNY_DLL=v["dll"]) if v.get("dll") else None
    t0 = time.time()
    try:
        r = subprocess.run(cmd, cwd=j["cwd"], capture_output=True, text=True, timeout=a.run_timeout, env=env)
    except subprocess.TimeoutExpired as e:  # Dafny can hang; a stuck run must not hold its worker
        r = subprocess.CompletedProcess(cmd, "timeout", e.stdout or "", e.stderr or "")
        r.stdout = r.stdout if isinstance(r.stdout, str) else r.stdout.decode(errors="replace")
        r.stderr = r.stderr if isinstance(r.stderr, str) else r.stderr.decode(errors="replace")
    dt = time.time() - t0
    with open(stem + ".log", "w") as fh:
        fh.write((f"DAFNY_DLL={env['DAFNY_DLL']} " if env else "") + " ".join(cmd) +
                 f"\nexit={r.returncode} wall={dt:.1f}s\n--- stdout\n{r.stdout[-20000:]}\n--- stderr\n{r.stderr[-20000:]}")
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
