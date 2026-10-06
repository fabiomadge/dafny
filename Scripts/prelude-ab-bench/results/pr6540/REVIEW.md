# Review of dafny-lang/dafny#6540, "fix: guard the equality axiom of single-constructor datatypes"

PR head `c61bf8b9a` (one commit, Ernie Cohen), base `5f717bf44` = current `master`. Approved by
RustanLeino on 2026-09-28 ("Thanks!"); no other reviews or comments, and no force-pushes. All
upstream checks pass. Evidence below comes from this checkout's Dafny built at `master` and at the PR, Dafny
4.11.0 (the released tool), and Z3 4.16.0, on Linux arm64.

## Verdict

Merge it; the approval stands. The fix is right, needed, minimal and self-contained, and the
author's reason for guarding only one direction is measured to the digit. Its cost is small:
+2.0% per program over the 97 programs it reaches, nearly all of it a fixed few hundred to 2,000
resource units on small VCs, and inherent to any sound guard (see the benchmark). Suggested before
merging, none blocking:

- **Correct the scope sentence.** The axiom was false for every single-constructor datatype, not
  only "whenever the constructor takes every value of its fields' types".
- **Make one `Count == 1` test, and say why one direction stays unguarded.** Prototyped.
- **Trim the test and explain it in its comment.** Drop `Contradiction`, and say why the `forall`
  statement and `{:induction false}` are there. Prototyped.
- **Cut the description to the template.**

## What it does, and should it be done

`Dt#Equal(a, b)` is defined field by field, one axiom per constructor, under
`Ctor?(a) && Ctor?(b)`. For one constructor the antecedent was `true`, so `a` and `b` ranged over
all of `DatatypeType`, the sort every datatype shares. With `Dt#Equal(a, b) <==> a == b`, a value
`X` of any other datatype then equals `Ctor(Dtor(X), ...)`. The issue's program, which is the
PR's test, proves its false lemma on 4.11.0 and on master (`5 verified, 0 errors`, with Dafny's
defaults and with lit's flags). Master proves it at 16 of 16 Boogie seeds; the PR refuses it at
16 of 16.

It should be done. The bug reaches every program through the built-in tuples. On 175 VCs of 7
datatype- and tuple-heavy lit programs (`Datatypes`, `Tuples`, `Maps`, `Compilation`, `Queue`,
`Bug159`, `git-issue-6366`), at seeds 1 and 2, 172 cost exactly what they cost on master, and no
outcome changes. Of the other three, `Tuples`' one VC costs +1.2%, and two in `git-issue-6366`
cost 3.9% less in total. Across the whole corpus the fix costs more (see the benchmark below).

## Is this the right design

Yes. Only the direction "equal fields imply `Dt#Equal`" is false of other datatypes' values, and
only it gets the antecedent. The other direction is sound unguarded: `Dt#Equal(a, b)` is `a == b`,
and every field's `X#Equal` is reflexive (`==`, `Seq#Equal`, `Set#Equal`, `Map#Equal`, the field
type's own `#Equal`).

Guarding both directions, as the issue proposed and as the branch did before the PR was opened
(`37882920f`), is sound but costly, as the description says. Measured on the standard library's
`Arithmetic/LittleEndianNat.dfy` with its own configuration:

| | `LemmaSeqAdd` | `LemmaSeqSub` |
|---|---|---|
| master, seeds 0 / 1 / 2 | 0.206M / 0.205M / 0.206M | 0.183M / 0.183M / 0.123M |
| PR | 0.206M / 0.206M / 0.206M | 0.183M / 0.183M / 0.124M |
| both guarded, library limit (5M) | out of resource; seed 1: "assertion could not be proved" at 0.59M | out of resource |
| both guarded, limit 1e9 | timed out after about 300 s at 256M (seed 0) and 275M (seed 2); seed 1 as above | timed out at 311M, 509M, 311M |

