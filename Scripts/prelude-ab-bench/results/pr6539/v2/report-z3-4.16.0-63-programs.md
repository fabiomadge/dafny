# Map#Glue prelude A/B benchmark

Seeds per (VC, prelude): 8 (0, 1, 2, 3, 4, 5, 6, 7; 0 is Dafny's default). VCs: 3330 in 159 jobs; **1029 affected** (master and PR counts differ), 2301 unaffected (identical counts under master and PR for every seed).
Unaffected VCs whose counts differ under the placebo: 0.

## Proof cost over affected VCs that pass everywhere

Totals are sums of per-VC means over seeds. "Per program" averages each program's own VC geomean, so a
program with hundreds of VCs weighs no more than one with two. Brackets are 95% bootstrap intervals that
resample programs, not VCs.

| group | programs | VCs | largest program | total PR/master | geomean over VCs | per program | placebo per program |
|---|---:|---:|---|---|---|---|---|
| all but synth | 63 | 934 | lit/dafny4/UnionFind.dfy (62% of VCs) | +11.3% [-3.4%, +21.0%] | +1.6% [+0.4%, +5.5%] | +0.6% [-0.6%, +2.0%] | +0.1% [-0.0%, +0.2%] |
| dafnybench | 7 | 18 | dafnybench/dafny_experiments_tmp_tmpz29_3_3i_circuit.dfy (67% of VCs) | -14.6% [-15.7%, +8.4%] | +0.6% [-3.9%, +7.5%] | +1.5% [-5.4%, +8.0%] | +0.3% [+0.0%, +0.9%] |
| kondo | 19 | 66 | kondo/shardedKvBatched/manual (26% of VCs) | -0.1% [-0.4%, +0.4%] | +0.2% [+0.2%, +0.2%] | +0.2% [+0.2%, +0.2%] | +0.1% [+0.1%, +0.1%] |
| lit | 34 | 839 | lit/dafny4/UnionFind.dfy (69% of VCs) | +13.8% [+0.6%, +36.7%] | +1.7% [+0.3%, +7.6%] | +0.7% [-1.2%, +2.6%] | +0.0% [-0.1%, +0.2%] |
| std | 3 | 11 | std/Collections/Imap.dfy (45% of VCs) | +0.6% [+0.1%, +1.4%] | +0.8% [+0.1%, +1.6%] | +0.6% [+0.1%, +1.6%] | +0.0% [-0.0%, +0.0%] |
| synth | 40 | 50 | synth/spec-01.dfy (6% of VCs) | +66.8% [-11.0%, +240.6%] | +25.1% [+11.5%, +44.7%] | +32.0% [+15.5%, +53.6%] | +1.0% [-1.0%, +3.2%] |

45 affected VCs fail (a verification error) in some run; their cost is the solver's search for a counterexample, reported separately:

| job | VC | master mean (min..max) | PR mean (min..max) | placebo mean |
|---|---|---|---|---|
| dafnybench/dafny_experiments_tmp_tmpz29_3_3i_circuit.dfy | CombineCircuits.CombineCircuitsCorrect (correctness) | 249.61M (193.03..333.97) | 324.02M (249.81..500.08) | 238.42M |
| lit/git-issues/git-issue-3855.dfy:pinned | Memory.dynMove (correctness) | 163.73M (55.83..295.24) | 161.39M (72.95..255.77) | 162.86M |
| kondo/flexPaxos/sync | PaxosProof.InvNextLearnerReceivedAcceptImpliesAccepted (correctness) | 141.28M (19.87..336.04) | 140.97M (19.87..335.36) | 142.12M |
| kondo/paxos/sync | PaxosProof.InvNextLeaderReceivedPromisesImpliesAcceptorState (correctness) | 115.78M (17.33..253.31) | 115.95M (17.33..254.65) | 117.65M |
| kondo/paxos/sync | PaxosProof.InvNextChosenImpliesProposingLeaderHearsChosenBallotP2bStep (correctness) | 105.15M (4.05..328.69) | 105.24M (4.05..329.43) | 106.11M |
| kondo/paxos/sync | PaxosProof.InvNextLearnerReceivedAcceptImpliesAccepted (correctness) | 62.40M (22.47..289.47) | 62.45M (22.47..289.89) | 63.28M |
| dafnybench/dafny_experiments_tmp_tmpz29_3_3i_circuit.dfy | BackwardConnections.CombineBackconnsHelper (correctness) | 11.68M (5.07..22.36) | 44.20M (4.03..295.60) | 24.72M |
| lit/git-issues/git-issue-3855.dfy:pinned | Memory.dynCopy (correctness) | 3.89M (2.35..4.98) | 4.28M (2.51..5.66) | 3.91M |
| kondo/shardedKv/sync | ShardedKVProof.InvNextSafety (correctness) | 3.88M (1.10..5.30) | 3.49M (1.23..5.21) | 3.71M |
| lit/git-issues/git-issue-3855.dfy:pinned | Main1 (correctness) | 3.19M (2.19..3.69) | 3.27M (2.70..3.90) | 3.22M |

## Total proof RU per seed (affected VCs that pass everywhere)

| prelude | seed 0 | seed 1 | seed 2 | seed 3 | seed 4 | seed 5 | seed 6 | seed 7 | mean | sd |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| master | 287.6M | 246.3M | 271.2M | 300.3M | 309.4M | 305.5M | 301.4M | 293.2M | 289.4M | 19.8M |
| pr | 308.4M | 326.4M | 376.1M | 325.2M | 544.0M | 345.3M | 279.1M | 313.8M | 352.3M | 77.1M |
| placebo | 279.8M | 257.4M | 282.8M | 293.4M | 305.1M | 308.4M | 298.9M | 318.7M | 293.1M | 18.1M |

## Solver time over those proofs (sum of per-VC means, seconds)

| group | master | PR | placebo |
|---|---:|---:|---:|
| all | 178.9 | 202.0 | 178.5 |
| lit | 151.5 | 172.7 | 150.8 |
| std | 0.4 | 0.4 | 0.5 |
| synth | 15.4 | 18.1 | 15.4 |

## Distribution of per-VC cost ratios over those proofs (mean over seeds)

| ratio bucket | PR/master | placebo/master |
|---|---:|---:|
| < 0.5x | 1 | 0 |
| 0.5-0.8x | 12 | 1 |
| 0.8-0.95x | 30 | 13 |
| 0.95-1.05x | 854 | 959 |
| 1.05-1.25x | 50 | 7 |
| 1.25-2x | 23 | 4 |
| 2-4x | 10 | 0 |
| >= 4x | 4 | 0 |

## Verdict changes at each job's limit (seeds passing out of 8)

| job | VC | limit | master ok | PR ok | placebo ok | master RU | PR RU |
|---|---|---:|---:|---:|---:|---:|---:|
| dafnybench/dafny_experiments_tmp_tmpz29_3_3i_circuit.dfy | BackwardConnections.CombineBackconnsHelper (correctness) | 50M | 8 | 7 | 7 | 11.68M | 44.20M |
| kondo/shardedKv/sync | ShardedKVProof.InvNextSafety (correctness) | 50M | 0 | 1 | 1 | 3.88M | 3.49M |
| lit/dafny4/UnionFind.dfy:legacy | M3.UnionFind.Join (correctness) (assertion batch 47) | 50M | 7 | 8 | 7 | 9.36M | 17.48M |
| lit/git-issues/git-issue-6535.dfy:legacy | Bad (correctness) | 50M | 8 | 0 | 8 | 0.03M | 0.03M |
| lit/git-issues/git-issue-6535.dfy:refresh | Bad (correctness) | 50M | 8 | 0 | 8 | 0.03M | 0.03M |
| synth/keyed-16.dfy | Keyed (correctness) | 50M | 8 | 6 | 8 | 11.17M | 45.45M |

## Largest changes among those proofs (by |PR - master| mean RU)

| job | VC | master | PR | PR/master | placebo | min..max master | min..max PR |
|---|---|---:|---:|---:|---:|---|---|
| synth/keyed-16.dfy | Keyed (correctness) | 11.17M | 45.45M | 4.07 | 11.62M | 5.92..22.45M | 8.01..239.98M |
| lit/dafny4/UnionFind.dfy:legacy | M3.UnionFind.Join (correctness) (assertion batch 124) | 6.18M | 22.13M | 3.58 | 9.21M | 1.85..15.67M | 4.47..40.30M |
| lit/dafny4/UnionFind.dfy:legacy | M3.UnionFind.Join (correctness) (assertion batch 47) | 9.36M | 17.48M | 1.87 | 9.64M | 1.83..53.73M | 2.62..41.71M |
| synth/keyed-08.dfy | Keyed (correctness) | 24.88M | 20.17M | 0.81 | 25.55M | 9.25..48.85M | 7.61..35.23M |
| synth/keyed-04.dfy | Keyed (correctness) | 7.83M | 10.87M | 1.39 | 6.19M | 3.75..18.50M | 5.08..20.46M |
| lit/dafny0/Maps.dfy:legacy | GeneralMaps4 (correctness) | 0.17M | 2.96M | 17.47 | 0.17M | 0.17..0.17M | 2.96..2.96M |
| lit/dafny0/Maps.dfy:refresh | GeneralMaps4 (correctness) | 0.17M | 2.96M | 17.47 | 0.17M | 0.17..0.17M | 2.96..2.96M |
| dafnybench/DafnyProjects_tmp_tmp2acw_s4s_RawSort.dfy | rawsort (correctness) | 14.60M | 12.29M | 0.84 | 14.91M | 3.22..27.85M | 3.25..22.05M |
| synth/chain-16.dfy | Chain (correctness) | 0.32M | 2.30M | 7.18 | 0.39M | 0.32..0.32M | 2.30..2.30M |
| lit/dafny4/UnionFind.dfy:refresh | M1.UnionFind.New (correctness) | 4.56M | 3.08M | 0.68 | 4.29M | 2.60..11.31M | 2.41..3.75M |
| lit/dafny4/UnionFind.dfy:legacy | M1.UnionFind.New (correctness) | 4.31M | 3.07M | 0.71 | 3.67M | 2.65..6.39M | 2.43..5.04M |
| synth/ichain-16.dfy | Chain (correctness) | 0.59M | 1.69M | 2.84 | 0.56M | 0.59..0.59M | 1.38..2.24M |
| lit/dafny4/UnionFind.dfy:refresh | M3.UnionFind.Join (correctness) (assertion batch 148) | 3.42M | 4.43M | 1.30 | 3.82M | 1.80..5.06M | 2.43..6.17M |
| lit/dafny4/UnionFind.dfy:refresh | M3.UnionFind.Join (correctness) (assertion batch 111) | 0.76M | 1.68M | 2.23 | 0.82M | 0.51..0.99M | 0.41..2.53M |
| lit/dafny4/UnionFind.dfy:legacy | M3.UnionFind.Join (correctness) (assertion batch 143) | 2.33M | 1.41M | 0.61 | 2.91M | 1.83..2.75M | 0.93..1.76M |
| lit/dafny4/UnionFind.dfy:refresh | M3.UnionFind.Join (correctness) (assertion batch 166) | 0.94M | 1.85M | 1.97 | 0.88M | 0.59..1.02M | 0.43..2.36M |
| lit/VSI-Benchmarks/b4.dfy:legacy | Map.RemoveNonFirst (correctness) | 12.09M | 12.93M | 1.07 | 11.69M | 9.27..14.98M | 8.64..15.99M |
| lit/dafny4/UnionFind.dfy:refresh | M2.UnionFind.FindAux (correctness) | 15.99M | 15.30M | 0.96 | 17.14M | 12.65..22.31M | 4.86..22.70M |
| lit/dafny4/UnionFind.dfy:refresh | M3.UnionFind.Join (correctness) (assertion batch 113) | 0.99M | 0.36M | 0.37 | 1.05M | 0.28..1.54M | 0.27..0.99M |
| lit/dafny4/UnionFind.dfy:refresh | M1.UnionFind.Union (correctness) | 1.69M | 1.09M | 0.65 | 1.43M | 1.01..5.22M | 0.97..1.45M |
| lit/dafny4/UnionFind.dfy:refresh | M3.UnionFind.Join (correctness) (assertion batch 128) | 2.18M | 2.76M | 1.27 | 2.05M | 1.17..7.10M | 0.98..5.85M |
| lit/dafny4/UnionFind.dfy:legacy | M3.UnionFind.Join (correctness) (assertion batch 63) | 0.53M | 1.02M | 1.92 | 0.53M | 0.36..0.70M | 0.78..1.36M |
| lit/dafny4/UnionFind.dfy:legacy | M3.UnionFind.Join (correctness) (assertion batch 109) | 1.27M | 1.75M | 1.38 | 1.26M | 0.81..1.63M | 0.93..2.16M |
| synth/equal-16.dfy | Equal (correctness) | 1.26M | 1.69M | 1.35 | 1.26M | 1.18..1.36M | 1.64..1.72M |
| lit/dafny4/UnionFind.dfy:legacy | M3.UnionFind.Join (correctness) (assertion batch 162) | 1.19M | 1.62M | 1.36 | 1.25M | 0.81..1.47M | 0.74..1.80M |

## Per job (proofs among the affected VCs)

| job | VCs | master | PR | PR vs master | placebo vs master |
|---|---:|---:|---:|---:|---:|
| lit/dafny4/UnionFind.dfy:legacy | 287 | 75.16M | 97.64M | +29.9% | +4.9% |
| lit/dafny4/UnionFind.dfy:refresh | 294 | 68.85M | 68.01M | -1.2% | +1.2% |
| synth/keyed-08.dfy | 1 | 24.88M | 20.17M | -18.9% | +2.7% |
| dafnybench/DafnyProjects_tmp_tmp2acw_s4s_RawSort.dfy | 1 | 14.60M | 12.29M | -15.8% | +2.1% |
| lit/VSI-Benchmarks/b4.dfy:refresh | 14 | 14.30M | 14.82M | +3.6% | -2.7% |
| lit/VSI-Benchmarks/b4.dfy:legacy | 14 | 13.81M | 14.84M | +7.4% | -2.9% |
| lit/git-issues/git-issue-3855.dfy:pinned | 59 | 12.04M | 12.04M | -0.0% | +0.5% |
| synth/keyed-16.dfy | 1 | 11.17M | 45.45M | +306.9% | +4.0% |
| synth/keyed-04.dfy | 1 | 7.83M | 10.87M | +38.8% | -21.0% |
| lit/comp/rust/loops.dfy:legacy | 4 | 5.55M | 5.65M | +1.8% | +0.5% |
| lit/comp/rust/loops.dfy:refresh | 4 | 5.55M | 5.65M | +1.8% | +0.5% |
| synth/keyed-02.dfy | 1 | 5.20M | 4.92M | -5.3% | +0.1% |
| kondo/shardedKvBatched/manual | 17 | 3.24M | 3.24M | -0.1% | +0.2% |
| lit/cloudmake/CloudMake-ParallelBuilds.dfy:legacy | 19 | 2.91M | 2.95M | +1.7% | -0.1% |
| lit/cloudmake/CloudMake-ParallelBuilds.dfy:refresh | 19 | 2.91M | 2.95M | +1.7% | -0.1% |
| kondo/shardedKv/manual | 16 | 2.86M | 2.84M | -0.5% | -0.6% |
| kondo/shardedKvBatched/sync | 9 | 1.77M | 1.78M | +0.5% | +0.0% |
| synth/keyed-01.dfy | 1 | 1.49M | 1.47M | -1.7% | +0.0% |
| synth/equal-16.dfy | 1 | 1.26M | 1.69M | +34.8% | +0.1% |
| lit/dafny0/IMaps.dfy:refresh | 7 | 1.16M | 1.19M | +2.5% | +0.0% |
| lit/dafny0/IMaps.dfy:legacy | 7 | 1.16M | 1.19M | +2.5% | +0.0% |
| lit/comp/rust/operators.dfy:refresh | 7 | 1.10M | 1.06M | -3.1% | +1.4% |
| lit/comp/rust/operators.dfy:legacy | 6 | 1.09M | 1.06M | -3.1% | +1.4% |
| dafnybench/dafny_experiments_tmp_tmpz29_3_3i_circuit.dfy | 12 | 0.99M | 0.95M | -4.1% | -0.0% |
| kondo/shardedKv/sync | 9 | 0.66M | 0.66M | +0.1% | +0.0% |
| lit/dafny0/Maps.dfy:refresh | 13 | 0.61M | 3.39M | +453.0% | +0.8% |
| lit/dafny0/Maps.dfy:legacy | 13 | 0.61M | 3.39M | +453.5% | +0.8% |
| synth/ichain-16.dfy | 1 | 0.59M | 1.69M | +184.0% | -5.6% |
| synth/chain-16.dfy | 1 | 0.32M | 2.30M | +617.9% | +23.3% |
| synth/equal-08.dfy | 1 | 0.27M | 0.29M | +8.2% | +3.6% |
| lit/comp/Comprehensions.dfy:legacy | 5 | 0.25M | 0.25M | -0.8% | +0.5% |
| lit/comp/Comprehensions.dfy:refresh | 5 | 0.23M | 0.23M | -0.2% | +1.0% |
| lit/comp/ComprehensionsNewSyntax.dfy:legacy | 3 | 0.21M | 0.21M | +0.6% | +0.5% |
| lit/comp/ComprehensionsNewSyntax.dfy:refresh | 3 | 0.19M | 0.19M | +1.5% | +1.2% |
| std/Collections/Map.dfy | 5 | 0.16M | 0.16M | +0.1% | +0.0% |
| lit/dafny4/git-issue167.dfy:refresh | 2 | 0.14M | 0.10M | -27.0% | +0.0% |
| synth/spec-16.dfy | 3 | 0.14M | 0.15M | +4.0% | +0.0% |
| lit/dafny4/git-issue167.dfy:legacy | 2 | 0.14M | 0.10M | -27.4% | -0.0% |
| lit/dafny4/KozenSilva.dfy:legacy | 3 | 0.13M | 0.13M | -0.3% | -0.0% |
| lit/dafny4/KozenSilva.dfy:refresh | 3 | 0.13M | 0.13M | -0.3% | -0.0% |
| std/Collections/Imap.dfy | 5 | 0.13M | 0.13M | +1.4% | -0.0% |
| synth/ichain-08.dfy | 1 | 0.10M | 0.26M | +159.7% | -2.5% |
| synth/spec-08.dfy | 3 | 0.10M | 0.10M | +2.0% | +0.0% |
| synth/equal-04.dfy | 1 | 0.08M | 0.07M | -9.2% | +0.0% |
| synth/spec-04.dfy | 3 | 0.08M | 0.08M | +0.9% | +0.0% |
| dafnybench/fv2020-tms_tmp_tmpnp85b47l_modeling_concurrency_safety.dfy | 1 | 0.08M | 0.09M | +13.6% | +0.0% |
| dafnybench/iron-sync_tmp_tmps49o3tyz_lib_Base_MapRemove.dfy | 1 | 0.08M | 0.08M | -0.9% | +0.0% |
| lit/dafny0/GeneralNewtypeCollectionsGeneric.dfy:pinned | 2 | 0.07M | 0.07M | +0.0% | +1.4% |
| lit/git-issues/git-issue-697b.dfy:refresh | 1 | 0.07M | 0.07M | -0.7% | +0.0% |
| dafnybench/dafny-programs_tmp_tmpcwodh6qh_src_ticketsystem.dfy | 1 | 0.07M | 0.08M | +13.7% | +0.0% |
| lit/dafny0/GeneralNewtypeCollections.dfy:pinned | 2 | 0.07M | 0.07M | +0.4% | -1.2% |
| lit/git-issues/git-issue-697b.dfy:legacy | 1 | 0.07M | 0.07M | -1.6% | +0.0% |
| synth/chain-08.dfy | 1 | 0.07M | 0.22M | +215.9% | +31.3% |
| synth/spec-02.dfy | 3 | 0.07M | 0.07M | +0.4% | +0.0% |
| lit/dafny0/ISets.dfy:legacy | 1 | 0.07M | 0.06M | -3.7% | -1.4% |
| lit/dafny0/ISets.dfy:refresh | 1 | 0.07M | 0.06M | -3.7% | -1.4% |
| synth/spec-01.dfy | 3 | 0.06M | 0.06M | +0.3% | +0.0% |
| lit/git-issues/git-issue-1163.dfy:legacy | 1 | 0.06M | 0.06M | +0.4% | -0.1% |
| lit/git-issues/git-issue-1163.dfy:refresh | 1 | 0.06M | 0.06M | +0.4% | -0.1% |
| synth/lookups-16.dfy | 1 | 0.06M | 0.07M | +13.4% | +0.0% |
| lit/comp/Calls.dfy:legacy | 1 | 0.06M | 0.06M | -0.0% | +0.0% |
| lit/comp/firstSteps/6_Calls-VariableCapture.dfy:legacy | 1 | 0.06M | 0.06M | -0.0% | +0.0% |
| synth/ilookups-16.dfy | 1 | 0.06M | 0.07M | +16.8% | +1.5% |
| lit/comp/Calls.dfy:refresh | 1 | 0.06M | 0.06M | +1.1% | +0.0% |
| lit/comp/firstSteps/6_Calls-VariableCapture.dfy:refresh | 1 | 0.06M | 0.06M | +1.1% | +0.0% |
| dafnybench/verification-class_tmp_tmpz9ik148s_2022_chapter05-distributed-state-machines_exercises_UtilitiesLibrary.dfy | 1 | 0.05M | 0.05M | +1.4% | +0.2% |
| synth/update-16.dfy | 1 | 0.05M | 0.05M | +5.4% | +0.0% |
| lit/dafny4/Regression19.dfy:legacy | 1 | 0.05M | 0.05M | +0.4% | +0.0% |
| lit/dafny4/Regression19.dfy:refresh | 1 | 0.05M | 0.05M | +0.4% | +0.0% |
| lit/git-issues/git-issue-1158.dfy:legacy | 1 | 0.04M | 0.04M | -2.3% | +0.0% |
| lit/git-issues/git-issue-1158.dfy:refresh | 1 | 0.04M | 0.04M | -2.3% | +0.0% |
| std/Parsers/Core/ParsersBuilders.dfy | 1 | 0.04M | 0.04M | +0.2% | +0.0% |
| lit/dafny4/Bug58.dfy:legacy | 3 | 0.04M | 0.04M | +0.9% | +0.0% |
| lit/dafny4/Bug58.dfy:refresh | 3 | 0.04M | 0.04M | +0.9% | +0.0% |
| kondo/clientServer/manual | 1 | 0.04M | 0.04M | +0.2% | +0.1% |
| kondo/clientServer/sync | 1 | 0.04M | 0.04M | +0.2% | +0.1% |
| kondo/distributedLock/manual | 1 | 0.04M | 0.04M | +0.2% | +0.1% |
| kondo/distributedLock/sync | 1 | 0.04M | 0.04M | +0.2% | +0.1% |
| kondo/flexPaxos/sync | 1 | 0.04M | 0.04M | +0.2% | +0.1% |
| kondo/lockServer/manual | 1 | 0.04M | 0.04M | +0.2% | +0.1% |
| kondo/lockServer/sync | 1 | 0.04M | 0.04M | +0.2% | +0.1% |
| kondo/paxos/sync | 1 | 0.04M | 0.04M | +0.2% | +0.1% |
| kondo/ringLeaderElection/manual | 1 | 0.04M | 0.04M | +0.2% | +0.1% |
| kondo/ringLeaderElection/sync | 1 | 0.04M | 0.04M | +0.2% | +0.1% |
| kondo/simplifiedLeaderElection/manual | 1 | 0.04M | 0.04M | +0.2% | +0.1% |
| kondo/simplifiedLeaderElection/sync | 1 | 0.04M | 0.04M | +0.2% | +0.1% |
| kondo/twoPhaseCommit/manual | 1 | 0.04M | 0.04M | +0.2% | +0.1% |
| kondo/twoPhaseCommit/paper-version | 1 | 0.04M | 0.04M | +0.2% | +0.1% |
| kondo/twoPhaseCommit/sync | 1 | 0.04M | 0.04M | +0.2% | +0.1% |
| synth/ichain-04.dfy | 1 | 0.03M | 0.07M | +95.8% | +2.0% |
| lit/dafny0/DiscoverBounds.dfy:legacy | 1 | 0.03M | 0.03M | +0.3% | +0.0% |
| lit/dafny0/DiscoverBounds.dfy:refresh | 1 | 0.03M | 0.03M | +0.3% | +0.0% |
| synth/lookups-08.dfy | 1 | 0.03M | 0.04M | +19.3% | +0.0% |
| synth/ilookups-08.dfy | 1 | 0.03M | 0.03M | -0.0% | +0.0% |
| synth/equal-02.dfy | 1 | 0.03M | 0.03M | -4.6% | +0.0% |
| synth/update-08.dfy | 1 | 0.03M | 0.03M | +4.6% | +0.0% |
| synth/chain-04.dfy | 1 | 0.03M | 0.07M | +129.8% | +3.3% |
| lit/dafny4/git-issue75.dfy:legacy | 2 | 0.03M | 0.03M | +0.6% | +0.0% |
| lit/dafny4/git-issue75.dfy:refresh | 2 | 0.03M | 0.03M | +0.6% | +0.0% |
| lit/comp/CovariantCollections.dfy:pinned | 1 | 0.03M | 0.03M | +0.3% | +0.0% |
| synth/update-04.dfy | 1 | 0.02M | 0.02M | +3.2% | +0.0% |
| synth/ilookups-04.dfy | 1 | 0.02M | 0.03M | +30.7% | +0.0% |
| synth/lookups-04.dfy | 1 | 0.02M | 0.03M | +23.8% | +0.0% |
| lit/dafny0/GeneralNewtypeMemberCompile.dfy:pinned | 1 | 0.02M | 0.02M | +0.4% | +0.0% |
| synth/update-02.dfy | 1 | 0.02M | 0.02M | +2.0% | +0.0% |
| dafnybench/Clover_update_map.dfy | 1 | 0.02M | 0.02M | +1.3% | +0.1% |
| synth/ichain-02.dfy | 1 | 0.02M | 0.03M | +64.2% | +3.4% |
| synth/update-01.dfy | 1 | 0.02M | 0.02M | +1.3% | +0.0% |
| lit/git-issues/git-issue-3320.dfy:legacy | 1 | 0.02M | 0.02M | +0.4% | -0.0% |
| lit/git-issues/git-issue-3320.dfy:refresh | 1 | 0.02M | 0.02M | +0.4% | -0.0% |
| synth/ilookups-02.dfy | 1 | 0.02M | 0.02M | +0.9% | +0.0% |
| lit/dafny0/TypeAdjustments.dfy:pinned | 1 | 0.02M | 0.02M | +0.4% | -0.0% |
| synth/chain-02.dfy | 1 | 0.02M | 0.03M | +78.1% | +2.5% |
| synth/lookups-02.dfy | 1 | 0.02M | 0.02M | +26.3% | +0.0% |
| lit/git-issues/git-issue-1165.dfy:legacy | 1 | 0.02M | 0.02M | +0.5% | +0.0% |
| lit/git-issues/git-issue-1165.dfy:refresh | 1 | 0.02M | 0.02M | +0.5% | +0.0% |
| synth/equal-01.dfy | 1 | 0.02M | 0.02M | -0.5% | +0.0% |
| synth/ilookups-01.dfy | 1 | 0.02M | 0.02M | +0.8% | +0.0% |
| lit/dafny4/Bug54.dfy:legacy | 1 | 0.02M | 0.02M | +2.0% | +0.0% |
| lit/dafny4/Bug54.dfy:refresh | 1 | 0.02M | 0.02M | +2.0% | +0.0% |
| synth/ichain-01.dfy | 1 | 0.02M | 0.02M | +1.7% | +0.1% |
| lit/git-issues/git-issue-336.dfy:legacy | 1 | 0.02M | 0.02M | +0.5% | +0.0% |
| lit/git-issues/git-issue-336.dfy:refresh | 1 | 0.02M | 0.02M | +0.5% | +0.0% |
| synth/lookups-01.dfy | 1 | 0.02M | 0.02M | +22.3% | +0.0% |
| synth/chain-01.dfy | 1 | 0.02M | 0.02M | +13.3% | +0.0% |
| lit/dafny0/Compilation.legacy.dfy:pinned | 1 | 0.01M | 0.01M | +0.6% | +0.0% |
| lit/dafny4/git-issue27.dfy:legacy | 1 | 0.01M | 0.01M | +0.7% | +0.0% |
| lit/dafny4/git-issue27.dfy:refresh | 1 | 0.01M | 0.01M | +0.6% | +0.0% |
| lit/dafny4/Bug108.dfy:legacy | 1 | 0.01M | 0.01M | +0.7% | +0.0% |
| lit/dafny4/Bug108.dfy:refresh | 1 | 0.01M | 0.01M | +0.7% | +0.0% |

## Synthetic programs: total RU by size N (master / PR / placebo, mean over seeds)

| family | N=1 | N=2 | N=4 | N=8 | N=16 |
|---|---|---|---|---|---|
| chain | 0.02 / 0.02 / 0.02 | 0.02 / 0.03 / 0.02 | 0.03 / 0.07 / 0.03 | 0.07 / 0.22 / 0.09 | 0.32 / 2.30 / 0.39 |
| equal | 0.02 / 0.02 / 0.02 | 0.03 / 0.03 / 0.03 | 0.08 / 0.07 / 0.08 | 0.27 / 0.29 / 0.28 | 1.26 / 1.69 / 1.26 |
| ichain | 0.02 / 0.02 / 0.02 | 0.02 / 0.03 / 0.02 | 0.03 / 0.07 / 0.03 | 0.10 / 0.26 / 0.10 | 0.59 / 1.69 / 0.56 |
| ilookups | 0.02 / 0.02 / 0.02 | 0.02 / 0.02 / 0.02 | 0.02 / 0.03 / 0.02 | 0.03 / 0.03 / 0.03 | 0.06 / 0.07 / 0.06 |
| keyed | 1.49 / 1.47 / 1.50 | 5.20 / 4.92 / 5.20 | 7.83 / 10.87 / 6.19 | 24.88 / 20.17 / 25.55 | 11.17 / 45.45 / 11.62 |
| lookups | 0.02 / 0.02 / 0.02 | 0.02 / 0.02 / 0.02 | 0.02 / 0.03 / 0.02 | 0.03 / 0.04 / 0.03 | 0.06 / 0.07 / 0.06 |
| spec | 0.08 / 0.08 / 0.08 | 0.08 / 0.08 / 0.08 | 0.09 / 0.09 / 0.09 | 0.11 / 0.11 / 0.11 | 0.16 / 0.16 / 0.16 |
| update | 0.02 / 0.02 / 0.02 | 0.02 / 0.02 / 0.02 | 0.02 / 0.02 / 0.02 | 0.03 / 0.03 / 0.03 | 0.05 / 0.05 / 0.05 |

## dafny4/UnionFind.dfy as on master (Main not isolated): Main's cost per seed

| resolver | prelude | seed 0 | seed 1 | seed 2 | seed 3 | seed 4 | seed 5 | seed 6 | seed 7 | over 50M |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| legacy | master | 20.7M | 17.0M | 67.6M | 11.8M | 29.3M | 29.3M | 22.6M | 14.8M | 1 |
| legacy | pr | 31.2M | 20.2M | 85.2M | 14.2M | 41.2M | 18.8M | 76.6M | 10.7M | 2 |
| legacy | placebo | 29.3M | 15.1M | 63.7M | 48.3M | 86.0M | 46.7M | 34.1M | 11.8M | 2 |
| legacy | domguard | 19.0M | 76.5M | 58.3M | 15.4M | 42.2M | 14.4M | 25.5M | 15.7M | 2 |
| legacy | master2 | 20.7M | 17.0M | 67.6M | 11.8M | 29.3M | 29.3M | 22.6M | 14.8M | 1 |
| legacy | pointwise | 42.9M | 15.9M | 37.5M | 13.9M | 58.9M | 18.7M | 36.6M | 18.5M | 1 |
| refresh | master | 21.1M | 20.7M | 30.9M | 13.8M | 23.8M | 10.1M | 37.1M | 31.0M | 0 |
| refresh | pr | 53.4M | 41.5M | 26.0M | 19.1M | 15.2M | 15.1M | 48.4M | 47.0M | 1 |
| refresh | placebo | 77.1M | 48.9M | 26.0M | 14.1M | 23.8M | 10.1M | 29.0M | 21.4M | 1 |
| refresh | domguard | 65.6M | 22.1M | 29.4M | 54.6M | 68.9M | 59.4M | 40.0M | 56.5M | 5 |
| refresh | master2 | 21.1M | 20.7M | 30.9M | 13.8M | 23.8M | 10.1M | 37.1M | 31.0M | 0 |
| refresh | pointwise | 33.1M | 13.2M | 48.8M | 18.0M | 35.0M | 13.9M | 26.4M | 13.5M | 0 |

## Comparisons over the affected proofs (all but synth)

| comparison | programs | VCs | total | geomean over VCs | per program | verdict flips at limit |
|---|---:|---:|---|---|---|---:|
| A/A: master2 vs master (same input, another process) | 63 | 934 | -0.0% [-0.0%, +0.0%] | +0.0% [-0.0%, +0.0%] | +0.0% [-0.0%, +0.0%] | 0 |
| placebo vs master (the old axiom, rewritten) | 63 | 934 | +1.8% [-1.4%, +2.8%] | +0.1% [+0.0%, +0.1%] | +0.1% [-0.0%, +0.2%] | 0 |
| shape: pointwise vs master (the PR's quantifier without its guard) | 63 | 934 | +1.1% [-12.8%, +4.7%] | +0.0% [-0.7%, +0.2%] | -0.8% [-2.2%, +0.2%] | 1 |
| guard: pr vs pointwise | 63 | 934 | +10.1% [+2.7%, +25.8%] | +1.6% [+0.6%, +5.6%] | +1.4% [+0.5%, +2.6%] | 0 |
| pr vs master | 63 | 934 | +11.3% [-4.6%, +20.6%] | +1.6% [+0.3%, +5.5%] | +0.6% [-0.6%, +1.9%] | 1 |
| domguard vs master | 63 | 934 | +1.2% [-7.3%, +3.8%] | +0.8% [+0.0%, +1.4%] | +0.1% [-0.9%, +1.0%] | 1 |
| domguard vs pr | 63 | 934 | -9.1% [-19.0%, -0.2%] | -0.8% [-4.4%, -0.1%] | -0.6% [-1.4%, -0.0%] | 0 |

## ... whose SMT contains the changed axiom (classify.py)

| comparison | programs | VCs | total | geomean over VCs | per program | verdict flips at limit |
|---|---:|---:|---|---|---|---:|
| A/A: master2 vs master (same input, another process) | 60 | 900 | +0.0% [+0.0%, +0.0%] | +0.0% [+0.0%, +0.0%] | +0.0% [+0.0%, +0.0%] | 0 |
| placebo vs master (the old axiom, rewritten) | 60 | 900 | +1.8% [-1.5%, +2.9%] | +0.1% [+0.0%, +0.1%] | +0.1% [+0.0%, +0.3%] | 0 |
| shape: pointwise vs master (the PR's quantifier without its guard) | 60 | 900 | +1.1% [-13.8%, +4.6%] | +0.0% [-0.8%, +0.2%] | -0.9% [-2.5%, +0.1%] | 1 |
| guard: pr vs pointwise | 60 | 900 | +10.2% [+3.0%, +26.3%] | +1.6% [+0.6%, +6.3%] | +1.5% [+0.5%, +2.8%] | 0 |
| pr vs master | 60 | 900 | +11.4% [-3.3%, +21.6%] | +1.6% [+0.2%, +5.8%] | +0.5% [-0.8%, +1.9%] | 1 |
| domguard vs master | 60 | 900 | +1.2% [-7.2%, +3.8%] | +0.8% [-0.1%, +1.5%] | -0.1% [-1.1%, +0.9%] | 1 |
| domguard vs pr | 60 | 900 | -9.2% [-19.4%, -0.3%] | -0.8% [-4.7%, -0.0%] | -0.6% [-1.4%, -0.0%] | 0 |

## ... whose SMT does not: a pure perturbation

| comparison | programs | VCs | total | geomean over VCs | per program | verdict flips at limit |
|---|---:|---:|---|---|---|---:|
| A/A: master2 vs master (same input, another process) | 2 | 15 | -0.0% [-0.0%, +0.0%] | +0.0% [-0.0%, +0.0%] | +0.0% [-0.0%, +0.0%] | 0 |
| placebo vs master (the old axiom, rewritten) | 2 | 15 | +0.0% [-0.0%, +0.1%] | +0.0% [+0.0%, +0.0%] | +0.0% [+0.0%, +0.0%] | 0 |
| shape: pointwise vs master (the PR's quantifier without its guard) | 2 | 15 | +0.0% [-0.0%, +0.1%] | +0.0% [-0.0%, +0.1%] | +0.0% [-0.0%, +0.1%] | 0 |
| guard: pr vs pointwise | 2 | 15 | -0.0% [-0.1%, +0.0%] | -0.0% [-0.1%, +0.0%] | -0.0% [-0.1%, +0.0%] | 0 |
| pr vs master | 2 | 15 | +0.0% [-0.0%, +0.0%] | +0.0% [+0.0%, +0.0%] | +0.0% [+0.0%, +0.0%] | 0 |
| domguard vs master | 2 | 15 | +0.0% [-0.0%, +0.1%] | +0.0% [-0.0%, +0.1%] | +0.0% [-0.0%, +0.1%] | 0 |
| domguard vs pr | 2 | 15 | +0.0% [-0.0%, +0.1%] | +0.0% [-0.0%, +0.1%] | +0.0% [-0.0%, +0.1%] | 0 |

19 of the 934 affected proofs have no classification (unmapped or mixed log names).

## Comparisons over the external programs' affected proofs

| comparison | programs | VCs | total | geomean over VCs | per program | verdict flips at limit |
|---|---:|---:|---|---|---|---:|
| A/A: master2 vs master (same input, another process) | 26 | 84 | +0.0% [+0.0%, +0.0%] | +0.0% [+0.0%, +0.0%] | +0.0% [+0.0%, +0.0%] | 0 |
| placebo vs master (the old axiom, rewritten) | 26 | 84 | +1.2% [-0.3%, +1.9%] | +0.0% [-0.0%, +0.2%] | +0.2% [+0.1%, +0.3%] | 0 |
| shape: pointwise vs master (the PR's quantifier without its guard) | 26 | 84 | -18.3% [-27.8%, +0.4%] | -0.5% [-1.8%, +0.2%] | -1.2% [-4.2%, +0.5%] | 0 |
| guard: pr vs pointwise | 26 | 84 | +11.0% [-0.4%, +18.6%] | +0.8% [+0.3%, +1.8%] | +1.8% [+0.3%, +3.8%] | 0 |
| pr vs master | 26 | 84 | -9.3% [-14.2%, +0.5%] | +0.3% [-0.4%, +1.1%] | +0.5% [-1.3%, +2.5%] | 0 |
| domguard vs master | 26 | 84 | -9.1% [-13.9%, +0.5%] | +0.1% [-0.7%, +0.8%] | -0.1% [-1.9%, +1.8%] | 0 |
| domguard vs pr | 26 | 84 | +0.2% [-0.1%, +0.3%] | -0.2% [-0.5%, -0.1%] | -0.6% [-0.8%, -0.4%] | 0 |

## Alternative sound encodings, over the same proofs

restrict: elements defined everywhere, `$ArbitraryBoxValue` outside the domain. domguard: the PR's axiom guarded by `Map#Domain(Map#Glue(a, b, t))`. eager: the PR's axiom plus the trigger `{ Map#Glue(a, b, t), Set#IsMember(a, bx) }`.

| encoding | programs | VCs | total vs master | geomean over VCs vs master | per program vs master | per program vs PR | verdict flips vs master at limit |
|---|---:|---:|---|---|---|---|---:|
| pr | 63 | 934 | +11.3% [-3.4%, +21.5%] | +1.6% [+0.3%, +5.6%] | +0.6% [-0.6%, +2.0%] |  | 6 |
| domguard | 63 | 934 | +1.2% [-7.2%, +3.8%] | +0.8% [+0.0%, +1.4%] | +0.1% [-0.9%, +1.0%] | -0.6% [-1.3%, -0.0%] | 5 |
| master2 | 63 | 934 | -0.0% [-0.0%, +0.0%] | +0.0% [-0.0%, +0.0%] | +0.0% [-0.0%, +0.0%] | -0.6% [-1.9%, +0.6%] | 0 |
| pointwise | 63 | 934 | +1.1% [-13.0%, +4.6%] | +0.0% [-0.8%, +0.2%] | -0.8% [-2.2%, +0.2%] | -1.4% [-2.6%, -0.5%] | 5 |

domguard: largest differences from the PR

| job | VC | master | PR | domguard |
|---|---|---:|---:|---:|
| lit/dafny4/UnionFind.dfy:legacy | M3.UnionFind.Join (correctness) (assertion batch 124) | 6.18M | 22.13M | 7.74M |
| lit/dafny4/UnionFind.dfy:legacy | M3.UnionFind.Join (correctness) (assertion batch 47) | 9.36M | 17.48M | 11.24M |
| lit/dafny4/UnionFind.dfy:refresh | M3.UnionFind.Join (correctness) (assertion batch 128) | 2.18M | 2.76M | 6.41M |
| lit/dafny4/UnionFind.dfy:legacy | M2.UnionFind.FindAux (correctness) | 13.66M | 13.73M | 16.74M |
| lit/dafny0/Maps.dfy:legacy | GeneralMaps4 (correctness) | 0.17M | 2.96M | 0.18M |
| lit/dafny0/Maps.dfy:refresh | GeneralMaps4 (correctness) | 0.17M | 2.96M | 0.18M |

master2: largest differences from the PR

| job | VC | master | PR | master2 |
|---|---|---:|---:|---:|
| lit/dafny4/UnionFind.dfy:legacy | M3.UnionFind.Join (correctness) (assertion batch 124) | 6.18M | 22.13M | 6.18M |
| lit/dafny4/UnionFind.dfy:legacy | M3.UnionFind.Join (correctness) (assertion batch 47) | 9.36M | 17.48M | 9.36M |
| lit/dafny0/Maps.dfy:legacy | GeneralMaps4 (correctness) | 0.17M | 2.96M | 0.17M |
| lit/dafny0/Maps.dfy:refresh | GeneralMaps4 (correctness) | 0.17M | 2.96M | 0.17M |
| dafnybench/DafnyProjects_tmp_tmp2acw_s4s_RawSort.dfy | rawsort (correctness) | 14.60M | 12.29M | 14.60M |
| lit/dafny4/UnionFind.dfy:refresh | M1.UnionFind.New (correctness) | 4.56M | 3.08M | 4.56M |

pointwise: largest differences from the PR

| job | VC | master | PR | pointwise |
|---|---|---:|---:|---:|
| lit/dafny4/UnionFind.dfy:legacy | M3.UnionFind.Join (correctness) (assertion batch 124) | 6.18M | 22.13M | 4.16M |
| lit/dafny4/UnionFind.dfy:legacy | M3.UnionFind.Join (correctness) (assertion batch 47) | 9.36M | 17.48M | 8.22M |
| lit/dafny4/UnionFind.dfy:refresh | M2.UnionFind.FindAux (correctness) | 15.99M | 15.30M | 23.80M |
| lit/dafny0/Maps.dfy:legacy | GeneralMaps4 (correctness) | 0.17M | 2.96M | 0.17M |
| lit/dafny0/Maps.dfy:refresh | GeneralMaps4 (correctness) | 0.17M | 2.96M | 0.17M |
| lit/dafny4/UnionFind.dfy:legacy | M2.UnionFind.FindAux (correctness) | 13.66M | 13.73M | 16.43M |

Synthetic programs at N=16 (total RU, mean over seeds):

| family | master | pr | domguard | master2 | pointwise |
|---|---:|---:|---:|---:|---:|
| chain | 0.32M | 2.30M | 0.33M | 0.32M | 0.29M |
| equal | 1.26M | 1.69M | 1.68M | 1.26M | 1.18M |
| ichain | 0.59M | 1.69M | 0.60M | 0.59M | 0.60M |
| ilookups | 0.06M | 0.07M | 0.06M | 0.06M | 0.06M |
| keyed | 11.17M | 45.45M | 39.41M | 11.17M | 40.24M |
| lookups | 0.06M | 0.07M | 0.07M | 0.06M | 0.07M |
| spec | 0.16M | 0.16M | 0.17M | 0.16M | 0.16M |
| update | 0.05M | 0.05M | 0.05M | 0.05M | 0.05M |
