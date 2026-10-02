# #6543 A/B benchmark (public corpora, seeds 1-4)

Seeds per (VC, prelude): 4 (1, 2, 3, 4; 0 is Dafny's default). VCs: 296 in 2 jobs; **146 affected** (master and PR counts differ), 150 unaffected (identical counts under master and PR for every seed).
Unaffected VCs whose counts differ under the placebo: 0.

## Proof cost over affected VCs that pass everywhere

Totals are sums of per-VC means over seeds. "Per program" averages each program's own VC geomean, so a
program with hundreds of VCs weighs no more than one with two. Brackets are 95% bootstrap intervals that
resample programs, not VCs.

| group | programs | VCs | largest program | total PR/master | geomean over VCs | per program | placebo per program |
|---|---:|---:|---|---|---|---|---|
| all but synth | 2 | 142 | kondo/flexPaxos/sync (50% of VCs) | -22.5% [-29.0%, -15.2%] | -2.2% [-2.3%, -2.0%] | -2.2% [-2.3%, -2.0%] | -0.2% [-0.7%, +0.3%] |
| kondo | 2 | 142 | kondo/flexPaxos/sync (50% of VCs) | -22.5% [-29.0%, -15.2%] | -2.2% [-2.3%, -2.0%] | -2.2% [-2.3%, -2.0%] | -0.2% [-0.7%, +0.3%] |

4 affected VCs fail (a verification error) in some run; their cost is the solver's search for a counterexample, reported separately:

| job | VC | master mean (min..max) | PR mean (min..max) | placebo mean |
|---|---|---|---|---|
| kondo/paxos/sync | PaxosProof.InvNextChosenImpliesProposingLeaderHearsChosenBallotP2bStep (correctness) | 139.68M (22.37..384.12) | 90.19M (12.24..312.98) | 140.44M |
| kondo/paxos/sync | PaxosProof.InvNextLearnerReceivedAcceptImpliesAccepted (correctness) | 94.59M (24.19..293.81) | 51.76M (18.15..71.27) | 152.74M |
| kondo/flexPaxos/sync | PaxosProof.InvNextLearnerReceivedAcceptImpliesAccepted (correctness) | 78.02M (19.87..213.78) | 192.17M (66.57..345.97) | 225.70M |
| kondo/flexPaxos/sync | PaxosProof.InvNextChosenImpliesProposingLeaderHearsChosenBallotP2bStep (correctness) | 29.92M (3.70..83.53) | 104.13M (14.26..306.00) | 25.05M |

## Total proof RU per seed (affected VCs that pass everywhere)

| prelude | seed 1 | seed 2 | seed 3 | seed 4 | mean | sd |
|---|---:|---:|---:|---:|---:|---:|
| master | 599.0M | 553.2M | 731.8M | 484.4M | 592.1M | 90.4M |
| pr | 347.3M | 607.6M | 317.5M | 562.2M | 458.6M | 127.7M |
| placebo | 523.6M | 526.5M | 717.2M | 386.4M | 538.4M | 117.7M |

## Solver time over those proofs (sum of per-VC means, seconds)

| group | master | PR | placebo |
|---|---:|---:|---:|
| all | 399.2 | 274.3 | 274.0 |

## Distribution of per-VC cost ratios over those proofs (mean over seeds)

| ratio bucket | PR/master | placebo/master |
|---|---:|---:|
| < 0.5x | 2 | 0 |
| 0.5-0.8x | 8 | 3 |
| 0.8-0.95x | 4 | 2 |
| 0.95-1.05x | 121 | 130 |
| 1.05-1.25x | 4 | 6 |
| 1.25-2x | 3 | 1 |
| 2-4x | 0 | 0 |
| >= 4x | 0 | 0 |

## Verdict changes at each job's limit (seeds passing out of 4)

| job | VC | limit | master ok | PR ok | placebo ok | master RU | PR RU |
|---|---|---:|---:|---:|---:|---:|---:|
| kondo/flexPaxos/sync | PaxosProof.InvNextAcceptorValidBundle (correctness) | 50M | 2 | 4 | 4 | 61.44M | 25.58M |
| kondo/flexPaxos/sync | PaxosProof.InvNextChosenImpliesProposingLeaderHearsChosenBallot (correctness) | 50M | 4 | 4 | 3 | 13.21M | 10.01M |
| kondo/flexPaxos/sync | PaxosProof.InvNextChosenImpliesProposingLeaderHearsChosenBallotP1bStep (correctness) | 50M | 4 | 3 | 4 | 33.74M | 64.82M |
| kondo/flexPaxos/sync | PaxosProof.InvNextLearnerReceivedAcceptImpliesAccepted (correctness) | 50M | 3 | 0 | 0 | 78.02M | 192.17M |
| kondo/paxos/sync | PaxosProof.InvNextAcceptorValidBundle (correctness) | 50M | 4 | 2 | 3 | 33.23M | 60.64M |
| kondo/paxos/sync | PaxosProof.InvNextChosenImpliesProposingLeaderHearsChosenBallotP2bStep (correctness) | 50M | 1 | 3 | 2 | 139.68M | 90.19M |
| kondo/paxos/sync | PaxosProof.InvNextLeaderReceivedPromisesImpliesAcceptorState (correctness) | 50M | 1 | 3 | 0 | 168.49M | 62.60M |
| kondo/paxos/sync | PaxosProof.InvNextLearnerReceivedAcceptImpliesAccepted (correctness) | 50M | 3 | 1 | 2 | 94.59M | 51.76M |

## Largest changes among those proofs (by |PR - master| mean RU)

| job | VC | master | PR | PR/master | placebo | min..max master | min..max PR |
|---|---|---:|---:|---:|---:|---|---|
| kondo/paxos/sync | PaxosProof.InvNextLeaderReceivedPromisesImpliesAcceptorState (correctness) | 168.49M | 62.60M | 0.37 | 169.50M | 27.40..386.84M | 29.81..142.95M |
| kondo/flexPaxos/sync | PaxosProof.InvNextAcceptorValidBundle (correctness) | 61.44M | 25.58M | 0.42 | 34.78M | 18.25..123.73M | 10.87..46.87M |
| kondo/flexPaxos/sync | PaxosProof.InvNextLeaderReceivedPromisesImpliesAcceptorState (correctness) | 121.78M | 89.58M | 0.74 | 90.48M | 34.72..210.72M | 44.34..189.98M |
| kondo/flexPaxos/sync | PaxosProof.InvNextChosenImpliesProposingLeaderHearsChosenBallotP1bStep (correctness) | 33.74M | 64.82M | 1.92 | 25.63M | 18.11..45.42M | 12.12..194.83M |
| kondo/paxos/sync | PaxosProof.InvNextAcceptorValidBundle (correctness) | 33.23M | 60.64M | 1.82 | 37.73M | 14.76..46.14M | 9.37..154.74M |
| kondo/paxos/sync | PaxosProof.InvNextLeaderHearedImpliesProposed (correctness) | 25.20M | 18.91M | 0.75 | 25.20M | 15.53..34.47M | 10.84..28.71M |
| kondo/paxos/sync | PaxosProof.InvNextChosenImpliesProposingLeaderHearsChosenBallot (correctness) | 14.39M | 10.16M | 0.71 | 12.68M | 6.25..26.43M | 4.39..14.39M |
| kondo/flexPaxos/sync | PaxosProof.InvNextChosenImpliesProposingLeaderHearsChosenBallot (correctness) | 13.21M | 10.01M | 0.76 | 18.64M | 3.56..30.66M | 4.07..20.47M |
| kondo/paxos/sync | PaxosProof.InvNextLeaderHighestHeardToPromisedRangeHasNoAccepts (correctness) | 13.76M | 11.24M | 0.82 | 14.69M | 7.30..28.00M | 8.20..13.10M |
| kondo/paxos/sync | PaxosProof.InvNextChosenImpliesProposingLeaderHearsChosenBallotP1bStep (correctness) | 26.47M | 27.87M | 1.05 | 24.91M | 21.92..33.78M | 11.27..41.49M |
| kondo/flexPaxos/sync | PaxosProof.InvNextLearnerReceivedAcceptImpliesProposed (correctness) | 4.03M | 2.69M | 0.67 | 4.30M | 2.32..5.94M | 2.11..3.26M |
| kondo/paxos/sync | PaxosProof.InvNextLearnerReceivedAcceptImpliesProposed (correctness) | 6.05M | 4.74M | 0.78 | 6.88M | 4.96..8.47M | 4.24..5.36M |
| kondo/flexPaxos/sync | PaxosProof.InvNextLeaderHighestHeardUpperBound (correctness) | 2.47M | 1.51M | 0.61 | 2.47M | 1.53..5.08M | 1.12..2.22M |
| kondo/flexPaxos/sync | PaxosProof.InvNextLeaderHearedImpliesProposed (correctness) | 10.16M | 10.77M | 1.06 | 10.16M | 4.09..20.51M | 4.16..22.24M |
| kondo/flexPaxos/sync | PaxosProof.InvNextLeaderValidReceivedPromises (correctness) | 1.27M | 0.88M | 0.70 | 1.27M | 1.13..1.47M | 0.58..1.35M |
| kondo/flexPaxos/sync | PaxosProof.InvNextLearnedImpliesQuorumOfAccepts (correctness) | 0.58M | 0.92M | 1.58 | 0.58M | 0.57..0.60M | 0.53..1.91M |
| kondo/paxos/sync | PaxosProof.InvNextLeaderHighestHeardUpperBound (correctness) | 1.62M | 1.91M | 1.18 | 1.62M | 1.22..1.99M | 1.61..2.44M |
| kondo/paxos/sync | PaxosProof.InvNextLearnerValidReceivedAccepts (correctness) | 1.10M | 0.93M | 0.84 | 1.10M | 0.77..1.39M | 0.77..1.23M |
| kondo/flexPaxos/sync | PaxosProof.InvNextChosenValImpliesLeaderOnlyHearsVal (correctness) | 2.56M | 2.71M | 1.06 | 2.56M | 1.89..3.71M | 2.25..3.19M |
| kondo/flexPaxos/sync | PaxosProof.InvNextChosenValImpliesAcceptorOnlyAcceptsVal (correctness) | 1.87M | 1.79M | 0.96 | 1.88M | 1.48..2.26M | 1.49..2.07M |
| kondo/flexPaxos/sync | PaxosProof.InvImpliesAtMostOneChosenVal (correctness) | 0.81M | 0.74M | 0.92 | 0.81M | 0.70..0.98M | 0.70..0.83M |
| kondo/paxos/sync | PaxosProof.InvNextLeaderValidReceivedPromises (correctness) | 0.95M | 0.88M | 0.93 | 0.95M | 0.60..1.27M | 0.57..1.24M |
| kondo/paxos/sync | PaxosProof.InvNextChosenValImpliesLeaderOnlyHearsVal (correctness) | 10.89M | 10.83M | 0.99 | 10.89M | 10.16..11.92M | 8.81..11.92M |
| kondo/flexPaxos/sync | PaxosProof.InvNextLeaderHighestHeardToPromisedRangeHasNoAccepts (correctness) | 10.99M | 10.93M | 0.99 | 13.53M | 8.56..15.44M | 4.90..16.43M |
| kondo/paxos/sync | PaxosProof.InvNextChosenValImpliesAcceptorOnlyAcceptsVal (correctness) | 1.75M | 1.69M | 0.97 | 1.84M | 1.43..1.99M | 1.45..1.90M |

## Per job (proofs among the affected VCs)

| job | VCs | master | PR | PR vs master | placebo vs master |
|---|---:|---:|---:|---:|---:|
| kondo/paxos/sync | 71 | 315.81M | 224.35M | -29.0% | +1.3% |
| kondo/flexPaxos/sync | 71 | 276.31M | 234.30M | -15.2% | -20.9% |

## Stability over the affected VCs (all but synth)

Flaky: some seeds pass at the job's limit and others do not. Spread: the coefficient of variation of a VC's cost across seeds, for VCs above 1M RU under master.

| prelude | flaky VCs | flaky, not under master | no longer flaky | median spread | 90th-percentile spread |
|---|---:|---:|---:|---:|---:|
| master | 7 | 0 | 0 | 0.34 | 1.01 |
| master2 | 7 | 0 | 0 | 0.34 | 1.01 |
| placebo | 6 | 2 | 3 | 0.28 | 0.87 |
| pr | 7 | 2 | 2 | 0.36 | 0.95 |

Flaky under the PR but not under master (seeds passing out of the run):

| job | VC | master | PR | placebo | PR mean RU |
|---|---|---:|---:|---:|---:|
| kondo/flexPaxos/sync | PaxosProof.InvNextChosenImpliesProposingLeaderHearsChosenBallotP1bStep (correctness) | 4 | 3 | 4 | 64.82M |
| kondo/paxos/sync | PaxosProof.InvNextAcceptorValidBundle (correctness) | 4 | 2 | 3 | 60.64M |

## Comparisons over the affected proofs (all but synth)

| comparison | programs | VCs | total | geomean over VCs | per program | verdict flips at limit |
|---|---:|---:|---|---|---|---:|
| A/A: master2 vs master (same input, another process) | 2 | 142 | +0.0% [+0.0%, +0.0%] | +0.0% [+0.0%, +0.0%] | +0.0% [+0.0%, +0.0%] | 0 |
| placebo vs master (the old axiom, rewritten) | 2 | 142 | -9.1% [-20.9%, +1.3%] | -0.2% [-0.7%, +0.3%] | -0.2% [-0.7%, +0.3%] | 4 |
| pr vs master | 2 | 142 | -22.5% [-29.0%, -15.2%] | -2.2% [-2.3%, -2.0%] | -2.2% [-2.3%, -2.0%] | 4 |

## Comparisons over the external programs' affected proofs

| comparison | programs | VCs | total | geomean over VCs | per program | verdict flips at limit |
|---|---:|---:|---|---|---|---:|
| A/A: master2 vs master (same input, another process) | 2 | 142 | +0.0% [+0.0%, +0.0%] | +0.0% [+0.0%, +0.0%] | +0.0% [+0.0%, +0.0%] | 0 |
| placebo vs master (the old axiom, rewritten) | 2 | 142 | -9.1% [-20.9%, +1.3%] | -0.2% [-0.7%, +0.3%] | -0.2% [-0.7%, +0.3%] | 4 |
| pr vs master | 2 | 142 | -22.5% [-29.0%, -15.2%] | -2.2% [-2.3%, -2.0%] | -2.2% [-2.3%, -2.0%] | 4 |

## Alternative sound encodings, over the same proofs

restrict: elements defined everywhere, `$ArbitraryBoxValue` outside the domain. domguard: the PR's axiom guarded by `Map#Domain(Map#Glue(a, b, t))`. eager: the PR's axiom plus the trigger `{ Map#Glue(a, b, t), Set#IsMember(a, bx) }`.

| encoding | programs | VCs | total vs master | geomean over VCs vs master | per program vs master | per program vs PR | verdict flips vs master at limit |
|---|---:|---:|---|---|---|---|---:|
| pr | 2 | 142 | -22.5% [-29.0%, -15.2%] | -2.2% [-2.3%, -2.0%] | -2.2% [-2.3%, -2.0%] |  | 7 |
| master2 | 2 | 142 | +0.0% [+0.0%, +0.0%] | +0.0% [+0.0%, +0.0%] | +0.0% [+0.0%, +0.0%] | +2.2% [+2.1%, +2.3%] | 0 |

master2: largest differences from the PR

| job | VC | master | PR | master2 |
|---|---|---:|---:|---:|
| kondo/paxos/sync | PaxosProof.InvNextLeaderReceivedPromisesImpliesAcceptorState (correctness) | 168.49M | 62.60M | 168.49M |
| kondo/flexPaxos/sync | PaxosProof.InvNextAcceptorValidBundle (correctness) | 61.44M | 25.58M | 61.44M |
| kondo/flexPaxos/sync | PaxosProof.InvNextLeaderReceivedPromisesImpliesAcceptorState (correctness) | 121.78M | 89.58M | 121.78M |
| kondo/flexPaxos/sync | PaxosProof.InvNextChosenImpliesProposingLeaderHearsChosenBallotP1bStep (correctness) | 33.74M | 64.82M | 33.74M |
| kondo/paxos/sync | PaxosProof.InvNextAcceptorValidBundle (correctness) | 33.23M | 60.64M | 33.23M |
| kondo/paxos/sync | PaxosProof.InvNextLeaderHearedImpliesProposed (correctness) | 25.20M | 18.91M | 25.20M |
