# #series A/B benchmark (public corpora, seeds 1-4)

Seeds per (VC, prelude): 4 (1, 2, 3, 4; 0 is Dafny's default). VCs: 4264 in 20 jobs; **4264 affected** (master and PR counts differ), 0 unaffected (identical counts under master and PR for every seed).

## Proof cost over affected VCs that pass everywhere

Totals are sums of per-VC means over seeds. "Per program" averages each program's own VC geomean, so a
program with hundreds of VCs weighs no more than one with two. Brackets are 95% bootstrap intervals that
resample programs, not VCs.

| group | programs | VCs | largest program | total PR/master | geomean over VCs | per program |
|---|---:|---:|---|---|---|---|
| all but synth | 19 | 4215 | std/Actions/Producers.dfy (48% of VCs) | +4.9% [-11.9%, +29.1%] | -0.8% [-2.6%, -0.1%] | -2.3% [-4.7%, +0.1%] |
| kondo | 5 | 489 | kondo/flexPaxos/sync (30% of VCs) | +14.4% [-83.8%, +45.3%] | -0.9% [-3.3%, +0.5%] | -1.3% [-3.3%, +0.3%] |
| libraries | 4 | 383 | libraries/NonlinearArithmetic/DivMod.dfy (66% of VCs) | +9.0% [-16.5%, +21.3%] | -3.9% [-4.8%, -1.7%] | -3.8% [-5.2%, -2.1%] |
| lit | 7 | 545 | lit/concurrency/12-MutexLifetime-short.dfy (71% of VCs) | -6.0% [-47.4%, +33.0%] | +0.0% [-4.0%, +2.4%] | -2.6% [-8.3%, +3.6%] |
| std | 3 | 2798 | std/Actions/Producers.dfy (72% of VCs) | +7.6% [-18.3%, +65.3%] | -0.5% [-4.2%, +0.1%] | -1.4% [-4.2%, +0.1%] |

49 affected VCs fail (a verification error) in some run; their cost is the solver's search for a counterexample, reported separately:

| job | VC | master mean (min..max) | PR mean (min..max) |
|---|---|---|---|
| lit/dafny2/SnapshotableTrees.dfy:refresh | SnapTree.Node.MutatingInsert_Right (correctness) | 500.04M (500.04..500.04) | 500.04M (500.04..500.04) |
| lit/dafny2/SnapshotableTrees.dfy:refresh | SnapTree.Node.FunctionalInsert_Right (correctness) | 500.04M (500.04..500.04) | 500.04M (500.04..500.04) |
| lit/dafny2/SnapshotableTrees.dfy:refresh | SnapTree.Node.FunctionalInsert_Left (correctness) | 463.52M (358.29..500.04) | 463.20M (352.68..500.04) |
| lit/dafny2/SnapshotableTrees.dfy:refresh | SnapTree.Node.MutatingInsert_Left (correctness) | 331.76M (130.23..500.04) | 500.04M (500.04..500.04) |
| libraries/dafny/Collections/Seqs.dfy | Dafny.Collections.Seq.LemmaMapDistributesOverConcat (correctness) | 296.29M (141.61..500.02) | 254.20M (2.33..441.63) |
| lit/dafny1/ExtensibleArrayAuto.dfy:refresh | ExtensibleArray.Append (correctness) | 267.35M (19.20..500.05) | 385.55M (42.06..500.05) |
| lit/dafny2/SnapshotableTrees.dfy:refresh | SnapTree.Iterator.Push (correctness) (assertion batch 2) | 243.21M (0.18..500.04) | 0.27M (0.15..0.54) |
| lit/dafny2/SnapshotableTrees.dfy:refresh | SnapTree.Iterator.Push (correctness) (assertion batch 13) | 179.42M (1.06..500.03) | 8.83M (0.74..29.85) |
| kondo/paxos/sync | PaxosProof.InvNextChosenImpliesProposingLeaderHearsChosenBallotP2bStep (correctness) | 139.68M (22.37..384.12) | 36.29M (15.78..87.84) |
| kondo/flexPaxos/sync | PaxosProof.InvNextLeaderReceivedPromisesImpliesAcceptorState (correctness) | 121.78M (34.72..210.72) | 142.05M (68.79..334.15) |

## Total proof RU per seed (affected VCs that pass everywhere)

| prelude | seed 1 | seed 2 | seed 3 | seed 4 | mean | sd |
|---|---:|---:|---:|---:|---:|---:|
| master | 2189.0M | 2015.2M | 2025.9M | 1715.2M | 1986.3M | 171.0M |
| pr | 2187.7M | 2274.6M | 1854.4M | 2019.2M | 2084.0M | 161.2M |

## Solver time over those proofs (sum of per-VC means, seconds)

| group | master | PR |
|---|---:|---:|
| all | 1280.7 | 1326.6 |
| lit | 526.8 | 501.3 |
| std | 335.2 | 324.8 |

## Distribution of per-VC cost ratios over those proofs (mean over seeds)

| ratio bucket | PR/master |
|---|---:|
| < 0.5x | 5 |
| 0.5-0.8x | 30 |
| 0.8-0.95x | 302 |
| 0.95-1.05x | 3746 |
| 1.05-1.25x | 93 |
| 1.25-2x | 30 |
| 2-4x | 6 |
| >= 4x | 3 |

## Verdict changes at each job's limit (seeds passing out of 4)

| job | VC | limit | master ok | PR ok | master RU | PR RU |
|---|---|---:|---:|---:|---:|---:|
| kondo/flexPaxos/sync | PaxosProof.InvNextLeaderReceivedPromisesImpliesAcceptorState (correctness) | 50M | 1 | 0 | 121.78M | 142.05M |
| kondo/flexPaxos/sync | PaxosProof.InvNextLearnerReceivedAcceptImpliesAccepted (correctness) | 50M | 3 | 2 | 78.02M | 99.40M |
| kondo/paxos/sync | PaxosProof.InvNextAcceptorValidBundle (correctness) | 50M | 4 | 1 | 33.23M | 106.46M |
| kondo/paxos/sync | PaxosProof.InvNextChosenImpliesProposingLeaderHearsChosenBallotP2bStep (correctness) | 50M | 1 | 3 | 139.68M | 36.29M |
| kondo/paxos/sync | PaxosProof.InvNextLeaderReceivedPromisesImpliesAcceptorState (correctness) | 50M | 1 | 2 | 168.49M | 112.62M |
| kondo/paxos/sync | PaxosProof.InvNextLearnerReceivedAcceptImpliesAccepted (correctness) | 50M | 3 | 2 | 94.59M | 46.20M |
| kondo/shardedKv/sync | ShardedKVProof.InvNextSafety (correctness) | 50M | 0 | 1 | 4.36M | 3.71M |
| kondo/simplifiedLeaderElection/sync | ToyLeaderElectionProof.InvNextHasVoteImpliesVoterNominates (correctness) | 50M | 4 | 2 | 13.95M | 133.58M |
| kondo/simplifiedLeaderElection/sync | ToyLeaderElectionProof.InvNextIsLeaderImpliesHasQuorum (correctness) | 50M | 4 | 3 | 1.64M | 1.52M |
| kondo/twoPhaseCommit/sync | TwoPCInvariantProof.InvNextLeaderTallyReflectsPreferences (correctness) | 50M | 2 | 4 | 58.07M | 1.45M |
| libraries/Collections/Sequences/LittleEndianNatConversions.dfy | LittleEndianNatConversions.LemmaSmallLargeSmall (correctness) | 40M | 4 | 3 | 17.40M | 44.35M |
| libraries/dafny/Collections/LittleEndianNatConversions.dfy | Dafny.Collections.LittleEndianNatConversions.LemmaSmallLargeSmall (correctness) | 40M | 3 | 1 | 30.09M | 128.37M |
| libraries/dafny/Collections/Seqs.dfy | Dafny.Collections.Seq.LemmaFilterDistributesOverConcat (correctness) (assertion batch 2) | 40M | 3 | 0 | 50.71M | 90.11M |
| libraries/dafny/Collections/Seqs.dfy | Dafny.Collections.Seq.LemmaMapDistributesOverConcat (correctness) | 40M | 0 | 1 | 296.29M | 254.20M |
| lit/concurrency/12-MutexLifetime-short.dfy:refresh | MutexGuardU32._ctor (correctness) (assertion batch 132) | 50M | 0 | 3 | 106.62M | 54.31M |
| lit/concurrency/12-MutexLifetime-short.dfy:refresh | MutexGuardU32._ctor (correctness) (assertion batch 96) | 50M | 3 | 4 | 46.78M | 39.97M |
| lit/dafny0/FunctionSpecifications.dfy:refresh | GoodPost (well-formedness) | 50M | 3 | 2 | 77.80M | 156.01M |
| lit/dafny1/ExtensibleArrayAuto.dfy:refresh | ExtensibleArray.Set (correctness) | 50M | 3 | 4 | 24.37M | 13.68M |
| lit/dafny2/SmallestMissingNumber-functional.dfy:refresh | SMN''_Correct (correctness) | 50M | 4 | 3 | 11.52M | 47.79M |
| lit/dafny2/SmallestMissingNumber-functional.dfy:refresh | SMN'_Correct (correctness) | 50M | 0 | 1 | 93.96M | 82.56M |
| lit/dafny2/SmallestMissingNumber-functional.dfy:refresh | SMN_Correct (correctness) | 50M | 4 | 2 | 14.78M | 40.44M |
| lit/dafny2/SnapshotableTrees.dfy:refresh | SnapTree.Iterator.Push (correctness) (assertion batch 13) | 50M | 1 | 4 | 179.42M | 8.83M |
| lit/dafny2/SnapshotableTrees.dfy:refresh | SnapTree.Iterator.Push (correctness) (assertion batch 2) | 50M | 2 | 4 | 243.21M | 0.27M |
| lit/dafny2/SnapshotableTrees.dfy:refresh | SnapTreeTestHarness.Main (correctness) | 50M | 2 | 3 | 4.99M | 5.31M |
| lit/dafny4/Lucas-down.dfy:refresh | Lucas_Binary'' (correctness) | 50M | 3 | 4 | 20.71M | 7.28M |
| lit/git-issues/git-issue-6535.dfy:refresh | Bad (correctness) | 50M | 4 | 0 | 0.03M | 0.03M |
| lit/vstte2012/RingBufferAuto.dfy:refresh | RingBuffer.Clear (correctness) | 50M | 2 | 1 | 4.59M | 8.17M |
| std/Actions/Producers.dfy | Std.Producers.ConcatenatedProducer.Invoke (correctness) (assertion batch 283) | 100M | 4 | 3 | 30.22M | 51.18M |
| std/Actions/Producers.dfy | Std.Producers.MappedProducer.Invoke (correctness) | 10M | 3 | 4 | 9.05M | 7.34M |
| std/Arithmetic/DivMod.dfy | Std.Arithmetic.DivMod.LemmaFundamentalDivModConverse (correctness) | 50M | 3 | 4 | 16.98M | 12.10M |
| std/Arithmetic/DivMod.dfy | Std.Arithmetic.DivMod.LemmaMultiplyDivideLt (correctness) | 50M | 2 | 3 | 1.20M | 0.96M |
| std/Base64.dfy | Std.Base64.DecodeValidEncode2Padding (correctness) | 5M | 2 | 3 | 4.11M | 3.28M |
| std/Base64.dfy | Std.Base64.DecodeValidUnpaddedPartialFrom1PaddedSeq (well-formedness) | 5M | 4 | 3 | 1.51M | 17.68M |
| std/Base64.dfy | Std.Base64.EncodeBVIsBase64 (correctness) | 5M | 1 | 0 | 14.24M | 70.61M |
| std/Base64.dfy | Std.Base64.EncodeBVLengthCongruentToZeroMod4 (correctness) (assertion batch 5) | 50M | 4 | 3 | 5.96M | 25.88M |

## Largest changes among those proofs (by |PR - master| mean RU)

| job | VC | master | PR | PR/master | min..max master | min..max PR |
|---|---|---:|---:|---:|---|---|
| kondo/flexPaxos/sync | PaxosProof.InvNextAcceptorValidBundle (correctness) | 61.44M | 163.40M | 2.66 | 18.25..123.73M | 31.31..340.52M |
| kondo/paxos/sync | PaxosProof.InvNextAcceptorValidBundle (correctness) | 33.23M | 106.46M | 3.20 | 14.76..46.14M | 32.48..211.67M |
| kondo/twoPhaseCommit/sync | TwoPCInvariantProof.InvNextLeaderTallyReflectsPreferences (correctness) | 58.07M | 1.45M | 0.02 | 0.67..131.29M | 0.83..3.05M |
| std/Base64.dfy | Std.Base64.EncodeBVIsBase64 (correctness) | 14.24M | 70.61M | 4.96 | 1.80..21.06M | 12.61..163.85M |
| kondo/paxos/sync | PaxosProof.InvNextLeaderReceivedPromisesImpliesAcceptorState (correctness) | 168.49M | 112.62M | 0.67 | 27.40..386.84M | 41.30..214.09M |
| lit/concurrency/12-MutexLifetime-short.dfy:refresh | MutexGuardU32._ctor (correctness) (assertion batch 132) | 106.62M | 54.31M | 0.51 | 59.24..164.93M | 46.08..71.70M |
| lit/dafny2/SmallestMissingNumber-functional.dfy:refresh | SMN''_Correct (correctness) | 11.52M | 47.79M | 4.15 | 4.62..28.21M | 5.09..160.24M |
| lit/dafny2/SmallestMissingNumber-functional.dfy:refresh | SMN_Correct (correctness) | 14.78M | 40.44M | 2.74 | 3.58..20.44M | 13.45..68.41M |
| kondo/flexPaxos/sync | PaxosProof.InvNextLearnerReceivedAcceptImpliesAccepted (correctness) | 78.02M | 99.40M | 1.27 | 19.87..213.78M | 34.38..203.62M |
| std/Base64.dfy | Std.Base64.DecodeValidUnpaddedPartialFrom1PaddedSeq (well-formedness) | 1.51M | 17.68M | 11.74 | 0.46..3.04M | 1.05..66.54M |
| kondo/paxos/sync | PaxosProof.InvNextChosenImpliesProposingLeaderHearsChosenBallotP1bStep (correctness) | 26.47M | 41.62M | 1.57 | 21.92..33.78M | 31.56..49.66M |
| kondo/paxos/sync | PaxosProof.InvNextLeaderHearedImpliesProposed (correctness) | 25.20M | 11.31M | 0.45 | 15.53..34.47M | 6.34..20.49M |
| lit/dafny4/Lucas-down.dfy:refresh | Lucas_Binary'' (correctness) | 20.71M | 7.28M | 0.35 | 3.60..61.38M | 1.91..19.71M |
| std/Base64.dfy | Std.Base64.UInt8sToBVsToUInt8s (correctness) (assertion batch 3) | 35.68M | 22.29M | 0.62 | 0.41..73.49M | 0.41..68.12M |
| kondo/flexPaxos/sync | PaxosProof.InvNextChosenImpliesProposingLeaderHearsChosenBallotP1bStep (correctness) | 33.74M | 20.85M | 0.62 | 18.11..45.42M | 9.95..35.53M |
| lit/dafny2/SmallestMissingNumber-functional.dfy:refresh | SMN'_Correct (correctness) | 93.96M | 82.56M | 0.88 | 62.21..122.19M | 26.73..136.94M |
| lit/dafny1/ExtensibleArrayAuto.dfy:refresh | ExtensibleArray.Set (correctness) | 24.37M | 13.68M | 0.56 | 2.49..84.48M | 2.54..32.01M |
| kondo/flexPaxos/sync | PaxosProof.InvNextChosenImpliesProposingLeaderHearsChosenBallotP2bStep (correctness) | 29.92M | 38.13M | 1.27 | 3.70..83.53M | 4.98..83.60M |
| kondo/flexPaxos/sync | PaxosProof.InvNextLeaderHighestHeardToPromisedRangeHasNoAccepts (correctness) | 10.99M | 18.00M | 1.64 | 8.56..15.44M | 10.74..31.55M |
| kondo/paxos/sync | PaxosProof.InvNextChosenImpliesProposingLeaderHearsChosenBallot (correctness) | 14.39M | 21.26M | 1.48 | 6.25..26.43M | 4.90..44.63M |
| lit/concurrency/12-MutexLifetime-short.dfy:refresh | MutexGuardU32._ctor (correctness) (assertion batch 96) | 46.78M | 39.97M | 0.85 | 38.80..58.15M | 31.38..49.13M |
| libraries/NonlinearArithmetic/DivMod.dfy | DivMod.LemmaFundamentalDivModConverse (correctness) | 5.27M | 11.90M | 2.26 | 4.97..5.82M | 4.64..32.64M |
| lit/dafny2/SnapshotableTrees.dfy:refresh | SnapTree.Tree.Insert (correctness) | 6.14M | 0.62M | 0.10 | 2.95..14.23M | 0.57..0.74M |
| std/Actions/Producers.dfy | Std.Producers.FlattenedProducer.Invoke (correctness) | 36.31M | 30.82M | 0.85 | 21.40..64.47M | 20.72..40.54M |
| kondo/paxos/sync | PaxosProof.InvNextLeaderHighestHeardToPromisedRangeHasNoAccepts (correctness) | 13.76M | 19.19M | 1.39 | 7.30..28.00M | 16.65..26.29M |

## Per job (proofs among the affected VCs)

| job | VCs | master | PR | PR vs master |
|---|---:|---:|---:|---:|
| lit/concurrency/12-MutexLifetime-short.dfy:refresh | 386 | 533.50M | 467.93M | -12.3% |
| std/Actions/Producers.dfy | 2024 | 468.90M | 453.60M | -3.3% |
| kondo/paxos/sync | 145 | 318.37M | 347.85M | +9.3% |
| kondo/flexPaxos/sync | 146 | 265.06M | 388.96M | +46.7% |
| lit/dafny2/SmallestMissingNumber-functional.dfy:refresh | 19 | 120.74M | 171.26M | +41.8% |
| std/Base64.dfy | 480 | 94.72M | 156.55M | +65.3% |
| kondo/twoPhaseCommit/sync | 90 | 63.86M | 6.99M | -89.1% |
| lit/dafny1/ExtensibleArrayAuto.dfy:refresh | 8 | 27.11M | 15.83M | -41.6% |
| lit/dafny4/Lucas-down.dfy:refresh | 12 | 20.97M | 7.55M | -64.0% |
| libraries/NonlinearArithmetic/DivMod.dfy | 254 | 20.48M | 24.97M | +21.9% |
| lit/dafny2/SnapshotableTrees.dfy:refresh | 99 | 15.47M | 11.41M | -26.3% |
| std/Arithmetic/DivMod.dfy | 294 | 13.97M | 11.41M | -18.3% |
| libraries/dafny/Collections/Seqs.dfy | 77 | 9.15M | 7.56M | -17.4% |
| kondo/simplifiedLeaderElection/sync | 59 | 7.60M | 5.37M | -29.3% |
| lit/vstte2012/RingBufferAuto.dfy:refresh | 11 | 2.16M | 2.49M | +15.1% |
| libraries/dafny/Collections/LittleEndianNatConversions.dfy | 26 | 1.76M | 1.72M | -2.3% |
| kondo/shardedKv/sync | 49 | 1.51M | 1.51M | -0.1% |
| libraries/Collections/Sequences/LittleEndianNatConversions.dfy | 26 | 0.90M | 0.96M | +7.4% |
| lit/dafny0/FunctionSpecifications.dfy:refresh | 10 | 0.07M | 0.07M | -7.8% |

## Stability over the affected VCs (all but synth)

Flaky: some seeds pass at the job's limit and others do not. Spread: the coefficient of variation of a VC's cost across seeds, for VCs above 1M RU under master.

| prelude | flaky VCs | flaky, not under master | no longer flaky | median spread | 90th-percentile spread |
|---|---:|---:|---:|---:|---:|
| master | 32 | 0 | 0 | 0.26 | 0.94 |
| master2 | 32 | 0 | 0 | 0.26 | 0.94 |
| pr | 34 | 13 | 11 | 0.21 | 0.86 |

Flaky under the PR but not under master (seeds passing out of the run):

| job | VC | master | PR | PR mean RU |
|---|---|---:|---:|---:|
| libraries/dafny/Collections/Seqs.dfy | Dafny.Collections.Seq.LemmaMapDistributesOverConcat (correctness) | 0 | 1 | 254.20M |
| kondo/simplifiedLeaderElection/sync | ToyLeaderElectionProof.InvNextHasVoteImpliesVoterNominates (correctness) | 4 | 2 | 133.58M |
| kondo/paxos/sync | PaxosProof.InvNextAcceptorValidBundle (correctness) | 4 | 1 | 106.46M |
| lit/dafny2/SmallestMissingNumber-functional.dfy:refresh | SMN'_Correct (correctness) | 0 | 1 | 82.56M |
| lit/concurrency/12-MutexLifetime-short.dfy:refresh | MutexGuardU32._ctor (correctness) (assertion batch 132) | 0 | 3 | 54.31M |
| std/Actions/Producers.dfy | Std.Producers.ConcatenatedProducer.Invoke (correctness) (assertion batch 283) | 4 | 3 | 51.18M |
| lit/dafny2/SmallestMissingNumber-functional.dfy:refresh | SMN''_Correct (correctness) | 4 | 3 | 47.79M |
| libraries/Collections/Sequences/LittleEndianNatConversions.dfy | LittleEndianNatConversions.LemmaSmallLargeSmall (correctness) | 4 | 3 | 44.35M |
| lit/dafny2/SmallestMissingNumber-functional.dfy:refresh | SMN_Correct (correctness) | 4 | 2 | 40.44M |
| std/Base64.dfy | Std.Base64.EncodeBVLengthCongruentToZeroMod4 (correctness) (assertion batch 5) | 4 | 3 | 25.88M |
| std/Base64.dfy | Std.Base64.DecodeValidUnpaddedPartialFrom1PaddedSeq (well-formedness) | 4 | 3 | 17.68M |
| kondo/shardedKv/sync | ShardedKVProof.InvNextSafety (correctness) | 0 | 1 | 3.71M |
| kondo/simplifiedLeaderElection/sync | ToyLeaderElectionProof.InvNextIsLeaderImpliesHasQuorum (correctness) | 4 | 3 | 1.52M |

## Comparisons over the affected proofs (all but synth)

| comparison | programs | VCs | total | geomean over VCs | per program | verdict flips at limit |
|---|---:|---:|---|---|---|---:|
| A/A: master2 vs master (same input, another process) | 19 | 4215 | +0.0% [-0.0%, +0.0%] | +0.0% [-0.0%, +0.0%] | +0.0% [-0.0%, +0.0%] | 0 |
| pr vs master | 19 | 4215 | +4.9% [-11.9%, +28.6%] | -0.8% [-2.7%, -0.1%] | -2.3% [-4.6%, +0.2%] | 14 |

## Comparisons over the external programs' affected proofs

| comparison | programs | VCs | total | geomean over VCs | per program | verdict flips at limit |
|---|---:|---:|---|---|---|---:|
| A/A: master2 vs master (same input, another process) | 9 | 872 | +0.0% [+0.0%, +0.0%] | +0.0% [+0.0%, +0.0%] | +0.0% [+0.0%, +0.0%] | 0 |
| pr vs master | 9 | 872 | +14.1% [-66.2%, +43.4%] | -2.2% [-4.0%, -0.3%] | -2.4% [-3.9%, -1.0%] | 4 |

## Alternative sound encodings, over the same proofs

restrict: elements defined everywhere, `$ArbitraryBoxValue` outside the domain. domguard: the PR's axiom guarded by `Map#Domain(Map#Glue(a, b, t))`. eager: the PR's axiom plus the trigger `{ Map#Glue(a, b, t), Set#IsMember(a, bx) }`.

| encoding | programs | VCs | total vs master | geomean over VCs vs master | per program vs master | per program vs PR | verdict flips vs master at limit |
|---|---:|---:|---|---|---|---|---:|
| pr | 19 | 4215 | +4.9% [-12.3%, +29.0%] | -0.8% [-2.6%, -0.1%] | -2.3% [-4.7%, +0.0%] |  | 35 |
| master2 | 19 | 4215 | +0.0% [-0.0%, +0.0%] | +0.0% [-0.0%, +0.0%] | +0.0% [-0.0%, +0.0%] | +2.4% [-0.1%, +4.8%] | 0 |

master2: largest differences from the PR

| job | VC | master | PR | master2 |
|---|---|---:|---:|---:|
| kondo/flexPaxos/sync | PaxosProof.InvNextAcceptorValidBundle (correctness) | 61.44M | 163.40M | 61.44M |
| kondo/paxos/sync | PaxosProof.InvNextAcceptorValidBundle (correctness) | 33.23M | 106.46M | 33.23M |
| kondo/twoPhaseCommit/sync | TwoPCInvariantProof.InvNextLeaderTallyReflectsPreferences (correctness) | 58.07M | 1.45M | 58.07M |
| std/Base64.dfy | Std.Base64.EncodeBVIsBase64 (correctness) | 14.24M | 70.61M | 14.24M |
| kondo/paxos/sync | PaxosProof.InvNextLeaderReceivedPromisesImpliesAcceptorState (correctness) | 168.49M | 112.62M | 168.49M |
| lit/concurrency/12-MutexLifetime-short.dfy:refresh | MutexGuardU32._ctor (correctness) (assertion batch 132) | 106.62M | 54.31M | 106.62M |
