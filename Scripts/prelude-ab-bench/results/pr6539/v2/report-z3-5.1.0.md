# Map#Glue prelude A/B benchmark

Seeds per (VC, prelude): 8 (0, 1, 2, 3, 4, 5, 6, 7; 0 is Dafny's default). VCs: 3330 in 159 jobs; **1023 affected** (master and PR counts differ), 2307 unaffected (identical counts under master and PR for every seed).
Unaffected VCs whose counts differ under the placebo: 5.

## Proof cost over affected VCs that pass everywhere

Totals are sums of per-VC means over seeds. "Per program" averages each program's own VC geomean, so a
program with hundreds of VCs weighs no more than one with two. Brackets are 95% bootstrap intervals that
resample programs, not VCs.

| group | programs | VCs | largest program | total PR/master | geomean over VCs | per program | placebo per program |
|---|---:|---:|---|---|---|---|---|
| all but synth | 63 | 930 | lit/dafny4/UnionFind.dfy (62% of VCs) | +13.6% [+4.6%, +25.5%] | +1.9% [+0.6%, +6.0%] | +1.6% [+0.3%, +3.0%] | +0.2% [-0.3%, +1.0%] |
| dafnybench | 7 | 19 | dafnybench/dafny_experiments_tmp_tmpz29_3_3i_circuit.dfy (68% of VCs) | +17.4% [+5.8%, +20.2%] | +3.2% [+1.2%, +12.5%] | +7.4% [+2.7%, +12.9%] | +2.4% [-1.8%, +9.7%] |
| kondo | 19 | 67 | kondo/shardedKvBatched/manual (25% of VCs) | +1.1% [+0.3%, +1.6%] | +0.7% [+0.5%, +1.0%] | +1.0% [+0.8%, +1.1%] | -0.1% [-0.2%, -0.1%] |
| lit | 34 | 833 | lit/dafny4/UnionFind.dfy (70% of VCs) | +13.9% [+0.4%, +37.4%] | +2.0% [+0.2%, +8.0%] | +0.8% [-1.2%, +2.7%] | -0.1% [-0.2%, +0.0%] |
| std | 3 | 11 | std/Collections/Imap.dfy (45% of VCs) | +1.0% [+0.2%, +1.4%] | +1.0% [+0.2%, +1.6%] | +0.8% [+0.2%, +1.6%] | +0.0% [+0.0%, +0.0%] |
| synth | 40 | 50 | synth/spec-01.dfy (6% of VCs) | +126.5% [+21.9%, +264.9%] | +28.3% [+13.8%, +48.9%] | +36.2% [+18.4%, +58.8%] | +1.3% [-0.4%, +3.5%] |

43 affected VCs fail (a verification error) in some run; their cost is the solver's search for a counterexample, reported separately:

| job | VC | master mean (min..max) | PR mean (min..max) | placebo mean |
|---|---|---|---|---|
| kondo/paxos/sync | PaxosProof.InvNextLeaderReceivedPromisesImpliesAcceptorState (correctness) | 136.35M (58.84..206.02) | 136.48M (58.84..206.02) | 136.66M |
| kondo/flexPaxos/sync | PaxosProof.InvNextChosenImpliesProposingLeaderHearsChosenBallotP2bStep (correctness) | 104.39M (10.46..287.12) | 106.77M (10.46..295.99) | 109.11M |
| lit/git-issues/git-issue-3855.dfy:pinned | Memory.dynMove (correctness) | 100.21M (50.40..203.39) | 145.08M (72.49..196.38) | 104.54M |
| kondo/flexPaxos/sync | PaxosProof.InvNextLearnerReceivedAcceptImpliesAccepted (correctness) | 89.65M (18.86..221.72) | 92.78M (18.86..233.48) | 95.82M |
| dafnybench/dafny_experiments_tmp_tmpz29_3_3i_circuit.dfy | CombineCircuits.CombineCircuitsCorrect (correctness) | 86.74M (63.43..142.55) | 112.21M (77.64..138.39) | 85.58M |
| kondo/paxos/sync | PaxosProof.InvNextLearnerReceivedAcceptImpliesAccepted (correctness) | 83.59M (14.12..217.89) | 84.14M (14.12..219.96) | 85.05M |
| lit/git-issues/git-issue-3855.dfy:pinned | Memory.dynCopy (correctness) | 3.70M (2.32..5.97) | 4.28M (2.32..7.55) | 3.68M |
| lit/git-issues/git-issue-3855.dfy:pinned | Main1 (correctness) | 3.37M (2.34..5.06) | 3.33M (2.48..5.06) | 3.37M |
| kondo/shardedKv/sync | ShardedKVProof.InvNextSafety (correctness) | 2.13M (0.83..4.51) | 2.04M (0.93..4.57) | 1.97M |
| lit/dafny0/TypeAdjustments.dfy:pinned | Comprehensions.Maps1 (correctness) | 0.59M (0.48..0.73) | 0.62M (0.48..0.83) | 0.59M |

## Total proof RU per seed (affected VCs that pass everywhere)

| prelude | seed 0 | seed 1 | seed 2 | seed 3 | seed 4 | seed 5 | seed 6 | seed 7 | mean | sd |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| master | 291.4M | 267.9M | 260.1M | 315.3M | 251.6M | 268.6M | 301.7M | 242.6M | 274.9M | 23.8M |
| pr | 327.3M | 322.9M | 281.4M | 321.7M | 320.7M | 356.4M | 569.9M | 362.0M | 357.8M | 83.4M |
| placebo | 293.1M | 266.2M | 262.3M | 294.0M | 247.3M | 284.1M | 313.3M | 247.7M | 276.0M | 22.3M |

## Solver time over those proofs (sum of per-VC means, seconds)

| group | master | PR | placebo |
|---|---:|---:|---:|
| all | 164.3 | 193.9 | 164.4 |
| lit | 141.2 | 163.0 | 141.8 |
| std | 0.6 | 0.5 | 0.5 |
| synth | 7.1 | 9.1 | 7.3 |

## Distribution of per-VC cost ratios over those proofs (mean over seeds)

| ratio bucket | PR/master | placebo/master |
|---|---:|---:|
| < 0.5x | 1 | 0 |
| 0.5-0.8x | 11 | 2 |
| 0.8-0.95x | 18 | 7 |
| 0.95-1.05x | 855 | 955 |
| 1.05-1.25x | 59 | 14 |
| 1.25-2x | 20 | 2 |
| 2-4x | 10 | 0 |
| >= 4x | 6 | 0 |

## Verdict changes at each job's limit (seeds passing out of 8)

| job | VC | limit | master ok | PR ok | placebo ok | master RU | PR RU |
|---|---|---:|---:|---:|---:|---:|---:|
| kondo/shardedKv/sync | ShardedKVProof.InvNextSafety (correctness) | 50M | 1 | 2 | 1 | 2.13M | 2.04M |
| lit/git-issues/git-issue-6535.dfy:legacy | Bad (correctness) | 50M | 8 | 0 | 8 | 0.03M | 0.03M |
| lit/git-issues/git-issue-6535.dfy:refresh | Bad (correctness) | 50M | 8 | 0 | 8 | 0.03M | 0.03M |
| synth/keyed-08.dfy | Keyed (correctness) | 50M | 8 | 7 | 8 | 10.37M | 19.91M |
| synth/keyed-16.dfy | Keyed (correctness) | 50M | 8 | 7 | 8 | 9.57M | 43.29M |

## Largest changes among those proofs (by |PR - master| mean RU)

| job | VC | master | PR | PR/master | placebo | min..max master | min..max PR |
|---|---|---:|---:|---:|---:|---|---|
| synth/keyed-16.dfy | Keyed (correctness) | 9.57M | 43.29M | 4.52 | 10.53M | 5.76..15.39M | 8.59..253.57M |
| lit/dafny4/UnionFind.dfy:legacy | M3.UnionFind.Join (correctness) (assertion batch 124) | 3.89M | 17.38M | 4.47 | 4.38M | 1.66..9.46M | 3.31..37.39M |
| lit/dafny4/UnionFind.dfy:legacy | M3.UnionFind.Join (correctness) (assertion batch 47) | 3.24M | 15.06M | 4.65 | 3.16M | 2.08..5.02M | 2.82..49.92M |
| synth/keyed-08.dfy | Keyed (correctness) | 10.37M | 19.91M | 1.92 | 10.60M | 7.44..14.53M | 7.75..73.52M |
| lit/dafny4/UnionFind.dfy:legacy | M2.UnionFind.FindAux (correctness) | 18.00M | 12.35M | 0.69 | 17.37M | 12.20..27.11M | 6.14..22.00M |
| synth/keyed-04.dfy | Keyed (correctness) | 9.02M | 14.06M | 1.56 | 9.02M | 3.76..18.51M | 5.40..26.12M |
| lit/dafny0/Maps.dfy:legacy | GeneralMaps4 (correctness) | 0.17M | 2.96M | 17.54 | 0.17M | 0.17..0.17M | 2.96..2.96M |
| lit/dafny0/Maps.dfy:refresh | GeneralMaps4 (correctness) | 0.17M | 2.96M | 17.54 | 0.17M | 0.17..0.17M | 2.96..2.96M |
| dafnybench/DafnyProjects_tmp_tmp2acw_s4s_RawSort.dfy | rawsort (correctness) | 10.04M | 12.08M | 1.20 | 12.57M | 2.03..14.84M | 1.41..22.81M |
| synth/chain-16.dfy | Chain (correctness) | 0.32M | 2.30M | 7.18 | 0.39M | 0.32..0.32M | 2.30..2.30M |
| lit/dafny4/UnionFind.dfy:refresh | M2.UnionFind.FindAux (correctness) | 16.90M | 14.97M | 0.89 | 17.50M | 10.17..21.99M | 9.28..21.97M |
| lit/VSI-Benchmarks/b4.dfy:refresh | Map.RemoveNonFirst (correctness) | 10.45M | 12.12M | 1.16 | 10.59M | 6.67..16.00M | 6.04..17.92M |
| lit/dafny4/UnionFind.dfy:legacy | M1.UnionFind.New (correctness) | 5.36M | 3.78M | 0.71 | 5.03M | 2.25..11.92M | 2.63..6.03M |
| lit/dafny4/UnionFind.dfy:refresh | M3.UnionFind.Join (correctness) (assertion batch 128) | 2.17M | 3.62M | 1.67 | 2.52M | 1.43..2.88M | 1.38..9.53M |
| dafnybench/dafny_experiments_tmp_tmpz29_3_3i_circuit.dfy | BackwardConnections.CombineBackconnsHelper (correctness) | 8.12M | 9.50M | 1.17 | 5.81M | 2.24..33.91M | 3.37..41.11M |
| synth/keyed-02.dfy | Keyed (correctness) | 6.19M | 4.92M | 0.79 | 5.45M | 4.80..11.25M | 4.80..5.24M |
| synth/ichain-16.dfy | Chain (correctness) | 0.59M | 1.64M | 2.76 | 0.56M | 0.59..0.59M | 1.38..2.09M |
| lit/dafny4/UnionFind.dfy:refresh | M3.UnionFind.Join (correctness) (assertion batch 166) | 0.70M | 1.65M | 2.34 | 0.70M | 0.51..1.02M | 0.43..2.43M |
| lit/dafny4/UnionFind.dfy:refresh | M3.UnionFind.Join (correctness) (assertion batch 111) | 0.87M | 1.76M | 2.01 | 0.87M | 0.51..1.02M | 0.42..2.48M |
| lit/VSI-Benchmarks/b4.dfy:legacy | Map.RemoveNonFirst (correctness) | 12.14M | 13.00M | 1.07 | 12.27M | 9.04..16.20M | 10.79..15.66M |
| lit/dafny4/UnionFind.dfy:legacy | M3.UnionFind.Join (correctness) (assertion batch 143) | 2.35M | 1.49M | 0.64 | 2.35M | 1.86..3.15M | 0.89..1.98M |
| lit/dafny4/UnionFind.dfy:refresh | M3.UnionFind.Join (correctness) (assertion batch 168) | 1.06M | 0.27M | 0.26 | 1.03M | 1.01..1.30M | 0.26..0.31M |
| lit/dafny4/UnionFind.dfy:legacy | M3.UnionFind.Join (correctness) (assertion batch 109) | 1.35M | 2.07M | 1.53 | 1.35M | 0.81..1.72M | 1.89..2.25M |
| lit/dafny4/UnionFind.dfy:refresh | M3.UnionFind.Join (correctness) (assertion batch 35) | 1.62M | 0.96M | 0.59 | 1.60M | 0.71..2.58M | 0.52..1.57M |
| synth/equal-16.dfy | Equal (correctness) | 1.17M | 1.70M | 1.46 | 1.19M | 1.03..1.22M | 1.66..1.72M |

## Per job (proofs among the affected VCs)

| job | VCs | master | PR | PR vs master | placebo vs master |
|---|---:|---:|---:|---:|---:|
| lit/dafny4/UnionFind.dfy:legacy | 287 | 72.43M | 90.68M | +25.2% | -0.5% |
| lit/dafny4/UnionFind.dfy:refresh | 294 | 68.60M | 69.94M | +2.0% | +0.8% |
| lit/VSI-Benchmarks/b4.dfy:legacy | 14 | 13.84M | 14.90M | +7.7% | +0.9% |
| lit/VSI-Benchmarks/b4.dfy:refresh | 14 | 12.17M | 14.07M | +15.7% | +1.2% |
| lit/git-issues/git-issue-3855.dfy:pinned | 59 | 11.87M | 11.79M | -0.6% | -0.1% |
| synth/keyed-08.dfy | 1 | 10.37M | 19.91M | +92.0% | +2.2% |
| dafnybench/DafnyProjects_tmp_tmp2acw_s4s_RawSort.dfy | 1 | 10.04M | 12.08M | +20.3% | +25.2% |
| synth/keyed-16.dfy | 1 | 9.57M | 43.29M | +352.1% | +10.0% |
| dafnybench/dafny_experiments_tmp_tmpz29_3_3i_circuit.dfy | 13 | 9.12M | 10.44M | +14.5% | -25.3% |
| synth/keyed-04.dfy | 1 | 9.02M | 14.06M | +55.9% | +0.0% |
| synth/keyed-02.dfy | 1 | 6.19M | 4.92M | -20.6% | -12.1% |
| lit/comp/rust/loops.dfy:legacy | 4 | 5.63M | 5.77M | +2.5% | -1.3% |
| lit/comp/rust/loops.dfy:refresh | 4 | 5.63M | 5.77M | +2.5% | -1.3% |
| kondo/shardedKvBatched/manual | 17 | 3.07M | 3.13M | +1.7% | -0.4% |
| lit/cloudmake/CloudMake-ParallelBuilds.dfy:legacy | 19 | 2.82M | 2.84M | +0.7% | +0.5% |
| lit/cloudmake/CloudMake-ParallelBuilds.dfy:refresh | 19 | 2.82M | 2.84M | +0.7% | +0.5% |
| kondo/shardedKv/manual | 16 | 2.82M | 2.86M | +1.6% | -0.4% |
| kondo/paxos/sync | 2 | 1.86M | 1.86M | +0.0% | -0.0% |
| kondo/shardedKvBatched/sync | 9 | 1.77M | 1.78M | +0.5% | -0.0% |
| synth/keyed-01.dfy | 1 | 1.53M | 1.50M | -1.7% | +0.0% |
| lit/dafny0/IMaps.dfy:refresh | 7 | 1.19M | 1.22M | +2.5% | -0.0% |
| lit/dafny0/IMaps.dfy:legacy | 7 | 1.19M | 1.22M | +2.5% | +0.0% |
| synth/equal-16.dfy | 1 | 1.17M | 1.70M | +45.6% | +2.1% |
| lit/comp/rust/operators.dfy:legacy | 5 | 0.98M | 0.97M | -0.8% | +1.0% |
| lit/comp/rust/operators.dfy:refresh | 4 | 0.80M | 0.79M | -1.0% | +1.3% |
| kondo/shardedKv/sync | 9 | 0.66M | 0.66M | +0.2% | -0.0% |
| lit/dafny0/Maps.dfy:refresh | 13 | 0.61M | 3.40M | +460.3% | +0.8% |
| lit/dafny0/Maps.dfy:legacy | 13 | 0.61M | 3.40M | +460.7% | +0.8% |
| synth/ichain-16.dfy | 1 | 0.59M | 1.64M | +175.8% | -5.6% |
| synth/chain-16.dfy | 1 | 0.32M | 2.30M | +617.9% | +23.3% |
| synth/equal-08.dfy | 1 | 0.27M | 0.29M | +8.7% | -0.0% |
| lit/comp/Comprehensions.dfy:legacy | 4 | 0.24M | 0.24M | -0.8% | -1.2% |
| lit/comp/Comprehensions.dfy:refresh | 4 | 0.23M | 0.23M | +0.6% | -0.7% |
| lit/comp/ComprehensionsNewSyntax.dfy:legacy | 3 | 0.21M | 0.21M | -1.1% | -1.4% |
| lit/comp/ComprehensionsNewSyntax.dfy:refresh | 3 | 0.20M | 0.19M | -2.3% | -0.8% |
| std/Collections/Map.dfy | 5 | 0.16M | 0.16M | +0.9% | +0.0% |
| lit/dafny4/git-issue167.dfy:refresh | 2 | 0.14M | 0.10M | -27.0% | +0.0% |
| synth/spec-16.dfy | 3 | 0.14M | 0.15M | +4.1% | -0.0% |
| lit/dafny4/git-issue167.dfy:legacy | 2 | 0.14M | 0.10M | -27.4% | +0.0% |
| lit/dafny4/KozenSilva.dfy:legacy | 3 | 0.13M | 0.13M | -0.3% | -0.0% |
| lit/dafny4/KozenSilva.dfy:refresh | 3 | 0.13M | 0.13M | -0.3% | -0.0% |
| std/Collections/Imap.dfy | 5 | 0.13M | 0.13M | +1.4% | +0.0% |
| synth/ichain-08.dfy | 1 | 0.10M | 0.26M | +159.7% | -2.5% |
| synth/spec-08.dfy | 3 | 0.10M | 0.10M | +2.1% | -0.0% |
| synth/equal-04.dfy | 1 | 0.08M | 0.07M | -5.1% | +0.0% |
| synth/spec-04.dfy | 3 | 0.08M | 0.08M | +1.0% | -0.0% |
| dafnybench/iron-sync_tmp_tmps49o3tyz_lib_Base_MapRemove.dfy | 1 | 0.08M | 0.08M | +1.2% | -3.5% |
| dafnybench/fv2020-tms_tmp_tmpnp85b47l_modeling_concurrency_safety.dfy | 1 | 0.08M | 0.09M | +14.0% | +0.1% |
| dafnybench/dafny-programs_tmp_tmpcwodh6qh_src_ticketsystem.dfy | 1 | 0.07M | 0.08M | +12.5% | +0.1% |
| lit/dafny0/GeneralNewtypeCollections.dfy:pinned | 2 | 0.07M | 0.07M | +0.0% | -0.2% |
| lit/git-issues/git-issue-697b.dfy:legacy | 1 | 0.07M | 0.07M | -3.2% | +0.0% |
| lit/dafny0/GeneralNewtypeCollectionsGeneric.dfy:pinned | 2 | 0.07M | 0.07M | +1.9% | +0.0% |
| lit/git-issues/git-issue-697b.dfy:refresh | 1 | 0.07M | 0.07M | +3.6% | +1.4% |
| synth/chain-08.dfy | 1 | 0.07M | 0.22M | +215.9% | +31.3% |
| synth/spec-02.dfy | 3 | 0.07M | 0.07M | +0.5% | -0.0% |
| lit/dafny0/ISets.dfy:legacy | 1 | 0.07M | 0.07M | -2.2% | -1.4% |
| lit/dafny0/ISets.dfy:refresh | 1 | 0.07M | 0.07M | -2.2% | -1.4% |
| synth/spec-01.dfy | 3 | 0.06M | 0.06M | +0.4% | -0.0% |
| synth/ilookups-16.dfy | 1 | 0.06M | 0.08M | +28.4% | +0.0% |
| lit/git-issues/git-issue-1163.dfy:legacy | 1 | 0.06M | 0.06M | +0.2% | +0.0% |
| lit/git-issues/git-issue-1163.dfy:refresh | 1 | 0.06M | 0.06M | +0.2% | +0.0% |
| synth/lookups-16.dfy | 1 | 0.06M | 0.07M | +13.3% | +0.0% |
| lit/comp/Calls.dfy:legacy | 1 | 0.06M | 0.06M | +0.4% | +0.4% |
| lit/comp/firstSteps/6_Calls-VariableCapture.dfy:legacy | 1 | 0.06M | 0.06M | +0.4% | +0.4% |
| lit/comp/Calls.dfy:refresh | 1 | 0.06M | 0.06M | +1.1% | +0.0% |
| lit/comp/firstSteps/6_Calls-VariableCapture.dfy:refresh | 1 | 0.06M | 0.06M | +1.1% | +0.0% |
| dafnybench/verification-class_tmp_tmpz9ik148s_2022_chapter05-distributed-state-machines_exercises_UtilitiesLibrary.dfy | 1 | 0.05M | 0.05M | +3.3% | +0.1% |
| synth/update-16.dfy | 1 | 0.05M | 0.05M | +5.4% | +0.0% |
| lit/dafny4/Regression19.dfy:legacy | 1 | 0.05M | 0.05M | +0.4% | +0.0% |
| lit/dafny4/Regression19.dfy:refresh | 1 | 0.05M | 0.05M | +0.4% | +0.0% |
| lit/git-issues/git-issue-1158.dfy:legacy | 1 | 0.04M | 0.04M | -2.3% | +0.0% |
| lit/git-issues/git-issue-1158.dfy:refresh | 1 | 0.04M | 0.04M | -2.3% | +0.0% |
| std/Parsers/Core/ParsersBuilders.dfy | 1 | 0.04M | 0.04M | +0.2% | +0.0% |
| lit/dafny4/Bug58.dfy:legacy | 3 | 0.04M | 0.04M | +0.9% | +0.0% |
| lit/dafny4/Bug58.dfy:refresh | 3 | 0.04M | 0.04M | +0.9% | +0.0% |
| kondo/clientServer/manual | 1 | 0.04M | 0.04M | +1.1% | -0.2% |
| kondo/clientServer/sync | 1 | 0.04M | 0.04M | +1.1% | -0.2% |
| kondo/distributedLock/manual | 1 | 0.04M | 0.04M | +1.1% | -0.2% |
| kondo/distributedLock/sync | 1 | 0.04M | 0.04M | +1.1% | -0.2% |
| kondo/flexPaxos/sync | 1 | 0.04M | 0.04M | +1.1% | -0.2% |
| kondo/lockServer/manual | 1 | 0.04M | 0.04M | +1.1% | -0.2% |
| kondo/lockServer/sync | 1 | 0.04M | 0.04M | +1.1% | -0.2% |
| kondo/ringLeaderElection/manual | 1 | 0.04M | 0.04M | +1.1% | -0.2% |
| kondo/ringLeaderElection/sync | 1 | 0.04M | 0.04M | +1.1% | -0.2% |
| kondo/simplifiedLeaderElection/manual | 1 | 0.04M | 0.04M | +1.1% | -0.2% |
| kondo/simplifiedLeaderElection/sync | 1 | 0.04M | 0.04M | +1.1% | -0.2% |
| kondo/twoPhaseCommit/manual | 1 | 0.04M | 0.04M | +1.1% | -0.2% |
| kondo/twoPhaseCommit/paper-version | 1 | 0.04M | 0.04M | +1.1% | -0.2% |
| kondo/twoPhaseCommit/sync | 1 | 0.04M | 0.04M | +1.1% | -0.2% |
| synth/ichain-04.dfy | 1 | 0.03M | 0.07M | +95.8% | +2.0% |
| lit/dafny0/DiscoverBounds.dfy:legacy | 1 | 0.03M | 0.03M | -1.8% | -1.0% |
| lit/dafny0/DiscoverBounds.dfy:refresh | 1 | 0.03M | 0.03M | -1.8% | -1.0% |
| synth/lookups-08.dfy | 1 | 0.03M | 0.04M | +19.1% | +0.0% |
| synth/ilookups-08.dfy | 1 | 0.03M | 0.03M | -0.0% | +0.0% |
| synth/equal-02.dfy | 1 | 0.03M | 0.03M | -4.6% | +0.0% |
| synth/update-08.dfy | 1 | 0.03M | 0.03M | +4.6% | +0.0% |
| synth/chain-04.dfy | 1 | 0.03M | 0.07M | +129.6% | +3.3% |
| lit/dafny4/git-issue75.dfy:legacy | 2 | 0.03M | 0.03M | +0.6% | +0.0% |
| lit/dafny4/git-issue75.dfy:refresh | 2 | 0.03M | 0.03M | +0.6% | +0.0% |
| lit/comp/CovariantCollections.dfy:pinned | 1 | 0.03M | 0.03M | +0.3% | +0.0% |
| synth/update-04.dfy | 1 | 0.02M | 0.02M | +3.2% | +0.0% |
| synth/ilookups-04.dfy | 1 | 0.02M | 0.03M | +30.4% | +0.0% |
| synth/lookups-04.dfy | 1 | 0.02M | 0.03M | +23.6% | +0.0% |
| lit/dafny0/GeneralNewtypeMemberCompile.dfy:pinned | 1 | 0.02M | 0.02M | +0.4% | +0.0% |
| synth/update-02.dfy | 1 | 0.02M | 0.02M | +2.0% | +0.0% |
| dafnybench/Clover_update_map.dfy | 1 | 0.02M | 0.02M | +1.3% | +0.0% |
| synth/ichain-02.dfy | 1 | 0.02M | 0.03M | +64.0% | +3.4% |
| synth/update-01.dfy | 1 | 0.02M | 0.02M | +1.3% | +0.0% |
| lit/git-issues/git-issue-3320.dfy:legacy | 1 | 0.02M | 0.02M | +0.4% | +0.0% |
| lit/git-issues/git-issue-3320.dfy:refresh | 1 | 0.02M | 0.02M | +0.4% | +0.0% |
| synth/ilookups-02.dfy | 1 | 0.02M | 0.02M | +17.1% | +0.0% |
| lit/dafny0/TypeAdjustments.dfy:pinned | 1 | 0.02M | 0.02M | +0.5% | +0.0% |
| synth/chain-02.dfy | 1 | 0.02M | 0.03M | +77.9% | +2.5% |
| synth/lookups-02.dfy | 1 | 0.02M | 0.02M | +26.0% | +0.0% |
| lit/git-issues/git-issue-1165.dfy:legacy | 1 | 0.02M | 0.02M | +0.5% | -0.0% |
| lit/git-issues/git-issue-1165.dfy:refresh | 1 | 0.02M | 0.02M | +0.5% | -0.0% |
| synth/equal-01.dfy | 1 | 0.02M | 0.02M | -0.5% | +0.0% |
| synth/ilookups-01.dfy | 1 | 0.02M | 0.02M | +0.8% | +0.0% |
| lit/dafny4/Bug54.dfy:legacy | 1 | 0.02M | 0.02M | +1.9% | -0.0% |
| lit/dafny4/Bug54.dfy:refresh | 1 | 0.02M | 0.02M | +1.9% | -0.0% |
| synth/ichain-01.dfy | 1 | 0.02M | 0.02M | +1.7% | +0.1% |
| lit/git-issues/git-issue-336.dfy:legacy | 1 | 0.02M | 0.02M | +0.5% | -0.0% |
| lit/git-issues/git-issue-336.dfy:refresh | 1 | 0.02M | 0.02M | +0.5% | -0.0% |
| synth/lookups-01.dfy | 1 | 0.02M | 0.02M | +21.9% | +0.0% |
| synth/chain-01.dfy | 1 | 0.02M | 0.02M | +13.3% | +0.0% |
| lit/dafny0/Compilation.legacy.dfy:pinned | 1 | 0.01M | 0.01M | +0.6% | +0.0% |
| lit/dafny4/git-issue27.dfy:legacy | 1 | 0.01M | 0.01M | +0.6% | -0.0% |
| lit/dafny4/git-issue27.dfy:refresh | 1 | 0.01M | 0.01M | +0.6% | -0.0% |
| lit/dafny4/Bug108.dfy:legacy | 1 | 0.01M | 0.01M | +0.7% | +0.0% |
| lit/dafny4/Bug108.dfy:refresh | 1 | 0.01M | 0.01M | +0.7% | +0.0% |

## Synthetic programs: total RU by size N (master / PR / placebo, mean over seeds)

| family | N=1 | N=2 | N=4 | N=8 | N=16 |
|---|---|---|---|---|---|
| chain | 0.02 / 0.02 / 0.02 | 0.02 / 0.03 / 0.02 | 0.03 / 0.07 / 0.03 | 0.07 / 0.22 / 0.09 | 0.32 / 2.30 / 0.39 |
| equal | 0.02 / 0.02 / 0.02 | 0.03 / 0.03 / 0.03 | 0.08 / 0.07 / 0.08 | 0.27 / 0.29 / 0.27 | 1.17 / 1.70 / 1.19 |
| ichain | 0.02 / 0.02 / 0.02 | 0.02 / 0.03 / 0.02 | 0.03 / 0.07 / 0.03 | 0.10 / 0.26 / 0.10 | 0.59 / 1.64 / 0.56 |
| ilookups | 0.02 / 0.02 / 0.02 | 0.02 / 0.02 / 0.02 | 0.02 / 0.03 / 0.02 | 0.03 / 0.03 / 0.03 | 0.06 / 0.08 / 0.06 |
| keyed | 1.53 / 1.50 / 1.53 | 6.19 / 4.92 / 5.45 | 9.02 / 14.06 / 9.02 | 10.37 / 19.91 / 10.60 | 9.57 / 43.29 / 10.53 |
| lookups | 0.02 / 0.02 / 0.02 | 0.02 / 0.02 / 0.02 | 0.02 / 0.03 / 0.02 | 0.03 / 0.04 / 0.03 | 0.06 / 0.07 / 0.06 |
| spec | 0.08 / 0.08 / 0.08 | 0.08 / 0.08 / 0.08 | 0.09 / 0.09 / 0.09 | 0.11 / 0.11 / 0.11 | 0.16 / 0.16 / 0.16 |
| update | 0.02 / 0.02 / 0.02 | 0.02 / 0.02 / 0.02 | 0.02 / 0.02 / 0.02 | 0.03 / 0.03 / 0.03 | 0.05 / 0.05 / 0.05 |

## dafny4/UnionFind.dfy as on master (Main not isolated): Main's cost per seed

| resolver | prelude | seed 0 | seed 1 | seed 2 | seed 3 | seed 4 | seed 5 | seed 6 | seed 7 | over 50M |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| legacy | master | 50.3M | 24.5M | 34.9M | 16.6M | 47.6M | 19.8M | 149.7M | 21.8M | 2 |
| legacy | pr | 23.0M | 16.6M | 61.6M | 11.9M | 62.5M | 80.7M | 85.1M | 95.3M | 5 |
| legacy | placebo | 38.2M | 18.9M | 34.9M | 15.4M | 27.2M | 16.1M | 39.1M | 23.5M | 0 |
| legacy | domguard | 23.1M | 20.4M | 48.5M | 20.8M | 42.3M | 40.0M | 35.1M | 22.7M | 0 |
| legacy | master2 | 50.3M | 24.5M | 34.9M | 16.6M | 47.6M | 19.8M | 149.7M | 21.8M | 2 |
| legacy | pointwise | 26.2M | 82.9M | 67.9M | 80.2M | 45.0M | 25.2M | 85.8M | 22.1M | 4 |
| refresh | master | 68.3M | 12.6M | 26.9M | 18.6M | 38.6M | 13.3M | 18.3M | 23.4M | 1 |
| refresh | pr | 15.2M | 8.9M | 27.5M | 50.8M | 26.6M | 51.5M | 120.0M | 11.2M | 3 |
| refresh | placebo | 86.7M | 10.6M | 46.4M | 19.5M | 46.9M | 10.0M | 29.9M | 36.6M | 1 |
| refresh | domguard | 18.8M | 14.1M | 21.8M | 32.6M | 35.2M | 14.7M | 25.6M | 44.1M | 0 |
| refresh | master2 | 68.3M | 12.6M | 26.9M | 18.6M | 38.6M | 13.3M | 18.3M | 23.4M | 1 |
| refresh | pointwise | 80.6M | 10.9M | 42.6M | 51.0M | 36.8M | 95.5M | 27.4M | 20.7M | 3 |

## Stability over the affected VCs (all but synth)

Flaky: some seeds pass at the job's limit and others do not. Spread: the coefficient of variation of a VC's cost across seeds, for VCs above 1M RU under master.

| prelude | flaky VCs | flaky, not under master | no longer flaky | median spread | 90th-percentile spread |
|---|---:|---:|---:|---:|---:|
| master | 4 | 0 | 0 | 0.24 | 0.57 |
| master2 | 4 | 0 | 0 | 0.24 | 0.57 |
| placebo | 4 | 0 | 0 | 0.26 | 0.60 |
| pointwise | 5 | 1 | 0 | 0.25 | 0.75 |
| pr | 4 | 0 | 0 | 0.25 | 0.78 |
| domguard | 5 | 1 | 0 | 0.26 | 0.78 |

## Comparisons over the affected proofs (all but synth)

| comparison | programs | VCs | total | geomean over VCs | per program | verdict flips at limit |
|---|---:|---:|---|---|---|---:|
| A/A: master2 vs master (same input, another process) | 63 | 930 | -0.0% [-0.0%, +0.0%] | -0.0% [-0.0%, +0.0%] | -0.0% [-0.0%, +0.0%] | 0 |
| placebo vs master (the old axiom, rewritten) | 63 | 930 | +0.2% [-6.0%, +6.2%] | +0.0% [-0.3%, +0.1%] | +0.2% [-0.3%, +1.0%] | 0 |
| shape: pointwise vs master (the PR's quantifier without its guard) | 63 | 930 | +14.7% [+0.7%, +20.1%] | +0.5% [-0.4%, +0.7%] | -0.1% [-0.7%, +0.3%] | 1 |
| guard: pr vs pointwise | 63 | 930 | -1.0% [-5.6%, +22.3%] | +1.4% [+0.4%, +5.7%] | +1.7% [+0.8%, +2.8%] | 1 |
| pr vs master | 63 | 930 | +13.6% [+5.0%, +26.4%] | +1.9% [+0.6%, +6.0%] | +1.6% [+0.4%, +2.9%] | 0 |
| domguard vs master | 63 | 930 | +5.3% [-9.1%, +9.6%] | +1.0% [+0.0%, +1.6%] | +0.6% [-0.1%, +1.5%] | 1 |
| domguard vs pr | 63 | 930 | -7.3% [-25.3%, -2.8%] | -0.8% [-4.8%, -0.1%] | -0.9% [-1.9%, -0.1%] | 1 |

## ... whose SMT contains the changed axiom (classify.py)

| comparison | programs | VCs | total | geomean over VCs | per program | verdict flips at limit |
|---|---:|---:|---|---|---|---:|
| A/A: master2 vs master (same input, another process) | 62 | 919 | +0.0% [+0.0%, +0.0%] | +0.0% [+0.0%, +0.0%] | +0.0% [+0.0%, +0.0%] | 0 |
| placebo vs master (the old axiom, rewritten) | 62 | 919 | +0.2% [-5.5%, +6.1%] | +0.0% [-0.3%, +0.1%] | +0.2% [-0.3%, +1.0%] | 0 |
| shape: pointwise vs master (the PR's quantifier without its guard) | 62 | 919 | +14.8% [+0.8%, +20.2%] | +0.5% [-0.4%, +0.7%] | -0.1% [-0.7%, +0.4%] | 1 |
| guard: pr vs pointwise | 62 | 919 | -1.0% [-5.7%, +23.4%] | +1.4% [+0.4%, +6.1%] | +1.7% [+0.8%, +2.9%] | 1 |
| pr vs master | 62 | 919 | +13.7% [+5.2%, +28.7%] | +1.9% [+0.5%, +6.6%] | +1.6% [+0.3%, +3.0%] | 0 |
| domguard vs master | 62 | 919 | +5.4% [-9.7%, +9.5%] | +1.1% [+0.0%, +1.7%] | +0.6% [-0.2%, +1.5%] | 1 |
| domguard vs pr | 62 | 919 | -7.3% [-25.0%, -2.6%] | -0.9% [-4.9%, -0.1%] | -0.9% [-2.1%, -0.1%] | 1 |

## ... whose SMT does not: a pure perturbation

| comparison | programs | VCs | total | geomean over VCs | per program | verdict flips at limit |
|---|---:|---:|---|---|---|---:|
| A/A: master2 vs master (same input, another process) | 3 | 10 | -0.0% [-0.1%, +0.0%] | -0.0% [-0.1%, +0.0%] | -0.0% [-0.1%, +0.0%] | 0 |
| placebo vs master (the old axiom, rewritten) | 3 | 10 | -0.0% [-0.0%, +0.0%] | +0.0% [-0.0%, +0.0%] | +0.0% [-0.0%, +0.0%] | 0 |
| shape: pointwise vs master (the PR's quantifier without its guard) | 3 | 10 | -0.0% [-0.0%, +0.0%] | +0.0% [-0.0%, +0.0%] | +0.0% [-0.0%, +0.0%] | 0 |
| guard: pr vs pointwise | 3 | 10 | -0.0% [-0.1%, +0.0%] | -0.0% [-0.1%, +0.0%] | -0.0% [-0.1%, +0.0%] | 0 |
| pr vs master | 3 | 10 | -0.0% [-0.0%, +0.0%] | -0.0% [-0.0%, +0.0%] | -0.0% [-0.0%, +0.0%] | 0 |
| domguard vs master | 3 | 10 | +0.0% [-0.0%, +0.1%] | +0.0% [-0.0%, +0.1%] | +0.0% [-0.0%, +0.1%] | 0 |
| domguard vs pr | 3 | 10 | +0.0% [-0.0%, +0.1%] | +0.0% [-0.0%, +0.1%] | +0.0% [-0.0%, +0.1%] | 0 |

1 of the 930 affected proofs have no classification (unmapped or mixed log names).

## Comparisons over the external programs' affected proofs

| comparison | programs | VCs | total | geomean over VCs | per program | verdict flips at limit |
|---|---:|---:|---|---|---|---:|
| A/A: master2 vs master (same input, another process) | 26 | 86 | +0.0% [+0.0%, +0.0%] | +0.0% [+0.0%, +0.0%] | +0.0% [+0.0%, +0.0%] | 0 |
| placebo vs master (the old axiom, rewritten) | 26 | 86 | +0.7% [-19.4%, +19.5%] | -0.2% [-1.1%, +0.9%] | +0.5% [-0.6%, +2.5%] | 0 |
| shape: pointwise vs master (the PR's quantifier without its guard) | 26 | 86 | +6.2% [+0.6%, +13.4%] | +0.3% [+0.1%, +0.5%] | +0.4% [+0.0%, +0.8%] | 0 |
| guard: pr vs pointwise | 26 | 86 | +5.1% [-1.9%, +14.3%] | +1.0% [+0.6%, +2.0%] | +2.3% [+1.0%, +3.9%] | 0 |
| pr vs master | 26 | 86 | +11.6% [+1.1%, +16.6%] | +1.2% [+0.8%, +2.4%] | +2.7% [+1.1%, +4.6%] | 0 |
| domguard vs master | 26 | 86 | -10.4% [-25.7%, +1.1%] | -0.0% [-1.4%, +1.3%] | +1.2% [-0.0%, +2.8%] | 0 |
| domguard vs pr | 26 | 86 | -19.7% [-33.1%, -0.2%] | -1.3% [-2.6%, -0.3%] | -1.4% [-3.1%, -0.4%] | 0 |

## Alternative sound encodings, over the same proofs

restrict: elements defined everywhere, `$ArbitraryBoxValue` outside the domain. domguard: the PR's axiom guarded by `Map#Domain(Map#Glue(a, b, t))`. eager: the PR's axiom plus the trigger `{ Map#Glue(a, b, t), Set#IsMember(a, bx) }`.

| encoding | programs | VCs | total vs master | geomean over VCs vs master | per program vs master | per program vs PR | verdict flips vs master at limit |
|---|---:|---:|---|---|---|---|---:|
| pr | 63 | 930 | +13.6% [+4.9%, +25.5%] | +1.9% [+0.6%, +5.9%] | +1.6% [+0.4%, +2.9%] |  | 5 |
| domguard | 63 | 930 | +5.3% [-9.4%, +9.5%] | +1.0% [+0.1%, +1.6%] | +0.6% [-0.2%, +1.4%] | -0.9% [-2.0%, -0.1%] | 4 |
| master2 | 63 | 930 | -0.0% [-0.0%, +0.0%] | -0.0% [-0.0%, +0.0%] | -0.0% [-0.0%, +0.0%] | -1.5% [-2.8%, -0.3%] | 0 |
| pointwise | 63 | 930 | +14.7% [+0.7%, +20.0%] | +0.5% [-0.4%, +0.7%] | -0.1% [-0.7%, +0.3%] | -1.6% [-2.7%, -0.8%] | 4 |

domguard: largest differences from the PR

| job | VC | master | PR | domguard |
|---|---|---:|---:|---:|
| lit/dafny4/UnionFind.dfy:legacy | M3.UnionFind.Join (correctness) (assertion batch 124) | 3.89M | 17.38M | 8.08M |
| lit/dafny4/UnionFind.dfy:refresh | M2.UnionFind.FindAux (correctness) | 16.90M | 14.97M | 20.61M |
| dafnybench/dafny_experiments_tmp_tmpz29_3_3i_circuit.dfy | BackwardConnections.CombineBackconnsHelper (correctness) | 8.12M | 9.50M | 5.03M |
| lit/dafny0/Maps.dfy:legacy | GeneralMaps4 (correctness) | 0.17M | 2.96M | 0.18M |
| lit/dafny0/Maps.dfy:refresh | GeneralMaps4 (correctness) | 0.17M | 2.96M | 0.18M |
| lit/VSI-Benchmarks/b4.dfy:legacy | Map.RemoveNonFirst (correctness) | 12.14M | 13.00M | 10.43M |

master2: largest differences from the PR

| job | VC | master | PR | master2 |
|---|---|---:|---:|---:|
| lit/dafny4/UnionFind.dfy:legacy | M3.UnionFind.Join (correctness) (assertion batch 124) | 3.89M | 17.38M | 3.89M |
| lit/dafny4/UnionFind.dfy:legacy | M3.UnionFind.Join (correctness) (assertion batch 47) | 3.24M | 15.06M | 3.24M |
| lit/dafny4/UnionFind.dfy:legacy | M2.UnionFind.FindAux (correctness) | 18.00M | 12.35M | 18.00M |
| lit/dafny0/Maps.dfy:legacy | GeneralMaps4 (correctness) | 0.17M | 2.96M | 0.17M |
| lit/dafny0/Maps.dfy:refresh | GeneralMaps4 (correctness) | 0.17M | 2.96M | 0.17M |
| dafnybench/DafnyProjects_tmp_tmp2acw_s4s_RawSort.dfy | rawsort (correctness) | 10.04M | 12.08M | 10.04M |

pointwise: largest differences from the PR

| job | VC | master | PR | pointwise |
|---|---|---:|---:|---:|
| lit/dafny4/UnionFind.dfy:refresh | M2.UnionFind.FindAux (correctness) | 16.90M | 14.97M | 27.19M |
| lit/dafny4/UnionFind.dfy:legacy | M3.UnionFind.Join (correctness) (assertion batch 124) | 3.89M | 17.38M | 7.20M |
| lit/dafny4/UnionFind.dfy:legacy | M2.UnionFind.FindAux (correctness) | 18.00M | 12.35M | 20.24M |
| lit/dafny0/Maps.dfy:legacy | GeneralMaps4 (correctness) | 0.17M | 2.96M | 0.17M |
| lit/dafny0/Maps.dfy:refresh | GeneralMaps4 (correctness) | 0.17M | 2.96M | 0.17M |
| lit/dafny4/UnionFind.dfy:legacy | M3.UnionFind.Join (correctness) (assertion batch 47) | 3.24M | 15.06M | 13.10M |

Synthetic programs at N=16 (total RU, mean over seeds):

| family | master | pr | domguard | master2 | pointwise |
|---|---:|---:|---:|---:|---:|
| chain | 0.32M | 2.30M | 0.33M | 0.32M | 0.29M |
| equal | 1.17M | 1.70M | 1.65M | 1.17M | 1.14M |
| ichain | 0.59M | 1.64M | 0.60M | 0.59M | 0.60M |
| ilookups | 0.06M | 0.08M | 0.07M | 0.06M | 0.07M |
| keyed | 9.57M | 43.29M | 42.39M | 9.57M | 43.05M |
| lookups | 0.06M | 0.07M | 0.07M | 0.06M | 0.07M |
| spec | 0.16M | 0.16M | 0.17M | 0.16M | 0.16M |
| update | 0.05M | 0.05M | 0.05M | 0.05M | 0.05M |
