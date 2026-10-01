#!/usr/bin/env python3
"""classify.py <jobs.json> <outdir> [--preludes master,pr] [--workers 16] [--marker 'Map#Glue']

Which VCs does a prelude change reach? Re-verifies each job once per prelude with one solver log
per Boogie procedure and split (`--solver-log <dir>/@PROC@.smt2`), maps each CSV row to its log,
and labels the VC:
  marker   - its SMT names the changed functions, so the change is in its background theory
  class    - unchanged (identical SMT), reordered (the same lines in another order: a pure
             perturbation) or content (different SMT)
Writes <outdir>/classes.csv. A cost change in a VC without the marker is a perturbation."""
import argparse, collections, concurrent.futures as cf, csv, glob, json, os, re, subprocess, tempfile
from corpus import run_limit

HERE = os.path.dirname(os.path.abspath(__file__))
ap = argparse.ArgumentParser()
ap.add_argument("jobs"); ap.add_argument("outdir")
ap.add_argument("--preludes", default="master,pr")
ap.add_argument("--workers", type=int, default=16)
ap.add_argument("--marker", default="Map#Glue")
ap.add_argument("--solver", default=None, help="SMT solver binary (default: the z3 next to Dafny)")
# Boogie shortens a log name once the whole log path reaches 180 characters
# (Helpers.SubstituteAtPROC), and a shortened name no longer says which VC it is.
ap.add_argument("--log-root", default=os.path.join(tempfile.gettempdir(), "pab"),
                help="short directory for the solver logs")
a = ap.parse_args()
a.outdir = os.path.abspath(a.outdir)
pa, pb = a.preludes.split(",")

ROW = re.compile(r"(.*) \((correctness|well-formedness)\)(?: \(assertion batch (\d+)\))?$")
LOG = re.compile(r"(Impl|CheckWellFormed|CheckWellformed)__(.*)_split(\d+)\.smt2$")
# Boogie shortens long names to a prefix and a counter, whose order can differ between runs
SHORT = re.compile(r"(Impl|CheckWellFormed|CheckWellformed)__(.*)-n\d+\.smt2$")
norm = lambda s: re.sub(r"[^A-Za-z0-9]", "", s)


def row_key(name):
    m = ROW.match(name)
    if not m:
        return None
    base, kind, batch = m.groups()
    base = base.replace("?", "q").replace("'", "k").replace("#", "h")
    return (kind, norm(base), int(batch) - 1 if batch else 0)


def log_key(fname):
    m = LOG.match(fname)
    if not m:
        return None
    prefix, name, split = m.groups()
    name = name[len("_module."):] if name.startswith("_module.") else name  # the default module is unnamed in display names
    name = re.sub(r"(^|\.)__default\.", r"\1", name)  # so is the default class
    name = re.sub(r"(?<=[A-Za-z0-9])_m(?=[A-Za-z0-9])", ".", name)  # nested module paths are joined by _m
    return ("correctness" if prefix == "Impl" else "well-formedness", norm(name), int(split))


def run(job, p, index):
    d = os.path.join(a.outdir, job["id"].replace("/", "__").replace(":", "--"), p)
    logs_dir = os.path.join(a.log_root, f"{index}{'ab'[p == pb]}")
    if not os.path.exists(d + "/rows.csv") or not os.path.isdir(logs_dir):
        os.makedirs(d, exist_ok=True)
        os.makedirs(logs_dir, exist_ok=True)
        cmd = ["bash", f"{HERE}/dafny.sh", "verify", "--prelude", f"{HERE}/preludes/{p}.bpl", "--cores:2",
               f"--resource-limit:{run_limit(job, 500e6)}", "--verification-time-limit:300", "--boogie", "/normalizeNames:0",
               "--solver-log", logs_dir + "/@PROC@.smt2", "--log-format", f"csv;LogFileName={d}/rows.csv"] + \
              (["--solver-path", a.solver] if a.solver else []) + job["args"]
        subprocess.run(cmd, cwd=job["cwd"], capture_output=True, timeout=7200)
    rows = [r["TestResult.DisplayName"] for r in csv.DictReader(open(d + "/rows.csv"))] if os.path.exists(d + "/rows.csv") else []
    logs, short = {}, collections.defaultdict(list)
    for f in glob.glob(logs_dir + "/*.smt2"):
        content = [l for l in open(f, errors="replace") if not l.startswith(";")]
        k, m = log_key(os.path.basename(f)), SHORT.match(os.path.basename(f))
        if k:
            logs[k] = content
        elif m:
            kind = "correctness" if m.group(1) == "Impl" else "well-formedness"
            short[(kind, log_key(f"{m.group(1)}__{m.group(2)}_split0.smt2")[1])].append(content)
    return rows, logs, short


def label(xs, ys):
    """Compare the logs of one VC (or of a group of VCs, as multisets) under the two preludes."""
    if sorted(map(tuple, xs)) == sorted(map(tuple, ys)):
        return "unchanged"
    return "reordered" if sorted(tuple(sorted(x)) for x in xs) == sorted(tuple(sorted(y)) for y in ys) else "content"


def classify(item):
    index, job = item
    (ra, la, sa), (rb, lb, sb) = run(job, pa, index), run(job, pb, index)
    out = []
    for name in ra:
        k = row_key(name)
        x, y = la.get(k), lb.get(k)
        if x is not None and y is not None:
            out.append((job["id"], name, label([x], [y]), any(a.marker in l for l in x + y), f"{k[0]}:{k[1]}:{k[2]}"))
            continue
        # a shortened name: the group of logs whose prefix this name extends, if the group agrees
        groups = [g for g in set(sa) | set(sb) if k and g[0] == k[0] and k[1].startswith(g[1])]
        if not groups:
            out.append((job["id"], name, "unmapped", "", ""))
            continue
        g = max(groups, key=lambda g: len(g[1]))
        marks = {any(a.marker in l for l in c) for c in sa.get(g, []) + sb.get(g, [])}
        # which log of the group is this VC's is unknown, so only a unanimous marker is kept
        out.append((job["id"], name, "group", marks.pop() if len(marks) == 1 else "mixed", f"{g[0]}:{g[1]}*"))
    return out


jobs = json.load(open(a.jobs))
with cf.ThreadPoolExecutor(a.workers) as ex:
    results = [r for rs in ex.map(classify, enumerate(jobs)) for r in rs]
with open(os.path.join(a.outdir, "classes.csv"), "w", newline="") as fh:
    w = csv.writer(fh, lineterminator="\n")
    w.writerow(["job", "vc", "class", "marker", "key"])
    w.writerows(results)
c = collections.Counter((r[2], r[3]) for r in results)
print(f"{len(results)} VCs:", ", ".join(f"{k[0]}{' +' + a.marker if k[1] is True else ''}: {v}" for k, v in sorted(c.items(), key=str)))
