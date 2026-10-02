# Review of dafny-lang/dafny#6542, "fix: type-guard the assumption after a heap-update forall statement"

PR head `939b457d9` (one commit, Ernie Cohen), base `5f717bf44` = current `master`. No reviews or
comments, on any revision, and no force-pushes. Evidence below comes from this checkout's Dafny
built at `master` and at the PR, Dafny 4.11.0 (the released tool), and Z3 4.16.0, on Linux arm64.

## Verdict

Merge it. The fix is right, needed, minimal and self-contained. It gives the assignment form of
the forall statement the shape that #6367 gave its call form. Suggested, none blocking:

- **Make the test's comment explain the test** rather than narrate history. Prototyped.
- **Cut the description to the template.**
- **Re-run the one failed upstream check.** `xunit-tests / win [1] (1)` failed in a
  language-server test that fails the same way in two unrelated sibling PRs.

## What it does, and should it be done

After a forall statement that assigns to the heap, the verifier assumes a quantifier saying what
the heap now holds. `TrForall_NewValueAssumption` conjoined the range's call facts outside the
bound variables' type antecedent. For `forall t: T | t.n < 10 && t in s { a[t.n] := 0; }` that
asserted `T.T_q(t)` (from the destructor `t.n`) of every datatype value. Instantiated at a value
of another datatype, this contradicts that value's constructor.

The issue's method, which is the PR's test, proves `ensures false` on 4.11.0 and on master
(`2 verified, 0 errors`, with Dafny's defaults and with lit's flags). Master proves it at 16 of 16
Boogie seeds; the PR refuses it at 16 of 16. #6540 alone does not fix it, and this PR alone does
not fix #6531: the two bugs are independent.

It should be done: it is a user-reachable unsoundness, and the fix costs little. On 142 VCs of 9
lit programs with heap-update forall statements (`ForallStmt`, `ForallCompilationNewSyntax`,
`ForallCompilation.legacy`, `MoForallCompilation`, `Inverses`, `LhsDuplicates`, `Bug159`, `Queue`,
`git-issue-6366`), at seeds 1 and 2:

- 135 VCs cost exactly what they cost on master;
- `Queue.dfy` costs 3.8% less in total, from one VC;
- no outcome changes.

The whole corpus agrees (see the benchmark below).

## Is this the right design

Yes. The type antecedent now sits outermost, around the range's call facts as well as the range:
`forall x :: Types(x) ==> Range#canCall && (Range ==> canCalls && heap update)`. This is the shape
#6367 gave the call form, and the shape of the induction hypothesis it fixed.

Assuming the call facts under the type antecedent is sound. The statement's well-formedness check
proves the range well-formed for every value of the bound variables' types, which is what
`Range#canCall` records. No alternative is simpler: the change moves one implication.

## Scope

Self-contained. Nothing obvious is missing:

- **The forall statement's three forms are covered.** `TrForallStmt.cs` builds three quantifiers:
  - the call form's (line 240), which #6367 fixed;
  - the frame axiom of the assignment form (line 421), whose existential keeps the type antecedent
    inside and has no call facts;
  - the new-value assumption, which this PR fixes.
- **`TrForall_NewValueAssumption` has one caller.**
- **The proof form uses a different path.** It exports the `CanCallAssumption` of its ensures
  quantifier through the generic comprehension case in `BoogieGenerator.ExpressionTranslator.cs`,
  where `BplForallTrim` keeps each bound variable's where clause as its antecedent. Sibling #6541
  changes that function for possibly empty types.
- **The other call-fact conjunctions in the verifier are not quantified over unguarded variables**
  (the let-such-that axiom, the decreases check of the induction hypothesis, function-call splits).
- **Pre-existing, unrelated.** In that decreases check, `BoogieGenerator.Methods.cs` adds
  `CanCallAssumption(ee)` twice (lines 790 and 795). The second was probably meant to be the
  callee's `es`.
- **`ProverLogStabilityTest` does not see the change.** It passes before and after: its program has
  no heap-update forall statement. Its docstring asks authors to extend the program in that case.
  Optional.

## Up to date with master

Yes: the base is master's tip (`5f717bf44`, committed 2026-09-19, still the tip on 2026-10-02).
The PR merges cleanly with each of #6539–#6541 and #6543–#6545. With all seven merged (taking
#6545's side of the expected-output conflicts that #6543, #6544 and #6545 have among themselves),
the test still matches its `.expect`. `ProverLogRegression` passes on the PR, and on the PR merged
with #6545.

## Code, comments, tests

- **Code: clean and minimal.** It splits the antecedent into `typeAntecedent` and the range, and
  adds one `BplImp`.
- **Doc comment: the right one.** The added line says why the type antecedent is outermost
  (`Range#canCall holds only for values of those types`). That is the one non-obvious fact here.
