# Review of dafny-lang/dafny#6543, "fix: say that every member of Map#Items is a pair"

PR head `c24a81114` (one commit, Ernie Cohen), base `5f717bf44` = current `master`. No reviews or
comments, no force-pushes. Evidence below was produced on Linux arm64 with this checkout's Dafny
built at `5f717bf44`, the prelude swapped with `--prelude`, and Z3 4.16.0, unless it says Z3 5.1.0
or Dafny 4.11.0.

## Verdict

Merge it, after small edits: one line of prelude comment instead of three, a one-line test
comment, and a description cut to the template. The fix is right, self-contained and cheap.
Whichever of this PR and #6545 merges second must regenerate `dafny0/SubsetTypes.dfy.expect`.

## What it does, and should it be done

The prelude defines membership in `Map#Items(m)` (and `IMap#Items(m)`) through the pair
projections of the unboxed item only, while `item` ranges over every `Box`. So a box that is not a
pair, but whose projections name a key and its value, is an item too. With
`Set#Card(Map#Items(m)) == Map#Card(m)`, the axioms then have no model. #6537's check reproduces:

| query (the background theory of #6537's `Base` lemma, `/prune:0`) | Z3 4.16.0 | Z3 5.1.0 |
|---|---|---|
| the axioms and #6537's term (Dafny 4.11.0's own prelude) | unsat | unsat |
| the same on `master` (also after `(push 1)`) | unsat | unsat |
| `master` without the `Map#Items` membership axiom | unknown | unknown |
| with this PR's prelude | unknown | unknown |
| control: the term with a genuine pair `#Make2(b1, b2)` | unknown | unknown |
| control: no term | unknown | unknown |

The PR adds a first conjunct to both axioms: `item == $Box(#Make2(_0($Unbox(item)), _1($Unbox(item))))`.
It holds of every item of a Dafny map, since `$Unbox($Box(p)) == p` and the destructors of
`#Make2`. It is also what was missing to prove facts such as `map[1 := 2].Items == {(1, 2)}`:
`git-issue-6537.dfy` gives `0 verified, 2 errors` on `master` (both resolvers) and on 4.11.0. With
this PR it gives `2 verified, 0 errors` (both resolvers).

It should be done. The inconsistency is not known to be reachable from a program: `.Items` has type
`set<(K, V)>`, so every member a program names is a pair. I did not search for such a program. But
the change is small and states only what is true. It makes `.Items` more complete, and it costs
almost nothing (below).

## Is this the right design

Yes:

- **Both directions need the conjunct.** The `<==` direction needs it for soundness. The `==>`
  direction is what proves `map[1 := 2].Items == {(1, 2)}`. Guarding only `<==` would fix the
  inconsistency without that gain.
- **There is no typed alternative.** A guard like `$IsBox(item, Tclass._System.Tuple2(..))` is not
  available: the prelude's `Map` carries no type arguments.
- **The conjunct uses only symbols the prelude declares** (`#_System._tuple#2._#Make2`,
  `_System.Tuple2._0`, `_1`). Going through the `Make2?` discriminator would need generated
  symbols and the unguarded `$Box($Unbox(x)) == x` axiom, which #6545 deletes.

Cost, at seeds 1–3, where runs are reproducible:

- **Reach:** of the 15 lit and standard-library programs that mention `Items`, the PR changes costs
  in 10, all under 1.4M RU.
- **Cost:** their passing VCs cost +0.4% in total, and +0.7% as a geomean of per-program geomeans.
  The largest per-program change is +2.1% (`git-issue-2380.dfy`).
- **Verdicts:** none of 756 (VC, seed) results changes at its own limit (`@ResourceLimit` where
  the declaration has one, else 50M).

## Scope

Self-contained. `IMap#Items` gets the same conjunct. `Map#Values` has no such hole: its member is
any box equal to some element. The other `Items` axioms are consistent with the new conjunct:
nonemptiness through `#Make2(k, v)`, the cardinality, and `$Is(Map#Items(v), TSet(Tuple2(..)))`.

## Up to date with master

Yes, the base is `master`'s tip. It merges cleanly with #6544 and #6539. With #6544 both PRs'
goldens stay right: SubsetTypes 761900, CoinductiveProofs 709865/56001.

It conflicts with #6545 in `dafny0/SubsetTypes.dfy.expect`: both edit its resource total. #6545
records 735600 / 83800. Built with all four prelude PRs merged (#6539, #6543, #6544, #6545,
#6545's C# change included), the test prints 736600 / 83800, so whichever merges second must
regenerate it. `git-issue-6537.dfy` still verifies with all four.

## Code, comments, tests

- **Regeneration:** `DafnyPrelude.bpl` regenerates from `PreludeCore.bpl` byte for byte, at the
  head and when merged with the siblings. Pre-existing: `Prelude/expand.sh` is committed `100644`,
  so `make check` fails until it is made executable.
- **Prelude comment:** three lines explain the conjunct; one is enough, e.g.
  `// item ranges over every Box; the first conjunct says that it is a pair.` The existing block
  comment above still says the axiom "relies on the two destructors for 2-tuples"; it now also
  relies on the constructor.
- **Test comment:** the test checks the gain, which also guards the conjunct: without it both
  assertions fail. Its five-line comment narrates the history. One line says what it tests:
  `// Every item of a map or imap is a pair, so these hold.`
- **Golden:** `SubsetTypes.dfy.expect`'s new total, 761900, is what the RUN line prints, the same
  in two runs. `master` prints 764300; the 13 verified and 91 errors are unchanged.
- **Release note:** accurate, and the same in kind as `RELEASE_NOTES.md`'s other "Fix soundness
  issue" entries.

Prototype of the comment edits: branch `review-pr6543` on fabiomadge/dafny (`d4016f73e`). It still regenerates
byte for byte. Through the xunit lit harness, `git-issue-6537.dfy` and `dafny0/SubsetTypes.dfy`
pass.

## Fact-check of the description and commit message

| claim | verdict |
|---|---|
| The axioms have no model (#6537's query), with the stated controls | ✓, Z3 4.16.0 and 5.1.0, `master` and 4.11.0 |
| The conjunct is a tautology for a genuine pair | ✓ (`$Unbox($Box(p)) == p`, the destructor axioms) |
| `DafnyPrelude.bpl` regenerates byte for byte | ✓ (after `chmod +x expand.sh`) |
| No Dafny program is known to prove `false` through the old axiom | not checked; consistent with `.Items: set<(K, V)>` |
| `map[1 := 2].Items == {(1, 2)}` did not verify and now does | ✓ (`master`, both resolvers, and 4.11.0: refused; PR, both resolvers: verifies) |
| SubsetTypes' total moves 764300 → 761900, verdicts unchanged | ✓ (Linux arm64; x64 and macOS not checked here) |
| The manual already describes `m.Items` as the set of pairs in `m` | ✓ (`docs/DafnyRef/Types.md:1643`) |
| The cited fork CI runs passed on this branch | ✓ (all five on `c24a81114`) |
| Upstream CI | ✓, every check passes on `c24a81114` |
| The verdict sweep of 1,092 programs changes only the new test | ✓ (run 36262477419: "1 of 1093 programs differ", `git-issue-6537.dfy`) |
| "Compared test by test … the only change is `git-issue-6537.dfy`" | not re-derived; consistent with upstream CI passing |
| The local macOS runs | not reproducible here |

## Benchmark (`Scripts/prelude-ab-bench`)

One Release build of `master`, with this PR's prelude swapped in by `--prelude`, Z3 4.16.0, at
Boogie seed 1, where two runs of `master` give every VC the same resource count (Dafny's default
seed, 0, does not). The corpus is 2,077 programs: every lit and standard-library program, Kondo's
and DafnyBench's 41, and the 90 files of dafny-lang/libraries. The PR changes the cost of 1,638 VCs.
Over the 1,570 of them that are proofs, in 156 programs, it costs +0.5% [+0.1, +1.2] per program
(each program weighs the same; 95% bootstrap intervals that resample programs): lit +0.1%
[-0.2, +0.3] (108 programs), the standard library +1.5% [-0.1, +4.1] (16), dafny-lang/libraries
+0.4% [+0.1, +0.5], Kondo +0.1% [-0.4, +0.4], DafnyBench +6.8% [-0.2, +18.1] (7).

At seed 1, six VCs change verdict at their limit, all in Kondo's Paxos proofs. Re-run at seeds 1 to
4 with a placebo (`master`'s two conjuncts in the other order), they are brittle: the placebo
changes as many verdicts there as the PR does (four each), and one VC that passes at 3 of 4 seeds
on `master` passes at none under either. On those two programs the PR costs -2.2% per program, the
placebo -0.2%.

## Suggested title, commit message and description

Title: keep it.

Commit message:

```
fix: say that every member of Map#Items is a pair

The membership axioms of Map#Items and IMap#Items spoke only of the pair
projections of the unboxed item, so they also admitted boxes that are not
pairs, and the axioms had no model. Each now says that the item is a pair.

Fixes #6537
```

Description:

````
Fixes #6537

### What was changed?

The prelude axioms for membership in `Map#Items(m)` and `IMap#Items(m)` spoke only of the pair
projections of the unboxed item, so a box that is not a pair, but whose projections name a key and
its value, was an item too, and the axioms had no model (the query in #6537 is refuted). Each
axiom now also says that the item is a pair:

```boogie
item == $Box(#_System._tuple#2._#Make2(_System.Tuple2._0($Unbox(item)), _System.Tuple2._1($Unbox(item)))) &&
```

That is true of every item of a Dafny map, and it is what was missing to prove

```dafny
assert map[1 := 2].Items == {(1, 2)}; // refused on master, verifies with this change
```

### How has this been tested?

`git-issues/git-issue-6537.dfy` checks that assertion for a `map` and an `imap`. The resource
total that `dafny0/SubsetTypes.dfy` records moves (764300 to 761900); its verdicts do not.
````
