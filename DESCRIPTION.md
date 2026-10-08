Fixes #5897.

A comprehension over a native newtype ignores a bound that is not a constant and iterates over the whole type:

```dafny
newtype u64 = x: int | 0 <= x < 0x1_0000_0000_0000_0000

method Main() {
  var n: u64 := 4;
  print |set i: u64 | 0 <= i < n|, "\n";  // never finishes
}
```

Fixing that exposes a second bug, which is on master for `int` as well: a bound that depends on a variable
enumerated later is relaxed in the wrong direction, so a compiled program denies what it verified:

```dafny
method Main() {
  var pairs := set i: int, j: int | 0 <= j < 5 && 0 <= i < 10 - j :: (i, j);
  assert (9, 0) in pairs;
  print (9, 0) in pairs, "\n";  // prints false
}
```

## Cause and fix

**Bounds that are not constants.** Bounds discovery combines the bounds the user wrote with the bounds implied
by the variable's type, and `BoundedPool.GetBest` kept the first of two it could not compare, which is the
type's own. An `IntBoundedPool` now keeps every bound it cannot compare statically, and the compiled range
starts at the largest lower bound and ends at the smallest upper bound. Constants are folded the way the native
type analysis folds them, so a named bound like the standard library's `TWO_TO_THE_64` counts too, and only the
tightest is kept.

A range's bounds are computed before the compiled code checks the conjuncts they rely on: in a set
comprehension, those that mention the bounded variable or one enumerated after it, and in a `forall` statement
or a quantifier, all of them. So a bound whose computation can fail, by a division by a variable, a call, or an
index, is used only where it comes first, as the bound a range used to be computed from alone. A call counts even
without a `requires`, since a constrained parameter type is a precondition too.

**Bounds outside their type.** Until now the backends' range helpers only ever received the type's constant
bounds. Discovery also turns `x <= e` into `e + 1`, moves terms across an inequality (`i < j + 50` gives `j`
the lower bound `i - 49`) and substitutes for a later variable a bound that the variable itself never reaches
(`i < 2 * j` with `j < 128` gives `i` the bound `2 * 128`), none of which need lie in the newtype's range. So
`CompileCollection` now emits each bound through `EmitIntegerRangeBound`, which computes its additions,
subtractions, and multiplications and divisions by constants in `int`. The type's own bound is dropped only
next to a bound that lies in its type wherever it is computed, which is what keeps `forall i: u8 | n > 0 && n -
1 <= i < n` from starting at -1 where `n` is 0. The arithmetic is computed in the compiler rather than in
discovery because the verifier's witness guesses and the native type analysis read discovery's bounds as values
of the variable's own type.

**Bounds that depend on a later variable.** `SanitizeForBoundDiscovery` substituted that variable's upper
bound whether the dependent bound grows or shrinks with it: the monotonicity check ran on the substituted
bound, which no longer mentions the variable, so it always passed. The check now runs on the dependent bound,
an upper bound is substituted where it grows and a lower bound where it shrinks, and the bound is not used
where it does neither. A product of nonnegative `int` factors grows with them. Every bound on the needed side is
substituted, so the tightest is taken at run time. Where that leaves a variable of a compiled `forall` statement
unbounded, as `i` in `0 <= j < 5 && 0 <= i < 10 - j * j`, the statement is tried with its bound variables in the
reverse order, as comprehensions already are, so that `j` is enumerated first and no substitution is needed.
Master compiled that statement too, but substituted `j`'s upper bound and assigned none of its 26 elements.

## Scope

- C++ cannot compile a range over a native newtype until #6550, so this PR's C++ part only takes effect then
  and `NativeNewtypeRanges.dfy` leaves `cpp` out. #6550 needs that part in turn: on its own it makes the
  program above print `0`, and `set x: i32 | 5 <= x < 3` count up until it wraps around, where master compiles
  neither. So #6550 is best merged after this PR, adding `cpp` to that test's list.
- The verifier reads only whether a bound depends on allocation, which no integer bound does, but it sees the order
  that bounds discovery leaves the bound variables in. Where a substitution that master made is now refused, a
  comprehension or quantifier can come out reversed where master kept its order, as in
  `forall i, j | 0 <= j < 5 && 0 <= i < (j - 2) * (j - 2) :: P(i, j)`. Apart from `DependentRangeBounds.dfy`, no file
  of the test suite or the standard libraries translates to different Boogie.
- A comprehension, quantifier or `forall` statement over three or more variables whose bounds neither order
  resolves, because one of them does not grow or shrink with a later variable, like `0 <= j < 3 &&
  0 <= k < (j - 1) * (j - 1) + 1 && 0 <= i < k * k`, is now rejected, where master compiled it by substituting a
  bound that happened to be right. No file of the test suite or the standard libraries is affected.
- A side with no bound of its own, and a bound whose computation can fail next to another bound, still iterate
  up to the type's limit, as before. So does a `forall` statement or quantifier over `int` whose bound divides
  by zero outside its guard, like `forall i | 0 < k && 0 <= i < 100 / k`, which master already gets wrong.

## Test

Four tests under `comp/`: `NativeNewtypeRanges.dfy` for set comprehensions over `u8`, `i32`, `i64` and `u64`,
at the type's edges and across 2^63; `NativeNewtypeRangeForms.dfy` for the forms C++ does not compile, among
them a type bounded by a named constant and subset types; `DependentRangeBounds.dfy` for dependent bounds in
both conjunct orders, under sums, negations, products, quotients and conversions, over cascades of three
variables, and in a quantifier, a `forall` statement, `:|` and a let-such-that; `UnguardedRangeBounds.dfy` for
bounds that rely on conjuncts checked only after the range is computed.

All four pass on C#, Java, JS, Go, Python and the Dafny backend. On master the first two do not finish on C#
within 120 s, and `DependentRangeBounds.dfy` prints `40 25 false`, `25 15`, `60 0` and `true` where it expects
`40 40 true`, `40 25`, `91 95` and `false`, before its `:|` finds no value. `UnguardedRangeBounds.dfy` passes
on master, which computes none of its bounds, and fails if a bound that can fail is kept next to another, or if
the type's own bound is dropped next to `n - 1`.

Resolving all 2082 files of the test suite and the standard libraries gives the same output as master, in the
same total time. Replaying every `%testDafnyForEachCompiler` RUN line, except `NativeNewtypeRanges.dfy`, whose
own `--compilers` the replay driver cannot pass through, and the 233 other lit tests that compile and run a
program, gives master's verdicts on C#, JS, Java, Python, Go and C++, except that `DependentRangeBounds.dfy`
and `NativeNewtypeRangeForms.dfy` now pass.

<small>By submitting this pull request, I confirm that my contribution is made under the terms of the [MIT license](https://github.com/dafny-lang/dafny/blob/master/LICENSE.txt).</small>
