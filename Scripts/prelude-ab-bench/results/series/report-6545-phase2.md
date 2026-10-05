# #6545 A/B benchmark (public corpora, seeds 1-4)

Seeds per (VC, prelude): 4 (1, 2, 3, 4; 0 is Dafny's default). VCs: 3879 in 16 jobs; **3879 affected** (master and PR counts differ), 0 unaffected (identical counts under master and PR for every seed).
Unaffected VCs whose counts differ under the placebo: 0.

## Proof cost over affected VCs that pass everywhere

Totals are sums of per-VC means over seeds. "Per program" averages each program's own VC geomean, so a
program with hundreds of VCs weighs no more than one with two. Brackets are 95% bootstrap intervals that
resample programs, not VCs.

| group | programs | VCs | largest program | total PR/master | geomean over VCs | per program | placebo per program |
|---|---:|---:|---|---|---|---|---|
| all but synth | 16 | 3833 | std/Actions/Producers.dfy (53% of VCs) | -6.1% [-26.6%, +13.1%] | -0.9% [-3.3%, -0.1%] | -2.6% [-5.2%, +0.2%] | -0.0% [-0.5%, +0.3%] |
| dafnybench | 1 | 20 | dafnybench/dafny_experiments_tmp_tmpz29_3_3i_circuit.dfy (100% of VCs) | +11.4% [+11.4%, +11.4%] | +1.1% [+1.1%, +1.1%] | +1.1% [+1.1%, +1.1%] | +1.0% [+1.0%, +1.0%] |
| kondo | 1 | 90 | kondo/twoPhaseCommit/sync (100% of VCs) | -87.2% [-87.2%, -87.2%] | -4.7% [-4.7%, -4.7%] | -4.7% [-4.7%, -4.7%] | -0.8% [-0.8%, -0.8%] |
| libraries | 4 | 382 | libraries/NonlinearArithmetic/DivMod.dfy (66% of VCs) | +16.2% [-16.5%, +36.2%] | -3.8% [-4.7%, -1.8%] | -3.8% [-5.2%, -2.1%] | -0.1% [-0.2%, +0.0%] |
| lit | 7 | 545 | lit/concurrency/12-MutexLifetime-short.dfy (71% of VCs) | -6.0% [-46.9%, +33.5%] | +0.0% [-4.9%, +2.7%] | -2.6% [-8.6%, +3.6%] | -0.3% [-1.0%, +0.5%] |
| std | 3 | 2796 | std/Actions/Producers.dfy (72% of VCs) | +2.2% [-18.3%, +6.8%] | -0.5% [-4.2%, -0.0%] | -1.5% [-4.2%, -0.0%] | +0.4% [+0.0%, +1.1%] |

46 affected VCs fail (a verification error) in some run; their cost is the solver's search for a counterexample, reported separately:

| job | VC | master mean (min..max) | PR mean (min..max) | placebo mean |
|---|---|---|---|---|
| lit/dafny2/SnapshotableTrees.dfy:refresh | SnapTree.Node.MutatingInsert_Right (correctness) | 500.04M (500.04..500.04) | 500.04M (500.04..500.04) | 500.04M |
| lit/dafny2/SnapshotableTrees.dfy:refresh | SnapTree.Node.FunctionalInsert_Right (correctness) | 500.04M (500.04..500.04) | 500.04M (500.04..500.04) | 500.04M |
| lit/dafny2/SnapshotableTrees.dfy:refresh | SnapTree.Node.FunctionalInsert_Left (correctness) | 463.52M (358.29..500.04) | 465.42M (361.55..500.04) | 466.58M |
| lit/dafny2/SnapshotableTrees.dfy:refresh | SnapTree.Node.MutatingInsert_Left (correctness) | 331.76M (130.23..500.04) | 500.04M (500.04..500.04) | 500.04M |
| libraries/dafny/Collections/Seqs.dfy | Dafny.Collections.Seq.LemmaMapDistributesOverConcat (correctness) | 296.29M (141.61..500.02) | 266.70M (2.33..469.48) | 305.37M |
| dafnybench/dafny_experiments_tmp_tmpz29_3_3i_circuit.dfy | CombineCircuits.CombineCircuitsCorrect (correctness) | 278.32M (214.71..387.99) | 307.11M (229.29..499.60) | 311.76M |
| lit/dafny1/ExtensibleArrayAuto.dfy:refresh | ExtensibleArray.Append (correctness) | 267.35M (19.20..500.05) | 385.55M (42.06..500.05) | 326.64M |
| lit/dafny2/SnapshotableTrees.dfy:refresh | SnapTree.Iterator.Push (correctness) (assertion batch 2) | 243.21M (0.18..500.04) | 0.27M (0.15..0.54) | 250.52M |
| lit/dafny2/SnapshotableTrees.dfy:refresh | SnapTree.Iterator.Push (correctness) (assertion batch 13) | 179.42M (1.06..500.03) | 8.83M (0.74..29.85) | 393.00M |
| std/Actions/Producers.dfy | Std.Producers.ConcatenatedProducer.Invoke (correctness) (assertion batch 277) | 81.19M (24.21..100.19) | 72.97M (15.24..100.19) | 74.97M |

## Total proof RU per seed (affected VCs that pass everywhere)

| prelude | seed 1 | seed 2 | seed 3 | seed 4 | mean | sd |
|---|---:|---:|---:|---:|---:|---:|
| master | 1607.3M | 1385.1M | 1223.9M | 1222.2M | 1359.6M | 157.6M |
| pr | 1512.0M | 1258.1M | 1090.9M | 1247.1M | 1277.1M | 150.9M |
| placebo | 1517.2M | 1695.5M | 1178.1M | 1203.5M | 1398.6M | 217.3M |

## Solver time over those proofs (sum of per-VC means, seconds)

| group | master | PR | placebo |
|---|---:|---:|---:|
| all | 895.0 | 854.1 | 890.2 |
| lit | 526.8 | 506.0 | 554.6 |
| std | 313.5 | 329.2 | 305.0 |

## Distribution of per-VC cost ratios over those proofs (mean over seeds)

| ratio bucket | PR/master | placebo/master |
|---|---:|---:|
| < 0.5x | 4 | 3 |
| 0.5-0.8x | 25 | 5 |
| 0.8-0.95x | 290 | 23 |
| 0.95-1.05x | 3406 | 3769 |
| 1.05-1.25x | 76 | 23 |
| 1.25-2x | 25 | 8 |
| 2-4x | 5 | 1 |
| >= 4x | 2 | 1 |

## Verdict changes at each job's limit (seeds passing out of 4)

| job | VC | limit | master ok | PR ok | placebo ok | master RU | PR RU |
|---|---|---:|---:|---:|---:|---:|---:|
| dafnybench/dafny_experiments_tmp_tmpz29_3_3i_circuit.dfy | BackwardConnections.CombineBackconnsHelper (correctness) | 50M | 4 | 3 | 2 | 8.19M | 29.50M |
| kondo/twoPhaseCommit/sync | TwoPCInvariantProof.InvNextLeaderTallyReflectsPreferences (correctness) | 50M | 2 | 4 | 3 | 58.07M | 2.62M |
| libraries/Collections/Sequences/LittleEndianNatConversions.dfy | LittleEndianNatConversions.LemmaSmallLargeSmall (correctness) | 40M | 4 | 3 | 4 | 17.40M | 52.04M |
| libraries/NonlinearArithmetic/DivMod.dfy | DivMod.LemmaHoistOverDenominator (correctness) | 40M | 4 | 4 | 3 | 4.17M | 2.52M |
| libraries/NonlinearArithmetic/DivMod.dfy | DivMod.LemmaMultiplyDivideLt (correctness) | 40M | 3 | 3 | 0 | 0.85M | 0.89M |
| libraries/dafny/Collections/LittleEndianNatConversions.dfy | Dafny.Collections.LittleEndianNatConversions.LemmaSmallLargeSmall (correctness) | 40M | 3 | 1 | 3 | 30.09M | 128.88M |
| libraries/dafny/Collections/Seqs.dfy | Dafny.Collections.Seq.LemmaFilterDistributesOverConcat (correctness) (assertion batch 2) | 40M | 3 | 0 | 2 | 50.71M | 94.02M |
| libraries/dafny/Collections/Seqs.dfy | Dafny.Collections.Seq.LemmaMapDistributesOverConcat (correctness) | 40M | 0 | 1 | 0 | 296.29M | 266.70M |
| lit/concurrency/12-MutexLifetime-short.dfy:refresh | Lifetime._ctor (correctness) | 50M | 4 | 4 | 3 | 32.07M | 32.45M |
| lit/concurrency/12-MutexLifetime-short.dfy:refresh | MutexGuardU32._ctor (correctness) (assertion batch 132) | 50M | 0 | 3 | 1 | 106.62M | 54.31M |
| lit/concurrency/12-MutexLifetime-short.dfy:refresh | MutexGuardU32._ctor (correctness) (assertion batch 96) | 50M | 3 | 4 | 3 | 46.78M | 39.97M |
| lit/dafny0/FunctionSpecifications.dfy:refresh | GoodPost (well-formedness) | 50M | 3 | 2 | 3 | 77.80M | 155.87M |
| lit/dafny1/ExtensibleArrayAuto.dfy:refresh | ExtensibleArray.Append (correctness) | 50M | 1 | 1 | 0 | 267.35M | 385.55M |
| lit/dafny1/ExtensibleArrayAuto.dfy:refresh | ExtensibleArray.Set (correctness) | 50M | 3 | 4 | 4 | 24.37M | 13.68M |
| lit/dafny2/SmallestMissingNumber-functional.dfy:refresh | SMN''_Correct (correctness) | 50M | 4 | 3 | 4 | 11.52M | 47.79M |
| lit/dafny2/SmallestMissingNumber-functional.dfy:refresh | SMN'_Correct (correctness) | 50M | 0 | 1 | 0 | 93.96M | 82.56M |
| lit/dafny2/SmallestMissingNumber-functional.dfy:refresh | SMN_Correct (correctness) | 50M | 4 | 2 | 4 | 14.78M | 40.44M |
| lit/dafny2/SnapshotableTrees.dfy:refresh | SnapTree.Iterator.Push (correctness) (assertion batch 13) | 50M | 1 | 4 | 0 | 179.42M | 8.83M |
| lit/dafny2/SnapshotableTrees.dfy:refresh | SnapTree.Iterator.Push (correctness) (assertion batch 2) | 50M | 2 | 4 | 2 | 243.21M | 0.27M |
| lit/dafny2/SnapshotableTrees.dfy:refresh | SnapTreeTestHarness.Main (correctness) | 50M | 2 | 3 | 2 | 4.99M | 5.30M |
| lit/dafny4/Lucas-down.dfy:refresh | Lucas_Binary'' (correctness) | 50M | 3 | 4 | 3 | 20.71M | 7.28M |
| lit/vstte2012/RingBufferAuto.dfy:refresh | RingBuffer.Clear (correctness) | 50M | 2 | 1 | 2 | 4.59M | 8.18M |
| std/Actions/Producers.dfy | Std.Producers.ConcatenatedProducer.Invoke (correctness) (assertion batch 273) | 100M | 3 | 4 | 4 | 31.73M | 2.34M |
| std/Actions/Producers.dfy | Std.Producers.ConcatenatedProducer.Invoke (correctness) (assertion batch 275) | 100M | 2 | 3 | 3 | 59.28M | 56.01M |
| std/Actions/Producers.dfy | Std.Producers.ConcatenatedProducer.Invoke (correctness) (assertion batch 277) | 100M | 1 | 2 | 2 | 81.19M | 72.97M |
| std/Actions/Producers.dfy | Std.Producers.FilteredProducer.Invoke (correctness) | 50M | 4 | 3 | 4 | 10.84M | 9.04M |
| std/Actions/Producers.dfy | Std.Producers.FlattenedProducer.Invoke (correctness) | 100M | 4 | 4 | 3 | 36.31M | 45.58M |
| std/Actions/Producers.dfy | Std.Producers.MappedProducer.Invoke (correctness) | 10M | 3 | 4 | 2 | 9.05M | 7.50M |
| std/Actions/Producers.dfy | Std.Producers.ProducerState.ValidChangeTransitive (correctness) (assertion batch 90) | none | 3 | 4 | 3 | 1.26M | 0.17M |
| std/Arithmetic/DivMod.dfy | Std.Arithmetic.DivMod.LemmaFundamentalDivModConverse (correctness) | 50M | 3 | 4 | 3 | 16.98M | 12.10M |
| std/Arithmetic/DivMod.dfy | Std.Arithmetic.DivMod.LemmaMultiplyDivideLt (correctness) | 50M | 2 | 3 | 2 | 1.20M | 0.96M |
| std/Base64.dfy | Std.Base64.DecodeValidEncode2Padding (correctness) | 5M | 2 | 3 | 2 | 4.11M | 3.28M |
| std/Base64.dfy | Std.Base64.DecodeValidUnpaddedPartialFrom1PaddedSeq (well-formedness) | 5M | 4 | 3 | 3 | 1.51M | 17.68M |
| std/Base64.dfy | Std.Base64.EncodeBVIsBase64 (correctness) | 5M | 1 | 0 | 0 | 14.24M | 70.61M |
| std/Base64.dfy | Std.Base64.EncodeBVLengthCongruentToZeroMod4 (correctness) (assertion batch 5) | 50M | 4 | 3 | 3 | 5.96M | 25.88M |

## Largest changes among those proofs (by |PR - master| mean RU)

| job | VC | master | PR | PR/master | placebo | min..max master | min..max PR |
|---|---|---:|---:|---:|---:|---|---|
| kondo/twoPhaseCommit/sync | TwoPCInvariantProof.InvNextLeaderTallyReflectsPreferences (correctness) | 58.07M | 2.62M | 0.05 | 28.75M | 0.67..131.29M | 1.09..7.05M |
| lit/concurrency/12-MutexLifetime-short.dfy:refresh | MutexGuardU32._ctor (correctness) (assertion batch 132) | 106.62M | 54.31M | 0.51 | 112.43M | 59.24..164.93M | 46.08..71.70M |
| lit/dafny2/SmallestMissingNumber-functional.dfy:refresh | SMN''_Correct (correctness) | 11.52M | 47.79M | 4.15 | 6.21M | 4.62..28.21M | 5.09..160.24M |
| lit/dafny2/SmallestMissingNumber-functional.dfy:refresh | SMN_Correct (correctness) | 14.78M | 40.44M | 2.74 | 28.24M | 3.58..20.44M | 13.45..68.41M |
| std/Base64.dfy | Std.Base64.DecodeValidUnpaddedPartialFrom1PaddedSeq (well-formedness) | 1.51M | 17.68M | 11.74 | 47.76M | 0.46..3.04M | 1.05..66.54M |
| lit/dafny4/Lucas-down.dfy:refresh | Lucas_Binary'' (correctness) | 20.71M | 7.28M | 0.35 | 20.71M | 3.60..61.38M | 1.91..19.71M |
| std/Base64.dfy | Std.Base64.UInt8sToBVsToUInt8s (correctness) (assertion batch 3) | 35.68M | 22.29M | 0.62 | 35.68M | 0.41..73.49M | 0.41..68.12M |
| lit/dafny2/SmallestMissingNumber-functional.dfy:refresh | SMN'_Correct (correctness) | 93.96M | 82.56M | 0.88 | 111.82M | 62.21..122.19M | 26.73..136.94M |
| lit/dafny1/ExtensibleArrayAuto.dfy:refresh | ExtensibleArray.Set (correctness) | 24.37M | 13.68M | 0.56 | 19.21M | 2.49..84.48M | 2.54..32.01M |
| std/Actions/Producers.dfy | Std.Producers.ConcatenatedProducer.Invoke (correctness) (assertion batch 276) | 6.02M | 15.07M | 2.51 | 7.81M | 4.61..10.20M | 4.20..47.09M |
| std/Actions/Producers.dfy | Std.Producers.ConcatenatedProducer.Invoke (correctness) (assertion batch 283) | 30.22M | 38.27M | 1.27 | 27.11M | 6.80..66.34M | 17.13..74.35M |
| lit/concurrency/12-MutexLifetime-short.dfy:refresh | MutexGuardU32._ctor (correctness) (assertion batch 96) | 46.78M | 39.97M | 0.85 | 47.03M | 38.80..58.15M | 31.38..49.13M |
| libraries/NonlinearArithmetic/DivMod.dfy | DivMod.LemmaFundamentalDivModConverse (correctness) | 5.27M | 11.90M | 2.26 | 5.08M | 4.97..5.82M | 4.64..32.64M |
| lit/dafny2/SnapshotableTrees.dfy:refresh | SnapTree.Tree.Insert (correctness) | 6.14M | 0.62M | 0.10 | 5.27M | 2.95..14.23M | 0.57..0.74M |
| lit/concurrency/12-MutexLifetime-short.dfy:refresh | MutexGuardU32._ctor (correctness) (assertion batch 86) | 19.02M | 24.15M | 1.27 | 18.08M | 13.86..22.30M | 20.79..28.21M |
| lit/concurrency/12-MutexLifetime-short.dfy:refresh | MutexGuardU32._ctor (correctness) (assertion batch 114) | 21.67M | 16.92M | 0.78 | 19.78M | 17.45..26.77M | 10.39..21.85M |
| lit/concurrency/12-MutexLifetime-short.dfy:refresh | MutexGuardU32._ctor (correctness) (assertion batch 134) | 9.47M | 13.40M | 1.42 | 8.94M | 7.15..14.59M | 6.14..20.30M |
| lit/concurrency/12-MutexLifetime-short.dfy:refresh | MutexGuardU32._ctor (correctness) (assertion batch 73) | 5.96M | 9.19M | 1.54 | 6.45M | 4.59..7.04M | 6.11..14.75M |
| lit/concurrency/12-MutexLifetime-short.dfy:refresh | MutexGuardU32._ctor (correctness) (assertion batch 90) | 14.91M | 11.89M | 0.80 | 14.82M | 11.98..20.74M | 11.39..12.62M |
| std/Arithmetic/DivMod.dfy | Std.Arithmetic.DivMod.LemmaRoundDown (correctness) | 2.87M | 0.65M | 0.23 | 0.64M | 0.32..6.49M | 0.59..0.73M |
| std/Base64.dfy | Std.Base64.DecodeValidEncode1Padding (correctness) | 1.77M | 3.82M | 2.15 | 2.70M | 1.26..2.40M | 1.06..10.23M |
| lit/concurrency/12-MutexLifetime-short.dfy:refresh | OutlivesClaim._ctor (correctness) (assertion batch 2) | 19.09M | 17.18M | 0.90 | 17.36M | 13.02..33.48M | 12.37..20.59M |
| lit/concurrency/12-MutexLifetime-short.dfy:refresh | MutexGuardU32._ctor (correctness) (assertion batch 113) | 4.15M | 5.79M | 1.40 | 4.13M | 3.18..4.75M | 5.21..6.87M |
| std/Base64.dfy | Std.Base64.DecodeEncodeRecursively (correctness) (assertion batch 24) | 2.63M | 4.16M | 1.58 | 2.63M | 0.65..6.78M | 0.10..13.28M |
| lit/concurrency/12-MutexLifetime-short.dfy:refresh | MutexGuardU32._ctor (correctness) (assertion batch 66) | 34.21M | 32.70M | 0.96 | 32.23M | 30.25..42.97M | 29.54..35.98M |

## Per job (proofs among the affected VCs)

| job | VCs | master | PR | PR vs master | placebo vs master |
|---|---:|---:|---:|---:|---:|
| lit/concurrency/12-MutexLifetime-short.dfy:refresh | 386 | 533.50M | 468.11M | -12.3% | -0.5% |
| std/Actions/Producers.dfy | 2023 | 451.97M | 460.83M | +2.0% | -0.4% |
| lit/dafny2/SmallestMissingNumber-functional.dfy:refresh | 19 | 120.74M | 171.26M | +41.8% | +21.5% |
| std/Base64.dfy | 479 | 80.49M | 85.94M | +6.8% | +68.8% |
| kondo/twoPhaseCommit/sync | 90 | 63.86M | 8.16M | -87.2% | -46.1% |
| lit/dafny1/ExtensibleArrayAuto.dfy:refresh | 8 | 27.11M | 15.83M | -41.6% | -18.1% |
| lit/dafny4/Lucas-down.dfy:refresh | 12 | 20.97M | 7.55M | -64.0% | +0.0% |
| libraries/NonlinearArithmetic/DivMod.dfy | 253 | 16.32M | 22.45M | +37.6% | -2.2% |
| lit/dafny2/SnapshotableTrees.dfy:refresh | 99 | 15.47M | 11.41M | -26.3% | -5.7% |
| std/Arithmetic/DivMod.dfy | 294 | 13.97M | 11.41M | -18.3% | -6.5% |
| libraries/dafny/Collections/Seqs.dfy | 77 | 9.15M | 7.56M | -17.4% | -14.3% |
| lit/vstte2012/RingBufferAuto.dfy:refresh | 11 | 2.16M | 2.49M | +15.1% | -4.2% |
| libraries/dafny/Collections/LittleEndianNatConversions.dfy | 26 | 1.76M | 1.72M | -2.3% | +0.2% |
| dafnybench/dafny_experiments_tmp_tmpz29_3_3i_circuit.dfy | 20 | 1.18M | 1.31M | +11.4% | +4.2% |
| libraries/Collections/Sequences/LittleEndianNatConversions.dfy | 26 | 0.90M | 0.96M | +7.4% | -0.0% |
| lit/dafny0/FunctionSpecifications.dfy:refresh | 10 | 0.07M | 0.07M | -7.8% | +0.0% |

## Stability over the affected VCs (all but synth)

Flaky: some seeds pass at the job's limit and others do not. Spread: the coefficient of variation of a VC's cost across seeds, for VCs above 1M RU under master.

| prelude | flaky VCs | flaky, not under master | no longer flaky | median spread | 90th-percentile spread |
|---|---:|---:|---:|---:|---:|
| master | 26 | 0 | 0 | 0.23 | 0.93 |
| master2 | 26 | 0 | 0 | 0.23 | 0.93 |
| placebo | 27 | 7 | 6 | 0.23 | 0.93 |
| pr | 24 | 10 | 12 | 0.16 | 0.93 |

Flaky under the PR but not under master (seeds passing out of the run):

| job | VC | master | PR | placebo | PR mean RU |
|---|---|---:|---:|---:|---:|
| libraries/dafny/Collections/Seqs.dfy | Dafny.Collections.Seq.LemmaMapDistributesOverConcat (correctness) | 0 | 1 | 0 | 266.70M |
| lit/dafny2/SmallestMissingNumber-functional.dfy:refresh | SMN'_Correct (correctness) | 0 | 1 | 0 | 82.56M |
| lit/concurrency/12-MutexLifetime-short.dfy:refresh | MutexGuardU32._ctor (correctness) (assertion batch 132) | 0 | 3 | 1 | 54.31M |
| libraries/Collections/Sequences/LittleEndianNatConversions.dfy | LittleEndianNatConversions.LemmaSmallLargeSmall (correctness) | 4 | 3 | 4 | 52.04M |
| lit/dafny2/SmallestMissingNumber-functional.dfy:refresh | SMN''_Correct (correctness) | 4 | 3 | 4 | 47.79M |
| lit/dafny2/SmallestMissingNumber-functional.dfy:refresh | SMN_Correct (correctness) | 4 | 2 | 4 | 40.44M |
| dafnybench/dafny_experiments_tmp_tmpz29_3_3i_circuit.dfy | BackwardConnections.CombineBackconnsHelper (correctness) | 4 | 3 | 2 | 29.50M |
| std/Base64.dfy | Std.Base64.EncodeBVLengthCongruentToZeroMod4 (correctness) (assertion batch 5) | 4 | 3 | 3 | 25.88M |
| std/Base64.dfy | Std.Base64.DecodeValidUnpaddedPartialFrom1PaddedSeq (well-formedness) | 4 | 3 | 3 | 17.68M |
| std/Actions/Producers.dfy | Std.Producers.FilteredProducer.Invoke (correctness) | 4 | 3 | 4 | 9.04M |

## Comparisons over the affected proofs (all but synth)

| comparison | programs | VCs | total | geomean over VCs | per program | verdict flips at limit |
|---|---:|---:|---|---|---|---:|
| A/A: master2 vs master (same input, another process) | 16 | 3833 | +0.0% [-0.0%, +0.0%] | +0.0% [-0.0%, +0.0%] | +0.0% [-0.0%, +0.0%] | 0 |
| placebo vs master (the old axiom, rewritten) | 16 | 3833 | +2.9% [-8.4%, +24.2%] | +0.1% [-0.2%, +0.6%] | -0.0% [-0.5%, +0.3%] | 5 |
| pr vs master | 16 | 3833 | -6.1% [-26.2%, +12.2%] | -0.9% [-3.1%, -0.2%] | -2.6% [-5.1%, +0.4%] | 10 |

## Comparisons over the external programs' affected proofs

| comparison | programs | VCs | total | geomean over VCs | per program | verdict flips at limit |
|---|---:|---:|---|---|---|---:|
| A/A: master2 vs master (same input, another process) | 6 | 492 | +0.0% [+0.0%, +0.0%] | +0.0% [+0.0%, +0.0%] | +0.0% [+0.0%, +0.0%] | 0 |
| placebo vs master (the old axiom, rewritten) | 6 | 492 | -33.3% [-44.6%, -1.1%] | -0.2% [-0.6%, +0.2%] | -0.0% [-0.4%, +0.5%] | 1 |
| pr vs master | 6 | 492 | -54.7% [-83.5%, +33.4%] | -3.8% [-4.5%, -1.7%] | -3.1% [-4.7%, -1.1%] | 1 |

## Alternative sound encodings, over the same proofs

restrict: elements defined everywhere, `$ArbitraryBoxValue` outside the domain. domguard: the PR's axiom guarded by `Map#Domain(Map#Glue(a, b, t))`. eager: the PR's axiom plus the trigger `{ Map#Glue(a, b, t), Set#IsMember(a, bx) }`.

| encoding | programs | VCs | total vs master | geomean over VCs vs master | per program vs master | per program vs PR | verdict flips vs master at limit |
|---|---:|---:|---|---|---|---|---:|
| pr | 16 | 3833 | -6.1% [-28.5%, +12.4%] | -0.9% [-3.3%, -0.1%] | -2.6% [-5.2%, +0.4%] |  | 30 |
| master2 | 16 | 3833 | +0.0% [-0.0%, +0.0%] | +0.0% [-0.0%, +0.0%] | +0.0% [-0.0%, +0.0%] | +2.7% [-0.3%, +5.6%] | 0 |

master2: largest differences from the PR

| job | VC | master | PR | master2 |
|---|---|---:|---:|---:|
| kondo/twoPhaseCommit/sync | TwoPCInvariantProof.InvNextLeaderTallyReflectsPreferences (correctness) | 58.07M | 2.62M | 58.07M |
| lit/concurrency/12-MutexLifetime-short.dfy:refresh | MutexGuardU32._ctor (correctness) (assertion batch 132) | 106.62M | 54.31M | 106.62M |
| lit/dafny2/SmallestMissingNumber-functional.dfy:refresh | SMN''_Correct (correctness) | 11.52M | 47.79M | 11.52M |
| lit/dafny2/SmallestMissingNumber-functional.dfy:refresh | SMN_Correct (correctness) | 14.78M | 40.44M | 14.78M |
| std/Base64.dfy | Std.Base64.DecodeValidUnpaddedPartialFrom1PaddedSeq (well-formedness) | 1.51M | 17.68M | 1.51M |
| lit/dafny4/Lucas-down.dfy:refresh | Lucas_Binary'' (correctness) | 20.71M | 7.28M | 20.71M |
