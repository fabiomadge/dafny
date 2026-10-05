# Draft review: dafny-lang/dafny#6545 at `21cd226c0`

**Event:** Comment

## Review body

The fix is right, and it makes proofs cheaper overall: -4.3% per program over 1,249 programs (Boogie
seed 1, Z3 4.16.0). Two requests:

1. **A regression test that fails on master.** `git-issue-6534.dfy` passes on master too. This
   program proves `false` on master, with either resolver, and on 4.11.0. Master's binary with only
   the deleted axiom removed refuses it, and so does this PR:

   ```dafny
   datatype Opt<T> = None | Some(v: T)

   function F(b: bool): int { if b then 1 else 0 }

   lemma Bad(x: Opt<int>, y: Opt<int>, z: Opt<int>)
     requires x == Some(0) && y == Some(1) && z == Some(2)
     requires forall o: Opt<bool> :: o.Some? ==> F(o.v) <= 1
     ensures false
   {
     assert x.v == 0 && y.v == 1 && z.v == 2;
   }
   ```

   `Opt<int>` and `Opt<bool>` values share a Boogie type, so the second precondition gets
   instantiated at `x`, `y` and `z`, which unboxes 0, 1 and 2 as bools. The deleted axiom then makes
   each of their boxes `$Box(true)` or `$Box(false)`, so two of them are equal. So "no program is
   known to prove false" (the test header, the issue) no longer holds. The test with `Bad`, and a
   header that explains the tests, is on https://github.com/fabiomadge/dafny/commit/c4637e279.

2. **The thirteen stabilizations in a PR of their own, landing first.** They improve master too. They
   touch files that other open PRs touch: #6431 edits `DivMod.dfy` and rebuilds
   `DafnyStandardLibraries.doo`, and #4596 stabilizes `Power2.dfy` differently. And a squash merge
   would fold them into the fix. As submitted they hold in CI's declaration order but not across
   orders. At Boogie seeds 0–8, eleven proofs in the edited files fail at some seeds, with this PR or
   on master. Two of them are ones this PR stabilizes with attributes: `EncodeBVIsBase64` (4 of 9
   seeds with this PR) and `DecodeValidEncode1Padding` (5 of 9).
   https://github.com/fabiomadge/dafny/commit/4571f1330, on top of this PR's stabilizations, has
   versions that pass at every seed I tried, with this PR and on master. With them, `SMN'_Correct`
   no longer needs its new 200M limit, nor `EncodeBVIsBase64` its new 50M one. The library verifies
   in its default order, and the `.doo` is rebuilt.

Merging: `dafny0/SubsetTypes.dfy.expect` conflicts with #6543, and
`dafny0/CoinductiveProofs.dfy.expect` with #6544, in the resource counts each records. Whichever
merges second must regenerate them.

## Inline comments

### `Source/DafnyCore/Verifier/BoogieGenerator.Methods.cs`, lines 387–388

The parenthetical points at the deleted axiom. What the next reader needs is who relies on this
conjunct:

```suggestion
          // The heap holds a box of the field's type, and saying so at the box, $IsBox(h[o, f], ..), is what lets
          // the per-type box/unbox axiom conclude $Box($Unbox(h[o, f])) == h[o, f], which CondApplyBox relies on.
```

The method's doc comment (line 256) still gives this axiom's conclusion as `$Is(h[o, f], TT(PP))`.
When `h[o, f]` is a box that the field's type unboxes, it is now
`$Is($Unbox(h[o, f]), TT(PP)) && $IsBox(h[o, f], TT(PP))`.
