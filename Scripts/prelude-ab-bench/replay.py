#!/usr/bin/env python3
"""replay.py <log-root> <outdir> --solver NAME=KIND:BINARY[:ARGS]:SOURCE ... [--cpu 60] [--mem-gb 8] [--workers 32]

Replays the queries that run.py --solver-log-root logged, one solver process per query, and measures each
process's CPU time (user + system, from wait4). CPU time is not free of the machine's load (on a host at
load 35 to 60 of 64 cores, short queries took 2.2 (Z3) and 1.45 (cvc5) times their CPU time at load 20),
and it includes the process's startup, which Dafny pays once per solver process. To compare solvers' work,
pass --perf, which also records user-space instructions and cycles (perf stat) and, because cvc5's
statistics cost it some 10^8 instructions, records no resource units; subtract a --part startup replay.
A query is its log's text up to the first (check-sat): the VC's own check, without the
follow-up queries Boogie sends after a failure. KIND is z3 or cvc5; ARGS are extra solver arguments, split
on commas; SOURCE names the logged variant whose queries this solver gets. Each process runs under
--cpu seconds of CPU time and --mem-gb of address space; a query killed by the CPU limit counts as timed out.

Writes run.py's per-run CSVs to <outdir> (DisplayName: the query's log name; Duration: CPU time;
ResourceCount: Z3's rlimit count or cvc5's resource units, which do not compare across solvers), so that
solvers.py compares the replays, and replays.jsonl with every replay's details. Only queries logged for
every SOURCE are replayed, and each job's replays alternate between the solvers, query by query.
"""
import argparse, collections, concurrent.futures as cf, json, os, re, resource, signal, subprocess, tempfile, threading, time

ap = argparse.ArgumentParser()
ap.add_argument("root"); ap.add_argument("outdir")
ap.add_argument("--solver", action="append", required=True)
ap.add_argument("--cpu", type=int, default=60)
ap.add_argument("--mem-gb", type=float, default=8)
ap.add_argument("--workers", type=int, default=32)
ap.add_argument("--jobs", default=None, help="only these job ids (a JSON job list, as for run.py)")
ap.add_argument("--only", default=None, help='only these queries: a JSON list of {"job": ..., "query": ...}')
ap.add_argument("--logged", default=None,
                help="run.py's output directory of the logging run: replay a job only once its runs there are done")
ap.add_argument("--perf", action="store_true", help="also count user-space instructions and cycles (perf stat)")
ap.add_argument("--part", choices=("full", "prelude", "startup"), default="full",
                help="replay the query, only its prelude (the text before the VC's first push), or only (exit)")
a = ap.parse_args()
only_q = collections.defaultdict(set)
for x in json.load(open(a.only)) if a.only else []:
    only_q[x["job"]].add(x["query"] + ".smt2")
os.makedirs(a.outdir, exist_ok=True)

solvers = {}
for spec in a.solver:
    name, rest = spec.split("=", 1)
    kind, binary, args, source = rest.split(":", 3)
    solvers[name] = {"kind": kind, "binary": binary, "args": [x for x in args.split(",") if x], "source": source}
BASE = {"z3": ["-smt2", "-in"],
        "cvc5": ["--lang=smt", "--no-strict-parsing", "--no-condense-function-values", "--incremental", "--produce-models"]}
TAIL = {"z3": "(get-info :rlimit)\n(exit)\n", "cvc5": "(get-info :all-statistics)\n(exit)\n"}
RU = {"z3": re.compile(r"\(:rlimit (\d+)\)"), "cvc5": re.compile(r'"resource::resourceUnitsUsed" (\d+)')}
LIMIT_OPT = re.compile(r"^\(set-option :(timeout|rlimit) \d+\)\n", re.M)

index = json.load(open(os.path.join(a.root, "index.json")))
only = {j["id"] for j in json.load(open(a.jobs))} if a.jobs else None
runs = collections.defaultdict(dict)  # (job, seed) -> variant -> log dir
for rid, r in index.items():
    d = os.path.join(a.root, rid)
    if os.path.isdir(d) and (only is None or r["job"] in only):
        runs[(r["job"], r["seed"])][r["variant"]] = d


def query(path, kind):
    text = open(path, errors="replace").read()
    i = text.find("(check-sat)")
    if i < 0:
        return None
    if a.part == "startup":
        return "(exit)\n"
    if a.part == "prelude":
        p = text.find("(push 1)")
        return LIMIT_OPT.sub("", text[:p]) + "(exit)\n" if 0 <= p < i else None
    text = text[:i + len("(check-sat)")] + "\n"
    if kind == "z3":
        text = LIMIT_OPT.sub("", text)  # the logging run's limits; --cpu limits the replay
    # cvc5 reports resource units only with all its statistics, which cost it some 10^8 instructions
    return text + ("(exit)\n" if a.perf else TAIL[kind])


def limits():
    resource.setrlimit(resource.RLIMIT_CPU, (a.cpu, a.cpu + 2))
    mem = int(a.mem_gb * 2 ** 30)
    resource.setrlimit(resource.RLIMIT_AS, (mem, mem))
    resource.setrlimit(resource.RLIMIT_CORE, (0, 0))


