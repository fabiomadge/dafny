# #6542 A/B benchmark (public corpora, seed 1)

Seeds per (VC, prelude): 1 (1; 0 is Dafny's default). VCs: 27063 in 2077 jobs; **43 affected** (master and PR counts differ), 27020 unaffected (identical counts under master and PR for every seed).

## Proof cost over affected VCs that pass everywhere

Totals are sums of per-VC means over seeds. "Per program" averages each program's own VC geomean, so a
program with hundreds of VCs weighs no more than one with two. Brackets are 95% bootstrap intervals that
resample programs, not VCs.

| group | programs | VCs | largest program | total PR/master | geomean over VCs | per program |
|---|---:|---:|---|---|---|---|
| all but synth | 15 | 27 | lit/comp/Forall.dfy (15% of VCs) | +39.5% [-11.9%, +55.0%] | +1.2% [-2.6%, +6.8%] | +2.8% [-3.7%, +11.6%] |
| libraries | 1 | 2 | libraries/dafny/Collections/Seqs.dfy (100% of VCs) | +0.3% [+0.3%, +0.3%] | +0.2% [+0.2%, +0.2%] | +0.2% [+0.2%, +0.2%] |
| lit | 14 | 25 | lit/comp/Forall.dfy (16% of VCs) | +39.7% [-12.0%, +55.2%] | +1.3% [-2.6%, +7.3%] | +3.0% [-3.8%, +12.1%] |

16 affected VCs fail (a verification error) in some run; their cost is the solver's search for a counterexample, reported separately:

| job | VC | master mean (min..max) | PR mean (min..max) |
|---|---|---|---|
| lit/comp/TypeParams.dfy:refresh | Standard (correctness) | 832.98M (832.98..832.98) | 836.07M (836.07..836.07) |
| lit/dafny0/FunctionSpecifications.dfy:refresh | GoodPost (well-formedness) | 311.14M (311.14..311.14) | 312.84M (312.84..312.84) |
| lit/cli/defaultTimeLimit.dfy:refresh | Foo (correctness) | 298.84M (298.84..298.84) | 376.73M (376.73..376.73) |
| kondo/paxos/sync | PaxosProof.InvNextLearnerReceivedAcceptImpliesAccepted (correctness) | 293.81M (293.81..293.81) | 378.69M (378.69..378.69) |
| libraries/dafny/Collections/Seqs.dfy | Dafny.Collections.Seq.LemmaMapDistributesOverConcat (correctness) | 243.34M (243.34..243.34) | 247.48M (247.48..247.48) |
| dafnybench/dafny_experiments_tmp_tmpz29_3_3i_circuit.dfy | CombineCircuits.CombineCircuitsCorrect (correctness) | 214.71M (214.71..214.71) | 250.31M (250.31..250.31) |
| libraries/dafny/Collections/Seqs.dfy | Dafny.Collections.Seq.LemmaFilterDistributesOverConcat (correctness) (assertion batch 2) | 171.40M (171.40..171.40) | 173.77M (173.77..173.77) |
| lit/dafny1/Rippling.legacy.dfy:refresh | P2 (correctness) | 22.88M (22.88..22.88) | 23.21M (23.21..23.21) |
| lit/hofs/Folding.legacy.dfy:refresh | FoldL_Use_Direct (correctness) | 21.23M (21.23..21.23) | 21.23M (21.23..21.23) |
| lit/vstte2012/RingBufferAuto.dfy:refresh | RingBuffer.ResizingEnqueue (correctness) | 8.76M (8.76..8.76) | 8.83M (8.83..8.83) |

## Total proof RU per seed (affected VCs that pass everywhere)

| prelude | seed 1 | mean | sd |
|---|---:|---:|---:|
| master | 66.2M | 66.2M | 0.0M |
| pr | 92.3M | 92.3M | 0.0M |

## Solver time over those proofs (sum of per-VC means, seconds)

| group | master | PR |
|---|---:|---:|
| all | 50.4 | 82.3 |
| lit | 50.3 | 82.2 |

## Distribution of per-VC cost ratios over those proofs (mean over seeds)

| ratio bucket | PR/master |
|---|---:|
| < 0.5x | 0 |
| 0.5-0.8x | 0 |
| 0.8-0.95x | 3 |
| 0.95-1.05x | 21 |
| 1.05-1.25x | 2 |
| 1.25-2x | 1 |
| 2-4x | 0 |
| >= 4x | 0 |

## Verdict changes at each job's limit (seeds passing out of 1)

| job | VC | limit | master ok | PR ok | master RU | PR RU |
|---|---|---:|---:|---:|---:|---:|
| lit/concurrency/12-MutexLifetime-short.dfy:refresh | Lifetime._ctor (correctness) | 50M | 1 | 0 | 41.47M | 65.91M |

## Largest changes among those proofs (by |PR - master| mean RU)

| job | VC | master | PR | PR/master | min..max master | min..max PR |
|---|---|---:|---:|---:|---|---|
| lit/concurrency/12-MutexLifetime-short.dfy:refresh | Lifetime._ctor (correctness) | 41.47M | 65.91M | 1.59 | 41.47..41.47M | 65.91..65.91M |
| lit/VSI-Benchmarks/b4.dfy:refresh | Map.RemoveNonFirst (correctness) | 12.46M | 15.44M | 1.24 | 12.46..12.46M | 15.44..15.44M |
| lit/VSI-Benchmarks/b5.dfy:refresh | Queue.Enqueue (correctness) | 4.86M | 4.04M | 0.83 | 4.86..4.86M | 4.04..4.04M |
| lit/dafny1/Queue.dfy:refresh | Queue.Enqueue (correctness) | 4.94M | 4.44M | 0.90 | 4.94..4.94M | 4.44..4.44M |
| lit/git-issues/git-issue-3855.dfy:pinned | Memory.fGC (correctness) | 0.81M | 0.90M | 1.11 | 0.81..0.81M | 0.90..0.90M |
| lit/comp/ComprehensionsNewSyntax.dfy:refresh | Enumerations (correctness) | 0.09M | 0.07M | 0.87 | 0.09..0.09M | 0.07..0.07M |
| lit/comp/ForallNewSyntax.dfy:refresh | ObjectTests.Functions (correctness) | 0.13M | 0.13M | 1.02 | 0.13..0.13M | 0.13..0.13M |
| lit/comp/Forall.dfy:refresh | ObjectTests.Functions (correctness) | 0.11M | 0.11M | 0.99 | 0.11..0.11M | 0.11..0.11M |
| lit/comp/ForallNewSyntax.dfy:refresh | ObjectTests.BasicCases (correctness) | 0.08M | 0.08M | 0.98 | 0.08..0.08M | 0.08..0.08M |
| lit/comp/ForallNewSyntax.dfy:refresh | ObjectTests.BadFieldAccesses (correctness) | 0.18M | 0.18M | 0.99 | 0.18..0.18M | 0.18..0.18M |
| lit/comp/Forall.dfy:refresh | ObjectTests.BasicCases (correctness) | 0.08M | 0.08M | 0.99 | 0.08..0.08M | 0.08..0.08M |
| lit/comp/Forall.dfy:refresh | ObjectTests.BadFieldAccesses (correctness) | 0.20M | 0.20M | 1.00 | 0.20..0.20M | 0.20..0.20M |
| lit/comp/Comprehensions.dfy:refresh | Enumerations (correctness) | 0.07M | 0.08M | 1.01 | 0.07..0.07M | 0.08..0.08M |
| lit/unicodecharsFalse/comp/Comprehensions.dfy:refresh | Enumerations (correctness) | 0.07M | 0.08M | 1.01 | 0.07..0.07M | 0.08..0.08M |
| libraries/dafny/Collections/Seqs.dfy | Dafny.Collections.Seq.LemmaFoldRightDistributesOverConcat (correctness) | 0.12M | 0.12M | 1.00 | 0.12..0.12M | 0.12..0.12M |
| lit/comp/Comprehensions.dfy:refresh | EnumerationsMaybeNull (correctness) | 0.08M | 0.08M | 1.00 | 0.08..0.08M | 0.08..0.08M |
| lit/comp/ComprehensionsNewSyntax.dfy:refresh | EnumerationsMaybeNull (correctness) | 0.08M | 0.08M | 1.00 | 0.08..0.08M | 0.08..0.08M |
| lit/comp/Forall.dfy:refresh | ForallWithNewtype.Test (correctness) | 0.01M | 0.01M | 1.00 | 0.01..0.01M | 0.01..0.01M |
| lit/unicodecharsFalse/comp/Comprehensions.dfy:refresh | EnumerationsMaybeNull (correctness) | 0.08M | 0.08M | 1.00 | 0.08..0.08M | 0.08..0.08M |
| libraries/dafny/Collections/Seqs.dfy | Dafny.Collections.Seq.MergeSortBy (well-formedness) | 0.07M | 0.07M | 1.00 | 0.07..0.07M | 0.07..0.07M |
| lit/dafny0/MoForallCompilation.dfy:refresh | Transpose (correctness) | 0.07M | 0.07M | 1.00 | 0.07..0.07M | 0.07..0.07M |
| lit/dafny0/SmallTests.dfy:refresh | Modifies.F (correctness) | 0.01M | 0.01M | 1.00 | 0.01..0.01M | 0.01..0.01M |
| lit/dafny0/ForallStmt.dfy:refresh | M2 (correctness) | 0.03M | 0.03M | 1.00 | 0.03..0.03M | 0.03..0.03M |
| lit/dafny0/ForallStmt.dfy:refresh | M0 (correctness) | 0.01M | 0.01M | 1.00 | 0.01..0.01M | 0.01..0.01M |
| lit/dafny0/MoForallCompilation.dfy:refresh | Node.IncEverything (correctness) | 0.02M | 0.02M | 1.00 | 0.02..0.02M | 0.02..0.02M |

## Per job (proofs among the affected VCs)

| job | VCs | master | PR | PR vs master |
|---|---:|---:|---:|---:|
| lit/concurrency/12-MutexLifetime-short.dfy:refresh | 1 | 41.47M | 65.91M | +58.9% |
| lit/VSI-Benchmarks/b4.dfy:refresh | 1 | 12.46M | 15.44M | +23.8% |
| lit/dafny1/Queue.dfy:refresh | 1 | 4.94M | 4.44M | -10.2% |
| lit/VSI-Benchmarks/b5.dfy:refresh | 1 | 4.86M | 4.04M | -16.8% |
| lit/git-issues/git-issue-3855.dfy:pinned | 1 | 0.81M | 0.90M | +10.9% |
| lit/comp/Forall.dfy:refresh | 4 | 0.41M | 0.40M | -0.8% |
| lit/comp/ForallNewSyntax.dfy:refresh | 3 | 0.38M | 0.38M | -0.1% |
| libraries/dafny/Collections/Seqs.dfy | 2 | 0.19M | 0.19M | +0.3% |
| lit/comp/ComprehensionsNewSyntax.dfy:refresh | 2 | 0.17M | 0.16M | -6.7% |
| lit/comp/Comprehensions.dfy:refresh | 2 | 0.15M | 0.16M | +0.5% |
| lit/unicodecharsFalse/comp/Comprehensions.dfy:refresh | 2 | 0.15M | 0.16M | +0.5% |
| lit/dafny0/MoForallCompilation.dfy:refresh | 2 | 0.09M | 0.09M | +0.0% |
| lit/dafny0/ForallStmt.dfy:refresh | 2 | 0.04M | 0.04M | +0.0% |
| lit/dafny0/SmallTests.dfy:refresh | 2 | 0.03M | 0.03M | +0.0% |
| lit/dafny0/ReadsOnMethods.dfy:refresh | 1 | 0.01M | 0.01M | -0.0% |

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
| A/A: master2 vs master (same input, another process) | 15 | 27 | +0.0% [+0.0%, +0.0%] | +0.0% [+0.0%, +0.1%] | +0.0% [+0.0%, +0.0%] | 0 |
| pr vs master | 15 | 27 | +39.5% [-11.8%, +55.3%] | +1.2% [-2.4%, +6.5%] | +2.8% [-3.5%, +11.0%] | 1 |

## Comparisons over the external programs' affected proofs

| comparison | programs | VCs | total | geomean over VCs | per program | verdict flips at limit |
|---|---:|---:|---|---|---|---:|
| A/A: master2 vs master (same input, another process) | 1 | 2 | +0.3% [+0.3%, +0.3%] | +0.2% [+0.2%, +0.2%] | +0.2% [+0.2%, +0.2%] | 0 |
| pr vs master | 1 | 2 | +0.3% [+0.3%, +0.3%] | +0.2% [+0.2%, +0.2%] | +0.2% [+0.2%, +0.2%] | 0 |

## Alternative sound encodings, over the same proofs

restrict: elements defined everywhere, `$ArbitraryBoxValue` outside the domain. domguard: the PR's axiom guarded by `Map#Domain(Map#Glue(a, b, t))`. eager: the PR's axiom plus the trigger `{ Map#Glue(a, b, t), Set#IsMember(a, bx) }`.

| encoding | programs | VCs | total vs master | geomean over VCs vs master | per program vs master | per program vs PR | verdict flips vs master at limit |
|---|---:|---:|---|---|---|---|---:|
| pr | 15 | 27 | +39.5% [-11.6%, +55.4%] | +1.2% [-2.3%, +6.9%] | +2.8% [-3.3%, +11.8%] |  | 1 |
| master2 | 15 | 27 | +0.0% [+0.0%, +0.0%] | +0.0% [+0.0%, +0.1%] | +0.0% [+0.0%, +0.0%] | -2.8% [-10.2%, +3.5%] | 0 |

master2: largest differences from the PR

| job | VC | master | PR | master2 |
|---|---|---:|---:|---:|
| lit/concurrency/12-MutexLifetime-short.dfy:refresh | Lifetime._ctor (correctness) | 41.47M | 65.91M | 41.47M |
| lit/VSI-Benchmarks/b4.dfy:refresh | Map.RemoveNonFirst (correctness) | 12.46M | 15.44M | 12.46M |
| lit/VSI-Benchmarks/b5.dfy:refresh | Queue.Enqueue (correctness) | 4.86M | 4.04M | 4.86M |
| lit/dafny1/Queue.dfy:refresh | Queue.Enqueue (correctness) | 4.94M | 4.44M | 4.94M |
| lit/git-issues/git-issue-3855.dfy:pinned | Memory.fGC (correctness) | 0.81M | 0.90M | 0.81M |
| lit/comp/ComprehensionsNewSyntax.dfy:refresh | Enumerations (correctness) | 0.09M | 0.07M | 0.09M |
