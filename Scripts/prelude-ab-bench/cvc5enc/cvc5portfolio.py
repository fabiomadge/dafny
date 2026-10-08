#!/usr/bin/env python3
"""cvc5portfolio.py [cvc5 arguments...]: stands in for cvc5 under Boogie (--solver-path) and answers each check-sat
with a portfolio of encodings of the same query, run in parallel; the first 'unsat' wins.

The 'plain' member is an ordinary interactive cvc5 session that gets every command unchanged, so it answers whatever
Boogie asks after a check-sat (models, reasons). At each (check-sat) the other members (PORTFOLIO, default
'eager,syn,cmp') each get a fresh cvc5 with the transcript since the last (reset), encoded:
  eager: Dafny's arithmetic synonyms keep their triggers and every atom gets their definitions (hybrid.py, eager);
  syn:   every synonym a definition (define-fun), as the {:inline} prelude gives;
  cmp:   only the comparison synonyms definitions.
An 'unsat' from any member is the answer; a 'sat' from the plain member is too (all members are equisatisfiable);
otherwise the plain member's answer stands. When another member wins while the plain session is still busy, that
session is killed and, before the next command that needs an answer, rebuilt from the transcript."""
import os, queue, subprocess, sys, threading
sys.setrecursionlimit(10000000)
threading.stack_size(1 << 29)
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from hybrid import make_rewriter
from qtag import parse, show
from syndef2 import AX

CVC5 = os.environ.get("CVC5", "cvc5")
MEMBERS = [m for m in os.environ.get("PORTFOLIO", "eager,syn,cmp").split(",") if m]
CMP = {"<", "<=", ">", ">="}
LOG = os.environ.get("PORTFOLIO_LOG")


def log(msg):
    if LOG:
        with open(LOG, "a") as f:
            f.write(msg + "\n")


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


def encode(transcript, member):
    """The transcript's text under a member's encoding."""
    syn = {}
    for c in transcript:
        m = AX.match(c.strip())
        if m:
            syn[m.group(3)] = m.group(4)
    if member == "eager":
        rewrite = make_rewriter(syn, eager=True)
        out = []
        for c in transcript:
            if c.lstrip().startswith("(assert") and syn and not AX.match(c.strip()):
                out.extend(show(e) for e in rewrite(parse(c)[0]))
            else:
                out.append(c)
        return "\n".join(out)
    text = "\n".join(transcript)
    for f, op in syn.items():
        if member == "cmp" and op not in CMP:
            continue
        for res in ("Int", "Bool"):
            decl = f"(declare-fun {f} (Int Int) {res})"
            text = text.replace(decl, f"(define-fun {f} ((x Int) (y Int)) {res} ({op} x y))", 1)
    return text


class Plain:
    """The interactive session; its output goes to Boogie, except a check-sat's answer, which the caller claims."""

    def __init__(self, args):
        self.p = subprocess.Popen([CVC5] + args, stdin=subprocess.PIPE, stdout=subprocess.PIPE, text=True)
        self.claims, self.lock = queue.Queue(), threading.Lock()
        self.claim_next = False
        threading.Thread(target=self.forward, daemon=True).start()

    def forward(self):
        for line in self.p.stdout:
            with self.lock:
                claimed = self.claim_next
                self.claim_next = False
            if claimed:
                self.claims.put(line)
            else:
                sys.stdout.write(line)
                sys.stdout.flush()
        self.claims.put(None)

    def send(self, text):
        self.p.stdin.write(text + "\n")
        self.p.stdin.flush()

    def kill(self):
        try:
            self.p.kill()
        except Exception:
            pass


def run_member(args, text, results, idx, procs, state):
    """One member: a fresh cvc5 on the encoded query. It registers its process under the state's lock, and stops at
    once if the check-sat was decided before it started."""
    try:
        p = subprocess.Popen([CVC5] + args, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.DEVNULL,
                             text=True)
        with state["lock"]:
            procs[idx] = p
            decided = state["decided"]
        if decided:
            p.kill()
            ans = "unknown"
        else:
            out, _ = p.communicate(text + "\n(check-sat)\n(exit)\n")
            ans = next((l.strip() for l in out.splitlines() if l.strip() in ("sat", "unsat", "unknown")), "unknown")
    except Exception as ex:
        ans = f"error {ex!r}"
    results.put((idx, ans))


def main():
    args = sys.argv[1:]
    plain, dead = Plain(args), False
    transcript = []  # commands since the last (reset), without check-sats and queries
    for cmd in commands(sys.stdin):
        head = cmd.lstrip()[:16]
        if head.startswith("(reset"):
            if dead:
                plain.kill()
                plain, dead = Plain(args), False
            transcript = []
            plain.send(cmd)
            continue
        if head.startswith("(check-sat"):
            try:
                if dead:
                    plain.kill()
                    plain, dead = Plain(args), False
                    for c in transcript:
                        plain.send(c)
                with plain.lock:
                    plain.claim_next = True
                plain.send(cmd)
                results, procs = queue.Queue(), {}
                state = {"lock": threading.Lock(), "decided": False}
                texts = []
                for i, m in enumerate(MEMBERS):
                    try:
                        texts.append(encode(transcript, m))
                    except Exception as ex:
                        log(f"encode {m}: {ex!r}")
                        texts.append(None)
                for i, t in enumerate(texts):
                    if t is not None:
                        threading.Thread(target=run_member, args=(args, t, results, i + 1, procs, state),
                                         daemon=True).start()
                pending = 1 + sum(t is not None for t in texts)
                threading.Thread(target=lambda: results.put((0, (plain.claims.get() or "unknown").strip())),
                                 daemon=True).start()
                plain_answer, answer = None, None
                while pending:
                    idx, ans = results.get()
                    pending -= 1
                    log(f"member {(['plain'] + MEMBERS)[idx]} -> {ans}")
                    if idx == 0:
                        plain_answer = ans
                        if ans in ("unsat", "sat"):
                            answer = ans
                            break
                    elif ans == "unsat":
                        answer = "unsat"
                        break
                    if plain_answer is not None and pending == 0:
                        answer = plain_answer
                with state["lock"]:
                    state["decided"] = True
                    running = list(procs.values())
                for p in running:
                    try:
                        p.kill()
                    except Exception:
                        pass
                if plain_answer is None:  # another member won while the plain session works: drop it
                    dead = True
                    plain.kill()
            except Exception as ex:  # never let the portfolio end the session: this VC is unknown
                log(f"check-sat: {ex!r}")
                answer = plain_answer = "unknown"
                dead = True
                plain.kill()
            sys.stdout.write((answer or plain_answer or "unknown") + "\n")
            sys.stdout.flush()
            continue
        if not (head.startswith("(get-") or head.startswith("(echo")):
            transcript.append(cmd)
        if dead:
            if head.startswith("(get-") or head.startswith("(echo"):
                plain.kill()
                plain, dead = Plain(args), False
                for c in transcript:
                    plain.send(c)
                plain.send(cmd)
            continue
        plain.send(cmd)
    try:
        plain.p.stdin.close()
        plain.p.wait()
    except Exception:
        pass


th = threading.Thread(target=main)
th.start()
th.join()