No alternative guard is better. An `$Is` antecedent needs the type arguments, which the trigger
`Dt#Equal(a, b)` does not bind. The two-constructor trigger shape adds nothing for one
constructor.

## Scope

Self-contained. Nothing obvious is missing:

- **No other single-constructor case is unsound.** The verifier's other two single-constructor
  special cases, `CheckCasePatternShape` (`BoogieGenerator.cs`) and the function-call case of
  `CheckWellformed` (`BoogieGenerator.ExpressionWellformed.cs`), assume `Ctor?` of one well-typed
  term. That is sound.
- **Codatatypes are already guarded.** Their equality axioms sit under `$Is(d0, T) && $Is(d1, T)`,
  and they have no single-constructor case.
- **The built-in tuples get the fix too.** They are single-constructor datatypes, and the same code
  now emits their axioms. At the SMT level, the issue's method confirms the scope. Master's axioms
  (`--boogie /prune:0`, cut before the first VC) refute both the term below and its negation, for
  `X` a value of another datatype. The PR's axioms leave the negation `unknown` (both re-checked
  2026-10-06 with `X = A` of `datatype R = A | B`):
  - for the pair, `Tuple2#Equal(X, #Make2(_0(X), _1(X)))`;
  - for `datatype S = S(n: nat)`, `S#Equal(X, S(S.n(X)))`.

  The `nat` case shows the qualifier in the description is not needed (see the fact-check).
- **`ProverLogStabilityTest` does not see the change.** It passes before and after, so its program's
  log holds no single-constructor equality axiom. Its docstring asks authors to extend the program
  in that case. Optional: it would regenerate the whole expected log, which #6545 also rewrites.

## Up to date with master

Yes: the base is master's tip (`5f717bf44`, committed 2026-09-19, still the tip on 2026-10-02). The PR merges cleanly with
each of #6539 and #6541–#6545. With all seven merged (taking #6545's side of the expected-output
conflicts that #6543, #6544 and #6545 have among themselves), the test still matches its
`.expect`. `ProverLogRegression` passes on the PR, and on the PR merged with #6545.

## Code, comments, tests

- **One `Count == 1` test instead of two.** The code removes a dead ternary from the old `else`
  branch, which is good. It now tests `dt.Ctors.Count == 1` twice, once for the trigger and once
  for the body. One `if`/`else` after `eqs` computes both and reads as two cases. Prototyped; the
  generated Boogie is byte for byte the PR's.
- **Say why the first conjunct stays unguarded.** The doc comment explains why that conjunct is
  sound unguarded and why the second needs the antecedent. It omits the one fact a maintainer
  would need before "simplifying" this case into the general one: guarding the first conjunct
  costs. Suggested:
  `Dt#Equal is equality (see AddExtensionalityAxiom), so the first conjunct holds of all values, and an antecedent there makes proofs about tuples far costlier (Std's LittleEndianNat.LemmaSeqAdd). The second needs one: a and b range over all of DatatypeType, the sort that every datatype shares.`
- **Test.**
  - **The header narrates history.** The `// error: (but this was once provable, due to a bug)`
    idiom already covers that.
  - **`Contradiction` tests nothing.** It verifies from `Bad`'s specification whatever the axiom
    says. Without it, master still proves `Bad` at 8 of 8 seeds and the PR refuses it at 8 of 8.
  - **The `forall` statement and `{:induction false}` are load-bearing.** Without either, master no
    longer proves `Bad` (seeds 0–3 and 0–7 checked). A comment should say so, or someone will
    remove them and the test will stop detecting the bug.

  Prototyped: branch `review-pr6540` on fabiomadge/dafny, commit `98b9e9dc1`, on top of the PR. Its expected output is
  regenerated (`3 verified, 1 error`), it passes in the xunit lit harness (a negative control with
  a wrong count fails), and master still proves `Bad` at seeds 0–3.
- **Release note: fine.**

## Fact-check of the description and commit message

