# Prelude A/B benchmark

Measures how a change to `DafnyPrelude.bpl` affects verification cost, by verifying the same
programs with one Dafny binary and swapping only the prelude (`--prelude`). Written to evaluate
dafny-lang/dafny#6539, which weakens the `Map#Glue`/`IMap#Glue` element axioms; the corpus and
the prelude variants are specific to that change, the runner and the report are not.

## Running it

```sh
dotnet build Source/Dafny/Dafny.csproj                 # the binary under test: Binaries/Dafny.dll
cd Scripts/prelude-ab-bench
python3 preludes.py --master origin/master --pr 074e49a64   # writes preludes/*.bpl
python3 synth.py                                       # writes synth/*.dfy
python3 corpus.py work/jobs.json                       # lit, std, synth and unionfind jobs
python3 run.py work/jobs.json work/out --preludes master,pr,placebo   # --solver <z3>, --seeds, --workers
python3 report.py work/jobs.json work/out work/report.md work/vcs.csv
```

`run.py` resumes: it skips (job, prelude, seed) runs whose CSV exists. Add
`restrict,domguard,eager` to `--preludes` to also measure the alternative encodings.
`dafny.sh` runs `Binaries/Dafny.dll` (override with `DAFNY_DLL`); without `--solver` Dafny uses
the `z3` next to it.

## What it measures

- **Preludes.** `master` and `pr`; `placebo`, which is master with the old axiom's equation
  flipped (`b == Map#Elements(...)`): the same meaning in different SMT text, so its spread is
  what a mere rewrite of this axiom costs; and three alternative sound encodings (see
  `preludes.py`).
- **Corpus.** Every lit test containing a `map`/`imap` comprehension (the only construct encoded
  with `Map#Glue`), with its first RUN line's flags, under the refreshed and the legacy resolver;
  the standard-library files with comprehensions (project mode, 5M per-VC limit); 40 synthetic
  programs scaling one use of a comprehension each (`synth.py`); and `dafny4/UnionFind.dfy` as on
  master, whose `Main` #6539 isolates.
- **Seeds.** Each run repeats for Boogie `/randomSeed` 0 (Dafny's default) to 4, which renames,
  reorders and reseeds the solver. (`dafny measure-complexity --mutations` would do this in one
  process, but crashes with Boogie type errors on a key-expression map comprehension whose key
  is a sequence.)
- **Costs.** Resource counts from `--log-format csv`, under a 500M/300 s cap so that costs above
  the tests' own limits are measured; verdicts are read at each job's limit (50M lit/synth, 5M
  standard library). A VC is *affected* when its counts under master and PR differ for some seed;
  unaffected VCs got identical SMT, so their identical counts double as a determinism check.
  Cost aggregates use the affected VCs that pass everywhere (proofs); geometric means of per-VC
  ratios describe the typical VC, totals the heavy ones; brackets are 95% bootstrap intervals
  over VCs.

## Results for #6539

`results/pr6539/`: reports and per-VC data for Z3 4.16.0 (the version CI uses) and Z3 5.1.0,
and `REVIEW.md`, the review they informed.
