# #6544 A/B benchmark (public corpora, seeds 1-4)

Seeds per (VC, prelude): 4 (1, 2, 3, 4; 0 is Dafny's default). VCs: 2030 in 1 jobs; **1156 affected** (master and PR counts differ), 874 unaffected (identical counts under master and PR for every seed).
Unaffected VCs whose counts differ under the placebo: 0.

## Proof cost over affected VCs that pass everywhere

Totals are sums of per-VC means over seeds. "Per program" averages each program's own VC geomean, so a
program with hundreds of VCs weighs no more than one with two. Brackets are 95% bootstrap intervals that
resample programs, not VCs.

| group | programs | VCs | largest program | total PR/master | geomean over VCs | per program | placebo per program |
|---|---:|---:|---|---|---|---|---|
| all but synth | 1 | 1148 | std/Actions/Producers.dfy (100% of VCs) | -0.4% [-0.4%, -0.4%] | -0.1% [-0.1%, -0.1%] | -0.1% [-0.1%, -0.1%] | +0.0% [+0.0%, +0.0%] |
| std | 1 | 1148 | std/Actions/Producers.dfy (100% of VCs) | -0.4% [-0.4%, -0.4%] | -0.1% [-0.1%, -0.1%] | -0.1% [-0.1%, -0.1%] | +0.0% [+0.0%, +0.0%] |

8 affected VCs fail (a verification error) in some run; their cost is the solver's search for a counterexample, reported separately:

| job | VC | master mean (min..max) | PR mean (min..max) | placebo mean |
|---|---|---|---|---|
| std/Actions/Producers.dfy | Std.Producers.ConcatenatedProducer.Invoke (correctness) (assertion batch 277) | 81.19M (24.21..100.19) | 68.76M (36.86..100.19) | 49.93M |
| std/Actions/Producers.dfy | Std.Producers.ConcatenatedProducer.Invoke (correctness) (assertion batch 275) | 59.28M (4.62..100.19) | 26.52M (5.77..66.90) | 56.15M |
| std/Actions/Producers.dfy | Std.Producers.FlattenedProducer.Invoke (correctness) | 36.31M (21.40..64.47) | 35.55M (23.31..52.25) | 24.56M |
| std/Actions/Producers.dfy | Std.Producers.ConcatenatedProducer.Invoke (correctness) (assertion batch 273) | 31.73M (1.54..100.19) | 3.46M (1.47..6.22) | 26.70M |
| std/Actions/Producers.dfy | Std.Producers.ConcatenatedProducer.Invoke (correctness) (assertion batch 283) | 30.22M (6.80..66.34) | 36.93M (9.04..71.51) | 34.69M |
| std/Actions/Producers.dfy | Std.Producers.MappedProducer.Invoke (correctness) | 9.05M (8.38..10.22) | 8.06M (7.16..10.22) | 8.60M |
| std/Actions/Producers.dfy | Std.Producers.LimitedProducer.Invoke (correctness) | 3.59M (2.56..5.97) | 3.22M (2.82..3.70) | 6.85M |
| std/Actions/Producers.dfy | Std.Producers.ProducerState.ValidChangeTransitive (correctness) (assertion batch 90) | 1.26M (0.22..4.13) | 1.28M (0.22..4.21) | 1.26M |

## Total proof RU per seed (affected VCs that pass everywhere)

| prelude | seed 1 | seed 2 | seed 3 | seed 4 | mean | sd |
|---|---:|---:|---:|---:|---:|---:|
| master | 353.6M | 341.4M | 360.9M | 347.3M | 350.8M | 7.3M |
| pr | 348.3M | 341.8M | 357.7M | 349.5M | 349.3M | 5.7M |
| placebo | 352.1M | 340.0M | 366.0M | 358.9M | 354.3M | 9.6M |

## Solver time over those proofs (sum of per-VC means, seconds)

| group | master | PR | placebo |
|---|---:|---:|---:|
| all | 222.3 | 220.4 | 214.4 |
| std | 222.3 | 220.4 | 214.4 |

## Distribution of per-VC cost ratios over those proofs (mean over seeds)

| ratio bucket | PR/master | placebo/master |
|---|---:|---:|
| < 0.5x | 0 | 0 |
| 0.5-0.8x | 2 | 1 |
| 0.8-0.95x | 10 | 1 |
| 0.95-1.05x | 1131 | 1141 |
| 1.05-1.25x | 4 | 4 |
| 1.25-2x | 1 | 1 |
| 2-4x | 0 | 0 |
| >= 4x | 0 | 0 |

## Verdict changes at each job's limit (seeds passing out of 4)

| job | VC | limit | master ok | PR ok | placebo ok | master RU | PR RU |
|---|---|---:|---:|---:|---:|---:|---:|
| std/Actions/Producers.dfy | Std.Producers.ConcatenatedProducer.Invoke (correctness) (assertion batch 273) | 100M | 3 | 4 | 3 | 31.73M | 3.46M |
| std/Actions/Producers.dfy | Std.Producers.ConcatenatedProducer.Invoke (correctness) (assertion batch 275) | 100M | 2 | 4 | 2 | 59.28M | 26.52M |
| std/Actions/Producers.dfy | Std.Producers.ConcatenatedProducer.Invoke (correctness) (assertion batch 277) | 100M | 1 | 2 | 3 | 81.19M | 68.76M |
| std/Actions/Producers.dfy | Std.Producers.ConcatenatedProducer.Invoke (correctness) (assertion batch 283) | 100M | 4 | 4 | 3 | 30.22M | 36.93M |
| std/Actions/Producers.dfy | Std.Producers.FlattenedProducer.Invoke (correctness) | 100M | 4 | 4 | 3 | 36.31M | 35.55M |
| std/Actions/Producers.dfy | Std.Producers.LimitedProducer.Invoke (correctness) | 10M | 4 | 4 | 3 | 3.59M | 3.22M |

## Largest changes among those proofs (by |PR - master| mean RU)

| job | VC | master | PR | PR/master | placebo | min..max master | min..max PR |
|---|---|---:|---:|---:|---:|---|---|
| std/Actions/Producers.dfy | Std.Producers.ConcatenatedProducer.Invoke (correctness) (assertion batch 276) | 6.02M | 7.71M | 1.28 | 8.10M | 4.61..10.20M | 3.98..14.48M |
| std/Actions/Producers.dfy | Std.Producers.ConcatenatedProducer.Invoke (correctness) (assertion batch 214) | 5.18M | 3.90M | 0.75 | 5.26M | 4.36..6.00M | 2.55..5.71M |
| std/Actions/Producers.dfy | Std.Producers.FilteredProducer.Invoke (correctness) | 10.84M | 10.15M | 0.94 | 11.71M | 7.63..15.94M | 8.25..13.27M |
| std/Actions/Producers.dfy | Std.Producers.ConcatenatedProducer.Invoke (correctness) (assertion batch 262) | 2.15M | 1.54M | 0.72 | 1.29M | 1.26..3.43M | 1.24..2.41M |
| std/Actions/Producers.dfy | Std.Producers.MappedProducerOfNewProducers.Invoke (correctness) | 10.05M | 9.56M | 0.95 | 10.21M | 8.71..11.11M | 8.02..10.49M |
| std/Actions/Producers.dfy | Std.Producers.ConcatenatedProducer.Invoke (correctness) (assertion batch 360) | 2.60M | 2.39M | 0.92 | 2.42M | 2.40..2.82M | 2.18..2.56M |
| std/Actions/Producers.dfy | Std.Producers.ConcatenatedProducer.Invoke (correctness) (assertion batch 200) | 1.19M | 0.99M | 0.83 | 1.19M | 0.71..1.89M | 0.72..1.17M |
| std/Actions/Producers.dfy | Std.Producers.ConcatenatedProducer.Invoke (correctness) (assertion batch 213) | 4.91M | 5.11M | 1.04 | 4.92M | 3.80..6.24M | 3.61..6.66M |
| std/Actions/Producers.dfy | Std.Producers.ConcatenatedProducer.Invoke (correctness) (assertion batch 270) | 1.56M | 1.74M | 1.11 | 1.58M | 1.51..1.64M | 1.62..2.03M |
| std/Actions/Producers.dfy | Std.Producers.ConcatenatedProducer.Invoke (correctness) (assertion batch 263) | 2.10M | 1.94M | 0.93 | 2.09M | 1.86..2.48M | 1.24..3.22M |
| std/Actions/Producers.dfy | Std.Producers.DefaultForEach (correctness) (assertion batch 132) | 2.77M | 2.90M | 1.04 | 2.71M | 2.52..3.32M | 2.53..3.92M |
| std/Actions/Producers.dfy | Std.Producers.ConcatenatedProducer.Invoke (correctness) (assertion batch 352) | 7.09M | 6.98M | 0.99 | 7.36M | 5.14..8.74M | 4.91..8.55M |
| std/Actions/Producers.dfy | Std.Producers.ConcatenatedProducer.Invoke (correctness) (assertion batch 353) | 6.80M | 6.70M | 0.99 | 6.76M | 5.43..8.36M | 5.16..8.03M |
| std/Actions/Producers.dfy | Std.Producers.DefaultFill (correctness) (assertion batch 60) | 0.36M | 0.43M | 1.17 | 0.36M | 0.32..0.42M | 0.34..0.57M |
| std/Actions/Producers.dfy | Std.Producers.ConcatenatedProducer.Invoke (correctness) (assertion batch 354) | 6.58M | 6.64M | 1.01 | 6.56M | 5.23..7.85M | 5.33..7.61M |
| std/Actions/Producers.dfy | Std.Producers.ConcatenatedProducer.Invoke (correctness) (assertion batch 345) | 1.20M | 1.26M | 1.05 | 1.21M | 1.10..1.34M | 1.15..1.46M |
| std/Actions/Producers.dfy | Std.Producers.ConcatenatedProducer.Invoke (correctness) (assertion batch 350) | 1.97M | 2.02M | 1.03 | 2.02M | 1.90..2.08M | 1.78..2.31M |
| std/Actions/Producers.dfy | Std.Producers.DefaultFill (correctness) (assertion batch 273) | 1.15M | 1.10M | 0.96 | 1.16M | 1.05..1.24M | 0.99..1.25M |
| std/Actions/Producers.dfy | Std.Producers.ConcatenatedProducer.Invoke (correctness) (assertion batch 185) | 0.31M | 0.35M | 1.13 | 0.31M | 0.28..0.38M | 0.28..0.38M |
| std/Actions/Producers.dfy | Std.Producers.ConcatenatedProducer.Invoke (correctness) (assertion batch 77) | 0.26M | 0.29M | 1.14 | 0.26M | 0.25..0.26M | 0.25..0.39M |
| std/Actions/Producers.dfy | Std.Producers.ConcatenatedProducer.Invoke (correctness) (assertion batch 304) | 0.35M | 0.32M | 0.90 | 0.35M | 0.28..0.43M | 0.28..0.42M |
| std/Actions/Producers.dfy | Std.Producers.ConcatenatedProducer.Invoke (correctness) (assertion batch 339) | 1.16M | 1.13M | 0.97 | 1.15M | 0.77..1.43M | 0.77..1.34M |
| std/Actions/Producers.dfy | Std.Producers.ConcatenatedProducer.Invoke (correctness) (assertion batch 269) | 0.35M | 0.32M | 0.91 | 0.35M | 0.35..0.35M | 0.28..0.35M |
| std/Actions/Producers.dfy | Std.Producers.DefaultForEach (correctness) (assertion batch 109) | 0.47M | 0.44M | 0.94 | 0.47M | 0.44..0.50M | 0.44..0.44M |
| std/Actions/Producers.dfy | Std.Producers.ConcatenatedProducer.Invoke (correctness) (assertion batch 211) | 1.38M | 1.40M | 1.02 | 1.43M | 1.28..1.50M | 1.27..1.52M |

## Per job (proofs among the affected VCs)

| job | VCs | master | PR | PR vs master | placebo vs master |
|---|---:|---:|---:|---:|---:|
| std/Actions/Producers.dfy | 1148 | 350.81M | 349.32M | -0.4% | +1.0% |

## Stability over the affected VCs (all but synth)

Flaky: some seeds pass at the job's limit and others do not. Spread: the coefficient of variation of a VC's cost across seeds, for VCs above 1M RU under master.

| prelude | flaky VCs | flaky, not under master | no longer flaky | median spread | 90th-percentile spread |
|---|---:|---:|---:|---:|---:|
| master | 5 | 0 | 0 | 0.15 | 0.71 |
| master2 | 5 | 0 | 0 | 0.15 | 0.71 |
| placebo | 8 | 3 | 0 | 0.13 | 0.79 |
| pr | 3 | 0 | 2 | 0.19 | 0.53 |

## Comparisons over the affected proofs (all but synth)

| comparison | programs | VCs | total | geomean over VCs | per program | verdict flips at limit |
|---|---:|---:|---|---|---|---:|
| A/A: master2 vs master (same input, another process) | 1 | 1148 | +0.0% [+0.0%, +0.0%] | +0.0% [+0.0%, +0.0%] | +0.0% [+0.0%, +0.0%] | 0 |
| placebo vs master (the old axiom, rewritten) | 1 | 1148 | +1.0% [+1.0%, +1.0%] | +0.0% [+0.0%, +0.0%] | +0.0% [+0.0%, +0.0%] | 0 |
| pr vs master | 1 | 1148 | -0.4% [-0.4%, -0.4%] | -0.1% [-0.1%, -0.1%] | -0.1% [-0.1%, -0.1%] | 0 |

## Alternative sound encodings, over the same proofs

restrict: elements defined everywhere, `$ArbitraryBoxValue` outside the domain. domguard: the PR's axiom guarded by `Map#Domain(Map#Glue(a, b, t))`. eager: the PR's axiom plus the trigger `{ Map#Glue(a, b, t), Set#IsMember(a, bx) }`.

| encoding | programs | VCs | total vs master | geomean over VCs vs master | per program vs master | per program vs PR | verdict flips vs master at limit |
|---|---:|---:|---|---|---|---|---:|
| pr | 1 | 1148 | -0.4% [-0.4%, -0.4%] | -0.1% [-0.1%, -0.1%] | -0.1% [-0.1%, -0.1%] |  | 3 |
| master2 | 1 | 1148 | +0.0% [+0.0%, +0.0%] | +0.0% [+0.0%, +0.0%] | +0.0% [+0.0%, +0.0%] | +0.1% [+0.1%, +0.1%] | 0 |

master2: largest differences from the PR

| job | VC | master | PR | master2 |
|---|---|---:|---:|---:|
| std/Actions/Producers.dfy | Std.Producers.ConcatenatedProducer.Invoke (correctness) (assertion batch 276) | 6.02M | 7.71M | 6.02M |
| std/Actions/Producers.dfy | Std.Producers.ConcatenatedProducer.Invoke (correctness) (assertion batch 214) | 5.18M | 3.90M | 5.18M |
| std/Actions/Producers.dfy | Std.Producers.FilteredProducer.Invoke (correctness) | 10.84M | 10.15M | 10.84M |
| std/Actions/Producers.dfy | Std.Producers.ConcatenatedProducer.Invoke (correctness) (assertion batch 262) | 2.15M | 1.54M | 2.15M |
| std/Actions/Producers.dfy | Std.Producers.MappedProducerOfNewProducers.Invoke (correctness) | 10.05M | 9.56M | 10.05M |
| std/Actions/Producers.dfy | Std.Producers.ConcatenatedProducer.Invoke (correctness) (assertion batch 360) | 2.60M | 2.39M | 2.60M |
