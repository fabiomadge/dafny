#!/usr/bin/env python3
"""Dafny's arithmetic synonyms as definitions, recognized by their defining axiom (forall x, y :: F(x, y) = x OP y),
so that queries whose names Boogie randomized are handled too. As a module: syndef(text) -> (text, names)."""
import re, sys
AX = re.compile(r"\(assert \(forall \(\((\S+) Int\) \((\S+) Int\) ?\) \(! ?\(= \((\S+) \1 \2\) \((\+|-|\*|div|mod|<|<=|>|>=) \1 \2\)\)")


def syndef(text):
    found = {}
    for m in AX.finditer(text):
        found[m.group(3)] = m.group(4)
    for f, op in found.items():
        for res in ("Int", "Bool"):
            decl = f"(declare-fun {f} (Int Int) {res})"
            if decl in text:
                text = text.replace(decl, f"(define-fun {f} ((x Int) (y Int)) {res} ({op} x y))", 1)
    return text, found


if __name__ == "__main__":
    t, found = syndef(open(sys.argv[1]).read())
    print(len(found), "synonyms:", found)
    if len(sys.argv) > 2:
        open(sys.argv[2], "w").write(t)
