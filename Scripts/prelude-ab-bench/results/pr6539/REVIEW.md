# Review of dafny-lang/dafny#6539, "fix: state Map#Glue's elements only inside its domain"

PR head `074e49a64` (one commit, Ernie Cohen), base `5f717bf44` = current `master`. No reviews or
comments on any revision; no force-pushes. Evidence below was produced with this checkout's Dafny
(C# identical to master) and Z3 4.16.0, unless it says Z3 5.1.0.

## Verdict

Merge it, after four changes: phrase the guard via `Map#Domain` (measured cheaper), correct two
claims about `UnionFind.dfy`, cut the description to the template, and simplify the test. The
fix is right, needed, minimal and self-contained.

## What it does, and should it be done

`Map#Equal`, and so `==` through extensionality, compares elements only inside the domain, but
`Map#Elements(Map#Glue(a, b, t)) == b` fixed a comprehension's elements everywhere. Two equal
comprehensions therefore equate their value functions outside the domain, and `false` follows.
This verifies on master (12 of 12 seeds with the refreshed resolver, 5 of 5 with the legacy one)
and is refused with the PR:

```dafny
lemma Bad(k: int)
  ensures false
{
  var s: set<int> := {};
  var m1 := map x: int | x in s :: 1;
  var m2 := map x: int | x in s :: 2;
  assert m1 == m2;
  var e := if k in m1 then m1[k] else 1; // a lookup outside the domain, never executed
}
```

It should be done: the axiom is at least as old as 2021 (d94956051), Leino reported it in #2375
(2022, via hand-edited Boogie), and that issue was closed in 2023 by a comment about an unrelated
completeness fix (#4147). Now plain Dafny reaches it.

## Is this the right design

Yes. Pointwise and guarded by membership is the core of Leino's proposal in #2375 ("axiomatize
this under the antecedent that k is in the domain"), and it is the shape of `Seq#Create`'s index
axiom (`0 <= i < len ==> Seq#Index(Seq#Create(...), i) == ...`). It is consistent (a sketch, not
a checked proof): the map theory then has the model in which every map's elements are one fixed
value outside its domain. `Map#Build`'s frame, the one axiom that reads elements outside the
domain, holds there too, as do `Merge`, `Subtract`, `Equal`, `Values`, `Items`, `$Is` and
`$IsAlloc`. Every translator use of
`Map#Elements` is a lookup, so nothing relied on the whole-array equation.

Alternatives, all sound, measured with the benchmark below:

| encoding | geomean vs master (4.16.0) | vs PR (4.16.0) | vs PR (5.1.0) |
|---|---|---|---|
| PR: guard `Set#IsMember(a, bx)` | +2.0% [+0.8, +3.4] | | |
| domguard: guard `Set#IsMember(Map#Domain(Map#Glue(a, b, t)), bx)` | +0.8% [-0.1, +1.8] | -1.1% [-2.3, -0.2] | -0.9% [-2.0, -0.1] |
| restrict: elements everywhere, `$ArbitraryBoxValue` outside the domain | +0.7% [-0.2, +1.6] | -1.3% [-2.5, -0.1] | not run |
| eager: PR plus trigger `{ Map#Glue(a, b, t), Set#IsMember(a, bx) }` | +2.0% [+0.8, +3.4] | +0.1% [-0.3, +0.4] | not run |

`domguard` is equal to the PR's axiom by the `Map#Domain(Map#Glue(a, b, t)) == a` axiom just
above it. It removes the regressions the PR's guard causes, on both Z3 versions:

| VC (mean over 5 seeds) | master | PR | domguard |
|---|---:|---:|---:|
| `dafny0/Maps.dfy` `GeneralMaps4` | 0.17M | 2.96M | 0.18M |
| `dafny4/UnionFind.dfy` `Join` batch 124 (its comprehension postcondition), legacy resolver | 5.8M | 31.0M (max 40.3M) | 8.9M |
| 16 nested comprehensions (`synth/chain-16`) | 0.32M | 2.30M | 0.33M |
| the same with `imap` (`synth/ichain-16`) | 0.59M | 1.55M | 0.60M |

In `GeneralMaps4` the PR's guard, whose `a` is the comprehension's `Set#FromBoogieMap(lambda)`,
takes Z3 from 3,126 quantifier instantiations to 56,688. Nearly all of them are in the key
comprehension's projection axioms. With `domguard` there are 3,413. Where `domguard` is worse
than the PR: `Join` batch 128 (refreshed resolver), 3.1M → 6.2M; and one seed of `FindAux` on
Z3 5.1.0, 58M, where that VC's other seeds are 7–12M. `restrict` doubles `FindAux` (14M → 31M),
and `eager` changes nothing.

## Scope

Self-contained. Nothing obvious is missing, but:

- The `IMap#Glue` half has no test. I found no Dafny program that reaches it (14 variants
  tried). The same derivation is `unsat` at the SMT level once a lookup term is present, so the
  change is right by analogy. The description should say so in a sentence.
- The benchmark finds a thin margin in `UnionFind.dfy`'s `Join` postcondition under the legacy
  resolver: 5.8M → 31.0M mean, 40.3M max, against the 50M limit. `domguard` keeps it at 8.9M.

## Up to date with master

Yes: the base is master's tip, so no rebase is needed. It merges cleanly with the author's
sibling PRs #6540–#6545 (#6543–#6545 also edit the prelude). No other open prelude PR touches
these axioms, except the stale #4537 and #4598, which restructure the whole prelude.

## Code, comments, tests

- `DafnyPrelude.bpl` and `PreludeCore.bpl` change alike, and `make check` regenerates the former
  byte for byte. (Pre-existing, unrelated: `Prelude/expand.sh` is committed `100644`, so `make`
  fails on a fresh Linux checkout until it is `chmod +x`.)
- The comment names `b'`, which nothing binds; one line says it:
  `// Inside the domain only: Map#Equal ignores elements outside it, so taking them from b there would be unsound.`
  With `domguard`, add a line saying why the guard names `Map#Domain`; otherwise someone will
  "simplify" it to `a`.
- The test needs neither the precondition nor `Contradiction`. `Contradiction` verifies from
  `Bad`'s specification whatever the prelude says. The lemma above has no precondition and
  still proves `false` under the old axiom for 12 of 12 seeds. The header comment narrates
  history. The repo's `// error: (but this was once provable, due to a bug)` idiom already
  covers that, and two end-of-line comments can explain the test instead.
- Release note, shorter: "Fix a soundness issue that let two map comprehensions over the same
  domain prove `false` when their value expressions differ outside it".
- `{:isolate_assertions}` on `Main` is the right change, for a different reason than the PR
  gives (see below).

All four suggestions are prototyped on branch `review-pr6539` (commits `07c25d14d`, `4abd4e921`).
Of the 49 lit tests with map comprehensions, 29 pass through the xunit harness with both the
PR's prelude and `domguard`, and 4 more with `domguard` (not run with the PR's). The other 16
compile to Java, JavaScript, Go or Rust, which this host lacks. The benchmark verifies 48 of
the 49 with their RUN-line flags (not `cli/inputFormatCollections.dfy`, which verifies a binary
encoding read from stdin), and nothing changes verdict except `git-issue-6535`. With `domguard`,
`UnionFind.dfy`'s largest VC is 16.9M (refreshed) and 16.6M (legacy); with the PR's guard it is
20.9M and 19.9M. `ProverLogStabilityTest` passes with both.

## Fact-check of the description and commit message

| claim | verdict |
|---|---|
| The #6535 program proves `false` on master (`2 verified, 0 errors`) and not with the PR | ✓, both resolvers |
| `TranslateMapComprehension` builds `Map#Glue(Set#FromBoogieMap(λ R), λ G, t)` | ✓ |
| "The other axioms that read the elements (`Map#Equal`, `Map#Merge`, `Map#Subtract`, `Map#Values`, `Map#Items`) read them only inside the domain" | ✗ as a blanket claim: `Map#Build`'s frame reads them outside the domain (harmlessly, as #6535 says) |
| "This change only weakens an axiom" | ✓ |
| `DafnyPrelude.bpl` regenerates byte for byte | ✓ |
| `Main`: about 21M → 53M (refreshed), 21M → 31M (legacy); lit limit 50M per VC; #6478 did the same for `Join` | ✓ at the default seed |
| "its largest VC is then about 17M (6M under the legacy resolver)" | ✗: those are `M3.UnionFind.JoinMaintainsReaches1` (16.95M / 6.27M), which `--filter-symbol Main` also selects. `Main`'s own isolated VCs peak at 0.18M |
| `Main` needs isolation *because of* the weaker axiom | ✗ misleading: `Main` is brittle on master. Over 5 seeds: 13.8–30.9M (refreshed) and 11.8–67.6M (legacy, one seed over 50M); on Z3 5.1.0, 12.6–68.3M. The placebo (master's axiom with its equation flipped) costs 77.1M at the default seed |
| The cited fork CI runs exist, ran on `074e49a`, and passed (Build and Test on attempt 2) | ✓ |
| The listed local lit tests and `ProverLogStabilityTest` pass | ✓ |
| Z3 5.1.0 fixed-limit sweep of 1,092 programs | not reproduced (the run exists; Z3 5.1.0 exists, 2026-08-16) |
| Affects 4.11.0 | not run; the axiom is identical at `v4.11.0` |

## Benchmark (`Scripts/prelude-ab-bench`)

The benchmark uses one Dafny binary with the prelude swapped via `--prelude`, 5 random seeds,
and raised caps. The corpus: 48 lit tests with map/imap comprehensions under both resolvers,
the three standard-library files with comprehensions, 40 synthetic programs, and master's
`UnionFind.dfy`. Of 1,875 VCs, 930 are affected. The other 945 gave bit-identical costs under
master and the PR for every seed: the change did not reach them.

| affected proofs (lit + std) | Z3 4.16.0 (844 VCs) | Z3 5.1.0 (841 VCs) |
|---|---|---|
| PR, geomean of per-VC ratios | +2.0% [+0.8, +3.4] | +1.9% [+0.7, +3.3] |
| PR, total | +17.8% [-2.1, +49.4] | +13.0% [-4.0, +35.7] |
| placebo, geomean / total | +0.0% / +0.5% | +0.1% / -1.6% |
| domguard, geomean / total | +0.8% / +2.4% | +0.9% / +7.3% |
| verdict changes at the tests' limits | only `git-issue-6535` | only `git-issue-6535` |

The typical VC changes by 2%. The total is carried by a few heavy VCs (UnionFind). The standard
library moves by under 1%. Solver time over the proofs: 137 s → 158 s (placebo 135 s). Among
the synthetic programs at N=16, lookups, updates and UnionFind-style postconditions cost at most
13% more, and equalities 34% more. Nesting costs 7× at 16 levels (2.6× with `imap`). 16 lookups
into a key-expression comprehension exceed 50M on 2 of 5 seeds on Z3 4.16.0 (not on 5.1.0).

## Suggested title, commit message and description

Title: keep it (`fix: state Map#Glue's elements only inside its domain`).

Commit message:

```
fix: state Map#Glue's elements only inside its domain

Map#Equal compares elements only inside the domain, yet the prelude said
Map#Elements(Map#Glue(a, b, t)) == b everywhere, so two equal map
comprehensions equated their value functions outside it too, and proved
false. Give the elements only inside the domain, for Map#Glue and IMap#Glue.

dafny4/UnionFind.dfy's Main, one VC whose cost already varies from 12M to
68M across seeds, now needs 53M at the default seed, over the 50M limit;
give it {:isolate_assertions}, as #6478 did for Join.

Fixes #6535
```

Description:

````markdown
Fixes #6535

### What was changed?

Map equality compares elements only inside the domain, but the prelude gave a map comprehension's
elements everywhere (`Map#Elements(Map#Glue(a, b, t)) == b`), so equal comprehensions made their
value functions equal outside the domain too. This verified:

```dafny
lemma Bad(k: int)
  ensures false
{
  var s: set<int> := {};
  var m1 := map x: int | x in s :: 1;
  var m2 := map x: int | x in s :: 2;
  assert m1 == m2;
  var e := if k in m1 then m1[k] else 1; // a lookup outside the domain, never executed
}
```

The elements are now given only inside the domain, as `Seq#Create`'s are only inside its length:

```boogie
axiom (forall a: Set, b: [Box]Box, t: Ty, bx: Box ::
  { Map#Elements(Map#Glue(a, b, t))[bx] }
  Set#IsMember(Map#Domain(Map#Glue(a, b, t)), bx) ==> Map#Elements(Map#Glue(a, b, t))[bx] == b[bx]);
```

and likewise for `IMap#Glue`, although I found no program that reaches its axiom.
`dafny4/UnionFind.dfy`'s `Main` is one VC whose cost already varies from 12M to 68M across random
seeds; with this change the default seed needs 53M, over the tests' 50M limit, so `Main` gets
`{:isolate_assertions}`, as `Join` did in #6478.

### How has this been tested?

`git-issues/git-issue-6535.dfy` is the lemma above. Over the 844 proofs in the lit tests and
standard library whose verification conditions this changes, cost changes by +0.8% (geometric
mean of per-proof ratios, 5 random seeds, Z3 4.16.0; 95% interval -0.1% to +1.8%).

This change was prepared with an AI assistant (Claude Code).

<small>By submitting this pull request, I confirm that my contribution is made under the terms of the [MIT license](https://github.com/dafny-lang/dafny/blob/master/LICENSE.txt).</small>
````

If the guard stays `Set#IsMember(a, bx)`, use that axiom in the description and "+2.0% (95%
interval +0.8% to +3.4%)" in the test sentence.

## Review comments, ready to post

1. `Source/DafnyCore/Prelude/PreludeCore.bpl`, the new `Map#Glue` axiom: Consider guarding with
   `Set#IsMember(Map#Domain(Map#Glue(a, b, t)), bx)`, which equals `Set#IsMember(a, bx)` by the
   axiom above. With `IMap#Glue`, use `IMap#Domain(IMap#Glue(a, b, t))[bx]`. It is measurably
   cheaper. Over the 844 affected lit/stdlib proofs (5 seeds, Z3 4.16.0) it is +0.8% geomean over
   master instead of +2.0%. It also removes this PR's largest regressions: `dafny0/Maps.dfy`
   `GeneralMaps4` 2.96M → 0.18M (master 0.17M), `UnionFind`'s `Join` postcondition under the
   legacy resolver 31M → 8.9M (master 5.8M), and 16 nested comprehensions 2.30M → 0.33M. The
   geomean gain holds on Z3 5.1.0 (-0.9% vs this PR, 95% interval -2.0% to -0.1%). In
   `GeneralMaps4`, guarding with `a` (the comprehension's `Set#FromBoogieMap(lambda)`) takes Z3
   from 3,126 to 56,688 quantifier instantiations, nearly all in the key-projection axioms.
   Benchmark and data:
   https://github.com/fabiomadge/dafny/tree/review-pr6539-bench/Scripts/prelude-ab-bench
2. Same place, the comment: `b'` is not bound anywhere. Suggest one line:
   `// Inside the domain only: Map#Equal ignores elements outside it, so taking them from b there would be unsound.`
3. `git-issue-6535.dfy`: the lemma needs neither the precondition nor `Contradiction`
   (`Contradiction` verifies from `Bad`'s specification whatever the prelude says). A local
   `var s: set<int> := {};` still proves `false` under the old axiom for 12 of 12 seeds. The
   header comment tells history; the `// error: (but this was once provable, due to a bug)`
   marker covers that, and two end-of-line comments can say what the test does. Suggested file
   as above.
4. Description, `UnionFind.dfy`: "its largest VC is then about 17M (6M under the legacy
   resolver)" are the costs of `M3.UnionFind.JoinMaintainsReaches1` (16.95M / 6.27M), which
   `--filter-symbol Main` also selects. `Main`'s isolated VCs peak at 0.18M. Also, `Main` was
   already brittle: over 5 random seeds on master it costs 13.8–30.9M (refreshed) and 11.8–67.6M
   (legacy, one seed over the 50M limit). Master's axiom with its equation merely flipped costs
   77.1M at the default seed. So `{:isolate_assertions}` is right, but for that reason rather
   than because this axiom is weaker.
5. Description: `Map#Build`'s frame reads elements outside the domain, so "the other axioms that
   read the elements ... read them only inside the domain" should say "the others except
   `Map#Build`'s frame, which only carries them over", or be dropped.
6. Description: consider reducing it to the template, with the example inline (draft above).
   The testing details can go: they are in the fork's CI runs and in #6535.

## Side findings, not for this PR

- `dafny measure-complexity --mutations 2` crashes on
  `method M() { var c := map i: int | 0 <= i < 3 :: [i] := i; }` with "Boogie program had 3 type
  errors: invalid type for argument 0 in application of map$project$0#0#i#0: Seq (expected:
  Seq)". Apparently because `CreateMapComprehensionProjectionFunctions` caches the Boogie
  projection functions on the AST (`MapComprehension.ProjectionFunctions`), so the second
  translation reuses functions typed against the first translation's `Seq` declaration.
  `--mutations 1` is fine.
- `Source/DafnyCore/Prelude/expand.sh` is committed non-executable.
