#!/usr/bin/env python3
"""corpus.py <jobs.json> [lit] [std] [synth] [unionfind]: write the benchmark's job list.

One job is one program (or project file) under one resolver configuration:
  lit       - every LitTest program containing a map/imap comprehension (the only construct the
              translator encodes with Map#Glue/IMap#Glue), with the flags of its first RUN line,
              under the refreshed and the legacy resolver unless the RUN line pins one
  std       - the standard-library files that contain comprehensions, in project mode
  synth     - the programs synth.py generated
  unionfind - dafny4/UnionFind.dfy as on --master (Main not isolated), under both resolvers
"""
import json, os, re, shlex, subprocess, sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.normpath(os.path.join(HERE, "..", ".."))
LIT = f"{ROOT}/Source/IntegrationTests/TestFiles/LitTests/LitTest"
STD = f"{ROOT}/Source/DafnyStandardLibraries/src/Std"

COMP = re.compile(r"\bi?map\s+[A-Za-z_][\w'?]*\s*(?::|<-|\||,)")
RUN = re.compile(r"^//\s*RUN:\s*(.*)$", re.M)

# The lit harness's verify flags (Source/IntegrationTests/LitTests.cs), minus the limits, which
# run.py sets.
LIT_DEFAULTS = ["--type-system-refresh", "--general-traits=datatype", "--general-newtypes",
                "--use-basename-for-filename", "--show-snippets:false", "--standard-libraries:false"]
LEGACY = ["--type-system-refresh=false", "--general-newtypes=false"]
# RUN-line flags that only the harness or a compiler understands
DROP = ("--refresh-exit-code", "--expect-exit-code", "--target", "-t:", "--spill-translation",
        "--output", "--include-runtime", "--no-verify", "--compile-verbose", "--build")
LEGACY_MAP = {"/deprecation:0": "--allow-deprecation", "/autoTriggers:0": "--manual-triggers",
              "/typeSystemRefresh:0": "--type-system-refresh=false",
              "/generalNewtypes:0": "--general-newtypes=false"}
SKIP_STYLES = {"tobinary", "diff", "NORUN"}  # not a Dafny verification run


def has_comprehension(path):
    return COMP.search(re.sub(r"//[^\n]*", "", open(path, encoding="utf-8-sig", errors="replace").read()))


def run_flags(line):
    toks = shlex.split(line.replace('"%s"', "").replace("%s", ""), posix=True)
    if any(t.startswith("%testDafnyForEach") for t in toks):
        toks = toks[toks.index("--") + 1:] if "--" in toks else []
    flags = []
    for t in toks:
        if t in LEGACY_MAP:
            flags.append(LEGACY_MAP[t])
        elif t.startswith("--") and not t.startswith(DROP):
            flags.append(t)
        elif t in (">", ">>", "|"):
            break
    return flags


def resolver_jobs(jid, path, flags, kind="lit", limit=50e6, both=True):
    pinned = any(t.startswith("--type-system-refresh") for t in flags)
    configs = [("pinned", [])] if pinned else [("refresh", []), ("legacy", LEGACY)][:2 if both else 1]
    return [{"id": f"{jid}:{res}", "kind": kind, "cwd": os.path.dirname(path),
             "args": LIT_DEFAULTS + extra + flags + [path], "limit": limit} for res, extra in configs]


def lit_jobs(every=False):
    """Programs with a comprehension under both resolvers; with every, all programs under lit's default resolver."""
    jobs = []
    for d, _, fs in os.walk(LIT):
        for f in sorted(fs):
            p = os.path.join(d, f)
            if not f.endswith(".dfy") or not (every or has_comprehension(p)):
                continue
            runs = RUN.findall(open(p, encoding="utf-8-sig", errors="replace").read())
            first = runs[0] if runs else ""
            m = re.search(r"%([\w-]+)", first)
            if (m.group(1) if m else "NORUN") in SKIP_STYLES:
                continue
            jobs += resolver_jobs(f"lit/{os.path.relpath(p, LIT)}", p, run_flags(first), both=not every)
    return jobs


def std_jobs(every=False):
    jobs = []
    for d, _, fs in os.walk(STD):
        for f in sorted(fs):
            p = os.path.join(d, f)
            if f.endswith(".dfy") and "TargetSpecific" not in p and (every or has_comprehension(p)):
                rel = os.path.relpath(p, STD)
                jobs.append({"id": f"std/{rel}", "kind": "std", "cwd": STD,
                             "args": [f"{STD}/dfyconfig.toml", f"--filter-position={rel}"], "limit": 5e6})
    return jobs


def synth_jobs():
    d = os.path.join(HERE, "synth")
    return [{"id": f"synth/{f}", "kind": "synth", "cwd": d, "args": LIT_DEFAULTS + [os.path.join(d, f)],
             "limit": 50e6} for f in (sorted(os.listdir(d)) if os.path.isdir(d) else []) if f.endswith(".dfy")]


def unionfind_jobs(ref="origin/master"):
    rel = "Source/IntegrationTests/TestFiles/LitTests/LitTest/dafny4/UnionFind.dfy"
    os.makedirs(f"{HERE}/work", exist_ok=True)
    path = f"{HERE}/work/UnionFind-noiso.dfy"
    src = subprocess.run(["git", "-C", ROOT, "show", f"{ref}:{rel}"], check=True, capture_output=True, text=True).stdout
    open(path, "w").write(src)
    return resolver_jobs("lit/dafny4/UnionFind-noiso.dfy", path, ["--relax-definite-assignment"])


if __name__ == "__main__":
    kinds = sys.argv[2:] or ["lit", "std", "synth", "unionfind"]
    jobs = []
    if "lit" in kinds: jobs += lit_jobs()
    if "std" in kinds: jobs += std_jobs()
    if "litall" in kinds: jobs += lit_jobs(every=True)  # for a seed-0 screen of what a change reaches
    if "stdall" in kinds: jobs += std_jobs(every=True)
    if "synth" in kinds: jobs += synth_jobs()
    if "unionfind" in kinds: jobs += unionfind_jobs()
    json.dump(jobs, open(sys.argv[1], "w"), indent=1)
    print(len(jobs), "jobs")
