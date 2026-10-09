#!/usr/bin/env python3
"""A static e-matching simulation over a Boogie query, to predict which top-level patterned axioms a solver could
ever instantiate.

Ground terms are the applications of declared functions in the query's ground assertions (inside lets, outside
quantifiers). Every equality that occurs anywhere, in any polarity, merges its two sides' classes, so the classes
over-approximate any E-graph the solver could build. A pattern matches modulo the classes; a pattern subterm under an
interpreted operator matches anything. Each round, every quantifier (the axioms and the VC's own) is matched against
the terms, and each instance (at most CAP per quantifier and round) adds its ground terms and equalities. An axiom
that no round matches is predicted never to fire. Over-approximating keeps more axioms, never fewer, than exact
syntactic matching would; equalities the solver derives by reasoning (not from an equality atom) are missed."""
import collections, sys
sys.setrecursionlimit(100000)
CAP = 64
QUANT = ("forall", "exists")


def head(e):
    """An application's operator, hashable: an indexed one, ((_ extract 7 0) x), as its text."""
    return e[0] if isinstance(e[0], str) else repr(e[0])


def strip(e):
    while isinstance(e, list) and len(e) >= 2 and e[0] == "!":
        e = e[1]
    return e


def patterns_of(q):
    body = q[2]
    if not (isinstance(body, list) and body and body[0] == "!"):
        return []
    return [body[i + 1] for i in range(2, len(body) - 1) if body[i] == ":pattern"]


class Sim:
    def __init__(self, declared):
        self.declared = declared
        self.ids = {}            # term tuple -> id
        self.terms = []          # id -> term tuple
        self.parent = []
        self.by_head = collections.defaultdict(list)   # head -> term ids
        self.new = []

    def find(self, i):
        while self.parent[i] != i:
            self.parent[i] = self.parent[self.parent[i]]
            i = self.parent[i]
        return i

    def union(self, a, b):
        a, b = self.find(a), self.find(b)
        if a != b:
            self.parent[a] = b

    def intern(self, t):
        i = self.ids.get(t)
        if i is None:
            i = len(self.terms)
            self.ids[t] = i
            self.terms.append(t)
            self.parent.append(i)
            if isinstance(t, tuple):
                self.by_head[t[0]].append(i)
            self.new.append(i)
        return i

    def ground(self, e, env, bound):
        """Intern the ground subterms of e (with env substituting variables); returns e's term, or None if e mentions
        a variable bound by an enclosing quantifier. Lets are inlined lazily through env."""
        e = strip(e)
        if isinstance(e, str):
            if e in env:
                return env[e]
            if e in bound:
                return None
            if e in self.declared:
                self.intern(e)
            return e
        if not e:
            return None
        h = head(e)
        if h in QUANT:
            inner = bound | {v[0] for v in e[1]}
            self.ground(e[2], env, inner)
            return None
        if h == "let":
            env2 = dict(env)
            for b in e[1]:
                v = self.ground(b[1], env, bound)
                env2[b[0]] = v if v is not None else ("let", b[0])
            return self.ground(e[2], env2, bound)
        args = [self.ground(a, env, bound) for a in e[1:]]
        if any(a is None for a in args):
            return None
        t = (h,) + tuple(args)
        if h in self.declared:
            self.intern(t)
        if h == "=" and len(args) == 2:
            self.union(self.intern(args[0]), self.intern(args[1]))
        return t

    def classes(self):
        cls = collections.defaultdict(lambda: collections.defaultdict(list))
        for i, t in enumerate(self.terms):
            if isinstance(t, tuple):
                cls[self.find(i)][t[0]].append(i)
        return cls

    def match(self, p, cls_id, sub, bvars, cls):
        """Substitutions extending sub under which pattern p matches some term of class cls_id."""
        p = strip(p)
        if isinstance(p, str):
            if p in bvars:
                if p in sub:
                    return [sub] if self.find(sub[p]) == cls_id else []
                s = dict(sub); s[p] = cls_id
                return [s]
            if p in self.declared:
                i = self.ids.get(p)
                return [sub] if i is not None and self.find(i) == cls_id else []
            return [sub]
        h = head(p)
        if h not in self.declared:
            return [sub]
        out = []
        for ti in cls[cls_id].get(h, ()):
            t = self.terms[ti]
            if len(t) != len(p):
                continue
            subs = [sub]
            for pa, ta in zip(p[1:], t[1:]):
                nxt = []
                for s in subs:
                    nxt.extend(self.match(pa, self.find(self.intern(ta)), s, bvars, cls))
                    if len(nxt) > CAP:
                        break
                subs = nxt
                if not subs:
                    break
            out.extend(subs)
            if len(out) > CAP:
                break
        return out

    def matches(self, multipat, bvars, cls):
        subs = [{}]
        for p in multipat:
            p = strip(p)
            if isinstance(p, str) or head(p) not in self.declared:
                continue
            nxt = []
            for ti in self.by_head.get(head(p), ()):
                c = self.find(ti)
                for s in subs:
                    nxt.extend(self.match(p, c, s, bvars, cls))
                    if len(nxt) > CAP:
                        break
                if len(nxt) > CAP:
                    break
            subs = nxt
            if not subs:
                return []
        return subs[:CAP]

    def instantiate(self, q, sub):
        rep = {v: self.terms[c] for v, c in sub.items()}
        self.ground(q[2], rep, set())


def fired(cmds_parsed, rounds=3):
    """For the parsed commands of a query: the indices of top-level patterned forall axioms (before the VC's push)
    that the simulation matches within `rounds` rounds, and the indices of all such axioms."""
    declared = {p[1] for p in cmds_parsed if p and p[0] in ("declare-fun", "declare-const", "define-fun")}
    sim = Sim(declared)
    push = next((i for i, p in enumerate(cmds_parsed) if p and p[0] == "push"), len(cmds_parsed))
    cand, quants = {}, []
    for i, p in enumerate(cmds_parsed):
        if not p or p[0] != "assert":
            continue
        y = strip(p[1])
        if i < push and isinstance(y, list) and y and y[0] == "forall" and patterns_of(y):
            cand[i] = y
        else:
            sim.ground(y, {}, set())
            collect_quants(y, quants)
    for i, y in cand.items():
        quants.append((i, y))
    hit = set()
    for _ in range(rounds):
        cls = sim.classes()
        sim.new = []
        for i, q in quants:
            bvars = {v[0] for v in q[1]}
            for mp in patterns_of(q):
                subs = sim.matches(mp, bvars, cls)
                if subs:
                    if i is not None:
                        hit.add(i)
                    for s in subs:
                        sim.instantiate(q, s)
        if not sim.new:
            break
    return hit, set(cand)


def collect_quants(e, out):
    """The VC's own patterned quantifiers (index None): they fire too and add terms."""
    st = [e]
    while st:
        x = strip(st.pop())
        if isinstance(x, list) and x:
            if x[0] == "forall" and len(x) == 3 and patterns_of(x):
                out.append((None, x))
            st.extend(x[1:] if x[0] != "forall" else [x[2]])
