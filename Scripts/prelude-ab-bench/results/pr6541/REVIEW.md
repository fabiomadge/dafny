# Review of dafny-lang/dafny#6541, "fix: keep a possibly empty bound variable in BplForallTrim"

PR head `dde49fee5` (one commit, Ernie Cohen), base `5f717bf44` = current `master`. No reviews or
comments, no force-pushes. Evidence below was produced on Linux arm64 with Z3 4.16.0, using this
PR's build, `master` built from the same tree, and Dafny 4.11.0 (the NuGet tool), unless it says
otherwise.

## Verdict

Merge it, after four changes:

1. Add tests for the lambda half of the fix and for the constant-field change. Neither is tested
   now: the lambda half can be reverted without failing the test, and the constant-field change
   fixes a crash that `master` already has.
2. Say in the description that the constant-field change fixes that crash on its own.
3. Say what the fix costs: proofs over an inhabited `witness *` type can lose call permissions.
4. Shorten the description and the commit message, and retitle.

The fix is right, needed and minimal, and it closes every route I tried.

## What it does, and should it be done

`BplForallTrim` builds the CanCall facts for lambdas and comprehensions. Comprehensions include
quantifiers, and with them the desugared forall statement. It drops every bound variable the body
does not mention, and that variable's type antecedent with it. `forall x :: A(x) ==> body`, with `x`
not in `body`, means `(exists x :: A(x)) ==> body`. So dropping `x` is sound only if `A` is
inhabited, and a `witness *` type may be empty. On 4.11.0 and on `master`, this proves `false`
(`2 verified, 0 errors`):

```dafny
type Empty = x: int | false witness *
function Never(): bool requires false ensures false { false }

lemma Candidate() ensures false {
  forall x: Empty ensures Never() { }
  assert Never();
}
```

`master` emits `assume Lit(true) ==> _module.__default.Never#canCall();`, and `Never`'s postcondition
does the rest. The PR emits `assume (exists x#0_1: int :: Lit(false)) ==> ...` instead, and refuses
the lemma.

It should be done. Every route below proves `false` on 4.11.0 and on `master`, and each is refused
with the PR:

- a forall statement, with one bound variable or two, over a subset type or a newtype;
- a forall statement whose range alone calls `Never()`;
- a lambda, with one parameter or two;
- an `iset` comprehension and an `imap` comprehension;
- a `forall` expression and an `exists` expression;
- a `seq` initializer;
- a function whose body is such a comprehension.

## Is this the right design

Yes. The trimming exists because a quantifier over `x` whose body does not mention `x` has no
trigger, so Z3 could not use it. The only sound alternatives are equivalent: keep `x` bound (which
is what the title describes), or guard the body by `exists x :: A(x)` (what the code does). The
existential makes the dependency explicit and leaves the nonempty case exactly as it was. When no
left-out variable is possibly empty, the new code computes the same result as the old. Checking
nonemptiness at the binder instead would change Dafny's well-formedness rules, for a corner case.

`Type.IsNonempty` is the right test. It is the ghost-context notion that the translator already uses
for the same purpose: `GeneratePartialGuesses` and `SeparateDisjunctsAccordingToVariableUsage`, in
`BoogieGenerator.Types.cs`, drop or split a variable only if `KnownToHaveToAValue(ghost)` holds.

- **Treated as possibly empty:** `witness *` subset types and newtypes; datatypes whose grounding
  constructor needs a possibly empty type; total arrows into one; non-null non-array class types;
  non-reference traits; type parameters and abstract types without `(0)` or `(00)`.
- **Treated as nonempty:** nullable references, non-null arrays and partial arrows.

The antecedents are `$Is` facts (`NOALLOC`), so allocation plays no part. Of the possibly empty types,
only provably empty ones are a soundness hole. Over the others, the body's well-formedness check
fails anyway: `forall d: D` with `datatype D = D(e: Empty)`, and `forall f: int -> Empty`, are refused
by every version.

The cost is inherent, and the description should state it. Take a type that is inhabited but
declared without a witness, `type Pos = x: int | 0 < x witness *`. Its antecedent is the inlined
`0 < x`, which gives Z3 nothing to match, so it cannot prove the new existential, and the call
permission is lost. Three small programs that verify on `master` fail with the PR:

- `var f := (x: Pos) => F(); assert f(5) == 7;`
- a function returning `(x: Pos) => F()`, and a lemma about its value at 5;
- `ghost function H(): bool { forall x: Pos :: F() == 7 }` with `lemma L() ensures H()`.

