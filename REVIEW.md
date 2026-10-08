# Review of dafny-lang/dafny#6563 (head `1509ab981`, base master `5f717bf44`)

Everything below was measured on fresh Release builds of master `5f717bf44` and of the PR head,
built with `git archive` into separate trees. Scripts and probes are under job `f479a154`'s tmp dir;
the prototype is commit `4861e8104` on branch `worktree-review-6563` in
`/local/home/fmadge/dafny/.claude/worktrees/review-6563`.

## 1. What it does, and whether it should be done

Two distinct user-visible bugs:

- **#5897 (performance).** A comprehension over a native newtype ignores a non-constant bound and
  iterates the whole type. For a 64-bit type it never finishes. Reproduced: the description's
  example 1 times out at 25 s on master's C# and prints `4` on the PR.
- **A soundness-visible bug, unfiled.** A bound that depends on a later bound variable is relaxed in
  the wrong direction, so a compiled program contradicts what it verified. Reproduced: example 2
  verifies on both builds (`1 verified, 0 errors`) and prints `false` on master, `true` on the PR.

Both are worth fixing, and the second one more than the first. Yes, this should be done.

## 2. Scope — the PR bundles three separable changes, and one of them cannot be tested here

Measured facts:

1. **The dependent-bound fix stands alone.** Example 2 is an `int`-only program that master gets
   wrong; it needs none of the native-range machinery.
2. **The native-range half does NOT stand alone.** I built the PR with `BoundsDiscovery.cs` reverted
   to master (keeping only `TypeImpliedIntegerBounds`): it fails 14 of the 54 range probes, and two
   of those failures are cases master gets right —
   `set i, j | 0 <= i && 0 <= j <= 9 && 9 - j <= i < 20` gives 110 instead of 155, with or without a
   native type. So the dependent-bound fix must land first or together, exactly as the commit series
   has it.
3. **The C++ half is unreachable today.** On master *and* on the PR, a native-newtype range emits
   `_module.u8.IntegerRange(...)`, which is not valid C++ and fails to compile. So
   `dafny_range_div`, `dafny_range_max`/`min`, `RangeIntLiteral`'s 128-bit path and the
   inverted-range clamp have **no test in this PR** — `NativeNewtypeRanges.dfy` excludes `cpp`.
   They are nevertheless load-bearing for #6550: with #6550 alone, example 1 compiles and prints
   `0`, and `set x: i32 | 5 <= x < 3` hangs; with #6563 merged in, C++ prints
   `NativeNewtypeRanges.dfy`'s expected output exactly (verified by running the backend directly and
   diffing against `.expect`, not just by the harness, which counts "unsupported feature" as a pass).

Suggested shape:

- **PR A** — the dependent-bound direction fix (`IsMonotonic`, the substitution direction and the
  substituted-bound list) plus `DependentRangeBounds.dfy`. The soundness fix; lands alone.
- **PR B** — #5897 (`ChooseIntegerBounds`, `Implies`, `CannotFail`, `IntBoundedPool`,
  `ExactIntegerRangeBound`, `EmitIntegerRangeBound`) plus the other three tests. Stacked on A.
- **PR C** — the C++ bound emission and the runtime header, stacked on #6550 so that `cpp` can be
  added to `NativeNewtypeRanges.dfy`'s compiler list in the same PR and every line it adds is
  exercised.

If it stays whole, the title covers only the #5897 half and should name the soundness fix too.

## 3. Correctness

### 3a. BLOCKER — `CannotFail` accepts a call whose precondition is a parameter type

`CannotFail` (`BoundedPool.cs:161`) accepts a `FunctionCallExpr` when `Function.Req.Count == 0`. A
constrained parameter type makes the argument's membership a precondition that `Req` does not list,
and the function's body is verified only under it.

```dafny
newtype u8 = x: int | 0 <= x < 0x100
type Pos = x: u8 | 0 < x witness 1

function Hundred(x: Pos): u8 { 100 / x }

method Main() {
  var k: u8 := 0;
  print forall i: u8 | 0 < k && i < Hundred(k) :: i < 100, "\n";
}
```

Verifies (`4 verified, 0 errors`). Master prints `true` on C#, Java, JS, Python and Go. The PR
keeps `Hundred(k)` as `i`'s upper bound *and* drops u8's own 256 (because `Implies` sees a
`u8`-typed function result), so the bound is evaluated where `k` is 0:

| build | cs | java | js | py | go |
|---|---|---|---|---|---|
| master | `true` | `true` | `true` | `true` | `true` |
| PR | DivideByZeroException | ArithmeticException | hangs | ZeroDivisionError | integer divide by zero |

A set comprehension is safe here, because a conjunct mentioning no bound variable is emitted before
the first loop; a `forall` statement and a quantifier check nothing first.

