# Ernie Cohen's seven soundness PRs, #6539 to #6545

Seven PRs from 2026-09-26 and 27, each closing a hole in Dafny's verification encoding. All seven
are on `master`'s tip, `5f717bf44`, which is still the tip on 2026-10-02, so none needs a rebase.
Only #6540 has a review (approved). Each PR's review is in `results/pr65NN/REVIEW.md`; this page
compares them.

## Verdicts

| PR | fixes | a program proves `false` on `master` | verdict | before merging | cost per program |
|---|---|---|---|---|---|
| #6539 `Map#Glue` elements | #6535 | yes | merge after changes | guard via `Map#Domain`; correct two `UnionFind.dfy` claims; trim the description and the test | +0.6% [-0.6, +1.9]; Z3 5.1.0: +1.6% [+0.4, +2.9] |
| #6540 single-constructor equality | #6531 | yes | merge (approved) | say what it costs (a fixed few hundred to 2,000 RU per VC); correct the scope sentence | +2.0% [+1.0, +3.2] |
| #6541 `BplForallTrim` | #6532 | yes | merge after changes | test the lambda half and the constant-field change, which also fixes a crash on `master`; state the cost | +1.5% [+1.2, +1.8] |
| #6542 heap-update `forall` | #6533 | yes | merge | the test's comment | +2.8% [-3.5, +11.0] |
| #6543 `Map#Items` pairs | #6537 | not known | merge | shorter comments | +0.5% [+0.1, +1.2] |
| #6544 ORDINAL `(o - m) + n` | #6536 | no: the axiom proves a false postcondition, but well-formedness rejects the program | merge after changes | correct the claim that constant ordinal arithmetic is folded; test the region where the axiom was false | -0.0% [-0.1, +0.1] |
| #6545 box identity | #6534 | yes, though the issue and the PR say none is known | merge after changes | that program as the regression test; land the 13 proof stabilizations separately (they hold only in CI's order; a version that holds at every seed is prototyped) | -4.3% [-4.7, -4.0] |
| all seven | | | | | -4.2% [-4.6, -3.8] |

Cost: the PR against `master` over the proofs whose cost it changes, each program weighing the same,
with 95% bootstrap intervals that resample programs (below). #6539's comes from its own benchmark
(`results/pr6539`), eight seeds.

Every PR's description and commit message follow one long template; each review suggests a version
cut to the repository's template around one compelling example. Each review's suggested changes are
prototyped on `fabiomadge/dafny`, branch `review-pr65NN`.

## How they interact

- **Merge conflicts only in recorded resource counts**: `dafny0/SubsetTypes.dfy.expect` (#6543 and
  #6545) and `dafny0/CoinductiveProofs.dfy.expect` (#6544 and #6545). Whichever lands second
  regenerates them; with all four prelude PRs merged the tests print counts that match no branch.
- **All seven together** apply cleanly otherwise and build, and each of the seven new regression
  tests prints its expected output on the merge (checked with lit's flags). They cost -4.2% [-4.6, -3.8] per program, about what #6545 costs alone: #6545 changes
  every query that unboxes, and the others reach far fewer VCs.
- **#6545 rebuilds `DafnyStandardLibraries.doo`**, as nine other open PRs do, and edits library proofs
  that #6431 and #4596 also edit.
- **Upstream CI**: the one red check on #6541, #6542, #6544 (Windows, `CachingTest.
  DocumentAddedToExistingProjectDoesNotCrash`) and #6545 (Windows, `VerificationStatusTest.
  ManualRunCancelCancelRunRun`) is a language-server flake that the changes do not touch.

## Benchmark (`Scripts/prelude-ab-bench`)

Release builds of `master` and of each PR (for the prelude-only #6543 and #6544, `master`'s binary
with the PR's prelude), and of all seven merged, Z3 4.16.0. The corpus is 2,077 programs: every lit
and standard-library program (1,946, of which 25 cannot run as `verify`), Kondo's and DafnyBench's 41,
and the 90 files of dafny-lang/libraries, at `master`'s sources.

Each variant ran at Boogie seed 1. There two runs of `master` give every VC the same resource
count; at Dafny's default seed, 0, many programs' Boogie output, and with it their costs, changes
between identical runs. Jobs where some VC's verdict at its limit changed were re-run at seeds 1 to
4, with `master` twice (an A/A control) and, for the prelude PRs, a placebo that rewrites `master`'s
axiom without changing its meaning.

Files: `report-<pr>.md` (seed 1), `report-<pr>-phase2.md` (seeds 1 to 4), `report-6545-own-sources.md`
(#6545's binary, prelude and edited programs against `master`'s on the same programs; seeds 1 to 4,
and in `report-6545-own-sources-seeds-0-8.md` seeds 0 to 8), and
`vcs-seed1.csv.gz`, every VC's resource count and outcome at seed 1 under each variant. In
`jobs.json`, `$DAFNY` is this branch's checkout, whose programs are `5f717bf44`'s plus #6539's test
changes (`dafny4/UnionFind.dfy`'s `{:isolate_assertions}` and `git-issues/git-issue-6535.dfy`), and
`$LIBRARIES` is dafny-lang/libraries at `b486ff7fa`.

| PR | VCs whose cost changes | programs (proofs) | per program | total | verdicts changed at seed 1 |
|---|---:|---:|---|---|---:|
| #6540 | 3,232 | 97 (3,182) | +2.0% [+1.0, +3.2] | -8.9% [-42.7, +32.1] | 9 |
| #6541 | 151 | 30 (135) | +1.5% [+1.2, +1.8] | -0.5% [-0.9, +2.1] | 0 |
| #6542 | 43 | 15 (27) | +2.8% [-3.5, +11.0] | +39.5% [-11.8, +55.3] | 1 |
| #6543 | 1,638 | 156 (1,570) | +0.5% [+0.1, +1.2] | +0.6% [-30.1, +26.5] | 6 |
| #6544 | 1,213 | 7 (1,196) | -0.0% [-0.1, +0.1] | -12.6% [-12.9, +0.3] | 1 |
| #6545 | 27,050 | 1,249 (24,821) | -4.3% [-4.7, -4.0] | +3.5% [-11.8, +22.2] | 23 |
| all seven | 27,048 | 1,248 (24,816) | -4.2% [-4.6, -3.8] | +5.8% [-10.5, +26.7] | 28 |
| A/A, `master` twice | 0 | | +0.0% | +0.0% | 0 |

One of the 28 is #6539's intended one: `git-issue-6535`'s false lemma is refused. Most others are
brittle VCs near their limits that move both ways, often under the placebo too. Kondo's two-phase-commit
proof, which #6540 seemed to lose at 2 of 4 seeds, fails on `master` too at 5 of 32 seeds (the PR: 8 of
32). The exception is in its review: #6545, as submitted, leaves several of the proofs it stabilizes
flaky across seeds; the prototype `4571f1330` makes eleven proofs in its edited files hold at every
seed tried.
