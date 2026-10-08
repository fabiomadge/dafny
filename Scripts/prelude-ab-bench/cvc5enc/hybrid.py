#!/usr/bin/env python3
"""hybrid.py IN OUT [eager][,axioms]: Dafny's arithmetic synonyms inlined inside formulas, with the triggers kept.

In every Boolean atom (not under a binder; let-bound values are left alone), each synonym application F(a, b) (F's
definition axiom: F(x, y) = x op y) is replaced by (op a b), so the solver's arithmetic sees the operators; and the
atom is given anchors (= F(a, b) (op a b)) for every synonym application it had, so the synonym terms that the
triggers (left as they were) match on stay in the E-graph. The atom P' with anchors A becomes (and P' A) where it is
asserted or in mixed polarity, and (=> A P') where it is refuted. With 'eager', the atom keeps its synonyms and only
gets the anchors (the definitions); with 'axioms', only the background before the VC's (push) is
transformed. Sound: each anchor follows from the definition axioms, which stay."""
import os, sys, threading
sys.setrecursionlimit(10000000)
threading.stack_size(1 << 29)
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from qtag import parse, show
from syndef2 import AX

BOOL_OPS = {"and", "or", "not", "=>", "xor", "=", "distinct", "<", "<=", ">", ">=", "true", "false"}


def make_rewriter(syn, eager=False, stats=None):
    """A function from an (assert F) expression to the list of expressions that replace it: the hoisted anchors, then
    the rewritten assertion."""
    stats = stats if stats is not None else {"atoms": 0, "anchors": 0}
    hoisted = {}

    def binderfree(e):
        if isinstance(e, str):
            return True
        if e and e[0] in ("forall", "exists", "let", "!", "lambda"):
            return False
        return all(binderfree(x) for x in e)

    def apps(e, out):
        if isinstance(e, list):
            if e and isinstance(e[0], str) and e[0] in syn and len(e) == 3:
                out.append(e)
            for x in e:
                apps(x, out)

    def inline(e):
        if isinstance(e, str):
            return e
        e = [inline(x) for x in e]
        if e and isinstance(e[0], str) and e[0] in syn and len(e) == 3:
            return [syn[e[0]], e[1], e[2]]
        return e

    def symbols(e, out):
        if isinstance(e, str):
            out.add(e)
        else:
            for x in e:
                symbols(x, out)

    def atom(e, pol, bound):
        found = []
        if not binderfree(e):
            return e
        apps(e, found)
        if not found:
            return e
        seen, local = set(), []
        for a in found:
            k = show(a)
            if k in seen:
                continue
            seen.add(k)
            anchor = ["=", a, inline(a)]
            syms = set()
            symbols(a, syms)
            if syms & bound:
                local.append(anchor)
            elif k not in hoisted:
                hoisted[k] = anchor
        stats["atoms"] += 1
        stats["anchors"] += len(local)
        p = e if eager else inline(e)
        if not local:
            return p
        d = local[0] if len(local) == 1 else ["and"] + local
        return ["=>", d, p] if pol < 0 else ["and", p, d]

    def is_formula(e):
        return isinstance(e, list) and e and isinstance(e[0], str) and (e[0] in BOOL_OPS or e[0] in ("forall", "exists"))

    def rw(e, pol, bound=frozenset()):
        if isinstance(e, str) or not e:
            return e
        op = e[0] if isinstance(e[0], str) else None
        if op == "not":
            return ["not", rw(e[1], -pol, bound)]
        if op in ("and", "or"):
            return [op] + [rw(x, pol, bound) for x in e[1:]]
        if op == "=>":
            return ["=>"] + [rw(x, -pol, bound) for x in e[1:-1]] + [rw(e[-1], pol, bound)]
        if op == "ite" and len(e) == 4:
            if is_formula(e[2]) or is_formula(e[3]):
                return ["ite", rw(e[1], 0, bound), rw(e[2], pol, bound), rw(e[3], pol, bound)]
            return e
        if op == "!":
            return ["!", rw(e[1], pol, bound)] + e[2:]
        if op in ("forall", "exists") and len(e) == 3:
            return [op, e[1], rw(e[2], pol, bound | {b[0] for b in e[1]})]
        if op == "let" and len(e) == 3:
            names = {b[0] for b in e[1]}
            binds = [[b[0], rw(b[1], 0, bound) if is_formula(b[1]) else b[1]] for b in e[1]]
            # a let-bound formula name is a Boolean, never a synonym argument; a let-bound term may be one
            terms = {b[0] for b in e[1] if not is_formula(b[1])}
            return ["let", binds, rw(e[2], pol, bound | terms)]
        if op == "xor":
            return ["xor"] + [rw(x, 0, bound) for x in e[1:]]
        if op == "=" and any(is_formula(x) for x in e[1:]):
            return ["="] + [rw(x, 0, bound) for x in e[1:]]
        return atom(e, pol, bound)

    def rewrite_assert(e):
        new = ["assert", rw(e[1], 1)]
        out = [["assert", hoisted.pop(k)] for k in list(hoisted)]
        stats["hoisted"] = stats.get("hoisted", 0) + len(out)
        return out + [new]

    return rewrite_assert


def transform(text, eager=False, axioms_only=False):
    syn = {m.group(3): m.group(4) for m in AX.finditer(text)}
    i = text.find("(check-sat)")
    head, tail = (text[:i], text[i:]) if i >= 0 else (text, "")
    exprs = parse(head)
    stats = {"atoms": 0, "anchors": 0}
    rewrite = make_rewriter(syn, eager, stats)
    out, in_vc = [], False
    for e in exprs:
        if isinstance(e, list) and e and e[0] == "push":
            in_vc = True
        if axioms_only and in_vc:
            out.append(e)
            continue
        if isinstance(e, list) and e and e[0] == "assert" and not AX.match(show(e)):
            out.extend(rewrite(e))
        else:
            out.append(e)
    return "\n".join(show(x) for x in out) + "\n" + tail, syn, stats


def main():
    mode = sys.argv[3] if len(sys.argv) > 3 else ""
    t, syn, stats = transform(open(sys.argv[1]).read(), eager="eager" in mode, axioms_only="axioms" in mode)
    open(sys.argv[2], "w").write(t)
    print(f"{len(syn)} synonyms, {stats['atoms']} atoms, {stats['anchors']} local anchors, {stats.get('hoisted', 0)} hoisted -> {sys.argv[2]}")


if __name__ == "__main__":
    th = threading.Thread(target=main)
    th.start()
    th.join()