- **The test is minimal; its comment should explain it.** Each part is needed:
  - without `var rs := {r};`, or without the parameter `r`, master no longer proves `false`
    (seeds 0–3);
  - without `requires a.Length == 10`, the index is out of range.

  Its header narrates history ("used to assert"), which the
  `// error: (but this was once provable, due to a bug)` idiom already covers. Suggested, and
  prototyped on branch `review-pr6542` on fabiomadge/dafny, commit `5cfba7392`:
  ```dafny
  // After the forall statement, the range's call facts (t.n is defined, so t was built by T)
  // hold only of values of type T. Of r, which is an R, they would contradict its constructor;
  // {r} brings r into play.
  ```
  The expected output is unchanged, and the test passes in the xunit lit harness.
- **Release note: fine.**

## Fact-check of the description and commit message

| claim | verdict |
|---|---|
| `TrForall_NewValueAssumption` conjoined the range's call facts outside the type antecedent | ✓ |
| master's assumption for #6533's program reads as quoted; the new one reads as quoted | ✓, `--bprint`, both exactly |
| "The method in #6533 proves `ensures false` this way, on 4.11.0 and on current master" | ✓, `2 verified, 0 errors`; 16 of 16 seeds on master |
| "This is the shape of #6366, which #6367 fixed for the call form of the forall statement" | ✓, #6367 changed `TrForallStmtCall` |
| "This change only adds a guard to an assumption" | ✓ |
| The regression test fails on master and passes with the change | ✓ |
| Fork CI (Build and Test, standard libraries, runtimes, documentation, DafnyRef.pdf) passes | ✓, all five runs on `939b457d9` succeeded |
| Compared test by test with master plus the new tests, only `git-issue-6533.dfy` changes; `ManualRunCancelCancelRunRun` failed on Windows in the master run | ✓, from the runs' result artifacts: 1,915 integration tests in both, one differs; 940 unit tests, only that one differs |
| Verdicts of 1,092 programs at 16M with Z3 5.1.0: no change but the new test | ✓, the run reports "1 of 1093 programs differ", the new test; the baseline is the fork's stored file |
| Locally on macOS the listed tests and `ProverLogStabilityTest` pass | macOS not checked; the tests pass in the fork's Linux CI, and `ProverLogRegression` passes here |
| (not in the description) upstream CI | one failure, `CachingTest.DocumentAddedToExistingProjectDoesNotCrash` (`TaskCanceledException`) on Windows. The same test fails on Windows in #6541 and #6544, so it does not come from this change |

## Benchmark (`Scripts/prelude-ab-bench`)

Release builds of `master` and of this PR, Z3 4.16.0, at Boogie seed 1, where two runs of
`master` give every VC the same resource count (Dafny's default seed, 0, does not). The corpus
is 2,077 programs: every lit and standard-library program, Kondo's and DafnyBench's 41, and the
90 files of dafny-lang/libraries. The PR changes the cost of 43 VCs. Over the 27 of them that are
proofs, in 15 programs, it costs +2.8% [-3.5, +11.0] per program (each program weighs the same;
95% bootstrap intervals that resample programs).

One verdict changes at its limit: `Lifetime._ctor` in `concurrency/12-MutexLifetime-short.dfy`,
41.5M on `master` and 65.9M with the PR, against the lit limit of 50M. At seeds 1 to 4 it passes
4 times on `master` (32.1M on average) and 3 times with the PR (39.3M); two runs of `master`
agree on all four.

## Suggested title, commit message and description

Title: keep it.

Commit message:

```
fix: type-guard the assumption after a heap-update forall statement

After a forall statement that assigns to the heap, the verifier assumed the
range's call facts (for `forall t: T | t.n < 10 { a[t.n] := 0; }`, that t
was built by T) of every value of the bound variables' Boogie type, and a
value of another datatype then proved false. The type antecedent now
encloses the call facts too, as #6367 did for the call form.

Fixes #6533
```

Description:

````markdown
Fixes #6533

### What was changed?

After a forall statement that assigns to the heap, the verifier assumes what the heap now holds.
The range's call facts sat outside the bound variables' type antecedent, so here it assumed of
every datatype value that it was built by `T` (from `t.n`). This verified (`2 verified, 0 errors`):

```dafny
datatype T = T(n: nat)
datatype R = X | Y(k: nat)

method M(a: array<int>, s: set<T>, r: R)
  requires a.Length == 10
  modifies a
  ensures false
{
  forall t: T | t.n < 10 && t in s {
    a[t.n] := 0;
  }
  var rs := {r};
}
```

The type antecedent now encloses the call facts, as #6367 did for the call form of the forall
statement:

```boogie
assume (forall t#0_2: DatatypeType ::
  $Is(t#0_2, Tclass._module.T())
     ==> _module.T.T_q(t#0_2)
       && (_module.T.n(t#0_2) < 10 && Set#IsMember(s#0, $Box(t#0_2))
         ==> _module.T.T_q(t#0_2)
           && read($Heap, a#0, IndexField(_module.T.n(t#0_2))) == $Box(LitInt(0))));
```

### How has this been tested?

`git-issues/git-issue-6533.dfy` is the method above.

This change was prepared with an AI assistant (Claude Code).

<small>By submitting this pull request, I confirm that my contribution is made under the terms of the [MIT license](https://github.com/dafny-lang/dafny/blob/master/LICENSE.txt).</small>
````