Declaring `witness 1` restores all three. Over the 61 lit tests that declare a `witness *` type, at
seeds 0 and 1, 19 of 1,824 (VC, seed) pairs change cost. The total over the proofs is 24.7M either
way, and the only outcome change is the new test. Possibly empty also covers common types
(non-null classes, type parameters), but across the whole corpus the change reaches little (see
the benchmark below).

A small inefficiency, not worth a revision: the existential binds every left-out variable. That
includes nonempty ones, such as a lambda's heap: `exists x: int, heap: Heap :: 0 < x &&
$IsGoodHeap(heap)`. Only the possibly empty ones need it.

**The second change** is needed by the first, and also fixes a bug of its own. A constant field's
right-hand side is stated in terms of its enclosing type's type parameters. Its CanCall was not
instantiated at the use, and the PR now substitutes `e.TypeArgumentSubstitutionsWithParents()`, the
same map the translator uses for member selects.

- **Needed by the first change.** I built the PR without this change. Three programs
  that verify on `master` then abort with "Boogie program had 2 resolution errors: undeclared
  identifier: _module.C$T": a constant whose right-hand side has an `iset`, a `forall` or a lambda
  over `T`, used outside the class.
- **A fix of its own.** `master` and 4.11.0 already abort the same way on this program, which
  verifies with the PR:

  ```dafny
  ghost function G<X>(): bool { true }
  class C<T> { ghost const k: bool := G<T>() }
  method UseK(c: C<int>) { ghost var b := c.k; assert b; }
  ```

  The same holds with a datatype member or an inherited trait constant. The description says only
  that the first change "exposed" this.

## Scope

Self-contained, and nothing obvious is missing. `BplForallTrim` has exactly the two callers the PR
changes. The translator's other free-variable pruning has no such hole:

- exact `let` bindings always have a value;
- the subset-type witness guesses already check `KnownToHaveToAValue`;
- `TrTrigger`'s term filter does not change meaning.

The call form and the assignment form of the forall statement do not go through `BplForallTrim`.
The probes `t/forms/CallForm.dfy`, `AssignForm.dfy` and `AssignFormIndex.dfy` are refused by all
three versions.

## Up to date with master

Yes. The base is `master`'s tip as of 2026-10-02, so no rebase is needed. It shares no file with
#6539 or #6540–#6545, and `git merge-tree` merges it with each of them cleanly.

## Code, comments, tests

- **Code.** The code is clean. The two callers build the possibly-empty set differently (a loop in
  one, `Zip` in the other); that is acceptable.
- **The constant-field comment** ends in a parenthetical about `BplForallTrim`. That is misleading
  now that the substitution is known to be needed anyway. One line is enough:
  `// The right-hand side is stated in terms of the enclosing type's type parameters, which are not in scope here.`
- **The test covers only the forall-statement route.** I built a mutant whose lambda caller passes
  an empty set. With it, the test still passes, and the lambda route above proves `false` again. Nothing tests the constant-field change.
- **The test's comments narrate history**: "used to be granted", "was, and still is, refused". The
  repository's `// error: (but this was once provable, due to a bug)` already covers that.
- **Prototype**, on branch `review-pr6541` on fabiomadge/dafny (`126cd9b99`):
  - The test gets a lambda case, and a control comment that explains the test.
  - `git-issues/git-issue-6532b.dfy` tests the constant. It aborts with exit 134 on `master`.
  - The code comment is the one line above.

  Each test catches its mutant: `git-issue-6532.dfy` fails on the lambda mutant, and
  `git-issue-6532b.dfy` fails without the second change. Both pass in the xunit lit harness on the
  prototype.
- **Release note.** It is accurate for the routes. It should also name quantifiers, and mention the
  constant-field crash if that fix stays in this PR.

## Fact-check of the description and commit message

