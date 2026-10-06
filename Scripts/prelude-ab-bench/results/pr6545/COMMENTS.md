# Draft review: dafny-lang/dafny#6545 at `21cd226c0` (Comment)

## Body

The fix is right, and it is cheaper overall: -4.3% per program over 1,249 programs. Two requests:

1. **A regression test that fails on master.** `git-issue-6534.dfy` passes there too. This proves
   `false` on master (both resolvers) and on 4.11.0, and is refused here. It is on
   https://github.com/fabiomadge/dafny/commit/c4637e279, with a header:

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

   `Opt<int>` and `Opt<bool>` share a Boogie type, so the second precondition is instantiated at
   `x`, `y` and `z`, unboxing 0, 1 and 2 as bools. The deleted axiom then collapses their boxes into
   `$Box(true)` and `$Box(false)`.

2. **Land the 13 stabilizations first, as their own PR.**
   - They help master too.
   - They overlap other open PRs: #6431 edits `DivMod.dfy` and the `.doo`, and #4596 edits
     `Power2.dfy`.
   - In this PR they would vanish into the squash commit.
   - They hold only in CI's order. At seeds 0–8, fifteen proofs in the edited files fail at some
     seeds, here or on master. Among them are the stabilized `EncodeBVIsBase64` and
     `DecodeValidEncode1Padding`, which pass at only 4 and 5 of 9 seeds here.

   https://github.com/fabiomadge/dafny/commit/37b20df68 makes eleven of the fifteen pass at every
   seed tried, here and on master, without the new 200M (`SMN'_Correct`) and 50M
   (`EncodeBVIsBase64`) limits. The other four are flaky on master too.

The `.expect` files conflict with #6543 (`SubsetTypes`) and #6544 (`CoinductiveProofs`); whichever
lands second regenerates them.

## Inline

### `Source/DafnyCore/Verifier/BoogieGenerator.Methods.cs`, lines 387–388

Suggest saying who relies on this conjunct:

```suggestion
          // The heap holds a box of the field's type, and saying so at the box, $IsBox(h[o, f], ..), is what lets
          // the per-type box/unbox axiom conclude $Box($Unbox(h[o, f])) == h[o, f], which CondApplyBox relies on.
```

The doc comment at line 256 should mention the new `$IsBox` conjunct too.
