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

## Options

`--enum-inst` proves 26 of the 30 queries cvc5 gives up on and 2 of those at the limit, in a median
0.1 s, and costs nothing on 217
random queries both prove (0.92x geomean, 0.98x total, no proof lost). `--mbqi` proves 32 (median 1.4 s,
1.15x total). Neither helps the limit cases: all options together prove 10 of 267 (`options.txt`).

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

All fourteen together prove 28 (22%). None reaches the arithmetic libraries; `--nl-ext=none` and `light`
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
| portfolio: default and eager definitions | 21 | 15 | 0 / 0 | 8 | 44 |
| rewritten proofs (`proof-fixes.patch`) | | | | 19 | 57 |
| rewritten proofs, eager definitions | | | | 19 | 47 |
| rewritten proofs, portfolio | | | | 19 | 41 [b] |

[a] At a higher machine load than the other runs. [b] From two runs at different loads.

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

**A portfolio** - the default and the eager encoding run side by side, the first proof wins - keeps every proof
either one finds, so nothing is lost by construction: in the whole library 76 failing VCs become 55 without touching
a proof, and 41 with the rewritten proofs, at up to twice the solver time. On the screens, pairing the eager
definitions with every synonym inlined proves 41 of the 53 lambda-induction misses and 27 of the 118 other misses,
again keeping all 320 controls.

Extending beta-reduction to lambdas bound to a variable (`var f := u => ...`, the form the Power lemmas use) fixes
one more lemma under cvc5 (`LemmaModNegNeg`) and breaks two under Z3 (`LemmaPowIncreases`, `LemmaMulDistributes`).

So the encoding is a large part of why cvc5 fails these proofs: the synonyms, related to their operators only by
quantified axioms, need instances that cvc5 does not find. The eager definitions supply part of them without changing
a trigger, and a portfolio makes the change free of regressions. The rewrites remain the only single change that
fixes all 19 lambda inductions with nothing lost under either solver; the eager definitions and the portfolio add to
them.

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
`stdlib-vcs.csv.gz`
(every standard-library VC's outcome, and Z3's resource count, for the original library, the rewritten
one and the original under the prototype, under both solvers, and the cvc5 runs of the encoding table).