def replay(text, s):
    cmd = [s["binary"]] + BASE[s["kind"]] + s["args"]
    if a.perf:
        fd, stat = tempfile.mkstemp(dir=a.outdir, suffix=".perf"); os.close(fd)
        cmd = ["perf", "stat", "-x,", "-o", stat, "-e", "instructions:u,cycles:u", "--"] + cmd
    p = subprocess.Popen(cmd, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, preexec_fn=limits)
    t0 = time.time()
    err = []
    def feed():
        try:
            p.stdin.write(text.encode()); p.stdin.close()
        except BrokenPipeError:
            pass
    th = threading.Thread(target=feed); th.start()
    te = threading.Thread(target=lambda: err.append(p.stderr.read().decode(errors="replace"))); te.start()
    out = p.stdout.read().decode(errors="replace")
    th.join(); te.join()
    _, status, ru = os.wait4(p.pid, 0)
    p.returncode = 0  # reaped above; keep Popen from waiting again
    wall = time.time() - t0
    cpu = ru.ru_utime + ru.ru_stime
    answer = next((l.strip() for l in out.splitlines() if l.strip() in ("sat", "unsat", "unknown")), None)
    # cvc5 catches the CPU limit's SIGXCPU, prints "interrupted by timeout" and aborts (signal 6); its
    # CPU time as wait4 reports it can then be a few seconds under the limit
    if os.WIFSIGNALED(status) and ("interrupted by timeout" in err[0] or cpu >= 0.9 * a.cpu):
        answer = "cap"
    elif answer is None:
        answer = f"error: {out.strip()[:100]}" if os.WIFEXITED(status) else f"signal {os.WTERMSIG(status)}"
    m = RU[s["kind"]].search(out)
    counts = {}
    if a.perf:
        for line in open(stat):
            f = line.strip().split(",")
            if len(f) > 2 and f[2] in ("instructions:u", "cycles:u"):
                counts[f[2].split(":")[0]] = int(f[0]) if f[0].isdigit() else None
        os.remove(stat)
    return {"answer": answer, "cpu": round(cpu, 4), "wall": round(wall, 3), "ru": int(m.group(1)) if m else 0,
            "maxrss_mb": ru.ru_maxrss // 1024, **counts}


def dur(sec):
    h, rem = divmod(sec, 3600)
    m, s = divmod(rem, 60)
    return f"{int(h):02d}:{int(m):02d}:{s:010.7f}"


lock = threading.Lock()
jsonl = open(os.path.join(a.outdir, "replays.jsonl"), "a")


def do_job(key):
    job, seed = key
    stem = job.replace("/", "__").replace(":", "--")
    outs = {n: os.path.join(a.outdir, f"{stem}@{n}@{seed}") for n in solvers}
    if all(os.path.exists(o + ".csv") for o in outs.values()):
        return job, "cached"
    dirs = runs[key]
    if not all(s["source"] in dirs for s in solvers.values()):
        return job, "missing logs"
    if a.logged and not all(os.path.exists(os.path.join(a.logged, f"{stem}@{s['source']}@{seed}.csv")) for s in solvers.values()):
        return job, "still logging"
    names = sorted(set.intersection(*(set(f for f in os.listdir(dirs[s["source"]]) if f.endswith(".smt2"))
                                      for s in solvers.values())))
    if a.only:
        names = [f for f in names if f in only_q.get(job, ())]
        if not names:
            return job, "not selected"
    rows = {n: [] for n in solvers}
    for f in names:
        for n, s in solvers.items():  # one query's replays back to back, so both see the same load
            text = query(os.path.join(dirs[s["source"]], f), s["kind"])
            if text is None:
                continue
            r = replay(text, s)
            rows[n].append((f[:-5], r))
            with lock:
                jsonl.write(json.dumps({"job": job, "seed": seed, "solver": n, "query": f[:-5], **r}) + "\n")
                jsonl.flush()
    for n, o in outs.items():
        with open(o + ".csv.tmp", "w") as fh:
            fh.write("TestResult.DisplayName,TestResult.Outcome,TestResult.Duration,TestResult.ResourceCount,RandomSeed\n")
            for q, r in rows[n]:
                outcome = "Passed" if r["answer"] == "unsat" else "TimedOut" if r["answer"] == "cap" else "Failed"
                fh.write(f"{q},{outcome},{dur(r['cpu'])},{r['ru']},{seed}\n")
        os.replace(o + ".csv.tmp", o + ".csv")
        open(o + ".log", "w").write(f"replay of {dirs[solvers[n]['source']]}\nexit=0\n")
    return job, f"{len(names)} queries"


t0 = time.time()
keys = sorted(runs)
with cf.ThreadPoolExecutor(a.workers) as ex:
    for i, (job, status) in enumerate(ex.map(do_job, keys), 1):
        if status != "cached":
            print(f"[{i}/{len(keys)} {time.time() - t0:6.0f}s] {job} {status}", flush=True)
print(f"done in {time.time() - t0:.0f}s")
