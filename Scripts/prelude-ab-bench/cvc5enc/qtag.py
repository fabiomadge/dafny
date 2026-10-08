#!/usr/bin/env python3
"""qtag.py IN OUT: the first query of a logged SMT file with every quantifier named (:qid qN), and OUT.json mapping
each name to its text (shortened) and patterns. Also used as a module: parse(), show()."""
import json, re, sys

TOKEN = re.compile(r'\s+|;[^\n]*|\|[^|]*\||"(?:[^"]|"")*"|[()]|[^\s()|";]+')


def parse(text):
    """All top-level S-expressions; atoms are strings, lists are Python lists."""
    stack, out = [[]], None
    for m in TOKEN.finditer(text):
        t = m.group(0)
        if t[0].isspace() or t[0] == ";":
            continue
        if t == "(":
            stack.append([])
        elif t == ")":
            e = stack.pop()
            stack[-1].append(e)
        else:
            stack[-1].append(t)
    assert len(stack) == 1
    return stack[0]


def show(e):
    return e if isinstance(e, str) else "(" + " ".join(show(x) for x in e) + ")"


def tag(exprs):
    info = {}

    def walk(e):
        if isinstance(e, str):
            return e
        e = [walk(x) for x in e]
        if len(e) == 3 and e[0] in ("forall", "exists"):
            body = e[2]
            name = f"q{len(info)}"
            if isinstance(body, list) and body and body[0] == "!":
                if ":qid" in body:
                    name = body[body.index(":qid") + 1]
                else:
                    body = body + [":qid", name]
                inner = body[1]
                pats = [show(body[i + 1]) for i in range(2, len(body) - 1) if body[i] == ":pattern"]
            else:
                inner, pats = body, []
                body = ["!", body, ":qid", name]
            info[name] = {"text": show(["forall" if e[0] == "forall" else "exists", e[1], inner])[:400],
                          "patterns": pats}
            e = [e[0], e[1], body]
        return e

    return [walk(x) for x in exprs], info


def first_query(text):
    return text[:text.find("(check-sat)") + 11]


if __name__ == "__main__":
    exprs = parse(first_query(open(sys.argv[1]).read()))
    tagged, info = tag(exprs)
    open(sys.argv[2], "w").write("\n".join(show(x) for x in tagged) + "\n")
    json.dump(info, open(sys.argv[2] + ".json", "w"), indent=0)
    print(len(info), "quantifiers named ->", sys.argv[2])
