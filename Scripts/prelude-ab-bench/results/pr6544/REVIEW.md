# Review of dafny-lang/dafny#6544, "fix: guard the ORDINAL (o - m) + n axiom by m <= Offset(o)"

PR head `9f392f16b` (one commit, Ernie Cohen), base `5f717bf44` = current `master`. No reviews or
comments, no force-pushes. Evidence below was produced on Linux arm64 with this checkout's Dafny
built at `5f717bf44`, the prelude swapped with `--prelude`, and Z3 4.16.0, unless it says Z3 5.1.0
or Dafny 4.11.0.

## Verdict

Merge it, after two changes:

- **Correct a false claim.** The description and the test comment say that a program cannot state
  the term and that constant ordinal arithmetic is folded before it reaches the solver. It can, and
  it is not: the old axiom proves `((0 as ORDINAL) - 1) + 1 == 0` from source.
- **Add that program to the test.** As it stands, the test only checks where the axiom now applies,
  not where it was false.

The new guard is right, and so are the other three compound ORDINAL axioms. Whichever of this PR and
#6545 merges second must regenerate `dafny0/CoinductiveProofs.dfy.expect`.

## What it does, and should it be done

The axiom for `(o - m) + n` carried the guard `n <= ORD#Offset(o) + m`. That is the guard of the
axiom above it, for `(o + m) - n`. `o - m` is specified only when `m <= ORD#Offset(o)`, and outside
that the axiom equated `(o - m) + n` with an ordinal, falsely. At `o = 0`, `m = n = 1` it says
`(0 - 1) + 1 == 0 - 0 == 0`, while `ORD#Plus`'s axiom makes that term's offset at least 1. #6536's
check reproduces:

