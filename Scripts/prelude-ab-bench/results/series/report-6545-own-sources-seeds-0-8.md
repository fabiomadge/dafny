# #6545 on its own edited programs (seeds 0-8)

Seeds per (VC, prelude): 9 (0, 1, 2, 3, 4, 5, 6, 7, 8; 0 is Dafny's default). VCs: 4475 in 10 jobs; **4475 affected** (master and PR counts differ), 0 unaffected (identical counts under master and PR for every seed).

## Proof cost over affected VCs that pass everywhere

Totals are sums of per-VC means over seeds. "Per program" averages each program's own VC geomean, so a
program with hundreds of VCs weighs no more than one with two. Brackets are 95% bootstrap intervals that
resample programs, not VCs.

| group | programs | VCs | largest program | total PR/master | geomean over VCs | per program |
|---|---:|---:|---|---|---|---|
| all but synth | 10 | 4461 | std/Actions/Producers.dfy (68% of VCs) | +2.8% [-8.4%, +23.4%] | -0.3% [-2.3%, +0.2%] | -0.5% [-2.4%, +1.8%] |
| lit | 5 | 478 | lit/dafny1/SchorrWaite-stages.dfy (51% of VCs) | +12.0% [-14.9%, +32.1%] | +0.3% [-0.7%, +2.2%] | +1.5% [-0.9%, +5.3%] |
| std | 5 | 3983 | std/Actions/Producers.dfy (77% of VCs) | +0.4% [-1.4%, +4.8%] | -0.3% [-4.2%, +0.0%] | -2.5% [-4.2%, -0.8%] |

14 affected VCs fail (a verification error) in some run; their cost is the solver's search for a counterexample, reported separately:

| job | VC | master mean (min..max) | PR mean (min..max) |
|---|---|---|---|
| std/Actions/Producers.dfy | Std.Producers.ConcatenatedProducer.Invoke (correctness) (assertion batch 277) | 67.09M (10.07..100.19) | 68.95M (12.30..100.19) |
| std/Actions/Producers.dfy | Std.Producers.ConcatenatedProducer.Invoke (correctness) (assertion batch 275) | 32.52M (4.62..100.19) | 36.51M (4.30..100.19) |
| std/Actions/Producers.dfy | Std.Producers.ConcatenatedProducer.Invoke (correctness) (assertion batch 273) | 29.24M (1.53..100.19) | 15.86M (1.81..100.19) |
| lit/dafny1/SchorrWaite-stages.dfy:refresh | M0.SchorrWaite (correctness) (assertion batch 40) | 20.36M (0.47..106.14) | 13.96M (2.22..75.77) |
| std/Base64.dfy | Std.Base64.EncodeBVIsBase64 (correctness) (assertion batch 7) | 18.06M (1.97..50.06) | 28.49M (0.35..50.06) |
| std/Base64.dfy | Std.Base64.EncodeBVLengthCongruentToZeroMod4 (correctness) (assertion batch 5) | 15.58M (1.24..50.05) | 17.34M (0.60..50.05) |
| std/Arithmetic/DivMod.dfy | Std.Arithmetic.DivMod.LemmaFundamentalDivModConverse (correctness) | 11.81M (10.35..14.61) | 41.62M (8.75..249.84) |
| lit/dafny1/SchorrWaite-stages.dfy:refresh | M0.SchorrWaite (correctness) (assertion batch 44) | 10.39M (0.95..84.47) | 1.08M (0.59..1.39) |
| std/Actions/Producers.dfy | Std.Producers.FilteredProducer.Invoke (correctness) | 10.34M (7.38..15.94) | 9.21M (7.03..10.89) |
| std/Actions/Producers.dfy | Std.Producers.MappedProducer.Invoke (correctness) | 8.55M (7.66..10.22) | 7.82M (6.24..9.71) |

## Total proof RU per seed (affected VCs that pass everywhere)

| prelude | seed 0 | seed 1 | seed 2 | seed 3 | seed 4 | seed 5 | seed 6 | seed 7 | seed 8 | mean | sd |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| master | 982.6M | 1065.6M | 1016.3M | 1040.6M | 1054.6M | 891.7M | 1006.0M | 1012.1M | 1063.6M | 1014.8M | 51.1M |
| pr | 936.6M | 1343.8M | 998.5M | 931.0M | 1089.4M | 1097.3M | 971.2M | 977.1M | 1047.3M | 1043.6M | 120.6M |

## Solver time over those proofs (sum of per-VC means, seconds)

| group | master | PR |
|---|---:|---:|
| all | 733.9 | 754.0 |
| lit | 153.9 | 172.1 |
| std | 580.1 | 581.9 |

## Distribution of per-VC cost ratios over those proofs (mean over seeds)

| ratio bucket | PR/master |
|---|---:|
| < 0.5x | 1 |
| 0.5-0.8x | 12 |
| 0.8-0.95x | 179 |
| 0.95-1.05x | 4212 |
| 1.05-1.25x | 47 |
| 1.25-2x | 7 |
| 2-4x | 2 |
| >= 4x | 1 |

## Verdict changes at each job's limit (seeds passing out of 9)

| job | VC | limit | master ok | PR ok | master RU | PR RU |
|---|---|---:|---:|---:|---:|---:|
| lit/dafny1/ExtensibleArrayAuto.dfy:refresh | ExtensibleArray.Set (correctness) | 50M | 7 | 9 | 20.80M | 11.23M |
| lit/dafny1/SchorrWaite-stages.dfy:refresh | M0.SchorrWaite (correctness) (assertion batch 44) | 50M | 8 | 9 | 10.39M | 1.08M |
| lit/dafny2/SmallestMissingNumber-functional.dfy:refresh | SMN''_Correct (correctness) | 50M | 9 | 8 | 8.31M | 26.11M |
| lit/dafny2/SmallestMissingNumber-functional.dfy:refresh | SMN_Correct (correctness) | 50M | 8 | 7 | 20.82M | 30.87M |
| std/Actions/Producers.dfy | Std.Producers.ConcatenatedProducer.Invoke (correctness) (assertion batch 273) | 100M | 7 | 8 | 29.24M | 15.86M |
| std/Actions/Producers.dfy | Std.Producers.ConcatenatedProducer.Invoke (correctness) (assertion batch 275) | 100M | 7 | 8 | 32.52M | 36.51M |
| std/Actions/Producers.dfy | Std.Producers.FilteredProducer.Invoke (correctness) | 50M | 9 | 8 | 10.34M | 9.21M |
| std/Actions/Producers.dfy | Std.Producers.MappedProducer.Invoke (correctness) | 10M | 8 | 9 | 8.55M | 7.82M |
| std/Arithmetic/DivMod.dfy | Std.Arithmetic.DivMod.LemmaFundamentalDivModConverse (correctness) | 50M | 9 | 6 | 11.81M | 41.62M |
| std/Base64.dfy | Std.Base64.DecodeRecursivelyBounds (correctness) | 5M | 9 | 8 | 0.13M | 3.78M |
| std/Base64.dfy | Std.Base64.DecodeValidEncode1Padding (correctness) (assertion batch 56) | 12M | 6 | 5 | 5.58M | 6.83M |
| std/Base64.dfy | Std.Base64.DecodeValidEncode2Padding (correctness) | 5M | 6 | 8 | 3.53M | 2.13M |
| std/Base64.dfy | Std.Base64.EncodeBVIsBase64 (correctness) (assertion batch 7) | 50M | 6 | 4 | 18.06M | 28.49M |
| std/Base64.dfy | Std.Base64.EncodeBVLengthCongruentToZeroMod4 (correctness) (assertion batch 5) | 50M | 7 | 8 | 15.58M | 17.34M |

## Largest changes among those proofs (by |PR - master| mean RU)

| job | VC | master | PR | PR/master | min..max master | min..max PR |
|---|---|---:|---:|---:|---|---|
| lit/dafny2/SmallestMissingNumber-functional.dfy:refresh | SMN''_Correct (correctness) | 8.31M | 26.11M | 3.14 | 4.48..28.21M | 4.30..160.24M |
| lit/dafny2/SmallestMissingNumber-functional.dfy:refresh | SMN'_Correct (correctness) | 79.15M | 89.51M | 1.13 | 21.52..122.19M | 26.73..174.55M |
| lit/dafny2/SmallestMissingNumber-functional.dfy:refresh | SMN_Correct (correctness) | 20.82M | 30.87M | 1.48 | 3.58..50.05M | 13.45..68.41M |
| lit/dafny1/ExtensibleArrayAuto.dfy:refresh | ExtensibleArray.Set (correctness) | 20.80M | 11.23M | 0.54 | 2.11..84.48M | 2.23..32.01M |
| std/Base64.dfy | Std.Base64.DecodeValidUnpaddedPartialFrom1PaddedSeq (well-formedness) | 2.24M | 8.85M | 3.94 | 0.46..7.28M | 0.32..66.54M |
| std/Actions/Producers.dfy | Std.Producers.ConcatenatedProducer.Invoke (correctness) (assertion batch 276) | 5.02M | 9.45M | 1.88 | 2.15..10.20M | 2.45..47.09M |
| std/Base64.dfy | Std.Base64.UInt8sToBVsToUInt8s (correctness) (assertion batch 3) | 33.90M | 29.64M | 0.87 | 0.41..80.57M | 0.41..80.57M |
| std/Base64.dfy | Std.Base64.DecodeRecursivelyBounds (correctness) | 0.13M | 3.78M | 29.28 | 0.10..0.17M | 0.10..32.99M |
| lit/dafny1/SchorrWaite-stages.dfy:refresh | M2.SchorrWaite (correctness) (assertion batch 35) | 2.83M | 1.16M | 0.41 | 0.94..14.48M | 0.64..1.91M |
| std/Base64.dfy | Std.Base64.DecodeValidEncode2Padding (correctness) | 3.53M | 2.13M | 0.60 | 0.70..8.17M | 0.64..10.92M |
| std/Base64.dfy | Std.Base64.EncodeBVIsBase64 (correctness) (assertion batch 5) | 5.41M | 4.11M | 0.76 | 0.12..32.85M | 0.15..15.34M |
| std/Actions/Producers.dfy | Std.Producers.ConcatenatedProducer.Invoke (correctness) (assertion batch 283) | 24.08M | 25.35M | 1.05 | 6.80..66.34M | 6.63..74.35M |
| lit/dafny4/NumberRepresentations.dfy:refresh | inc (correctness) | 4.39M | 3.26M | 0.74 | 0.13..11.29M | 0.13..5.72M |
| std/Actions/Producers.dfy | Std.Producers.ConcatenatedProducer.Invoke (correctness) (assertion batch 272) | 2.93M | 1.89M | 0.64 | 1.76..8.34M | 0.78..2.64M |
| std/Base64.dfy | Std.Base64.DecodeEncodeRecursively (correctness) (assertion batch 24) | 1.68M | 2.71M | 1.61 | 0.10..6.78M | 0.08..13.28M |
| std/Actions/Producers.dfy | Std.Producers.ConcatenatedProducer.Invoke (correctness) (assertion batch 353) | 6.61M | 5.96M | 0.90 | 5.01..9.43M | 4.39..7.15M |
| lit/dafny1/SchorrWaite-stages.dfy:refresh | M0.SchorrWaite (correctness) (assertion batch 42) | 1.12M | 1.77M | 1.58 | 0.87..2.20M | 0.93..5.01M |
| std/Actions/Producers.dfy | Std.Producers.ConcatenatedProducer.Invoke (correctness) (assertion batch 214) | 4.39M | 3.76M | 0.86 | 2.61..6.00M | 2.60..5.19M |
| lit/dafny1/ExtensibleArrayAuto.dfy:refresh | Main (correctness) | 1.64M | 1.04M | 0.63 | 0.85..2.88M | 0.81..1.38M |
| std/Actions/Producers.dfy | Std.Producers.MappedProducerOfNewProducers.Invoke (correctness) | 10.00M | 9.44M | 0.94 | 8.71..11.46M | 7.79..11.16M |
| std/Actions/Producers.dfy | Std.Producers.ConcatenatedProducer.Invoke (correctness) (assertion batch 352) | 6.70M | 6.15M | 0.92 | 5.14..9.19M | 4.51..7.64M |
| std/Actions/Producers.dfy | Std.Producers.ConcatenatedProducer.Invoke (correctness) (assertion batch 354) | 6.24M | 5.71M | 0.91 | 4.51..8.34M | 4.16..7.12M |
| std/Base64.dfy | Std.Base64.Encode1PaddingIs1Padding (correctness) | 5.19M | 5.63M | 1.08 | 1.53..17.67M | 1.69..22.87M |
| std/Actions/Producers.dfy | Std.Producers.ConcatenatedProducer.Invoke (correctness) (assertion batch 360) | 2.32M | 1.92M | 0.83 | 1.76..2.82M | 1.63..2.08M |
| std/Actions/Producers.dfy | Std.Producers.ConcatenatedProducer.Invoke (correctness) (assertion batch 351) | 6.27M | 5.88M | 0.94 | 4.53..8.19M | 4.84..7.53M |

## Per job (proofs among the affected VCs)

| job | VCs | master | PR | PR vs master |
|---|---:|---:|---:|---:|
| std/Actions/Producers.dfy | 3053 | 699.77M | 698.81M | -0.1% |
| lit/dafny2/SmallestMissingNumber-functional.dfy:refresh | 19 | 108.76M | 146.97M | +35.1% |
| std/Base64.dfy | 584 | 90.71M | 95.11M | +4.9% |
| lit/dafny1/ExtensibleArrayAuto.dfy:refresh | 77 | 63.92M | 53.48M | -16.3% |
| lit/dafny1/SchorrWaite-stages.dfy:refresh | 245 | 21.36M | 20.32M | -4.9% |
| lit/dafny4/NumberRepresentations.dfy:refresh | 62 | 13.38M | 12.26M | -8.3% |
| std/Arithmetic/DivMod.dfy | 283 | 10.07M | 9.95M | -1.2% |
| lit/vstte2012/Tree.dfy:refresh | 75 | 5.55M | 5.42M | -2.3% |
| std/Arithmetic/Mul.dfy | 54 | 0.83M | 0.79M | -4.0% |
| std/Arithmetic/Power2.dfy | 9 | 0.44M | 0.44M | +0.2% |

## Stability over the affected VCs (all but synth)

Flaky: some seeds pass at the job's limit and others do not. Spread: the coefficient of variation of a VC's cost across seeds, for VCs above 1M RU under master.

| prelude | flaky VCs | flaky, not under master | no longer flaky | median spread | 90th-percentile spread |
|---|---:|---:|---:|---:|---:|
| master | 15 | 0 | 0 | 0.22 | 1.19 |
| pr | 16 | 4 | 3 | 0.22 | 1.43 |

Flaky under the PR but not under master (seeds passing out of the run):

| job | VC | master | PR | PR mean RU |
|---|---|---:|---:|---:|
| std/Arithmetic/DivMod.dfy | Std.Arithmetic.DivMod.LemmaFundamentalDivModConverse (correctness) | 9 | 6 | 41.62M |
| lit/dafny2/SmallestMissingNumber-functional.dfy:refresh | SMN''_Correct (correctness) | 9 | 8 | 26.11M |
| std/Actions/Producers.dfy | Std.Producers.FilteredProducer.Invoke (correctness) | 9 | 8 | 9.21M |
| std/Base64.dfy | Std.Base64.DecodeRecursivelyBounds (correctness) | 9 | 8 | 3.78M |

## Comparisons over the affected proofs (all but synth)

| comparison | programs | VCs | total | geomean over VCs | per program | verdict flips at limit |
|---|---:|---:|---|---|---|---:|
| pr vs master | 10 | 4461 | +2.8% [-9.0%, +23.6%] | -0.3% [-2.3%, +0.2%] | -0.5% [-2.4%, +2.0%] | 5 |
