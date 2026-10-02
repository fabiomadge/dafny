# #6545 A/B benchmark (public corpora, seed 1)

Seeds per (VC, prelude): 1 (1; 0 is Dafny's default). VCs: 27063 in 2077 jobs; **27050 affected** (master and PR counts differ), 13 unaffected (identical counts under master and PR for every seed).

## Proof cost over affected VCs that pass everywhere

Totals are sums of per-VC means over seeds. "Per program" averages each program's own VC geomean, so a
program with hundreds of VCs weighs no more than one with two. Brackets are 95% bootstrap intervals that
resample programs, not VCs.

| group | programs | VCs | largest program | total PR/master | geomean over VCs | per program |
|---|---:|---:|---|---|---|---|
| all but synth | 1249 | 24821 | std/Actions/Producers.dfy (8% of VCs) | +3.5% [-11.5%, +23.0%] | -2.0% [-2.6%, -1.5%] | -4.3% [-4.7%, -4.0%] |
| dafnybench | 7 | 63 | dafnybench/dafny_experiments_tmp_tmpz29_3_3i_circuit.dfy (33% of VCs) | +208.5% [-2.7%, +469.3%] | +3.2% [-2.0%, +9.1%] | +0.7% [-1.8%, +4.9%] |
| kondo | 19 | 1380 | kondo/flexPaxos/sync (11% of VCs) | -27.8% [-67.8%, +18.7%] | -1.5% [-2.3%, -0.8%] | -1.3% [-2.0%, -0.7%] |
| libraries | 77 | 3128 | libraries/JSON/ZeroCopy/Deserializer.dfy (31% of VCs) | +61.8% [+1.6%, +183.3%] | -2.2% [-3.8%, -1.3%] | -4.1% [-6.8%, -2.0%] |
| lit | 1082 | 12638 | lit/concurrency/09-CounterNoStateMachine.dfy (5% of VCs) | -9.4% [-26.8%, +10.8%] | -2.8% [-3.5%, -2.2%] | -4.6% [-5.0%, -4.3%] |
| std | 64 | 7612 | std/Actions/Producers.dfy (27% of VCs) | +25.2% [-0.7%, +71.5%] | -0.6% [-1.5%, -0.1%] | -0.9% [-2.5%, +1.4%] |

2229 affected VCs fail (a verification error) in some run; their cost is the solver's search for a counterexample, reported separately:

| job | VC | master mean (min..max) | PR mean (min..max) |
|---|---|---|---|
| lit/comp/TypeParams.dfy:refresh | Standard (correctness) | 832.98M (832.98..832.98) | 15.86M (15.86..15.86) |
| lit/dafny1/ExtensibleArrayAuto.dfy:refresh | ExtensibleArray.Append (correctness) | 500.05M (500.05..500.05) | 42.06M (42.06..42.06) |
| lit/dafny2/SnapshotableTrees.dfy:refresh | SnapTree.Node.MutatingInsert_Right (correctness) | 500.04M (500.04..500.04) | 500.04M (500.04..500.04) |
| lit/dafny2/SnapshotableTrees.dfy:refresh | SnapTree.Node.FunctionalInsert_Right (correctness) | 500.04M (500.04..500.04) | 500.04M (500.04..500.04) |
| lit/dafny2/SnapshotableTrees.dfy:refresh | SnapTree.Node.FunctionalInsert_Left (correctness) | 500.04M (500.04..500.04) | 500.04M (500.04..500.04) |
| lit/dafny0/FunctionSpecifications.dfy:refresh | GoodPost (well-formedness) | 311.14M (311.14..311.14) | 0.02M (0.02..0.02) |
| lit/cli/defaultTimeLimit.dfy:refresh | Foo (correctness) | 298.84M (298.84..298.84) | 276.73M (276.73..276.73) |
| kondo/paxos/sync | PaxosProof.InvNextLearnerReceivedAcceptImpliesAccepted (correctness) | 293.81M (293.81..293.81) | 306.72M (306.72..306.72) |
| libraries/dafny/Collections/Seqs.dfy | Dafny.Collections.Seq.LemmaMapDistributesOverConcat (correctness) | 243.34M (243.34..243.34) | 2.33M (2.33..2.33) |
| dafnybench/dafny_experiments_tmp_tmpz29_3_3i_circuit.dfy | CombineCircuits.CombineCircuitsCorrect (correctness) | 214.71M (214.71..214.71) | 235.85M (235.85..235.85) |

## Total proof RU per seed (affected VCs that pass everywhere)

| prelude | seed 1 | mean | sd |
|---|---:|---:|---:|
| master | 5552.0M | 5552.0M | 0.0M |
| pr | 5747.0M | 5747.0M | 0.0M |

## Solver time over those proofs (sum of per-VC means, seconds)

| group | master | PR |
|---|---:|---:|
| all | 3780.5 | 3716.1 |
| lit | 1733.0 | 1823.8 |
| std | 820.7 | 816.7 |

## Distribution of per-VC cost ratios over those proofs (mean over seeds)

| ratio bucket | PR/master |
|---|---:|
| < 0.5x | 49 |
| 0.5-0.8x | 268 |
| 0.8-0.95x | 4019 |
| 0.95-1.05x | 19296 |
| 1.05-1.25x | 983 |
| 1.25-2x | 150 |
| 2-4x | 41 |
| >= 4x | 15 |

## Verdict changes at each job's limit (seeds passing out of 1)

| job | VC | limit | master ok | PR ok | master RU | PR RU |
|---|---|---:|---:|---:|---:|---:|
| dafnybench/dafny_experiments_tmp_tmpz29_3_3i_circuit.dfy | BackwardConnections.CombineBackconnsHelper (correctness) | 50M | 1 | 0 | 9.40M | 60.96M |
| kondo/twoPhaseCommit/sync | TwoPCInvariantProof.InvNextLeaderTallyReflectsPreferences (correctness) | 50M | 0 | 1 | 131.29M | 1.09M |
| libraries/Collections/Sequences/LittleEndianNatConversions.dfy | LittleEndianNatConversions.LemmaSmallLargeSmall (correctness) | 40M | 1 | 0 | 37.12M | 169.63M |
| libraries/NonlinearArithmetic/DivMod.dfy | DivMod.LemmaMultiplyDivideLt (correctness) | 40M | 0 | 1 | 1.90M | 0.45M |
| libraries/dafny/Collections/LittleEndianNatConversions.dfy | Dafny.Collections.LittleEndianNatConversions.LemmaSmallLargeSmall (correctness) | 40M | 1 | 0 | 10.99M | 187.63M |
| libraries/dafny/Collections/Seqs.dfy | Dafny.Collections.Seq.LemmaMapDistributesOverConcat (correctness) | 40M | 0 | 1 | 243.34M | 2.33M |
| lit/concurrency/12-MutexLifetime-short.dfy:refresh | MutexGuardU32._ctor (correctness) (assertion batch 132) | 50M | 0 | 1 | 141.80M | 46.08M |
| lit/concurrency/12-MutexLifetime-short.dfy:refresh | MutexGuardU32._ctor (correctness) (assertion batch 96) | 50M | 0 | 1 | 58.15M | 38.18M |
| lit/dafny0/FunctionSpecifications.dfy:refresh | GoodPost (well-formedness) | 50M | 0 | 1 | 311.14M | 0.02M |
| lit/dafny1/ExtensibleArrayAuto.dfy:refresh | ExtensibleArray.Append (correctness) | 50M | 0 | 1 | 500.05M | 42.06M |
| lit/dafny2/SmallestMissingNumber-functional.dfy:refresh | SMN''_Correct (correctness) | 50M | 1 | 0 | 28.21M | 160.24M |
| lit/dafny2/SmallestMissingNumber-functional.dfy:refresh | SMN_Correct (correctness) | 50M | 1 | 0 | 15.25M | 68.41M |
| lit/dafny2/SnapshotableTrees.dfy:refresh | SnapTree.Iterator.Push (correctness) (assertion batch 13) | 50M | 0 | 1 | 118.93M | 0.74M |
| lit/dafny4/Lucas-down.dfy:refresh | Lucas_Binary'' (correctness) | 50M | 0 | 1 | 61.38M | 4.92M |
| lit/vstte2012/RingBufferAuto.dfy:refresh | RingBuffer.Clear (correctness) | 50M | 0 | 1 | 3.83M | 0.12M |
| lit/vstte2012/RingBufferAuto.dfy:refresh | RingBuffer.ResizingEnqueue (correctness) | 50M | 0 | 1 | 8.76M | 10.42M |
| std/Actions/Producers.dfy | Std.Producers.ConcatenatedProducer.Invoke (correctness) (assertion batch 275) | 100M | 1 | 0 | 32.13M | 100.19M |
| std/Arithmetic/DivMod.dfy | Std.Arithmetic.DivMod.LemmaFundamentalDivModConverse (correctness) | 50M | 0 | 1 | 31.84M | 10.74M |
| std/Arithmetic/DivMod.dfy | Std.Arithmetic.DivMod.LemmaMultiplyDivideLe (correctness) | 50M | 1 | 0 | 0.38M | 1.20M |
| std/Base64.dfy | Std.Base64.DecodeEncodeRecursively (correctness) (assertion batch 24) | 5M | 1 | 0 | 1.10M | 13.28M |
| std/Base64.dfy | Std.Base64.DecodeValidEncode2Padding (correctness) | 5M | 0 | 1 | 7.26M | 0.82M |
| std/Base64.dfy | Std.Base64.EncodeBVIsBase64 (correctness) | 5M | 1 | 0 | 1.80M | 163.85M |
| std/Base64.dfy | Std.Base64.EncodeBVLengthCongruentToZeroMod4 (correctness) (assertion batch 5) | 50M | 1 | 0 | 8.58M | 50.05M |

## Largest changes among those proofs (by |PR - master| mean RU)

| job | VC | master | PR | PR/master | min..max master | min..max PR |
|---|---|---:|---:|---:|---|---|
| libraries/dafny/Collections/LittleEndianNatConversions.dfy | Dafny.Collections.LittleEndianNatConversions.LemmaSmallLargeSmall (correctness) | 10.99M | 187.63M | 17.08 | 10.99..10.99M | 187.63..187.63M |
| libraries/JSON/ZeroCopy/Serializer.dfy | JSON.ZeroCopy.Serializer.Number (well-formedness) (assertion batch 17) | 135.34M | 299.37M | 2.21 | 135.34..135.34M | 299.37..299.37M |
| std/Base64.dfy | Std.Base64.EncodeBVIsBase64 (correctness) | 1.80M | 163.85M | 90.92 | 1.80..1.80M | 163.85..163.85M |
| lit/dafny2/SmallestMissingNumber-functional.dfy:refresh | SMN''_Correct (correctness) | 28.21M | 160.24M | 5.68 | 28.21..28.21M | 160.24..160.24M |
| kondo/twoPhaseCommit/sync | TwoPCInvariantProof.InvNextLeaderTallyReflectsPreferences (correctness) | 131.29M | 1.09M | 0.01 | 131.29..131.29M | 1.09..1.09M |
| lit/dafny2/SnapshotableTrees.dfy:refresh | SnapTree.Iterator.Push (correctness) (assertion batch 13) | 118.93M | 0.74M | 0.01 | 118.93..118.93M | 0.74..0.74M |
| lit/concurrency/12-MutexLifetime-short.dfy:refresh | MutexGuardU32._ctor (correctness) (assertion batch 132) | 141.80M | 46.08M | 0.32 | 141.80..141.80M | 46.08..46.08M |
| std/Actions/Producers.dfy | Std.Producers.ConcatenatedProducer.Invoke (correctness) (assertion batch 283) | 6.80M | 74.35M | 10.94 | 6.80..6.80M | 74.35..74.35M |
| lit/dafny4/Lucas-down.dfy:refresh | Lucas_Binary'' (correctness) | 61.38M | 4.92M | 0.08 | 61.38..61.38M | 4.92..4.92M |
| kondo/paxos/sync | PaxosProof.InvNextLeaderReceivedPromisesImpliesAcceptorState (correctness) | 171.77M | 115.41M | 0.67 | 171.77..171.77M | 115.41..115.41M |
| lit/dafny2/SmallestMissingNumber-functional.dfy:refresh | SMN_Correct (correctness) | 15.25M | 68.41M | 4.48 | 15.25..15.25M | 68.41..68.41M |
| dafnybench/dafny_experiments_tmp_tmpz29_3_3i_circuit.dfy | BackwardConnections.CombineBackconnsHelper (correctness) | 9.40M | 60.96M | 6.49 | 9.40..9.40M | 60.96..60.96M |
| std/Actions/Producers.dfy | Std.Producers.ConcatenatedProducer.Invoke (correctness) (assertion batch 276) | 4.64M | 47.09M | 10.15 | 4.64..4.64M | 47.09..47.09M |
| kondo/flexPaxos/sync | PaxosProof.InvNextLeaderReceivedPromisesImpliesAcceptorState (correctness) | 174.48M | 143.12M | 0.82 | 174.48..174.48M | 143.12..143.12M |
| lit/dafny4/FlyingRobots.dfy:refresh | FormArmy (correctness) | 43.48M | 14.58M | 0.34 | 43.48..43.48M | 14.58..14.58M |
| lit/concurrency/09-CounterNoStateMachine.dfy:refresh | Incrementer (correctness) (assertion batch 105) | 8.79M | 35.61M | 4.05 | 8.79..8.79M | 35.61..35.61M |
| std/Actions/Producers.dfy | Std.Producers.FlattenedProducer.Invoke (correctness) | 64.47M | 89.12M | 1.38 | 64.47..64.47M | 89.12..89.12M |
| lit/dafny2/SmallestMissingNumber-functional.dfy:refresh | SMN'_Correct (correctness) | 120.25M | 98.28M | 0.82 | 120.25..120.25M | 98.28..98.28M |
| kondo/flexPaxos/sync | PaxosProof.InvNextLearnerReceivedAcceptImpliesAccepted (correctness) | 45.53M | 23.67M | 0.52 | 45.53..45.53M | 23.67..23.67M |
| libraries/dafny/NonlinearArithmetic/DivMod.dfy | Dafny.DivMod.LemmaFundamentalDivModConverse (correctness) | 5.31M | 26.70M | 5.03 | 5.31..5.31M | 26.70..26.70M |
| lit/concurrency/12-MutexLifetime-short.dfy:refresh | MutexGuardU32._ctor (correctness) (assertion batch 96) | 58.15M | 38.18M | 0.66 | 58.15..58.15M | 38.18..38.18M |
| lit/concurrency/12-MutexLifetime-short.dfy:refresh | MutexGuardU32._ctor (correctness) (assertion batch 138) | 47.85M | 28.58M | 0.60 | 47.85..47.85M | 28.58..28.58M |
| libraries/Collections/Sequences/Seq.dfy | Seq.LemmaFilterDistributesOverConcat (correctness) (assertion batch 2) | 61.24M | 79.89M | 1.30 | 61.24..61.24M | 79.89..79.89M |
| lit/dafny3/SimpleInduction.dfy:refresh | FibLemma (correctness) | 20.52M | 2.70M | 0.13 | 20.52..20.52M | 2.70..2.70M |
| lit/dafny2/MinWindowMax.dfy:refresh | MinimumWindowMax (correctness) (assertion batch 133) | 21.67M | 4.79M | 0.22 | 21.67..21.67M | 4.79..4.79M |

## Per job (proofs among the affected VCs)

| job | VCs | master | PR | PR vs master |
|---|---:|---:|---:|---:|
| lit/concurrency/12-MutexLifetime-short.dfy:refresh | 386 | 618.33M | 468.57M | -24.2% |
| lit/dafny0/RlimitMultiplier.dfy:refresh | 2 | 593.99M | 593.99M | -0.0% |
| std/Actions/Producers.dfy | 2025 | 516.07M | 637.40M | +23.5% |
| kondo/flexPaxos/sync | 147 | 383.01M | 332.14M | -13.3% |
| kondo/paxos/sync | 146 | 305.87M | 222.14M | -27.4% |
| std/JSON/ZeroCopy/Deserializer.dfy | 1068 | 243.70M | 240.83M | -1.2% |
| libraries/JSON/ZeroCopy/Deserializer.dfy | 983 | 217.08M | 214.35M | -1.3% |
| lit/dafny2/SmallestMissingNumber-functional.dfy:refresh | 19 | 164.19M | 327.40M | +99.4% |
| libraries/JSON/ZeroCopy/Serializer.dfy | 98 | 154.05M | 317.08M | +105.8% |
| lit/concurrency/09-CounterNoStateMachine.dfy:refresh | 591 | 153.20M | 172.49M | +12.6% |
| lit/dafny2/SnapshotableTrees.dfy:refresh | 101 | 143.27M | 11.16M | -92.2% |
| kondo/twoPhaseCommit/sync | 90 | 137.13M | 6.62M | -95.2% |
| lit/concurrency/10-SequenceInvariant.dfy:refresh | 485 | 129.67M | 129.38M | -0.2% |
| std/Base64.dfy | 480 | 114.15M | 282.49M | +147.5% |
| lit/dafny2/MinWindowMax.dfy:refresh | 237 | 97.35M | 77.26M | -20.6% |
| std/Actions/BulkActions.dfy | 594 | 78.48M | 78.97M | +0.6% |
| lit/dafny4/UnionFind.dfy:refresh | 323 | 71.62M | 73.95M | +3.3% |
| libraries/Collections/Sequences/Seq.dfy | 78 | 65.23M | 84.11M | +29.0% |
| lit/concurrency/06-ThreadOwnership.dfy:refresh | 94 | 63.79M | 59.61M | -6.6% |
| lit/dafny4/Lucas-down.dfy:refresh | 12 | 61.63M | 5.14M | -91.7% |
| lit/dafny4/FlyingRobots.dfy:refresh | 31 | 58.66M | 20.69M | -64.7% |
| std/JSON/ZeroCopy/Serializer.dfy | 648 | 56.84M | 56.96M | +0.2% |
| lit/dafny4/Regression16.dfy:refresh | 5 | 50.66M | 35.29M | -30.3% |
| lit/dafny1/SchorrWaite-stages.dfy:refresh | 230 | 47.16M | 51.92M | +10.1% |
| lit/concurrency/07-CounterThreadOwnership.dfy:refresh | 176 | 45.83M | 35.98M | -21.5% |
| lit/dafny1/SchorrWaite.dfy:refresh | 276 | 36.39M | 36.01M | -1.0% |
| std/Actions/Consumers.dfy | 470 | 32.41M | 32.33M | -0.2% |
| lit/dafny3/GenericSort.dfy:refresh | 20 | 28.36M | 14.73M | -48.0% |
| lit/concurrency/08-CounterNoTermination.dfy:refresh | 139 | 26.37M | 25.75M | -2.4% |
| libraries/NonlinearArithmetic/DivMod.dfy | 255 | 25.00M | 18.01M | -27.9% |
| lit/vacid0/Composite.dfy:refresh | 13 | 22.08M | 15.40M | -30.3% |
| kondo/simplifiedLeaderElection/sync | 61 | 22.05M | 32.45M | +47.2% |
| lit/dafny3/SimpleInduction.dfy:refresh | 10 | 21.07M | 3.13M | -85.1% |
| lit/VSI-Benchmarks/b4.dfy:refresh | 72 | 20.83M | 23.32M | +12.0% |
| libraries/dafny/NonlinearArithmetic/DivMod.dfy | 252 | 18.35M | 38.31M | +108.8% |
| lit/dafny1/ExtensibleArray.dfy:refresh | 9 | 18.32M | 15.34M | -16.3% |
| libraries/dafny/Collections/Seqs.dfy | 77 | 15.98M | 6.13M | -61.6% |
| std/Actions/Actions.dfy | 188 | 15.42M | 15.44M | +0.2% |
| libraries/NonlinearArithmetic/Internals/DivInternals.dfy | 11 | 15.34M | 25.28M | +64.8% |
| libraries/dafny/NonlinearArithmetic/Internals/DivInternals.dfy | 11 | 15.34M | 25.28M | +64.8% |
| libraries/dafny/BinaryOperations.dfy | 10 | 14.50M | 14.50M | -0.0% |
| lit/dafny0/Termination.dfy:refresh | 107 | 14.36M | 12.32M | -14.2% |
| std/Arithmetic/DivMod.dfy | 295 | 12.98M | 10.70M | -17.5% |
| libraries/dafny/Collections/LittleEndianNatConversions.dfy | 27 | 12.74M | 189.36M | +1386.6% |
| lit/git-issues/git-issue-3855.dfy:pinned | 99 | 12.26M | 12.29M | +0.2% |
| lit/vstte2012/BreadthFirstSearch.dfy:refresh | 148 | 11.97M | 11.08M | -7.5% |
| lit/git-issues/github-issue-2174.dfy:refresh | 17 | 11.71M | 11.70M | -0.1% |
| std/Collections/Seq.dfy | 191 | 11.43M | 10.61M | -7.2% |
| dafnybench/DafnyProjects_tmp_tmp2acw_s4s_RawSort.dfy | 7 | 11.31M | 11.03M | -2.5% |
| dafnybench/dafny_experiments_tmp_tmpz29_3_3i_circuit.dfy | 21 | 10.53M | 62.34M | +491.9% |
| lit/dafny2/pq-intrinsic-extrinsic.dfy:refresh | 52 | 10.06M | 11.20M | +11.4% |
| lit/dafny2/TreeBarrier.dfy:refresh | 7 | 9.90M | 9.79M | -1.1% |
| lit/cloudmake/CloudMake-CachedBuilds.dfy:refresh | 76 | 9.71M | 9.39M | -3.3% |
| std/Parsers/String/StringParsers.dfy | 184 | 9.65M | 9.66M | +0.1% |
| kondo/ringLeaderElection/sync | 49 | 9.45M | 10.94M | +15.7% |
| lit/dafny1/PriorityQueue.dfy:refresh | 22 | 8.67M | 8.75M | +1.0% |
| lit/dafny1/BinaryTree.dfy:refresh | 19 | 8.38M | 8.83M | +5.3% |
| lit/VSI-Benchmarks/b5.dfy:refresh | 18 | 7.87M | 4.68M | -40.5% |
| lit/dafny1/Queue.dfy:refresh | 18 | 7.79M | 4.68M | -40.0% |
| lit/dafny1/ExtensibleArrayAuto.dfy:refresh | 8 | 7.43M | 4.72M | -36.5% |
| std/Arithmetic/LittleEndianNat.dfy | 246 | 7.20M | 7.19M | -0.2% |
| libraries/Collections/Sequences/MergeSort.dfy | 2 | 6.72M | 1.47M | -78.1% |
| lit/dafny2/COST-verif-comp-2011-3-TwoDuplicates.dfy:refresh | 4 | 6.65M | 3.91M | -41.2% |
| lit/dafny4/GHC-MergeSort.dfy:refresh | 55 | 6.14M | 7.85M | +27.7% |
| lit/examples/induction-principle-code/EliminateMulZero.dfy:refresh | 30 | 6.12M | 5.12M | -16.4% |
| lit/vstte2012/Tree.dfy:refresh | 67 | 6.01M | 5.49M | -8.7% |
| kondo/lockServer/manual | 86 | 5.93M | 6.48M | +9.3% |
| libraries/Collections/Sequences/LittleEndianNat.dfy | 188 | 5.76M | 5.66M | -1.7% |
| libraries/dafny/Collections/LittleEndianNat.dfy | 188 | 5.76M | 5.66M | -1.7% |
| lit/comp/rust/loops.dfy:refresh | 8 | 5.67M | 8.65M | +52.5% |
| std/Termination.dfy | 44 | 5.53M | 8.57M | +54.9% |
| lit/cloudmake/CloudMake-ParallelBuilds.dfy:refresh | 66 | 5.45M | 5.61M | +3.0% |
| kondo/twoPhaseCommit/manual | 82 | 5.27M | 5.30M | +0.5% |
| kondo/twoPhaseCommit/paper-version | 89 | 5.24M | 5.24M | -0.1% |
| std/JSON/Serializer.dfy | 30 | 4.96M | 5.00M | +0.9% |
| lit/VSComp2010/Problem5-DoubleEndedQueue.dfy:refresh | 19 | 4.52M | 4.55M | +0.8% |
| kondo/shardedKvBatched/manual | 66 | 4.51M | 4.30M | -4.7% |
| lit/cloudmake/CloudMake-ConsistentBuilds.legacy.dfy:refresh | 42 | 4.14M | 4.13M | -0.4% |
| lit/comp/Arrays.dfy:refresh | 89 | 4.09M | 3.20M | -21.6% |
| lit/unicodecharsFalse/comp/Arrays.dfy:refresh | 89 | 4.05M | 3.17M | -21.8% |
| lit/git-issues/github-issue-2230.dfy:refresh | 2 | 3.98M | 3.98M | -0.0% |
| kondo/shardedKv/manual | 65 | 3.96M | 4.20M | +6.2% |
| lit/dafny2/Classics.dfy:refresh | 4 | 3.93M | 7.48M | +90.1% |
| lit/examples/induction-principle-code/VarUnchanged.dfy:refresh | 30 | 3.84M | 3.82M | -0.6% |
| lit/git-issues/git-issue-505.dfy:refresh | 2 | 3.76M | 3.76M | -0.0% |
| lit/dafny4/NumberRepresentations.dfy:refresh | 39 | 3.71M | 11.49M | +209.5% |
| lit/examples/induction-principle-code/Equiv.dfy:refresh | 31 | 3.69M | 3.62M | -1.9% |
| std/Parsers/Core/ParsersTheorems.dfy | 67 | 3.69M | 3.67M | -0.5% |
| lit/VSI-Benchmarks/b8.dfy:refresh | 33 | 3.65M | 4.00M | +9.4% |
| lit/examples/induction-principle-code/Pure.dfy:refresh | 26 | 3.64M | 3.61M | -1.0% |
| lit/dafny4/NipkowKlein-chapter7.dfy:refresh | 26 | 3.49M | 3.44M | -1.5% |
| kondo/simplifiedLeaderElection/manual | 61 | 3.42M | 2.91M | -14.9% |
| kondo/ringLeaderElection/manual | 66 | 3.38M | 5.11M | +51.2% |
| lit/dafny0/Fp64ResolutionAndLanguage.dfy:refresh | 12 | 3.23M | 2.17M | -32.7% |
| std/JSON/Deserializer.dfy | 59 | 3.18M | 3.17M | -0.0% |
| lit/dafny2/COST-verif-comp-2011-4-FloydCycleDetect.dfy:refresh | 23 | 3.04M | 3.59M | +18.1% |
| std/Unicode/Utf8EncodingForm.dfy | 65 | 2.94M | 3.35M | +13.9% |
| lit/dafny0/NoTypeArgs.dfy:refresh | 8 | 2.90M | 2.92M | +0.6% |
| lit/VerifyThis2015/Problem3.dfy:refresh | 18 | 2.82M | 2.69M | -4.6% |
| std/Arithmetic/Internal/DivInternals.dfy | 95 | 2.82M | 2.73M | -3.0% |
| std/JSON/Utils/Cursors.dfy | 39 | 2.81M | 2.54M | -9.6% |
| lit/dafny0/LetExpr.dfy:refresh | 39 | 2.75M | 2.74M | -0.4% |
| libraries/JSON/Utils/Cursors.dfy | 39 | 2.74M | 3.01M | +9.8% |
| std/JSON/Spec.dfy | 13 | 2.73M | 2.79M | +1.9% |
| lit/lambdas/MatrixAssoc.dfy:pinned | 46 | 2.70M | 2.10M | -22.1% |
| kondo/shardedKvBatched/sync | 49 | 2.67M | 2.88M | +8.1% |
| lit/vacid0/LazyInitArray.dfy:refresh | 6 | 2.65M | 2.81M | +6.0% |
| lit/dafny4/Lucas-up.dfy:refresh | 29 | 2.53M | 2.46M | -2.9% |
| lit/vstte2012/RingBuffer.dfy:refresh | 11 | 2.53M | 1.90M | -24.9% |
| std/Parsers/Core/Parsers.dfy | 57 | 2.46M | 2.27M | -7.7% |
| kondo/lockServer/sync | 61 | 2.40M | 2.45M | +1.9% |
| lit/vacid0/SparseArray.dfy:refresh | 7 | 2.37M | 2.55M | +7.3% |
| lit/dafny0/MultiSets.dfy:refresh | 35 | 2.34M | 3.51M | +50.1% |
| lit/dafny4/Primes.dfy:refresh | 27 | 2.28M | 5.36M | +135.4% |
| lit/vstte2012/RingBufferAuto.dfy:refresh | 11 | 2.21M | 2.76M | +25.0% |
| kondo/clientServer/manual | 60 | 2.19M | 2.25M | +2.5% |
| libraries/Unicode/UnicodeStringsWithUnicodeChar.dfy | 18 | 2.16M | 2.15M | -0.3% |
| lit/dafny0/Fp64ComprehensiveEdgeCases.dfy:refresh | 10 | 2.08M | 2.08M | -0.1% |
| lit/wishlist/sequences-literals.dfy:refresh | 4 | 2.04M | 2.04M | -0.1% |
| lit/dafny3/InfiniteTrees.dfy:pinned | 48 | 2.04M | 2.04M | +0.2% |
| std/JSON/API.dfy | 4 | 2.03M | 2.03M | -0.0% |
| lit/dafny1/ListContents.dfy:refresh | 10 | 2.03M | 1.82M | -10.4% |
| lit/VSI-Benchmarks/b3.dfy:refresh | 11 | 2.00M | 4.85M | +142.4% |
| lit/VerifyThis2015/Problem1.dfy:refresh | 76 | 1.96M | 1.98M | +1.0% |
| kondo/clientServer/sync | 53 | 1.94M | 1.79M | -7.7% |
| lit/examples/Simple_compiler/Compiler.dfy:refresh | 19 | 1.93M | 1.96M | +1.5% |
| lit/concurrency/05-RecInvariantCut.dfy:refresh | 35 | 1.92M | 1.62M | -15.9% |
| std/JSON/ConcreteSyntax.Spec.dfy | 16 | 1.85M | 1.88M | +1.4% |
| std/Unicode/UnicodeStringsWithUnicodeChar.dfy | 20 | 1.84M | 1.83M | -0.7% |
| lit/concurrency/03-SimpleCounter.dfy:refresh | 42 | 1.75M | 1.74M | -0.6% |
| libraries/JSON/ConcreteSyntax.Spec.dfy | 16 | 1.73M | 1.73M | -0.2% |
| dafnybench/fv2020-tms_tmp_tmpnp85b47l_modeling_concurrency_safety.dfy | 12 | 1.72M | 1.66M | -3.3% |
| lit/dafny4/git-issue196.dfy:refresh | 9 | 1.72M | 1.02M | -40.4% |
| lit/comp/GeneralNewtypes.dfy:pinned | 75 | 1.63M | 1.59M | -2.7% |
| lit/concurrency/02-DoubleRead.dfy:refresh | 40 | 1.62M | 1.62M | -0.1% |
| std/Arithmetic/Internal/ModInternals.dfy | 211 | 1.58M | 1.50M | -5.5% |
| kondo/distributedLock/manual | 52 | 1.58M | 1.85M | +17.2% |
| lit/vstte2012/Combinators.dfy:refresh | 26 | 1.55M | 3.05M | +95.9% |
| kondo/shardedKv/sync | 49 | 1.51M | 1.49M | -1.8% |
| std/Unicode/UnicodeEncodingForm.dfy | 19 | 1.50M | 1.93M | +28.2% |
| lit/git-issues/git-issue-1250.dfy:refresh | 8 | 1.47M | 1.47M | -0.6% |
| libraries/Unicode/Utf8EncodingForm.dfy | 18 | 1.47M | 1.64M | +11.5% |
| libraries/dafny/Unicode/Utf8EncodingForm.dfy | 18 | 1.47M | 1.64M | +11.5% |
| lit/dafny0/Computations.dfy:refresh | 44 | 1.47M | 1.52M | +3.4% |
| lit/dafny0/Maps.dfy:refresh | 49 | 1.39M | 1.36M | -1.8% |
| std/Unicode/Utf16EncodingForm.dfy | 11 | 1.37M | 1.32M | -3.7% |
| libraries/Unicode/Utf16EncodingForm.dfy | 11 | 1.35M | 1.31M | -3.1% |
| libraries/dafny/Unicode/Utf16EncodingForm.dfy | 11 | 1.35M | 1.31M | -3.1% |
| lit/dafny0/Twostate-Verification.dfy:refresh | 65 | 1.34M | 1.37M | +2.4% |
| lit/dafny3/Filter.dfy:refresh | 30 | 1.33M | 1.33M | -0.5% |
| std/Strings.dfy | 33 | 1.32M | 1.65M | +24.8% |
| std/JSON/ZeroCopy/API.dfy | 6 | 1.32M | 1.32M | -0.1% |
| lit/dafny0/Basics.dfy:refresh | 53 | 1.31M | 1.31M | -0.2% |
| lit/hofs/VectorUpdate.dfy:refresh | 8 | 1.24M | 2.30M | +85.1% |
| lit/dafny2/MajorityVote.dfy:refresh | 16 | 1.22M | 1.29M | +5.6% |
| kondo/distributedLock/sync | 48 | 1.21M | 1.46M | +20.4% |
| libraries/JSON/Utils/Vectors.dfy | 23 | 1.18M | 1.21M | +2.7% |
| libraries/JSON/Utils/Str.dfy | 28 | 1.18M | 1.17M | -1.1% |
| lit/dafny0/TypeInferenceRefresh.dfy:pinned | 91 | 1.17M | 1.11M | -5.1% |
| lit/comp/rust/operators.dfy:refresh | 22 | 1.13M | 1.34M | +19.2% |
| libraries/Unicode/UnicodeStringsWithoutUnicodeChar.dfy | 12 | 1.11M | 1.11M | -0.2% |
| lit/comp/Forall.dfy:refresh | 27 | 1.09M | 1.15M | +5.9% |
| libraries/dafny/NonlinearArithmetic/Power.dfy | 63 | 1.07M | 1.03M | -3.8% |
| lit/comp/CovariantCollections.dfy:pinned | 26 | 1.07M | 1.00M | -6.4% |
| lit/comp/ForallNewSyntax.dfy:refresh | 25 | 1.07M | 1.14M | +7.0% |
| lit/comp/Collections.dfy:refresh | 37 | 1.06M | 1.03M | -3.5% |
| lit/unicodecharsFalse/comp/Collections.dfy:refresh | 37 | 1.06M | 1.03M | -3.5% |
| lit/dafny2/MonotonicHeapstate.dfy:refresh | 17 | 1.06M | 1.05M | -1.3% |
| std/Arithmetic/Power.dfy | 63 | 1.06M | 1.02M | -4.3% |
| lit/concurrency/01-InnerOuter.dfy:refresh | 32 | 1.05M | 1.04M | -0.6% |
| libraries/Unicode/UnicodeEncodingForm.dfy | 15 | 1.04M | 0.95M | -9.2% |
| libraries/Collections/Sequences/LittleEndianNatConversions.dfy | 26 | 1.03M | 0.87M | -15.7% |
| libraries/JSON/Grammar.dfy | 42 | 1.03M | 1.02M | -0.7% |
| std/JSON/Grammar.dfy | 42 | 1.03M | 1.02M | -0.7% |
| lit/traits/TraitCompile.dfy:pinned | 74 | 1.02M | 1.01M | -1.2% |
| lit/dafny0/Array.dfy:refresh | 41 | 1.02M | 0.86M | -15.4% |
| lit/dafny0/InductivePredicates.dfy:refresh | 32 | 1.02M | 1.12M | +9.2% |
| libraries/NonlinearArithmetic/Power.dfy | 62 | 1.01M | 0.98M | -3.8% |
| lit/dafny4/ACL2-extractor.dfy:refresh | 32 | 0.99M | 0.99M | -0.7% |
| lit/dafny1/SeparationLogicList.dfy:refresh | 13 | 0.98M | 1.00M | +2.4% |
| lit/dafny1/BDD.dfy:refresh | 5 | 0.97M | 0.96M | -0.8% |
| lit/dafny1/Induction.legacy.dfy:refresh | 32 | 0.97M | 1.09M | +12.5% |
| lit/dafny3/Iter.dfy:refresh | 12 | 0.95M | 1.02M | +7.0% |
| std/DynamicArray.dfy | 20 | 0.95M | 0.94M | -1.0% |
| std/JSON/Utils/Views.Writers.dfy | 17 | 0.94M | 0.87M | -8.0% |
| lit/dafny4/SoftwareFoundations-Basics.dfy:refresh | 53 | 0.93M | 0.91M | -2.1% |
| lit/comp/Comprehensions.dfy:refresh | 32 | 0.92M | 0.90M | -1.8% |
| lit/unicodecharsFalse/comp/Comprehensions.dfy:refresh | 32 | 0.92M | 0.90M | -1.8% |
| libraries/dafny/Unicode/Utf8EncodingScheme.dfy | 4 | 0.92M | 0.36M | -61.2% |
| lit/examples/induction-principle-code/Induction.dfy:refresh | 17 | 0.90M | 0.90M | -0.1% |
| lit/traits/TraitExample.dfy:refresh | 29 | 0.90M | 0.94M | +3.4% |
| lit/VSI-Benchmarks/b6.dfy:refresh | 17 | 0.90M | 0.94M | +4.7% |
| lit/dafny0/Fp32ResolutionAndLanguage.dfy:refresh | 12 | 0.88M | 0.87M | -1.1% |
| std/Arithmetic/Mul.dfy | 54 | 0.87M | 0.85M | -1.8% |
| libraries/JSON/Utils/Views.Writers.dfy | 17 | 0.87M | 0.86M | -1.0% |
| libraries/NonlinearArithmetic/Mul.dfy | 53 | 0.86M | 0.83M | -2.9% |
| libraries/dafny/NonlinearArithmetic/Multiply.dfy | 53 | 0.86M | 0.83M | -2.9% |
| lit/c++/maps.dfy:refresh | 9 | 0.84M | 0.99M | +18.8% |
| lit/dafny0/Fp32ComprehensiveEdgeCases.dfy:refresh | 10 | 0.83M | 0.83M | -0.2% |
| dafnybench/dafny-programs_tmp_tmpcwodh6qh_src_ticketsystem.dfy | 9 | 0.82M | 0.80M | -1.5% |
| lit/dafny3/CachedContainer.dfy:refresh | 27 | 0.81M | 0.81M | +1.1% |
| lit/examples/induction-principle-code/PureNoInductionPrinciple.dfy:refresh | 2 | 0.80M | 0.79M | -0.8% |
| lit/dafny0/IMaps.dfy:refresh | 14 | 0.80M | 0.81M | +1.3% |
| lit/dafny0/Inverses.dfy:refresh | 31 | 0.78M | 0.78M | -1.1% |
| libraries/Collections/Sets/Sets.dfy | 28 | 0.77M | 0.77M | +0.8% |
| libraries/dafny/Collections/Sets.dfy | 28 | 0.77M | 0.77M | +0.8% |
| lit/dafny0/GeneralNewtypeCollections.dfy:pinned | 44 | 0.77M | 0.72M | -5.3% |
| std/Collections/Set.dfy | 28 | 0.76M | 0.76M | +0.7% |
| lit/comp/Uninitialized.dfy:refresh | 24 | 0.75M | 0.75M | -0.9% |
| lit/comp/Numbers.dfy:pinned | 75 | 0.74M | 0.71M | -3.8% |
| lit/unicodecharsFalse/comp/Numbers.dfy:pinned | 75 | 0.74M | 0.71M | -3.8% |
| lit/dafny0/ReadsOnMethods.dfy:refresh | 68 | 0.74M | 0.73M | -0.9% |
| lit/dafny3/Streams.dfy:refresh | 29 | 0.74M | 0.72M | -1.9% |
| lit/comp/Poly.dfy:refresh | 15 | 0.72M | 0.58M | -19.7% |
| lit/dafny1/MoreInduction.dfy:refresh | 26 | 0.72M | 0.74M | +2.9% |
| lit/dafny4/KozenSilva.dfy:refresh | 25 | 0.72M | 0.71M | -1.5% |
| lit/dafny4/NipkowKlein-chapter3.dfy:refresh | 20 | 0.72M | 0.73M | +1.9% |
| lit/dafny0/GeneralNewtypeCollectionsGeneric.dfy:pinned | 44 | 0.72M | 0.71M | -1.6% |
| lit/hofs/Folding.legacy.dfy:refresh | 21 | 0.70M | 0.70M | +0.9% |
| lit/dafny0/DefaultParameters.dfy:refresh | 72 | 0.67M | 0.65M | -2.8% |
| libraries/dafny/NonlinearArithmetic/Internals/ModInternals.dfy | 39 | 0.66M | 0.63M | -3.9% |
| libraries/NonlinearArithmetic/Internals/ModInternals.dfy | 39 | 0.65M | 0.63M | -4.0% |
| lit/VerifyThis2015/Problem2.dfy:refresh | 32 | 0.65M | 0.66M | +2.9% |
| lit/dafny4/Ackermann.dfy:refresh | 14 | 0.65M | 0.57M | -11.0% |
| lit/dafny0/MoForallCompilation.dfy:refresh | 18 | 0.64M | 0.64M | -0.4% |
| lit/blogposts/TestGenerationWithInliningQuantifiedDefinitions.dfy:refresh | 8 | 0.64M | 0.53M | -16.9% |
| lit/dafny1/Rippling.legacy.dfy:refresh | 46 | 0.63M | 0.61M | -2.5% |
| lit/dafny0/Iterators.dfy:refresh | 35 | 0.62M | 0.62M | -0.2% |
| lit/dafny2/Z-BirthdayBook.dfy:refresh | 18 | 0.62M | 0.61M | -0.8% |
| libraries/Unicode/Utf8EncodingScheme.dfy | 4 | 0.61M | 1.91M | +211.0% |
| lit/dafny4/Leq.dfy:refresh | 16 | 0.60M | 0.58M | -2.7% |
| lit/VSI-Benchmarks/b7.dfy:refresh | 16 | 0.60M | 0.59M | -1.7% |
| lit/dafny0/CanCall.dfy:refresh | 34 | 0.59M | 0.59M | -0.4% |
| lit/dafny0/DeterministicPick.dfy:refresh | 5 | 0.58M | 0.58M | -0.5% |
| std/JSON/Utils/Views.dfy | 14 | 0.58M | 0.55M | -5.4% |
| libraries/JSON/Utils/Views.dfy | 14 | 0.58M | 0.55M | -5.4% |
| lit/dafny0/GeneralNewtypeVerify.dfy:pinned | 43 | 0.57M | 0.56M | -2.8% |
| lit/dafny2/COST-verif-comp-2011-2-MaxTree-class.dfy:refresh | 9 | 0.56M | 0.67M | +20.5% |
| lit/dafny1/UnboundedStack.dfy:refresh | 10 | 0.55M | 0.56M | +2.7% |
| lit/dafny0/SmallTests.dfy:refresh | 56 | 0.52M | 0.52M | +0.1% |
| lit/dafny0/AutoContracts.dfy:refresh | 36 | 0.52M | 0.52M | +0.3% |
| lit/dafny4/gcd.dfy:refresh | 23 | 0.51M | 0.50M | -2.3% |
| libraries/dafny/Unicode/UnicodeEncodingForm.dfy | 14 | 0.51M | 0.50M | -2.7% |
| lit/examples/parser_combinators.dfy:refresh | 9 | 0.51M | 0.50M | -1.4% |
| lit/dafny4/ClassRefinement.dfy:refresh | 11 | 0.49M | 0.49M | -1.2% |
| lit/comp/rust/newtypes.dfy:refresh | 25 | 0.49M | 0.47M | -2.7% |
| lit/hofs/SumSum.dfy:refresh | 11 | 0.47M | 0.47M | +1.7% |
| lit/dafny0/ForLoops.dfy:refresh | 23 | 0.46M | 0.45M | -2.7% |
| lit/autoRevealDependencies/ast.dfy:refresh | 7 | 0.46M | 0.48M | +4.0% |
| lit/dafny0/ArrayElementInitCompile.dfy:refresh | 18 | 0.46M | 0.45M | -1.9% |
| lit/VSComp2010/Problem4-Queens.dfy:refresh | 8 | 0.45M | 0.44M | -3.1% |
| lit/git-issues/git-issue-697j.dfy:refresh | 66 | 0.45M | 0.42M | -6.0% |
| std/JSON/Utils/Parsers.dfy | 6 | 0.44M | 0.44M | -0.1% |
| lit/dafny2/Calculations.dfy:refresh | 20 | 0.44M | 0.43M | -1.8% |
| std/JSON/ConcreteSyntax.SpecProperties.dfy | 7 | 0.44M | 0.45M | +2.5% |
| lit/dafny0/Fuel.dfy:refresh | 31 | 0.44M | 0.43M | -2.2% |
| libraries/JSON/Utils/Parsers.dfy | 6 | 0.44M | 0.44M | +0.5% |
| lit/VSComp2010/Problem3-FindZero.dfy:refresh | 6 | 0.43M | 0.45M | +4.5% |
| lit/dafny4/Fstar-QuickSort.dfy:refresh | 6 | 0.43M | 0.41M | -5.9% |
| lit/dafny4/CoqArt-InsertionSort.dfy:refresh | 21 | 0.43M | 0.43M | -0.5% |
| std/Unicode/Utf8EncodingScheme.dfy | 4 | 0.43M | 3.12M | +628.9% |
| lit/dafny3/Abstemious.dfy:pinned | 21 | 0.43M | 0.43M | -0.7% |
| lit/hofs/TreeMapSimple.dfy:refresh | 7 | 0.42M | 0.41M | -2.7% |
| lit/dafny0/CoinductiveProofs.dfy:refresh | 23 | 0.42M | 0.39M | -6.3% |
| lit/autoRevealDependencies/tree-map-simple.dfy:refresh | 7 | 0.42M | 0.42M | +0.4% |
| lit/comp/TypeDescriptors.dfy:refresh | 11 | 0.41M | 0.41M | -1.6% |
| lit/dafny4/ExpandedGuardedness.dfy:refresh | 12 | 0.41M | 0.43M | +3.8% |
| lit/comp/TailRecursion.dfy:refresh | 28 | 0.41M | 0.41M | -0.9% |
| lit/dafny2/StoreAndRetrieve.dfy:refresh | 16 | 0.41M | 0.41M | -0.2% |
| lit/dafny0/ControlStructures.dfy:refresh | 18 | 0.41M | 0.34M | -15.5% |
| lit/DafnyTests/TestAttribute/TestAttribute.dfy:refresh | 42 | 0.40M | 0.41M | +2.0% |
| lit/comp/rust/traits.dfy:refresh | 23 | 0.40M | 0.41M | +3.7% |
| std/Parsers/Core/ParsersBuilders.dfy | 5 | 0.40M | 0.38M | -4.0% |
| lit/comp/UnicodeStrings.dfy:pinned | 21 | 0.40M | 0.39M | -2.1% |
| lit/VSComp2010/Problem1-SumMax.dfy:refresh | 3 | 0.39M | 0.38M | -4.3% |
| std/JSON/ByteStrConversion.dfy | 4 | 0.39M | 0.39M | -0.6% |
| lit/patterns/OrPatterns.dfy:refresh | 12 | 0.39M | 0.38M | -1.9% |
| lit/dafny1/MatrixFun.dfy:refresh | 6 | 0.39M | 0.44M | +14.5% |
| lit/hofs/Monads.dfy:refresh | 14 | 0.39M | 0.38M | -0.5% |
| lit/dafny1/Substitution.dfy:refresh | 9 | 0.38M | 0.39M | +1.8% |
| lit/comp/NativeNumbers.dfy:refresh | 25 | 0.38M | 0.37M | -3.3% |
| lit/unicodecharsFalse/comp/NativeNumbers.dfy:refresh | 25 | 0.38M | 0.37M | -3.3% |
| lit/dafny0/ComprehensionsNewSyntax.dfy:pinned | 16 | 0.38M | 0.38M | -0.2% |
| lit/dafny0/Comprehensions.dfy:pinned | 16 | 0.38M | 0.38M | -0.3% |
| lit/examples/induction-principle-code/Interp.dfy:refresh | 3 | 0.38M | 0.37M | -0.8% |
| lit/hofs/ReadsReadsOnMethods.dfy:refresh | 20 | 0.37M | 0.36M | -1.3% |
| lit/dafny3/Paulson.dfy:refresh | 12 | 0.37M | 0.37M | +1.5% |
| lit/traits/NonReferenceTraitsVerify.dfy:refresh | 42 | 0.36M | 0.36M | -1.3% |
| lit/blogposts/TestGenerationNoInliningEnumerativeDefinitions.dfy:refresh | 5 | 0.36M | 0.36M | +1.4% |
| lit/hofs/ReadsReads.dfy:refresh | 16 | 0.36M | 0.35M | -1.7% |
| lit/dafny3/Inc.dfy:refresh | 8 | 0.35M | 0.35M | +0.5% |
| lit/comp/Iterators.dfy:refresh | 8 | 0.34M | 0.34M | +0.3% |
| lit/dafny0/TypeParameters.dfy:refresh | 30 | 0.34M | 0.33M | -1.6% |
| lit/dafny0/BoundedPolymorphismVerification.dfy:pinned | 33 | 0.33M | 0.33M | -1.3% |
| lit/dafny0/TypeConversionsCompile.dfy:refresh | 8 | 0.33M | 0.33M | +0.6% |
| lit/comp/MoreAutoInit.dfy:refresh | 37 | 0.33M | 0.32M | -4.0% |
| lit/dafny0/Strings.dfy:refresh | 11 | 0.33M | 0.33M | -1.0% |
| lit/VSI-Benchmarks/b2.dfy:refresh | 5 | 0.33M | 0.33M | -0.0% |
| lit/traits/TraitOverride2.dfy:refresh | 18 | 0.32M | 0.32M | +0.0% |
| lit/dafny0/Datatypes.dfy:refresh | 28 | 0.32M | 0.32M | -0.8% |
| lit/dafny0/Newtypes.dfy:refresh | 43 | 0.32M | 0.30M | -5.2% |
| lit/lambdas/StateMonad.dfy:pinned | 3 | 0.31M | 0.31M | -0.5% |
| lit/traits/GeneralTraitsVerify.dfy:pinned | 52 | 0.31M | 0.30M | -4.6% |
| lit/c++/sets.dfy:refresh | 8 | 0.31M | 0.30M | -0.7% |
| lit/dafny0/DefiniteAssignment.dfy:refresh | 14 | 0.31M | 0.35M | +12.8% |
| lit/dafny0/SplitExpr.dfy:refresh | 8 | 0.31M | 0.38M | +25.2% |
| lit/traits/GeneralTraitsCompile.dfy:pinned | 48 | 0.30M | 0.29M | -4.7% |
| lit/git-issues/git-issue-977.dfy:pinned | 20 | 0.30M | 0.29M | -3.2% |
| lit/comp/AutoInit.dfy:refresh | 16 | 0.30M | 0.30M | -0.4% |
| lit/concurrency/04-LeastGreatest.dfy:refresh | 18 | 0.30M | 0.31M | +3.5% |
| lit/comp/EuclideanDivision.dfy:refresh | 11 | 0.30M | 0.29M | -2.0% |
| lit/dafny0/SeqSlice.dfy:refresh | 6 | 0.30M | 0.29M | -1.9% |
| lit/dafny0/Compilation.dfy:refresh | 36 | 0.29M | 0.28M | -4.5% |
| lit/dafny0/Refinement.dfy:refresh | 28 | 0.29M | 0.30M | +1.7% |
| libraries/Collections/Maps/Maps.dfy | 13 | 0.28M | 0.30M | +4.0% |
| libraries/dafny/Collections/Maps.dfy | 13 | 0.28M | 0.30M | +4.0% |
| lit/dafny4/McCarthy91.dfy:refresh | 5 | 0.28M | 0.33M | +17.0% |
| std/Collections/Map.dfy | 13 | 0.28M | 0.28M | +1.3% |
| lit/dafny0/OlderVerification.dfy:pinned | 19 | 0.28M | 0.27M | -0.6% |
| lit/examples/induction-principle-code/AST.dfy:refresh | 3 | 0.27M | 0.27M | -0.7% |
| lit/git-issues/git-issue-930.dfy:refresh | 14 | 0.27M | 0.27M | -1.1% |
| lit/dafny0/TypeAdjustments.dfy:pinned | 19 | 0.27M | 0.26M | -1.9% |
| std/Arithmetic/Internal/MulInternals.dfy | 10 | 0.26M | 0.25M | -4.7% |
| lit/dafny3/SetIterations.dfy:refresh | 8 | 0.26M | 0.26M | -1.1% |
| lit/comp/ComprehensionsNewSyntax.dfy:refresh | 10 | 0.26M | 0.26M | -0.8% |
| lit/dafny4/BinarySearch.dfy:refresh | 6 | 0.26M | 0.25M | -4.4% |
| lit/dafny0/DTypes.dfy:refresh | 20 | 0.25M | 0.25M | -1.4% |
| lit/dafny0/ForallStmt.dfy:refresh | 19 | 0.25M | 0.25M | -0.7% |
| libraries/NonlinearArithmetic/Internals/MulInternals.dfy | 9 | 0.25M | 0.25M | -2.2% |
| libraries/dafny/NonlinearArithmetic/Internals/MulInternals.dfy | 9 | 0.25M | 0.25M | -2.2% |
| lit/dafny0/SeqFromArray.dfy:refresh | 10 | 0.25M | 0.26M | +5.1% |
| lit/dafny0/LabelsOldAt.dfy:refresh | 28 | 0.25M | 0.27M | +9.0% |
| lit/dafny0/BoundedPolymorphismCompilation.dfy:pinned | 27 | 0.25M | 0.24M | -1.7% |
| lit/dafny3/InductionVsCoinduction.dfy:refresh | 12 | 0.25M | 0.25M | -0.6% |
| lit/dafny0/LoopModifies.dfy:refresh | 21 | 0.24M | 0.24M | -2.1% |
| lit/dafny0/Twostate-Functions.dfy:refresh | 18 | 0.24M | 0.25M | +2.2% |
| lit/comp/ErasableTypeWrappers.dfy:pinned | 13 | 0.24M | 0.24M | -0.9% |
| lit/dafny4/Bug140.dfy:refresh | 8 | 0.24M | 0.24M | +1.0% |
| lit/dafny0/Compilation.legacy.dfy:pinned | 31 | 0.23M | 0.22M | -5.2% |
| lit/dafny3/SimpleCoinduction.dfy:refresh | 13 | 0.23M | 0.23M | -0.9% |
| lit/dafny0/PrintEffects.dfy:refresh | 13 | 0.23M | 0.23M | -0.0% |
| lit/dafny0/Reads.dfy:refresh | 20 | 0.23M | 0.23M | +1.5% |
| lit/dafny0/ForallCompilation.legacy.dfy:refresh | 14 | 0.23M | 0.24M | +2.3% |
| lit/dafny0/ForallCompilationNewSyntax.dfy:refresh | 14 | 0.23M | 0.24M | +2.3% |
| lit/dafny1/FindZero.dfy:refresh | 8 | 0.23M | 0.21M | -6.6% |
| lit/dafny0/fun-with-slices.dfy:refresh | 2 | 0.23M | 0.27M | +21.1% |
| lit/git-issues/git-issue-3868.dfy:refresh | 16 | 0.23M | 0.22M | -0.3% |
| lit/git-issues/git-issue-2500.dfy:refresh | 25 | 0.22M | 0.22M | -2.2% |
| std/Ordinal.dfy | 10 | 0.22M | 0.21M | -4.9% |
| lit/dafny1/SumOfCubes.dfy:refresh | 17 | 0.22M | 0.21M | -4.6% |
| lit/c++/class.dfy:refresh | 16 | 0.22M | 0.22M | +1.4% |
| lit/dafny4/MonadicLaws.dfy:refresh | 8 | 0.22M | 0.22M | -0.5% |
| lit/dafny3/Zip.dfy:refresh | 8 | 0.22M | 0.22M | -0.5% |
| lit/git-issues/git-issue-1989.dfy:refresh | 17 | 0.22M | 0.22M | +0.5% |
| std/Collections/Imap.dfy | 11 | 0.21M | 0.21M | -1.5% |
| libraries/Collections/Maps/Imaps.dfy | 11 | 0.21M | 0.21M | -2.2% |
| libraries/dafny/Collections/Imaps.dfy | 11 | 0.21M | 0.21M | -2.2% |
| lit/dafny0/Predicates.dfy:refresh | 16 | 0.21M | 0.21M | +2.1% |
| libraries/NonlinearArithmetic/Power2.dfy | 8 | 0.21M | 0.20M | -5.4% |
| libraries/dafny/NonlinearArithmetic/Power2.dfy | 8 | 0.21M | 0.20M | -5.4% |
| lit/referrers/memorylocations.dfy:pinned | 15 | 0.20M | 0.21M | +1.5% |
| lit/dafny0/AutoReq.dfy:refresh | 30 | 0.20M | 0.20M | -3.2% |
| lit/VSComp2010/Problem2-Invert.dfy:refresh | 3 | 0.20M | 0.20M | +1.2% |
| lit/comp/Class.dfy:refresh | 18 | 0.20M | 0.20M | -1.7% |
| lit/dafny0/ArrayElementInit.dfy:refresh | 9 | 0.20M | 0.19M | -2.4% |
| lit/dafny0/ArrayElementInitERR.dfy:refresh | 9 | 0.20M | 0.19M | -2.4% |
| lit/comp/ByMethodCompilation.dfy:refresh | 13 | 0.20M | 0.18M | -6.5% |
| lit/dafny0/DividedConstructors.dfy:refresh | 16 | 0.19M | 0.21M | +9.8% |
| lit/dafny1/TerminationDemos.dfy:refresh | 12 | 0.19M | 0.19M | -1.9% |
| lit/comp/Calls.dfy:refresh | 6 | 0.19M | 0.19M | -1.1% |
| lit/dafny0/Fp32ClassificationPredicates.dfy:refresh | 15 | 0.19M | 0.19M | -0.8% |
| lit/dafny0/DirtyLoops.dfy:refresh | 22 | 0.19M | 0.19M | -1.5% |
| libraries/dafny/Collections/Arrays.dfy | 2 | 0.19M | 0.18M | -3.8% |
| std/Arithmetic/Power2.dfy | 8 | 0.19M | 0.17M | -6.9% |
| lit/dafny4/Bug49.dfy:refresh | 13 | 0.19M | 0.18M | -0.9% |
| lit/triggers/some-terms-do-not-look-like-the-triggers-they-match.dfy:refresh | 4 | 0.19M | 0.20M | +5.9% |
| lit/c++/seqs.dfy:refresh | 12 | 0.19M | 0.18M | -2.4% |
| dafnybench/verification-class_tmp_tmpz9ik148s_2022_chapter05-distributed-state-machines_exercises_UtilitiesLibrary.dfy | 11 | 0.18M | 0.18M | -0.1% |
| lit/dafny0/TypeMembers.dfy:refresh | 29 | 0.18M | 0.17M | -7.9% |
| lit/dafny4/git-issue245.dfy:refresh | 24 | 0.18M | 0.18M | -2.3% |
| std/Collections/Array.dfy | 2 | 0.18M | 0.18M | +1.6% |
| lit/dafny0/PrecedenceLinter.dfy:refresh | 17 | 0.18M | 0.17M | -3.4% |
| libraries/Collections/Arrays/BinarySearch.dfy | 2 | 0.18M | 0.18M | +1.5% |
| lit/dafny0/ConcurrentAttribute.dfy:refresh | 15 | 0.18M | 0.18M | -1.3% |
| lit/dafny0/NonZeroInitializationCompile.dfy:refresh | 15 | 0.18M | 0.17M | -1.7% |
| lit/comp/ForLoops-Compilation.dfy:refresh | 23 | 0.18M | 0.16M | -6.9% |
| lit/dafny2/Intervals.dfy:refresh | 4 | 0.17M | 0.18M | +2.1% |
| lit/comp/StaticMembersOfGenericTypes.dfy:refresh | 9 | 0.17M | 0.17M | -1.5% |
| lit/comp/TypeParams.dfy:refresh | 16 | 0.17M | 0.17M | -2.3% |
| std/Parsers/String/StringBuilders.dfy | 4 | 0.17M | 0.18M | +4.5% |
| lit/dafny0/Bitvectors.dfy:refresh | 11 | 0.17M | 0.17M | -2.4% |
| lit/hofs/WhileLoop.dfy:refresh | 4 | 0.17M | 0.13M | -21.0% |
| lit/traits/TraitOverride1.dfy:refresh | 29 | 0.17M | 0.16M | -2.4% |
| lit/git-issues/git-issue-276c.dfy:refresh | 18 | 0.16M | 0.16M | -3.5% |
| lit/git-issues/git-issue-19b.dfy:refresh | 21 | 0.16M | 0.17M | +1.6% |
| lit/dafny4/git-issue167.dfy:refresh | 4 | 0.16M | 0.16M | -1.1% |
| lit/vstte2012/Two-Way-Sort.dfy:refresh | 4 | 0.16M | 0.18M | +10.2% |
| lit/dafny4/NatList.dfy:refresh | 11 | 0.16M | 0.16M | -1.3% |
| lit/dafny0/DiscoverBounds.dfy:refresh | 10 | 0.16M | 0.16M | -0.9% |
| lit/dafnydoc/doc1/TestDafnyDoc.dfy:refresh | 16 | 0.16M | 0.15M | -3.3% |
| lit/git-issues/git-issue-506.dfy:refresh | 2 | 0.16M | 0.16M | -0.3% |
| lit/git-issues/git-issue-446b.dfy:refresh | 10 | 0.16M | 0.16M | -0.8% |
| lit/comp/Datatype.dfy:refresh | 13 | 0.16M | 0.15M | -3.1% |
| lit/logger/ProofDependencyLogging.dfy:refresh | 32 | 0.16M | 0.14M | -8.2% |
| lit/logger/ProofDependencyWarnings.dfy:refresh | 32 | 0.16M | 0.14M | -8.2% |
| lit/dafny0/Fp64ClassificationPredicates.dfy:refresh | 15 | 0.16M | 0.15M | -2.9% |
| lit/dafny0/CoPrefix.dfy:refresh | 13 | 0.16M | 0.15M | -3.9% |
| lit/git-issues/git-issue-446a.dfy:refresh | 9 | 0.15M | 0.15M | -0.9% |
| lit/dafny0/Constant.dfy:refresh | 17 | 0.15M | 0.14M | -6.1% |
| lit/ghost/Comp.dfy:refresh | 7 | 0.15M | 0.15M | -1.6% |
| lit/comp/firstSteps/6_Calls-VariableCapture.dfy:refresh | 4 | 0.15M | 0.15M | -0.8% |
| std/Frames.dfy | 9 | 0.15M | 0.15M | -0.2% |
| lit/dafny0/PrefixTypeSubst.dfy:refresh | 12 | 0.15M | 0.14M | -4.0% |
| lit/dafny0/OpaqueTypeWithMembers.dfy:refresh | 17 | 0.15M | 0.14M | -4.0% |
| lit/hofs/Frame.dfy:refresh | 6 | 0.15M | 0.15M | -1.2% |
| lit/dafny0/InSetComprehension.dfy:refresh | 8 | 0.15M | 0.15M | -0.4% |
| lit/c++/arrays.dfy:refresh | 9 | 0.14M | 0.14M | -3.3% |
| lit/git-issues/git-issue-897a.dfy:refresh | 1 | 0.14M | 0.13M | -6.4% |
| lit/git-issues/git-issue-817.dfy:pinned | 7 | 0.14M | 0.14M | -1.1% |
| libraries/JSON/Errors.dfy | 2 | 0.14M | 0.14M | -0.4% |
| lit/dafny1/TreeDatatype.dfy:refresh | 10 | 0.14M | 0.14M | -1.3% |
| lit/dafny0/Corecursion.dfy:pinned | 14 | 0.14M | 0.14M | -1.0% |
| lit/dafny4/git-issue63.dfy:refresh | 6 | 0.14M | 0.14M | -0.7% |
| lit/dafny1/ListCopy.dfy:refresh | 2 | 0.14M | 0.14M | -1.4% |
| lit/git-issues/git-issue-446.dfy:refresh | 9 | 0.14M | 0.14M | -0.8% |
| lit/dafny1/UltraFilter.dfy:refresh | 6 | 0.14M | 0.13M | -1.6% |
| lit/comp/BuiltIns.dfy:refresh | 3 | 0.13M | 0.13M | -0.6% |
| lit/dafny0/RankPos.dfy:refresh | 11 | 0.13M | 0.13M | -1.0% |
| lit/dafny0/GeneralNewtypeMemberVerify.dfy:pinned | 19 | 0.13M | 0.13M | -4.4% |
| lit/dafny3/WideTrees.dfy:refresh | 7 | 0.13M | 0.13M | -0.8% |
| lit/lambdas/LitInt.dfy:refresh | 2 | 0.13M | 0.18M | +37.8% |
| std/Collections/Multiset.dfy | 2 | 0.13M | 0.13M | +1.3% |
| lit/git-issues/git-issue-283.dfy:refresh | 9 | 0.13M | 0.13M | -0.8% |
| lit/dafny0/OpaqueFunctions.dfy:refresh | 18 | 0.13M | 0.13M | +1.9% |
| lit/git-issues/git-issue-1130.dfy:refresh | 10 | 0.13M | 0.13M | -1.2% |
| lit/traits/NonReferenceTraitsCompile.dfy:refresh | 11 | 0.13M | 0.12M | -1.9% |
| lit/git-issues/git-issue-1619.dfy:refresh | 18 | 0.13M | 0.12M | -4.7% |
| lit/git-issues/git-issue-1094.dfy:refresh | 12 | 0.13M | 0.13M | -0.8% |
| lit/git-issues/git-issue-2013.dfy:pinned | 12 | 0.13M | 0.12M | -1.8% |
| lit/patterns/PatternMatching.dfy:refresh | 9 | 0.13M | 0.12M | -5.4% |
| lit/dafny2/SegmentSum.dfy:refresh | 3 | 0.13M | 0.16M | +29.3% |
| lit/dafny0/Char.dfy:refresh | 8 | 0.13M | 0.13M | +1.7% |
| lit/git-issues/git-issue-2927.dfy:refresh | 6 | 0.12M | 0.12M | -1.2% |
| lit/dafny4/git-issue133.dfy:refresh | 6 | 0.12M | 0.12M | -1.0% |
| lit/comp/rust/externalclasses.dfy:refresh | 8 | 0.12M | 0.12M | -2.6% |
| lit/comp/Variance.dfy:refresh | 13 | 0.12M | 0.12M | -1.2% |
| lit/dafny0/Wellfounded.dfy:refresh | 3 | 0.12M | 0.12M | -0.5% |
| lit/dafny4/Bug68.dfy:refresh | 8 | 0.12M | 0.12M | -0.8% |
| lit/dafny0/NestedMatch.dfy:refresh | 12 | 0.12M | 0.12M | -3.2% |
| lit/comp/rust/mapsubsets.dfy:pinned | 8 | 0.12M | 0.12M | -2.2% |
| lit/comp/BranchCoverage.dfy:refresh | 7 | 0.12M | 0.12M | -4.2% |
| lit/dafny3/EWD-1062.dfy:refresh | 7 | 0.12M | 0.12M | -2.0% |
| std/BoundedInts.dfy | 32 | 0.12M | 0.10M | -16.2% |
| lit/comp/rust/traits-datatypes.dfy:pinned | 12 | 0.12M | 0.12M | -2.6% |
| lit/hofs/Simple.dfy:refresh | 5 | 0.12M | 0.12M | -1.1% |
| lit/dafny4/Bug159.dfy:refresh | 8 | 0.12M | 0.12M | -1.0% |
| lit/dafny0/StatementExpressions.dfy:refresh | 20 | 0.12M | 0.11M | -10.0% |
| lit/dafny1/Celebrity.dfy:refresh | 5 | 0.12M | 0.12M | -0.3% |
| lit/dafny0/ExtremeReads.dfy:refresh | 10 | 0.12M | 0.12M | +1.5% |
| lit/dafny0/LabeledAsserts.dfy:refresh | 11 | 0.11M | 0.12M | +4.7% |
| lit/hofs/Fold.dfy:refresh | 3 | 0.11M | 0.11M | -2.5% |
| lit/comp/DowncastClone.dfy:pinned | 7 | 0.11M | 0.11M | -0.8% |
| lit/ast/reveal/revealFunctions.dfy:pinned | 25 | 0.11M | 0.10M | -7.9% |
| lit/exceptions/Exceptions1Expressions.dfy:refresh | 5 | 0.11M | 0.11M | -0.3% |
| lit/git-issues/git-issue-405.dfy:refresh | 6 | 0.11M | 0.11M | -0.7% |
| lit/triggers/InductionWithoutTriggers.dfy:refresh | 12 | 0.11M | 0.11M | -5.2% |
| std/Arithmetic/Logarithm.dfy | 11 | 0.11M | 0.11M | -3.9% |
| libraries/NonlinearArithmetic/Logarithm.dfy | 11 | 0.11M | 0.10M | -4.9% |
| lit/hofs/Requires.dfy:refresh | 10 | 0.11M | 0.10M | -4.8% |
| lit/comp/firstSteps/7_Arrays.dfy:refresh | 7 | 0.11M | 0.10M | -2.3% |
| lit/dafny0/RuntimeTypeTests0.dfy:refresh | 9 | 0.11M | 0.11M | -1.0% |
| lit/git-issues/git-issue-1256.dfy:refresh | 15 | 0.11M | 0.10M | -4.2% |
| lit/git-issues/git-issue-936.dfy:refresh | 9 | 0.11M | 0.11M | -0.9% |
| lit/dafny0/AllLiteralsAxiom.dfy:refresh | 4 | 0.11M | 0.10M | -2.2% |
| lit/hofs/Renaming.dfy:refresh | 4 | 0.11M | 0.11M | -0.2% |
| lit/dafny0/NonZeroInitialization.dfy:refresh | 12 | 0.10M | 0.10M | -5.1% |
| lit/git-issues/git-issue-2672.dfy:refresh | 5 | 0.10M | 0.10M | -1.8% |
| lit/verification/nonLinearArithmetic.dfy:refresh | 16 | 0.10M | 0.09M | -9.4% |
| libraries/BoundedInts.dfy | 29 | 0.10M | 0.09M | -16.4% |
| lit/dafny0/Fp32SpecialValues.dfy:refresh | 12 | 0.10M | 0.10M | -2.6% |
| lit/git-issues/git-issue-6366.dfy:refresh | 4 | 0.10M | 0.10M | -0.7% |
| lit/dafny0/SubsetTypes.dfy:pinned | 13 | 0.10M | 0.10M | -7.2% |
| lit/git-issues/git-issue-1676.dfy:refresh | 20 | 0.10M | 0.09M | -9.1% |
| lit/comp/AsIs-Compile.dfy:refresh | 6 | 0.10M | 0.10M | -1.8% |
| lit/dafny1/pow2.dfy:refresh | 7 | 0.10M | 0.10M | -3.2% |
| lit/dafny0/SharedDestructorsCompile.dfy:refresh | 3 | 0.10M | 0.10M | -1.1% |
| lit/ast/reveal/focus.dfy:pinned | 29 | 0.10M | 0.08M | -15.7% |
| lit/ast/reveal/revealInBlock.dfy:pinned | 20 | 0.10M | 0.09M | -8.0% |
| lit/dafny0/GeneralNewtypeMemberCompile.dfy:pinned | 15 | 0.10M | 0.09M | -4.7% |
| lit/hofs/Apply.dfy:refresh | 7 | 0.10M | 0.10M | +0.9% |
| lit/examples/induction-principle-code/Utils.dfy:refresh | 2 | 0.10M | 0.11M | +9.7% |
| lit/c++/datatypes.dfy:refresh | 12 | 0.10M | 0.09M | -5.5% |
| libraries/Relations.dfy | 3 | 0.10M | 0.10M | +2.4% |
| lit/git-issues/git-issue-4684.dfy:refresh | 4 | 0.10M | 0.10M | +0.6% |
| lit/traits/TraitResolution0.dfy:refresh | 8 | 0.10M | 0.10M | -0.9% |
| lit/git-issues/git-issue-663.dfy:refresh | 23 | 0.10M | 0.09M | -9.8% |
| lit/git-issues/git-issue-2380.dfy:refresh | 2 | 0.10M | 0.09M | -1.2% |
| lit/comp/rust/datatypes.dfy:refresh | 5 | 0.10M | 0.09M | -2.3% |
| lit/git-issues/git-issue-817a.dfy:pinned | 5 | 0.10M | 0.09M | -1.0% |
| lit/dafny0/ModifyStmt.dfy:refresh | 11 | 0.09M | 0.10M | +7.2% |
| lit/git-issues/git-issue-966.dfy:refresh | 6 | 0.09M | 0.09M | -0.9% |
| lit/git-issues/git-issue-2299.dfy:refresh | 7 | 0.09M | 0.10M | +6.2% |
| lit/git-issues/git-issue-2429.dfy:pinned | 7 | 0.09M | 0.09M | -0.9% |
| lit/dafny0/OnDemandResolutionOrdering.dfy:pinned | 12 | 0.09M | 0.09M | -4.2% |
| lit/comp/Extern.dfy:refresh | 7 | 0.09M | 0.09M | -3.0% |
| lit/hofs/Compilation.dfy:refresh | 2 | 0.09M | 0.09M | -3.6% |
| lit/git-issues/git-issue-3883.dfy:refresh | 11 | 0.09M | 0.09M | -2.9% |
| lit/ast/reveal/revealInExpression.dfy:pinned | 15 | 0.09M | 0.08M | -8.3% |
| lit/dafny0/ByMethod.dfy:refresh | 15 | 0.09M | 0.08M | -9.4% |
| lit/triggers/induction-triggers.dfy:refresh | 17 | 0.09M | 0.08M | -10.3% |
| lit/dafny0/Backticks.dfy:refresh | 12 | 0.09M | 0.10M | +10.5% |
| lit/dafny4/Circ.dfy:refresh | 3 | 0.09M | 0.09M | +1.8% |
| lit/dafny4/git-issue41.dfy:refresh | 9 | 0.09M | 0.09M | -1.7% |
| lit/proof-obligation-desc/read-frame-subset.dfy:refresh | 6 | 0.09M | 0.09M | -0.5% |
| lit/git-issues/git-issue-276v.dfy:refresh | 18 | 0.09M | 0.08M | -10.6% |
| lit/git-issues/git-issue-817c.dfy:pinned | 5 | 0.09M | 0.09M | -1.5% |
| lit/dafny0/Fp64SpecialValues.dfy:refresh | 12 | 0.09M | 0.08M | -3.0% |
| std/JSON/Errors.dfy | 1 | 0.09M | 0.09M | -0.3% |
| std/Unicode/UnicodeStrings.dfy | 2 | 0.09M | 0.09M | -0.6% |
| lit/Landin/Knot18.dfy:refresh | 4 | 0.09M | 0.09M | -0.6% |
| lit/comp/separate-compilation/usesTimesTwo.dfy:refresh | 5 | 0.09M | 0.08M | -1.7% |
| lit/dafny4/LeastGreatest.dfy:refresh | 9 | 0.09M | 0.07M | -13.7% |
| lit/dafny0/ReturnTests.dfy:refresh | 10 | 0.09M | 0.09M | +0.5% |
| lit/comp/rust/bymethod.dfy:refresh | 5 | 0.08M | 0.08M | -5.3% |
| lit/referrers/localsmemorylocation.dfy:pinned | 6 | 0.08M | 0.08M | +0.1% |
| lit/git-issues/git-issue-1875.dfy:refresh | 5 | 0.08M | 0.08M | -0.9% |
| lit/dafny4/Bug170.dfy:refresh | 5 | 0.08M | 0.08M | -3.1% |
| lit/dafny0/MultiDimArray.dfy:refresh | 5 | 0.08M | 0.09M | +3.3% |
| lit/git-issues/git-issue-697b.dfy:refresh | 3 | 0.08M | 0.09M | +2.6% |
| libraries/dafny/Relations.dfy | 3 | 0.08M | 0.08M | -0.7% |
| std/Functions.dfy | 3 | 0.08M | 0.08M | -0.7% |
| libraries/Unicode/UnicodeStrings.dfy | 2 | 0.08M | 0.08M | -0.3% |
| lit/git-issues/git-issue-1163.dfy:refresh | 2 | 0.08M | 0.08M | -0.7% |
| lit/dafny4/Bug92.dfy:refresh | 9 | 0.08M | 0.08M | -0.2% |
| lit/dafny2/COST-verif-comp-2011-1-MaxArray.dfy:refresh | 2 | 0.08M | 0.08M | -5.9% |
| lit/dafny4/Bug151.dfy:refresh | 6 | 0.08M | 0.08M | -1.1% |
| lit/comp/rust/arrays.dfy:refresh | 4 | 0.08M | 0.08M | -1.6% |
| lit/dafny4/git-issue195.dfy:refresh | 4 | 0.08M | 0.08M | -0.7% |
| lit/dafny3/Dijkstra.dfy:refresh | 7 | 0.08M | 0.08M | -5.4% |
| lit/exceptions/NatOutcome.dfy:refresh | 11 | 0.08M | 0.08M | -1.5% |
| lit/git-issues/git-issue-321.dfy:refresh | 3 | 0.08M | 0.08M | -0.7% |
| lit/dafny0/Fp32EqualityErrors.dfy:refresh | 15 | 0.08M | 0.08M | -4.1% |
| lit/git-issues/git-issue-2301.dfy:refresh | 3 | 0.08M | 0.09M | +17.5% |
| lit/c++/bit-vectors.dfy:refresh | 6 | 0.08M | 0.08M | -3.9% |
| lit/dafny4/git-issue70.dfy:refresh | 3 | 0.08M | 0.07M | -6.9% |
| lit/dafny0/ISets.dfy:refresh | 2 | 0.08M | 0.07M | -4.7% |
| lit/git-issues/git-issue-3995.dfy:refresh | 13 | 0.08M | 0.07M | -3.7% |
| lit/dafny1/KatzManna.dfy:refresh | 4 | 0.08M | 0.08M | +8.7% |
| lit/logger/FunctionHidingRefactoring.dfy:pinned | 12 | 0.08M | 0.07M | -9.5% |
| dafnybench/iron-sync_tmp_tmps49o3tyz_lib_Base_MapRemove.dfy | 1 | 0.08M | 0.08M | -0.6% |
| lit/git-issues/git-issue-755.dfy:refresh | 5 | 0.08M | 0.07M | -0.8% |
| lit/dafny4/Bug75.dfy:refresh | 9 | 0.08M | 0.07M | -3.1% |
| lit/dafny4/Bug54.dfy:refresh | 4 | 0.08M | 0.07M | -1.1% |
| lit/hofs/ArrowTypeOptimizations.dfy:refresh | 10 | 0.07M | 0.07M | -2.5% |
| lit/dafny0/FunctionSpecifications.dfy:refresh | 10 | 0.07M | 0.07M | -7.7% |
| lit/git-issues/git-issue-2690.dfy:refresh | 3 | 0.07M | 0.07M | -0.5% |
| lit/comp/rust/continue.dfy:refresh | 1 | 0.07M | 0.07M | -0.3% |
| libraries/Collections/Sets/Isets.dfy | 3 | 0.07M | 0.07M | -1.9% |
| libraries/dafny/Collections/Isets.dfy | 3 | 0.07M | 0.07M | -1.9% |
| lit/comp/firstSteps/7_Dt_Algebraic.dfy:refresh | 7 | 0.07M | 0.07M | -3.3% |
| lit/dafny4/Issue09.dfy:refresh | 2 | 0.07M | 0.08M | +3.4% |
| lit/git-issues/git-issue-784.dfy:refresh | 4 | 0.07M | 0.07M | -10.6% |
| lit/git-issues/git-issue-5017c.dfy:pinned | 11 | 0.07M | 0.07M | -1.8% |
| lit/git-issues/git-issue-3734.dfy:refresh | 4 | 0.07M | 0.07M | -2.9% |
| std/Collections/Iset.dfy | 3 | 0.07M | 0.07M | -0.1% |
| lit/git-issues/git-issue-1958.dfy:pinned | 6 | 0.07M | 0.07M | -4.0% |
| lit/git-issues/git-issue-276.dfy:refresh | 18 | 0.07M | 0.06M | -13.6% |
| lit/dafny0/Fp64EqualityErrors.dfy:refresh | 15 | 0.07M | 0.07M | -4.5% |
| lit/dafny1/Cubes.dfy:refresh | 2 | 0.07M | 0.07M | -0.1% |
| lit/git-issues/git-issue-276r.dfy:pinned | 17 | 0.07M | 0.06M | -16.7% |
| lit/dafny2/TreeFill.dfy:refresh | 3 | 0.07M | 0.07M | +0.2% |
| std/Actions/GenericAction.dfy | 6 | 0.07M | 0.07M | -1.1% |
| lit/git-issues/git-issue-495.dfy:refresh | 10 | 0.07M | 0.07M | -4.8% |
| lit/dafny0/BindingGuards.dfy:refresh | 10 | 0.07M | 0.06M | -7.7% |
| lit/comp/rust/methods.dfy:refresh | 10 | 0.07M | 0.06M | -8.4% |
| lit/git-issues/git-issue-1165.dfy:refresh | 6 | 0.07M | 0.07M | -0.7% |
| lit/git-issues/git-issue-867.dfy:refresh | 4 | 0.07M | 0.07M | -0.5% |
| lit/git-issues/git-issue-5017a.dfy:refresh | 14 | 0.07M | 0.06M | -8.1% |
| lit/git-issues/git-issue-1113.dfy:refresh | 7 | 0.07M | 0.07M | -1.2% |
| lit/verification/outOfResourceAndIsolateAssertions.dfy:refresh | 16 | 0.07M | 0.06M | -13.1% |
| lit/comp/rust/classes.dfy:refresh | 3 | 0.07M | 0.07M | +0.5% |
| lit/git-issues/git-issue-364.dfy:refresh | 4 | 0.07M | 0.07M | -0.7% |
| lit/git-issues/git-issue-731.dfy:refresh | 3 | 0.07M | 0.07M | -1.1% |
| lit/dafny0/ChainingDisjointTests.dfy:refresh | 4 | 0.07M | 0.06M | -10.1% |
| lit/ast/redeclareBodyRun.dfy:pinned | 10 | 0.07M | 0.06M | -5.1% |
| lit/dafny0/AsIsAgain.dfy:refresh | 7 | 0.07M | 0.06M | -3.3% |
| lit/exports/ExportInductivePredicate.dfy:refresh | 8 | 0.07M | 0.05M | -19.3% |
| lit/traits/TraitsDecreases.dfy:refresh | 12 | 0.07M | 0.06M | -1.9% |
| lit/dafny0/UnfoldingPerformance.dfy:refresh | 4 | 0.07M | 0.07M | +3.7% |
| lit/dafny4/git-issue158.dfy:refresh | 4 | 0.07M | 0.06M | -1.7% |
| lit/git-issues/git-issue-1212.dfy:refresh | 5 | 0.07M | 0.06M | -1.3% |
| lit/git-issues/git-issue-276a.dfy:refresh | 15 | 0.06M | 0.06M | -12.2% |
| lit/comp/rust/array2d.dfy:refresh | 2 | 0.06M | 0.06M | -2.0% |
| lit/dafny4/Regression19.dfy:refresh | 3 | 0.06M | 0.06M | -1.2% |
| lit/git-issues/git-issue-5136.dfy:pinned | 8 | 0.06M | 0.07M | +3.0% |
| lit/dafny4/Bug91.dfy:refresh | 5 | 0.06M | 0.06M | -0.8% |
| lit/dafny0/DatatypeUpdate.dfy:pinned | 5 | 0.06M | 0.06M | -3.1% |
| lit/dafny0/Definedness.dfy:refresh | 9 | 0.06M | 0.06M | +3.2% |
| lit/dafny0/Deprecation.dfy:refresh | 7 | 0.06M | 0.06M | -0.4% |
| lit/dafny0/RealCompare.dfy:refresh | 10 | 0.06M | 0.06M | -10.0% |
| lit/dafny0/GhostAllocations.dfy:refresh | 6 | 0.06M | 0.06M | +5.6% |
| lit/git-issues/git-issue-1604b.dfy:refresh | 6 | 0.06M | 0.06M | -4.0% |
| lit/dafny0/Fp32LiteralSyntax.dfy:refresh | 11 | 0.06M | 0.06M | -6.5% |
| lit/comp/rust/subsetconstraints.dfy:refresh | 6 | 0.06M | 0.06M | -4.1% |
| lit/hofs/Lambda.dfy:refresh | 3 | 0.06M | 0.06M | -0.9% |
| lit/git-issues/git-issue-2883.dfy:refresh | 4 | 0.06M | 0.06M | +7.0% |
| lit/at-attributes/at-attributes-acceptable-builtin.dfy:refresh | 16 | 0.06M | 0.05M | -13.0% |
| lit/dafny3/OpaqueTrees.dfy:refresh | 3 | 0.06M | 0.06M | -0.6% |
| lit/git-issues/git-issue-4939a.dfy:pinned | 11 | 0.06M | 0.06M | -2.8% |
| lit/hofs/Classes.dfy:refresh | 4 | 0.06M | 0.06M | +0.8% |
| lit/dafny4/git-issue257.dfy:refresh | 7 | 0.06M | 0.06M | -1.5% |
| lit/git-issues/git-issue-1731.dfy:pinned | 8 | 0.06M | 0.06M | -2.4% |
| lit/dafny0/Modules1.dfy:refresh | 9 | 0.06M | 0.05M | -8.1% |
| lit/git-issues/git-issue-4982.dfy:refresh | 10 | 0.06M | 0.06M | -1.8% |
| lit/c++/ints.dfy:refresh | 15 | 0.06M | 0.05M | -14.3% |
| lit/git-issues/git-issue-4056.dfy:refresh | 3 | 0.06M | 0.06M | -1.0% |
| lit/git-issues/git-issue-2307.dfy:refresh | 16 | 0.06M | 0.05M | -14.4% |
| libraries/dafny/BoundedInts.dfy | 15 | 0.06M | 0.05M | -16.5% |
| lit/dafny4/Regression4.dfy:refresh | 4 | 0.05M | 0.05M | -1.2% |
| lit/dafny0/Fp32Equality.dfy:refresh | 15 | 0.05M | 0.05M | -6.0% |
| lit/proof-obligation-desc/assignment-shrinks.dfy:refresh | 2 | 0.05M | 0.05M | +1.8% |
| lit/git-issues/git-issue-2693.dfy:refresh | 6 | 0.05M | 0.06M | +9.5% |
| lit/c++/functions.dfy:refresh | 7 | 0.05M | 0.05M | -5.0% |
| lit/git-issues/git-issue-697d.dfy:refresh | 4 | 0.05M | 0.05M | -2.5% |
| lit/dafny0/ContainerRanks.dfy:refresh | 5 | 0.05M | 0.05M | -1.1% |
| lit/examples/maximum.dfy:refresh | 4 | 0.05M | 0.05M | -0.7% |
| lit/exports/FIFO.dfy:refresh | 5 | 0.05M | 0.05M | -0.4% |
| lit/exports/LIFO.dfy:refresh | 5 | 0.05M | 0.05M | -0.4% |
| lit/git-issues/git-issue-3923.dfy:refresh | 8 | 0.05M | 0.05M | -5.7% |
| lit/exceptions/Exceptions1.dfy:refresh | 7 | 0.05M | 0.05M | -2.6% |
| lit/dafny4/git-issue2.dfy:refresh | 1 | 0.05M | 0.05M | -1.6% |
| std/Unicode/UnicodeBase.dfy | 9 | 0.05M | 0.05M | -5.5% |
| lit/triggers/TriggersForSuchThat.dfy:refresh | 11 | 0.05M | 0.05M | -11.1% |
| lit/git-issues/git-issue-5597.dfy:pinned | 5 | 0.05M | 0.05M | -1.0% |
| lit/dafny0/MiscTypeInferenceTests.dfy:pinned | 10 | 0.05M | 0.05M | -2.0% |
| lit/git-issues/git-issue-2947.dfy:refresh | 3 | 0.05M | 0.05M | -0.6% |
| lit/traits/TraitVerify.dfy:refresh | 6 | 0.05M | 0.05M | -2.4% |
| lit/dafny0/NullComparisonWarnings.dfy:refresh | 4 | 0.05M | 0.05M | -0.4% |
| lit/git-issues/git-issue-2216.dfy:refresh | 4 | 0.05M | 0.05M | -0.9% |
| lit/comp/Let.dfy:refresh | 5 | 0.05M | 0.05M | -3.6% |
| lit/logger/ByProofRefactoring.dfy:pinned | 14 | 0.05M | 0.04M | -9.9% |
| lit/git-issues/git-issue-321a.dfy:refresh | 2 | 0.05M | 0.05M | +6.3% |
| lit/comp/rust/elephant.dfy:refresh | 4 | 0.05M | 0.05M | -0.9% |
| lit/triggers/old-is-a-special-case-for-triggers.dfy:refresh | 4 | 0.05M | 0.05M | +0.3% |
| lit/git-issues/git-issue-2852.dfy:refresh | 2 | 0.05M | 0.05M | -0.5% |
| lit/git-issues/git-issue-5644.dfy:refresh | 4 | 0.05M | 0.05M | -2.9% |
| lit/git-issues/git-issue-889a.dfy:refresh | 9 | 0.05M | 0.04M | -9.7% |
| lit/autoRevealDependencies/complicated.dfy:refresh | 5 | 0.05M | 0.04M | -6.3% |
| lit/comp/Various.dfy:refresh | 4 | 0.05M | 0.05M | -2.0% |
| libraries/Unicode/Unicode.dfy | 9 | 0.05M | 0.04M | -6.0% |
| libraries/dafny/Unicode/Unicode.dfy | 9 | 0.05M | 0.04M | -6.0% |
| std/Relations.dfy | 3 | 0.05M | 0.05M | -0.8% |
| lit/dafny0/GhostITECompilation.dfy:refresh | 6 | 0.05M | 0.04M | -5.4% |
| lit/dafny0/Fp64Equality.dfy:refresh | 15 | 0.05M | 0.04M | -7.0% |
| lit/git-issues/git-issue-952.dfy:refresh | 4 | 0.05M | 0.05M | +15.6% |
| lit/git-issues/git-issue-356-errors.dfy:pinned | 11 | 0.05M | 0.04M | -9.3% |
| lit/dafny4/git-issue5.dfy:refresh | 9 | 0.05M | 0.04M | -10.1% |
| lit/proof-obligation-desc/modify-frame-subset.dfy:refresh | 4 | 0.05M | 0.05M | -0.5% |
| lit/git-issues/git-issue-336.dfy:refresh | 4 | 0.05M | 0.05M | -1.2% |
| lit/dafny2/COST-verif-comp-2011-2-MaxTree-datatype.dfy:refresh | 3 | 0.05M | 0.04M | -2.3% |
| lit/dafny2/TuringFactorial.dfy:refresh | 3 | 0.05M | 0.04M | -4.0% |
| lit/dafny4/git-issue104.dfy:refresh | 2 | 0.05M | 0.05M | -1.4% |
| lit/dafny0/TypeInferenceSubsetTypes.dfy:pinned | 6 | 0.05M | 0.05M | +5.0% |
| lit/dafny4/git-issue228.dfy:refresh | 8 | 0.05M | 0.04M | -7.7% |
| lit/git-issues/git-issue-3792.dfy:refresh | 2 | 0.05M | 0.05M | -0.5% |
| lit/git-issues/git-issue-3320.dfy:refresh | 3 | 0.05M | 0.05M | -0.8% |
| lit/dafny2/CalcDefaultMainOperator.dfy:refresh | 9 | 0.05M | 0.04M | -12.6% |
| lit/comp/rust/small/05-coerce.dfy:pinned | 3 | 0.05M | 0.04M | -1.4% |
| lit/dafny0/ComputationsNeg.dfy:refresh | 5 | 0.04M | 0.04M | -6.5% |
| lit/git-issues/git-issue-6164.dfy:refresh | 4 | 0.04M | 0.04M | +0.1% |
| lit/git-issues/git-issue-1158.dfy:refresh | 1 | 0.04M | 0.04M | -1.1% |
| lit/traits/TraitUsingParentMembers.dfy:refresh | 4 | 0.04M | 0.04M | -1.8% |
| lit/comp/rust/small/06-type-bounds.dfy:pinned | 5 | 0.04M | 0.04M | -1.2% |
| lit/dafny4/git-issue96.dfy:refresh | 4 | 0.04M | 0.04M | -1.0% |
| lit/dafny1/InductionOptions.legacy.dfy:refresh | 4 | 0.04M | 0.04M | -3.9% |
| lit/dafny0/GhostAutoInit.dfy:refresh | 7 | 0.04M | 0.04M | -4.9% |
| lit/dafny4/git-issue76.dfy:refresh | 7 | 0.04M | 0.04M | -2.1% |
| libraries/Wrappers.dfy | 5 | 0.04M | 0.04M | -1.3% |
| lit/dafny0/RuntimeTypeTests2.dfy:refresh | 2 | 0.04M | 0.04M | -9.2% |
| lit/dafny4/Bug58.dfy:refresh | 3 | 0.04M | 0.04M | -0.9% |
| lit/git-issues/git-issue-2672-legacy.dfy:pinned | 5 | 0.04M | 0.04M | -4.7% |
| lit/dafny0/NatTypes.dfy:refresh | 6 | 0.04M | 0.04M | -6.3% |
| lit/git-issues/git-issue-953.dfy:refresh | 6 | 0.04M | 0.04M | -0.4% |
| lit/git-issues/git-issue-3873.dfy:refresh | 3 | 0.04M | 0.04M | -1.8% |
| lit/proof-obligation-desc/modifiable.dfy:refresh | 4 | 0.04M | 0.04M | +1.2% |
| lit/git-issues/git-issue-1180b.dfy:refresh | 7 | 0.04M | 0.04M | +0.8% |
| lit/git-issues/git-issue-1423.dfy:refresh | 4 | 0.04M | 0.04M | -1.1% |
| lit/dafny4/Regression9.dfy:refresh | 2 | 0.04M | 0.04M | -0.2% |
| lit/dafny0/Fp64LiteralSyntax.dfy:refresh | 11 | 0.04M | 0.04M | -9.4% |
| libraries/NonlinearArithmetic/Internals/ModInternalsNonlinear.dfy | 10 | 0.04M | 0.04M | -12.8% |
| libraries/dafny/NonlinearArithmetic/Internals/ModInternalsNonlinear.dfy | 10 | 0.04M | 0.04M | -12.8% |
| lit/git-issues/git-issue-1112.dfy:refresh | 5 | 0.04M | 0.04M | -1.2% |
| lit/git-issues/git-issue-532.dfy:refresh | 2 | 0.04M | 0.04M | +5.7% |
| lit/git-issues/git-issue-6090.dfy:refresh | 6 | 0.04M | 0.04M | -4.7% |
| libraries/NonlinearArithmetic/Internals/GeneralInternals.dfy | 1 | 0.04M | 0.04M | -1.9% |
| libraries/dafny/NonlinearArithmetic/Internals/GeneralInternals.dfy | 1 | 0.04M | 0.04M | -1.9% |
| std/Arithmetic/Internal/GeneralInternals.dfy | 1 | 0.04M | 0.04M | -1.9% |
| lit/ast/redeclareBodyVerification.dfy:refresh | 7 | 0.04M | 0.04M | -6.0% |
| lit/git-issues/git-issue-697k.dfy:refresh | 6 | 0.04M | 0.04M | -3.0% |
| lit/git-issues/git-issue-332.dfy:refresh | 6 | 0.04M | 0.04M | +9.9% |
| lit/dafny0/BitvectorsMore.dfy:refresh | 9 | 0.04M | 0.04M | -10.0% |
| lit/dafny2/SmallestMissingNumber-imperative.dfy:refresh | 2 | 0.04M | 0.04M | -0.5% |
| lit/git-issues/git-issue-3059.dfy:refresh | 5 | 0.04M | 0.04M | -1.5% |
| lit/triggers/splitting-triggers-recovers-expressivity.dfy:refresh | 5 | 0.04M | 0.04M | -7.7% |
| dafnybench/Clover_update_map.dfy | 2 | 0.04M | 0.04M | -1.0% |
| lit/comp/NestedArrays.dfy:refresh | 4 | 0.04M | 0.04M | -5.4% |
| lit/git-issues/git-issue-1604.dfy:refresh | 3 | 0.04M | 0.04M | -3.2% |
| lit/dafny1/ListReverse.dfy:refresh | 2 | 0.04M | 0.04M | +2.1% |
| lit/comp/firstSteps/4_Calls-FunctionsValues-Class+NT.dfy:refresh | 3 | 0.04M | 0.04M | -2.9% |
| lit/comp/ExternCopyFromTrait.dfy:refresh | 7 | 0.04M | 0.04M | -3.2% |
| lit/dafny0/CompilationErrors.dfy:refresh | 7 | 0.04M | 0.04M | -6.7% |
| lit/git-issues/git-issue-731b.dfy:refresh | 2 | 0.04M | 0.04M | -0.7% |
| lit/git-issues/git-issue-258.dfy:refresh | 1 | 0.04M | 0.04M | -3.3% |
| lit/git-issues/git-issue-5023.dfy:refresh | 7 | 0.04M | 0.04M | -4.6% |
| lit/git-issues/git-issue-697h.dfy:refresh | 3 | 0.04M | 0.04M | -0.5% |
| libraries/JSON/Utils/Seq.dfy | 4 | 0.04M | 0.04M | -1.1% |
| lit/git-issues/git-issue-817b.dfy:pinned | 4 | 0.04M | 0.04M | +1.5% |
| lit/git-issues/git-issue-4952.dfy:refresh | 6 | 0.04M | 0.04M | -2.6% |
| lit/git-issues/git-issue-1143.dfy:refresh | 3 | 0.04M | 0.04M | -2.0% |
| lit/comp/rust/small/08-not-all-trait-items-implemented.dfy:pinned | 5 | 0.04M | 0.04M | -2.4% |
| lit/dafny4/Bug146.dfy:refresh | 2 | 0.04M | 0.04M | -1.2% |
| lit/dafny0/LegacyConversions.dfy:refresh | 10 | 0.04M | 0.03M | -9.9% |
| lit/dafny4/Regression6.dfy:refresh | 2 | 0.04M | 0.04M | -1.7% |
| lit/dafny0/Unchanged.dfy:refresh | 1 | 0.04M | 0.04M | +4.3% |
| std/Arithmetic/Internal/ModInternalsNonlinear.dfy | 10 | 0.04M | 0.03M | -14.5% |
| lit/dafny0/ImplicitTypeParamPrint.dfy:refresh | 3 | 0.04M | 0.04M | -1.0% |
| std/Arithmetic/Internal/MulInternalsNonlinear.dfy | 6 | 0.04M | 0.03M | -4.6% |
| libraries/FileIO/FileIO.dfy | 3 | 0.04M | 0.04M | -0.9% |
| lit/c++/extern.dfy:refresh | 5 | 0.04M | 0.03M | -6.3% |
| lit/exceptions/VoidOutcome.dfy:refresh | 6 | 0.04M | 0.03M | -1.8% |
| lit/dafny4/Regression12.dfy:refresh | 3 | 0.04M | 0.03M | -1.0% |
| lit/dafny0/PredExpr.dfy:refresh | 6 | 0.04M | 0.03M | -10.4% |
| lit/comp/rust/conversions.dfy:pinned | 5 | 0.03M | 0.03M | -4.2% |
| lit/dafny0/MatchBraces.dfy:refresh | 5 | 0.03M | 0.03M | -7.0% |
| lit/dafny4/git-issue148.dfy:refresh | 3 | 0.03M | 0.03M | -0.8% |
| lit/dafny4/git-issue44.dfy:refresh | 4 | 0.03M | 0.03M | -2.4% |
| lit/dafny0/Fp32Fp64Conversions.dfy:refresh | 9 | 0.03M | 0.03M | -10.0% |
| lit/comp/ExternJavaString.dfy:refresh | 3 | 0.03M | 0.03M | -1.1% |
| lit/unicodecharsFalse/comp/ExternJavaString.dfy:refresh | 3 | 0.03M | 0.03M | -1.1% |
| lit/comp/rust/lambda.dfy:refresh | 3 | 0.03M | 0.03M | -2.1% |
| lit/git-issues/git-issue-1211.dfy:refresh | 1 | 0.03M | 0.03M | -0.3% |
| lit/git-issues/git-issue-1545.dfy:refresh | 5 | 0.03M | 0.03M | -3.1% |
| lit/comp/ExternDLL.dfy:refresh | 7 | 0.03M | 0.03M | -3.5% |
| lit/comp/rust/avoid_soundness_mut.dfy:refresh | 4 | 0.03M | 0.04M | +4.8% |
| lit/dafny0/TypeAntecedents.dfy:refresh | 5 | 0.03M | 0.03M | +0.1% |
| lit/exports/DecreasesExports.dfy:refresh | 6 | 0.03M | 0.03M | -11.3% |
| lit/git-issues/git-issue-697.dfy:refresh | 3 | 0.03M | 0.03M | -3.7% |
| lit/git-issues/git-issue-851.dfy:refresh | 8 | 0.03M | 0.03M | -12.2% |
| lit/git-issues/git-issue-3955.dfy:refresh | 3 | 0.03M | 0.04M | +11.3% |
| libraries/JSON/Utils/Lexers.dfy | 2 | 0.03M | 0.03M | -0.7% |
| std/JSON/Utils/Lexers.dfy | 2 | 0.03M | 0.03M | -0.7% |
| lit/dafny0/GhostDatatypeConstructors-Verification.dfy:refresh | 4 | 0.03M | 0.03M | -4.5% |
| lit/git-issues/git-issue-3868b.dfy:refresh | 3 | 0.03M | 0.03M | -1.5% |
| lit/dafny4/git-issue75.dfy:refresh | 3 | 0.03M | 0.03M | -2.3% |
| lit/dafny4/Bug160.dfy:refresh | 2 | 0.03M | 0.03M | -0.7% |
| lit/logger/CSVLogger.dfy:refresh | 6 | 0.03M | 0.03M | -10.8% |
| lit/logger/MultipleLoggers.dfy:refresh | 6 | 0.03M | 0.03M | -10.8% |
| lit/logger/ResCountXML.dfy:refresh | 6 | 0.03M | 0.03M | -10.8% |
| lit/VSI-Benchmarks/b1.dfy:refresh | 5 | 0.03M | 0.03M | -7.2% |
| lit/metatests/ConsistentWhenSupported.dfy:refresh | 2 | 0.03M | 0.03M | +0.2% |
| lit/comp/rust/classes-relax.dfy:refresh | 3 | 0.03M | 0.03M | +9.9% |
| lit/dafny4/Bug56.dfy:refresh | 2 | 0.03M | 0.03M | -0.7% |
| lit/comp/rust/newtype-set-comp.dfy:refresh | 4 | 0.03M | 0.03M | -4.1% |
| lit/git-issues/git-issue-276b.dfy:refresh | 10 | 0.03M | 0.03M | -17.0% |
| lit/dafny0/RangeCompilation.dfy:refresh | 4 | 0.03M | 0.03M | -5.1% |
| lit/git-issues/git-issue-3719.dfy:refresh | 3 | 0.03M | 0.03M | -4.6% |
| lit/git-issues/git-issue-697e.dfy:pinned | 3 | 0.03M | 0.03M | -3.8% |
| lit/git-issues/git-issue-314.dfy:pinned | 1 | 0.03M | 0.03M | -1.7% |
| libraries/dafny/Wrappers.dfy | 4 | 0.03M | 0.03M | -1.4% |
| std/Wrappers.dfy | 4 | 0.03M | 0.03M | -1.4% |
| lit/git-issues/git-issue-1252.dfy:refresh | 4 | 0.03M | 0.03M | +5.1% |
| lit/c++/tuple.dfy:refresh | 7 | 0.03M | 0.03M | -7.4% |
| lit/git-issues/git-issue-3987.dfy:refresh | 1 | 0.03M | 0.03M | -2.8% |
| libraries/NonlinearArithmetic/Internals/DivInternalsNonlinear.dfy | 8 | 0.03M | 0.02M | -16.7% |
| libraries/dafny/NonlinearArithmetic/Internals/DivInternalsNonlinear.dfy | 8 | 0.03M | 0.02M | -16.7% |
| lit/git-issues/git-issue-5520.dfy:refresh | 8 | 0.03M | 0.03M | -12.1% |
| lit/dafny0/LitTriggers.dfy:refresh | 5 | 0.03M | 0.03M | -9.0% |
| lit/dafny4/Bug144.dfy:refresh | 3 | 0.03M | 0.03M | +3.5% |
| lit/traits/TraitsMultipleInheritance.dfy:refresh | 1 | 0.03M | 0.03M | +10.1% |
| lit/git-issues/git-issue-2726a.dfy:refresh | 1 | 0.03M | 0.03M | -0.5% |
| lit/git-issues/git-issue-4778.dfy:refresh | 2 | 0.03M | 0.03M | -0.9% |
| lit/git-issues/git-issue-4731.dfy:refresh | 3 | 0.03M | 0.03M | -1.2% |
| std/Arithmetic/Internal/DivInternalsNonlinear.dfy | 8 | 0.03M | 0.02M | -14.6% |
| lit/git-issues/git-issue-283d.dfy:refresh | 4 | 0.03M | 0.03M | -6.1% |
| lit/git-issues/git-issue-5647.dfy:refresh | 3 | 0.03M | 0.03M | -3.3% |
| lit/git-issues/git-issue-3411.dfy:refresh | 1 | 0.03M | 0.03M | -0.6% |
| lit/dafny4/git-issue203.dfy:refresh | 3 | 0.03M | 0.03M | -5.7% |
| lit/triggers/function-applications-are-triggers.dfy:refresh | 1 | 0.03M | 0.03M | +1.3% |
| lit/comp/Print.dfy:refresh | 2 | 0.03M | 0.03M | -1.3% |
| lit/dafny0/Skeletons.dfy:refresh | 4 | 0.03M | 0.03M | -8.6% |
| lit/dafny4/Bug71.dfy:refresh | 1 | 0.03M | 0.03M | -2.3% |
| lit/git-issues/git-issue-5523.dfy:refresh | 1 | 0.03M | 0.03M | -0.4% |
| lit/dafny4/git-issue254.dfy:refresh | 3 | 0.03M | 0.03M | +15.4% |
| lit/comp/rust/shadowing.dfy:refresh | 4 | 0.03M | 0.03M | -5.1% |
| lit/comp/externalImportsAndExports/exportedAndTestExternAssumptions.dfy:refresh | 4 | 0.03M | 0.03M | +7.2% |
| lit/git-issues/git-issue-697f.dfy:refresh | 4 | 0.03M | 0.02M | -8.1% |
| lit/dafny0/DecreasesTo0.dfy:refresh | 4 | 0.03M | 0.03M | -3.2% |
| lit/dafny4/git-issue88.dfy:refresh | 3 | 0.03M | 0.03M | -2.4% |
| lit/dafny0/PrefixSyntax.dfy:refresh | 5 | 0.03M | 0.02M | -10.8% |
| lit/git-issues/git-issue-283f.dfy:refresh | 4 | 0.03M | 0.02M | -6.7% |
| lit/git-issues/git-issue-5065.dfy:refresh | 2 | 0.03M | 0.03M | -2.7% |
| lit/wishlist/git-issue-6158.dfy:refresh | 2 | 0.03M | 0.03M | -2.8% |
| lit/dafny0/AsIs-UnusedTypeParameters.dfy:refresh | 2 | 0.03M | 0.03M | -1.2% |
| lit/dafny4/git-issue40.dfy:refresh | 3 | 0.03M | 0.03M | -2.8% |
| lit/comp/AsIs-Compile-Expanded.dfy:pinned | 8 | 0.03M | 0.02M | -14.1% |
| lit/comp/Ghosts.dfy:refresh | 8 | 0.03M | 0.02M | -6.1% |
| lit/dafny4/git-issue141.dfy:refresh | 1 | 0.03M | 0.03M | +0.4% |
| lit/git-issues/git-issue-6535.dfy:refresh | 1 | 0.03M | 0.03M | -0.9% |
| lit/git-issues/git-issue-1479.dfy:refresh | 1 | 0.03M | 0.03M | -0.5% |
| lit/triggers/looping-is-hard-to-decide-modulo-equality.dfy:refresh | 3 | 0.03M | 0.02M | -1.2% |
| lit/git-issues/git-issue-351.dfy:refresh | 1 | 0.03M | 0.02M | -1.6% |
| lit/comp/BuiltIns_Unsupported.dfy:refresh | 3 | 0.03M | 0.02M | -3.3% |
| lit/git-issues/git-issue-4188.dfy:refresh | 4 | 0.03M | 0.02M | -7.5% |
| lit/git-issues/git-issue-701.dfy:refresh | 1 | 0.02M | 0.02M | -1.7% |
| lit/exports/xrefine3.dfy:refresh | 3 | 0.02M | 0.02M | -1.8% |
| lit/ast/function.dfy:pinned | 9 | 0.02M | 0.02M | -13.1% |
| lit/git-issues/git-issue-334.dfy:refresh | 1 | 0.02M | 0.02M | -0.7% |
| lit/verification/constructorFresh.dfy:refresh | 3 | 0.02M | 0.03M | +7.2% |
| lit/expectations/ExpectAndExceptions.dfy:refresh | 2 | 0.02M | 0.02M | -1.3% |
| lit/dafny4/git-issue4.dfy:refresh | 5 | 0.02M | 0.02M | -11.6% |
| libraries/Functions.dfy | 1 | 0.02M | 0.02M | -1.7% |
| lit/git-issues/git-issue-5873.dfy:pinned | 4 | 0.02M | 0.02M | -1.8% |
| lit/comp/rust/cargoreleasefailure.dfy:refresh | 5 | 0.02M | 0.02M | -8.0% |
| lit/ghost/AllowedGhostBindings.dfy:refresh | 2 | 0.02M | 0.02M | -0.9% |
| lit/git-issues/git-issue-4141.dfy:refresh | 1 | 0.02M | 0.02M | -1.8% |
| lit/git-issues/git-issue-2708.dfy:refresh | 3 | 0.02M | 0.02M | -2.3% |
| lit/git-issues/git-issue-326.dfy:refresh | 2 | 0.02M | 0.02M | -1.1% |
| lit/git-issues/git-issue-1074.dfy:refresh | 3 | 0.02M | 0.02M | -1.4% |
| lit/git-issues/git-issue-895.dfy:refresh | 1 | 0.02M | 0.02M | -2.2% |
| lit/git-issues/git-issue-6395.dfy:refresh | 5 | 0.02M | 0.02M | -3.9% |
| lit/git-issues/git-issue-1185.dfy:refresh | 3 | 0.02M | 0.02M | -1.4% |
| lit/git-issues/git-issue-1029.dfy:refresh | 3 | 0.02M | 0.02M | -1.5% |
| lit/git-issues/git-issue-615.dfy:refresh | 3 | 0.02M | 0.02M | +2.4% |
| libraries/dafny/FileIO/FileIO.dfy | 2 | 0.02M | 0.02M | -0.9% |
| lit/git-issues/git-issue-6210.dfy:refresh | 2 | 0.02M | 0.02M | -1.0% |
| lit/git-issues/git-issue-2748.dfy:pinned | 2 | 0.02M | 0.02M | -5.4% |
| lit/git-issues/git-issue-1093.dfy:refresh | 2 | 0.02M | 0.02M | +6.5% |
| lit/dafny4/git-issue176.dfy:refresh | 1 | 0.02M | 0.02M | -0.7% |
| lit/triggers/let-expressions.dfy:refresh | 1 | 0.02M | 0.02M | -1.9% |
| lit/exports/RevealProvideAll.dfy:refresh | 3 | 0.02M | 0.02M | -4.3% |
| lit/git-issues/git-issue-600.dfy:refresh | 2 | 0.02M | 0.02M | -0.9% |
| lit/dafny0/BigOrdinals.dfy:refresh | 3 | 0.02M | 0.02M | -5.8% |
| lit/exceptions/GenericOutcomeDt.dfy:refresh | 2 | 0.02M | 0.02M | -1.0% |
| libraries/NonlinearArithmetic/Internals/MulInternalsNonlinear.dfy | 6 | 0.02M | 0.02M | -7.8% |
| libraries/dafny/NonlinearArithmetic/Internals/MulInternalsNonlinear.dfy | 6 | 0.02M | 0.02M | -7.8% |
| lit/dafny0/Assigned.dfy:refresh | 3 | 0.02M | 0.02M | -3.2% |
| lit/unicodecharsFalse/DafnyTests/RunAllTestsOption.dfy:refresh | 2 | 0.02M | 0.02M | -1.0% |
| lit/dafny0/ResultInTypeNewtype.dfy:pinned | 3 | 0.02M | 0.02M | -2.7% |
| lit/dafny0/ResultInTypeSubsetType.dfy:pinned | 3 | 0.02M | 0.02M | -2.7% |
| lit/c++/recursion.dfy:refresh | 5 | 0.02M | 0.02M | -11.2% |
| lit/dafny0/OpaqueTypeWithMembersE.dfy:refresh | 4 | 0.02M | 0.02M | -4.3% |
| lit/traits/Traits-Fields.dfy:refresh | 2 | 0.02M | 0.02M | +8.4% |
| lit/verification/progress.dfy:refresh | 7 | 0.02M | 0.02M | -11.9% |
| lit/dafny4/Regression7.dfy:refresh | 2 | 0.02M | 0.02M | -1.0% |
| lit/dafny0/AdvancedLHS.dfy:refresh | 3 | 0.02M | 0.02M | +4.4% |
| lit/git-issues/git-issue-5521.dfy:refresh | 6 | 0.02M | 0.02M | -12.1% |
| lit/dafny4/Bug150.dfy:refresh | 1 | 0.02M | 0.02M | -0.7% |
| lit/git-issues/git-issue-4272.dfy:pinned | 4 | 0.02M | 0.02M | -11.5% |
| lit/git-issues/git-issue-2211a.dfy:refresh | 2 | 0.02M | 0.02M | -1.0% |
| lit/git-issues/git-issue-897b.dfy:refresh | 1 | 0.02M | 0.02M | -0.6% |
| lit/exports/xrefine2.dfy:refresh | 4 | 0.02M | 0.02M | -11.1% |
| lit/git-issues/git-issue-2211.dfy:refresh | 2 | 0.02M | 0.02M | -1.0% |
| lit/comp/firstSteps/5_Calls-FunctionsValues-Dt.dfy:refresh | 2 | 0.02M | 0.02M | -1.6% |
| lit/comp/JsModule.dfy:refresh | 1 | 0.02M | 0.02M | -0.5% |
| lit/verification/proofDivision/isolateAllAssertions.dfy:refresh | 6 | 0.02M | 0.02M | -13.4% |
| lit/dafny0/TypeConversions.dfy:refresh | 3 | 0.02M | 0.02M | -9.4% |
| lit/git-issues/git-issue-3804b.dfy:pinned | 5 | 0.02M | 0.02M | -15.8% |
| lit/git-issues/git-issue-6317b.dfy:refresh | 2 | 0.02M | 0.02M | -1.1% |
| lit/git-issues/github-issue-4144.dfy:refresh | 2 | 0.02M | 0.02M | -1.1% |
| lit/dafny4/Regression3.dfy:refresh | 3 | 0.02M | 0.02M | -8.4% |
| lit/git-issues/git-issue-623.dfy:pinned | 3 | 0.02M | 0.02M | -3.6% |
| lit/exports/OpaqueFunctions.dfy:refresh | 4 | 0.02M | 0.02M | -13.4% |
| lit/git-issues/git-issue-2266.dfy:refresh | 1 | 0.02M | 0.02M | -1.6% |
| lit/proof-obligation-desc/yield-ensures.dfy:refresh | 2 | 0.02M | 0.02M | -0.4% |
| lit/git-issues/github-issue-5814.dfy:refresh | 3 | 0.02M | 0.02M | -1.7% |
| lit/dafny4/Bug118.dfy:refresh | 1 | 0.02M | 0.02M | -0.0% |
| lit/dafny4/Bug161.dfy:refresh | 2 | 0.02M | 0.02M | -2.3% |
| lit/git-issues/github-issue-4804.dfy:refresh | 3 | 0.02M | 0.02M | -10.3% |
| lit/ast/assume.dfy:refresh | 2 | 0.02M | 0.02M | -1.2% |
| lit/wishlist/GoModule.dfy:refresh | 2 | 0.02M | 0.02M | -1.2% |
| lit/comp/rust/borrowing.dfy:refresh | 2 | 0.02M | 0.02M | -4.1% |
| lit/git-issues/PR4715Test.dfy:refresh | 2 | 0.02M | 0.02M | -7.2% |
| lit/git-issues/git-issue-4812.dfy:refresh | 4 | 0.02M | 0.02M | -4.5% |
| lit/dafny0/NoReferencesVerification.dfy:refresh | 2 | 0.02M | 0.02M | -1.0% |
| lit/dafny4/git-issue27.dfy:refresh | 2 | 0.02M | 0.02M | -3.7% |
| lit/dafny0/Calculations.dfy:refresh | 3 | 0.02M | 0.02M | -7.3% |
| lit/git-issues/github-issue-4483.dfy:refresh | 2 | 0.02M | 0.02M | -4.3% |
| lit/git-issues/git-issue-697g.dfy:refresh | 2 | 0.02M | 0.02M | -4.6% |
| lit/dafny4/Bug120.dfy:refresh | 2 | 0.02M | 0.02M | -7.3% |
| lit/c++/generic.dfy:refresh | 3 | 0.02M | 0.02M | -4.0% |
| lit/dafny0/RankNeg.dfy:refresh | 1 | 0.02M | 0.02M | -0.8% |
| lit/dafny4/Bug168.dfy:refresh | 2 | 0.02M | 0.02M | -4.2% |
| lit/git-issues/git-issue-327.dfy:refresh | 5 | 0.02M | 0.01M | -18.7% |
| lit/git-issues/git-issue-5719.dfy:pinned | 3 | 0.02M | 0.02M | -4.1% |
| lit/git-issues/git-issue-2959b.dfy:refresh | 3 | 0.02M | 0.02M | -6.1% |
| lit/git-issues/github-issue-3871.dfy:refresh | 1 | 0.02M | 0.02M | -1.1% |
| lit/verification/proofDivision/isolatePaths.dfy:refresh | 4 | 0.02M | 0.01M | -15.1% |
| lit/git-issues/git-issue-779.dfy:pinned | 1 | 0.02M | 0.02M | -0.7% |
| lit/dafny4/Bug165.dfy:refresh | 1 | 0.02M | 0.02M | -0.7% |
| lit/dafny0/EqualityTypesCompile.dfy:refresh | 1 | 0.02M | 0.02M | -0.7% |
| lit/git-issues/git-issue-1909.dfy:refresh | 1 | 0.02M | 0.02M | -3.4% |
| lit/wishlist/sequences-s0-in-s.dfy:refresh | 2 | 0.02M | 0.02M | -1.8% |
| lit/comp/CSharpStyling.dfy:refresh | 3 | 0.02M | 0.01M | -11.0% |
| lit/git-issues/git-issue-4202.dfy:refresh | 1 | 0.02M | 0.02M | -1.0% |
| lit/git-issues/git-issue-2511.dfy:refresh | 3 | 0.02M | 0.01M | -5.1% |
| lit/git-issues/git-issue-2640.dfy:refresh | 3 | 0.02M | 0.01M | -11.1% |
| lit/git-issues/github-issue-3874.dfy:refresh | 1 | 0.02M | 0.02M | -0.2% |
| lit/git-issues/git-issue-885.dfy:pinned | 2 | 0.02M | 0.02M | -2.1% |
| lit/dafny4/Regression15.dfy:refresh | 3 | 0.02M | 0.01M | -2.7% |
| lit/comp/rust/externalclasses-errors.dfy:refresh | 3 | 0.02M | 0.01M | -2.1% |
| lit/dafny4/git-issue15.dfy:refresh | 1 | 0.02M | 0.01M | -0.7% |
| lit/proof-obligation-desc/distinct-lhs.dfy:refresh | 2 | 0.01M | 0.01M | -8.1% |
| lit/exports/xrefine1.dfy:refresh | 3 | 0.01M | 0.01M | -11.7% |
| lit/autoRevealDependencies/subset-types.dfy:refresh | 2 | 0.01M | 0.01M | -4.6% |
| lit/autoRevealDependencies/typecasting.dfy:refresh | 2 | 0.01M | 0.01M | -4.6% |
| lit/dafny4/git-issue51.dfy:refresh | 2 | 0.01M | 0.02M | +10.0% |
| lit/git-issues/git-issue-2510.dfy:refresh | 2 | 0.01M | 0.01M | -1.4% |
| lit/dafny4/Bug81.dfy:refresh | 1 | 0.01M | 0.01M | -0.6% |
| lit/git-issues/git-issue-6038.dfy:refresh | 2 | 0.01M | 0.01M | -1.4% |
| lit/git-issues/git-issue-2726.dfy:refresh | 1 | 0.01M | 0.01M | -1.4% |
| lit/printing/ModulePrint.dfy:refresh | 2 | 0.01M | 0.02M | +11.0% |
| lit/hofs/Consequence.dfy:refresh | 2 | 0.01M | 0.01M | -4.9% |
| lit/dafny4/Bug145.dfy:refresh | 1 | 0.01M | 0.01M | -0.7% |
| lit/dafny4/git-issue26.dfy:refresh | 1 | 0.01M | 0.01M | -1.4% |
| lit/dafny0/DecreasesTo1.dfy:refresh | 2 | 0.01M | 0.01M | -1.6% |
| lit/dafny4/git-issue239.dfy:refresh | 1 | 0.01M | 0.01M | -0.8% |
| lit/git-issues/git-issue-1665.dfy:refresh | 3 | 0.01M | 0.01M | -7.4% |
| lit/dafny4/Regression18.dfy:refresh | 4 | 0.01M | 0.01M | -13.0% |
| lit/dafny0/AsIs-Verify.dfy:refresh | 3 | 0.01M | 0.01M | -5.8% |
| lit/c++/while.dfy:refresh | 2 | 0.01M | 0.01M | -8.0% |
| lit/git-issues/git-issue-386.dfy:refresh | 2 | 0.01M | 0.01M | -1.4% |
| lit/dafny4/Bug128.legacy.dfy:refresh | 1 | 0.01M | 0.01M | -1.0% |
| lit/git-issues/git-issue-1957.dfy:refresh | 1 | 0.01M | 0.01M | -0.0% |
| lit/dafny4/Bug162.dfy:refresh | 1 | 0.01M | 0.01M | -0.8% |
| lit/comp/DefaultParameters-Compile.dfy:refresh | 1 | 0.01M | 0.01M | +6.5% |
| lit/dafny4/Bug132.dfy:refresh | 2 | 0.01M | 0.02M | +13.4% |
| lit/git-issues/git-issue-3839/git-issue-3839a.dfy:refresh | 4 | 0.01M | 0.01M | -8.0% |
| lit/comp/replaceables/replaceableHappyflow.dfy:refresh | 4 | 0.01M | 0.01M | -18.2% |
| lit/triggers/auto-triggers-fix-an-issue-listed-in-the-ironclad-notebook.dfy:refresh | 1 | 0.01M | 0.01M | -0.8% |
| lit/dafny0/NameclashesCompile.dfy:refresh | 2 | 0.01M | 0.01M | -4.6% |
| lit/dafny4/git-issue129.dfy:refresh | 2 | 0.01M | 0.01M | -5.2% |
| lit/git-issues/git-issue-698.dfy:refresh | 3 | 0.01M | 0.01M | -12.9% |
| lit/git-issues/git-issue-698b.dfy:refresh | 3 | 0.01M | 0.01M | -12.8% |
| lit/git-issues/git-issue-353.dfy:refresh | 2 | 0.01M | 0.01M | -1.5% |
| lit/git-issues/git-issue-370.dfy:refresh | 1 | 0.01M | 0.01M | -4.3% |
| lit/dafny4/git-issue147.dfy:refresh | 2 | 0.01M | 0.01M | -1.7% |
| lit/git-issues/github-issue-5029.dfy:refresh | 3 | 0.01M | 0.01M | -12.5% |
| lit/git-issues/git-issue-4724.dfy:refresh | 2 | 0.01M | 0.01M | -1.5% |
| lit/comp/rust/strings.dfy:refresh | 3 | 0.01M | 0.01M | -11.8% |
| lit/autoRevealDependencies/func-depth-succ.dfy:refresh | 4 | 0.01M | 0.01M | -7.6% |
| lit/git-issues/git-issue-4035.dfy:refresh | 2 | 0.01M | 0.01M | +8.9% |
| lit/dafny3/CalcExample.dfy:refresh | 2 | 0.01M | 0.01M | -3.2% |
| lit/server/counterexample_commandline.dfy:refresh | 1 | 0.01M | 0.01M | +0.7% |
| lit/comp/DuplicateArrowNames.dfy:refresh | 1 | 0.01M | 0.01M | -0.8% |
| lit/dafny0/TypeSynonyms.dfy:refresh | 2 | 0.01M | 0.01M | -3.5% |
| lit/git-issues/git-issue-3358.dfy:refresh | 1 | 0.01M | 0.01M | -0.8% |
| lit/git-issues/github-issue-3658.dfy:refresh | 2 | 0.01M | 0.01M | -1.6% |
| lit/git-issues/git-issue-5554.dfy:refresh | 1 | 0.01M | 0.01M | -1.0% |
| lit/HigherOrderIntrinsicSpecification/ReadPreconditionBypass4.dfy:refresh | 2 | 0.01M | 0.01M | +10.2% |
| lit/git-issues/git-issue-1435.dfy:refresh | 1 | 0.01M | 0.01M | +6.7% |
| lit/git-issues/github-issue-2989.dfy:refresh | 2 | 0.01M | 0.01M | -1.6% |
| lit/git-issues/git-issue-922.dfy:refresh | 2 | 0.01M | 0.01M | -1.7% |
| lit/dafny4/Bug108.dfy:refresh | 1 | 0.01M | 0.01M | -0.8% |
| lit/git-issues/git-issue-1231.dfy:refresh | 4 | 0.01M | 0.01M | -12.9% |
| lit/logger/VerboseName.dfy:refresh | 3 | 0.01M | 0.01M | -10.5% |
| lit/proof-obligation-desc/forall-lhs-unique.dfy:refresh | 1 | 0.01M | 0.01M | -0.3% |
| lit/comp/SequenceConcatOptimization.dfy:refresh | 1 | 0.01M | 0.01M | -0.7% |
| lit/comp/rust/docstring.dfy:refresh | 3 | 0.01M | 0.01M | -8.2% |
| lit/git-issues/git-issue-4000.dfy:refresh | 3 | 0.01M | 0.01M | -14.6% |
| lit/dafny4/git-issue1.dfy:refresh | 2 | 0.01M | 0.01M | -3.3% |
| lit/ghost/Aliasing.dfy:refresh | 2 | 0.01M | 0.01M | -3.6% |
| lit/git-issues/github-issue-2928.dfy:refresh | 1 | 0.01M | 0.01M | -1.3% |
| lit/autoRevealDependencies/power.dfy:refresh | 2 | 0.01M | 0.01M | -9.8% |
| lit/git-issues/git-issue-3691.dfy:refresh | 2 | 0.01M | 0.01M | -1.7% |
| lit/comp/ExternDafnyString.dfy:refresh | 1 | 0.01M | 0.01M | -1.1% |
| lit/unicodecharsFalse/comp/ExternDafnyString.dfy:refresh | 1 | 0.01M | 0.01M | -1.1% |
| lit/referrers/memorylocations-errors.dfy:pinned | 1 | 0.01M | 0.01M | -0.9% |
| lit/git-issues/git-issue-4309.dfy:refresh | 3 | 0.01M | 0.01M | -3.4% |
| lit/triggers/wf-checks-use-the-original-quantifier.dfy:refresh | 1 | 0.01M | 0.01M | -0.7% |
| lit/git-issues/git-issue-5726b.dfy:pinned | 3 | 0.01M | 0.01M | -2.6% |
| lit/wishlist/assign-such-that-antecedent.dfy:refresh | 3 | 0.01M | 0.01M | -11.9% |
| lit/git-issues/git-issue-3804.dfy:pinned | 2 | 0.01M | 0.01M | -10.1% |
| lit/git-issues/git-issue-261.dfy:refresh | 1 | 0.01M | 0.01M | -1.1% |
| lit/git-issues/git-issue-1607.dfy:refresh | 2 | 0.01M | 0.01M | -4.7% |
| lit/git-issues/git-issue-1812.dfy:refresh | 1 | 0.01M | 0.01M | -1.0% |
| lit/dafny4/Bug55.dfy:refresh | 1 | 0.01M | 0.01M | -1.3% |
| lit/git-issues/git-issue-674.dfy:refresh | 2 | 0.01M | 0.01M | -3.8% |
| lit/git-issues/git-issue-757.dfy:refresh | 2 | 0.01M | 0.01M | -1.8% |
| lit/verification/issue4894.dfy:refresh | 1 | 0.01M | 0.01M | +6.1% |
| lit/git-issues/git-issue-859.dfy:refresh | 3 | 0.01M | 0.01M | -4.5% |
| lit/dafny0/Protected.dfy:refresh | 3 | 0.01M | 0.01M | -17.6% |
| lit/git-issues/git-issue-4152.dfy:refresh | 1 | 0.01M | 0.01M | -4.6% |
| lit/exceptions/NatOutcomeDt.dfy:refresh | 1 | 0.01M | 0.01M | -1.0% |
| lit/git-issues/git-issue-403.dfy:refresh | 3 | 0.01M | 0.01M | -14.7% |
| lit/git-issues/git-issue-2608.dfy:refresh | 2 | 0.01M | 0.01M | -10.1% |
| lit/dafny0/InitialValues.dfy:refresh | 2 | 0.01M | 0.01M | -3.0% |
| lit/git-issues/git-issue-5331.dfy:pinned | 1 | 0.01M | 0.01M | -0.9% |
| lit/git-issues/git-issue-1714.dfy:refresh | 2 | 0.01M | 0.01M | -2.0% |
| lit/ast/reveal/revealConstants.dfy:pinned | 3 | 0.01M | 0.01M | -16.5% |
| lit/git-issues/git-issue-202.dfy:refresh | 1 | 0.01M | 0.01M | -0.9% |
| lit/dafny0/OpaqueConstants.dfy:refresh | 3 | 0.01M | 0.01M | -15.7% |
| lit/dafny4/Bug100.dfy:refresh | 1 | 0.01M | 0.01M | -1.7% |
| lit/c++/returns.dfy:refresh | 3 | 0.01M | 0.01M | -15.8% |
| lit/comp/firstSteps/2_Modules.dfy:refresh | 3 | 0.01M | 0.01M | -16.6% |
| lit/git-issues/git-issue-833.dfy:refresh | 2 | 0.01M | 0.01M | +13.2% |
| lit/git-issues/git-issue-549.dfy:refresh | 2 | 0.01M | 0.01M | -1.9% |
| lit/git-issues/git-issue-4449.dfy:refresh | 2 | 0.01M | 0.01M | -2.9% |
| lit/git-issues/git-issue-4787.dfy:refresh | 1 | 0.01M | 0.01M | -1.0% |
| lit/verification/proofDivision/isolateAssertionOrJump.dfy:refresh | 2 | 0.01M | 0.01M | -11.3% |
| lit/proof-obligation-desc/function-contract-override.dfy:refresh | 2 | 0.01M | 0.01M | -1.9% |
| lit/dafny0/GhostGuards.dfy:refresh | 1 | 0.01M | 0.01M | -3.4% |
| lit/git-issues/git-issue-443.dfy:refresh | 2 | 0.01M | 0.01M | -8.4% |
| lit/exports/ClassMemberExport.dfy:refresh | 2 | 0.01M | 0.01M | -2.0% |
| lit/git-issues/git-issue-921.dfy:refresh | 2 | 0.01M | 0.01M | -2.1% |
| lit/comp/rust/datatypes-scoping.dfy:refresh | 2 | 0.01M | 0.01M | -3.1% |
| lit/git-issues/github-issue-3797.dfy:refresh | 2 | 0.01M | 0.01M | -10.6% |
| lit/git-issues/git-issue-610.dfy:refresh | 2 | 0.01M | 0.01M | -4.6% |
| lit/dafny0/Superposition.legacy.dfy:refresh | 2 | 0.01M | 0.01M | -12.7% |
| lit/DafnyTests/RunAllTests/RunAllTestsOption.dfy:refresh | 1 | 0.01M | 0.01M | -1.1% |
| lit/git-issues/git-issue-2367.dfy:refresh | 2 | 0.01M | 0.01M | -9.1% |
| lit/git-issues/git-issue-5570.dfy:pinned | 2 | 0.01M | 0.01M | -2.2% |
| lit/dafny4/git-issue106.dfy:refresh | 1 | 0.01M | 0.01M | -6.5% |
| lit/git-issues/git-issue-3382.dfy:refresh | 2 | 0.01M | 0.01M | -10.8% |
| lit/cli/defaultTimeLimit.dfy:refresh | 1 | 0.01M | 0.01M | -6.4% |
| lit/dafny0/RealTypes.dfy:refresh | 2 | 0.01M | 0.01M | -14.7% |
| lit/dafny4/git-issue67.dfy:refresh | 1 | 0.01M | 0.01M | -4.3% |
| lit/git-issues/git-issue-1815a.dfy:refresh | 1 | 0.01M | 0.01M | -1.1% |
| lit/comp/rust/reserved-names.dfy:refresh | 1 | 0.01M | 0.01M | -5.9% |
| lit/cli/runArgument.dfy:refresh | 1 | 0.01M | 0.01M | -1.1% |
| lit/comp/CompileWithArguments.dfy:refresh | 1 | 0.01M | 0.01M | -1.1% |
| lit/unicodecharsFalse/comp/CompileWithArguments.dfy:refresh | 1 | 0.01M | 0.01M | -1.1% |
| lit/dafny4/LargeConstants.dfy:refresh | 3 | 0.01M | 0.01M | -14.3% |
| lit/git-issues/git-issue-1151.dfy:refresh | 1 | 0.01M | 0.01M | -1.1% |
| lit/git-issues/git-issue-356-errors2.dfy:refresh | 2 | 0.01M | 0.01M | -13.4% |
| lit/comp/rust/small/03-methodnamed.dfy:pinned | 1 | 0.01M | 0.01M | -1.2% |
| lit/dafny4/git-issue28.dfy:refresh | 1 | 0.01M | 0.01M | -6.9% |
| lit/comp/rust/nestedmodules.dfy:refresh | 3 | 0.01M | 0.01M | -7.0% |
| lit/dafny4/git-issue98.dfy:refresh | 1 | 0.01M | 0.01M | -1.2% |
| lit/dafny4/Bug166.dfy:refresh | 1 | 0.01M | 0.01M | -1.2% |
| lit/git-issues/git-issue-4936b.dfy:refresh | 1 | 0.01M | 0.01M | -1.2% |
| lit/newtype/aliases.dfy:refresh | 2 | 0.01M | 0.01M | -14.6% |
| lit/dafny4/Bug133.dfy:refresh | 1 | 0.01M | 0.01M | -6.3% |
| lit/ast/const.dfy:refresh | 2 | 0.01M | 0.01M | -14.7% |
| lit/dafny0/Tooltips.dfy:refresh | 2 | 0.01M | 0.01M | -2.5% |
| lit/git-issues/git-issue-1150.dfy:refresh | 1 | 0.01M | 0.01M | -6.7% |
| lit/git-issues/git-issue-904.dfy:refresh | 2 | 0.01M | 0.01M | -15.0% |
| lit/dafny0/AssumptionVariables1.dfy:refresh | 2 | 0.01M | 0.01M | -5.1% |
| lit/dafny4/git-issue210.dfy:refresh | 1 | 0.01M | 0.01M | -1.3% |
| lit/git-issues/git-issue-2173.dfy:refresh | 1 | 0.01M | 0.01M | -1.3% |
| lit/triggers/triggers-prevent-some-inlining.dfy:refresh | 1 | 0.01M | 0.01M | -6.5% |
| lit/dafny4/git-issue206.dfy:refresh | 1 | 0.01M | 0.01M | -1.5% |
| lit/git-issues/git-issue-2956a.dfy:refresh | 1 | 0.01M | 0.01M | -1.3% |
| lit/triggers/redundancy-detection-is-bidirectional.dfy:refresh | 2 | 0.01M | 0.01M | -8.8% |
| lit/comp/rust/small/04-mismatched.dfy:pinned | 2 | 0.01M | 0.01M | -2.6% |
| lit/git-issues/git-issue-2197.dfy:refresh | 1 | 0.01M | 0.01M | -1.5% |
| lit/git-issues/github-issue-1267.dfy:refresh | 1 | 0.01M | 0.01M | -1.3% |
| lit/autoRevealDependencies/func-depth-fail.dfy:refresh | 3 | 0.01M | 0.01M | -8.0% |
| lit/git-issues/git-issue-1852.dfy:refresh | 2 | 0.01M | 0.01M | -17.4% |
| lit/exports/ExportRefinement.dfy:refresh | 2 | 0.01M | 0.01M | -5.4% |
| lit/dafny4/Bug94.dfy:refresh | 1 | 0.01M | 0.01M | -1.6% |
| lit/git-issues/git-issue-856.dfy:refresh | 1 | 0.01M | 0.01M | -1.5% |
| lit/git-issues/git-issue-1815b.dfy:refresh | 1 | 0.01M | 0.01M | -1.4% |
| lit/git-issues/git-issue-1564-3.dfy:refresh | 2 | 0.01M | 0.01M | -14.2% |
| lit/git-issues/git-issue-1564-3to4.dfy:refresh | 2 | 0.01M | 0.01M | -14.2% |
| lit/git-issues/git-issue-1564-4.dfy:refresh | 2 | 0.01M | 0.01M | -14.2% |
| lit/git-issues/git-issue-1564-eag.dfy:refresh | 2 | 0.01M | 0.01M | -14.2% |
| lit/HigherOrderIntrinsicSpecification/ReadPreconditionBypass1.dfy:refresh | 1 | 0.01M | 0.01M | +10.8% |
| lit/HigherOrderIntrinsicSpecification/ReadPreconditionBypass2.dfy:refresh | 1 | 0.01M | 0.01M | +10.8% |
| lit/HigherOrderIntrinsicSpecification/ReadPreconditionBypass3.dfy:refresh | 1 | 0.01M | 0.01M | +10.8% |
| lit/git-issues/git-issue-4012.dfy:refresh | 1 | 0.01M | 0.01M | -1.4% |
| lit/exports/OpenImportRefined.dfy:refresh | 2 | 0.01M | 0.01M | -10.6% |
| lit/dafny4/Bug89.dfy:refresh | 2 | 0.01M | 0.01M | -16.8% |
| lit/git-issues/git-issue-4176.dfy:refresh | 1 | 0.01M | 0.01M | -2.4% |
| lit/ast/statement/assignSuchThat.dfy:refresh | 2 | 0.01M | 0.01M | -13.3% |
| lit/git-issues/git-issue-849a.dfy:refresh | 1 | 0.01M | 0.01M | -7.3% |
| lit/git-issues/git-issue-4217.dfy:refresh | 1 | 0.01M | 0.01M | -1.5% |
| lit/git-issues/git-issue-4939b.dfy:pinned | 1 | 0.01M | 0.01M | -1.5% |
| lit/ast/method.dfy:pinned | 2 | 0.01M | 0.01M | -9.8% |
| lit/git-issues/git-issue-6014.dfy:refresh | 1 | 0.01M | 0.01M | -3.0% |
| lit/dafny4/Bug67.dfy:refresh | 1 | 0.01M | 0.01M | -1.5% |
| lit/git-issues/git-issue-4844.dfy:refresh | 1 | 0.01M | 0.01M | -1.5% |
| lit/ast/statement/calls/CallByHide.dfy:pinned | 2 | 0.01M | 0.01M | -10.4% |
| lit/git-issues/git-issue-5365.dfy:pinned | 1 | 0.01M | 0.01M | -1.5% |
| lit/git-issues/git-issue-5238.dfy:refresh | 1 | 0.01M | 0.01M | -1.5% |
| lit/git-issues/github-issue-3343.dfy:refresh | 1 | 0.01M | 0.01M | -1.5% |
| lit/dafny4/git-issue57.dfy:refresh | 2 | 0.01M | 0.01M | -11.8% |
| lit/git-issues/git-issue-371.dfy:refresh | 2 | 0.01M | 0.01M | -15.3% |
| lit/git-issues/git-issue-659.dfy:refresh | 2 | 0.01M | 0.01M | -18.0% |
| lit/git-issues/git-issue-864z1.dfy:refresh | 2 | 0.01M | 0.01M | -17.9% |
| lit/triggers/suppressing-warnings-behaves-properly.dfy:refresh | 1 | 0.01M | 0.01M | -8.9% |
| lit/dafny0/JustWarnings.dfy:refresh | 1 | 0.01M | 0.01M | -1.5% |
| lit/dafny0/LhsDuplicates.dfy:refresh | 1 | 0.01M | 0.01M | -1.5% |
| lit/git-issues/git-issue-1963c.dfy:refresh | 2 | 0.01M | 0.01M | -16.9% |
| lit/git-issues/git-issue-4994.dfy:refresh | 1 | 0.01M | 0.01M | -1.6% |
| lit/git-issues/git-issue-956.dfy:refresh | 1 | 0.01M | 0.01M | -7.8% |
| lit/comp/MainMethod.dfy:refresh | 2 | 0.01M | 0.01M | -18.3% |
| lit/git-issues/git-issue-3370.dfy:refresh | 1 | 0.01M | 0.01M | -1.5% |
| lit/git-issues/git-issue-6154a.dfy:refresh | 1 | 0.01M | 0.01M | -1.5% |
| lit/git-issues/git-issue-4007.dfy:refresh | 1 | 0.01M | 0.01M | -3.0% |
| lit/git-issues/git-issue-3461b.dfy:refresh | 2 | 0.01M | 0.01M | -18.5% |
| lit/git-issues/git-issue-5184/git-issue-5184.dfy:refresh | 1 | 0.01M | 0.01M | -1.6% |
| lit/comp/rust/type-test.dfy:refresh | 1 | 0.01M | 0.01M | -3.2% |
| lit/git-issues/git-issue-2612b.dfy:refresh | 1 | 0.01M | 0.01M | -1.9% |
| lit/comp/rust/tests.dfy:refresh | 1 | 0.01M | 0.01M | -1.6% |
| lit/triggers/large-quantifiers-dont-break-dafny.dfy:refresh | 1 | 0.01M | 0.01M | -5.4% |
| lit/dafny4/Juggernaut.dfy:refresh | 1 | 0.01M | 0.01M | -3.2% |
| lit/git-issues/git-issue-3605.dfy:refresh | 1 | 0.01M | 0.01M | -1.6% |
| lit/proof-obligation-desc/ensures-stronger.dfy:refresh | 1 | 0.01M | 0.01M | -1.6% |
| lit/git-issues/git-issue-3868a.dfy:refresh | 1 | 0.01M | 0.01M | -1.7% |
| lit/dafny4/Bug124.dfy:refresh | 1 | 0.01M | 0.01M | -8.5% |
| lit/git-issues/git-issue-863.dfy:refresh | 1 | 0.01M | 0.01M | -9.3% |
| lit/git-issues/git-issue-2597-verification.dfy:refresh | 1 | 0.01M | 0.01M | +11.9% |
| lit/proof-obligation-desc/precondition-satisfied.dfy:refresh | 2 | 0.01M | 0.01M | -6.8% |
| lit/dafny0/CustomErrorMesage.dfy:refresh | 1 | 0.01M | 0.01M | -3.4% |
| lit/git-issues/git-issue-555.dfy:refresh | 2 | 0.01M | 0.01M | -13.5% |
| lit/git-issues/git-issue-2920.dfy:refresh | 1 | 0.01M | 0.01M | -9.8% |
| lit/dafny4/Bug72.dfy:refresh | 1 | 0.01M | 0.01M | -3.5% |
| lit/dafny4/Bug63.dfy:refresh | 1 | 0.01M | 0.01M | -7.0% |
| lit/git-issues/git-issue-4205a.dfy:refresh | 1 | 0.01M | 0.01M | -1.7% |
| lit/dafny4/git-issue235.dfy:refresh | 2 | 0.01M | 0.01M | -11.6% |
| lit/dafny4/git-issue39.dfy:refresh | 1 | 0.01M | 0.01M | -13.4% |
| lit/dafny0/GeneralNewtypeMemberVerifyReal.dfy:pinned | 2 | 0.01M | 0.00M | -20.5% |
| lit/triggers/loop-detection-messages--unit-tests.dfy:refresh | 1 | 0.01M | 0.01M | -8.8% |
| lit/comp/rust/nomaybeplacebos.dfy:refresh | 2 | 0.01M | 0.01M | -13.8% |
| lit/traits/TraitCompileErrors.dfy:refresh | 2 | 0.01M | 0.01M | -11.9% |
| lit/git-issues/github-issue-4017.dfy:refresh | 1 | 0.01M | 0.01M | -1.8% |
| lit/git-issues/git-issue-362.dfy:refresh | 1 | 0.01M | 0.01M | -6.0% |
| lit/wishlist/granted/strings.dfy:refresh | 1 | 0.01M | 0.01M | -1.8% |
| lit/git-issues/git-issue-975.dfy:refresh | 1 | 0.01M | 0.01M | -10.4% |
| lit/dafny4/Regression10.dfy:refresh | 1 | 0.01M | 0.01M | -1.9% |
| lit/dafny4/git-issue74.dfy:refresh | 1 | 0.01M | 0.01M | -6.3% |
| lit/git-issues/git-issue-2265.dfy:refresh | 1 | 0.01M | 0.00M | -10.5% |
| lit/triggers/constructors-cause-matching-loops.dfy:refresh | 1 | 0.01M | 0.01M | -6.3% |
| lit/git-issues/git-issue-4224.dfy:pinned | 1 | 0.01M | 0.00M | -9.6% |
| lit/c++/bv-truncation.dfy:refresh | 1 | 0.01M | 0.00M | -9.7% |
| lit/proof-obligation-desc/requires-weaker.dfy:refresh | 1 | 0.01M | 0.01M | -1.9% |
| lit/dafny0/Include.dfy:refresh | 1 | 0.01M | 0.00M | -11.3% |
| lit/git-issues/git-issue-2747.dfy:refresh | 1 | 0.01M | 0.00M | -10.8% |
| lit/comp/ExternCtors.dfy:refresh | 1 | 0.01M | 0.01M | -1.9% |
| lit/dafny4/Bug116.dfy:refresh | 1 | 0.01M | 0.00M | -9.8% |
| lit/git-issues/git-issue-1762.dfy:refresh | 1 | 0.01M | 0.00M | -6.6% |
| lit/git-issues/git-issue-396.dfy:refresh | 1 | 0.01M | 0.00M | -9.9% |
| lit/triggers/loop-detection-is-not-too-strict.dfy:refresh | 1 | 0.01M | 0.00M | -9.9% |
| lit/git-issues/git-issue-944.dfy:refresh | 1 | 0.01M | 0.01M | -2.0% |
| lit/comp/rust/small/10-type-parameter-equality.dfy:pinned | 1 | 0.01M | 0.00M | -4.0% |
| lit/metatests/EachResolverUniformSuccess.dfy:refresh | 1 | 0.00M | 0.00M | -12.2% |
| lit/dafny4/Bug99.dfy:refresh | 1 | 0.00M | 0.00M | -7.0% |
| libraries/Math.dfy | 1 | 0.00M | 0.00M | -12.4% |
| lit/exports/ExportVerify.dfy:refresh | 1 | 0.00M | 0.00M | -12.3% |
| lit/dafny0/Simple.dfy:refresh | 1 | 0.00M | 0.00M | -7.1% |
| lit/dafny0/BadFunction.dfy:refresh | 1 | 0.00M | 0.00M | -9.5% |
| lit/wishlist/granted/useless-casts-in-decreases-clauses.dfy:refresh | 1 | 0.00M | 0.00M | -12.7% |
| lit/git-issues/git-issue-4205.dfy:refresh | 1 | 0.00M | 0.00M | -2.2% |
| lit/git-issues/git-issue-262.dfy:refresh | 1 | 0.00M | 0.00M | -2.2% |
| lit/git-issues/git-issue-1761.dfy:refresh | 1 | 0.00M | 0.00M | -7.4% |
| lit/git-issues/git-issue-5642.dfy:refresh | 1 | 0.00M | 0.00M | -7.4% |
| lit/dafny0/RevealConsistency.dfy:refresh | 1 | 0.00M | 0.00M | -12.4% |
| lit/comp/rust/small/07-instantiated-methods.dfy:pinned | 1 | 0.00M | 0.00M | -2.2% |
| lit/dafny4/git-issue20.dfy:refresh | 1 | 0.00M | 0.00M | -11.3% |
| lit/git-issues/git-issue-3719b.dfy:refresh | 1 | 0.00M | 0.00M | -11.6% |
| lit/git-issues/git-issue-1111.dfy:refresh | 1 | 0.00M | 0.00M | -13.6% |
| lit/git-issues/git-issue-588.dfy:refresh | 1 | 0.00M | 0.00M | -13.6% |
| lit/git-issues/git-issue-374.dfy:refresh | 1 | 0.00M | 0.00M | -13.5% |
| lit/git-issues/git-issue-448.dfy:refresh | 1 | 0.00M | 0.00M | -4.6% |
| lit/patterns/abstractModuleAndMatchFlattening.dfy:refresh | 1 | 0.00M | 0.00M | -2.6% |
| lit/comp/rust/small/02-binary.dfy:pinned | 1 | 0.00M | 0.00M | -2.3% |
| lit/comp/rust/datatypes-impl.dfy:refresh | 1 | 0.00M | 0.00M | -13.9% |
| lit/autoRevealDependencies/datatype-reveals.dfy:refresh | 1 | 0.00M | 0.00M | -15.4% |
| lit/git-issues/git-issue-945.dfy:refresh | 1 | 0.00M | 0.00M | -2.4% |
| lit/dafny4/git-issue120.dfy:refresh | 1 | 0.00M | 0.00M | -15.5% |
| lit/git-issues/github-issue-3766-b.dfy:refresh | 1 | 0.00M | 0.00M | -2.4% |
| lit/git-issues/git-issue-3719a.dfy:refresh | 1 | 0.00M | 0.00M | -14.3% |
| lit/git-issues/git-issue-3809.dfy:refresh | 1 | 0.00M | 0.00M | -8.2% |
| lit/git-issues/git-issue-4823.dfy:pinned | 1 | 0.00M | 0.00M | -2.5% |
| lit/git-issues/git-issue-3978.dfy:refresh | 1 | 0.00M | 0.00M | -12.5% |
| lit/git-issues/git-issue-1604c.dfy:refresh | 1 | 0.00M | 0.00M | -14.6% |
| lit/git-issues/git-issue-4233.dfy:refresh | 1 | 0.00M | 0.00M | -12.9% |
| lit/comp/rust/small/01-hash.dfy:pinned | 1 | 0.00M | 0.00M | -11.2% |
| lit/ast/files/defaultModuleAndIncludes/root.dfy:refresh | 1 | 0.00M | 0.00M | -5.2% |
| lit/git-issues/git-issue-4139.dfy:refresh | 1 | 0.00M | 0.00M | -5.2% |
| lit/git-issues/git-issue-425.dfy:refresh | 1 | 0.00M | 0.00M | -8.8% |
| lit/dafny4/predicateReturnVariable.dfy:refresh | 1 | 0.00M | 0.00M | -15.4% |
| lit/exports/AliasedImportConsistency.dfy:refresh | 1 | 0.00M | 0.00M | -17.3% |
| lit/git-issues/git-issue-3482.dfy:refresh | 1 | 0.00M | 0.00M | -9.0% |
| lit/git-issues/git-issue-686.dfy:refresh | 1 | 0.00M | 0.00M | -9.2% |
| lit/git-issues/git-issue-2016.dfy:refresh | 1 | 0.00M | 0.00M | -17.8% |
| lit/git-issues/github-issue-3766-a.dfy:refresh | 1 | 0.00M | 0.00M | -2.8% |
| lit/git-issues/git-issue-4998.dfy:refresh | 1 | 0.00M | 0.00M | -9.3% |
| lit/dafny0/GhostPrint.dfy:refresh | 1 | 0.00M | 0.00M | -18.0% |
| lit/ast/statement/AssertBy.dfy:refresh | 1 | 0.00M | 0.00M | -16.4% |
| lit/git-issues/git-issue-MainE.dfy:refresh | 1 | 0.00M | 0.00M | -16.5% |
| lit/git-issues/git-issue-1210.dfy:refresh | 1 | 0.00M | 0.00M | -16.8% |
| lit/git-issues/git-issue-1903.dfy:refresh | 1 | 0.00M | 0.00M | -9.6% |
| lit/comp/elseWithHavocStatement.dfy:refresh | 1 | 0.00M | 0.00M | -14.6% |
| lit/metatests/OutputEncoding.dfy:refresh | 1 | 0.00M | 0.00M | -17.6% |
| lit/git-issues/git-issue-1151-more.dfy:refresh | 1 | 0.00M | 0.00M | -6.0% |
| lit/comp/firstSteps/3_Calls-As.dfy:refresh | 1 | 0.00M | 0.00M | -15.2% |
| lit/comp/replaceables/replaceableExecutionErrors.dfy:refresh | 1 | 0.00M | 0.00M | -17.7% |
| lit/git-issues/git-issue-478-good.dfy:refresh | 1 | 0.00M | 0.00M | -17.7% |
| lit/git-issues/git-issue-1838.dfy:refresh | 1 | 0.00M | 0.00M | -17.7% |
| lit/cli/diagnosticsFormats.legacy.dfy:refresh | 1 | 0.00M | 0.00M | -15.3% |
| lit/cli/json-output.dfy:refresh | 1 | 0.00M | 0.00M | -15.3% |
| lit/proof-obligation-desc/conversion-satisfies-constraints.dfy:refresh | 1 | 0.00M | 0.00M | -15.3% |
| lit/dafny4/Bug134.dfy:refresh | 1 | 0.00M | 0.00M | -15.3% |
| lit/dafny4/git-issue29.dfy:refresh | 1 | 0.00M | 0.00M | -15.3% |
| lit/git-issues/github-issue-4004_v2.dfy:refresh | 1 | 0.00M | 0.00M | -15.3% |
| lit/dafny0/Fp32Wellformedness.dfy:refresh | 1 | 0.00M | 0.00M | -6.3% |
| lit/git-issues/git-issue-864rr.dfy:refresh | 1 | 0.00M | 0.00M | -18.6% |
| lit/git-issues/git-issue-950.dfy:refresh | 1 | 0.00M | 0.00M | -18.8% |
| lit/triggers/loop-detection-looks-at-ranges-too.dfy:refresh | 1 | 0.00M | 0.00M | -10.7% |
| lit/wishlist/FuelTriggers.dfy:refresh | 1 | 0.00M | 0.00M | -6.5% |
| lit/dafny4/Bug136.dfy:refresh | 1 | 0.00M | 0.00M | -11.0% |
| lit/git-issues/git-issue-3497.dfy:refresh | 1 | 0.00M | 0.00M | -11.0% |
| lit/git-issues/git-issue-4394.dfy:pinned | 1 | 0.00M | 0.00M | -11.2% |
| lit/ast/functions/constantWithReveal.dfy:refresh | 1 | 0.00M | 0.00M | -19.7% |
| lit/dafny4/Bug103.dfy:refresh | 1 | 0.00M | 0.00M | -11.3% |
| lit/metatests/LegacyResolverFails.dfy:refresh | 1 | 0.00M | 0.00M | -19.8% |
| lit/exports/IncludeSkipTranslate.dfy:refresh | 1 | 0.00M | 0.00M | -11.4% |
| lit/git-issues/git-issue-816.dfy:refresh | 1 | 0.00M | 0.00M | -19.9% |
| lit/git-issues/git-issue-4055.dfy:refresh | 1 | 0.00M | 0.00M | -11.4% |
| lit/dafny4/Regression13.dfy:refresh | 1 | 0.00M | 0.00M | -11.4% |
| lit/git-issues/git-issue-3839/git-issue-3839b.dfy:refresh | 1 | 0.00M | 0.00M | -17.5% |
| lit/git-issues/git-issue-3839/git-issue-3839c.dfy:refresh | 1 | 0.00M | 0.00M | -17.5% |
| lit/cli/badProverPath.dfy:refresh | 1 | 0.00M | 0.00M | -20.6% |
| lit/cli/proverPath.dfy:refresh | 1 | 0.00M | 0.00M | -20.6% |
| lit/cli/solverLog.dfy:refresh | 1 | 0.00M | 0.00M | -20.6% |
| lit/git-issues/git-issue-401.dfy:refresh | 1 | 0.00M | 0.00M | -20.6% |
| lit/git-issues/git-issue-401a.dfy:refresh | 1 | 0.00M | 0.00M | -20.6% |
| lit/git-issues/git-issue-3839/git-issue-3839d.dfy:refresh | 1 | 0.00M | 0.00M | -20.6% |
| lit/dafny0/SiblingImports.dfy:refresh | 1 | 0.00M | 0.00M | -7.0% |
| lit/c++/const.dfy:refresh | 1 | 0.00M | 0.00M | -7.0% |
| lit/comp/Module.dfy:refresh | 1 | 0.00M | 0.00M | -7.0% |
| lit/contract-wrappers/RefineContract.dfy:refresh | 1 | 0.00M | 0.00M | -7.0% |
| lit/git-issues/git-issue-4181.dfy:refresh | 1 | 0.00M | 0.00M | -7.0% |
| lit/git-issues/github-issue-305-b.dfy:refresh | 1 | 0.00M | 0.00M | -7.0% |
| lit/dafny0/ModuleInsertion.dfy:refresh | 1 | 0.00M | 0.00M | -7.0% |
| lit/expectations/Expect.dfy:refresh | 1 | 0.00M | 0.00M | -7.0% |
| lit/git-issues/git-issue-032.dfy:refresh | 1 | 0.00M | 0.00M | -7.0% |
| lit/dafny4/Bug121.dfy:refresh | 1 | 0.00M | 0.00M | -12.0% |
| lit/dafny0/Includee.dfy:refresh | 1 | 0.00M | 0.00M | -7.2% |
| lit/dafny0/Fp64Wellformedness.dfy:refresh | 1 | 0.00M | 0.00M | -7.3% |
| lit/dafny0/ReadsOnMethods_Printing.dfy:refresh | 1 | 0.00M | 0.00M | -12.4% |
| lit/dafny4/Bug122.dfy:refresh | 1 | 0.00M | 0.00M | -12.7% |
| lit/ast/statement/assignment.dfy:refresh | 1 | 0.00M | 0.00M | -7.6% |
| lit/irondafny0/opened_workaround.dfy:refresh | 1 | 0.00M | 0.00M | -13.1% |
| lit/logger/JsonLogger.dfy:refresh | 1 | 0.00M | 0.00M | -8.1% |
| lit/logger/TextLogger.dfy:refresh | 1 | 0.00M | 0.00M | -8.1% |
| lit/wishlist/exists-b-exists-not-b.dfy:refresh | 1 | 0.00M | 0.00M | -8.2% |
| lit/git-issues/git-issue-1618.dfy:refresh | 1 | 0.00M | 0.00M | -8.5% |

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
| A/A: master2 vs master (same input, another process) | 1249 | 24821 | +0.0% [-0.0%, +0.0%] | +0.0% [-0.0%, +0.0%] | +0.0% [-0.0%, +0.0%] | 0 |
| pr vs master | 1249 | 24821 | +3.5% [-11.8%, +22.2%] | -2.0% [-2.6%, -1.5%] | -4.3% [-4.7%, -4.0%] | 12 |

## Comparisons over the external programs' affected proofs

| comparison | programs | VCs | total | geomean over VCs | per program | verdict flips at limit |
|---|---:|---:|---|---|---|---:|
| A/A: master2 vs master (same input, another process) | 103 | 4571 | +0.0% [+0.0%, +0.0%] | +0.0% [+0.0%, +0.0%] | +0.0% [+0.0%, +0.0%] | 0 |
| pr vs master | 103 | 4571 | +11.4% [-22.4%, +79.0%] | -1.9% [-2.9%, -1.2%] | -3.3% [-5.4%, -1.7%] | 3 |

## Alternative sound encodings, over the same proofs

restrict: elements defined everywhere, `$ArbitraryBoxValue` outside the domain. domguard: the PR's axiom guarded by `Map#Domain(Map#Glue(a, b, t))`. eager: the PR's axiom plus the trigger `{ Map#Glue(a, b, t), Set#IsMember(a, bx) }`.

| encoding | programs | VCs | total vs master | geomean over VCs vs master | per program vs master | per program vs PR | verdict flips vs master at limit |
|---|---:|---:|---|---|---|---|---:|
| pr | 1249 | 24821 | +3.5% [-11.9%, +22.4%] | -2.0% [-2.5%, -1.5%] | -4.3% [-4.7%, -4.0%] |  | 23 |
| master2 | 1249 | 24821 | +0.0% [-0.0%, +0.0%] | +0.0% [-0.0%, +0.0%] | +0.0% [-0.0%, +0.0%] | +4.5% [+4.1%, +5.0%] | 0 |

master2: largest differences from the PR

| job | VC | master | PR | master2 |
|---|---|---:|---:|---:|
| libraries/dafny/Collections/LittleEndianNatConversions.dfy | Dafny.Collections.LittleEndianNatConversions.LemmaSmallLargeSmall (correctness) | 10.99M | 187.63M | 10.99M |
| libraries/JSON/ZeroCopy/Serializer.dfy | JSON.ZeroCopy.Serializer.Number (well-formedness) (assertion batch 17) | 135.34M | 299.37M | 135.34M |
| std/Base64.dfy | Std.Base64.EncodeBVIsBase64 (correctness) | 1.80M | 163.85M | 1.80M |
| lit/dafny2/SmallestMissingNumber-functional.dfy:refresh | SMN''_Correct (correctness) | 28.21M | 160.24M | 28.21M |
| kondo/twoPhaseCommit/sync | TwoPCInvariantProof.InvNextLeaderTallyReflectsPreferences (correctness) | 131.29M | 1.09M | 131.29M |
| lit/dafny2/SnapshotableTrees.dfy:refresh | SnapTree.Iterator.Push (correctness) (assertion batch 13) | 118.93M | 0.74M | 118.93M |