**No test needs the call case:** deleting that one arm leaves all four new tests passing (mutant M3).
Prototyped as a deletion, with the case added to `UnguardedRangeBounds.dfy` — it fails at
`1509ab981` and passes with the fix. **The deletion costs nothing measurable:** translating the whole
corpus to C# with and without the arm gives byte-identical code for all 1355 files that translate;
the only difference is the new test case. (Keeping calls whose arguments already have their
parameter's type, compared with constraints, would also be sound, but nothing needs it.)

### 3b. A program master compiles correctly is now rejected

```dafny
forall i: int, j: int | 0 <= j < 5 && 0 <= i < j * j { a[j, i] := 1; }
```

Master compiles this and gets the right answer (30 writes). The PR rejects it:

```
Error: forall statements in non-ghost contexts must be compilable, but Dafny's heuristics
can't figure out how to produce or compile a bounded set of values for 'i'
```

`IsMonotonic` returns false for `j * j` (neither operand is constant), so the conjunct is dropped and
`i` loses its only upper bound. Master substituted `j`'s upper bound, which over-approximates and is
right here. The set-comprehension form survives, because the one reordering comprehensions try
enumerates `j` first.

The description's Scope mentions that such a bound "is no longer used" and that no corpus file loses
a bound — which my own sweep confirms (2082 files, 0 stdout differences) — but not that a user
program can now be **rejected**.

Only `forall` statements are affected: they need finite bounds and, unlike comprehensions and
quantifiers, are never tried in the reverse order. `:|` and let-such-that still work (they need only
enumerability), as do set comprehensions. And master's luck cuts both ways here:

```dafny
method Fill(a: array2<int>)
  requires a.Length0 == 5 && a.Length1 == 20
  modifies a
  ensures forall i, j | 0 <= j < 5 && 0 <= i < 20 - j * j :: a[j, i] == 1
{
  forall i: int, j: int | 0 <= j < 5 && 0 <= i < 20 - j * j {
    a[j, i] := 1;
  }
}
```

verifies on master, whose compiled code then assigns **none** of the 70 elements (`a[0, 19]` prints
`0`). The PR rejects it.

**Fix (prototyped):** in `ForallStmt.ResolveGhostness`, where a compiled `forall` statement turns out
to have unbounded variables, retry bounds discovery with the bound variables reversed, as
comprehensions already do, and keep that order if it bounds them all. The compiled code cannot
observe the enumeration order, and ghost `forall` statements are never touched, so the verifier
sees every statement that compiles today exactly as written. With it, all three two-variable shapes
compile and print the right answer on cs/java/js/py/go: `j * j` (30), `(j - 2) * (j - 2)` (10, not
monotone at all) and `20 - j * j` (70, where master printed 0). `Fill` verifies on master and on the
prototype alike, its negative control fails on both, and the program prints `1`. The resolve sweep
over all 2082 files differs from the PR only in the new test line.

**Residual:** a cascade that neither order resolves — `forall i, j, k | 0 <= j < 3 && 0 <= k < j * j
&& 0 <= i < k * k` — is still rejected where master compiled it (14, correct by luck). Teaching
`IsMonotonic` that a product of nonnegative factors grows with them would close this one (not
prototyped); closing every such case would need master's unsound rule back. Say so in Scope.

### 3c. Probes that came out clean

54 range probes × 5 backends: master fails 17, the PR fails 0. Also no regression from a null-field
receiver (`b != null && i < b.v`), a `real`-to-`int` bound, or a subset-typed parameter reached
through a set comprehension.

## 4. Simplification — `SubstituteBound` is dead code the PR refactors

`SinglePassCodeGenerator.SubstituteBound` substitutes a later bound variable's bound into the bound
being emitted. It can never fire: `SanitizeForBoundDiscovery`'s own contract says the stored bound's
"free variables are not among `boundVars[bvi..]`". Measured: translating all 2082 corpus files to C#
with a probe inside it reported one hit, and that hit is a printing artifact (`Substitute` drops a
`{:trigger}` attribute), not a substitution.

The PR changes its signature and threads the new bound list through it. Deleting it instead removes
it, `CompileCollection`'s three extra parameters, and both call sites' extra arguments — 28 lines
fewer than the PR, rather than 3 more.

`IntBoundedPool` is also simpler if it stores one list per side and derives `LowerBound`/`UpperBound`
from it: two invariants, one constructor and the first/rest splitting in `GetBest`,
`CombineIntegerBounds`, `Substituter` and `Clone` all go away, and `SanitizeForBoundDiscovery` can
return one list rather than a head and a tail.

Both are in the prototype.

## 5. CI is red, and the fix is a dedent

`singletons` fails: `dotnet format whitespace --verify-no-changes` reports 7 errors, at
`SinglePassCodeGenerator.cs:1551-1555` and `BoundedPool.cs:133,135` — the two multi-line conditions.
Dedenting the continuation lines by 4 is enough; lifting `ExactIntegerRangeBound`'s `switch` into a
named predicate also reads better. Prototyped; the check is clean.

## 6. Comments

The code comments are in good shape: each one states something that is genuinely hard to recover
from the code — which discovery operations can take a bound out of its type, why the type's bound is
kept next to a computed one, why the min/max tree is balanced, why C++ needs 128 bits and its own
division. I would change two things:

- `ChooseIntegerBounds`'s docstring ends "while the first is the bound that the program states
  first". For a native type the first candidate is the *type's* implied bound, because
  `DiscoverBestBounds_MultipleVars` conjoins the type constraint first — which is why
  `set i: u64 | 0 < k && i < 1000 / k` is safe. Say "the one a range used to be computed from alone",
  as the PR body already does.
- `NativeNewtypeRanges.dfy:57`, "Dafny's division rounds -1 / 2 down to -1, where C++'s rounds it to
  0", explains a C++ difference in the one test file that excludes C++. It belongs next to
  `dafny_range_div`.

`UnguardedRangeBounds.dfy`'s four-line header restates `ChooseIntegerBounds`'s docstring; two lines
would do.

## 7. Tests

- All four pass the harness on cs, java, go, js, dfy and py.
- Discrimination, measured: `DependentRangeBounds.dfy` prints `40 25 false` / `25 15` / `60 0` /
  `true` on master and then its `:|` throws — exactly as the description says. `NativeNewtypeRanges.dfy`
  and `NativeNewtypeRangeForms.dfy` do not finish on master's C# within 120 s.
  `UnguardedRangeBounds.dfy` passes on master, and earns its place as a mutant killer: keeping every
  bound regardless of `CannotFail` (M1) fails it, and dropping the shape check in `Implies` (M2)
  fails `DependentRangeBounds.dfy`.
- `NativeNewtypeRanges.dfy`'s `-- --allow-deprecation --unicode-char false` are no-ops for the six
  backends it runs: the test passes the harness with them stripped. They are there only for the
  future `cpp` leg, and `--unicode-char` is itself deprecated, which is why the second flag is
  needed. Drop both and add them back with `cpp`.
- The Rust leg named in the RUN line is non-blocking and currently fails
  (`The Rust compiler requires --enforce-determinism`), consistent with the description's "the
  harness does not check".

## 8. Description, title, commits, news

- **Length.** 1850 words. Your own PRs run 229–1108 (median ~600): #6482 229, #6453 401, #6443 592,
  #6449 736, #6514 799, #6524 1108. The structure is right; the prose is roughly 3× too long. Most of
  the cuts are in "Cause and fix", which re-derives each commit's reasoning. Draft at
  `DESCRIPTION.md`.
- **Lead with the stronger example.** The verified `assert` that the compiled program denies is the
  compelling one; the hang is the filed issue. Both are self-contained and both reproduce.
- **Claims I verified:** example 1 and 2 (exact); "with #6550, prints 0" (exact); the inverted literal
  range hanging under #6550 alone; "C++ does not compile it"; the per-test master outputs; "Resolving
  all 2082 files of the test suite and the standard libraries gives the same output as master, in the
  same total time" (0 differences, −0.10%).
- **One claim is true only by an artifact.** "Replaying all 330 `%testDafnyForEachCompiler` RUN lines
  ... gives the same verdicts as master, except that `DependentRangeBounds.dfy` and
  `NativeNewtypeRangeForms.dfy` now pass" leaves out `NativeNewtypeRanges.dfy`, whose verdict is
  unchanged only because the replay driver's `--compilers` collides with that test's own. Say which
  tests the replay could not run.
- **News fragments** follow the convention (`5897.fix`, and a descriptive `dependent-range-bounds.fix`,
  which `docs/dev/README.md` allows). If the dependent fix becomes its own PR, rename it to `<PR>.fix`.
- **Commits.** The squash merge makes the series moot, but two commits are superseded by later ones
  (`79c807962`, whose own message the author later called unsafe, and `b95728a89`), so a reviewer
  reading commit-by-commit is reading retracted reasoning. Worth saying in the PR that only the
  squashed state matters, or squashing locally before review.

## 9. Freshness

Master has not moved since `5f717bf44` (2026-09-19), so **no rebase is needed**; `mergeable` is
`MERGEABLE` and `mergeStateStatus: BLOCKED` is just the missing review plus the red check. Nine open
PRs touch the same files; all nine trial-merge cleanly (`git merge-tree --write-tree`): #6514, #6524,
#6526, #6527, #6530, #6550, #6552, #6334, #6335.

## 10. Prototype

On branch `review-6563`: `4861e8104` fixes 3a, 4 and 5, with the new test case; the commit after it
fixes 3b, with a `forall` statement added to `DependentRangeBounds.dfy` that the PR rejects. On the
final build: release build and IntegrationTests clean, `dotnet format whitespace` clean, 54 probes ×
5 backends correct, the four lit tests pass the harness on six backends, and resolving all 2082
corpus files gives the same output as `1509ab981` except for that new test line.
