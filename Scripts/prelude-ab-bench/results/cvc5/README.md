# cvc5 1.4.1 as Dafny's solver

Dafny `master` at `5f717bf44` (Release build, Boogie 3.5.5) with Z3 4.16.0, the version CI uses, against
cvc5 1.4.1 (2026-09-25, the static arm64 release build). The corpus is the public one of
`results/series`: 2,077 jobs (every lit test's first RUN line, the standard library, dafny-lang/libraries,
Kondo, DafnyBench), Boogie seed 1. 1,387 programs pose 26,922 queries.

## Out of the box, cvc5 does not work

Boogie 3.5.5 drives cvc5 (`--solver-option SOLVER=cvc5`), but three bugs stop Dafny before proving
power matters:

1. **A VC that cvc5 does not prove ends the program's verification.** Dafny's `--extract-counterexample`
   binding sets `EnhancedErrorMessages = 1` whatever the option's value (`CommonOptionBag.cs`), so Boogie
   asks for a model after every failure. Boogie's model converter has no case for `Real` values, and
   cvc5's `0.0` (the prelude declares `real_pow`) throws `BadExprFromProver`, which stops the rest of the
   program: `dafny0/Maps.dfy` reports 6 of its 67 VCs. `--boogie /enhancedErrorMessages:0` does not help.
   548 of the 1,387 programs have a query that cvc5 does not prove.
2. **`bv2int`.** `AddBitvectorNatConversionFunction` emits Z3's name; cvc5 accepts `bv2nat` or
   `ubv_to_int`. The queries of 40 jobs (260 queries) fail to parse.
3. **Batch mode.** With `-proverOpt:BATCH_MODE=true`, Boogie sends `(get-model)` after every
   `(check-sat)`; after `unsat`, cvc5 answers with an error and every VC is inconclusive. No public job
   uses batch mode.

Boogie also sends cvc5 no time limit, resource limit or seed (pass `--solver-option C:--tlimit-per=<ms>`),
and reports no resource count for it.

The numbers below come from a build with two patches: `if (value)` around that binding, and
`options.IsUsingZ3() ? "bv2int" : "bv2nat"`. Under Z3 the patched build proves exactly what `master`
proves (4,811 of 4,811 VCs in a 150-job pilot; -0.1% wall-clock time per program).

## Proving power

Each query is replayed in its own solver process, under a 60-second CPU-time limit (see Method).

| | cvc5 proves | cvc5 gives up | cvc5 at the limit |
|---|---:|---:|---:|
| Z3 proves (24,715) | 24,392 (98.7%) | 30 | 293 |
| Z3 does not (2,207) | 38 | 2,073 | 96 |

- Of the 917 programs whose every query Z3 proves, cvc5 proves every query of 830.
- cvc5's misses are mostly the limit, on queries Z3 finds easy (median 0.09 CPU-seconds): nonlinear
  arithmetic (`DivMod`, `Mul`, `Power`, `ModInternals`, `LittleEndianNat`, in the standard library and in
  dafny-lang/libraries), `Std/Actions/Producers.dfy`, a few lit tests. Re-run at lower load with twice
  the limit, 1 of the 293 limit cases finishes within 60 CPU-seconds and 27 within 120; 266 run out again.
- Of the 38 queries only cvc5 proves, 33 are true facts that Z3 misses: the `wishlist` and trigger tests,
  `dafny0/IndexIntoUpdate.dfy` (marked "FIXME: This should verify"), assign-such-that witnesses that are in
  scope, and `dafny0/Fuel.dfy`'s fuel and opacity tests (cvc5 is not held back by fuel). The other five are
  false.

## cvc5 proves `false` in four lit tests

Under cvc5, `HigherOrderIntrinsicSpecification/ReadPreconditionBypass1.dfy` to `4.dfy` verify completely,
`ensures false` included, where each test expects its precondition errors. This is not a cvc5 bug: cvc5
checks its own proof (`--check-proofs`), and Z3 4.16.0 also answers `unsat` on the 34 assertions of Dafny's
query that cvc5's unsat core keeps (`soundness/`, from `ReadPreconditionBypass1.dfy`'s `Main` at Dafny's
default seed).

The contradiction is in the encoding. `myf`'s reads clause, `reads o.inner`, reads `o.inner` without `o`,
which Dafny accepts because `myf` `requires false`. Yet the axiom that defines `Reads1` for `myf`'s handle
holds unconditionally, and the frame axiom of `Reads1` (heaps that agree on a function's reads set agree on
the reads set) then makes the reads sets `{inner1}` and `{inner2}` of two heaps that differ only in
`outer.inner` equal. Z3 does not find the contradiction in the whole query, only in the core. It is present
with #6545's prelude too.

## Time

Measured as work, user-space instructions (`perf stat`), which do not depend on the machine's load.
Inside Dafny a solver process is reused and, after each `(reset)`, re-reads the prelude, so the work a VC
costs is its whole query less the solver's startup.

