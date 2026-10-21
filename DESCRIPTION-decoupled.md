Fixes #5897.

A comprehension over a native newtype ignores a bound that is not a constant and iterates over the whole type:

```dafny
newtype u64 = x: int | 0 <= x < 0x1_0000_0000_0000_0000

method Main() {
  var n: u64 := 4;
  print |set i: u64 | 0 <= i < n|, "\n";  // never finishes
}
```

Fixing that exposes a second bug, which is on master for `int` as well: a bound that depends on a variable enumerated later is relaxed in the wrong direction, so a compiled program denies what it verified:

```dafny
method Main() {
  var pairs := set i: int, j: int | 0 <= j < 5 && 0 <= i < 10 - j :: (i, j);
  assert (9, 0) in pairs;
  print (9, 0) in pairs, "\n";  // prints false
}
```

## Changes

- **Every bound counts.** `IntBoundedPool` keeps every bound it cannot compare statically, and the compiled range runs from the largest lower bound to the smallest upper bound. The compiled code computes a range's bounds before it checks the conjuncts they rely on, so a bound whose computation can fail, by a division by a variable, a call or an index, is used only where it is the first.
- **Bounds are computed in `int`.** Discovery moves terms across an inequality and substitutes other variables' bounds, so a bound need not lie in its variable's type. `EmitIntegerRangeBound` computes sums, differences, multiplications and divisions by constants, and products of type `int`, in `int`, and the type's own bound is dropped only next to a bound that stays in the type. This is done in the compiler, because the verifier's witness guesses and the native type analysis read discovery's bounds as values of the variable's type.
- **Substitution follows monotonicity.** A later variable's upper bound takes its place where the dependent bound grows with it, a lower bound where it shrinks, and the dependent bound is dropped where it does neither. A product of nonnegative factors counts where its variable stays nonnegative. Master substituted the upper bound regardless.
- **The compiler chooses the enumeration order.** Discovery reordered bound variables by reversing them in the AST, which the verifier translates. The chosen order is now a separate list that only the compiler follows. `forall` statements get the same choice, an order that bounds a native variable by more than its type's limits wins a tie, and where neither the declared nor the reversed order works, each variable is enumerated after those its bounds mention.
- **The trigger generator's new variables come where the bounds need them.** To break a matching loop, the trigger generator replaces a term like `j - 1` with a new variable, in the other variables' bounds too, but master enumerated that variable last, so for `if j, i :| 0 <= j < 5 && 0 <= i < (j - 1) * (j - 1) + 1 && i * j == 2` every backend generated code that refers to that variable before declaring it. With `i, j` declared, master hid this by substituting j's bound into i's, which the monotone substitution no longer does. Each new variable now comes right after the variables its term mentions, in the order only the compiler sees, so the verifier is unaffected. This does not depend on #6566, which moves the rewrite into the verifier's translation and deletes `ExprSubstituter.cs`: whichever of the two lands second resolves a conflict in the trigger generator.

The five commits can be reviewed one at a time: the bounds of #5897, their C++ part, the substitution, the enumeration order with the trigger generator's new variables, and the product rule.

## Scope

- C++ cannot compile a range over a native newtype until #6550, and #6550 alone makes the first program print `0`. So #6550 is best merged after this PR, adding `cpp` to `NativeNewtypeRanges.dfy`'s compilers.
- The verifier now sees every quantifier's bound variables in their declared order. Where master had reversed them, 7 files of the test suite translate to Boogie with the bound variables in a different order, and all 7 verify.
- Where a nested quantifier mentions the same term, the program still fails to compile, as on master: the rewrite shares one list of terms between the two quantifiers, so it binds the new variable in both of them or only in the inner one. #6566 fixes that. Of 128 such generated programs, all pass with #6566 underneath, and the 56 that fail on master still fail without it, 24 of them now with master's crash "An item with the same key has already been added" instead of code that does not compile, because the dependent bound now keeps the term.
- A side with no usable bound still iterates up to its type's limit, as when two variables bound each other only through `%`, and a `forall` statement or quantifier whose bound divides by zero outside its guard still fails, as on master.

## Test

Four tests under `comp/`: `NativeNewtypeRanges.dfy` and `NativeNewtypeRangeForms.dfy` for ranges over native and subset types, the second with the forms C++ does not compile; `DependentRangeBounds.dfy` for dependent bounds in comprehensions, quantifiers, `forall` statements, binding guards, `:|` and let-such-that, in every order, and in the copies that the trigger generator makes; and `UnguardedRangeBounds.dfy` for bounds that rely on conjuncts checked only after the range is computed. All four pass on C#, Java, JS, Go, Python and the Dafny backend. On master, the first two do not finish, and master finds no bounds for six of `DependentRangeBounds.dfy`'s comprehensions.

Resolving the test suite and the standard libraries gives master's output for every file but `DependentRangeBounds.dfy`, in the same total time, and the IntegrationTests suite gives master's results, except that the new tests pass.

<small>By submitting this pull request, I confirm that my contribution is made under the terms of the [MIT license](https://github.com/dafny-lang/dafny/blob/master/LICENSE.txt).</small>
