# Map#Glue prelude A/B benchmark

Seeds per (VC, prelude): 5 (0, 1, 2, 3, 4; 0 is Dafny's default). VCs: 1867 in 114 jobs; **927 affected** (master and PR counts differ), 940 unaffected (identical counts under master and PR for every seed).
Unaffected VCs whose counts differ under the placebo: 4.

## Proof cost over affected VCs that pass everywhere

Totals are sums of per-VC means over seeds; brackets are 95% bootstrap intervals over VCs.

| group | VCs | master RU | PR RU | PR vs master | geomean PR/master | placebo vs master | placebo geomean |
|---|---:|---:|---:|---|---|---|---|
| lit + std | 841 | 202.2M | 228.5M | +13.0% [-4.0%, +35.7%] | +1.9% [+0.7%, +3.3%] | -1.6% [-4.7%, +1.2%] | +0.1% [-0.1%, +0.2%] |
| lit | 830 | 201.9M | 228.1M | +13.0% [-3.4%, +35.0%] | +1.9% [+0.7%, +3.4%] | -1.6% [-4.7%, +1.2%] | +0.1% [-0.1%, +0.2%] |
| std | 11 | 0.3M | 0.3M | +0.5% [-0.7%, +1.5%] | +0.6% [-0.6%, +1.8%] | +0.0% [+0.0%, +0.0%] | +0.0% [+0.0%, +0.0%] |
| synth | 50 | 41.0M | 53.3M | +29.9% [+6.0%, +64.4%] | +23.3% [+11.7%, +38.1%] | +2.0% [-9.9%, +11.7%] | +1.0% [-0.6%, +2.9%] |

36 affected VCs fail (a verification error) in some run; their cost is the solver's search for a counterexample, reported separately:

| job | VC | master mean (min..max) | PR mean (min..max) | placebo mean |
|---|---|---|---|---|
| lit/git-issues/git-issue-3855.dfy:pinned | Memory.dynMove (correctness) | 128.62M (63.53..258.59) | 152.26M (72.49..236.83) | 139.82M |
| lit/git-issues/git-issue-3855.dfy:pinned | Memory.dynCopy (correctness) | 3.99M (2.32..5.97) | 3.93M (2.32..5.27) | 3.96M |
| lit/git-issues/git-issue-3855.dfy:pinned | Main1 (correctness) | 3.48M (2.34..5.06) | 3.41M (2.65..5.06) | 3.48M |
| lit/dafny0/TypeAdjustments.dfy:pinned | Comprehensions.Maps1 (correctness) | 0.61M (0.49..0.73) | 0.61M (0.48..0.73) | 0.61M |
| lit/dafny0/IMaps.dfy:legacy | m4 (correctness) | 0.04M (0.02..0.08) | 0.04M (0.02..0.08) | 0.04M |
| lit/dafny0/IMaps.dfy:refresh | m4 (correctness) | 0.04M (0.02..0.08) | 0.04M (0.02..0.08) | 0.04M |
| lit/dafny0/Maps.dfy:legacy | GeneralMaps5 (correctness) | 0.04M (0.04..0.04) | 0.04M (0.04..0.04) | 0.04M |
| lit/dafny0/Maps.dfy:refresh | GeneralMaps5 (correctness) | 0.04M (0.04..0.04) | 0.04M (0.04..0.04) | 0.04M |
| lit/git-issues/git-issue-851.dfy:legacy | OtherBindersInStatements.MapComprehension3 (correctness) | 0.03M (0.03..0.05) | 0.03M (0.03..0.05) | 0.03M |
| lit/git-issues/git-issue-851.dfy:refresh | OtherBindersInStatements.MapComprehension3 (correctness) | 0.03M (0.03..0.05) | 0.03M (0.03..0.05) | 0.03M |

## Total proof RU per seed (affected VCs that pass everywhere)

| prelude | seed 0 | seed 1 | seed 2 | seed 3 | seed 4 | mean | sd |
|---|---:|---:|---:|---:|---:|---:|---:|
| master | 268.8M | 239.0M | 233.0M | 258.0M | 217.3M | 243.2M | 18.3M |
| pr | 293.2M | 283.6M | 247.7M | 283.3M | 300.9M | 281.7M | 18.2M |
| placebo | 260.3M | 238.8M | 228.4M | 258.5M | 218.5M | 240.9M | 16.4M |

## Solver time over those proofs (sum of per-VC means, seconds)

| group | master | PR | placebo |
|---|---:|---:|---:|
| all | 143.2 | 164.9 | 138.5 |
| lit | 137.0 | 157.3 | 132.2 |
| std | 0.4 | 0.4 | 0.4 |
| synth | 5.9 | 7.3 | 5.9 |

## Distribution of per-VC cost ratios over those proofs (mean over seeds)

| ratio bucket | PR/master | placebo/master |
|---|---:|---:|
| < 0.5x | 1 | 0 |
| 0.5-0.8x | 12 | 1 |
| 0.8-0.95x | 23 | 8 |
| 0.95-1.05x | 774 | 864 |
| 1.05-1.25x | 40 | 16 |
| 1.25-2x | 27 | 2 |
| 2-4x | 10 | 0 |
| >= 4x | 4 | 0 |

## Verdict changes at each job's limit (seeds passing out of 5)

| job | VC | limit | master ok | PR ok | placebo ok | master RU | PR RU |
|---|---|---:|---:|---:|---:|---:|---:|
| lit/git-issues/git-issue-6535.dfy:legacy | Bad (correctness) | 50M | 5 | 0 | 5 | 0.03M | 0.03M |
| lit/git-issues/git-issue-6535.dfy:refresh | Bad (correctness) | 50M | 5 | 0 | 5 | 0.03M | 0.03M |

## Largest changes among those proofs (by |PR - master| mean RU)

| job | VC | master | PR | PR/master | placebo | min..max master | min..max PR |
|---|---|---:|---:|---:|---:|---|---|
| lit/dafny4/UnionFind.dfy:legacy | M3.UnionFind.Join (correctness) (assertion batch 124) | 4.61M | 18.64M | 4.04 | 4.89M | 2.82..9.46M | 10.85..28.96M |
| lit/dafny4/UnionFind.dfy:legacy | M3.UnionFind.Join (correctness) (assertion batch 47) | 3.58M | 13.85M | 3.87 | 3.46M | 2.58..5.02M | 3.51..49.92M |
| lit/dafny4/UnionFind.dfy:legacy | M2.UnionFind.FindAux (correctness) | 17.29M | 10.31M | 0.60 | 14.10M | 12.20..27.11M | 6.14..14.79M |
| synth/keyed-16.dfy | Keyed (correctness) | 9.05M | 13.81M | 1.53 | 10.58M | 5.76..15.39M | 8.60..15.72M |
| lit/dafny4/UnionFind.dfy:refresh | M2.UnionFind.FindAux (correctness) | 17.66M | 13.77M | 0.78 | 16.83M | 13.98..21.99M | 9.28..21.97M |
| synth/keyed-04.dfy | Keyed (correctness) | 9.79M | 13.00M | 1.33 | 9.79M | 5.31..18.51M | 5.40..26.12M |
| lit/VSI-Benchmarks/b4.dfy:legacy | Map.RemoveNonFirst (correctness) | 10.34M | 13.35M | 1.29 | 10.54M | 9.04..12.97M | 11.01..15.66M |
| lit/dafny0/Maps.dfy:legacy | GeneralMaps4 (correctness) | 0.17M | 2.96M | 17.52 | 0.17M | 0.17..0.17M | 2.96..2.96M |
| lit/dafny0/Maps.dfy:refresh | GeneralMaps4 (correctness) | 0.17M | 2.96M | 17.52 | 0.17M | 0.17..0.17M | 2.96..2.96M |
| synth/chain-16.dfy | Chain (correctness) | 0.32M | 2.30M | 7.18 | 0.39M | 0.32..0.32M | 2.30..2.30M |
| lit/dafny4/UnionFind.dfy:refresh | M3.UnionFind.Join (correctness) (assertion batch 128) | 2.05M | 3.94M | 1.92 | 2.32M | 1.43..2.68M | 1.41..9.53M |
| lit/VSI-Benchmarks/b4.dfy:refresh | Map.RemoveNonFirst (correctness) | 10.55M | 12.22M | 1.16 | 10.78M | 6.67..16.00M | 6.04..17.92M |
| synth/keyed-08.dfy | Keyed (correctness) | 10.70M | 12.35M | 1.15 | 11.07M | 7.44..14.53M | 7.75..15.93M |
| synth/keyed-02.dfy | Keyed (correctness) | 6.27M | 4.98M | 0.79 | 5.07M | 4.81..11.25M | 4.80..5.24M |
| lit/dafny4/UnionFind.dfy:refresh | M3.UnionFind.Join (correctness) (assertion batch 166) | 0.63M | 1.69M | 2.68 | 0.63M | 0.53..1.02M | 0.43..2.43M |
| lit/dafny4/UnionFind.dfy:legacy | M3.UnionFind.Join (correctness) (assertion batch 143) | 2.39M | 1.34M | 0.56 | 2.38M | 1.88..3.15M | 0.89..1.58M |
| synth/ichain-16.dfy | Chain (correctness) | 0.59M | 1.55M | 2.61 | 0.56M | 0.59..0.59M | 1.38..2.08M |
| lit/dafny4/UnionFind.dfy:refresh | M3.UnionFind.Join (correctness) (assertion batch 35) | 1.87M | 1.00M | 0.54 | 1.83M | 1.31..2.58M | 0.60..1.57M |
| lit/dafny4/UnionFind.dfy:refresh | M1.UnionFind.New (correctness) | 5.58M | 4.76M | 0.85 | 5.97M | 2.84..9.15M | 3.11..8.95M |
| lit/dafny4/UnionFind.dfy:refresh | M3.UnionFind.Join (correctness) (assertion batch 168) | 1.08M | 0.26M | 0.24 | 1.02M | 1.01..1.30M | 0.26..0.26M |
| lit/dafny4/UnionFind.dfy:legacy | M3.UnionFind.Join (correctness) (assertion batch 109) | 1.33M | 2.07M | 1.55 | 1.33M | 0.81..1.72M | 1.89..2.25M |
| lit/dafny4/UnionFind.dfy:legacy | M3.UnionFind.Join (correctness) (assertion batch 119) | 4.39M | 5.06M | 1.15 | 4.45M | 3.82..5.36M | 4.15..6.19M |
| lit/dafny4/UnionFind.dfy:refresh | M3.UnionFind.Join (correctness) (assertion batch 48) | 2.49M | 3.13M | 1.26 | 1.60M | 1.28..5.90M | 1.29..5.03M |
| synth/equal-16.dfy | Equal (correctness) | 1.16M | 1.69M | 1.46 | 1.20M | 1.03..1.22M | 1.66..1.72M |
| lit/dafny4/UnionFind.dfy:refresh | M3.UnionFind.Join (correctness) (assertion batch 111) | 0.99M | 1.49M | 1.50 | 0.99M | 0.97..1.02M | 0.42..2.48M |

## Per job (proofs among the affected VCs)

| job | VCs | master | PR | PR vs master | placebo vs master |
|---|---:|---:|---:|---:|---:|
| lit/dafny4/UnionFind.dfy:refresh | 294 | 70.94M | 68.43M | -3.5% | -1.6% |
| lit/dafny4/UnionFind.dfy:legacy | 287 | 70.59M | 88.57M | +25.5% | -3.2% |
| lit/VSI-Benchmarks/b4.dfy:refresh | 14 | 12.27M | 14.15M | +15.3% | +1.9% |
| lit/VSI-Benchmarks/b4.dfy:legacy | 14 | 12.03M | 15.25M | +26.7% | +1.7% |
| lit/git-issues/git-issue-3855.dfy:pinned | 59 | 11.12M | 11.05M | -0.6% | +0.1% |
| synth/keyed-08.dfy | 1 | 10.70M | 12.35M | +15.4% | +3.4% |
| synth/keyed-04.dfy | 1 | 9.79M | 13.00M | +32.8% | +0.0% |
| synth/keyed-16.dfy | 1 | 9.05M | 13.81M | +52.7% | +16.9% |
| synth/keyed-02.dfy | 1 | 6.27M | 4.98M | -20.6% | -19.1% |
| lit/comp/rust/loops.dfy:legacy | 4 | 5.66M | 5.67M | +0.2% | -2.1% |
| lit/comp/rust/loops.dfy:refresh | 4 | 5.66M | 5.67M | +0.2% | -2.1% |
| lit/cloudmake/CloudMake-ParallelBuilds.dfy:legacy | 19 | 2.82M | 2.85M | +1.0% | +0.8% |
| lit/cloudmake/CloudMake-ParallelBuilds.dfy:refresh | 19 | 2.82M | 2.85M | +1.0% | +0.8% |
| synth/keyed-01.dfy | 1 | 1.53M | 1.50M | -1.7% | +0.0% |
| synth/equal-16.dfy | 1 | 1.16M | 1.69M | +45.6% | +3.4% |
| lit/dafny0/IMaps.dfy:refresh | 7 | 1.12M | 1.16M | +4.0% | -0.0% |
| lit/dafny0/IMaps.dfy:legacy | 7 | 1.12M | 1.16M | +4.1% | +0.0% |
| lit/comp/rust/operators.dfy:refresh | 3 | 0.87M | 0.89M | +3.0% | +1.9% |
| lit/comp/rust/operators.dfy:legacy | 2 | 0.79M | 0.82M | +3.2% | +2.0% |
| lit/dafny0/Maps.dfy:refresh | 13 | 0.61M | 3.40M | +460.7% | +1.0% |
| lit/dafny0/Maps.dfy:legacy | 13 | 0.61M | 3.40M | +461.0% | +1.0% |
| synth/ichain-16.dfy | 1 | 0.59M | 1.55M | +161.4% | -5.6% |
| synth/chain-16.dfy | 1 | 0.32M | 2.30M | +618.0% | +23.1% |
| synth/equal-08.dfy | 1 | 0.28M | 0.29M | +3.1% | -0.0% |
| lit/comp/Comprehensions.dfy:legacy | 5 | 0.26M | 0.25M | -1.4% | -1.8% |
| lit/comp/Comprehensions.dfy:refresh | 4 | 0.23M | 0.23M | +1.3% | -1.1% |
| lit/comp/ComprehensionsNewSyntax.dfy:legacy | 3 | 0.21M | 0.21M | -0.9% | -2.2% |
| lit/comp/ComprehensionsNewSyntax.dfy:refresh | 3 | 0.19M | 0.19M | +0.4% | -1.3% |
| std/Collections/Map.dfy | 5 | 0.16M | 0.16M | -0.2% | +0.0% |
| lit/dafny4/git-issue167.dfy:refresh | 2 | 0.15M | 0.10M | -28.0% | +0.0% |
| synth/spec-16.dfy | 3 | 0.14M | 0.15M | +4.1% | -0.0% |
| lit/dafny4/git-issue167.dfy:legacy | 2 | 0.14M | 0.10M | -26.3% | -0.0% |
| lit/dafny4/KozenSilva.dfy:legacy | 3 | 0.13M | 0.13M | -0.3% | -0.0% |
| lit/dafny4/KozenSilva.dfy:refresh | 3 | 0.13M | 0.13M | -0.3% | -0.0% |
| std/Collections/Imap.dfy | 5 | 0.13M | 0.13M | +1.3% | +0.0% |
| synth/ichain-08.dfy | 1 | 0.10M | 0.25M | +150.9% | -2.5% |
| synth/spec-08.dfy | 3 | 0.10M | 0.10M | +2.1% | -0.0% |
| synth/equal-04.dfy | 1 | 0.08M | 0.07M | -10.2% | +0.0% |
| synth/spec-04.dfy | 3 | 0.08M | 0.08M | +1.0% | -0.0% |
| lit/dafny0/GeneralNewtypeCollections.dfy:pinned | 2 | 0.07M | 0.07M | -0.2% | -0.3% |
| lit/git-issues/git-issue-697b.dfy:legacy | 1 | 0.07M | 0.07M | -4.4% | +0.0% |
| lit/dafny0/GeneralNewtypeCollectionsGeneric.dfy:pinned | 2 | 0.07M | 0.07M | +0.8% | -0.0% |
| lit/git-issues/git-issue-697b.dfy:refresh | 1 | 0.07M | 0.07M | +3.4% | +2.2% |
| synth/chain-08.dfy | 1 | 0.07M | 0.22M | +215.9% | +31.3% |
| synth/spec-02.dfy | 3 | 0.07M | 0.07M | +0.5% | -0.0% |
| lit/dafny0/ISets.dfy:legacy | 1 | 0.07M | 0.07M | +0.4% | -2.3% |
| lit/dafny0/ISets.dfy:refresh | 1 | 0.07M | 0.07M | +0.4% | -2.3% |
| synth/spec-01.dfy | 3 | 0.06M | 0.06M | +0.5% | -0.1% |
| synth/ilookups-16.dfy | 1 | 0.06M | 0.08M | +29.3% | +0.0% |
| lit/git-issues/git-issue-1163.dfy:legacy | 1 | 0.06M | 0.06M | +0.2% | +0.0% |
| lit/git-issues/git-issue-1163.dfy:refresh | 1 | 0.06M | 0.06M | +0.2% | +0.0% |
| synth/lookups-16.dfy | 1 | 0.06M | 0.07M | +13.3% | +0.0% |
| lit/comp/Calls.dfy:legacy | 1 | 0.06M | 0.06M | -0.3% | +0.7% |
| lit/comp/firstSteps/6_Calls-VariableCapture.dfy:legacy | 1 | 0.06M | 0.06M | -0.3% | +0.7% |
| lit/comp/Calls.dfy:refresh | 1 | 0.06M | 0.06M | +1.1% | +0.0% |
| lit/comp/firstSteps/6_Calls-VariableCapture.dfy:refresh | 1 | 0.06M | 0.06M | +1.1% | +0.0% |
| synth/update-16.dfy | 1 | 0.05M | 0.05M | +5.3% | +0.0% |
| lit/dafny4/Regression19.dfy:legacy | 1 | 0.05M | 0.05M | +0.3% | +0.0% |
| lit/dafny4/Regression19.dfy:refresh | 1 | 0.05M | 0.05M | +0.3% | +0.0% |
| lit/git-issues/git-issue-1158.dfy:legacy | 1 | 0.04M | 0.04M | -2.3% | +0.0% |
| lit/git-issues/git-issue-1158.dfy:refresh | 1 | 0.04M | 0.04M | -2.3% | +0.0% |
| std/Parsers/Core/ParsersBuilders.dfy | 1 | 0.04M | 0.04M | +0.2% | +0.0% |
| lit/dafny4/Bug58.dfy:legacy | 3 | 0.04M | 0.04M | +0.9% | +0.0% |
| lit/dafny4/Bug58.dfy:refresh | 3 | 0.04M | 0.04M | +0.9% | +0.0% |
| lit/dafny0/DiscoverBounds.dfy:legacy | 1 | 0.03M | 0.03M | -1.4% | -1.7% |
| lit/dafny0/DiscoverBounds.dfy:refresh | 1 | 0.03M | 0.03M | -1.4% | -1.7% |
| synth/ichain-04.dfy | 1 | 0.03M | 0.07M | +93.8% | +2.0% |
| synth/lookups-08.dfy | 1 | 0.03M | 0.04M | +19.1% | +0.0% |
| synth/ilookups-08.dfy | 1 | 0.03M | 0.03M | -0.0% | +0.0% |
| synth/equal-02.dfy | 1 | 0.03M | 0.03M | -4.5% | +0.0% |
| synth/update-08.dfy | 1 | 0.03M | 0.03M | +4.5% | +0.0% |
| synth/chain-04.dfy | 1 | 0.03M | 0.07M | +129.5% | +3.3% |
| lit/dafny4/git-issue75.dfy:legacy | 2 | 0.03M | 0.03M | +0.6% | +0.0% |
| lit/dafny4/git-issue75.dfy:refresh | 2 | 0.03M | 0.03M | +0.6% | +0.0% |
| lit/comp/CovariantCollections.dfy:pinned | 1 | 0.03M | 0.03M | +0.3% | +0.0% |
| synth/update-04.dfy | 1 | 0.02M | 0.02M | +3.2% | +0.0% |
| synth/ilookups-04.dfy | 1 | 0.02M | 0.03M | +31.4% | +0.0% |
| synth/lookups-04.dfy | 1 | 0.02M | 0.03M | +23.6% | +0.0% |
| lit/dafny0/GeneralNewtypeMemberCompile.dfy:pinned | 1 | 0.02M | 0.02M | +0.4% | +0.0% |
| synth/update-02.dfy | 1 | 0.02M | 0.02M | +2.0% | +0.0% |
| synth/ichain-02.dfy | 1 | 0.02M | 0.03M | +62.8% | +3.4% |
| synth/update-01.dfy | 1 | 0.02M | 0.02M | +1.3% | +0.0% |
| lit/git-issues/git-issue-3320.dfy:legacy | 1 | 0.02M | 0.02M | +0.4% | +0.0% |
| lit/git-issues/git-issue-3320.dfy:refresh | 1 | 0.02M | 0.02M | +0.4% | +0.0% |
| synth/ilookups-02.dfy | 1 | 0.02M | 0.02M | +13.8% | +0.0% |
| lit/dafny0/TypeAdjustments.dfy:pinned | 1 | 0.02M | 0.02M | +0.5% | +0.0% |
| synth/chain-02.dfy | 1 | 0.02M | 0.03M | +77.8% | +2.5% |
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
| equal | 0.02 / 0.02 / 0.02 | 0.03 / 0.03 / 0.03 | 0.08 / 0.07 / 0.08 | 0.28 / 0.29 / 0.28 | 1.16 / 1.69 / 1.20 |
| ichain | 0.02 / 0.02 / 0.02 | 0.02 / 0.03 / 0.02 | 0.03 / 0.07 / 0.03 | 0.10 / 0.25 / 0.10 | 0.59 / 1.55 / 0.56 |
| ilookups | 0.02 / 0.02 / 0.02 | 0.02 / 0.02 / 0.02 | 0.02 / 0.03 / 0.02 | 0.03 / 0.03 / 0.03 | 0.06 / 0.08 / 0.06 |
| keyed | 1.53 / 1.50 / 1.53 | 6.27 / 4.98 / 5.07 | 9.79 / 13.00 / 9.79 | 10.70 / 12.35 / 11.07 | 9.05 / 13.81 / 10.58 |
| lookups | 0.02 / 0.02 / 0.02 | 0.02 / 0.02 / 0.02 | 0.02 / 0.03 / 0.02 | 0.03 / 0.04 / 0.03 | 0.06 / 0.07 / 0.06 |
| spec | 0.08 / 0.08 / 0.08 | 0.08 / 0.08 / 0.08 | 0.09 / 0.09 / 0.09 | 0.11 / 0.11 / 0.11 | 0.16 / 0.16 / 0.16 |
| update | 0.02 / 0.02 / 0.02 | 0.02 / 0.02 / 0.02 | 0.02 / 0.02 / 0.02 | 0.03 / 0.03 / 0.03 | 0.05 / 0.05 / 0.05 |

## dafny4/UnionFind.dfy as on master (Main not isolated): Main's cost per seed

| resolver | prelude | seed 0 | seed 1 | seed 2 | seed 3 | seed 4 | over 50M |
|---|---|---:|---:|---:|---:|---:|---:|
| legacy | master | 50.3M | 24.5M | 34.9M | 16.6M | 47.6M | 1 |
| legacy | pr | 23.0M | 16.6M | 61.6M | 11.9M | 62.5M | 2 |
| legacy | placebo | 38.2M | 18.9M | 34.9M | 15.4M | 27.2M | 0 |
| legacy | domguard | 23.1M | 20.4M | 48.5M | 20.8M | 42.3M | 0 |
| refresh | master | 68.3M | 12.6M | 26.9M | 18.6M | 38.6M | 1 |
| refresh | pr | 15.2M | 8.9M | 27.5M | 50.8M | 26.6M | 1 |
| refresh | placebo | 86.7M | 10.6M | 46.4M | 19.5M | 46.9M | 1 |
| refresh | domguard | 18.8M | 14.1M | 21.8M | 32.6M | 35.2M | 0 |

## Alternative sound encodings, over the same proofs

restrict: elements defined everywhere, `$ArbitraryBoxValue` outside the domain. domguard: the PR's axiom guarded by `Map#Domain(Map#Glue(a, b, t))`. eager: the PR's axiom plus the trigger `{ Map#Glue(a, b, t), Set#IsMember(a, bx) }`.

| encoding | VCs | total vs master | geomean vs master | total vs PR | geomean vs PR | verdict flips vs master at limit |
|---|---:|---|---|---|---|---:|
| pr | 841 | +13.0% [-3.9%, +37.2%] | +1.9% [+0.6%, +3.3%] | +0.0%  | +0.0%  | 2 |
| domguard | 841 | +7.3% [-4.4%, +21.2%] | +0.9% [+0.1%, +1.8%] | -5.1% [-14.9%, +5.7%] | -0.9% [-2.0%, -0.1%] | 3 |

domguard: largest differences from the PR

| job | VC | master | PR | domguard |
|---|---|---:|---:|---:|
| lit/dafny4/UnionFind.dfy:legacy | M3.UnionFind.Join (correctness) (assertion batch 124) | 4.61M | 18.64M | 9.69M |
| lit/dafny4/UnionFind.dfy:refresh | M2.UnionFind.FindAux (correctness) | 17.66M | 13.77M | 19.40M |
| lit/dafny4/UnionFind.dfy:refresh | M3.UnionFind.Join (correctness) (assertion batch 128) | 2.05M | 3.94M | 8.09M |
| lit/dafny0/Maps.dfy:legacy | GeneralMaps4 (correctness) | 0.17M | 2.96M | 0.18M |
| lit/dafny0/Maps.dfy:refresh | GeneralMaps4 (correctness) | 0.17M | 2.96M | 0.18M |
| lit/VSI-Benchmarks/b4.dfy:legacy | Map.RemoveNonFirst (correctness) | 10.34M | 13.35M | 10.71M |

Synthetic programs at N=16 (total RU, mean over seeds):

| family | master | pr | domguard |
|---|---:|---:|---:|
| chain | 0.32M | 2.30M | 0.33M |
| equal | 1.16M | 1.69M | 1.64M |
| ichain | 0.59M | 1.55M | 0.60M |
| ilookups | 0.06M | 0.08M | 0.07M |
| keyed | 9.05M | 13.81M | 12.16M |
| lookups | 0.06M | 0.07M | 0.07M |
| spec | 0.16M | 0.16M | 0.17M |
| update | 0.05M | 0.05M | 0.05M |
