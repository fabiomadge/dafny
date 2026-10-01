# Map#Glue prelude A/B benchmark

Seeds per (VC, prelude): 5 (0, 1, 2, 3, 4; 0 is Dafny's default). VCs: 1875 in 132 jobs; **930 affected** (master and PR counts differ), 945 unaffected (identical counts under master and PR for every seed).
Unaffected VCs whose counts differ under the placebo: 3.

## Proof cost over affected VCs that pass everywhere

Totals are sums of per-VC means over seeds; brackets are 95% bootstrap intervals over VCs.

| group | VCs | master RU | PR RU | PR vs master | geomean PR/master | placebo vs master | placebo geomean |
|---|---:|---:|---:|---|---|---|---|
| lit + std | 844 | 203.7M | 239.8M | +17.8% [-2.1%, +49.4%] | +2.0% [+0.8%, +3.4%] | +0.5% [-2.4%, +3.3%] | +0.0% [-0.2%, +0.2%] |
| lit | 833 | 203.3M | 239.5M | +17.8% [-1.7%, +48.6%] | +2.0% [+0.8%, +3.4%] | +0.5% [-2.7%, +3.5%] | +0.0% [-0.2%, +0.2%] |
| std | 11 | 0.3M | 0.3M | +0.7% [-0.1%, +1.5%] | +0.8% [-0.0%, +1.8%] | +0.0% [-0.0%, +0.0%] | -0.0% [-0.0%, +0.0%] |
| synth | 50 | 50.5M | 112.0M | +121.6% [+13.1%, +370.0%] | +26.1% [+12.8%, +44.2%] | -1.5% [-22.1%, +5.6%] | +0.5% [-2.0%, +2.6%] |

36 affected VCs fail (a verification error) in some run; their cost is the solver's search for a counterexample, reported separately:

| job | VC | master mean (min..max) | PR mean (min..max) | placebo mean |
|---|---|---|---|---|
| lit/git-issues/git-issue-3855.dfy:pinned | Memory.dynMove (correctness) | 185.56M (55.83..339.27) | 226.07M (72.95..295.59) | 193.73M |
| lit/git-issues/git-issue-3855.dfy:pinned | Memory.dynCopy (correctness) | 3.75M (2.35..4.98) | 4.14M (2.51..5.66) | 3.79M |
| lit/git-issues/git-issue-3855.dfy:pinned | Main1 (correctness) | 3.25M (2.85..3.59) | 3.25M (2.70..3.90) | 3.31M |
| lit/dafny0/TypeAdjustments.dfy:pinned | Comprehensions.Maps1 (correctness) | 0.61M (0.48..0.73) | 0.67M (0.48..0.93) | 0.61M |
| lit/dafny0/IMaps.dfy:legacy | m4 (correctness) | 0.04M (0.02..0.08) | 0.04M (0.02..0.08) | 0.04M |
| lit/dafny0/IMaps.dfy:refresh | m4 (correctness) | 0.04M (0.02..0.08) | 0.04M (0.02..0.08) | 0.04M |
| lit/dafny0/Maps.dfy:legacy | GeneralMaps5 (correctness) | 0.04M (0.04..0.04) | 0.04M (0.04..0.04) | 0.04M |
| lit/dafny0/Maps.dfy:refresh | GeneralMaps5 (correctness) | 0.04M (0.04..0.04) | 0.04M (0.04..0.04) | 0.04M |
| lit/git-issues/git-issue-851.dfy:legacy | OtherBindersInStatements.MapComprehension3 (correctness) | 0.03M (0.03..0.05) | 0.03M (0.03..0.05) | 0.03M |
| lit/git-issues/git-issue-851.dfy:refresh | OtherBindersInStatements.MapComprehension3 (correctness) | 0.03M (0.03..0.05) | 0.03M (0.03..0.05) | 0.03M |

## Total proof RU per seed (affected VCs that pass everywhere)

| prelude | seed 0 | seed 1 | seed 2 | seed 3 | seed 4 | mean | sd |
|---|---:|---:|---:|---:|---:|---:|---:|
| master | 249.3M | 224.8M | 240.7M | 273.3M | 282.9M | 254.2M | 21.3M |
| pr | 294.8M | 293.8M | 345.6M | 303.4M | 521.6M | 351.9M | 87.0M |
| placebo | 253.4M | 225.1M | 244.5M | 271.0M | 278.3M | 254.4M | 19.0M |

## Solver time over those proofs (sum of per-VC means, seconds)

| group | master | PR | placebo |
|---|---:|---:|---:|
| all | 136.7 | 157.8 | 134.8 |
| lit | 129.6 | 149.0 | 127.7 |
| std | 0.3 | 0.3 | 0.4 |
| synth | 6.7 | 8.4 | 6.8 |

## Distribution of per-VC cost ratios over those proofs (mean over seeds)

| ratio bucket | PR/master | placebo/master |
|---|---:|---:|
| < 0.5x | 1 | 0 |
| 0.5-0.8x | 11 | 2 |
| 0.8-0.95x | 26 | 16 |
| 0.95-1.05x | 771 | 858 |
| 1.05-1.25x | 47 | 15 |
| 1.25-2x | 22 | 3 |
| 2-4x | 10 | 0 |
| >= 4x | 6 | 0 |

## Verdict changes at each job's limit (seeds passing out of 5)

| job | VC | limit | master ok | PR ok | placebo ok | master RU | PR RU |
|---|---|---:|---:|---:|---:|---:|---:|
| lit/git-issues/git-issue-6535.dfy:legacy | Bad (correctness) | 50M | 5 | 0 | 5 | 0.03M | 0.03M |
| lit/git-issues/git-issue-6535.dfy:refresh | Bad (correctness) | 50M | 5 | 0 | 5 | 0.03M | 0.03M |
| synth/keyed-16.dfy | Keyed (correctness) | 50M | 5 | 3 | 5 | 10.67M | 64.00M |

## Largest changes among those proofs (by |PR - master| mean RU)

| job | VC | master | PR | PR/master | placebo | min..max master | min..max PR |
|---|---|---:|---:|---:|---:|---|---|
| synth/keyed-16.dfy | Keyed (correctness) | 10.67M | 64.00M | 6.00 | 11.39M | 5.92..22.45M | 8.01..239.98M |
| lit/dafny4/UnionFind.dfy:legacy | M3.UnionFind.Join (correctness) (assertion batch 124) | 5.79M | 30.97M | 5.35 | 4.88M | 1.85..15.67M | 19.87..40.30M |
| lit/dafny4/UnionFind.dfy:legacy | M3.UnionFind.Join (correctness) (assertion batch 47) | 3.21M | 13.37M | 4.17 | 3.35M | 1.83..4.64M | 2.62..32.47M |
| synth/keyed-08.dfy | Keyed (correctness) | 22.55M | 25.74M | 1.14 | 23.62M | 9.25..48.85M | 7.61..35.23M |
| lit/dafny0/Maps.dfy:legacy | GeneralMaps4 (correctness) | 0.17M | 2.96M | 17.49 | 0.17M | 0.17..0.17M | 2.96..2.96M |
| lit/dafny0/Maps.dfy:refresh | GeneralMaps4 (correctness) | 0.17M | 2.96M | 17.49 | 0.17M | 0.17..0.17M | 2.96..2.96M |
| lit/dafny4/UnionFind.dfy:refresh | M2.UnionFind.FindAux (correctness) | 16.42M | 14.28M | 0.87 | 18.37M | 12.65..22.31M | 4.86..20.94M |
| synth/chain-16.dfy | Chain (correctness) | 0.32M | 2.30M | 7.18 | 0.39M | 0.32..0.32M | 2.30..2.30M |
| lit/dafny4/UnionFind.dfy:refresh | M1.UnionFind.New (correctness) | 4.82M | 2.90M | 0.60 | 4.40M | 2.60..11.31M | 2.41..3.44M |
| lit/dafny4/UnionFind.dfy:refresh | M3.UnionFind.Join (correctness) (assertion batch 128) | 1.56M | 3.05M | 1.96 | 1.58M | 1.17..1.95M | 0.98..5.85M |
| lit/dafny4/UnionFind.dfy:refresh | M3.UnionFind.Join (correctness) (assertion batch 148) | 3.53M | 4.72M | 1.34 | 4.20M | 2.71..4.27M | 2.71..6.17M |
| synth/keyed-04.dfy | Keyed (correctness) | 7.02M | 8.19M | 1.17 | 4.38M | 3.75..18.50M | 5.08..20.46M |
| lit/dafny4/UnionFind.dfy:legacy | M1.UnionFind.New (correctness) | 4.34M | 3.30M | 0.76 | 3.32M | 2.74..6.07M | 2.48..5.04M |
| lit/VSI-Benchmarks/b4.dfy:legacy | Map.RemoveNonFirst (correctness) | 12.28M | 11.25M | 0.92 | 11.64M | 11.18..14.98M | 8.64..12.67M |
| lit/dafny4/UnionFind.dfy:legacy | M2.UnionFind.FindAux (correctness) | 13.77M | 12.76M | 0.93 | 15.03M | 10.55..16.24M | 9.84..17.17M |
| synth/ichain-16.dfy | Chain (correctness) | 0.59M | 1.55M | 2.61 | 0.56M | 0.59..0.59M | 1.38..2.08M |
| lit/dafny4/UnionFind.dfy:refresh | M1.UnionFind.Union (correctness) | 2.00M | 1.13M | 0.56 | 1.61M | 1.01..5.22M | 0.99..1.45M |
| lit/dafny4/UnionFind.dfy:legacy | M3.UnionFind.Join (correctness) (assertion batch 143) | 2.36M | 1.49M | 0.63 | 3.32M | 1.83..2.75M | 1.39..1.76M |
| lit/dafny4/UnionFind.dfy:refresh | M3.UnionFind.Join (correctness) (assertion batch 111) | 0.71M | 1.53M | 2.16 | 0.81M | 0.51..0.98M | 0.41..2.38M |
| lit/dafny4/UnionFind.dfy:refresh | M3.UnionFind.Join (correctness) (assertion batch 166) | 0.91M | 1.64M | 1.80 | 0.81M | 0.59..1.02M | 0.43..2.35M |
| lit/VSI-Benchmarks/b4.dfy:refresh | Map.RemoveNonFirst (correctness) | 13.09M | 12.42M | 0.95 | 12.48M | 11.18..17.97M | 10.03..16.11M |
| lit/dafny4/UnionFind.dfy:legacy | M3.UnionFind.Join (correctness) (assertion batch 63) | 0.46M | 1.02M | 2.21 | 0.46M | 0.36..0.62M | 0.78..1.36M |
| lit/dafny4/UnionFind.dfy:refresh | M3.UnionFind.Join (correctness) (assertion batch 113) | 0.89M | 0.41M | 0.46 | 0.99M | 0.28..1.26M | 0.27..0.99M |
| synth/equal-16.dfy | Equal (correctness) | 1.26M | 1.69M | 1.34 | 1.26M | 1.18..1.36M | 1.64..1.72M |
| lit/dafny4/UnionFind.dfy:legacy | M3.UnionFind.Join (correctness) (assertion batch 109) | 1.44M | 1.82M | 1.27 | 1.42M | 1.27..1.63M | 0.93..2.16M |

## Per job (proofs among the affected VCs)

| job | VCs | master | PR | PR vs master | placebo vs master |
|---|---:|---:|---:|---:|---:|
| lit/dafny4/UnionFind.dfy:refresh | 294 | 69.42M | 67.59M | -2.6% | +2.9% |
| lit/dafny4/UnionFind.dfy:legacy | 287 | 69.20M | 102.21M | +47.7% | +0.1% |
| synth/keyed-08.dfy | 1 | 22.55M | 25.74M | +14.1% | +4.7% |
| lit/VSI-Benchmarks/b4.dfy:refresh | 14 | 14.80M | 14.35M | -3.0% | -4.2% |
| lit/VSI-Benchmarks/b4.dfy:legacy | 14 | 13.99M | 13.16M | -6.0% | -4.5% |
| lit/git-issues/git-issue-3855.dfy:pinned | 59 | 10.97M | 10.99M | +0.2% | +0.5% |
| synth/keyed-16.dfy | 1 | 10.67M | 64.00M | +499.8% | +6.8% |
| synth/keyed-04.dfy | 1 | 7.02M | 8.19M | +16.8% | -37.5% |
| lit/comp/rust/loops.dfy:legacy | 4 | 5.51M | 5.72M | +3.8% | +0.8% |
| lit/comp/rust/loops.dfy:refresh | 4 | 5.51M | 5.72M | +3.8% | +0.8% |
| synth/keyed-02.dfy | 1 | 5.04M | 5.00M | -0.8% | +0.1% |
| lit/cloudmake/CloudMake-ParallelBuilds.dfy:legacy | 19 | 2.85M | 3.01M | +5.5% | -0.2% |
| lit/cloudmake/CloudMake-ParallelBuilds.dfy:refresh | 19 | 2.85M | 3.01M | +5.5% | -0.2% |
| synth/keyed-01.dfy | 1 | 1.49M | 1.47M | -1.7% | +0.0% |
| synth/equal-16.dfy | 1 | 1.26M | 1.69M | +34.5% | +0.1% |
| lit/dafny0/IMaps.dfy:refresh | 7 | 1.09M | 1.14M | +4.0% | +0.0% |
| lit/dafny0/IMaps.dfy:legacy | 7 | 1.09M | 1.14M | +4.0% | +0.0% |
| lit/comp/rust/operators.dfy:refresh | 5 | 1.05M | 1.04M | -1.0% | +2.4% |
| lit/comp/rust/operators.dfy:legacy | 4 | 0.91M | 0.90M | -1.1% | +2.7% |
| lit/dafny0/Maps.dfy:refresh | 13 | 0.62M | 3.40M | +447.1% | +0.8% |
| lit/dafny0/Maps.dfy:legacy | 13 | 0.62M | 3.40M | +447.6% | +0.8% |
| synth/ichain-16.dfy | 1 | 0.59M | 1.55M | +161.4% | -5.6% |
| synth/chain-16.dfy | 1 | 0.32M | 2.30M | +618.0% | +23.1% |
| synth/equal-08.dfy | 1 | 0.27M | 0.29M | +8.0% | +5.7% |
| lit/comp/Comprehensions.dfy:legacy | 4 | 0.24M | 0.24M | -0.5% | +0.7% |
| lit/comp/Comprehensions.dfy:refresh | 4 | 0.22M | 0.22M | -0.1% | +1.5% |
| lit/comp/ComprehensionsNewSyntax.dfy:legacy | 3 | 0.21M | 0.21M | -0.0% | +0.9% |
| lit/comp/ComprehensionsNewSyntax.dfy:refresh | 3 | 0.19M | 0.19M | +0.6% | +1.9% |
| std/Collections/Map.dfy | 5 | 0.16M | 0.16M | +0.3% | +0.0% |
| lit/dafny4/git-issue167.dfy:refresh | 2 | 0.15M | 0.10M | -28.0% | +0.0% |
| synth/spec-16.dfy | 3 | 0.14M | 0.15M | +4.0% | +0.0% |
| lit/dafny4/git-issue167.dfy:legacy | 2 | 0.14M | 0.10M | -26.3% | +0.0% |
| lit/dafny4/KozenSilva.dfy:legacy | 3 | 0.13M | 0.13M | -0.3% | -0.0% |
| lit/dafny4/KozenSilva.dfy:refresh | 3 | 0.13M | 0.13M | -0.3% | -0.0% |
| std/Collections/Imap.dfy | 5 | 0.13M | 0.13M | +1.3% | -0.0% |
| synth/ichain-08.dfy | 1 | 0.10M | 0.25M | +150.9% | -2.5% |
| synth/spec-08.dfy | 3 | 0.10M | 0.10M | +1.9% | +0.0% |
| synth/equal-04.dfy | 1 | 0.08M | 0.07M | -10.1% | +0.0% |
| synth/spec-04.dfy | 3 | 0.08M | 0.08M | +0.8% | +0.0% |
| lit/dafny0/GeneralNewtypeCollections.dfy:pinned | 2 | 0.07M | 0.07M | -1.4% | -1.9% |
| lit/git-issues/git-issue-697b.dfy:refresh | 1 | 0.07M | 0.07M | -0.5% | +0.0% |
| lit/dafny0/GeneralNewtypeCollectionsGeneric.dfy:pinned | 2 | 0.07M | 0.07M | -0.2% | +2.2% |
| lit/git-issues/git-issue-697b.dfy:legacy | 1 | 0.07M | 0.07M | -2.0% | +0.0% |
| synth/chain-08.dfy | 1 | 0.07M | 0.22M | +215.8% | +31.3% |
| synth/spec-02.dfy | 3 | 0.07M | 0.07M | +0.3% | +0.0% |
| lit/dafny0/ISets.dfy:legacy | 1 | 0.07M | 0.06M | -4.0% | -2.3% |
| lit/dafny0/ISets.dfy:refresh | 1 | 0.07M | 0.06M | -4.0% | -2.3% |
| synth/spec-01.dfy | 3 | 0.06M | 0.06M | +0.2% | +0.0% |
| lit/git-issues/git-issue-1163.dfy:legacy | 1 | 0.06M | 0.06M | +0.3% | -0.1% |
| lit/git-issues/git-issue-1163.dfy:refresh | 1 | 0.06M | 0.06M | +0.3% | -0.1% |
| synth/lookups-16.dfy | 1 | 0.06M | 0.07M | +13.3% | +0.0% |
| lit/comp/Calls.dfy:legacy | 1 | 0.06M | 0.06M | +0.4% | +0.0% |
| lit/comp/firstSteps/6_Calls-VariableCapture.dfy:legacy | 1 | 0.06M | 0.06M | +0.4% | +0.0% |
| lit/comp/Calls.dfy:refresh | 1 | 0.06M | 0.06M | +1.1% | +0.0% |
| lit/comp/firstSteps/6_Calls-VariableCapture.dfy:refresh | 1 | 0.06M | 0.06M | +1.1% | +0.0% |
| synth/ilookups-16.dfy | 1 | 0.06M | 0.06M | +10.0% | +2.5% |
| synth/update-16.dfy | 1 | 0.05M | 0.05M | +5.4% | +0.0% |
| lit/dafny4/Regression19.dfy:legacy | 1 | 0.05M | 0.05M | +0.3% | +0.0% |
| lit/dafny4/Regression19.dfy:refresh | 1 | 0.05M | 0.05M | +0.3% | +0.0% |
| lit/git-issues/git-issue-1158.dfy:legacy | 1 | 0.04M | 0.04M | -2.3% | +0.0% |
| lit/git-issues/git-issue-1158.dfy:refresh | 1 | 0.04M | 0.04M | -2.3% | +0.0% |
| std/Parsers/Core/ParsersBuilders.dfy | 1 | 0.04M | 0.04M | +0.2% | +0.0% |
| lit/dafny4/Bug58.dfy:legacy | 3 | 0.04M | 0.04M | +0.9% | +0.0% |
| lit/dafny4/Bug58.dfy:refresh | 3 | 0.04M | 0.04M | +0.9% | +0.0% |
| synth/ichain-04.dfy | 1 | 0.03M | 0.07M | +93.8% | +2.0% |
| lit/dafny0/DiscoverBounds.dfy:legacy | 1 | 0.03M | 0.03M | +0.3% | +0.0% |
| lit/dafny0/DiscoverBounds.dfy:refresh | 1 | 0.03M | 0.03M | +0.3% | +0.0% |
| synth/lookups-08.dfy | 1 | 0.03M | 0.04M | +19.2% | +0.0% |
| synth/ilookups-08.dfy | 1 | 0.03M | 0.03M | -0.0% | +0.0% |
| synth/equal-02.dfy | 1 | 0.03M | 0.03M | -4.5% | +0.0% |
| synth/update-08.dfy | 1 | 0.03M | 0.03M | +4.5% | +0.0% |
| synth/chain-04.dfy | 1 | 0.03M | 0.07M | +129.7% | +3.3% |
| lit/dafny4/git-issue75.dfy:legacy | 2 | 0.03M | 0.03M | +0.6% | +0.0% |
| lit/dafny4/git-issue75.dfy:refresh | 2 | 0.03M | 0.03M | +0.6% | +0.0% |
| lit/comp/CovariantCollections.dfy:pinned | 1 | 0.03M | 0.03M | +0.3% | +0.0% |
| synth/update-04.dfy | 1 | 0.02M | 0.02M | +3.2% | +0.0% |
| synth/ilookups-04.dfy | 1 | 0.02M | 0.03M | +31.8% | +0.0% |
| synth/lookups-04.dfy | 1 | 0.02M | 0.03M | +23.8% | +0.0% |
| lit/dafny0/GeneralNewtypeMemberCompile.dfy:pinned | 1 | 0.02M | 0.02M | +0.4% | +0.0% |
| synth/update-02.dfy | 1 | 0.02M | 0.02M | +2.0% | +0.0% |
| synth/ichain-02.dfy | 1 | 0.02M | 0.03M | +62.9% | +3.4% |
| synth/update-01.dfy | 1 | 0.02M | 0.02M | +1.3% | +0.0% |
| lit/git-issues/git-issue-3320.dfy:legacy | 1 | 0.02M | 0.02M | +0.5% | -0.0% |
| lit/git-issues/git-issue-3320.dfy:refresh | 1 | 0.02M | 0.02M | +0.5% | -0.0% |
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
| lit/dafny4/git-issue27.dfy:refresh | 1 | 0.01M | 0.01M | +0.7% | +0.0% |
| lit/dafny4/Bug108.dfy:legacy | 1 | 0.01M | 0.01M | +0.7% | +0.0% |
| lit/dafny4/Bug108.dfy:refresh | 1 | 0.01M | 0.01M | +0.7% | +0.0% |

## Synthetic programs: total RU by size N (master / PR / placebo, mean over seeds)

| family | N=1 | N=2 | N=4 | N=8 | N=16 |
|---|---|---|---|---|---|
| chain | 0.02 / 0.02 / 0.02 | 0.02 / 0.03 / 0.02 | 0.03 / 0.07 / 0.03 | 0.07 / 0.22 / 0.09 | 0.32 / 2.30 / 0.39 |
| equal | 0.02 / 0.02 / 0.02 | 0.03 / 0.03 / 0.03 | 0.08 / 0.07 / 0.08 | 0.27 / 0.29 / 0.28 | 1.26 / 1.69 / 1.26 |
| ichain | 0.02 / 0.02 / 0.02 | 0.02 / 0.03 / 0.02 | 0.03 / 0.07 / 0.03 | 0.10 / 0.25 / 0.10 | 0.59 / 1.55 / 0.56 |
| ilookups | 0.02 / 0.02 / 0.02 | 0.02 / 0.02 / 0.02 | 0.02 / 0.03 / 0.02 | 0.03 / 0.03 / 0.03 | 0.06 / 0.06 / 0.06 |
| keyed | 1.49 / 1.47 / 1.50 | 5.04 / 5.00 / 5.05 | 7.02 / 8.19 / 4.38 | 22.55 / 25.74 / 23.62 | 10.67 / 64.00 / 11.39 |
| lookups | 0.02 / 0.02 / 0.02 | 0.02 / 0.02 / 0.02 | 0.02 / 0.03 / 0.02 | 0.03 / 0.04 / 0.03 | 0.06 / 0.07 / 0.06 |
| spec | 0.08 / 0.08 / 0.08 | 0.08 / 0.08 / 0.08 | 0.09 / 0.09 / 0.09 | 0.11 / 0.11 / 0.11 | 0.16 / 0.16 / 0.16 |
| update | 0.02 / 0.02 / 0.02 | 0.02 / 0.02 / 0.02 | 0.02 / 0.02 / 0.02 | 0.03 / 0.03 / 0.03 | 0.05 / 0.05 / 0.05 |

## dafny4/UnionFind.dfy as on master (Main not isolated): Main's cost per seed

| resolver | prelude | seed 0 | seed 1 | seed 2 | seed 3 | seed 4 | over 50M |
|---|---|---:|---:|---:|---:|---:|---:|
| legacy | master | 20.7M | 17.0M | 67.6M | 11.8M | 29.3M | 1 |
| legacy | pr | 31.2M | 20.2M | 85.2M | 14.2M | 41.2M | 1 |
| legacy | placebo | 29.3M | 15.1M | 63.7M | 48.3M | 86.0M | 2 |
| legacy | domguard | 19.0M | 76.5M | 58.3M | 15.4M | 42.2M | 2 |
| legacy | eager | 45.8M | 46.6M | 52.9M | 17.4M | 35.7M | 1 |
| legacy | restrict | 13.4M | 25.3M | 18.6M | 10.1M | 27.2M | 0 |
| refresh | master | 21.1M | 20.7M | 30.9M | 13.8M | 23.8M | 0 |
| refresh | pr | 53.4M | 41.5M | 26.0M | 19.1M | 15.2M | 1 |
| refresh | placebo | 77.1M | 48.9M | 26.0M | 14.1M | 23.8M | 1 |
| refresh | domguard | 65.6M | 22.1M | 29.4M | 54.6M | 68.9M | 3 |
| refresh | eager | 72.7M | 31.1M | 63.4M | 23.2M | 13.9M | 2 |
| refresh | restrict | 27.4M | 14.1M | 25.0M | 21.8M | 15.9M | 0 |

## Alternative sound encodings, over the same proofs

restrict: elements defined everywhere, `$ArbitraryBoxValue` outside the domain. domguard: the PR's axiom guarded by `Map#Domain(Map#Glue(a, b, t))`. eager: the PR's axiom plus the trigger `{ Map#Glue(a, b, t), Set#IsMember(a, bx) }`.

| encoding | VCs | total vs master | geomean vs master | total vs PR | geomean vs PR | verdict flips vs master at limit |
|---|---:|---|---|---|---|---:|
| pr | 844 | +17.8% [-2.5%, +51.3%] | +2.0% [+0.8%, +3.4%] | +0.0%  | +0.0%  | 3 |
| domguard | 844 | +2.4% [-7.6%, +16.7%] | +0.8% [-0.1%, +1.8%] | -13.0% [-28.1%, -0.0%] | -1.1% [-2.3%, -0.2%] | 3 |
| eager | 844 | +16.1% [+0.8%, +35.4%] | +2.0% [+0.8%, +3.4%] | -1.4% [-10.8%, +7.1%] | +0.1% [-0.3%, +0.4%] | 3 |
| restrict | 844 | +12.3% [-3.1%, +28.3%] | +0.7% [-0.2%, +1.6%] | -4.6% [-22.3%, +17.0%] | -1.3% [-2.5%, -0.1%] | 2 |

domguard: largest differences from the PR

| job | VC | master | PR | domguard |
|---|---|---:|---:|---:|
| lit/dafny4/UnionFind.dfy:legacy | M3.UnionFind.Join (correctness) (assertion batch 124) | 5.79M | 30.97M | 8.86M |
| lit/dafny4/UnionFind.dfy:refresh | M3.UnionFind.Join (correctness) (assertion batch 128) | 1.56M | 3.05M | 6.23M |
| lit/dafny0/Maps.dfy:legacy | GeneralMaps4 (correctness) | 0.17M | 2.96M | 0.18M |
| lit/dafny0/Maps.dfy:refresh | GeneralMaps4 (correctness) | 0.17M | 2.96M | 0.18M |
| lit/dafny4/UnionFind.dfy:refresh | M2.UnionFind.FindAux (correctness) | 16.42M | 14.28M | 11.55M |
| lit/VSI-Benchmarks/b4.dfy:refresh | Map.RemoveNonFirst (correctness) | 13.09M | 12.42M | 10.60M |

eager: largest differences from the PR

| job | VC | master | PR | eager |
|---|---|---:|---:|---:|
| lit/dafny4/UnionFind.dfy:legacy | M3.UnionFind.Join (correctness) (assertion batch 124) | 5.79M | 30.97M | 19.78M |
| lit/dafny4/UnionFind.dfy:legacy | M2.UnionFind.FindAux (correctness) | 13.77M | 12.76M | 16.92M |
| lit/dafny4/UnionFind.dfy:refresh | M3.UnionFind.Join (correctness) (assertion batch 128) | 1.56M | 3.05M | 5.04M |
| lit/dafny4/UnionFind.dfy:refresh | M1.UnionFind.New (correctness) | 4.82M | 2.90M | 4.20M |
| lit/dafny4/UnionFind.dfy:refresh | M2.UnionFind.FindAux (correctness) | 16.42M | 14.28M | 15.01M |
| lit/dafny4/UnionFind.dfy:legacy | M3.UnionFind.Join (correctness) (assertion batch 47) | 3.21M | 13.37M | 12.80M |

restrict: largest differences from the PR

| job | VC | master | PR | restrict |
|---|---|---:|---:|---:|
| lit/dafny4/UnionFind.dfy:refresh | M2.UnionFind.FindAux (correctness) | 16.42M | 14.28M | 30.64M |
| lit/dafny4/UnionFind.dfy:legacy | M3.UnionFind.Join (correctness) (assertion batch 124) | 5.79M | 30.97M | 15.86M |
| lit/dafny4/UnionFind.dfy:legacy | M3.UnionFind.Join (correctness) (assertion batch 47) | 3.21M | 13.37M | 3.35M |
| lit/dafny4/UnionFind.dfy:legacy | M3.UnionFind.Join (correctness) (assertion batch 119) | 3.94M | 3.70M | 7.82M |
| lit/dafny0/Maps.dfy:legacy | GeneralMaps4 (correctness) | 0.17M | 2.96M | 0.23M |
| lit/dafny0/Maps.dfy:refresh | GeneralMaps4 (correctness) | 0.17M | 2.96M | 0.23M |

Synthetic programs at N=16 (total RU, mean over seeds):

| family | master | pr | domguard | eager | restrict |
|---|---:|---:|---:|---:|---:|
| chain | 0.32M | 2.30M | 0.33M | 2.30M | 0.33M |
| equal | 1.26M | 1.69M | 1.68M | 1.69M | 1.72M |
| ichain | 0.59M | 1.55M | 0.60M | 1.55M | 0.62M |
| ilookups | 0.06M | 0.06M | 0.06M | 0.06M | 0.06M |
| keyed | 10.67M | 64.00M | 54.40M | 64.00M | 11.88M |
| lookups | 0.06M | 0.07M | 0.07M | 0.07M | 0.06M |
| spec | 0.16M | 0.16M | 0.17M | 0.16M | 0.17M |
| update | 0.05M | 0.05M | 0.05M | 0.05M | 0.05M |
