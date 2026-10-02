# #6542 A/B benchmark (public corpora, seeds 1-4)

Seeds per (VC, prelude): 4 (1, 2, 3, 4; 0 is Dafny's default). VCs: 386 in 1 jobs; **1 affected** (master and PR counts differ), 385 unaffected (identical counts under master and PR for every seed).

## Proof cost over affected VCs that pass everywhere

Totals are sums of per-VC means over seeds. "Per program" averages each program's own VC geomean, so a
program with hundreds of VCs weighs no more than one with two. Brackets are 95% bootstrap intervals that
resample programs, not VCs.

| group | programs | VCs | largest program | total PR/master | geomean over VCs | per program |
|---|---:|---:|---|---|---|---|
| all but synth | 1 | 1 | lit/concurrency/12-MutexLifetime-short.dfy (100% of VCs) | +22.4% [+22.4%, +22.4%] | +22.4% [+22.4%, +22.4%] | +22.4% [+22.4%, +22.4%] |
| lit | 1 | 1 | lit/concurrency/12-MutexLifetime-short.dfy (100% of VCs) | +22.4% [+22.4%, +22.4%] | +22.4% [+22.4%, +22.4%] | +22.4% [+22.4%, +22.4%] |

0 affected VCs fail (a verification error) in some run; their cost is the solver's search for a counterexample, reported separately:

| job | VC | master mean (min..max) | PR mean (min..max) |
|---|---|---|---|

## Total proof RU per seed (affected VCs that pass everywhere)

| prelude | seed 1 | seed 2 | seed 3 | seed 4 | mean | sd |
|---|---:|---:|---:|---:|---:|---:|
| master | 41.5M | 22.6M | 18.1M | 46.1M | 32.1M | 11.9M |
| pr | 65.9M | 26.3M | 18.8M | 46.1M | 39.3M | 18.3M |

## Solver time over those proofs (sum of per-VC means, seconds)

| group | master | PR |
|---|---:|---:|
| all | 22.3 | 32.8 |
| lit | 22.3 | 32.8 |

## Distribution of per-VC cost ratios over those proofs (mean over seeds)

| ratio bucket | PR/master |
|---|---:|
| < 0.5x | 0 |
| 0.5-0.8x | 0 |
| 0.8-0.95x | 0 |
| 0.95-1.05x | 0 |
| 1.05-1.25x | 1 |
| 1.25-2x | 0 |
| 2-4x | 0 |
| >= 4x | 0 |

## Verdict changes at each job's limit (seeds passing out of 4)

| job | VC | limit | master ok | PR ok | master RU | PR RU |
|---|---|---:|---:|---:|---:|---:|
| lit/concurrency/12-MutexLifetime-short.dfy:refresh | Lifetime._ctor (correctness) | 50M | 4 | 3 | 32.07M | 39.25M |

## Largest changes among those proofs (by |PR - master| mean RU)

| job | VC | master | PR | PR/master | min..max master | min..max PR |
|---|---|---:|---:|---:|---|---|
| lit/concurrency/12-MutexLifetime-short.dfy:refresh | Lifetime._ctor (correctness) | 32.07M | 39.25M | 1.22 | 18.13..46.08M | 18.76..65.91M |

## Per job (proofs among the affected VCs)

| job | VCs | master | PR | PR vs master |
|---|---:|---:|---:|---:|
| lit/concurrency/12-MutexLifetime-short.dfy:refresh | 1 | 32.07M | 39.25M | +22.4% |

## Stability over the affected VCs (all but synth)

Flaky: some seeds pass at the job's limit and others do not. Spread: the coefficient of variation of a VC's cost across seeds, for VCs above 1M RU under master.

| prelude | flaky VCs | flaky, not under master | no longer flaky | median spread | 90th-percentile spread |
|---|---:|---:|---:|---:|---:|
| master | 0 | 0 | 0 | 0.37 | 0.37 |
| master2 | 0 | 0 | 0 | 0.37 | 0.37 |
| pr | 1 | 1 | 0 | 0.47 | 0.47 |

Flaky under the PR but not under master (seeds passing out of the run):

| job | VC | master | PR | PR mean RU |
|---|---|---:|---:|---:|
| lit/concurrency/12-MutexLifetime-short.dfy:refresh | Lifetime._ctor (correctness) | 4 | 3 | 39.25M |

## Comparisons over the affected proofs (all but synth)

| comparison | programs | VCs | total | geomean over VCs | per program | verdict flips at limit |
|---|---:|---:|---|---|---|---:|
| A/A: master2 vs master (same input, another process) | 1 | 1 | +0.0% [+0.0%, +0.0%] | +0.0% [+0.0%, +0.0%] | +0.0% [+0.0%, +0.0%] | 0 |
| pr vs master | 1 | 1 | +22.4% [+22.4%, +22.4%] | +22.4% [+22.4%, +22.4%] | +22.4% [+22.4%, +22.4%] | 1 |

## Alternative sound encodings, over the same proofs

restrict: elements defined everywhere, `$ArbitraryBoxValue` outside the domain. domguard: the PR's axiom guarded by `Map#Domain(Map#Glue(a, b, t))`. eager: the PR's axiom plus the trigger `{ Map#Glue(a, b, t), Set#IsMember(a, bx) }`.

| encoding | programs | VCs | total vs master | geomean over VCs vs master | per program vs master | per program vs PR | verdict flips vs master at limit |
|---|---:|---:|---|---|---|---|---:|
| pr | 1 | 1 | +22.4% [+22.4%, +22.4%] | +22.4% [+22.4%, +22.4%] | +22.4% [+22.4%, +22.4%] |  | 1 |
| master2 | 1 | 1 | +0.0% [+0.0%, +0.0%] | +0.0% [+0.0%, +0.0%] | +0.0% [+0.0%, +0.0%] | -18.3% [-18.3%, -18.3%] | 0 |

master2: largest differences from the PR

| job | VC | master | PR | master2 |
|---|---|---:|---:|---:|
| lit/concurrency/12-MutexLifetime-short.dfy:refresh | Lifetime._ctor (correctness) | 32.07M | 39.25M | 32.07M |
