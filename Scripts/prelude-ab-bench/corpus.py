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
# RUN-line flags that only the harness or a compiler understands, or that write files (run.py sets
# its own log; a lit placeholder such as %t would otherwise name a file in the test's directory)
DROP = ("--refresh-exit-code", "--expect-exit-code", "--target", "-t:", "--spill-translation",
        "--output", "--include-runtime", "--no-verify", "--compile-verbose", "--build", "--log-format",
        "--solver-log", "--solver-path", "--verification-coverage-report", "--coverage-report",
        "--outer-module", "--test-assumptions")
PRINT = re.compile(r"^--[bdrs]?print([:=].*)?$")
LEGACY_MAP = {"/deprecation:0": "--allow-deprecation", "/autoTriggers:0": "--manual-triggers",
              "/typeSystemRefresh:0": "--type-system-refresh=false",
              "/generalNewtypes:0": "--general-newtypes=false"}
SKIP_STYLES = {"tobinary", "diff", "NORUN"}  # not a Dafny verification run
INCLUDE = re.compile(r'^\s*include\s+"([^"]+)"', re.M)
MULTIPLIER = re.compile(r"\{:timeLimitMultiplier\s+(\d+)\s*\}|@TimeLimitMultiplier\(\s*(\d+)\s*\)")


def has_comprehension(path):
    return COMP.search(re.sub(r"//[^\n]*", "", open(path, encoding="utf-8-sig", errors="replace").read()))


def valued_options():
    """The options of `dafny verify` that take a value, which a RUN line may give as the next token."""
    out = subprocess.run(["bash", f"{HERE}/dafny.sh", "verify", "--help"], capture_output=True, text=True).stdout
    return frozenset(re.findall(r"^\s+(?:-\w, )?(--[\w-]+)\s+<", out, re.M)) | {"--general-traits"}  # hidden from the help


def run_flags(line, src_dir, valued=frozenset()):
    toks = shlex.split(line.replace('"%s"', "").replace("%s", ""), posix=True)
    if any(t.startswith("%testDafnyForEach") for t in toks):
        toks = toks[toks.index("--") + 1:] if "--" in toks else []
    toks = [t.replace("%S", src_dir) for t in toks]  # lit's source directory, e.g. in --library=%S/...
    flags, i = [], 0
    while i < len(toks):
        t = toks[i]
        if t in (">", ">>", "|"):
            break
        takes_value = (t in valued or t == "--input") and i + 1 < len(toks) and toks[i + 1] not in (">", ">>", "|")
        value = toks[i + 1:i + 2] if takes_value else []
        i += 1 + len(value)
        if t in LEGACY_MAP:
            flags.append(LEGACY_MAP[t])
        elif t == "--input":  # `dafny run`'s further inputs; the others are a compiler's extern code
            flags += [v for v in value if v.endswith((".dfy", ".toml"))]
        elif t.startswith("--") and not t.startswith(DROP) and not PRINT.match(t) and "%" not in t + "".join(value):
            flags += [t] + value
    return flags


def sources(job):
    """The job's Dafny sources: its .dfy arguments (or a project's filtered file) and their includes."""
    todo = [t.split("=", 1)[1].rsplit(":", 1)[0] if t.startswith("--filter-position=") else t
            for t in job["args"] if t.endswith(".dfy") or t.startswith("--filter-position=")]
    seen = []
    while todo:
        f = os.path.normpath(os.path.join(job["cwd"], todo.pop()))
        if f in seen or not os.path.isfile(f):
            continue
        seen.append(f)
        todo += [os.path.join(os.path.dirname(f), i) for i in INCLUDE.findall(open(f, encoding="utf-8-sig", errors="replace").read())]
    return [(f, open(f, encoding="utf-8-sig", errors="replace").read()) for f in seen]


def run_limit(job, cap):
    """The resource limit a job can run under, at most cap: Dafny multiplies it by a declaration's
    time-limit multiplier into a 32-bit {:rlimit}, and aborts once that overflows."""
    worst = max([1] + [int(x or y) for _, text in sources(job) for x, y in MULTIPLIER.findall(text)])
    return int(min(float(cap), (2 ** 31 - 1) // worst))


DECL = re.compile(r"((?:@\w+(?:\([^)]*\))?\s*)*)\b(?:(?:ghost|static|opaque|twostate|least|greatest)\s+)*"
                  r"(?:lemma|method|function|predicate|constructor|iterator)\s+((?:\{:[^}]*\}\s*)*)([\w'?]+)")  # a Dafny name
TYPE = re.compile(r"\b(?:class|trait|datatype|codatatype|newtype|module)\s+(?:\{:[^}]*\}\s*)*([\w.]+)")
LIMIT = re.compile(r'@ResourceLimit\(\s*"([^"]+)"\s*\)|\{:resource_limit\s+"?([\d.eE+]+)"?\s*\}|\{:rlimit\s+(\d+)\s*\}'
                   r'|@TimeLimitMultiplier\(\s*(\d+)\s*\)|\{:timeLimitMultiplier\s+(\d+)\s*\}')


def declared_limits(job):
    """Per-declaration resource limits, keyed by (enclosing type or module, member) and by member:
    {:resource_limit N} and @ResourceLimit("N") give N, {:rlimit N} N * 1000, and a time-limit
    multiplier N times the job's limit. A member name with conflicting limits is left out."""
    by_pair, by_member = {}, {}
    for _, text in sources(job):
        types = [(m.start(), m.group(1).split(".")[-1]) for m in TYPE.finditer(text)]
        for m in DECL.finditer(text):
            found = LIMIT.findall(m.group(1) + " " + m.group(2))
            if not found:
                continue
            res, res2, rl, mul, mul2 = found[-1]
            limit = float(res or res2) if res or res2 else float(rl) * 1000 if rl else int(mul or mul2) * job["limit"]
            owner = max((t for t in types if t[0] < m.start()), default=(0, ""))[1]
            by_pair[(owner, m.group(3))] = limit
            by_member.setdefault(m.group(3), set()).add(limit)
    return by_pair, {k: v.pop() for k, v in by_member.items() if len(v) == 1}


def vc_limit(job, limits, vc):
    """The limit at which a VC's verdict is read: its declaration's own, else the job's."""
    name = vc.split(" (")[0].split(".")
    by_pair, by_member = limits
    if len(name) > 1 and (name[-2], name[-1]) in by_pair:
        return by_pair[(name[-2], name[-1])]
    return by_member.get(name[-1], job["limit"])


def resolver_jobs(jid, path, flags, kind="lit", limit=50e6, both=True):
    pinned = any(t.startswith("--type-system-refresh") for t in flags)
    configs = [("pinned", [])] if pinned else [("refresh", []), ("legacy", LEGACY)][:2 if both else 1]
    return [{"id": f"{jid}:{res}", "kind": kind, "cwd": os.path.dirname(path),
             "args": LIT_DEFAULTS + extra + flags + [path], "limit": limit} for res, extra in configs]


def lit_jobs(every=False):
    """Programs with a comprehension under both resolvers; with every, all programs under lit's default resolver."""
    jobs, valued = [], valued_options()
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
            jobs += resolver_jobs(f"lit/{os.path.relpath(p, LIT)}", p, run_flags(first, d, valued), both=not every)
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