| queries both prove (stratum by Z3's CPU time) | queries | cvc5 / Z3 per program [95%] | 10th, 50th, 90th percentile over queries | cvc5 cheaper | by cycles |
|---|---:|---|---|---:|---|
| a random sample | 999 | **3.98x** [3.78, 4.19] | 2.7x, 3.5x, 7.2x | 0% | 4.0x |
| Z3 0.1 to 0.3 s | 194 | 7.5x [5.2, 11.2] | 3.0x, 3.6x, 17x | 0% | 9.2x |
| Z3 at least 0.3 s | 240 | 3.4x [2.1, 5.4] | 0.44x, 5.9x, 30x | 23% | 4.1x |

On the random sample both solvers execute about 1.8 instructions per cycle, so its instruction ratio is
a time ratio; on the larger queries cvc5's rate is lower, and the cycle ratios are the better guide.
Counting only the VC beyond the prelude, the random sample's ratio is 6.0x [5.7, 6.4]. So on the small
queries that make up most of a program, cvc5 always does more work, typically 3 to 7 times Z3's. On the
heavy ones it varies most: cheaper on almost a quarter of them, at least 15 times costlier on a quarter,
at least 30 times on a tenth. These ratios leave out the 1.3% of queries that cvc5 does not prove
within the limit.

Timing whole processes understates the difference: starting a solver costs either about 12.5 ms of CPU
time, mostly in the kernel, about as much as a typical query's own work under Z3 (a median of 51 million
instructions), and that shared cost pulls the ratio toward 1 (1.67x per program on the same sample). The
main replay's cvc5 times also include printing its statistics, which it needs to report resource units
(about 1.2 x 10^8 instructions per query).

## Where cvc5's work goes

