# #6543 A/B benchmark (public corpora, seed 1)

Seeds per (VC, prelude): 1 (1; 0 is Dafny's default). VCs: 27063 in 2077 jobs; **1638 affected** (master and PR counts differ), 25425 unaffected (identical counts under master and PR for every seed).

## Proof cost over affected VCs that pass everywhere

Totals are sums of per-VC means over seeds. "Per program" averages each program's own VC geomean, so a
program with hundreds of VCs weighs no more than one with two. Brackets are 95% bootstrap intervals that
resample programs, not VCs.

| group | programs | VCs | largest program | total PR/master | geomean over VCs | per program |
|---|---:|---:|---|---|---|---|
| all but synth | 156 | 1570 | lit/dafny4/UnionFind.dfy (21% of VCs) | +0.6% [-29.7%, +26.2%] | -0.0% [-0.6%, +0.5%] | +0.5% [+0.1%, +1.2%] |
| dafnybench | 7 | 46 | dafnybench/dafny_experiments_tmp_tmpz29_3_3i_circuit.dfy (39% of VCs) | +90.0% [-3.2%, +175.8%] | +2.5% [-0.8%, +13.5%] | +6.8% [-0.2%, +18.1%] |
| kondo | 19 | 266 | kondo/flexPaxos/sync (27% of VCs) | -2.7% [-38.2%, +24.9%] | -1.3% [-2.3%, +0.5%] | +0.1% [-0.4%, +0.4%] |
| libraries | 6 | 63 | libraries/JSON/Utils/Str.dfy (22% of VCs) | +0.3% [-0.2%, +0.8%] | +0.3% [-0.0%, +0.5%] | +0.4% [+0.1%, +0.5%] |
| lit | 108 | 1084 | lit/dafny4/UnionFind.dfy (30% of VCs) | +0.3% [-5.3%, +3.2%] | +0.0% [-0.6%, +0.3%] | +0.1% [-0.2%, +0.3%] |
| std | 16 | 111 | std/Strings.dfy (20% of VCs) | +3.4% [-0.1%, +12.0%] | +1.5% [+0.1%, +3.5%] | +1.5% [-0.1%, +4.1%] |

68 affected VCs fail (a verification error) in some run; their cost is the solver's search for a counterexample, reported separately:

| job | VC | master mean (min..max) | PR mean (min..max) |
|---|---|---|---|
| lit/comp/TypeParams.dfy:refresh | Standard (correctness) | 832.98M (832.98..832.98) | 477.67M (477.67..477.67) |
| lit/dafny0/FunctionSpecifications.dfy:refresh | GoodPost (well-formedness) | 311.14M (311.14..311.14) | 311.09M (311.09..311.09) |
| lit/cli/defaultTimeLimit.dfy:refresh | Foo (correctness) | 298.84M (298.84..298.84) | 265.32M (265.32..265.32) |
| kondo/paxos/sync | PaxosProof.InvNextLearnerReceivedAcceptImpliesAccepted (correctness) | 293.81M (293.81..293.81) | 51.15M (51.15..51.15) |
| libraries/dafny/Collections/Seqs.dfy | Dafny.Collections.Seq.LemmaMapDistributesOverConcat (correctness) | 243.34M (243.34..243.34) | 276.95M (276.95..276.95) |
| dafnybench/dafny_experiments_tmp_tmpz29_3_3i_circuit.dfy | CombineCircuits.CombineCircuitsCorrect (correctness) | 214.71M (214.71..214.71) | 228.11M (228.11..228.11) |
| libraries/dafny/Collections/Seqs.dfy | Dafny.Collections.Seq.LemmaFilterDistributesOverConcat (correctness) (assertion batch 2) | 171.40M (171.40..171.40) | 179.87M (179.87..179.87) |
| lit/git-issues/git-issue-3855.dfy:pinned | Memory.dynMove (correctness) | 151.34M (151.34..151.34) | 57.46M (57.46..57.46) |
| lit/dafny1/Rippling.legacy.dfy:refresh | P2 (correctness) | 22.88M (22.88..22.88) | 21.50M (21.50..21.50) |
| kondo/paxos/sync | PaxosProof.InvNextChosenImpliesProposingLeaderHearsChosenBallotP2bStep (correctness) | 22.37M (22.37..22.37) | 312.98M (312.98..312.98) |

## Total proof RU per seed (affected VCs that pass everywhere)

| prelude | seed 1 | mean | sd |
|---|---:|---:|---:|
| master | 859.2M | 859.2M | 0.0M |
| pr | 864.6M | 864.6M | 0.0M |

## Solver time over those proofs (sum of per-VC means, seconds)

| group | master | PR |
|---|---:|---:|
| all | 753.0 | 602.4 |
| lit | 111.1 | 119.9 |
| std | 19.2 | 11.5 |

## Distribution of per-VC cost ratios over those proofs (mean over seeds)

| ratio bucket | PR/master |
|---|---:|
| < 0.5x | 6 |
| 0.5-0.8x | 10 |
| 0.8-0.95x | 30 |
| 0.95-1.05x | 1495 |
| 1.05-1.25x | 19 |
| 1.25-2x | 5 |
| 2-4x | 3 |
| >= 4x | 2 |

## Verdict changes at each job's limit (seeds passing out of 1)

| job | VC | limit | master ok | PR ok | master RU | PR RU |
|---|---|---:|---:|---:|---:|---:|
| kondo/flexPaxos/sync | PaxosProof.InvNextAcceptorValidBundle (correctness) | 50M | 0 | 1 | 67.36M | 46.87M |
| kondo/flexPaxos/sync | PaxosProof.InvNextChosenImpliesProposingLeaderHearsChosenBallotP2bStep (correctness) | 50M | 1 | 0 | 16.81M | 306.00M |
| kondo/flexPaxos/sync | PaxosProof.InvNextLearnerReceivedAcceptImpliesAccepted (correctness) | 50M | 1 | 0 | 45.53M | 279.76M |
| kondo/paxos/sync | PaxosProof.InvNextAcceptorValidBundle (correctness) | 50M | 1 | 0 | 14.76M | 61.59M |
| kondo/paxos/sync | PaxosProof.InvNextChosenImpliesProposingLeaderHearsChosenBallotP2bStep (correctness) | 50M | 1 | 0 | 22.37M | 312.98M |
| kondo/paxos/sync | PaxosProof.InvNextLeaderReceivedPromisesImpliesAcceptorState (correctness) | 50M | 0 | 1 | 171.77M | 29.81M |

## Largest changes among those proofs (by |PR - master| mean RU)

| job | VC | master | PR | PR/master | min..max master | min..max PR |
|---|---|---:|---:|---:|---|---|
| kondo/flexPaxos/sync | PaxosProof.InvNextLearnerReceivedAcceptImpliesAccepted (correctness) | 45.53M | 279.76M | 6.14 | 45.53..45.53M | 279.76..279.76M |
| kondo/paxos/sync | PaxosProof.InvNextLeaderReceivedPromisesImpliesAcceptorState (correctness) | 171.77M | 29.81M | 0.17 | 171.77..171.77M | 29.81..29.81M |
| kondo/flexPaxos/sync | PaxosProof.InvNextLeaderReceivedPromisesImpliesAcceptorState (correctness) | 174.48M | 70.51M | 0.40 | 174.48..174.48M | 70.51..70.51M |
| kondo/paxos/sync | PaxosProof.InvNextAcceptorValidBundle (correctness) | 14.76M | 61.59M | 4.17 | 14.76..14.76M | 61.59..61.59M |
| kondo/flexPaxos/sync | PaxosProof.InvNextAcceptorValidBundle (correctness) | 67.36M | 46.87M | 0.70 | 67.36..67.36M | 46.87..46.87M |
| dafnybench/DafnyProjects_tmp_tmp2acw_s4s_RawSort.dfy | rawsort (correctness) | 11.04M | 31.14M | 2.82 | 11.04..11.04M | 31.14..31.14M |
| kondo/paxos/sync | PaxosProof.InvNextChosenImpliesProposingLeaderHearsChosenBallotP1bStep (correctness) | 21.92M | 11.27M | 0.51 | 21.92..21.92M | 11.27..11.27M |
| kondo/flexPaxos/sync | PaxosProof.InvNextChosenImpliesProposingLeaderHearsChosenBallot (correctness) | 13.04M | 4.07M | 0.31 | 13.04..13.04M | 4.07..4.07M |
| kondo/flexPaxos/sync | PaxosProof.InvNextChosenImpliesProposingLeaderHearsChosenBallotP1bStep (correctness) | 18.11M | 12.12M | 0.67 | 18.11..18.11M | 12.12..12.12M |
| kondo/paxos/sync | PaxosProof.InvNextLeaderHearedImpliesProposed (correctness) | 15.53M | 10.84M | 0.70 | 15.53..15.53M | 10.84..10.84M |
| kondo/paxos/sync | PaxosProof.InvNextLearnerReceivedAcceptImpliesProposed (correctness) | 8.47M | 4.38M | 0.52 | 8.47..8.47M | 4.38..4.38M |
| kondo/paxos/sync | PaxosProof.InvNextLeaderHighestHeardToPromisedRangeHasNoAccepts (correctness) | 8.32M | 12.11M | 1.45 | 8.32..8.32M | 12.11..12.11M |
| lit/dafny4/UnionFind.dfy:refresh | M3.UnionFind.Join (correctness) (assertion batch 148) | 3.12M | 6.20M | 1.99 | 3.12..3.12M | 6.20..6.20M |
| kondo/flexPaxos/sync | PaxosProof.InvNextLeaderHighestHeardUpperBound (correctness) | 5.08M | 2.22M | 0.44 | 5.08..5.08M | 2.22..2.22M |
| kondo/paxos/sync | PaxosProof.InvNextChosenImpliesProposingLeaderHearsChosenBallot (correctness) | 12.13M | 14.39M | 1.19 | 12.13..12.13M | 14.39..14.39M |
| lit/VSI-Benchmarks/b4.dfy:refresh | Map.RemoveNonFirst (correctness) | 12.46M | 10.57M | 0.85 | 12.46..12.46M | 10.57..10.57M |
| dafnybench/dafny_experiments_tmp_tmpz29_3_3i_circuit.dfy | BackwardConnections.CombineBackconnsHelper (correctness) | 9.40M | 11.24M | 1.20 | 9.40..9.40M | 11.24..11.24M |
| lit/dafny4/UnionFind.dfy:refresh | M1.UnionFind.New (correctness) | 2.60M | 4.40M | 1.69 | 2.60..2.60M | 4.40..4.40M |
| kondo/flexPaxos/sync | PaxosProof.InvNextLeaderHighestHeardToPromisedRangeHasNoAccepts (correctness) | 15.44M | 14.27M | 0.92 | 15.44..15.44M | 14.27..14.27M |
| lit/dafny4/UnionFind.dfy:refresh | M2.UnionFind.FindAux (correctness) | 16.51M | 15.65M | 0.95 | 16.51..16.51M | 15.65..15.65M |
| lit/dafny4/UnionFind.dfy:refresh | M3.UnionFind.Join (correctness) (assertion batch 123) | 2.71M | 1.87M | 0.69 | 2.71..2.71M | 1.87..1.87M |
| lit/dafny4/UnionFind.dfy:refresh | M3.UnionFind.Join (correctness) (assertion batch 168) | 0.27M | 1.04M | 3.83 | 0.27..0.27M | 1.04..1.04M |
| lit/dafny4/UnionFind.dfy:refresh | M3.UnionFind.Join (correctness) (assertion batch 113) | 0.98M | 0.28M | 0.28 | 0.98..0.98M | 0.28..0.28M |
| kondo/flexPaxos/sync | PaxosProof.InvNextChosenValImpliesAcceptorOnlyAcceptsVal (correctness) | 1.48M | 2.07M | 1.40 | 1.48..1.48M | 2.07..2.07M |
| kondo/paxos/sync | PaxosProof.InvNextChosenValImpliesAcceptorOnlyAcceptsVal (correctness) | 1.99M | 1.45M | 0.73 | 1.99..1.99M | 1.45..1.45M |

## Per job (proofs among the affected VCs)

| job | VCs | master | PR | PR vs master |
|---|---:|---:|---:|---:|
| kondo/flexPaxos/sync | 72 | 363.61M | 454.61M | +25.0% |
| kondo/paxos/sync | 71 | 280.93M | 172.42M | -38.6% |
| lit/dafny4/UnionFind.dfy:refresh | 323 | 71.62M | 74.83M | +4.5% |
| lit/VSI-Benchmarks/b4.dfy:refresh | 65 | 20.68M | 18.70M | -9.6% |
| lit/git-issues/git-issue-3855.dfy:pinned | 81 | 11.87M | 11.88M | +0.1% |
| lit/vstte2012/BreadthFirstSearch.dfy:refresh | 134 | 11.71M | 11.70M | -0.1% |
| dafnybench/DafnyProjects_tmp_tmp2acw_s4s_RawSort.dfy | 3 | 11.09M | 31.20M | +181.3% |
| dafnybench/dafny_experiments_tmp_tmpz29_3_3i_circuit.dfy | 18 | 10.52M | 12.35M | +17.5% |
| lit/examples/induction-principle-code/EliminateMulZero.dfy:refresh | 26 | 5.72M | 5.68M | -0.7% |
| lit/comp/rust/loops.dfy:refresh | 4 | 5.65M | 5.65M | -0.0% |
| std/JSON/Serializer.dfy | 21 | 4.72M | 4.73M | +0.1% |
| kondo/shardedKvBatched/manual | 33 | 4.09M | 4.06M | -0.9% |
| lit/examples/induction-principle-code/VarUnchanged.dfy:refresh | 28 | 3.73M | 3.72M | -0.3% |
| lit/examples/induction-principle-code/Equiv.dfy:refresh | 26 | 3.63M | 3.65M | +0.5% |
| kondo/shardedKv/manual | 32 | 3.54M | 3.65M | +3.0% |
| lit/dafny4/NipkowKlein-chapter7.dfy:refresh | 26 | 3.49M | 3.39M | -3.0% |
| lit/examples/induction-principle-code/Pure.dfy:refresh | 23 | 3.46M | 3.48M | +0.6% |
| lit/cloudmake/CloudMake-ParallelBuilds.dfy:refresh | 28 | 3.09M | 3.19M | +3.3% |
| std/JSON/Deserializer.dfy | 15 | 2.52M | 2.53M | +0.1% |
| kondo/shardedKvBatched/sync | 19 | 2.28M | 2.29M | +0.2% |
| std/JSON/Spec.dfy | 10 | 2.22M | 2.21M | -0.3% |
| std/JSON/API.dfy | 4 | 2.03M | 2.03M | +0.0% |
| lit/examples/Simple_compiler/Compiler.dfy:refresh | 13 | 1.76M | 1.71M | -2.9% |
| dafnybench/fv2020-tms_tmp_tmpnp85b47l_modeling_concurrency_safety.dfy | 12 | 1.72M | 1.64M | -4.5% |
| lit/dafny0/Maps.dfy:refresh | 48 | 1.38M | 1.39M | +0.5% |
| kondo/shardedKv/sync | 19 | 1.13M | 1.13M | +0.2% |
| lit/dafny2/COST-verif-comp-2011-4-FloydCycleDetect.dfy:refresh | 1 | 1.03M | 1.03M | +0.0% |
| std/Strings.dfy | 22 | 0.98M | 1.32M | +34.3% |
| lit/dafny1/BDD.dfy:refresh | 5 | 0.97M | 0.98M | +1.3% |
| lit/c++/maps.dfy:refresh | 6 | 0.83M | 0.78M | -6.0% |
| dafnybench/dafny-programs_tmp_tmpcwodh6qh_src_ticketsystem.dfy | 9 | 0.82M | 0.81M | -0.9% |
| lit/examples/induction-principle-code/PureNoInductionPrinciple.dfy:refresh | 2 | 0.80M | 0.76M | -5.1% |
| lit/dafny0/IMaps.dfy:refresh | 14 | 0.80M | 0.34M | -56.9% |
| lit/comp/Collections.dfy:refresh | 7 | 0.79M | 0.73M | -7.9% |
| lit/unicodecharsFalse/comp/Collections.dfy:refresh | 7 | 0.79M | 0.73M | -7.9% |
| libraries/JSON/Utils/Str.dfy | 14 | 0.66M | 0.65M | -0.5% |
| lit/dafny2/Z-BirthdayBook.dfy:refresh | 18 | 0.62M | 0.62M | +0.4% |
| lit/comp/rust/operators.dfy:refresh | 1 | 0.46M | 0.46M | -1.5% |
| lit/comp/CovariantCollections.dfy:pinned | 6 | 0.41M | 0.41M | +0.2% |
| std/Unicode/UnicodeEncodingForm.dfy | 2 | 0.39M | 0.38M | -1.6% |
| lit/examples/induction-principle-code/Interp.dfy:refresh | 3 | 0.38M | 0.38M | +0.1% |
| std/Unicode/UnicodeStringsWithUnicodeChar.dfy | 2 | 0.37M | 0.37M | +0.0% |
| lit/dafny4/KozenSilva.dfy:refresh | 8 | 0.36M | 0.36M | +0.2% |
| lit/comp/TypeDescriptors.dfy:refresh | 1 | 0.36M | 0.36M | +0.0% |
| std/Actions/Producers.dfy | 1 | 0.34M | 0.34M | -0.0% |
| std/JSON/ByteStrConversion.dfy | 3 | 0.33M | 0.51M | +54.1% |
| std/Parsers/String/StringParsers.dfy | 3 | 0.30M | 0.30M | +0.1% |
| libraries/Collections/Maps/Maps.dfy | 13 | 0.28M | 0.29M | +0.8% |
| libraries/dafny/Collections/Maps.dfy | 13 | 0.28M | 0.29M | +0.8% |
| std/Collections/Map.dfy | 13 | 0.28M | 0.28M | +0.9% |
| lit/dafny0/Computations.dfy:refresh | 10 | 0.23M | 0.23M | +0.3% |
| std/Collections/Imap.dfy | 11 | 0.21M | 0.21M | +0.5% |
| libraries/Collections/Maps/Imaps.dfy | 11 | 0.21M | 0.21M | +0.5% |
| libraries/dafny/Collections/Imaps.dfy | 11 | 0.21M | 0.21M | +0.5% |
| lit/dafny0/GeneralNewtypeCollections.dfy:pinned | 6 | 0.21M | 0.21M | +0.4% |
| lit/dafny0/GeneralNewtypeCollectionsGeneric.dfy:pinned | 6 | 0.19M | 0.20M | +0.4% |
| lit/comp/Comprehensions.dfy:refresh | 4 | 0.19M | 0.19M | +0.1% |
| lit/unicodecharsFalse/comp/Comprehensions.dfy:refresh | 4 | 0.19M | 0.19M | +0.1% |
| lit/comp/ComprehensionsNewSyntax.dfy:refresh | 3 | 0.19M | 0.19M | +0.5% |
| lit/comp/NativeNumbers.dfy:refresh | 1 | 0.18M | 0.18M | +0.5% |
| lit/unicodecharsFalse/comp/NativeNumbers.dfy:refresh | 1 | 0.18M | 0.18M | +0.5% |
| lit/dafny0/TypeAdjustments.dfy:pinned | 5 | 0.15M | 0.15M | +0.4% |
| lit/comp/Poly.dfy:refresh | 2 | 0.15M | 0.15M | +0.6% |
| lit/dafny4/ExpandedGuardedness.dfy:refresh | 2 | 0.14M | 0.14M | +0.1% |
| lit/dafny4/git-issue63.dfy:refresh | 6 | 0.14M | 0.14M | +0.4% |
| lit/dafny4/git-issue167.dfy:refresh | 2 | 0.14M | 0.14M | +0.8% |
| lit/dafny0/DiscoverBounds.dfy:refresh | 3 | 0.13M | 0.13M | +0.4% |
| lit/comp/rust/traits.dfy:refresh | 1 | 0.13M | 0.13M | +0.0% |
| lit/dafny0/Wellfounded.dfy:refresh | 3 | 0.12M | 0.12M | +0.3% |
| libraries/dafny/Collections/Seqs.dfy | 1 | 0.12M | 0.12M | +0.4% |
| lit/dafny4/Bug68.dfy:refresh | 7 | 0.12M | 0.12M | +0.4% |
| lit/comp/Calls.dfy:refresh | 2 | 0.11M | 0.11M | +0.2% |
| lit/comp/firstSteps/6_Calls-VariableCapture.dfy:refresh | 2 | 0.11M | 0.11M | +0.2% |
| std/Parsers/Core/Parsers.dfy | 1 | 0.11M | 0.11M | +0.1% |
| lit/DafnyTests/TestAttribute/TestAttribute.dfy:refresh | 5 | 0.10M | 0.11M | +0.3% |
| std/Parsers/String/StringBuilders.dfy | 1 | 0.10M | 0.10M | +0.1% |
| lit/comp/MoreAutoInit.dfy:refresh | 3 | 0.10M | 0.10M | +0.2% |
| std/Parsers/Core/ParsersTheorems.dfy | 1 | 0.10M | 0.10M | +0.1% |
| lit/dafny4/git-issue133.dfy:refresh | 4 | 0.10M | 0.10M | +0.4% |
| lit/dafny0/TypeInferenceRefresh.dfy:pinned | 5 | 0.10M | 0.10M | +0.4% |
| lit/git-issues/git-issue-2380.dfy:refresh | 2 | 0.10M | 0.10M | +2.3% |
| lit/comp/rust/mapsubsets.dfy:pinned | 3 | 0.10M | 0.10M | +0.2% |
| dafnybench/iron-sync_tmp_tmps49o3tyz_lib_Base_MapRemove.dfy | 1 | 0.08M | 0.08M | +11.5% |
| lit/dafny0/Termination.dfy:refresh | 4 | 0.08M | 0.08M | +0.3% |
| lit/dafny4/git-issue70.dfy:refresh | 2 | 0.08M | 0.08M | +1.8% |
| lit/dafny0/GeneralNewtypeMemberVerify.dfy:pinned | 6 | 0.07M | 0.08M | +0.5% |
| lit/dafny0/ISets.dfy:refresh | 1 | 0.07M | 0.07M | +0.2% |
| lit/git-issues/git-issue-697b.dfy:refresh | 1 | 0.07M | 0.07M | +0.6% |
| lit/dafny4/Bug151.dfy:refresh | 4 | 0.07M | 0.07M | +0.4% |
| lit/dafny4/Bug91.dfy:refresh | 5 | 0.06M | 0.06M | +0.5% |
| lit/dafny4/Regression19.dfy:refresh | 2 | 0.06M | 0.06M | +0.6% |
| lit/git-issues/git-issue-1163.dfy:refresh | 1 | 0.06M | 0.06M | -0.6% |
| kondo/clientServer/manual | 2 | 0.05M | 0.05M | +0.4% |
| kondo/distributedLock/manual | 2 | 0.05M | 0.05M | +0.4% |
| kondo/lockServer/manual | 2 | 0.05M | 0.05M | +0.4% |
| kondo/ringLeaderElection/manual | 2 | 0.05M | 0.05M | +0.4% |
| kondo/simplifiedLeaderElection/manual | 2 | 0.05M | 0.05M | +0.4% |
| kondo/twoPhaseCommit/manual | 2 | 0.05M | 0.05M | +0.4% |
| kondo/twoPhaseCommit/paper-version | 2 | 0.05M | 0.05M | +0.4% |
| dafnybench/verification-class_tmp_tmpz9ik148s_2022_chapter05-distributed-state-machines_exercises_UtilitiesLibrary.dfy | 1 | 0.05M | 0.05M | +1.1% |
| lit/dafny0/SubsetTypes.dfy:pinned | 1 | 0.05M | 0.05M | +0.2% |
| lit/comp/AutoInit.dfy:refresh | 1 | 0.05M | 0.05M | +0.1% |
| lit/dafny4/git-issue195.dfy:refresh | 1 | 0.05M | 0.05M | +0.1% |
| lit/git-issues/git-issue-1158.dfy:refresh | 1 | 0.04M | 0.04M | +0.4% |
| std/Parsers/Core/ParsersBuilders.dfy | 1 | 0.04M | 0.04M | +0.1% |
| lit/dafny4/Bug58.dfy:refresh | 3 | 0.04M | 0.04M | +0.6% |
| lit/dafny0/Compilation.dfy:refresh | 2 | 0.04M | 0.04M | +0.3% |
| lit/comp/rust/small/05-coerce.dfy:pinned | 2 | 0.04M | 0.04M | +0.3% |
| dafnybench/Clover_update_map.dfy | 2 | 0.04M | 0.04M | +0.3% |
| kondo/clientServer/sync | 1 | 0.04M | 0.04M | +0.4% |
| kondo/distributedLock/sync | 1 | 0.04M | 0.04M | +0.4% |
| kondo/lockServer/sync | 1 | 0.04M | 0.04M | +0.4% |
| kondo/ringLeaderElection/sync | 1 | 0.04M | 0.04M | +0.4% |
| kondo/simplifiedLeaderElection/sync | 1 | 0.04M | 0.04M | +0.4% |
| kondo/twoPhaseCommit/sync | 1 | 0.04M | 0.04M | +0.4% |
| lit/dafny0/SmallTests.dfy:refresh | 3 | 0.04M | 0.04M | +0.5% |
| lit/dafny4/Bug49.dfy:refresh | 2 | 0.04M | 0.04M | +0.3% |
| lit/dafny0/BoundedPolymorphismCompilation.dfy:pinned | 2 | 0.04M | 0.04M | +0.3% |
| lit/dafny0/ReadsOnMethods.dfy:refresh | 2 | 0.04M | 0.04M | +0.4% |
| lit/dafny4/git-issue158.dfy:refresh | 1 | 0.03M | 0.03M | -0.8% |
| lit/dafny0/GeneralNewtypeMemberCompile.dfy:pinned | 2 | 0.03M | 0.03M | +0.4% |
| lit/dafny4/Bug160.dfy:refresh | 2 | 0.03M | 0.03M | +0.4% |
| lit/comp/rust/small/06-type-bounds.dfy:pinned | 2 | 0.03M | 0.03M | +0.4% |
| lit/dafny4/Bug54.dfy:refresh | 2 | 0.03M | 0.03M | +0.5% |
| lit/dafny4/git-issue75.dfy:refresh | 2 | 0.03M | 0.03M | +0.5% |
| lit/dafny0/GeneralNewtypeVerify.dfy:pinned | 1 | 0.03M | 0.03M | +0.2% |
| lit/git-issues/git-issue-755.dfy:refresh | 1 | 0.03M | 0.03M | +0.9% |
| lit/comp/Arrays.dfy:refresh | 1 | 0.03M | 0.03M | +0.2% |
| lit/unicodecharsFalse/comp/Arrays.dfy:refresh | 1 | 0.03M | 0.03M | +0.2% |
| lit/git-issues/git-issue-3873.dfy:refresh | 1 | 0.03M | 0.03M | +0.3% |
| lit/git-issues/git-issue-6535.dfy:refresh | 1 | 0.03M | 0.03M | +0.4% |
| lit/git-issues/git-issue-1479.dfy:refresh | 1 | 0.03M | 0.03M | +0.3% |
| lit/git-issues/git-issue-1875.dfy:refresh | 1 | 0.03M | 0.03M | +1.0% |
| lit/comp/Class.dfy:refresh | 1 | 0.02M | 0.02M | +0.4% |
| lit/hofs/Apply.dfy:refresh | 1 | 0.02M | 0.02M | +0.3% |
| lit/dafny0/TypeParameters.dfy:refresh | 1 | 0.02M | 0.02M | +0.3% |
| lit/dafny4/git-issue176.dfy:refresh | 1 | 0.02M | 0.02M | +0.3% |
| lit/dafny0/Datatypes.dfy:refresh | 1 | 0.02M | 0.02M | +0.3% |
| lit/dafny0/RuntimeTypeTests0.dfy:refresh | 1 | 0.02M | 0.02M | +0.3% |
| lit/git-issues/git-issue-3320.dfy:refresh | 1 | 0.02M | 0.02M | +0.3% |
| lit/git-issues/git-issue-1165.dfy:refresh | 1 | 0.02M | 0.02M | +0.3% |
| lit/git-issues/git-issue-336.dfy:refresh | 1 | 0.02M | 0.02M | +0.4% |
| lit/dafny0/BoundedPolymorphismVerification.dfy:pinned | 1 | 0.02M | 0.02M | +0.4% |
| lit/dafny4/git-issue15.dfy:refresh | 1 | 0.02M | 0.02M | +0.4% |
| lit/dafny0/DatatypeUpdate.dfy:pinned | 1 | 0.01M | 0.01M | +0.4% |
| lit/dafny4/git-issue44.dfy:refresh | 1 | 0.01M | 0.01M | +0.5% |
| lit/dafny4/Bug162.dfy:refresh | 1 | 0.01M | 0.01M | +0.5% |
| lit/dafny0/Compilation.legacy.dfy:pinned | 1 | 0.01M | 0.01M | +0.5% |
| lit/triggers/auto-triggers-fix-an-issue-listed-in-the-ironclad-notebook.dfy:refresh | 1 | 0.01M | 0.01M | +0.5% |
| lit/dafny4/Regression12.dfy:refresh | 1 | 0.01M | 0.01M | +0.5% |
| lit/dafny4/git-issue27.dfy:refresh | 1 | 0.01M | 0.01M | +0.5% |
| lit/dafny4/Bug108.dfy:refresh | 1 | 0.01M | 0.01M | +0.5% |
| lit/dafny0/NonZeroInitializationCompile.dfy:refresh | 1 | 0.01M | 0.01M | +0.6% |
| lit/dafny0/TypeSynonyms.dfy:refresh | 1 | 0.01M | 0.01M | +0.6% |
| lit/git-issues/git-issue-3883.dfy:refresh | 1 | 0.01M | 0.01M | +0.6% |
| lit/git-issues/git-issue-3059.dfy:refresh | 1 | 0.01M | 0.01M | +0.7% |

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
| A/A: master2 vs master (same input, another process) | 156 | 1570 | +0.0% [-0.0%, +0.0%] | +0.0% [-0.0%, +0.0%] | +0.0% [-0.0%, +0.0%] | 0 |
| pr vs master | 156 | 1570 | +0.6% [-30.1%, +26.5%] | -0.0% [-0.6%, +0.4%] | +0.5% [+0.1%, +1.2%] | 4 |

## Comparisons over the external programs' affected proofs

| comparison | programs | VCs | total | geomean over VCs | per program | verdict flips at limit |
|---|---:|---:|---|---|---|---:|
| A/A: master2 vs master (same input, another process) | 32 | 375 | +0.0% [+0.0%, +0.0%] | +0.0% [+0.0%, +0.0%] | +0.0% [+0.0%, +0.0%] | 0 |
| pr vs master | 32 | 375 | +0.7% [-36.7%, +85.8%] | -0.6% [-1.6%, +1.2%] | +1.6% [+0.0%, +4.2%] | 4 |

## Alternative sound encodings, over the same proofs

restrict: elements defined everywhere, `$ArbitraryBoxValue` outside the domain. domguard: the PR's axiom guarded by `Map#Domain(Map#Glue(a, b, t))`. eager: the PR's axiom plus the trigger `{ Map#Glue(a, b, t), Set#IsMember(a, bx) }`.

| encoding | programs | VCs | total vs master | geomean over VCs vs master | per program vs master | per program vs PR | verdict flips vs master at limit |
|---|---:|---:|---|---|---|---|---:|
| pr | 156 | 1570 | +0.6% [-29.5%, +26.3%] | -0.0% [-0.6%, +0.4%] | +0.5% [+0.1%, +1.2%] |  | 6 |
| master2 | 156 | 1570 | +0.0% [-0.0%, +0.0%] | +0.0% [-0.0%, +0.0%] | +0.0% [-0.0%, +0.0%] | -0.5% [-1.1%, -0.1%] | 0 |

master2: largest differences from the PR

| job | VC | master | PR | master2 |
|---|---|---:|---:|---:|
| kondo/flexPaxos/sync | PaxosProof.InvNextLearnerReceivedAcceptImpliesAccepted (correctness) | 45.53M | 279.76M | 45.53M |
| kondo/paxos/sync | PaxosProof.InvNextLeaderReceivedPromisesImpliesAcceptorState (correctness) | 171.77M | 29.81M | 171.77M |
| kondo/flexPaxos/sync | PaxosProof.InvNextLeaderReceivedPromisesImpliesAcceptorState (correctness) | 174.48M | 70.51M | 174.48M |
| kondo/paxos/sync | PaxosProof.InvNextAcceptorValidBundle (correctness) | 14.76M | 61.59M | 14.76M |
| kondo/flexPaxos/sync | PaxosProof.InvNextAcceptorValidBundle (correctness) | 67.36M | 46.87M | 67.36M |
| dafnybench/DafnyProjects_tmp_tmp2acw_s4s_RawSort.dfy | rawsort (correctness) | 11.04M | 31.14M | 11.04M |
