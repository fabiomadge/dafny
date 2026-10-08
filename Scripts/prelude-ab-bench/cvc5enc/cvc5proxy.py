#!/usr/bin/env python3
"""cvc5proxy.py [cvc5 arguments...]: stands in for cvc5 under Boogie (--solver-path). It splits Boogie's command
stream into S-expressions and rewrites each background assertion - one outside a (push), so not a VC - with
hybrid.py's encoding (Dafny's arithmetic synonyms inlined in formulas, triggers kept, anchors added) before passing it
on; everything else, and every answer, passes through unchanged. The background is held back until a command needs an
answer, so that the synonyms (recognized by their definition axioms) are known before it is rewritten; they are
forgotten at (reset). HYBRID_MODE=eager keeps the synonyms and only adds the anchors;
HYBRID_SCOPE=all rewrites the VCs too, =vc only the VCs;
CVC5PROXY_LOG=FILE logs what cvc5 is sent."""
import os, subprocess, sys, threading
sys.setrecursionlimit(10000000)
threading.stack_size(1 << 29)
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from hybrid import make_rewriter
from qtag import parse, show
from syndef2 import AX

CVC5 = os.environ.get("CVC5", "cvc5")


def commands(stream):
    """Yield the top-level S-expressions of a character stream as strings, as soon as each is complete."""
    buf, depth, state = [], 0, None  # state: None, '"', '|', ';'
    while True:
        line = stream.readline()
        if not line:
            break
        for ch in line:
            buf.append(ch)
            if state == ";":
                if ch == "\n":
                    state = None
                continue
            if state == '"':
                if ch == '"':
                    state = None
                continue
            if state == "|":
                if ch == "|":
                    state = None
                continue
            if ch == ";":
                state = ";"
            elif ch == '"':
                state = '"'
            elif ch == "|":
                state = "|"
            elif ch == "(":
                depth += 1
            elif ch == ")":
                depth -= 1
                if depth == 0:
                    yield "".join(buf)
                    buf = []
        if depth == 0 and buf and "".join(buf).strip() == "":
            buf = []
    if "".join(buf).strip():
        yield "".join(buf)


def main():
    eager = "eager" in os.environ.get("HYBRID_MODE", "")
    scope = os.environ.get("HYBRID_SCOPE", "")  # all: background and VCs; vc: only the VCs; else only the background
    whole = scope in ("all", "vc")
    background_too = scope != "vc"
    log = open(os.environ["CVC5PROXY_LOG"], "a") if os.environ.get("CVC5PROXY_LOG") else None
    solver = subprocess.Popen([CVC5] + sys.argv[1:], stdin=subprocess.PIPE, text=True)
    syn, stats = {}, {"atoms": 0, "anchors": 0}
    rewrite = make_rewriter(syn, eager, stats)
    in_vc = False

    def send(text):
        solver.stdin.write(text + "\n")
        if log:
            log.write(text + "\n")

    background = []  # commands outside a push, held back until something needs an answer

    def flush_background():
        for c in background:
            m = AX.match(c.strip())
            if m:
                syn[m.group(3)] = m.group(4)
        for c in background:
            try:
                if background_too and c.lstrip().startswith("(assert") and syn and not AX.match(c.strip()):
                    for e in rewrite(parse(c)[0]):
                        send(show(e))
                else:
                    send(c)
            except Exception as ex:  # never let the encoding break a run: pass the command on as it came
                sys.stderr.write(f"cvc5proxy: {ex!r}\n")
                send(c)
        background.clear()

    for cmd in commands(sys.stdin):
        head = cmd.lstrip()[:12]
        if head.startswith("(reset"):
            background.clear() if False else None
            flush_background()
            syn.clear()
            in_vc = False
            send(cmd)
        elif not in_vc and (head.startswith("(assert") or head.startswith("(declare") or head.startswith("(define")
                            or head.startswith("(set-") or head.startswith("(;")):
            background.append(cmd)
        elif in_vc and whole and head.startswith("(assert") and syn:
            try:
                for e in rewrite(parse(cmd)[0]):
                    send(show(e))
            except Exception as ex:
                sys.stderr.write(f"cvc5proxy: {ex!r}\n")
                send(cmd)
        else:
            flush_background()
            if head.startswith("(push"):
                in_vc = True
            elif head.startswith("(pop"):
                in_vc = False
            send(cmd)
        if not background:
            solver.stdin.flush()
            if log:
                log.flush()
    flush_background()
    solver.stdin.flush()
    solver.stdin.close()
    sys.exit(solver.wait())


th = threading.Thread(target=main)
th.start()
th.join()
