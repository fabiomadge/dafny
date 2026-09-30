#!/usr/bin/env python3
"""preludes.py [--master REF] [--pr REF]: write the prelude variants to preludes/.

master   - DafnyPrelude.bpl at REF (default origin/master)
master2  - master again: runs under it measure nondeterminism across processes (an A/A control)
pr       - DafnyPrelude.bpl at REF (default 074e49a64, the head of dafny-lang/dafny#6539)
placebo  - master with the Glue element axioms' equations flipped: the same (unsound) meaning in
           different SMT text, which measures how much a mere rewrite of the axiom moves costs
pointwise - pr without its guard: the PR's quantifier shape with master's (unsound) meaning, so
           master -> pointwise is what the shape costs and pointwise -> pr what the guard costs
restrict - elements defined everywhere: b inside the domain, $ArbitraryBoxValue outside it
domguard - pr, guarded by membership in Map#Domain(Map#Glue(a, b, t)) instead of a
eager    - pr, with a second trigger that fires on known membership in a
"""
import argparse, os, subprocess

HERE = os.path.dirname(os.path.abspath(__file__))
ap = argparse.ArgumentParser()
ap.add_argument("--master", default="origin/master")
ap.add_argument("--pr", default="074e49a64")
a = ap.parse_args()


def show(ref):
    return subprocess.run(["git", "-C", HERE, "show", f"{ref}:Source/DafnyCore/DafnyPrelude.bpl"],
                          check=True, capture_output=True, text=True).stdout


def sub(src, pairs):
    for old, new in pairs:
        assert src.count(old) == 1, old[:70]
        src = src.replace(old, new)
    return src


master, pr = show(a.master), show(a.pr)
MAP_PR = """axiom (forall a: Set, b: [Box]Box, t: Ty, bx: Box ::
  { Map#Elements(Map#Glue(a, b, t))[bx] }
  Set#IsMember(a, bx) ==> Map#Elements(Map#Glue(a, b, t))[bx] == b[bx]);"""
IMAP_PR = """axiom (forall a: [Box]bool, b: [Box]Box, t: Ty, bx: Box ::
  { IMap#Elements(IMap#Glue(a, b, t))[bx] }
  a[bx] ==> IMap#Elements(IMap#Glue(a, b, t))[bx] == b[bx]);"""
variants = {
    "master": master,
    "master2": master,  # an A/A control: identical input in another process measures nondeterminism
    "pr": pr,
    "placebo": sub(master, [
        ("  Map#Elements(Map#Glue(a, b, t)) == b);", "  b == Map#Elements(Map#Glue(a, b, t)));"),
        ("  IMap#Elements(IMap#Glue(a, b, t)) == b);", "  b == IMap#Elements(IMap#Glue(a, b, t)));")]),
    "pointwise": sub(pr, [
        ("  Set#IsMember(a, bx) ==> Map#Elements(Map#Glue(a, b, t))[bx] == b[bx]);",
         "  Map#Elements(Map#Glue(a, b, t))[bx] == b[bx]);"),
        ("  a[bx] ==> IMap#Elements(IMap#Glue(a, b, t))[bx] == b[bx]);",
         "  IMap#Elements(IMap#Glue(a, b, t))[bx] == b[bx]);")]),
    "restrict": sub(pr, [(MAP_PR, """function Map#Restrict(Set, [Box]Box): [Box]Box;
axiom (forall a: Set, b: [Box]Box, bx: Box ::
  { Map#Restrict(a, b)[bx] }
  Map#Restrict(a, b)[bx] == (if Set#IsMember(a, bx) then b[bx] else $ArbitraryBoxValue));
axiom (forall a: Set, b: [Box]Box, t: Ty ::
  { Map#Elements(Map#Glue(a, b, t)) }
  Map#Elements(Map#Glue(a, b, t)) == Map#Restrict(a, b));"""), (IMAP_PR, """function IMap#Restrict([Box]bool, [Box]Box): [Box]Box;
axiom (forall a: [Box]bool, b: [Box]Box, bx: Box ::
  { IMap#Restrict(a, b)[bx] }
  IMap#Restrict(a, b)[bx] == (if a[bx] then b[bx] else $ArbitraryBoxValue));
axiom (forall a: [Box]bool, b: [Box]Box, t: Ty ::
  { IMap#Elements(IMap#Glue(a, b, t)) }
  IMap#Elements(IMap#Glue(a, b, t)) == IMap#Restrict(a, b));""")]),
    "domguard": sub(pr, [
        ("  Set#IsMember(a, bx) ==> Map#Elements(Map#Glue(a, b, t))[bx] == b[bx]);",
         "  Set#IsMember(Map#Domain(Map#Glue(a, b, t)), bx) ==> Map#Elements(Map#Glue(a, b, t))[bx] == b[bx]);"),
        ("  a[bx] ==> IMap#Elements(IMap#Glue(a, b, t))[bx] == b[bx]);",
         "  IMap#Domain(IMap#Glue(a, b, t))[bx] ==> IMap#Elements(IMap#Glue(a, b, t))[bx] == b[bx]);")]),
    "eager": sub(pr, [
        ("  { Map#Elements(Map#Glue(a, b, t))[bx] }\n  Set#IsMember(a, bx) ==>",
         "  { Map#Elements(Map#Glue(a, b, t))[bx] } { Map#Glue(a, b, t), Set#IsMember(a, bx) }\n  Set#IsMember(a, bx) ==>"),
        ("  { IMap#Elements(IMap#Glue(a, b, t))[bx] }\n  a[bx] ==>",
         "  { IMap#Elements(IMap#Glue(a, b, t))[bx] } { IMap#Glue(a, b, t), a[bx] }\n  a[bx] ==>")]),
}
os.makedirs(f"{HERE}/preludes", exist_ok=True)
for name, text in variants.items():
    open(f"{HERE}/preludes/{name}.bpl", "w").write(text)
print("wrote", ", ".join(f"preludes/{n}.bpl" for n in variants))