| query (the background theory of #6536's `Base` lemma, `/prune:0`) | Z3 4.16.0 | Z3 5.1.0 |
|---|---|---|
| the axioms and `(0 - 1) + 1` (Dafny 4.11.0's own prelude) | unsat | unsat |
| the same on `master` (also after `(push 1)`) | unsat | unsat |
| `master` without the `o-m+n` axiom | unknown | unknown |
| with this PR's prelude | unknown | unknown |
| control: `(1 - 1) + 1` | unknown | unknown |
| control: no term | unknown | unknown |

The false axiom is reached from source. For

```dafny
lemma Undefined() ensures ((0 as ORDINAL) - 1) + 1 == 0 { }
```

the term `ORD#Plus(ORD#Minus(ORD#FromNat(0), ORD#FromNat(1)), ORD#FromNat(1))` appears in the
lemma's postcondition, in its correctness VC and in its callers; nothing folds it. On `master` and
on 4.11.0, the correctness VC is proved, by this axiom. Only the separate well-formedness error,
"ORDINAL subtraction could not be proved to remain above limit ordinal", rejects the program. With
this PR the postcondition is refused too. So no program is known to verify a proof of `false`
through the old guard, because well-formedness catches every `o - m` with `m > o.Offset`. Hiding
the term from well-formedness does not help either. I put it in a branch that a function's
precondition excludes (`if b then ((0 as ORDINAL) - 1) + 1 else 0` under `requires !b`), and also
behind an opaque predicate. Then `ensures false` fails on `master` too, at seeds 0 to 3 and with
either resolver, because the term reaches the solver only in that excluded branch. But the axiom's
falsity is visible in a proof today.

It should be done: the guard is wrong, the fix is one line, and the regression test shows it also
makes the axiom more complete.

## Is this the right design

Yes. The new guard, `0 <= m && 0 <= n && m <= ORD#Offset(o)`, is exactly where `o - m` is defined.
Both conclusions hold there. Write `o` as `λ + k`, with `λ` a limit ordinal or 0 and
`k = ORD#Offset(o)`:

- `(o - m) + n` is `λ + (k - m + n)`.
- For `n <= m` that is `o - (m - n)`, which is defined because `m - n <= m <= k`.
- For `m <= n` it is `o + (n - m)`.
- At `m == n` both give `o`.
- Negative `m` and `n` are excluded, as before.

Replacing the guard, rather than conjoining the new one with the old, also covers
`m <= o.Offset < n - m`. The axiom is true there, and the test shows the gain.

The other compound ORDINAL axioms have the right guards, by the same decomposition:
`o+m+n == o+(m+n)`; `o-m-n == o-(m+n)` for `m+n <= Offset(o)`; `o+m-n` for `n <= Offset(o) + m`.
A probe found nothing else: 448 ground terms, all four compound forms at `o` among 0–3, a fresh
`ω`, `ω+1` and `ω+2`, and `m, n` in 0–3. They are refuted on `master` under both Z3 versions and
not refuted without the `o-m+n` axiom or with this PR, whether `ω` is a limit or unconstrained.

Cost, at seeds 1–3, where runs are reproducible:

- **Reach:** of 146 lit and standard-library programs that mention `ORDINAL` or extreme
  predicates, the PR changes costs in 10.
- **Cost:** their passing VCs cost −1.9% in total, and +0.0% as a geomean of per-program geomeans.
- **Producers:** `std/Actions/Producers.dfy` has 1,149 of these VCs, −1.9% in total and −0.1% per
  VC. Two runs of `master` agree on all of its 2,030 VCs at seeds 1 and 3, and on all but 2 at
  seed 2, so these moves are the PR's.
- **Verdicts:** none of 10,266 (VC, seed) results is lost at its own limit: `@ResourceLimit` where
  the declaration has one, else 5M for the library and 50M for lit tests. Two are gained, in
  `ConcatenatedProducer.Invoke` (`@ResourceLimit("1e8")`): batch 277 at seed 1 and batch 275 at
  seed 2 fail at 100M on `master` and take 38M and 14M with the PR. The library's CI, at the
  default seed, passes with the PR (fork run 36257569014).

## Scope

Self-contained. The translator's other three `ORD#Minus` sites (co-datatype prefix axioms,
prefix-lemma calls, prefix-equality splitting) subtract 1 and pass the result on as an argument.
None wraps it in `ORD#Plus(_, ORD#FromNat(n))`. I did not check each site's guard.

## Up to date with master

Yes, the base is `master`'s tip. It merges cleanly with #6543 and #6539. With #6543 both PRs'
goldens stay right: SubsetTypes 761900, CoinductiveProofs 709865/56001.

It conflicts with #6545 in `dafny0/CoinductiveProofs.dfy.expect`: both edit its resource counts.
#6545 records 684789 / 49866. Built with all four prelude PRs merged (#6539, #6543, #6544, #6545,
#6545's C# change included), the test prints 690950 / 55987, so whichever merges second must
regenerate it. `git-issue-6536.dfy` still verifies with all four.

## Code, comments, tests

- **Regeneration:** `DafnyPrelude.bpl` regenerates from `PreludeCore.bpl` byte for byte, at the
  head and merged with the siblings. Pre-existing: `Prelude/expand.sh` is committed `100644`.
- **Prelude comment:** "(o-m is specified only for m <= ORD#Offset(o), so that is the guard)" is
  the one thing a reader needs. Keep it.
- **Test comment:** nine lines narrate history and claim that "a program cannot state such a term",
  which is false (above). One line says what the test checks.
- **Missing test:** `Undefined` above checks the fix itself. On `master` its postcondition is proved
  and only the well-formedness error appears. With the PR both errors appear. The two runs end
  alike, "4 verified, 2 errors", but the expected output differs in which errors. The test then
  expects errors, so its RUN line needs `%exits-with 4`.
- **Golden:** `CoinductiveProofs.dfy.expect`'s new counts, 709865 and 56001, are what the RUN line
  prints, under both resolvers and in two runs each. `master` prints 709784 and 55967; the 23
  verified and 12 errors are unchanged.
- **Release note:** accurate.

Prototype of the test: branch `review-pr6544` on fabiomadge/dafny (`366398279`). It has the one-line comment, the
`Undefined` lemma, its expected output, and `%exits-with 4` on the RUN line, since the test now
expects errors. Through the xunit lit harness it passes with #6544's prelude in the harness bin. With
`master`'s prelude swapped in it fails as it should: the diff adds `MinusThenPlus`'s postcondition
error and drops `Undefined`'s. With all four prelude PRs merged, Dafny gives the same output as with
#6544 alone.

## Fact-check of the description and commit message

| claim | verdict |
|---|---|
| At `o = 0, m = n = 1` the old guard holds and the axiom is false; the axioms have no model | ✓ (Z3 4.16.0 and 5.1.0, `master` and 4.11.0) |
| `o - m` is specified only for `m <= ORD#Offset(o)` | ✓ (`ORD#Minus`'s axioms' antecedent) |
| The soundness argument for the new guard | ✓ (checked by hand; no refutation in the probe) |
| `DafnyPrelude.bpl` regenerates byte for byte | ✓ (after `chmod +x expand.sh`) |
| The well-formedness condition for `o - m` is `m <= o.Offset` | ✓ (`IsNat` of the RHS and offsets compared) |
| Constant ordinal arithmetic is folded and never reaches the solver | ✗: `((0 as ORDINAL) - 1) + 1` reaches it, and the old axiom proves `Undefined`'s postcondition |
| The other `ORD#Minus` sites are guarded and never wrapped in `ORD#Plus(_, ORD#FromNat(n))` | ✓ never wrapped: each subtracts 1 and passes the result on; the guards not each checked |
| No Dafny program is known to prove `false` through the old guard | ✓ as stated: well-formedness rejects every such program |
| The manual allows `o - m` only for a natural `m` no larger than `o`'s offset | ✓ (`docs/DafnyRef/Types.md:914`) |
| `MinusThenPlus` did not verify and now does | ✓ (`master`: `3 verified, 1 error`; PR: `4 verified`; both resolvers) |
| CoinductiveProofs' counts move, verdicts unchanged | ✓ (Linux arm64; x64 not checked here) |
| The cited fork CI runs passed on this branch | ✓ (all five on `9f392f16b`) |
| Upstream CI | all pass except `xunit-tests / win [1]`: `CachingTest.DocumentAddedToExistingProjectDoesNotCrash` (`TaskCanceledException`), a language-server test that also fails on #6541 and #6542 |
| The verdict sweep changes only the new test | ✓ (run 36257568950: "1 of 1093 programs differ", `git-issue-6536.dfy`) |
| The local macOS runs | not reproducible here |

## Benchmark (`Scripts/prelude-ab-bench`)

One Release build of `master`, with this PR's prelude swapped in by `--prelude`, Z3 4.16.0, at
Boogie seed 1, where two runs of `master` give every VC the same resource count (Dafny's default
seed, 0, does not). The corpus is 2,077 programs: every lit and standard-library program, Kondo's
and DafnyBench's 41, and the 90 files of dafny-lang/libraries. The PR changes the cost of 1,213
VCs. Over the 1,196 of them that are proofs, in 7 programs (93% of them in
`std/Actions/Producers.dfy`), it costs -0.0% [-0.1, +0.1] per program, and -12.6% in total, which
is one VC: `ConcatenatedProducer.Invoke`'s assertion batch 277, from 100.2M, over its
`@ResourceLimit("1e8")`, to 37.8M.

At seeds 1 to 4, with a placebo (`master`'s guard written as `n - m <= ORD#Offset(o)`),
`Producers.dfy` costs -0.1% per VC with the PR and +0.0% with the placebo.
`ConcatenatedProducer.Invoke`'s batches 273 and 275 pass at 4 of 4 seeds with the PR, against 3
and 2 on `master` and with the placebo. Its batch 277, near its 100M limit, moves with any change:
it passes at 1 of 4 seeds on `master`, 2 with the PR and 3 with the placebo, and the placebo also
loses one seed each of batch 283 and `FlattenedProducer.Invoke`.

## Suggested title, commit message and description

Title: keep it.

Commit message:

```
fix: guard the ORDINAL (o - m) + n axiom by m <= Offset(o)

The axiom carried the guard of (o + m) - n, so it also applied where o - m
is undefined, and there it was false: it proves ((0 as ORDINAL) - 1) + 1 == 0.
Its guard is now m <= ORD#Offset(o), where o - m is defined and both of its
conclusions hold.

Fixes #6536
```

Description:

````
Fixes #6536

### What was changed?

The prelude axiom for the `ORDINAL` term `(o - m) + n` carried the guard `n <= ORD#Offset(o) + m`,
which is the guard of `(o + m) - n`. So it also applied where `o - m` is undefined, and there it is
false. On `master`, the correctness check of

```dafny
lemma Undefined() ensures ((0 as ORDINAL) - 1) + 1 == 0 { }
```

passes by this axiom (only the well-formedness error for `0 - 1` stops the program). The guard is
now `m <= ORD#Offset(o)`, exactly where `o - m` is defined. Both conclusions of the axiom hold there,
and the axiom now also applies where `n` exceeds `ORD#Offset(o) + m`.

### How has this been tested?

`git-issues/git-issue-6536.dfy`: `Undefined`'s postcondition is now refused, and `(o - m) + n` is
proved for `m <= o.Offset < n - m` and for `n <= m`. The resource counts that
`dafny0/CoinductiveProofs.dfy` records move; its verdicts do not.

This change was prepared with an AI assistant (Claude Code).

<small>By submitting this pull request, I confirm that my contribution is made under the terms of the [MIT license](https://github.com/dafny-lang/dafny/blob/master/LICENSE.txt).</small>
````
