# Draft review: dafny-lang/dafny#6541 at `dde49fee5` (Comment)

## Body

The fix is right. Four requests:

1. **Test the lambda half and the constant-field change.** Reverting the lambda half does not fail
   the test. For example (both on [126cd9b99](https://github.com/fabiomadge/dafny/commit/126cd9b99), where the
   test's comments also explain the tests rather than their history):

   ```dafny
   lemma ViaLambda() ensures false {
     var f := (x: Empty) => Never();
     assert Never(); // error: (but this was once provable, due to a bug)
   }
   ```

   and, in its own file:

   ```dafny
   ghost function G<X>(): bool { true }
   class C<T> { ghost const k: bool := G<T>() }
   method UseK(c: C<int>) { ghost var b := c.k; assert b; }
   ```

2. **The constant-field change fixes a master crash of its own**, not one the first change
   "exposed": master crashes on `UseK` (exit 134, "undeclared identifier: _module.C$T"). Say so in
   the description and the release note. The release note should also name quantifiers: `forall`
   and `exists` expressions are routes too.
3. **State the cost.** With `type Pos = x: int | 0 < x witness *` and `function F(): int { 7 }`,
   `var f := (x: Pos) => F(); assert f(5) == 7;` verifies on master but not here; `witness 1` fixes
   it.
4. **Retitle.** The variable is still dropped; what changes is that the body is guarded by
   `exists x :: A(x)`. Suggest `fix: don't drop a possibly empty bound variable's type from call permissions`.

A minimal description and commit message: [link](https://github.com/fabiomadge/dafny/blob/review-pr6539-bench/Scripts/prelude-ab-bench/results/pr6541/REVIEW.md#suggested-title-commit-message-and-description).

## Inline

### `Source/DafnyCore/Verifier/BoogieGenerator.ExpressionTranslator.cs`, lines 1774–1776

The substitution is needed regardless of `BplForallTrim` (see `UseK`), so the parenthetical
misleads:

```suggestion
            // The type arguments are substituted too: the right-hand side is stated in terms of the enclosing
            // type's type parameters, which are not in scope here.
```