| claim | verdict |
|---|---|
| For one constructor `AddInductiveDatatypeAxioms` used the antecedent `true` | ✓ |
| master's axioms for `W = W(k: int)` and for `()` read as quoted | ✓, `--bprint` |
| The new axioms for `W` and `()` read as quoted; the two-constructor axioms are unchanged | ✓ |
| #6531's program proves `false` on 4.11.0 and on master | ✓, `5 verified, 0 errors`; 16 of 16 seeds on master |
| "false whenever the constructor takes every value of its fields' types (no fields, `bool` fields, and the built-in tuples)" | ✗ too narrow: Boogie's constructor functions are total, so a `nat` field is refuted the same way (`unsat` with one term). Every single-constructor datatype was affected |
| Guarding both directions makes `LemmaSeqAdd`/`LemmaSeqSub` time out: "a VC in each grows from about 0.2M resources to several hundred million" | ✓, 256M–509M at the 300 s time limit |
| "the standard library's CI fails" with both guarded | ✓, fork run 36256094763 on `37882920f` failed; locally both lemmas are out of resource at the library's 5M limit |
| With one direction guarded the two lemmas cost 0.206M and 0.183M, as on master | ✓, the same on Linux |
| "This change only adds a guard to one direction of an axiom" | ✓ |
| Fork CI (Build and Test, standard libraries, runtimes, documentation, DafnyRef.pdf) passes | ✓, all five runs on `c61bf8b9a` succeeded |
| Compared test by test with master plus the new tests, only `git-issue-6531.dfy` changes; `ManualRunCancelCancelRunRun` failed on Windows in the master run | ✓, from the runs' result artifacts: 1,915 integration tests in both, one differs; 940 unit tests, only that one differs |
| Verdicts of 1,092 programs at 16M with Z3 5.1.0: no change but the new test | ✓, the run reports "1 of 1093 programs differ", the new test; the baseline is the fork's stored file |
| Locally on macOS the listed tests and `ProverLogStabilityTest` pass | macOS not checked; the tests pass in the fork's Linux CI, and `ProverLogRegression` passes here |

## Benchmark (`Scripts/prelude-ab-bench`)

