# Draft review: dafny-lang/dafny#6539 at `074e49a64`

**Event:** Comment

## Review body

The fix is right. One change to the axiom, where this PR's cost comes from, a simpler test, and two
corrections to the description.

Description:

- "its largest VC is then about 17M (6M under the legacy resolver)": those are the costs of
  `M3.UnionFind.JoinMaintainsReaches1`, which `--filter-symbol Main` also selects. `Main`'s own VCs
  then peak at 0.18M. And `Main` was already brittle on master: over 8 random seeds it costs
  11.8M to 67.6M under the legacy resolver. So `{:isolate_assertions}` is right, but not because
  this axiom is weaker.
- "The other axioms that read the elements of a map ... read them only inside the domain":
  `Map#Build`'s frame reads them outside the domain too (harmlessly: it only carries them over).
- The `IMap#Glue` half has no test. I found no program that reaches its axiom; worth a sentence.

## Inline comments

### `Source/DafnyCore/Prelude/PreludeCore.bpl`, lines 910–914

Guarding with `Map#Domain(Map#Glue(a, b, t))` means the same as guarding with `a` (by the axiom
just above), and it is cheaper. The guard is where this PR's cost comes from, and its largest
regressions go away with the other spelling: `dafny0/Maps.dfy`'s `GeneralMaps4` costs 0.17M on
master, 2.96M with this guard, and 0.18M with the suggested one; `dafny4/UnionFind.dfy`'s `Join`
postcondition (legacy resolver) costs 6.2M, 22.1M and 7.7M. Over the 63 programs whose proofs this
changes, the suggestion costs 0.6% less per program than this PR (8 seeds, Z3 4.16.0; benchmark and
data in
https://github.com/fabiomadge/dafny/tree/review-pr6539-bench/Scripts/prelude-ab-bench/results/pr6539/v2).
In `GeneralMaps4`, the guard on `a` (the comprehension's `Set#FromBoogieMap(lambda)`) takes Z3 from
about 3,000 quantifier instantiations to 57,000, nearly all in the key comprehension's projection
axioms. The comment also names `b'`, which nothing binds.

```suggestion
// Inside the domain only: Map#Equal ignores elements outside it, so taking them from b there would be unsound.
// Guarded by Map#Domain(Map#Glue(a, b, t)), which equals a: a guard on a itself is measurably slower.
axiom (forall a: Set, b: [Box]Box, t: Ty, bx: Box ::
  { Map#Elements(Map#Glue(a, b, t))[bx] }
  Set#IsMember(Map#Domain(Map#Glue(a, b, t)), bx) ==> Map#Elements(Map#Glue(a, b, t))[bx] == b[bx]);
```

(and `DafnyPrelude.bpl` regenerated).

### `Source/DafnyCore/Prelude/PreludeCore.bpl`, line 1048

The same for `IMap#Glue`:

```suggestion
  IMap#Domain(IMap#Glue(a, b, t))[bx] ==> IMap#Elements(IMap#Glue(a, b, t))[bx] == b[bx]);
```

### `Source/IntegrationTests/TestFiles/LitTests/LitTest/git-issues/git-issue-6535.dfy`, lines 4–22

The test needs neither the precondition nor `Contradiction`. `Contradiction` verifies from `Bad`'s
specification whatever the prelude says, and with a local empty set master still proves `Bad` (12
of 12 seeds). The header retells history, which the `// error:` marker already covers.

```suggestion
lemma Bad(k: int)
  ensures false // error: (but this was once provable, due to a bug)
{
  var s: set<int> := {};
  var m1 := map x: int | x in s :: 1;
  var m2 := map x: int | x in s :: 2;
  assert m1 == m2; // both are empty
  var e := if k in m1 then m1[k] else 1; // a lookup outside the domain, never executed
}
```

(The expected output changes to the new positions and `0 verified, 1 error`.)
