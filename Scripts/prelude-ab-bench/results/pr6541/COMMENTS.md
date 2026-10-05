# Draft review: dafny-lang/dafny#6541 at `dde49fee5` (Comment)

## Body

The fix is right. Three requests:

1. **Test the lambda half and the constant-field change.** The lambda half can be reverted without
   failing the test. For example (both on https://github.com/fabiomadge/dafny/commit/126cd9b99):

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

2. **The constant-field change fixes a master bug of its own.** Master rejects `UseK` ("undeclared
   identifier: _module.C$T"). Say so, rather than "exposed".
3. **State the cost.** With `type Pos = x: int | 0 < x witness *` and `function F(): int { 7 }`,
   `var f := (x: Pos) => F(); assert f(5) == 7;` verifies on master but not here; `witness 1` fixes
   it.

Title suggestion: `fix: don't drop a possibly empty bound variable's type from call permissions`.
