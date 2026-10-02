# #6545 on its own edited programs (seeds 1-4)

Seeds per (VC, prelude): 4 (1, 2, 3, 4; 0 is Dafny's default). VCs: 4475 in 10 jobs; **4475 affected** (master and PR counts differ), 0 unaffected (identical counts under master and PR for every seed).

## Proof cost over affected VCs that pass everywhere

Totals are sums of per-VC means over seeds. "Per program" averages each program's own VC geomean, so a
program with hundreds of VCs weighs no more than one with two. Brackets are 95% bootstrap intervals that
resample programs, not VCs.

| group | programs | VCs | largest program | total PR/master | geomean over VCs | per program |
|---|---:|---:|---|---|---|---|
| all but synth | 10 | 4463 | std/Actions/Producers.dfy (68% of VCs) | +5.0% [-5.6%, +30.3%] | -0.3% [-2.1%, +0.3%] | -0.1% [-2.3%, +2.9%] |
| lit | 5 | 480 | lit/dafny1/SchorrWaite-stages.dfy (51% of VCs) | +19.4% [-14.4%, +39.3%] | +0.9% [+0.1%, +3.3%] | +2.6% [+0.1%, +7.3%] |
| std | 5 | 3983 | std/Actions/Producers.dfy (77% of VCs) | +0.8% [-1.9%, +1.2%] | -0.4% [-4.2%, -0.0%] | -2.7% [-4.3%, -1.0%] |

12 affected VCs fail (a verification error) in some run; their cost is the solver's search for a counterexample, reported separately:

| job | VC | master mean (min..max) | PR mean (min..max) |
|---|---|---|---|
| std/Actions/Producers.dfy | Std.Producers.ConcatenatedProducer.Invoke (correctness) (assertion batch 277) | 81.19M (24.21..100.19) | 72.97M (15.24..100.19) |
| std/Actions/Producers.dfy | Std.Producers.ConcatenatedProducer.Invoke (correctness) (assertion batch 275) | 59.28M (4.62..100.19) | 56.01M (4.50..100.19) |
| std/Actions/Producers.dfy | Std.Producers.ConcatenatedProducer.Invoke (correctness) (assertion batch 273) | 31.73M (1.54..100.19) | 2.34M (2.10..2.61) |
| std/Base64.dfy | Std.Base64.EncodeBVIsBase64 (correctness) (assertion batch 7) | 14.08M (1.98..50.06) | 25.55M (0.35..50.06) |
| std/Arithmetic/DivMod.dfy | Std.Arithmetic.DivMod.LemmaFundamentalDivModConverse (correctness) | 12.30M (12.07..12.54) | 71.29M (10.77..249.84) |
| std/Actions/Producers.dfy | Std.Producers.FilteredProducer.Invoke (correctness) | 10.84M (7.63..15.94) | 9.04M (7.78..9.70) |
| std/Actions/Producers.dfy | Std.Producers.MappedProducer.Invoke (correctness) | 9.05M (8.38..10.22) | 7.50M (6.24..8.38) |
| std/Base64.dfy | Std.Base64.EncodeBVLengthCongruentToZeroMod4 (correctness) (assertion batch 5) | 5.96M (4.71..8.58) | 25.88M (0.60..50.05) |
| std/Base64.dfy | Std.Base64.DecodeValidEncode1Padding (correctness) (assertion batch 56) | 4.36M (1.38..12.06) | 7.53M (2.80..12.06) |
| std/Actions/Producers.dfy | Std.Producers.ProducerState.ValidChangeTransitive (correctness) (assertion batch 90) | 1.24M (0.22..4.04) | 0.17M (0.11..0.23) |

## Total proof RU per seed (affected VCs that pass everywhere)

| prelude | seed 1 | seed 2 | seed 3 | seed 4 | mean | sd |
|---|---:|---:|---:|---:|---:|---:|
| master | 1068.7M | 1028.5M | 1043.2M | 1103.9M | 1061.0M | 28.6M |
| pr | 1346.9M | 1075.4M | 934.6M | 1101.1M | 1114.5M | 148.4M |

## Solver time over those proofs (sum of per-VC means, seconds)

| group | master | PR |
|---|---:|---:|
| all | 753.4 | 812.2 |
| lit | 149.7 | 186.1 |
| std | 603.7 | 626.0 |

## Distribution of per-VC cost ratios over those proofs (mean over seeds)

| ratio bucket | PR/master |
|---|---:|
| < 0.5x | 0 |
| 0.5-0.8x | 17 |
| 0.8-0.95x | 199 |
| 0.95-1.05x | 4154 |
| 1.05-1.25x | 74 |
| 1.25-2x | 14 |
| 2-4x | 3 |
| >= 4x | 2 |

## Verdict changes at each job's limit (seeds passing out of 4)

| job | VC | limit | master ok | PR ok | master RU | PR RU |
|---|---|---:|---:|---:|---:|---:|
| lit/dafny1/ExtensibleArrayAuto.dfy:refresh | ExtensibleArray.Set (correctness) | 50M | 3 | 4 | 24.37M | 13.68M |
| lit/dafny1/SchorrWaite-stages.dfy:refresh | M0.SchorrWaite (correctness) (assertion batch 40) | 50M | 4 | 3 | 15.57M | 22.87M |
| lit/dafny2/SmallestMissingNumber-functional.dfy:refresh | SMN''_Correct (correctness) | 50M | 4 | 3 | 11.52M | 47.79M |
| lit/dafny2/SmallestMissingNumber-functional.dfy:refresh | SMN_Correct (correctness) | 50M | 4 | 2 | 14.78M | 40.44M |
| std/Actions/Producers.dfy | Std.Producers.ConcatenatedProducer.Invoke (correctness) (assertion batch 273) | 100M | 3 | 4 | 31.73M | 2.34M |
| std/Actions/Producers.dfy | Std.Producers.ConcatenatedProducer.Invoke (correctness) (assertion batch 275) | 100M | 2 | 3 | 59.28M | 56.01M |
| std/Actions/Producers.dfy | Std.Producers.ConcatenatedProducer.Invoke (correctness) (assertion batch 277) | 100M | 1 | 2 | 81.19M | 72.97M |
| std/Actions/Producers.dfy | Std.Producers.FilteredProducer.Invoke (correctness) | 50M | 4 | 3 | 10.84M | 9.04M |
| std/Actions/Producers.dfy | Std.Producers.MappedProducer.Invoke (correctness) | 10M | 3 | 4 | 9.05M | 7.50M |
| std/Arithmetic/DivMod.dfy | Std.Arithmetic.DivMod.LemmaFundamentalDivModConverse (correctness) | 50M | 4 | 3 | 12.30M | 71.29M |
| std/Base64.dfy | Std.Base64.DecodeValidEncode1Padding (correctness) (assertion batch 56) | 12M | 3 | 2 | 4.36M | 7.53M |
| std/Base64.dfy | Std.Base64.DecodeValidEncode2Padding (correctness) | 5M | 2 | 3 | 4.11M | 3.28M |
| std/Base64.dfy | Std.Base64.DecodeValidUnpaddedPartialFrom1PaddedSeq (well-formedness) | 5M | 4 | 3 | 1.51M | 17.68M |
| std/Base64.dfy | Std.Base64.EncodeBVIsBase64 (correctness) (assertion batch 7) | 50M | 3 | 2 | 14.08M | 25.55M |
| std/Base64.dfy | Std.Base64.EncodeBVLengthCongruentToZeroMod4 (correctness) (assertion batch 5) | 50M | 4 | 3 | 5.96M | 25.88M |

## Largest changes among those proofs (by |PR - master| mean RU)

| job | VC | master | PR | PR/master | min..max master | min..max PR |
|---|---|---:|---:|---:|---|---|
| lit/dafny2/SmallestMissingNumber-functional.dfy:refresh | SMN''_Correct (correctness) | 11.52M | 47.79M | 4.15 | 4.62..28.21M | 5.09..160.24M |
| lit/dafny2/SmallestMissingNumber-functional.dfy:refresh | SMN_Correct (correctness) | 14.78M | 40.44M | 2.74 | 3.58..20.44M | 13.45..68.41M |
| std/Base64.dfy | Std.Base64.DecodeValidUnpaddedPartialFrom1PaddedSeq (well-formedness) | 1.51M | 17.68M | 11.74 | 0.46..3.04M | 1.05..66.54M |
| std/Base64.dfy | Std.Base64.UInt8sToBVsToUInt8s (correctness) (assertion batch 3) | 35.68M | 22.29M | 0.62 | 0.41..73.49M | 0.41..68.12M |
| lit/dafny2/SmallestMissingNumber-functional.dfy:refresh | SMN'_Correct (correctness) | 93.96M | 82.56M | 0.88 | 62.21..122.19M | 26.73..136.94M |
| lit/dafny1/ExtensibleArrayAuto.dfy:refresh | ExtensibleArray.Set (correctness) | 24.37M | 13.68M | 0.56 | 2.49..84.48M | 2.54..32.01M |
| std/Actions/Producers.dfy | Std.Producers.ConcatenatedProducer.Invoke (correctness) (assertion batch 276) | 6.18M | 15.07M | 2.44 | 4.61..10.20M | 4.20..47.09M |
| std/Actions/Producers.dfy | Std.Producers.ConcatenatedProducer.Invoke (correctness) (assertion batch 283) | 30.22M | 38.27M | 1.27 | 6.80..66.34M | 17.13..74.35M |
| lit/dafny1/SchorrWaite-stages.dfy:refresh | M0.SchorrWaite (correctness) (assertion batch 40) | 15.57M | 22.87M | 1.47 | 1.60..48.22M | 2.22..75.77M |
| std/Base64.dfy | Std.Base64.EncodeBVIsBase64 (correctness) (assertion batch 5) | 11.28M | 6.02M | 0.53 | 0.65..32.85M | 1.41..15.34M |
| lit/dafny4/NumberRepresentations.dfy:refresh | dec (correctness) (assertion batch 17) | 6.58M | 8.63M | 1.31 | 5.22..7.66M | 3.98..11.31M |
| std/Base64.dfy | Std.Base64.DecodeEncodeRecursively (correctness) (assertion batch 24) | 2.63M | 4.16M | 1.58 | 0.65..6.78M | 0.10..13.28M |
| std/Actions/Producers.dfy | Std.Producers.ConcatenatedProducer.Invoke (correctness) (assertion batch 272) | 3.51M | 2.06M | 0.59 | 1.76..8.34M | 1.78..2.64M |
| std/Actions/Producers.dfy | Std.Producers.ConcatenatedProducer.Invoke (correctness) (assertion batch 262) | 2.15M | 1.19M | 0.55 | 1.26..3.43M | 1.10..1.28M |
| std/Base64.dfy | Std.Base64.DecodeValidEncode2Padding (correctness) | 4.11M | 3.28M | 0.80 | 0.81..7.26M | 0.64..10.92M |
| std/Base64.dfy | Std.Base64.AboutDecodeValid (correctness) | 2.60M | 3.41M | 1.31 | 1.84..3.96M | 1.88..7.59M |
| std/Actions/Producers.dfy | Std.Producers.ConcatenatedProducer.Invoke (correctness) (assertion batch 214) | 5.18M | 4.44M | 0.86 | 4.36..6.00M | 3.27..5.19M |
| std/Actions/Producers.dfy | Std.Producers.ConcatenatedProducer.Invoke (correctness) (assertion batch 352) | 7.09M | 6.43M | 0.91 | 5.14..8.74M | 5.37..6.98M |
| std/Actions/Producers.dfy | Std.Producers.ConcatenatedProducer.Invoke (correctness) (assertion batch 360) | 2.60M | 1.96M | 0.75 | 2.40..2.82M | 1.63..2.08M |
| std/Actions/Producers.dfy | Std.Producers.ConcatenatedProducer.Invoke (correctness) (assertion batch 353) | 6.80M | 6.16M | 0.91 | 5.43..8.36M | 5.12..6.73M |
| std/Base64.dfy | Std.Base64.Encode1PaddingIs1Padding (correctness) | 2.96M | 2.40M | 0.81 | 1.70..3.95M | 1.69..3.26M |
| lit/dafny1/ExtensibleArrayAuto.dfy:refresh | Main (correctness) | 1.65M | 1.14M | 0.69 | 1.17..2.88M | 1.03..1.38M |
| std/Actions/Producers.dfy | Std.Producers.MappedProducerOfNewProducers.Invoke (correctness) | 10.05M | 9.58M | 0.95 | 8.71..11.11M | 8.46..11.16M |
| lit/dafny1/ExtensibleArrayAuto.dfy:refresh | ExtensibleArray.Append (correctness) (assertion batch 43) | 1.48M | 1.92M | 1.30 | 1.17..2.01M | 1.48..2.53M |
| std/Actions/Producers.dfy | Std.Producers.ConcatenatedProducer.Invoke (correctness) (assertion batch 354) | 6.58M | 6.15M | 0.93 | 5.23..7.85M | 5.28..7.12M |

## Per job (proofs among the affected VCs)

| job | VCs | master | PR | PR vs master |
|---|---:|---:|---:|---:|
| std/Actions/Producers.dfy | 3053 | 711.04M | 719.54M | +1.2% |
| lit/dafny2/SmallestMissingNumber-functional.dfy:refresh | 19 | 120.74M | 171.26M | +41.8% |
| std/Base64.dfy | 584 | 96.56M | 94.73M | -1.9% |
| lit/dafny1/ExtensibleArrayAuto.dfy:refresh | 77 | 68.09M | 55.91M | -17.9% |
| lit/dafny1/SchorrWaite-stages.dfy:refresh | 247 | 36.42M | 43.41M | +19.2% |
| lit/dafny4/NumberRepresentations.dfy:refresh | 62 | 12.06M | 13.74M | +14.0% |
| std/Arithmetic/DivMod.dfy | 283 | 10.04M | 9.87M | -1.7% |
| lit/vstte2012/Tree.dfy:refresh | 75 | 4.83M | 4.83M | +0.0% |
| std/Arithmetic/Mul.dfy | 54 | 0.82M | 0.79M | -3.8% |
| std/Arithmetic/Power2.dfy | 9 | 0.44M | 0.43M | -1.1% |

## Stability over the affected VCs (all but synth)

Flaky: some seeds pass at the job's limit and others do not. Spread: the coefficient of variation of a VC's cost across seeds, for VCs above 1M RU under master.

| prelude | flaky VCs | flaky, not under master | no longer flaky | median spread | 90th-percentile spread |
|---|---:|---:|---:|---:|---:|
| master | 9 | 0 | 0 | 0.21 | 0.99 |
| pr | 13 | 7 | 3 | 0.15 | 0.96 |

Flaky under the PR but not under master (seeds passing out of the run):

| job | VC | master | PR | PR mean RU |
|---|---|---:|---:|---:|
| std/Arithmetic/DivMod.dfy | Std.Arithmetic.DivMod.LemmaFundamentalDivModConverse (correctness) | 4 | 3 | 71.29M |
| lit/dafny2/SmallestMissingNumber-functional.dfy:refresh | SMN''_Correct (correctness) | 4 | 3 | 47.79M |
| lit/dafny2/SmallestMissingNumber-functional.dfy:refresh | SMN_Correct (correctness) | 4 | 2 | 40.44M |
| std/Base64.dfy | Std.Base64.EncodeBVLengthCongruentToZeroMod4 (correctness) (assertion batch 5) | 4 | 3 | 25.88M |
| lit/dafny1/SchorrWaite-stages.dfy:refresh | M0.SchorrWaite (correctness) (assertion batch 40) | 4 | 3 | 22.87M |
| std/Base64.dfy | Std.Base64.DecodeValidUnpaddedPartialFrom1PaddedSeq (well-formedness) | 4 | 3 | 17.68M |
| std/Actions/Producers.dfy | Std.Producers.FilteredProducer.Invoke (correctness) | 4 | 3 | 9.04M |

## Comparisons over the affected proofs (all but synth)

| comparison | programs | VCs | total | geomean over VCs | per program | verdict flips at limit |
|---|---:|---:|---|---|---|---:|
| pr vs master | 10 | 4463 | +5.0% [-5.8%, +30.2%] | -0.3% [-2.2%, +0.3%] | -0.1% [-2.4%, +3.2%] | 6 |
