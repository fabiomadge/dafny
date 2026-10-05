# Draft review: dafny-lang/dafny#6541 at `dde49fee5`

**Event:** Comment

## Review body

The fix is right; every route I tried to `false` through a possibly empty type is refused with it.
Three requests:

1. **Tests for the other two changes.** The test covers only the forall statement: the lambda half
   of the fix can be reverted without failing it, and the constant-field change is untested. Both
   tests are on https://github.com/fabiomadge/dafny/commit/126cd9b99:

   ```dafny
   lemma ViaLambda()
     ensures false
   {
     var f := (x: Empty) => Never();
     assert Never(); // error: (but this was once provable, due to a bug)
   }
   ```

   and, as `git-issue-6532b.dfy`:

   ```dafny
   ghost function G<X>(): bool { true }

   class C<T> {
     ghost const k: bool := G<T>()
   }

   method UseK(c: C<int>) {
     ghost var b := c.k;
     assert b;
   }
   ```

2. **The constant-field change fixes a crash of its own.** The description says the first change
   "exposed" it, but master already rejects `UseK` with "Boogie program had 2 resolution errors:
   undeclared identifier: _module.C$T", and it verifies with this PR. Worth saying so.

3. **Say what the fix costs.** Over a type that is inhabited but declared `witness *`, Z3 cannot
   prove the new existential, so call permissions are lost. With
   `type Pos = x: int | 0 < x witness *` and `function F(): int { 7 }`,
   `var f := (x: Pos) => F(); assert f(5) == 7;` verifies on master and not with this PR;
   `witness 1` restores it. Users can run into this, so it belongs in the description and the
   release note.

A title that says what users get: `fix: don't drop a possibly empty bound variable's type from call
permissions`.
