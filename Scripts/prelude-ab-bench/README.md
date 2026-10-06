# Prelude A/B benchmark

Measures how a change to `DafnyPrelude.bpl` affects verification cost, by verifying the same
programs with one Dafny binary and swapping only the prelude (`--prelude`). Written to evaluate
dafny-lang/dafny#6539, which weakens the `Map#Glue`/`IMap#Glue` element axioms; the corpus and
the prelude variants are specific to that change, the runner, screen, classifier and report are not.

## Running it

```sh
dotnet build Source/Dafny/Dafny.csproj                 # the binary under test: Binaries/Dafny.dll
cd Scripts/prelude-ab-bench
python3 preludes.py --master origin/master --pr 074e49a64   # writes preludes/*.bpl
python3 synth.py                                       # writes synth/*.dfy

# 1. Screen: what does the change reach? Every lit test and standard-library file at one nonzero
#    seed, with an A/A run (master2) that marks the programs whose costs differ between identical runs.
python3 corpus.py work/screen.json litall stdall
python3 run.py work/screen.json work/screen --preludes master,master2,pr --seeds 1
python3 screen.py work/screen.json work/screen master pr master2 --seed 1

# 2. Classify the reached VCs: does their SMT contain the changed axiom, or is it only reordered?
python3 classify.py <reached-jobs.json> work/classes

# 3. Measure: several seeds, the controls, the alternatives.
python3 corpus.py work/jobs.json                       # lit, std, synth and unionfind jobs
python3 run.py work/jobs.json work/out --preludes master,master2,pr,pointwise,placebo,domguard --seeds 0,1,2,3,4,5,6,7
python3 report.py work/jobs.json work/out work/report.md work/vcs.csv --classes=work/classes/classes.csv
```

`run.py` resumes: it skips (job, prelude, seed) runs whose CSV exists, and kills a run after
`--run-timeout` seconds. `dafny.sh` runs `Binaries/Dafny.dll` (override with `DAFNY_DLL`) with core
dumps off; without `--solver` Dafny uses the `z3` next to it. To compare translators rather than
preludes, run each binary into the same output directory under its own name: `DAFNY_DLL=<binary>
run.py … --prelude-dir <dir> --preludes pr` reads `<dir>/pr.bpl`. `report.py` needs `master` and
`pr`; it reports a `placebo`, `master2` or any other variant when there are runs of it. `classify.py` keeps its solver logs
under `--log-root` (default `$TMPDIR/pab`), which must be short: Boogie shortens a log's name once
the whole path reaches 180 characters, and a shortened name no longer says which VC it is.

## What it measures, and what can go wrong

- **Controls.** `master2` is master again: its runs measure nondeterminism across processes (an
  A/A test). `placebo` flips the old axiom's equation: the same meaning in different text.
  `pointwise` is the PR's quantifier without its guard, keeping master's meaning, so master ->
  pointwise is what the PR's *shape* costs and pointwise -> pr what its *guard* costs.
- **Reach is not what the source mentions, and depends on the seed.** At seed 0, Dafny's
  default, a prelude change reorders the SMT of VCs that do not use the changed axiom, which
  moves their cost like any perturbation. #6539's seed-0 screen found cost changes in 76 lit and
  standard-library jobs, many without a map comprehension, and `classify.py` (one solver log per
  procedure, `--solver-log <dir>/@PROC@.smt2`) showed that most of those VCs never contain the
  axiom: 694 such VCs changed at seed 0. At each of seeds 1 to 7 the change moved the same 1,365
  or so VCs with the axiom, and 0 to 7 without it, no more than the A/A run. Seed 0 is also where
  identical runs differ most, from the order in which Boogie emits declarations: of the 192
  measured jobs, 27 differ between two runs of master at seed 0, and at most 7 at any other seed.
  So screen at a nonzero seed, with an A/A run, and classify the SMT; don't grep sources.
- **A screen only covers what runs.** `corpus.py` turns each lit test's first RUN line into
  `verify` flags. 25 of the 1,946 jobs still cannot run that way (tests of `build`, `run`, the
  auditor, formatting, or of CLI errors); none contains a comprehension.