| claim | verdict |
|---|---|
| `BplForallTrim` drops an unmentioned bound variable with its antecedent | ✓ (`BoogieGenerator.cs:5162-5198`) |
| A forall statement's call permissions reach the solver this way | ✓: `master` emits `assume Lit(true) ==> _module.__default.Never#canCall();` |
| The program proves `false` on 4.11.0 and current `master` | ✓, `2 verified, 0 errors` on both |
| Both callers pass the possibly empty variables; the lambda's heap counts as nonempty | ✓ |
| "Nothing changes for bound variables of types known to be nonempty" | ✓: the new code computes the old result when no left-out variable is possibly empty |
| "The first change exposed a second" (constant field type arguments) | ✓ that the first change alone crashes. ✗ as the whole story: `master` and 4.11.0 already crash on `const k: bool := G<T>()` used outside its class or datatype, or inherited from a trait |
| "This change only weakens what the verifier assumes" | ✓ for the first change. The second turns an internal error into a proof. Not said: inhabited `witness *` types can lose call permissions (three examples, fixed by a declared witness) |
| Regression test: `master` gives `3 verified, 1 error`, and both lemmas are refused with the change | ✓; the PR's output matches its `.expect` |
| Release note: "a `forall` statement, lambda or comprehension" | ✓ for every route listed under "What it does" |
| The fork's five workflows pass on this branch | ✓: runs 36256118427, …366, …382, …462, …469 succeeded on `dde49fee5` |
| Only `git-issue-6532.dfy` differs from the `master` baseline run | Not re-derived test by test. The baseline (36256058553) fails the six issue tests on Linux and `ManualRunCancelCancelRunRun` on Windows, as said |
| Fixed-limit sweep: no verdict changes apart from the new test | ✓: run 36256119902 lists exactly 1 of 1,093 programs (the new test). Its binary was built from `f699ab84`, this PR merged with `.github`-only changes |
| Local macOS runs of the listed tests and `ProverLogStabilityTest` pass | Not re-run on macOS. On Linux, the 61 `witness *` lit tests change no outcome except the new test, and upstream's xunit jobs (which run `ProverLogStabilityTest`) passed on Ubuntu and macOS |
| (not in the description) upstream's own CI on this PR | One failure: Windows xunit, `CachingTest.DocumentAddedToExistingProjectDoesNotCrash` (`TaskCanceledException`). The same test fails on #6542 and #6544, so it is unrelated |

## Benchmark (`Scripts/prelude-ab-bench`)

Release builds of `master` and of this PR, Z3 4.16.0, at Boogie seed 1, where two runs of
`master` give every VC the same resource count (Dafny's default seed, 0, does not). The corpus
is 2,077 programs: every lit and standard-library program, Kondo's and DafnyBench's 41, and the
90 files of dafny-lang/libraries. The PR changes the cost of 151 VCs. Over the 135 of them that
are proofs, in 30 programs, it costs +1.5% [+1.2, +1.8] per program (each program weighs the same;
95% bootstrap intervals that resample programs), and no verdict changes at any VC's limit.

Most of it is one lemma counted 19 times. Every Kondo program includes `UtilitiesLibrary`, whose
`EachUnionMemberBelongsToASet` costs +915 resource units (22,513 to 23,428), +2.1% per program.
Its quantifier ranges over a type parameter, so its guard binds that one variable,
`(exists member#1: Box :: $IsBox(member#1, T)) ==> UnionSeqOfSets#canCall(T, theSets#0)`. Binding
only the possibly empty variables (the inefficiency above) would leave this guard, and so the
cost, as they are.

## Suggested title, commit message and description

Title: `fix: don't drop a possibly empty bound variable's type from call permissions`

Commit message:

```
fix: don't drop a possibly empty bound variable's type from call permissions

BplForallTrim, which builds the CanCall facts of lambdas and comprehensions
(and so of quantifiers and forall statements), dropped a bound variable that
the body does not mention, with its type antecedent. That is sound only for a
nonempty type, and a `witness *` type may be empty: `forall x: Empty ensures
Never() {}` granted the call to `Never`, whose precondition is false, and
proved false. If a dropped variable's type may be empty, the body is now
guarded by the existence of a value.

Also instantiate a constant field's right-hand side with the receiver's type
arguments in its CanCall: `const k := G<T>()`, used outside its class, made
Boogie fail with "undeclared identifier".

Fixes #6532
```

Description:

> Fixes #6532
>
> `BplForallTrim`, which builds the CanCall facts of lambdas and comprehensions (and so of
> quantifiers and forall statements), dropped a bound variable that the body does not mention,
> with its type antecedent. That is sound only for a nonempty type. On 4.11.0 and `master` this
> proves `false`:
>
> ```dafny
> type Empty = x: int | false witness *
> function Never(): bool requires false ensures false { false }
>
> lemma Candidate() ensures false {
>   forall x: Empty ensures Never() { }
>   assert Never();
> }
> ```
>
> If a dropped variable's type may be empty (`!Type.IsNonempty`), the body is now guarded by
> `exists x :: A(x)`. A proof that used such a call permission over an inhabited `witness *` type
> can need the type to declare a witness.
>
> The change also instantiates a constant field's right-hand side with the receiver's type
> arguments in its CanCall. `master` already crashed there ("undeclared identifier") for
> `const k := G<T>()` used outside its class, and the first change added more such cases.
>
> Tests: `git-issues/git-issue-6532.dfy` (a forall statement, a lambda, a control) and
> `git-issues/git-issue-6532b.dfy` (the constant).
