#!/usr/bin/env python3
"""corpora.py <jobs.json>: download external Dafny programs into work/corpora and write their jobs.

kondo      - GLaDOS-Michigan/Kondo's protocol proofs (OSDI'24), one job per protocol variant, from
             its `verify` script's file list; that script's `dafny /timeLimit:20 /compile:0
             /noNLarith /autoTriggers:1` becomes `verify --disable-nonlinear-arithmetic`
dafnybench - sun-wendy/DafnyBench's ground-truth programs that contain a map/imap comprehension,
             minus its copies of Dafny's own lit tests, with Dafny's default flags
Both are pinned to the commits the #6539 results used. Some variants no longer verify, or no longer
resolve, on current Dafny; their VCs simply do not appear."""
import glob, io, json, os, re, sys, tarfile, urllib.request

HERE = os.path.dirname(os.path.abspath(__file__))
DIR = os.path.join(HERE, "work", "corpora")
PINS = {"Kondo": ("GLaDOS-Michigan/Kondo", "1d6c43e475cadfdf7a10bfb5137cd777ccf2138f"),
        "DafnyBench": ("sun-wendy/DafnyBench", "0cd28feed9cd0179b07fdb9d002f8c39063658e4")}
COMP = re.compile(r"\bi?map\s+[A-Za-z_][\w'?]*\s*(?::|<-|\||,)")


def fetch(name):
    repo, sha = PINS[name]
    root = os.path.join(DIR, f"{name}-{sha}")
    if not os.path.isdir(root):
        os.makedirs(DIR, exist_ok=True)
        data = urllib.request.urlopen(f"https://codeload.github.com/{repo}/tar.gz/{sha}").read()
        tarfile.open(fileobj=io.BytesIO(data)).extractall(DIR)
    return root


def kondo():
    k = os.path.join(fetch("Kondo"), "kondoPrototypes")
    jobs = []
    for script in sorted(glob.glob(f"{k}/*/*/verify")):
        d = os.path.dirname(script)
        m = re.search(r'^files="([^"]*)"', open(script).read(), re.M)
        if m:
            files = [os.path.normpath(f.replace("$scriptpath", d)) for f in m.group(1).split()]
            jobs.append({"id": "kondo/" + os.path.relpath(d, k), "kind": "kondo", "cwd": d, "limit": 50e6,
                         "args": ["--disable-nonlinear-arithmetic", "--allow-warnings", "--use-basename-for-filename",
                                  "--show-snippets:false"] + files})
    return jobs


def dafnybench():
    gt = os.path.join(fetch("DafnyBench"), "DafnyBench", "dataset", "ground_truth")
    copies = ("_Test_dafny4_", "_Test_git-issues_")  # dafny-language-server and linear-dafny copies of lit tests
    return [{"id": "dafnybench/" + os.path.basename(f), "kind": "dafnybench", "cwd": gt, "limit": 50e6,
             "args": ["--allow-warnings", "--use-basename-for-filename", "--show-snippets:false", f]}
            for f in sorted(glob.glob(f"{gt}/*.dfy"))
            if not any(c in f for c in copies) and COMP.search(re.sub(r"//[^\n]*", "", open(f, errors="replace").read()))]


if __name__ == "__main__":
    jobs = kondo() + dafnybench()
    json.dump(jobs, open(sys.argv[1], "w"), indent=1)
    print(len(jobs), "external jobs")
