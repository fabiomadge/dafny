# #6541 A/B benchmark (public corpora)

Seeds per (VC, prelude): 1 (1; 0 is Dafny's default). VCs: 27063 in 2077 jobs; **151 affected** (master and PR counts differ), 26912 unaffected (identical counts under master and PR for every seed).

## Proof cost over affected VCs that pass everywhere

Totals are sums of per-VC means over seeds. "Per program" averages each program's own VC geomean, so a
program with hundreds of VCs weighs no more than one with two. Brackets are 95% bootstrap intervals that
resample programs, not VCs.

| group | programs | VCs | largest program | total PR/master | geomean over VCs | per program |
|---|---:|---:|---|---|---|---|
| all but synth | 30 | 135 | lit/vstte2012/BreadthFirstSearch.dfy (49% of VCs) | -0.5% [-1.0%, +2.1%] | +0.7% [+0.2%, +1.8%] | +1.5% [+1.2%, +1.8%] |
| dafnybench | 1 | 2 | dafnybench/verification-class_tmp_tmpz9ik148s_2022_chapter05-distributed-state-machines_exercises_UtilitiesLibrary.dfy (100% of VCs) | -1.1% [-1.1%, -1.1%] | -1.1% [-1.1%, -1.1%] | -1.1% [-1.1%, -1.1%] |
| kondo | 19 | 38 | kondo/clientServer/manual (5% of VCs) | +2.3% [+2.3%, +2.3%] | +2.1% [+2.1%, +2.1%] | +2.1% [+2.1%, +2.1%] |
| libraries | 1 | 1 | libraries/dafny/Collections/Seqs.dfy (100% of VCs) | +0.4% [+0.4%, +0.4%] | +0.4% [+0.4%, +0.4%] | +0.4% [+0.4%, +0.4%] |
| lit | 7 | 91 | lit/vstte2012/BreadthFirstSearch.dfy (73% of VCs) | -0.8% [-1.1%, +2.8%] | +0.2% [-0.0%, +1.6%] | +0.8% [+0.2%, +1.7%] |
| std | 2 | 3 | std/Parsers/Core/ParsersTheorems.dfy (67% of VCs) | +0.4% [-0.0%, +1.6%] | +0.8% [-0.0%, +1.3%] | +0.6% [-0.0%, +1.3%] |

16 affected VCs fail (a verification error) in some run; their cost is the solver's search for a counterexample, reported separately:

| job | VC | master mean (min..max) | PR mean (min..max) |
|---|---|---|---|
| lit/comp/TypeParams.dfy:refresh | Standard (correctness) | 832.98M (832.98..832.98) | 803.84M (803.84..803.84) |
| lit/dafny0/FunctionSpecifications.dfy:refresh | GoodPost (well-formedness) | 311.14M (311.14..311.14) | 311.01M (311.01..311.01) |
| lit/cli/defaultTimeLimit.dfy:refresh | Foo (correctness) | 298.84M (298.84..298.84) | 282.62M (282.62..282.62) |
| kondo/paxos/sync | PaxosProof.InvNextLearnerReceivedAcceptImpliesAccepted (correctness) | 293.81M (293.81..293.81) | 303.15M (303.15..303.15) |
| libraries/dafny/Collections/Seqs.dfy | Dafny.Collections.Seq.LemmaMapDistributesOverConcat (correctness) | 243.34M (243.34..243.34) | 282.91M (282.91..282.91) |
| dafnybench/dafny_experiments_tmp_tmpz29_3_3i_circuit.dfy | CombineCircuits.CombineCircuitsCorrect (correctness) | 214.71M (214.71..214.71) | 218.16M (218.16..218.16) |
| libraries/dafny/Collections/Seqs.dfy | Dafny.Collections.Seq.LemmaFilterDistributesOverConcat (correctness) (assertion batch 2) | 171.40M (171.40..171.40) | 178.95M (178.95..178.95) |
| lit/dafny1/Rippling.legacy.dfy:refresh | P2 (correctness) | 22.88M (22.88..22.88) | 20.01M (20.01..20.01) |
| lit/hofs/Folding.legacy.dfy:refresh | FoldL_Use_Direct (correctness) | 21.23M (21.23..21.23) | 21.23M (21.23..21.23) |
| lit/vstte2012/RingBufferAuto.dfy:refresh | RingBuffer.ResizingEnqueue (correctness) | 8.76M (8.76..8.76) | 8.78M (8.78..8.78) |

## Total proof RU per seed (affected VCs that pass everywhere)

| prelude | seed 1 | mean | sd |
|---|---:|---:|---:|
| master | 11.2M | 11.2M | 0.0M |
| pr | 11.2M | 11.2M | 0.0M |

## Solver time over those proofs (sum of per-VC means, seconds)

| group | master | PR |
|---|---:|---:|
| all | 8.2 | 7.7 |
| lit | 6.9 | 6.5 |
| std | 0.4 | 0.4 |

## Distribution of per-VC cost ratios over those proofs (mean over seeds)

| ratio bucket | PR/master |
|---|---:|
| < 0.5x | 0 |
| 0.5-0.8x | 2 |
| 0.8-0.95x | 6 |
| 0.95-1.05x | 120 |
| 1.05-1.25x | 6 |
| 1.25-2x | 1 |
| 2-4x | 0 |
| >= 4x | 0 |

## Verdict changes at each job's limit (seeds passing out of 1)

| job | VC | limit | master ok | PR ok | master RU | PR RU |
|---|---|---:|---:|---:|---:|---:|
| (none) | | | | | | |

## Largest changes among those proofs (by |PR - master| mean RU)

| job | VC | master | PR | PR/master | min..max master | min..max PR |
|---|---|---:|---:|---:|---|---|
| lit/vstte2012/BreadthFirstSearch.dfy:refresh | BreadthFirstSearch.BFS (correctness) (assertion batch 47) | 0.15M | 0.22M | 1.48 | 0.15..0.15M | 0.22..0.22M |
| lit/vstte2012/BreadthFirstSearch.dfy:refresh | BreadthFirstSearch.BFS (correctness) (assertion batch 71) | 0.45M | 0.52M | 1.15 | 0.45..0.45M | 0.52..0.52M |
| lit/vstte2012/BreadthFirstSearch.dfy:refresh | BreadthFirstSearch.BFS (correctness) (assertion batch 57) | 0.32M | 0.25M | 0.78 | 0.32..0.32M | 0.25..0.25M |
| lit/vstte2012/BreadthFirstSearch.dfy:refresh | BreadthFirstSearch.BFS (correctness) (assertion batch 85) | 0.69M | 0.63M | 0.91 | 0.69..0.69M | 0.63..0.63M |
| lit/vstte2012/BreadthFirstSearch.dfy:refresh | BreadthFirstSearch.BFS (correctness) (assertion batch 45) | 0.22M | 0.17M | 0.77 | 0.22..0.22M | 0.17..0.17M |
| lit/vstte2012/BreadthFirstSearch.dfy:refresh | BreadthFirstSearch.BFS (correctness) (assertion batch 61) | 0.62M | 0.58M | 0.94 | 0.62..0.62M | 0.58..0.58M |
| lit/vstte2012/BreadthFirstSearch.dfy:refresh | BreadthFirstSearch.BFS (correctness) (assertion batch 67) | 0.19M | 0.15M | 0.81 | 0.19..0.19M | 0.15..0.15M |
| lit/vstte2012/BreadthFirstSearch.dfy:refresh | BreadthFirstSearch.BFS (correctness) (assertion batch 81) | 0.15M | 0.12M | 0.83 | 0.15..0.15M | 0.12..0.12M |
| lit/vstte2012/BreadthFirstSearch.dfy:refresh | BreadthFirstSearch.BFS (correctness) (assertion batch 38) | 0.09M | 0.11M | 1.20 | 0.09..0.09M | 0.11..0.11M |
| lit/vstte2012/BreadthFirstSearch.dfy:refresh | BreadthFirstSearch.BFS (correctness) (assertion batch 60) | 0.16M | 0.15M | 0.91 | 0.16..0.16M | 0.15..0.15M |
| lit/vstte2012/BreadthFirstSearch.dfy:refresh | BreadthFirstSearch.BFS (correctness) (assertion batch 51) | 0.16M | 0.17M | 1.07 | 0.16..0.16M | 0.17..0.17M |
| lit/vstte2012/BreadthFirstSearch.dfy:refresh | BreadthFirstSearch.BFS (correctness) (assertion batch 48) | 0.15M | 0.14M | 0.92 | 0.15..0.15M | 0.14..0.14M |
| lit/dafny0/Maps.dfy:refresh | m14 (correctness) | 0.13M | 0.14M | 1.08 | 0.13..0.13M | 0.14..0.14M |
| lit/vstte2012/BreadthFirstSearch.dfy:refresh | BreadthFirstSearch.BFS (correctness) (assertion batch 59) | 0.12M | 0.13M | 1.07 | 0.12..0.12M | 0.13..0.13M |
| lit/vstte2012/BreadthFirstSearch.dfy:refresh | BreadthFirstSearch.BFS (correctness) (assertion batch 50) | 0.36M | 0.36M | 0.98 | 0.36..0.36M | 0.36..0.36M |
| lit/vstte2012/BreadthFirstSearch.dfy:refresh | BreadthFirstSearch.BFS (correctness) (assertion batch 58) | 0.16M | 0.17M | 1.03 | 0.16..0.16M | 0.17..0.17M |
| lit/vstte2012/BreadthFirstSearch.dfy:refresh | BreadthFirstSearch.BFS (correctness) (assertion batch 84) | 0.08M | 0.08M | 1.07 | 0.08..0.08M | 0.08..0.08M |
| lit/vstte2012/BreadthFirstSearch.dfy:refresh | BreadthFirstSearch.BFS (correctness) (assertion batch 42) | 0.19M | 0.20M | 1.03 | 0.19..0.19M | 0.20..0.20M |
| lit/vstte2012/BreadthFirstSearch.dfy:refresh | BreadthFirstSearch.BFS (correctness) (assertion batch 34) | 0.12M | 0.12M | 1.04 | 0.12..0.12M | 0.12..0.12M |
| lit/vstte2012/BreadthFirstSearch.dfy:refresh | BreadthFirstSearch.BFS (correctness) (assertion batch 82) | 0.09M | 0.10M | 1.04 | 0.09..0.09M | 0.10..0.10M |
| lit/vstte2012/BreadthFirstSearch.dfy:refresh | BreadthFirstSearch.BFS (correctness) (assertion batch 55) | 0.13M | 0.13M | 1.03 | 0.13..0.13M | 0.13..0.13M |
| lit/vstte2012/BreadthFirstSearch.dfy:refresh | BreadthFirstSearch.BFS (correctness) (assertion batch 33) | 0.09M | 0.10M | 1.04 | 0.09..0.09M | 0.10..0.10M |
| lit/vstte2012/BreadthFirstSearch.dfy:refresh | BreadthFirstSearch.BFS (correctness) (assertion batch 79) | 0.09M | 0.09M | 1.04 | 0.09..0.09M | 0.09..0.09M |
| std/Parsers/Core/ParsersTheorems.dfy | Std.Parsers.Theorems.AboutConcatBindSucceeds (correctness) | 0.07M | 0.08M | 1.04 | 0.07..0.07M | 0.08..0.08M |
| lit/vstte2012/BreadthFirstSearch.dfy:refresh | BreadthFirstSearch.BFS (correctness) (assertion batch 56) | 0.39M | 0.39M | 1.01 | 0.39..0.39M | 0.39..0.39M |

## Per job (proofs among the affected VCs)

| job | VCs | master | PR | PR vs master |
|---|---:|---:|---:|---:|
| lit/vstte2012/BreadthFirstSearch.dfy:refresh | 66 | 8.41M | 8.31M | -1.1% |
| lit/hofs/TreeMapSimple.dfy:refresh | 5 | 0.41M | 0.41M | +0.6% |
| lit/autoRevealDependencies/tree-map-simple.dfy:refresh | 5 | 0.40M | 0.41M | +0.9% |
| std/Actions/Producers.dfy | 1 | 0.34M | 0.34M | -0.0% |
| lit/dafny4/ExpandedGuardedness.dfy:refresh | 6 | 0.28M | 0.28M | +0.3% |
| lit/dafny0/Maps.dfy:refresh | 4 | 0.22M | 0.23M | +5.8% |
| std/Parsers/Core/ParsersTheorems.dfy | 2 | 0.14M | 0.14M | +1.6% |
| libraries/dafny/Collections/Seqs.dfy | 1 | 0.12M | 0.12M | +0.4% |
| lit/dafny4/Bug151.dfy:refresh | 4 | 0.07M | 0.07M | +0.6% |
| kondo/clientServer/manual | 2 | 0.04M | 0.04M | +2.3% |
| kondo/clientServer/sync | 2 | 0.04M | 0.04M | +2.3% |
| kondo/distributedLock/manual | 2 | 0.04M | 0.04M | +2.3% |
| kondo/distributedLock/sync | 2 | 0.04M | 0.04M | +2.3% |
| kondo/flexPaxos/sync | 2 | 0.04M | 0.04M | +2.3% |
| kondo/lockServer/manual | 2 | 0.04M | 0.04M | +2.3% |
| kondo/lockServer/sync | 2 | 0.04M | 0.04M | +2.3% |
| kondo/paxos/sync | 2 | 0.04M | 0.04M | +2.3% |
| kondo/ringLeaderElection/manual | 2 | 0.04M | 0.04M | +2.3% |
| kondo/ringLeaderElection/sync | 2 | 0.04M | 0.04M | +2.3% |
| kondo/shardedKv/manual | 2 | 0.04M | 0.04M | +2.3% |
| kondo/shardedKv/sync | 2 | 0.04M | 0.04M | +2.3% |
| kondo/shardedKvBatched/manual | 2 | 0.04M | 0.04M | +2.3% |
| kondo/shardedKvBatched/sync | 2 | 0.04M | 0.04M | +2.3% |
| kondo/simplifiedLeaderElection/manual | 2 | 0.04M | 0.04M | +2.3% |
| kondo/simplifiedLeaderElection/sync | 2 | 0.04M | 0.04M | +2.3% |
| kondo/twoPhaseCommit/manual | 2 | 0.04M | 0.04M | +2.3% |
| kondo/twoPhaseCommit/paper-version | 2 | 0.04M | 0.04M | +2.3% |
| kondo/twoPhaseCommit/sync | 2 | 0.04M | 0.04M | +2.3% |
| dafnybench/verification-class_tmp_tmpz9ik148s_2022_chapter05-distributed-state-machines_exercises_UtilitiesLibrary.dfy | 2 | 0.04M | 0.04M | -1.1% |
| lit/comp/CovariantCollections.dfy:pinned | 1 | 0.03M | 0.03M | +0.1% |

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
| A/A: master2 vs master (same input, another process) | 30 | 135 | +0.0% [-0.0%, +0.0%] | +0.0% [-0.0%, +0.0%] | +0.0% [-0.0%, +0.0%] | 0 |
| pr vs master | 30 | 135 | -0.5% [-0.9%, +2.1%] | +0.7% [+0.2%, +1.8%] | +1.5% [+1.2%, +1.8%] | 0 |

## Comparisons over the external programs' affected proofs

| comparison | programs | VCs | total | geomean over VCs | per program | verdict flips at limit |
|---|---:|---:|---|---|---|---:|
| A/A: master2 vs master (same input, another process) | 21 | 41 | +0.1% [+0.0%, +0.1%] | +0.0% [+0.0%, +0.0%] | +0.0% [+0.0%, +0.1%] | 0 |
| pr vs master | 21 | 41 | +1.9% [+1.4%, +2.3%] | +1.9% [+1.5%, +2.1%] | +1.8% [+1.5%, +2.1%] | 0 |

## Alternative sound encodings, over the same proofs

restrict: elements defined everywhere, `$ArbitraryBoxValue` outside the domain. domguard: the PR's axiom guarded by `Map#Domain(Map#Glue(a, b, t))`. eager: the PR's axiom plus the trigger `{ Map#Glue(a, b, t), Set#IsMember(a, bx) }`.

| encoding | programs | VCs | total vs master | geomean over VCs vs master | per program vs master | per program vs PR | verdict flips vs master at limit |
|---|---:|---:|---|---|---|---|---:|
| pr | 30 | 135 | -0.5% [-0.9%, +2.2%] | +0.7% [+0.3%, +1.8%] | +1.5% [+1.2%, +1.9%] |  | 0 |
| master2 | 30 | 135 | +0.0% [-0.0%, +0.0%] | +0.0% [-0.0%, +0.0%] | +0.0% [-0.0%, +0.0%] | -1.5% [-1.8%, -1.1%] | 0 |

master2: largest differences from the PR

| job | VC | master | PR | master2 |
|---|---|---:|---:|---:|
| lit/vstte2012/BreadthFirstSearch.dfy:refresh | BreadthFirstSearch.BFS (correctness) (assertion batch 47) | 0.15M | 0.22M | 0.15M |
| lit/vstte2012/BreadthFirstSearch.dfy:refresh | BreadthFirstSearch.BFS (correctness) (assertion batch 71) | 0.45M | 0.52M | 0.45M |
| lit/vstte2012/BreadthFirstSearch.dfy:refresh | BreadthFirstSearch.BFS (correctness) (assertion batch 57) | 0.32M | 0.25M | 0.32M |
| lit/vstte2012/BreadthFirstSearch.dfy:refresh | BreadthFirstSearch.BFS (correctness) (assertion batch 85) | 0.69M | 0.63M | 0.69M |
| lit/vstte2012/BreadthFirstSearch.dfy:refresh | BreadthFirstSearch.BFS (correctness) (assertion batch 45) | 0.22M | 0.17M | 0.22M |
| lit/vstte2012/BreadthFirstSearch.dfy:refresh | BreadthFirstSearch.BFS (correctness) (assertion batch 61) | 0.62M | 0.58M | 0.62M |