Release builds of `master` and of this PR, Z3 4.16.0, at Boogie seed 1, where two runs of
`master` give every VC the same resource count (Dafny's default seed, 0, does not). The corpus
is 2,077 programs: every lit and standard-library program, Kondo's and DafnyBench's 41, and the
90 files of dafny-lang/libraries. The PR changes the cost of 3,232 VCs. Over the 3,182 of them that
are proofs, in 97 programs, it costs +2.0% [+1.0, +3.2] per program (each program weighs the same;
95% bootstrap intervals that resample programs): lit +3.2% [+2.0, +5.1] (57 programs),
dafny-lang/libraries +0.7% [+0.3, +1.3], the standard library +0.1% [-0.2, +0.2], Kondo +0.1%
[-2.8, +2.2].

At seed 1, nine VCs change verdict at their limit, all in Kondo's protocol proofs. Re-run at seeds
1 to 4, most are brittle Paxos VCs near the 50M limit that move both ways. One looked lost:
in both `kondoPrototypes/twoPhaseCommit/manual` and `paper-version`, `InvNextLeaderVotesValid` passes
at 4 of 4 seeds on `master` and at 2 of 4 with the PR. It is brittle on `master` too. At seeds 1 to
16, `master` proves it at 14 and 13 of 16 seeds (failing at 10 and 14, and at 9, 14 and 15), and the
PR at 13 and 11. The failing searches give up ("incomplete quantifiers") at about the cost of the
passing ones (0.3M). In `manual`'s seed-1 log, the PR's VC differs from `master`'s only in the
equality axioms of two datatypes. Restoring `master`'s axiom for either one proves it. So does
`master`'s meaning written as the PR's two implications, but only at seed 1, not at seed 4.

Where the cost per program comes from: 3,068 of the 3,182 proofs move by less than 5%. The small VCs
that move most gain a nearly fixed amount, for instance +1,567, +1,578 and +1,579 resource units
for `git-issue-1180b.dfy`'s three `Datatype` VCs. Most of it is Boogie's pruning, not the new
antecedent: the axiom now mentions `Ctor?`, so a VC that uses the type's equality also receives
`Ctor?`'s axioms (its definition, and the inversion axiom with its `exists`). In
`git-issue-904.dfy`'s `FOO.f` (4,504 on `master`, 6,616 with the PR), the PR's log with `master`'s
axiom swapped back in costs 6,434. Any guard on `Ctor?` pays this.

No other shape does better. On `manual`'s VC at 16 seeds, with costs on `git-issue-904`'s `FOO.f`:

| axiom, written into the PR's log | `InvNextLeaderVotesValid` proved | `FOO.f` RU |
|---|---:|---:|
| `master`'s (unsound) | 14/16 | 6,434 |
| the PR's | 13/16 | 6,616 |
| the PR's, with `a != b` added to the antecedent (no reflexive instances) | 13/16 | 6,564 |
| `Ctor?(a) && Ctor?(b) ==> (Dt#Equal(a, b) <==> fields)`, trigger `{Dt#Equal(a, b)}` | 11/16 | 6,538 |

## Suggested title, commit message and description

Title: keep it.

Commit message:

```
fix: guard the equality axiom of single-constructor datatypes

For a datatype with one constructor, the axiom that defines Dt#Equal field
by field had no antecedent, so it spoke about the values of every datatype:
with Dt#Equal(a, b) <==> a == b, a value X of another datatype equaled
Ctor(Dtor(X)), and false followed. Its direction "equal fields imply
Dt#Equal" now has the antecedent Ctor?(a) && Ctor?(b). The other direction
holds of all values; guarding it too makes the standard library's
LittleEndianNat.LemmaSeqAdd and LemmaSeqSub run out of resources.

Fixes #6531
```

Description:

````markdown
Fixes #6531

### What was changed?

For a datatype with one constructor, the axiom that defines its equality field by field had no
antecedent, so it held for every value of `DatatypeType`, the sort all datatypes share:

```boogie
axiom (forall a: DatatypeType, b: DatatypeType :: { _module.W#Equal(a, b) }
  _module.W#Equal(a, b) <==> _module.W.k(a) == _module.W.k(b));
```

Since `W#Equal` is `==`, a value `X` of any other datatype equals `W(W.k(X))`. This verified
(`5 verified, 0 errors`), with `ensures false`:

```dafny
datatype Unit = U
datatype R = X | Y(n: nat)
datatype S = S(n: nat)

function F(u: Unit, s: S): R {
  if u == U then (if s.n == 0 then X else Y(0)) else Y(1)
}

function G(us: seq<Unit>, s: S): seq<R> {
  if |us| == 0 then [] else [F(us[0], s)] + G(us[1..], s)
}

// False: G([U], S(1)) == [Y(0)].
lemma {:induction false} Bad(us: seq<Unit>, s: S)
  requires 0 < |us| && s.n <= 1
  ensures G(us, s)[0].X?
{
  forall us': seq<Unit>, s': S | 0 < |us'| && s'.n <= 1
    ensures G(us', s') != []
  { }
}

lemma Contradiction() ensures false {
  Bad([U], S(1));
  assert G([U], S(1)) == [F(U, S(1))] + G([], S(1));
}
```

The direction "equal fields imply equal" now has the antecedent `W?(a) && W?(b)`, as with several
constructors. The other direction holds of all values and stays unguarded: guarding it too makes
the standard library's `LittleEndianNat.LemmaSeqAdd` and `LemmaSeqSub` run out of resources.

### How has this been tested?

`git-issues/git-issue-6531.dfy` checks that `Bad` is now refused.

This change was prepared with an AI assistant (Claude Code).

<small>By submitting this pull request, I confirm that my contribution is made under the terms of the [MIT license](https://github.com/dafny-lang/dafny/blob/master/LICENSE.txt).</small>
````
