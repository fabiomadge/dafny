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
CPU times, resource units and memory under both solvers), `soundness/` (the query and its cores).
