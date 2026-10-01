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

# 1. Screen: what does the change reach? One seed, every lit test and standard-library file.
python3 corpus.py work/screen.json litall stdall
python3 run.py work/screen.json work/screen --preludes master,pr --seeds 0
python3 screen.py work/screen.json work/screen

# 2. Classify the reached VCs: does their SMT contain the changed axiom, or is it only reordered?
python3 classify.py <reached-jobs.json> work/classes

# 3. Measure: several seeds, the controls, the alternatives.
python3 corpus.py work/jobs.json                       # lit, std, synth and unionfind jobs
python3 run.py work/jobs.json work/out --preludes master,master2,pr,pointwise,placebo,domguard --seeds 0,1,2,3,4,5,6,7
python3 report.py work/jobs.json work/out work/report.md work/vcs.csv --classes=work/classes/classes.csv
```

`run.py` resumes: it skips (job, prelude, seed) runs whose CSV exists, and kills a run after
`--run-timeout` seconds. `dafny.sh` runs `Binaries/Dafny.dll` (override with `DAFNY_DLL`) with core
dumps off; without `--solver` Dafny uses the `z3` next to it.

## What it measures, and what can go wrong

- **Controls.** `master2` is master again: its runs measure nondeterminism across processes (an
  A/A test). `placebo` flips the old axiom's equation: the same meaning in different text.
  `pointwise` is the PR's quantifier without its guard, keeping master's meaning, so master ->
  pointwise is what the PR's *shape* costs and pointwise -> pr what its *guard* costs.
- **Reach is not what the source mentions.** A prelude change reorders the SMT of VCs that do
  not use the changed axiom, which moves their cost like any perturbation, and some VCs differ
  between two runs of the same input. For #6539 the screen found cost changes in 72 lit and
  standard-library jobs, many without a map comprehension; `classify.py` (one solver log per
  procedure, `--solver-log <dir>/@PROC@.smt2`) showed that most of those VCs never contain the
  axiom. Select by screen and classification, not by grepping sources.
- **VCs are not independent.** One program can contribute most of the VCs (`UnionFind.dfy`: 69%
  of #6539's affected proofs). The report's intervals resample programs, and "per program"
  weighs each program once; a VC-level bootstrap is several times too confident.
- **Seeds.** Each run repeats for Boogie `/randomSeed` 0 (Dafny's default) and up; heavy VCs vary
  a lot across seeds (for #6539, a median coefficient of variation of 0.18 among VCs over 1M, and
  0.68 at the 90th percentile), so a single seed shows brittleness, not cause. (`dafny
  measure-complexity --mutations` repeats in one process, but crashed on key-expression map
  comprehensions until the projection functions stopped being cached on the AST.)
- **Costs.** Resource counts from `--log-format csv`, under a 500M/300 s cap so that costs above
  the tests' own limits are measured; verdicts are read at each job's limit (50M lit/synth/external,
  5M standard library). Durations are recorded but taken under load: identical SMT gave durations
  within about ±5%, and log RU tracked log time with a correlation of 0.96.
- **Corpus.** Lit tests are regression tests, mostly tiny; `synth.py`'s programs are written to
  stress the change and are reported apart. External programs make the result less about
  Dafny's own tests: `corpora/` lists Kondo's protocol proofs and DafnyBench's programs.

## Results for #6539

`results/pr6539/REVIEW.md` is the review these results informed. `v2/` holds the current run:
reports, per-VC data, classifications and raw CSVs for Z3 4.16.0 (the version CI uses), and the
first run's Z3 5.1.0 data re-reported with program-level intervals. `v1/` is the first run, whose
corpus was selected by grepping and whose intervals resampled VCs; it is kept for its raw data.
