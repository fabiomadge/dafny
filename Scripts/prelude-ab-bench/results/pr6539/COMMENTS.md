# Draft review: dafny-lang/dafny#6539 at `074e49a64` (Comment)

## Body

The fix is right. Suggestions inline. In the description:

- The "about 17M (6M legacy)" are `M3.UnionFind.JoinMaintainsReaches1`'s costs: `--filter-symbol Main`
  matches it too. `Main`'s own VCs then peak at 0.18M, and `Main` was already brittle on master
  (11.8M–67.6M over 8 seeds, legacy resolver). So it needs `{:isolate_assertions}` regardless of
  this change.
- `Map#Build`'s frame does read elements outside the domain (harmlessly).
- The `IMap#Glue` half is untested: I found no program that reaches it. Worth saying.

## Inline

### `Source/DafnyCore/Prelude/PreludeCore.bpl`, lines 910–914

Suggest guarding with `Map#Domain(Map#Glue(a, b, t))`, which equals `a` by the axiom above. The
guard is where this PR's cost comes from, and this spelling removes its worst regressions:
`GeneralMaps4` (`dafny0/Maps.dfy`) costs 0.17M on master, 2.96M here and 0.18M suggested;
`UnionFind.dfy`'s `Join` (legacy resolver) costs 6.2M, 22.1M and 7.7M. It is -0.6% per program
against this PR over the 63 affected programs
([data](https://github.com/fabiomadge/dafny/tree/review-pr6539-bench/Scripts/prelude-ab-bench/results/pr6539/v2)).

```suggestion
// Inside the domain only: Map#Equal ignores elements outside it, so taking them from b there would be unsound.
// Guarded by Map#Domain(Map#Glue(a, b, t)), which equals a: a guard on a itself is measurably slower.
axiom (forall a: Set, b: [Box]Box, t: Ty, bx: Box ::
  { Map#Elements(Map#Glue(a, b, t))[bx] }
  Set#IsMember(Map#Domain(Map#Glue(a, b, t)), bx) ==> Map#Elements(Map#Glue(a, b, t))[bx] == b[bx]);
```

### `Source/DafnyCore/Prelude/PreludeCore.bpl`, line 1048

Same for `IMap#Glue`:

```suggestion
  IMap#Domain(IMap#Glue(a, b, t))[bx] ==> IMap#Elements(IMap#Glue(a, b, t))[bx] == b[bx]);
```

### `Source/IntegrationTests/TestFiles/LitTests/LitTest/git-issues/git-issue-6535.dfy`, lines 4–22

Simpler. `Contradiction` follows from `Bad`'s specification under any prelude, and master still
proves this version (update the `.expect`):

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