Not in the mode Boogie runs it in, and not in one part of cvc5 that an option turns off. Summed over 200 queries of the
random sample, cvc5's own timers (`--stats-internal`) put 45% of its time in quantifier instantiation (30% in
conflict-based instantiation, `--cbqi`, and 7% in e-matching), 12% in the UF solver, 6% in preprocessing, 6% in the
decision heuristic and 4% in CNF conversion. The instruction sample, replayed under other modes (user instructions less
each mode's startup; `modes.csv.gz`):

| cvc5 | vs Z3 per query, random sample (geometric mean) | random sample, total | proofs lost of 1,434 |
|---|---:|---:|---:|
| as Boogie runs it (`--incremental --produce-models`) | 4.05x | 7.1x | |
| `--no-produce-models`, or `--no-cegqi` | 4.05x | 7.1x | 0 |
| `(set-logic AUFBVDTNIRA)` instead of `ALL` | 4.02x | 7.1x | 11 (floating-point tests no longer parse) |
| without `--incremental` (the VC's `push` dropped) | 3.83x | 6.6x | 1 |
| `--cbqi-mode=conflict` | 3.97x | 5.4x | 3 |
| `--no-cbqi` | 3.78x | 3.8x | 10 |
| `--ieval=off` | 3.85x | 6.2x | 10 |
| `--no-cbqi --user-pat=strict --simplification=none` | 3.49x | 4.3x | 14 |
| the same without `--incremental` | 3.43x | 3.7x | 9 |
| the same with `--ieval=off` (and `--incremental`) | 3.33x | 3.6x | 16 |

A proof lost is one the default mode finds within 60 CPU-seconds and the mode does not, in both of two replays; a few
are queries near the limit in every mode. Conflict-based instantiation is the one large part: without it the total
falls by about 40%, mostly on heavy queries, but a typical query by 7%, and proofs are lost. Instantiation evaluation,
12% of cvc5's time in the profile below, saves 5% of a typical query's work when turned off and costs the heavy
queries more (1.08x over all 1,434). With every option that saves work, a typical query still costs cvc5 3.3 to 3.5
times Z3's work.

## Closing the gap

The other candidates, measured on 200 queries of the random sample (`relevance.csv.gz`):

- **Not the axioms alone.** Boogie's pruning leaves a median 86 assertions in a query; cvc5's unsat core keeps 11 of
  them, Z3's 3. On its own core cvc5 does a quarter of its work on the full query, as much as Z3 does on the full query
  (1.03x per query, 0.80x in total). But Z3 gains nearly as much from its own core (0.33x), and given the same
  assertions, Z3's core, cvc5 does 2.97x Z3's work per query (9.8x in total; it still proves 197 of the 200) and is
  never cheaper: reading the script costs it 1.8 times Z3's work, checking it 10.5 times.
- **No filter finds the core.** Keeping only the axioms whose patterns e-matching could fire (every symbol of one
  pattern reachable from the VC and the axioms kept so far) keeps all of them: Boogie's pruning already does as much.
  SInE axiom selection, which spreads relevance through each axiom's rarest symbols, keeps 61% to 96% of the
  assertions and loses 35 to 3 of the 200 proofs; at its most selective cvc5 still does 2.3 times Z3's work.
- **Not a fixed cost.** A trivial check costs either solver 11 to 14 million instructions beyond its startup, paid
  again after each `(reset)`, which Boogie sends between VCs; a `push` and `pop` instead cost either about 1 million.
- **No hotspot.** cvc5 1.4.1 built with symbols (the same answers as the release binary on these queries, and within
  5 to 8% of its instructions) has a flat profile (`profile-*.txt`, 60 queries): memory allocation 9%; building,
  hashing and looking up terms and their attributes about 12%; the equality engine 5%; flushing the output after each
  command 2%. Inclusively, checking takes 69% (conflict-based instantiation 18%, of it instantiation evaluation 12%),
  the `(push 1)` before the VC 21%, preprocessing 16% (substitution 9%), CNF conversion and registering terms 10%
  (rewriting each quantifier as it is registered 7%), and parsing 9%.

So no change on Dafny's side makes cvc5 competitive: the difference is how much cvc5 does per term and per axiom,
throughout. Re-verification could send cvc5 only the assertions an earlier proof used (Boogie can already ask a solver
for an unsat core over named facts): on Z3's core cvc5 does 0.98x the work Z3 does on the full query (0.78x in total).
But a VC whose proof then needs more than the old core has to be sent again in full, and Z3 gains nearly as much from
the same pruning.

## Making cvc5 itself faster

Changes to cvc5 itself help, though not enough (`speedups.csv.gz`). On the 1,000 random queries, against Z3 replayed
alongside:

| cvc5 | instructions | cycles | vs Z3 per query: instructions | cycles | proofs lost |
|---|---:|---:|---:|---:|---:|
| the release binary | 1 | 1 | 4.05x | 4.69x | |
| built from source, flushing its output only when a client waits on it | 1.02x | 1.02x | 4.15x | 4.79x | 0 |
| ... linked with jemalloc | 0.88x | 0.93x | 3.56x | 4.33x | 0 |
| ... built with profile-guided optimization | 1.00x | 0.94x | 4.05x | 4.43x | 0 |
| ... both | 0.85x | 0.83x | 3.46x | 3.91x | 0 |
| ... both, with `--no-cbqi --user-pat=strict --simplification=none` | 0.74x | 0.69x | 3.01x | 3.22x | 2 |

The builds are cvc5 1.4.1 (`configure.sh unrestricted --auto-download --static --no-static-binary -DBUILD_GMP=1`, GCC
11.5) with `cvc5-flush-when-waited-on.patch`, which flushes the output after a failure, `check-sat*`, `get-*`, `echo`
or any command under `print-success` instead of after every command (2% of the profile); Dafny verifies and reports
errors through it as before. The profile-guided build is trained on 300 other queries of the corpus under
`--no-early-exit` (by default cvc5 ends with `_exit` and writes no profile); jemalloc is preloaded. The other 28
options screened on 200 queries save at most 2% each.

The faster build proves 18 of the 323 queries Z3 proves and the release binary misses (the release binary, run in
the same session, 3): some now finish within the limit. The three options cost proofs. Replayed over the public corpus
next to the release binary, query by query:

| | release | the build, with the three options |
|---|---:|---:|
| queries Z3 proves (24,715) | 24,391 (98.7%) | 24,345 (98.5%) |
| programs Z3 proves completely (917) | 830 | 829 |
| work on the 24,315 queries both prove, per query (instructions) | 1 | 0.74x |
| CPU time | 9.6 h | 8.4 h |

They prove 67 queries the release binary does not and lose 114, half of them by giving up; `--simplification=none`
alone accounts for about half of the losses (`configs-*` in `speedups.csv.gz`). `--enum-inst` would add proofs at no
cost, but it is unsound here (below).

**Without rebuilding or patching cvc5.** The official shared build of 1.4.1 (`cvc5-Linux-arm64-shared.zip`) with
jemalloc preloaded (`LD_PRELOAD`; the build wants Debian's `libedit.so.2`, which a symlink to the system's
`libedit.so.0` satisfies, as cvc5 uses it only for its shell) does 0.95x the static release binary's instructions and
0.86x its cycles on the 1,000 random queries, with no proof lost: 4.03 times Z3's cycles per query instead of 4.69.
Over the public corpus, next to the static release binary, it proves 15 more of Z3's queries (24,402) and 4 more
complete programs (834), and loses none (`corpus-stock` in `speedups.csv.gz`). Adding `--user-pat=strict` (0.80x
cycles on the sample) proves 23 more of Z3's queries than the release binary but 3 fewer complete programs: it gives
up on 12 queries the release binary proves and runs out of time on 36.

**Axioms held back until they can match.** On a typical query cvc5 never instantiates 40 of the 65 axioms, and
without them it does half the work (0.50x per query, 199 of 200 still proved; 0.51x with `--no-cbqi` on both sides;
`unused-axioms-*` in `relevance.csv.gz`). Its timers on 60 queries put the difference in preprocessing (30% of it:
substitution and non-clausal simplification, which visit every axiom), CNF conversion and registering terms (17%), and
instantiation (18%): cvc5 pays for every axiom up front. Dafny cannot tell which axioms will be used: a simulation of
e-matching over the query's terms (`../../cvc5enc/ematch.py`) drops 64% of the axioms but loses 15% of the proofs on
the 1,000 queries, and Z3 gains as much from the same filter (0.69x). cvc5 can: `cvc5-lazy-axioms.patch` (against
cvc5 1.4.1, with the flush change; on with `CVC5_LAZY_AXIOMS=1`) holds back each input axiom asserted before the first
`push` whose bound variables are all of uninterpreted sorts and whose patterns are applications of uninterpreted
functions, and releases it as a lemma, with the top-level substitutions applied, once some ground term exists for every
function of one of its patterns. After 20 full-effort checks, and before it answers, it releases the rest, so a `sat`
or `unknown` is about the whole input; an axiom held back only weakens the problem, so an `unsat` stays sound. On the
1,000 random queries:

| cvc5 | instructions | cycles | vs Z3 per query: instructions | cycles | proofs lost |
|---|---:|---:|---:|---:|---:|
| built from source, with jemalloc | 0.88x | 0.84x | 3.56x | 3.93x | 0 |
| ... holding axioms back | 0.71x | | 2.87x | | 0 |
| ... and profile-guided (trained with axioms held back) | 0.69x | 0.62x | 2.79x | 2.91x | 0 |

Holding back axioms over any sort does more (0.67x), but over the corpus six queries the release binary proves in
about a second, under every seed, then run out of time. Keeping axioms with arithmetic or Boolean variables in place
restores five: other strategies instantiate those without a trigger match (bisecting one query found Dafny's
`INTERNAL_sub_boogie(x, y) == x - y`); in the sixth, holding back a function's definition axiom over `T@U`, whose
pattern terms occur in the VC, changes the search enough to lose a proof the release binary finds in 0.13 s. Other
variants did worse: releasing
everything at the first last-call round pre-empted the modules that run there and prove many queries; returning after
a release starved instantiation where axioms trickled out; checking that each axiom still is one quantifier after
rewriting costs a tenth of the gain (it rewrites the axioms that stay held back); and testing one level of each pattern
against the equality engine saves 4% more but runs out of time on about one query in 1,000. Replayed over the public
corpus next to the release binary, query by query:

| | release | the build with axioms held back |
|---|---:|---:|
| queries Z3 proves (24,715) | 24,387 (98.7%) | 24,399 (98.7%) |
| programs Z3 proves completely (917) | 830 | 834 |
| work on the 24,412 queries both prove, per query (instructions) | 1 | 0.69x |
| CPU time | 9.8 h | 9.1 h |

It proves 25 queries the release binary does not and runs out of time on 13 it proves: ten of those take the
release binary 34 to 52 s, close to the limit, and three take it 0.1, 0.3 and 8.8 s (the `LittleEndianNat` lemma
above, `Classics.dfy`'s `AdditiveFactorial`, `PriorityQueue.dfy`'s `SiftDown`). CPU time falls less than the work,
since the time-outs take two thirds of it. So cvc5 itself can be made to do two thirds of its work without losing
proofs: 2.8 times Z3's on a typical query, from 4.05. The rest of the gap is in how cvc5 builds, stores and processes
terms (allocation, hashing, attributes, the equality engine), spread too thinly to remove by one change.

## Options

`--enum-inst` proves 26 of the 30 queries cvc5 gives up on and 2 of those at the limit, in a median
0.1 s, and costs nothing on 217
random queries both prove (0.92x geomean, 0.98x total, no proof lost). `--mbqi` proves 32 (median 1.4 s,
1.15x total). Neither helps the limit cases: all options together prove 10 of 267 (`options.txt`). Neither can be
used: both make Dafny verify wrong programs (next section), so their proofs here, and the rows below that use them,
show nothing.

## Instantiation that ignores the patterns proves `false`

Boogie's arguments type encoding, the one Dafny selects, maps every value to one sort `T@U`, and for each built-in type
asserts that casting out and back in is the identity on all of `T@U`, unguarded:
`(forall ((x T@U)) (= (bool_2_U (U_2_bool x)) x))` (`TypeErasureArguments.cs`, `GenReverseCastAxiom`, which "makes use
of the assumption that only well-typed terms are generated by the SMT-solver"). With `int_2_U` injective this has no
model: `T@U` would have at most two elements and infinitely many. The patterns keep e-matching from it; instantiation
that does not follow them finds it (boogie-org/boogie#1168). The first assertion of every query, the encoding's, is
refuted on its own by cvc5 `--enum-inst` and `--mbqi` and by Z3 with MBQI, not by either solver as Dafny runs it.
Through Dafny, a program with two real errors (`ensures y > x` after `y := x`, and `assert s[0] < s[1]`):

| solver | Dafny |
|---|---|
| Z3 as Dafny sets it (`smt.mbqi false`) | 0 verified, 2 errors |
| Z3 with `smt.mbqi=true` | 1 verified, 1 time-out |
| cvc5 | 0 verified, 2 errors |
| cvc5 `--mbqi` | 2 verified, 0 errors |
| cvc5 `--enum-inst` | 2 verified, 0 errors |

On 24,552 of the public corpus's 26,922 queries (the replay was stopped there; `corpus-free` in `speedups.csv.gz`), the
faster build with `--enum-inst` proves 1,923 that Z3 does not (the release binary 38), 1,902 of them in lit tests that
expect their errors (`DefaultParameters.dfy` 71 queries, `SubsetTypes.dfy` 43, `SmallTests.dfy` 33). Under
`/typeEncoding:p`, which guards the cast by the value's type, the program's two VCs time out under cvc5 `--enum-inst`
instead, and Z3 loses one of six proofs of a small test program.

## Flags against proof changes

**Flags.** Fourteen option sets, each on one miss from each of the 125 programs with misses and on 120
random queries both prove, at 30 CPU-seconds:

| options | misses proved | control proofs lost | work on controls |
|---|---:|---:|---:|
| `--enum-inst --inst-when=last-call` | 19 | 0 | 1.02x |
| `--enum-inst --nl-cov` | 13 | 0 | 1.02x |
| `--enum-inst` | 12 | 0 | 1.02x |
| `--mbqi` | 10 | 0 | 1.03x |
| `--user-pat=strict` | 9 | 0 | 0.93x |
| `--simplification=none` | 5 | 1 | 0.95x |
| `--term-db-mode=relevant`, `--relevant-triggers`, `--multi-trigger-when-single`, `--nl-ext-tplanes` | 0 | 0 to 1 | 1.00x |

All fourteen together prove 28 (22%); the four rows with `--enum-inst` or `--mbqi` are void (above). None reaches
the arithmetic libraries; `--nl-ext=none` and `light`
do not help there either. On the 53 lambda-induction queries below, `--user-pat=use` (match patterns that
contain arithmetic, as Z3 does) proves none, and the best set, `--user-pat=use --enum-inst
--inst-when=last-call`, proves 6. Dafny's patterns use its arithmetic synonyms (`INTERNAL_add_boogie`),
so that cvc5 by default does not match `+` inside a pattern is not what stops it.

**Proofs.** Of the 177 library declarations cvc5 misses, 53 prove arithmetic facts by induction over a
lambda (`LemmaMulInductionAuto(m, u => ...)`): 17 in the standard library and 36 in dafny-lang/libraries,
its predecessor, left alone here. `proof-fixes.patch` rewrites every such proof in the standard library
outside the induction lemmas themselves, 36 lemmas in `Mul.dfy`, `DivMod.dfy`, `Power.dfy` and
`Power2.dfy`, and the induction in `MulInternals.LemmaMulDistributes`. Each becomes one to nine calls of
quantifier-free lemmas (`LemmaFundamentalDivMod`, `LemmaFundamentalDivModConverse`, `LemmaMulInequality`,
...), or a recursion where the fact is inductive (a new `LemmaDivPosIsDiv`). The whole library, before
and after (one build, seed 1; every VC in `stdlib-vcs.csv.gz`):

| | Z3, the library's limits | cvc5, 60 s per VC |
|---|---|---|
| VCs that fail | 4 -> 3 | 76 -> 57 |
| fixed | `LemmaFundamentalDivModConverse` (fails at seed 1 after 31.8M RU; now 16,925) | all 19 lambda inductions |
| broken | none | none |
| resources | 1,326M -> 1,283M RU (-3.3%); of the VCs that change by more than 10,000 RU, 43 are at least 10% cheaper and none 10% costlier | |

Four VCs elsewhere flipped between the cvc5 runs, two each way; both libraries give each of them the same
queries (Boogie's solver log differs only in its resets), so the flips are timing at the 60-second limit.
Of the rewritten lemmas' 41 VCs that Z3 proves in both libraries, 40 cost at least 2 times less, up to
407 times (`LemmaDivByMultipleIsStronglyOrdered`: 3,829,641 -> 9,410); one split of `LemmaModNegNeg`
costs 1,449 RU more. 51 more misses are `calc` chains over `/` and `%`, where cvc5 runs out even on a
step that cancels `+ n - n` (`ModInternals.HelperAddDenom`); those were not rewritten (the eager definitions below
prove it and eight more). An upstream
change would also need the library's `.doo` rebuilt.

**Translator.** `beta-reduce-lambda-args.patch` tries the implementation side, behind
`DAFNY_BETA_LAMBDA_ARGS=1`. Without it, Boogie substitutes a lambda argument's encoding into the callee's
specification, and the solver has to reduce `Apply1(..., Lit(AtLayer((lambda ly :: Handle1(...)), ...)),
$Box(e))` before the lambda's body takes part in the proof. With it, for a call to a lemma that passes a
lambda literal without `requires` or `reads`, Dafny checks the callee's preconditions itself, with each
application of the lambda replaced by its body, makes the Boogie call `free`, and assumes the
postconditions in the same form. It drops the triggers that mention the lambda's formal, whose reduced
form need not be a trigger (`LemmaMulInduction(i => x * i == i * x)` would get `x * i == i * x`). On the
original library:

- cvc5 proves 9 of the 19 lambda inductions (`Mul` 4 of 5, `DivMod` 5 of 10, `Power` and `Power2` 0 of
  3, `LemmaMulDistributes`, which passes a variable rather than a literal, 0 of 1), each confirmed alone:
  76 -> 67 failing VCs, with two timing flips.
- Z3 needs 1.3% fewer resources, and 18 VCs at least 10% fewer, and proves `LemmaFundamentalDivModConverse`
  at seed 1, but loses `LemmaRemainder`, a division induction: it fails at 4 of 5 seeds, where without the
  prototype it passes at all 5 (about 150,000 RU).

So the lambda's encoding is one obstacle; the other is the induction's arithmetic over the `MulAuto` and
`DivAuto` quantifiers, and putting the reduced terms into the query from the start changes Z3's search
enough to lose a proof. The rewrites fix both solvers; the prototype would need its Z3 regression
understood before it could be proposed.

## Why cvc5 fails the lambda inductions

A lambda induction (`LemmaMulInductionAuto(x, u => P(u))`) leaves the induction step to the solver: to prove
`P(i) ==> P(i + 1)` it has to instantiate the quantifiers of `MulAuto` or `DivAuto` (commutativity,
distributivity, the facts about `/` and `%`) at terms that only appear after earlier instances. Z3 finds that chain;
cvc5 does not. The rewrites work for both solvers because every lemma call is an instance with explicit arguments.
Three measurements, on beta-reduced queries of lemmas the prototype does not fix:

- **The instances.** Z3 refutes `LemmaRoundDown` with 97 instances of 33 quantifiers, out of the 2,357 it makes;
  49 of them only connect Dafny's arithmetic synonyms to their operators (`INTERNAL_add_boogie(x, y) == x + y`).
  cvc5 instantiates about as often, 1,783 times in 20 s, and gives up. Given Z3's instances as ground facts it
  proves the query in 4.7 s; with any one family of them withheld (synonyms, library facts, prelude), not within
  60 s. The gap is in finding the instances, not in the reasoning about them. Withholding one quantifier's
  instances at a time, cvc5 finds the instances of 28 of the 33 itself, `MulAuto`'s and `DivAuto`'s facts among them;
  what it cannot find are the instances of four synonym definition axioms (`+`, `mod`, `div`, `<`) and of
  `DivPlus#canCall`, whose trigger is a synonym term.
- **The schedule.** `LemmaMulEqualityConverse` runs out after 120 s under cvc5's default
  `--inst-when=full-last-call` (34,569 decisions and 64 conflicts in 30 s), but is proved in 5.6 s with
  `--inst-when=full` and in 0.3 s with instantiation capped at 10 rounds: the instances it needs come early, and
  later rounds bury the conflict.
- **The synonyms.** Dafny's prelude declares the synonyms as functions with bodies, which Boogie turns into
  quantified definition axioms, so that triggers can mention arithmetic. cvc5 reaches an operator only by
  instantiating that axiom. With the synonyms as definitions instead, it proves `LemmaMulEqualityConverse` in
  0.1 s and `LemmaRoundDown` in 14 s; its arithmetic rewriter, which puts products into a normal form, can then
  settle `MulAuto`'s commutativity and distributivity by itself.

## Changing the encoding instead

Each change with the original proofs, on the screens' 53 lambda-induction queries, 118 other misses and 120
controls, and on 200 random queries both solvers prove that contain synonyms (30 CPU-seconds each); and on the whole
standard library (60 s per VC, seed 1; each group of runs next to its own baseline, all columns in
`stdlib-vcs.csv.gz`). A placebo (the same queries with the background assertions in reverse order) shows the noise:

| cvc5 | lambda misses (53) | other misses (118) | controls lost (120 / 200) | library: lambda inductions proved (19) | library: other VCs failing |
|---|---:|---:|---:|---:|---:|
| default | 0 | 0 | 0 / 0 | 0 | 57 to 58 |
| placebo | 2 | 1 | 1 / 0 | | |
| beta-reduction of lambda arguments (`beta-reduce-lambda-args.patch`) | | | | 9 | 57 |
| `--inst-when=full` | 23 | 15 | 1 / - | 8 | 162 [a] |
| every synonym inlined | 39 | 16 | 4 / 7 | 13 | 107 |
| comparisons inlined (`cvc5-comparison-synonyms.patch`) | 20 | 2 | 0 / 0 | 9 | 61 |
| eager definitions (`../../cvc5enc/`) | 21 | 15 | 0 / 0 | 8 | 49 |
| portfolio of the default, eager definitions, every synonym inlined, comparisons inlined (`cvc5enc/cvc5portfolio.py`) | 43 | 27 | 0 / 0 | 17 | 40 |
| the portfolio, with beta-reduction | | | | 18 | 39 |
| rewritten proofs (`proof-fixes.patch`) | | | | 19 | 57 |
| rewritten proofs, eager definitions | | | | 19 | 47 |
| rewritten proofs, the portfolio | | | | 19 | 40 |

[a] At a higher machine load than the other runs.

**Inlining** Dafny's synonyms (`{:inline}`) gives cvc5 the operators directly, but every trigger that mentions
arithmetic then becomes a pattern over interpreted operators (`{:trigger (x + y) / n}` becomes `(div (+ x y) n)`):
62 VCs of the arithmetic library that pass today fail, 24 more of them as give-ups. The comparisons never occur in
patterns, and inlining only them loses none of the 320 replayed controls; still, in the whole library six lemmas of
`DivMod` and `ModInternals` then time out, and so do two of the rewritten lemmas, each confirmed alone. Variants that
inline the synonyms inside formulas while keeping the triggers (with the synonym terms kept alive by equalities) lose
4 to 14 of the 320 controls, and `--inst-when=full` on top of them is the strongest single change on the screens
(40 of the 53) but loses 8.

**Eager definitions** keep Dafny's encoding as it is - the synonyms stay in every term and trigger - and give every
Boolean atom that mentions a synonym the synonym's definition (`INTERNAL_add_boogie(a, b) == a + b`) in the atom's
own scope: `(and P D)` where it is asserted or in mixed polarity, `(=> D P)` where it is refuted. Each definition
follows from the definition axioms, which stay, so the query means the same; but cvc5 no longer has to instantiate
those axioms to connect a synonym to its operator, which is where the leave-one-out above found it stuck. It is the
only change measured that loses none of the 320 replayed controls and gains more than it loses in the whole library:
16 declarations, each confirmed alone, 7 lambda inductions and 9 other arithmetic proofs that cvc5 could not do
before, mostly `calc` chains (`ModInternals.HelperAddDenom`, `LemmaDivDenominator`, `LittleEndianNat.LemmaSeqAdd`), against 4 lost
(`LemmaPowAuto`, `LemmaPowModNoopAuto`, `LemmaModMulEquivalent`, `LemmaMulModNoopLeft`), and 2 lost in the rewritten
library. With the definitions in the VCs only, 11 of the 16 gains remain and 1 of the 4 losses. Combined with
beta-reduction it does worse in the whole-library run (6 of 19, 12 lost). For Z3 the same change breaks `LemmaRoundDown`, so it is for cvc5
only. It is measured through a proxy between Dafny and cvc5 (`cvc5enc/cvc5proxy.py`, `HYBRID_MODE=eager
HYBRID_SCOPE=all`); in Dafny it would be a pass over the Boogie program, or over the SMT text, for solvers other
than Z3.

**A portfolio** runs several encodings of the same query side by side, and the first proof wins, so one that
includes the unchanged query loses no proof that cvc5 finds alone. The encodings complement each other: of the 19
lambda inductions, some configuration measured in the whole library proves 18 (all but `LemmaHoistOverDenominator`).
`cvc5enc/cvc5portfolio.py` is such a portfolio, standing in for cvc5 under Dafny: an ordinary cvc5 session gets every
command unchanged and answers whatever Boogie asks after a check-sat, and at each check-sat fresh cvc5 processes get
the same query with the eager definitions, with every synonym inlined, and with the comparisons inlined. In the whole
library, next to a baseline run under the same load, it proves 17 of the 19 lambda inductions with the original
proofs, 18 with beta-reduction (the members' runs predicted 18), and all 19 with the rewritten proofs; the failing
VCs go from 76 to 42, 40 and 40. It lost one VC, a `JSON` well-formedness batch that times out alone either way; the
gains sampled alone (9 of 37, in the configuration that claimed them) all hold. It costs up to four solver processes
per open VC.

**The portfolio on the public corpus.** Its other three members, replayed on the 323 queries Z3 proves and plain cvc5
misses, on the instruction sample, and on queries neither solver proves (all 96 on which plain cvc5 runs out of time,
and 200 random ones of the 2,073 on which it gives up; 60 CPU-seconds each; every replay in
`portfolio-members.csv.gz`):

| | plain cvc5 | portfolio |
|---|---:|---:|
| queries Z3 proves (24,715) that cvc5 proves | 24,392 (98.7%) | 24,495 (99.1%) |
| programs Z3 proves completely (917) that cvc5 proves completely | 830 | 849 |

The members rescue 103 of the 323 misses (the eager definitions 61, every synonym inlined 76, the comparisons inlined
35), and prove five queries of library lemmas that Z3 does not prove in the replay (`Lemma2To64` in all three copies,
`LemmaModAddDenominator`, `LemmaMultiplyDivideLt`), all five among plain cvc5's time-outs; they prove none of the
sampled give-ups. Where a member proves a query plain cvc5 proves, its work is plain cvc5's (0.99x to 1.01x). Work
against Z3 (user instructions less startup):

| design | per query, random sample (geometric mean) | random sample, total |
|---|---:|---:|
| plain cvc5 | 4.05x | 7.1x |
| parallel portfolio (all four members at once) | 15.8x | 25.4x |
| fallback portfolio (the others only when plain cvc5 gives up or runs out of time) | 4.05x | 7.1x |

The fallback costs extra only where plain cvc5 does not prove the query. Plain cvc5 spends 9.9 CPU-hours on the corpus
(Z3 1.1 in the same replay), 6.5 of them on the 389 queries that reach the 60-second limit; giving up takes it a median
0.07 s. With the other members capped at 60, 20 or 10 seconds each, the fallback adds 148%, 53% or 28% to plain
cvc5's CPU time (the sampled give-ups scaled up to all 2,073) and rescues 103, 92 or 88 of the 323 misses; triggering
it only on time-outs saves almost nothing more. The parallel portfolio's wall time per VC in the whole library equals
the plain run's (0.97x), and the eager encoding's Python rewrite costs a median 24 ms per query.

Extending beta-reduction to lambdas bound to a variable (`var f := u => ...`, the form the Power lemmas use) fixes
one more lemma under cvc5 (`LemmaModNegNeg`) and breaks two under Z3 (`LemmaPowIncreases`, `LemmaMulDistributes`).

So the encoding is a large part of why cvc5 fails these proofs: the synonyms, related to their operators only by
quantified axioms, need instances that cvc5 does not find. No single encoding fixes that without costing proofs
elsewhere, but a portfolio of them does: without touching a proof, it brings cvc5 to 18 of the 19 lambda inductions
and 40 failing VCs in the standard library, against 57 with the rewritten proofs alone. The rewrites remain the only
change that also suits Z3, and the only one that needs no extra solver time.

## Method

- **Not wall clock.** The shared host ran at load averages up to 364 on 64 cores, so durations and
  wall-clock limits measured the machine. `run.py --solver-log-root` logs every query each solver gets,
  and `replay.py` replays each in its own process and reads its CPU time from `wait4`.
- **Not resource counts across solvers.** Z3's rlimit and cvc5's resource units count different work.
- **CPU time is load-sensitive too, and includes process startup.** At the main replay's load averages,
  about 35 to 60, short queries took 2.2 (Z3) and 1.45 (cvc5) times their CPU time at load 20, and each
  process's CPU time includes a startup that Dafny pays once per process. The time ratios above therefore
  count instructions; the CPU times in `summary.md` and `report.md` (the main replay's) only rank queries.
- **Verdicts are deterministic.** Replayed twice, 500 random queries give the same answers and the same
  resource counts under both solvers. Z3 replays give the Dafny runs' verdicts, and for most VCs the
  same resource counts.

Files: `summary.md` and `report.md` (main replay), `options.txt`, `instructions.csv.gz` (the instruction counts), `queries.csv.gz` (every query's answers,
CPU times, resource units and memory under both solvers), `soundness/` (the query and its cores),
`proof-fixes.patch`, `beta-reduce-lambda-args.patch` and `cvc5-comparison-synonyms.patch` (all against `master`),
`../../cvc5enc/` (the proxy and the query rewrites),
`portfolio-members.csv.gz` (the portfolio members' replays on the public corpus), `modes.csv.gz` (the instruction
sample under cvc5's other modes), `relevance.csv.gz` (both solvers on unsat cores and filtered queries),
`profile-self.txt`, `profile-self-core.txt` and `profile-inclusive.txt` (cvc5's profile), `speedups.csv.gz` (cvc5's
builds and option sets on the samples and the corpus), `cvc5-flush-when-waited-on.patch` and
`cvc5-lazy-axioms.patch` (against cvc5 1.4.1; the second includes the first),
`stdlib-vcs.csv.gz`
(every standard-library VC's outcome, and Z3's resource count, for the original library, the rewritten
one and the original under the prototype, under both solvers, and the cvc5 runs of the encoding table).
