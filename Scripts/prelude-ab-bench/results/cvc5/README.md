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
  dafny-lang/libraries), `Std/Actions/Producers.dfy`, a few lit tests. Re-run at low load with twice the
  limit, none of the first 68 limit cases finishes within 60 CPU-seconds, and 6 within 120.
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

On a random sample of 1,000 queries both prove, replayed at low load, cvc5 needs **2.43x** [2.29, 2.58]
Z3's CPU time per program (each program weighs the same), and 2.88x as a geomean over queries. On the
queries both need at least a second for, it needs 3.1x [2.0, 4.9] per program. A query's fixed cost (5th
percentile, low load) is 0.016 s for Z3 and 0.025 s for cvc5. 1,152 queries take cvc5 at least a second
where Z3 is 20 times faster; they make cvc5's total 5.1 times Z3's.

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
- **CPU time is load-sensitive too.** At the main replay's load averages, about 35 to 60, short queries
  took 2.2 (Z3) and 1.45 (cvc5) times their CPU time at load 20, so the main replay understates cvc5's
  cost by about 1.4x; the time
  ratios above come from the low-load sample. `summary.md` and `report.md` are the main replay's.
- **Verdicts are deterministic.** Replayed twice, 500 random queries give the same answers and the same
  resource counts under both solvers. Z3 replays give the Dafny runs' verdicts, and for most VCs the
  same resource counts.

Files: `summary.md` and `report.md` (main replay), `options.txt`, `queries.csv.gz` (every query's answers,
CPU times, resource units and memory under both solvers), `soundness/` (the query and its cores).
