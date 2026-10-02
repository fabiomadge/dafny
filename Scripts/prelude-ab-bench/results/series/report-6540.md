# #6540 A/B benchmark (public corpora, seed 1)

Seeds per (VC, prelude): 1 (1; 0 is Dafny's default). VCs: 27063 in 2077 jobs; **3232 affected** (master and PR counts differ), 23831 unaffected (identical counts under master and PR for every seed).

## Proof cost over affected VCs that pass everywhere

Totals are sums of per-VC means over seeds. "Per program" averages each program's own VC geomean, so a
program with hundreds of VCs weighs no more than one with two. Brackets are 95% bootstrap intervals that
resample programs, not VCs.

| group | programs | VCs | largest program | total PR/master | geomean over VCs | per program |
|---|---:|---:|---|---|---|---|
| all but synth | 97 | 3182 | std/JSON/ZeroCopy/Deserializer.dfy (31% of VCs) | -8.9% [-39.2%, +37.1%] | +0.3% [-0.2%, +1.1%] | +2.0% [+1.0%, +3.3%] |
| dafnybench | 1 | 12 | dafnybench/dafny_experiments_tmp_tmpz29_3_3i_circuit.dfy (100% of VCs) | +88.5% [+88.5%, +88.5%] | +6.8% [+6.8%, +6.8%] | +6.8% [+6.8%, +6.8%] |
| kondo | 19 | 370 | kondo/flexPaxos/sync (17% of VCs) | -17.9% [-81.0%, +86.4%] | +0.2% [-3.7%, +3.7%] | +0.1% [-2.8%, +2.2%] |
| libraries | 7 | 1098 | libraries/JSON/ZeroCopy/Deserializer.dfy (82% of VCs) | +2.6% [-0.2%, +2.7%] | +0.4% [+0.3%, +1.4%] | +0.7% [+0.3%, +1.3%] |
| lit | 57 | 246 | lit/dafny4/FlyingRobots.dfy (11% of VCs) | -8.9% [-11.0%, +1.3%] | +0.8% [-0.4%, +2.2%] | +3.2% [+2.0%, +5.1%] |
| std | 13 | 1456 | std/JSON/ZeroCopy/Deserializer.dfy (68% of VCs) | +0.6% [-2.0%, +0.9%] | +0.2% [+0.0%, +0.4%] | +0.1% [-0.2%, +0.2%] |

50 affected VCs fail (a verification error) in some run; their cost is the solver's search for a counterexample, reported separately:

| job | VC | master mean (min..max) | PR mean (min..max) |
|---|---|---|---|
| lit/comp/TypeParams.dfy:refresh | Standard (correctness) | 832.98M (832.98..832.98) | 818.64M (818.64..818.64) |
| lit/dafny0/FunctionSpecifications.dfy:refresh | GoodPost (well-formedness) | 311.14M (311.14..311.14) | 310.76M (310.76..310.76) |
| lit/cli/defaultTimeLimit.dfy:refresh | Foo (correctness) | 298.84M (298.84..298.84) | 258.12M (258.12..258.12) |
| kondo/paxos/sync | PaxosProof.InvNextLearnerReceivedAcceptImpliesAccepted (correctness) | 293.81M (293.81..293.81) | 48.32M (48.32..48.32) |
| libraries/dafny/Collections/Seqs.dfy | Dafny.Collections.Seq.LemmaMapDistributesOverConcat (correctness) | 243.34M (243.34..243.34) | 275.00M (275.00..275.00) |
| dafnybench/dafny_experiments_tmp_tmpz29_3_3i_circuit.dfy | CombineCircuits.CombineCircuitsCorrect (correctness) | 214.71M (214.71..214.71) | 230.38M (230.38..230.38) |
| kondo/paxos/sync | PaxosProof.InvNextLeaderReceivedPromisesImpliesAcceptorState (correctness) | 171.77M (171.77..171.77) | 283.81M (283.81..283.81) |
| libraries/dafny/Collections/Seqs.dfy | Dafny.Collections.Seq.LemmaFilterDistributesOverConcat (correctness) (assertion batch 2) | 171.40M (171.40..171.40) | 180.25M (180.25..180.25) |
| libraries/JSON/ZeroCopy/Deserializer.dfy | JSON.ZeroCopy.Deserializer.Core.TryStructural (well-formedness) | 33.84M (33.84..33.84) | 26.44M (26.44..26.44) |
| lit/dafny1/Rippling.legacy.dfy:refresh | P2 (correctness) | 22.88M (22.88..22.88) | 21.45M (21.45..21.45) |

## Total proof RU per seed (affected VCs that pass everywhere)

| prelude | seed 1 | mean | sd |
|---|---:|---:|---:|
| master | 1303.1M | 1303.1M | 0.0M |
| pr | 1187.1M | 1187.1M | 0.0M |

## Solver time over those proofs (sum of per-VC means, seconds)

| group | master | PR |
|---|---:|---:|
| all | 976.5 | 752.1 |
| lit | 45.5 | 43.2 |
| std | 187.6 | 170.6 |

## Distribution of per-VC cost ratios over those proofs (mean over seeds)

| ratio bucket | PR/master |
|---|---:|
| < 0.5x | 9 |
| 0.5-0.8x | 9 |
| 0.8-0.95x | 18 |
| 0.95-1.05x | 3068 |
| 1.05-1.25x | 50 |
| 1.25-2x | 18 |
| 2-4x | 8 |
| >= 4x | 2 |

## Verdict changes at each job's limit (seeds passing out of 1)

| job | VC | limit | master ok | PR ok | master RU | PR RU |
|---|---|---:|---:|---:|---:|---:|
| kondo/flexPaxos/sync | PaxosProof.InvNextAcceptorValidBundle (correctness) | 50M | 0 | 1 | 67.36M | 30.81M |
| kondo/flexPaxos/sync | PaxosProof.InvNextChosenImpliesProposingLeaderHearsChosenBallotP2bStep (correctness) | 50M | 1 | 0 | 16.81M | 55.68M |
| kondo/flexPaxos/sync | PaxosProof.InvNextLeaderReceivedPromisesImpliesAcceptorState (correctness) | 50M | 0 | 1 | 174.48M | 23.11M |
| kondo/flexPaxos/sync | PaxosProof.InvNextLearnerReceivedAcceptImpliesAccepted (correctness) | 50M | 1 | 0 | 45.53M | 75.23M |
| kondo/paxos/sync | PaxosProof.InvNextChosenImpliesProposingLeaderHearsChosenBallotP2bStep (correctness) | 50M | 1 | 0 | 22.37M | 105.73M |
| kondo/paxos/sync | PaxosProof.InvNextLearnerReceivedAcceptImpliesAccepted (correctness) | 50M | 0 | 1 | 293.81M | 48.32M |
| kondo/twoPhaseCommit/manual | TwoPCInvariantProof.InvNextLeaderVotesValid (correctness) | 50M | 1 | 0 | 0.27M | 0.31M |
| kondo/twoPhaseCommit/paper-version | TwoPCInvariantProof.InvNextLeaderVotesValid (correctness) | 50M | 1 | 0 | 0.28M | 0.30M |
| kondo/twoPhaseCommit/sync | TwoPCInvariantProof.InvNextLeaderTallyReflectsPreferences (correctness) | 50M | 0 | 1 | 131.29M | 0.87M |

## Largest changes among those proofs (by |PR - master| mean RU)

| job | VC | master | PR | PR/master | min..max master | min..max PR |
|---|---|---:|---:|---:|---|---|
| kondo/flexPaxos/sync | PaxosProof.InvNextLeaderReceivedPromisesImpliesAcceptorState (correctness) | 174.48M | 23.11M | 0.13 | 174.48..174.48M | 23.11..23.11M |
| kondo/twoPhaseCommit/sync | TwoPCInvariantProof.InvNextLeaderTallyReflectsPreferences (correctness) | 131.29M | 0.87M | 0.01 | 131.29..131.29M | 0.87..0.87M |
| kondo/paxos/sync | PaxosProof.InvNextChosenImpliesProposingLeaderHearsChosenBallotP2bStep (correctness) | 22.37M | 105.73M | 4.73 | 22.37..22.37M | 105.73..105.73M |
| kondo/flexPaxos/sync | PaxosProof.InvNextChosenImpliesProposingLeaderHearsChosenBallotP2bStep (correctness) | 16.81M | 55.68M | 3.31 | 16.81..16.81M | 55.68..55.68M |
| kondo/flexPaxos/sync | PaxosProof.InvNextAcceptorValidBundle (correctness) | 67.36M | 30.81M | 0.46 | 67.36..67.36M | 30.81..30.81M |
| kondo/paxos/sync | PaxosProof.InvNextAcceptorValidBundle (correctness) | 14.76M | 49.78M | 3.37 | 14.76..14.76M | 49.78..49.78M |
| kondo/flexPaxos/sync | PaxosProof.InvNextLearnerReceivedAcceptImpliesAccepted (correctness) | 45.53M | 75.23M | 1.65 | 45.53..45.53M | 75.23..75.23M |
| kondo/paxos/sync | PaxosProof.InvNextLeaderHearedImpliesProposed (correctness) | 15.53M | 40.03M | 2.58 | 15.53..15.53M | 40.03..40.03M |
| dafnybench/dafny_experiments_tmp_tmpz29_3_3i_circuit.dfy | BackwardConnections.CombineBackconnsHelper (correctness) | 9.40M | 18.50M | 1.97 | 9.40..9.40M | 18.50..18.50M |
| kondo/flexPaxos/sync | PaxosProof.InvNextLeaderHighestHeardToPromisedRangeHasNoAccepts (correctness) | 15.44M | 7.63M | 0.49 | 15.44..15.44M | 7.63..7.63M |
| lit/dafny4/FlyingRobots.dfy:refresh | FlyRobotArmy_Recursively (correctness) | 9.57M | 2.53M | 0.26 | 9.57..9.57M | 2.53..2.53M |
| kondo/flexPaxos/sync | PaxosProof.InvNextChosenImpliesProposingLeaderHearsChosenBallot (correctness) | 13.04M | 6.03M | 0.46 | 13.04..13.04M | 6.03..6.03M |
| kondo/paxos/sync | PaxosProof.InvNextChosenImpliesProposingLeaderHearsChosenBallot (correctness) | 12.13M | 5.94M | 0.49 | 12.13..12.13M | 5.94..5.94M |
| libraries/JSON/ZeroCopy/Deserializer.dfy | JSON.ZeroCopy.Deserializer.Numbers.Exp (well-formedness) (assertion batch 16) | 0.84M | 4.88M | 5.83 | 0.84..0.84M | 4.88..4.88M |
| kondo/flexPaxos/sync | PaxosProof.InvNextLearnerReceivedAcceptImpliesProposed (correctness) | 2.32M | 5.39M | 2.32 | 2.32..2.32M | 5.39..5.39M |
| std/JSON/ZeroCopy/Deserializer.dfy | Std.JSON.ZeroCopy.Deserializer.Sequences.AppendLast (well-formedness) (assertion batch 29) | 2.73M | 5.58M | 2.04 | 2.73..2.73M | 5.58..5.58M |
| kondo/simplifiedLeaderElection/sync | ToyLeaderElectionProof.InvNextReceivedVotesValid (correctness) | 9.08M | 6.73M | 0.74 | 9.08..9.08M | 6.73..6.73M |
| std/JSON/ZeroCopy/Deserializer.dfy | Std.JSON.ZeroCopy.Deserializer.Core.Structural (well-formedness) (assertion batch 5) | 3.57M | 1.35M | 0.38 | 3.57..3.57M | 1.35..1.35M |
| kondo/flexPaxos/sync | PaxosProof.InvNextLeaderHighestHeardUpperBound (correctness) | 5.08M | 3.04M | 0.60 | 5.08..5.08M | 3.04..3.04M |
| kondo/flexPaxos/sync | PaxosProof.InvNextChosenImpliesProposingLeaderHearsChosenBallotP1bStep (correctness) | 18.11M | 20.12M | 1.11 | 18.11..18.11M | 20.12..20.12M |
| libraries/JSON/ZeroCopy/Deserializer.dfy | JSON.ZeroCopy.Deserializer.Sequences.AppendLast (well-formedness) (assertion batch 31) | 1.12M | 2.79M | 2.50 | 1.12..1.12M | 2.79..2.79M |
| kondo/paxos/sync | PaxosProof.InvNextChosenImpliesProposingLeaderHearsChosenBallotP1bStep (correctness) | 21.92M | 20.27M | 0.92 | 21.92..21.92M | 20.27..20.27M |
| kondo/paxos/sync | PaxosProof.InvNextLeaderHighestHeardToPromisedRangeHasNoAccepts (correctness) | 8.32M | 6.68M | 0.80 | 8.32..8.32M | 6.68..6.68M |
| kondo/paxos/sync | PaxosProof.InvNextChosenValImpliesLeaderOnlyHearsVal (correctness) | 10.74M | 11.88M | 1.11 | 10.74..10.74M | 11.88..11.88M |
| kondo/paxos/sync | PaxosProof.InvNextLeaderValidReceivedPromises (correctness) | 0.60M | 1.71M | 2.85 | 0.60..0.60M | 1.71..1.71M |

## Per job (proofs among the affected VCs)

| job | VCs | master | PR | PR vs master |
|---|---:|---:|---:|---:|
| kondo/flexPaxos/sync | 63 | 377.74M | 247.53M | -34.5% |
| std/JSON/ZeroCopy/Deserializer.dfy | 983 | 236.56M | 238.82M | +1.0% |
| libraries/JSON/ZeroCopy/Deserializer.dfy | 899 | 209.73M | 215.43M | +2.7% |
| kondo/twoPhaseCommit/sync | 22 | 135.05M | 4.35M | -96.8% |
| kondo/paxos/sync | 61 | 128.81M | 264.86M | +105.6% |
| lit/dafny4/FlyingRobots.dfy:refresh | 27 | 58.59M | 51.58M | -12.0% |
| kondo/simplifiedLeaderElection/sync | 19 | 21.20M | 18.90M | -10.9% |
| std/JSON/ZeroCopy/Serializer.dfy | 142 | 18.07M | 18.12M | +0.3% |
| std/Actions/BulkActions.dfy | 76 | 15.70M | 15.55M | -1.0% |
| dafnybench/dafny_experiments_tmp_tmpz29_3_3i_circuit.dfy | 12 | 10.30M | 19.40M | +88.5% |
| kondo/ringLeaderElection/sync | 8 | 8.68M | 9.69M | +11.6% |
| std/Parsers/String/StringParsers.dfy | 148 | 8.61M | 8.41M | -2.4% |
| libraries/JSON/ZeroCopy/Serializer.dfy | 44 | 8.06M | 8.12M | +0.8% |
| lit/cloudmake/CloudMake-CachedBuilds.dfy:refresh | 25 | 5.79M | 5.50M | -5.0% |
| kondo/lockServer/manual | 24 | 4.04M | 4.24M | +4.8% |
| kondo/shardedKvBatched/manual | 22 | 3.66M | 3.48M | -4.9% |
| lit/cloudmake/CloudMake-ConsistentBuilds.legacy.dfy:refresh | 25 | 3.39M | 3.39M | -0.0% |
| kondo/shardedKv/manual | 22 | 3.12M | 3.33M | +6.5% |
| kondo/twoPhaseCommit/manual | 18 | 3.06M | 3.04M | -0.5% |
| std/Arithmetic/LittleEndianNat.dfy | 64 | 2.99M | 3.00M | +0.4% |
| kondo/twoPhaseCommit/paper-version | 18 | 2.78M | 2.93M | +5.4% |
| libraries/Collections/Sequences/LittleEndianNat.dfy | 64 | 2.66M | 2.67M | +0.4% |
| libraries/dafny/Collections/LittleEndianNat.dfy | 64 | 2.66M | 2.67M | +0.4% |
| lit/examples/induction-principle-code/EliminateMulZero.dfy:refresh | 6 | 2.46M | 2.43M | -1.4% |
| std/JSON/Utils/Cursors.dfy | 17 | 2.25M | 2.09M | -7.1% |
| libraries/JSON/Utils/Cursors.dfy | 17 | 2.18M | 2.16M | -1.1% |
| lit/cloudmake/CloudMake-ParallelBuilds.dfy:refresh | 14 | 2.14M | 2.15M | +0.3% |
| kondo/simplifiedLeaderElection/manual | 10 | 2.14M | 2.47M | +15.4% |
| kondo/shardedKvBatched/sync | 8 | 1.79M | 1.76M | -1.5% |
| kondo/ringLeaderElection/manual | 11 | 1.58M | 1.54M | -2.2% |
| kondo/lockServer/sync | 15 | 1.42M | 1.48M | +4.8% |
| lit/examples/Simple_compiler/Compiler.dfy:refresh | 6 | 1.27M | 1.27M | +0.6% |
| lit/dafny3/InfiniteTrees.dfy:pinned | 19 | 1.19M | 1.20M | +0.3% |
| std/Parsers/Core/ParsersTheorems.dfy | 17 | 1.10M | 1.10M | +0.1% |
| kondo/clientServer/sync | 10 | 1.09M | 1.10M | +0.6% |
| kondo/distributedLock/manual | 12 | 1.00M | 1.06M | +5.3% |
| kondo/clientServer/manual | 10 | 1.00M | 0.98M | -1.7% |
| std/JSON/API.dfy | 1 | 0.70M | 0.70M | +0.0% |
| kondo/shardedKv/sync | 9 | 0.66M | 0.66M | +0.5% |
| lit/dafny0/Twostate-Verification.dfy:refresh | 16 | 0.64M | 0.64M | +0.7% |
| lit/blogposts/TestGenerationWithInliningQuantifiedDefinitions.dfy:refresh | 7 | 0.61M | 0.68M | +11.5% |
| kondo/distributedLock/sync | 8 | 0.56M | 0.56M | -0.8% |
| lit/examples/induction-principle-code/Pure.dfy:refresh | 2 | 0.48M | 0.48M | +0.1% |
| std/JSON/ZeroCopy/API.dfy | 1 | 0.45M | 0.45M | +0.0% |
| lit/examples/induction-principle-code/Equiv.dfy:refresh | 3 | 0.43M | 0.44M | +2.3% |
| lit/examples/induction-principle-code/VarUnchanged.dfy:refresh | 2 | 0.39M | 0.39M | +0.6% |
| lit/blogposts/TestGenerationNoInliningEnumerativeDefinitions.dfy:refresh | 5 | 0.36M | 0.36M | +0.0% |
| libraries/dafny/Collections/Seqs.dfy | 6 | 0.35M | 0.35M | +0.5% |
| std/Actions/Producers.dfy | 1 | 0.34M | 0.34M | -0.0% |
| lit/dafny4/KozenSilva.dfy:refresh | 6 | 0.31M | 0.31M | +0.3% |
| lit/lambdas/StateMonad.dfy:pinned | 3 | 0.31M | 0.31M | +0.9% |
| lit/hofs/TreeMapSimple.dfy:refresh | 2 | 0.31M | 0.31M | +0.4% |
| lit/autoRevealDependencies/tree-map-simple.dfy:refresh | 2 | 0.30M | 0.31M | +2.9% |
| lit/dafny4/NipkowKlein-chapter7.dfy:refresh | 2 | 0.24M | 0.24M | -0.4% |
| std/Collections/Seq.dfy | 4 | 0.21M | 0.21M | -0.0% |
| libraries/Collections/Sequences/Seq.dfy | 4 | 0.18M | 0.19M | +0.8% |
| lit/dafny0/MoForallCompilation.dfy:refresh | 3 | 0.17M | 0.17M | +0.4% |
| lit/dafny4/Bug92.dfy:refresh | 9 | 0.08M | 0.08M | +2.5% |
| std/Parsers/Core/Parsers.dfy | 1 | 0.08M | 0.08M | +0.2% |
| lit/dafny4/git-issue133.dfy:refresh | 3 | 0.07M | 0.07M | +0.7% |
| lit/comp/rust/traits-datatypes.dfy:pinned | 3 | 0.07M | 0.07M | +0.6% |
| lit/comp/Comprehensions.dfy:refresh | 1 | 0.07M | 0.07M | +4.1% |
| lit/unicodecharsFalse/comp/Comprehensions.dfy:refresh | 1 | 0.07M | 0.07M | +4.1% |
| lit/comp/rust/datatypes.dfy:refresh | 1 | 0.07M | 0.07M | +0.6% |
| std/Actions/Consumers.dfy | 1 | 0.06M | 0.06M | +0.1% |
| lit/dafny0/DefaultParameters.dfy:refresh | 2 | 0.06M | 0.06M | +0.6% |
| lit/referrers/localsmemorylocation.dfy:pinned | 4 | 0.06M | 0.07M | +3.6% |
| lit/hofs/Monads.dfy:refresh | 3 | 0.06M | 0.06M | +1.0% |
| lit/git-issues/git-issue-6366.dfy:refresh | 1 | 0.05M | 0.05M | +0.7% |
| lit/referrers/memorylocations.dfy:pinned | 3 | 0.04M | 0.05M | +3.2% |
| lit/git-issues/git-issue-1212.dfy:refresh | 3 | 0.04M | 0.05M | +2.4% |
| lit/dafny1/Rippling.legacy.dfy:refresh | 3 | 0.04M | 0.04M | +4.8% |
| lit/dafny4/git-issue195.dfy:refresh | 2 | 0.03M | 0.03M | +1.7% |
| lit/dafny4/git-issue167.dfy:refresh | 1 | 0.03M | 0.03M | +1.6% |
| lit/dafny0/TypeInferenceRefresh.dfy:pinned | 3 | 0.02M | 0.02M | +2.3% |
| lit/ghost/AllowedGhostBindings.dfy:refresh | 2 | 0.02M | 0.02M | +1.6% |
| lit/dafny3/GenericSort.dfy:refresh | 3 | 0.02M | 0.02M | +3.2% |
| lit/dafny0/DecreasesTo0.dfy:refresh | 2 | 0.02M | 0.02M | +3.5% |
| lit/dafny0/GhostAutoInit.dfy:refresh | 2 | 0.02M | 0.02M | +1.7% |
| lit/dafny0/TypeAntecedents.dfy:refresh | 2 | 0.02M | 0.02M | +2.4% |
| lit/dafny4/git-issue40.dfy:refresh | 1 | 0.01M | 0.01M | +1.4% |
| lit/comp/Datatype.dfy:refresh | 1 | 0.01M | 0.01M | +1.8% |
| lit/dafny0/LetExpr.dfy:refresh | 1 | 0.01M | 0.01M | +1.9% |
| lit/git-issues/github-issue-1267.dfy:refresh | 1 | 0.01M | 0.01M | +2.3% |
| lit/dafny0/Fp64EqualityErrors.dfy:refresh | 1 | 0.01M | 0.01M | +3.1% |
| lit/dafny0/OpaqueFunctions.dfy:refresh | 1 | 0.01M | 0.01M | +2.6% |
| lit/git-issues/git-issue-1958.dfy:pinned | 1 | 0.01M | 0.01M | +5.8% |
| lit/dafny0/Fp32EqualityErrors.dfy:refresh | 1 | 0.01M | 0.01M | +3.3% |
| lit/dafny4/Bug67.dfy:refresh | 1 | 0.01M | 0.01M | +6.8% |
| lit/dafny4/git-issue5.dfy:refresh | 1 | 0.01M | 0.01M | +2.7% |
| lit/git-issues/git-issue-863.dfy:refresh | 1 | 0.01M | 0.01M | +10.7% |
| lit/dafny4/Bug72.dfy:refresh | 1 | 0.01M | 0.01M | +3.2% |
| lit/git-issues/git-issue-1180b.dfy:refresh | 1 | 0.01M | 0.01M | +27.7% |
| lit/dafny4/git-issue1.dfy:refresh | 1 | 0.01M | 0.01M | +3.6% |
| lit/dafny0/DecreasesTo1.dfy:refresh | 1 | 0.00M | 0.01M | +10.5% |
| lit/git-issues/git-issue-904.dfy:refresh | 1 | 0.00M | 0.01M | +46.9% |
| lit/git-issues/git-issue-3482.dfy:refresh | 1 | 0.00M | 0.00M | +1.8% |

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
| A/A: master2 vs master (same input, another process) | 97 | 3182 | +0.0% [-0.0%, +0.0%] | +0.0% [-0.0%, +0.0%] | +0.0% [-0.0%, +0.0%] | 0 |
| pr vs master | 97 | 3182 | -8.9% [-42.7%, +32.1%] | +0.3% [-0.2%, +1.0%] | +2.0% [+1.0%, +3.2%] | 6 |

## Comparisons over the external programs' affected proofs

| comparison | programs | VCs | total | geomean over VCs | per program | verdict flips at limit |
|---|---:|---:|---|---|---|---:|
| A/A: master2 vs master (same input, another process) | 27 | 1480 | +0.0% [+0.0%, +0.0%] | +0.0% [+0.0%, +0.0%] | +0.0% [+0.0%, +0.0%] | 0 |
| pr vs master | 27 | 1480 | -11.8% [-56.0%, +61.4%] | +0.4% [-1.3%, +2.4%] | +0.5% [-1.6%, +2.0%] | 6 |

## Alternative sound encodings, over the same proofs

restrict: elements defined everywhere, `$ArbitraryBoxValue` outside the domain. domguard: the PR's axiom guarded by `Map#Domain(Map#Glue(a, b, t))`. eager: the PR's axiom plus the trigger `{ Map#Glue(a, b, t), Set#IsMember(a, bx) }`.

| encoding | programs | VCs | total vs master | geomean over VCs vs master | per program vs master | per program vs PR | verdict flips vs master at limit |
|---|---:|---:|---|---|---|---|---:|
| pr | 97 | 3182 | -8.9% [-40.3%, +37.4%] | +0.3% [-0.2%, +1.1%] | +2.0% [+1.0%, +3.2%] |  | 9 |
| master2 | 97 | 3182 | +0.0% [-0.0%, +0.0%] | +0.0% [-0.0%, +0.0%] | +0.0% [-0.0%, +0.0%] | -2.0% [-3.2%, -1.0%] | 0 |

master2: largest differences from the PR

| job | VC | master | PR | master2 |
|---|---|---:|---:|---:|
| kondo/flexPaxos/sync | PaxosProof.InvNextLeaderReceivedPromisesImpliesAcceptorState (correctness) | 174.48M | 23.11M | 174.48M |
| kondo/twoPhaseCommit/sync | TwoPCInvariantProof.InvNextLeaderTallyReflectsPreferences (correctness) | 131.29M | 0.87M | 131.29M |
| kondo/paxos/sync | PaxosProof.InvNextChosenImpliesProposingLeaderHearsChosenBallotP2bStep (correctness) | 22.37M | 105.73M | 22.37M |
| kondo/flexPaxos/sync | PaxosProof.InvNextChosenImpliesProposingLeaderHearsChosenBallotP2bStep (correctness) | 16.81M | 55.68M | 16.81M |
| kondo/flexPaxos/sync | PaxosProof.InvNextAcceptorValidBundle (correctness) | 67.36M | 30.81M | 67.36M |
| kondo/paxos/sync | PaxosProof.InvNextAcceptorValidBundle (correctness) | 14.76M | 49.78M | 14.76M |