- **VCs are not independent.** One program can contribute most of the VCs (`UnionFind.dfy`: 69%
  of #6539's affected proofs). The report's intervals resample programs, and "per program"
  weighs each program once; a VC-level bootstrap is several times too confident.
- **Seeds.** Each run repeats for Boogie `/randomSeed` 0 (Dafny's default) and up; heavy VCs vary
  a lot across seeds (for #6539, a median coefficient of variation of 0.18 among VCs over 1M, and
  0.68 at the 90th percentile), so a single seed shows brittleness, not cause. Boogie's seed
  renames and reorders the input as well as reseeding Z3, and Z3's seed alone leaves many VCs'
  costs unchanged, so sampling seeds means re-running Boogie. (`dafny measure-complexity
  --mutations` repeats in one process, but crashed on key-expression map comprehensions until the
  projection functions stopped being cached on the AST.) A logged query replays in Z3 to the same
  resource count (60 of 60 sampled), which makes one VC easy to study without Dafny.
- **Stability.** The report counts *flaky* VCs (some seeds pass at the job's limit, others do
  not) and each VC's cost spread per prelude, next to the A/A and placebo controls, so that a
  change that makes proofs brittle shows up even when their mean cost does not move.
- **Costs.** Resource counts from `--log-format csv`, under a 500M/300 s cap so that costs above
  the tests' own limits are measured; verdicts are read at each job's limit (50M lit/synth/external,
  5M standard library), or at a declaration's own (`{:resource_limit}`, `@ResourceLimit`, `{:rlimit}`,
  a time-limit multiplier; a limit of 0 is none). Dafny multiplies the cap by a declaration's `{:timeLimitMultiplier N}` into
  a 32-bit `{:rlimit}`, and aborts when that overflows, so such programs run under (2^31 - 1)/N.
  Durations are recorded but taken under load: identical SMT gave durations within about ±5%, and
  log RU tracked log time with a correlation of 0.96.
- **Corpus.** Lit tests are regression tests, mostly tiny; `synth.py`'s programs are written to
  stress the change and are reported apart. External programs make the result less about
  Dafny's own tests: `corpora/` lists Kondo's protocol proofs and DafnyBench's programs.

## Comparing solvers

Two solvers' resource counts do not convert into each other, and wall-clock time is only as good as
the machine is quiet, so solvers are compared per query, outside Dafny. CPU time moves with load as
well, not equally for two solvers, and includes a process's startup (`results/cvc5`), so compare their
work with `replay.py --perf` (user-space instructions), less a `--part startup` replay; verdicts within
the CPU limit do not depend on it.

```sh
# 1. Log every query each variant sends; the time limit only shortens the run (the logged text does not depend on it).
python3 run.py jobs.json work/log --variants variants.json --preludes z3,cvc5 --seeds 1 --resource-limit 0 \
  --time-limit 2 --solver-log-root /short/root
# 2. Replay each query in its own solver process, under a CPU-time limit; CPU time comes from wait4.
python3 replay.py /short/root work/replay --cpu 60 --logged work/log \
  --solver "z3=z3:/path/to/z3::z3" --solver "cvc5=cvc5:/path/to/cvc5::cvc5"
# 3. Compare: verdicts within the limit, CPU time on what both prove.
python3 solvers.py jobs.json work/replay z3 cvc5 work/report.md work/vcs.csv --cap 60
```

`variants.json` maps a variant to its Dafny build, solver and `--solver-option`s; cvc5 needs
`SOLVER=cvc5` and a per-query limit, `C:--tlimit-per=<ms>`, because Boogie sends cvc5 no limits. A
replay is the logged text up to the first `(check-sat)`: the VC's check, not the follow-up queries
that Boogie sends after a failure. Replayed in Z3, it gives the logging run's verdicts, and, for most
VCs, its exact resource counts.

## Results for #6539

`results/series/README.md` compares the author's six sibling PRs, #6540 to #6545, which are
reviewed in `results/pr65NN/REVIEW.md` and benchmarked as binaries as well as preludes.

`results/pr6539/REVIEW.md` is the review these results informed. `v2/` holds the current run:
reports, per-VC data, classifications and raw CSVs for Z3 4.16.0 (the version CI uses) and Z3
5.1.0. `report-z3-4.16.0.md` covers all 80 programs; the `-63-programs` report and the Z3 5.1.0
one cover the 63 measured under all six preludes. `v1/` is the first run, whose corpus was
selected by grepping and whose intervals resampled VCs; it is kept for its raw data.
