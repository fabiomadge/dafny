# #6544 A/B benchmark (public corpora, seed 1)

Seeds per (VC, prelude): 1 (1; 0 is Dafny's default). VCs: 27063 in 2077 jobs; **1213 affected** (master and PR counts differ), 25850 unaffected (identical counts under master and PR for every seed).

## Proof cost over affected VCs that pass everywhere

Totals are sums of per-VC means over seeds. "Per program" averages each program's own VC geomean, so a
program with hundreds of VCs weighs no more than one with two. Brackets are 95% bootstrap intervals that
resample programs, not VCs.

| group | programs | VCs | largest program | total PR/master | geomean over VCs | per program |
|---|---:|---:|---|---|---|---|
| all but synth | 7 | 1196 | std/Actions/Producers.dfy (93% of VCs) | -12.6% [-12.9%, +0.3%] | -0.1% [-0.2%, +0.1%] | -0.0% [-0.1%, +0.1%] |
| lit | 1 | 1 | lit/dafny0/CoinductiveProofs.dfy (100% of VCs) | +0.0% [+0.0%, +0.0%] | +0.0% [+0.0%, +0.0%] | +0.0% [+0.0%, +0.0%] |
| std | 6 | 1195 | std/Actions/Producers.dfy (93% of VCs) | -12.6% [-12.9%, +0.3%] | -0.1% [-0.2%, +0.1%] | -0.0% [-0.1%, +0.1%] |

17 affected VCs fail (a verification error) in some run; their cost is the solver's search for a counterexample, reported separately:

| job | VC | master mean (min..max) | PR mean (min..max) |
|---|---|---|---|
| lit/comp/TypeParams.dfy:refresh | Standard (correctness) | 832.98M (832.98..832.98) | 804.22M (804.22..804.22) |
| lit/dafny0/FunctionSpecifications.dfy:refresh | GoodPost (well-formedness) | 311.14M (311.14..311.14) | 311.03M (311.03..311.03) |
| lit/cli/defaultTimeLimit.dfy:refresh | Foo (correctness) | 298.84M (298.84..298.84) | 270.28M (270.28..270.28) |
| kondo/paxos/sync | PaxosProof.InvNextLearnerReceivedAcceptImpliesAccepted (correctness) | 293.81M (293.81..293.81) | 304.73M (304.73..304.73) |
| libraries/dafny/Collections/Seqs.dfy | Dafny.Collections.Seq.LemmaMapDistributesOverConcat (correctness) | 243.34M (243.34..243.34) | 294.97M (294.97..294.97) |
| dafnybench/dafny_experiments_tmp_tmpz29_3_3i_circuit.dfy | CombineCircuits.CombineCircuitsCorrect (correctness) | 214.71M (214.71..214.71) | 219.08M (219.08..219.08) |
| libraries/dafny/Collections/Seqs.dfy | Dafny.Collections.Seq.LemmaFilterDistributesOverConcat (correctness) (assertion batch 2) | 171.40M (171.40..171.40) | 180.46M (180.46..180.46) |
| std/Actions/Producers.dfy | Std.Producers.ConcatenatedProducer.Invoke (correctness) (assertion batch 277) | 100.19M (100.19..100.19) | 37.82M (37.82..37.82) |
| lit/dafny1/Rippling.legacy.dfy:refresh | P2 (correctness) | 22.88M (22.88..22.88) | 20.00M (20.00..20.00) |
| lit/hofs/Folding.legacy.dfy:refresh | FoldL_Use_Direct (correctness) | 21.23M (21.23..21.23) | 21.23M (21.23..21.23) |

## Total proof RU per seed (affected VCs that pass everywhere)

| prelude | seed 1 | mean | sd |
|---|---:|---:|---:|
| master | 473.1M | 473.1M | 0.0M |
| pr | 413.4M | 413.4M | 0.0M |

## Solver time over those proofs (sum of per-VC means, seconds)

| group | master | PR |
|---|---:|---:|
| all | 353.9 | 320.4 |
| lit | 0.0 | 0.0 |
| std | 353.9 | 320.4 |

## Distribution of per-VC cost ratios over those proofs (mean over seeds)

| ratio bucket | PR/master |
|---|---:|
| < 0.5x | 3 |
| 0.5-0.8x | 2 |
| 0.8-0.95x | 12 |
| 0.95-1.05x | 1165 |
| 1.05-1.25x | 9 |
| 1.25-2x | 3 |
| 2-4x | 1 |
| >= 4x | 1 |

## Verdict changes at each job's limit (seeds passing out of 1)

| job | VC | limit | master ok | PR ok | master RU | PR RU |
|---|---|---:|---:|---:|---:|---:|
| std/Actions/Producers.dfy | Std.Producers.ConcatenatedProducer.Invoke (correctness) (assertion batch 277) | 100M | 0 | 1 | 100.19M | 37.82M |

## Largest changes among those proofs (by |PR - master| mean RU)

| job | VC | master | PR | PR/master | min..max master | min..max PR |
|---|---|---:|---:|---:|---|---|
| std/Actions/Producers.dfy | Std.Producers.FlattenedProducer.Invoke (correctness) | 64.47M | 23.31M | 0.36 | 64.47..64.47M | 23.31..23.31M |
| std/Actions/Producers.dfy | Std.Producers.ConcatenatedProducer.Invoke (correctness) (assertion batch 275) | 32.13M | 5.77M | 0.18 | 32.13..32.13M | 5.77..5.77M |
| std/Actions/Producers.dfy | Std.Producers.ConcatenatedProducer.Invoke (correctness) (assertion batch 283) | 6.80M | 15.82M | 2.33 | 6.80..6.80M | 15.82..15.82M |
| std/Actions/Producers.dfy | Std.Producers.ConcatenatedProducer.Invoke (correctness) (assertion batch 273) | 1.54M | 6.22M | 4.04 | 1.54..1.54M | 6.22..6.22M |
| std/Actions/Producers.dfy | Std.Producers.ConcatenatedProducer.Invoke (correctness) (assertion batch 214) | 6.00M | 2.75M | 0.46 | 6.00..6.00M | 2.75..2.75M |
| std/Actions/Producers.dfy | Std.Producers.ConcatenatedProducer.Invoke (correctness) (assertion batch 276) | 4.64M | 6.42M | 1.38 | 4.64..4.64M | 6.42..6.42M |
| std/Actions/Producers.dfy | Std.Producers.FilteredProducer.Invoke (correctness) | 9.79M | 8.25M | 0.84 | 9.79..9.79M | 8.25..8.25M |
| std/Actions/Producers.dfy | Std.Producers.MappedProducerOfNewProducers.Invoke (correctness) | 11.11M | 9.68M | 0.87 | 11.11..11.11M | 9.68..9.68M |
| std/Actions/Producers.dfy | Std.Producers.ConcatenatedProducer.Invoke (correctness) (assertion batch 262) | 3.43M | 2.41M | 0.70 | 3.43..3.43M | 2.41..2.41M |
| std/Actions/Producers.dfy | Std.Producers.ConcatenatedProducer.Invoke (correctness) (assertion batch 351) | 7.59M | 6.60M | 0.87 | 7.59..7.59M | 6.60..6.60M |
| std/Actions/Producers.dfy | Std.Producers.MappedProducer.Invoke (correctness) | 8.38M | 7.48M | 0.89 | 8.38..8.38M | 7.48..7.48M |
| std/Actions/Producers.dfy | Std.Producers.ConcatenatedProducer.Invoke (correctness) (assertion batch 200) | 1.89M | 1.03M | 0.54 | 1.89..1.89M | 1.03..1.03M |
| std/Actions/Producers.dfy | Std.Producers.ConcatenatedProducer.Invoke (correctness) (assertion batch 212) | 5.20M | 5.98M | 1.15 | 5.20..5.20M | 5.98..5.98M |
| std/Actions/Producers.dfy | Std.Producers.ConcatenatedProducer.Invoke (correctness) (assertion batch 263) | 2.48M | 3.22M | 1.30 | 2.48..2.48M | 3.22..3.22M |
| std/Actions/Producers.dfy | Std.Producers.ConcatenatedProducer.Invoke (correctness) (assertion batch 360) | 2.63M | 2.18M | 0.83 | 2.63..2.63M | 2.18..2.18M |
| std/Actions/Producers.dfy | Std.Producers.ConcatenatedProducer.Invoke (correctness) (assertion batch 213) | 6.24M | 6.66M | 1.07 | 6.24..6.24M | 6.66..6.66M |
| std/Actions/Producers.dfy | Std.Producers.ConcatenatedProducer.Invoke (correctness) (assertion batch 352) | 8.14M | 7.77M | 0.95 | 8.14..8.14M | 7.77..7.77M |
| std/Actions/Producers.dfy | Std.Producers.LimitedProducer.Invoke (correctness) | 3.26M | 3.55M | 1.09 | 3.26..3.26M | 3.55..3.55M |
| std/Actions/Producers.dfy | Std.Producers.ConcatenatedProducer.Invoke (correctness) (assertion batch 353) | 6.79M | 7.05M | 1.04 | 6.79..6.79M | 7.05..7.05M |
| std/Actions/Producers.dfy | Std.Producers.ConcatenatedProducer.Invoke (correctness) (assertion batch 354) | 6.96M | 7.17M | 1.03 | 6.96..6.96M | 7.17..7.17M |
| std/Actions/Producers.dfy | Std.Producers.ConcatenatedProducer.Invoke (correctness) (assertion batch 304) | 0.28M | 0.42M | 1.49 | 0.28..0.28M | 0.42..0.42M |
| std/Actions/Producers.dfy | Std.Producers.ConcatenatedProducer.Invoke (correctness) (assertion batch 313) | 1.71M | 1.84M | 1.08 | 1.71..1.71M | 1.84..1.84M |
| std/Actions/Producers.dfy | Std.Producers.ConcatenatedProducer.Invoke (correctness) (assertion batch 272) | 1.76M | 1.87M | 1.06 | 1.76..1.76M | 1.87..1.87M |
| std/Actions/Producers.dfy | Std.Producers.ConcatenatedProducer.Invoke (correctness) (assertion batch 194) | 1.17M | 1.28M | 1.09 | 1.17..1.17M | 1.28..1.28M |
| std/Actions/Producers.dfy | Std.Producers.ConcatenatedProducer.Invoke (correctness) (assertion batch 345) | 1.19M | 1.26M | 1.06 | 1.19..1.19M | 1.26..1.26M |

## Per job (proofs among the affected VCs)

| job | VCs | master | PR | PR vs master |
|---|---:|---:|---:|---:|
| std/Actions/Producers.dfy | 1109 | 460.71M | 400.96M | -13.0% |
| std/Termination.dfy | 32 | 4.74M | 4.74M | -0.0% |
| std/Actions/BulkActions.dfy | 19 | 3.91M | 3.93M | +0.5% |
| std/Actions/Consumers.dfy | 21 | 3.00M | 2.99M | -0.3% |
| std/Actions/Actions.dfy | 5 | 0.50M | 0.50M | -0.0% |
| std/Ordinal.dfy | 9 | 0.22M | 0.22M | +0.1% |
| lit/dafny0/CoinductiveProofs.dfy:refresh | 1 | 0.03M | 0.03M | +0.0% |

## Stability over the affected VCs (all but synth)

Flaky: some seeds pass at the job's limit and others do not. Spread: the coefficient of variation of a VC's cost across seeds, for VCs above 1M RU under master.

| prelude | flaky VCs | flaky, not under master | no longer flaky | median spread | 90th-percentile spread |
|---|---:|---:|---:|---:|---:|
| master | 0 | 0 | 0 | 0.00 | 0.00 |
| master2 | 0 | 0 | 0 | 0.00 | 0.00 |
| pr | 0 | 0 | 0 | 0.00 | 0.00 |

## Comparisons over the affected proofs (all but synth)

| comparison | programs | VCs | total | geomean over VCs | per program | verdict flips at limit |
|---|---:|---:|---|---|---|---:|
| A/A: master2 vs master (same input, another process) | 7 | 1196 | -0.0% [-0.0%, +0.0%] | -0.0% [-0.0%, +0.0%] | -0.0% [-0.0%, +0.0%] | 0 |
| pr vs master | 7 | 1196 | -12.6% [-12.9%, +0.3%] | -0.1% [-0.2%, +0.1%] | -0.0% [-0.1%, +0.1%] | 0 |

## Alternative sound encodings, over the same proofs

restrict: elements defined everywhere, `$ArbitraryBoxValue` outside the domain. domguard: the PR's axiom guarded by `Map#Domain(Map#Glue(a, b, t))`. eager: the PR's axiom plus the trigger `{ Map#Glue(a, b, t), Set#IsMember(a, bx) }`.

| encoding | programs | VCs | total vs master | geomean over VCs vs master | per program vs master | per program vs PR | verdict flips vs master at limit |
|---|---:|---:|---|---|---|---|---:|
| pr | 7 | 1196 | -12.6% [-12.9%, +0.3%] | -0.1% [-0.2%, +0.1%] | -0.0% [-0.1%, +0.1%] |  | 1 |
| master2 | 7 | 1196 | -0.0% [-0.0%, +0.0%] | -0.0% [-0.0%, +0.0%] | -0.0% [-0.0%, +0.0%] | +0.0% [-0.1%, +0.1%] | 0 |

master2: largest differences from the PR

| job | VC | master | PR | master2 |
|---|---|---:|---:|---:|
| std/Actions/Producers.dfy | Std.Producers.FlattenedProducer.Invoke (correctness) | 64.47M | 23.31M | 64.47M |
| std/Actions/Producers.dfy | Std.Producers.ConcatenatedProducer.Invoke (correctness) (assertion batch 275) | 32.13M | 5.77M | 32.13M |
| std/Actions/Producers.dfy | Std.Producers.ConcatenatedProducer.Invoke (correctness) (assertion batch 283) | 6.80M | 15.82M | 6.80M |
| std/Actions/Producers.dfy | Std.Producers.ConcatenatedProducer.Invoke (correctness) (assertion batch 273) | 1.54M | 6.22M | 1.54M |
| std/Actions/Producers.dfy | Std.Producers.ConcatenatedProducer.Invoke (correctness) (assertion batch 214) | 6.00M | 2.75M | 6.00M |
| std/Actions/Producers.dfy | Std.Producers.ConcatenatedProducer.Invoke (correctness) (assertion batch 276) | 4.64M | 6.42M | 4.64M |
