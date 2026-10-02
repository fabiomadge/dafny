# #6540 A/B benchmark (public corpora, seeds 1-4)

Seeds per (VC, prelude): 4 (1, 2, 3, 4; 0 is Dafny's default). VCs: 557 in 5 jobs; **186 affected** (master and PR counts differ), 371 unaffected (identical counts under master and PR for every seed).

## Proof cost over affected VCs that pass everywhere

Totals are sums of per-VC means over seeds. "Per program" averages each program's own VC geomean, so a
program with hundreds of VCs weighs no more than one with two. Brackets are 95% bootstrap intervals that
resample programs, not VCs.

| group | programs | VCs | largest program | total PR/master | geomean over VCs | per program |
|---|---:|---:|---|---|---|---|
| all but synth | 5 | 181 | kondo/flexPaxos/sync (35% of VCs) | +8.0% [-61.3%, +34.5%] | +1.0% [-2.4%, +2.3%] | -0.0% [-2.9%, +2.1%] |
| kondo | 5 | 181 | kondo/flexPaxos/sync (35% of VCs) | +8.0% [-61.4%, +34.5%] | +1.0% [-2.5%, +2.3%] | -0.0% [-2.9%, +2.1%] |

5 affected VCs fail (a verification error) in some run; their cost is the solver's search for a counterexample, reported separately:

| job | VC | master mean (min..max) | PR mean (min..max) |
|---|---|---|---|
| kondo/paxos/sync | PaxosProof.InvNextLeaderReceivedPromisesImpliesAcceptorState (correctness) | 168.49M (27.40..386.84) | 203.03M (80.97..345.02) |
| kondo/paxos/sync | PaxosProof.InvNextChosenImpliesProposingLeaderHearsChosenBallotP2bStep (correctness) | 139.68M (22.37..384.12) | 55.78M (20.48..105.73) |
| kondo/paxos/sync | PaxosProof.InvNextLearnerReceivedAcceptImpliesAccepted (correctness) | 94.59M (24.19..293.81) | 35.13M (21.31..49.27) |
| kondo/twoPhaseCommit/paper-version | TwoPCInvariantProof.InvNextLeaderVotesValid (correctness) | 0.28M (0.27..0.29) | 0.32M (0.27..0.40) |
| kondo/twoPhaseCommit/manual | TwoPCInvariantProof.InvNextLeaderVotesValid (correctness) | 0.27M (0.27..0.27) | 0.30M (0.27..0.33) |

## Total proof RU per seed (affected VCs that pass everywhere)

| prelude | seed 1 | seed 2 | seed 3 | seed 4 | mean | sd |
|---|---:|---:|---:|---:|---:|---:|
| master | 625.1M | 859.0M | 453.9M | 437.9M | 593.9M | 169.7M |
| pr | 417.0M | 738.5M | 887.5M | 523.0M | 641.5M | 183.3M |

## Solver time over those proofs (sum of per-VC means, seconds)

| group | master | PR |
|---|---:|---:|
| all | 358.6 | 443.3 |

## Distribution of per-VC cost ratios over those proofs (mean over seeds)

| ratio bucket | PR/master |
|---|---:|
| < 0.5x | 1 |
| 0.5-0.8x | 6 |
| 0.8-0.95x | 7 |
| 0.95-1.05x | 150 |
| 1.05-1.25x | 10 |
| 1.25-2x | 5 |
| 2-4x | 2 |
| >= 4x | 0 |

## Verdict changes at each job's limit (seeds passing out of 4)

| job | VC | limit | master ok | PR ok | master RU | PR RU |
|---|---|---:|---:|---:|---:|---:|
| kondo/flexPaxos/sync | PaxosProof.InvNextAcceptorValidBundle (correctness) | 50M | 2 | 4 | 61.44M | 34.08M |
| kondo/flexPaxos/sync | PaxosProof.InvNextChosenImpliesProposingLeaderHearsChosenBallot (correctness) | 50M | 4 | 3 | 13.21M | 24.88M |
| kondo/flexPaxos/sync | PaxosProof.InvNextChosenImpliesProposingLeaderHearsChosenBallotP2bStep (correctness) | 50M | 3 | 1 | 29.92M | 96.50M |
| kondo/flexPaxos/sync | PaxosProof.InvNextLeaderReceivedPromisesImpliesAcceptorState (correctness) | 50M | 1 | 2 | 121.78M | 95.86M |
| kondo/flexPaxos/sync | PaxosProof.InvNextLearnerReceivedAcceptImpliesAccepted (correctness) | 50M | 3 | 0 | 78.02M | 97.73M |
| kondo/paxos/sync | PaxosProof.InvNextAcceptorValidBundle (correctness) | 50M | 4 | 2 | 33.23M | 92.91M |
| kondo/paxos/sync | PaxosProof.InvNextChosenImpliesProposingLeaderHearsChosenBallotP1bStep (correctness) | 50M | 4 | 3 | 26.47M | 23.94M |
| kondo/paxos/sync | PaxosProof.InvNextChosenImpliesProposingLeaderHearsChosenBallotP2bStep (correctness) | 50M | 1 | 2 | 139.68M | 55.78M |
| kondo/paxos/sync | PaxosProof.InvNextLeaderReceivedPromisesImpliesAcceptorState (correctness) | 50M | 1 | 0 | 168.49M | 203.03M |
| kondo/paxos/sync | PaxosProof.InvNextLearnerReceivedAcceptImpliesAccepted (correctness) | 50M | 3 | 4 | 94.59M | 35.13M |
| kondo/twoPhaseCommit/manual | TwoPCInvariantProof.InvNextLeaderVotesValid (correctness) | 50M | 4 | 2 | 0.27M | 0.30M |
| kondo/twoPhaseCommit/paper-version | TwoPCInvariantProof.InvNextLeaderVotesValid (correctness) | 50M | 4 | 2 | 0.28M | 0.32M |
| kondo/twoPhaseCommit/sync | TwoPCInvariantProof.InvNextLeaderTallyReflectsPreferences (correctness) | 50M | 2 | 3 | 58.07M | 17.66M |

## Largest changes among those proofs (by |PR - master| mean RU)

| job | VC | master | PR | PR/master | min..max master | min..max PR |
|---|---|---:|---:|---:|---|---|
| kondo/flexPaxos/sync | PaxosProof.InvNextChosenImpliesProposingLeaderHearsChosenBallotP2bStep (correctness) | 29.92M | 96.50M | 3.23 | 3.70..83.53M | 24.24..252.25M |
| kondo/paxos/sync | PaxosProof.InvNextAcceptorValidBundle (correctness) | 33.23M | 92.91M | 2.80 | 14.76..46.14M | 48.56..208.60M |
| kondo/twoPhaseCommit/sync | TwoPCInvariantProof.InvNextLeaderTallyReflectsPreferences (correctness) | 58.07M | 17.66M | 0.30 | 0.67..131.29M | 0.87..67.32M |
| kondo/flexPaxos/sync | PaxosProof.InvNextAcceptorValidBundle (correctness) | 61.44M | 34.08M | 0.55 | 18.25..123.73M | 30.81..37.55M |
| kondo/flexPaxos/sync | PaxosProof.InvNextLeaderReceivedPromisesImpliesAcceptorState (correctness) | 121.78M | 95.86M | 0.79 | 34.72..210.72M | 23.11..240.76M |
| kondo/flexPaxos/sync | PaxosProof.InvNextLearnerReceivedAcceptImpliesAccepted (correctness) | 78.02M | 97.73M | 1.25 | 19.87..213.78M | 75.23..124.82M |
| kondo/flexPaxos/sync | PaxosProof.InvNextChosenImpliesProposingLeaderHearsChosenBallot (correctness) | 13.21M | 24.88M | 1.88 | 3.56..30.66M | 4.40..71.39M |
| kondo/flexPaxos/sync | PaxosProof.InvNextChosenImpliesProposingLeaderHearsChosenBallotP1bStep (correctness) | 33.74M | 25.38M | 0.75 | 18.11..45.42M | 13.63..35.84M |
| kondo/paxos/sync | PaxosProof.InvNextChosenImpliesProposingLeaderHearsChosenBallot (correctness) | 14.39M | 7.29M | 0.51 | 6.25..26.43M | 5.17..11.66M |
| kondo/paxos/sync | PaxosProof.InvNextChosenValImpliesLeaderOnlyHearsVal (correctness) | 10.89M | 13.92M | 1.28 | 10.16..11.92M | 10.94..17.45M |
| kondo/paxos/sync | PaxosProof.InvNextChosenImpliesProposingLeaderHearsChosenBallotP1bStep (correctness) | 26.47M | 23.94M | 0.90 | 21.92..33.78M | 8.36..50.95M |
| kondo/paxos/sync | PaxosProof.InvNextLeaderHighestHeardToPromisedRangeHasNoAccepts (correctness) | 13.76M | 11.42M | 0.83 | 7.30..28.00M | 6.68..13.72M |
| kondo/flexPaxos/sync | PaxosProof.InvNextLeaderHearedImpliesProposed (correctness) | 10.16M | 8.35M | 0.82 | 4.09..20.51M | 4.39..14.09M |
| kondo/flexPaxos/sync | PaxosProof.InvNextLeaderHighestHeardToPromisedRangeHasNoAccepts (correctness) | 10.99M | 12.45M | 1.13 | 8.56..15.44M | 7.63..17.17M |
| kondo/paxos/sync | PaxosProof.InvNextLeaderHearedImpliesProposed (correctness) | 25.20M | 24.10M | 0.96 | 15.53..34.47M | 4.80..40.03M |
| kondo/paxos/sync | PaxosProof.InvNextLeaderHighestHeardUpperBound (correctness) | 1.62M | 2.64M | 1.63 | 1.22..1.99M | 1.89..3.04M |
| kondo/flexPaxos/sync | PaxosProof.InvNextLearnerReceivedAcceptImpliesProposed (correctness) | 4.03M | 4.69M | 1.16 | 2.32..5.94M | 3.15..5.39M |
| kondo/flexPaxos/sync | PaxosProof.InvNextLeaderHighestHeardUpperBound (correctness) | 2.47M | 2.94M | 1.19 | 1.53..5.08M | 2.36..3.68M |
| kondo/flexPaxos/sync | PaxosProof.InvNextLeaderValidReceivedPromises (correctness) | 1.27M | 0.94M | 0.74 | 1.13..1.47M | 0.63..1.21M |
| kondo/twoPhaseCommit/sync | TwoPCInvariantProof.InvNextAC1 (correctness) | 1.00M | 0.75M | 0.75 | 0.77..1.22M | 0.44..0.86M |
| kondo/flexPaxos/sync | PaxosProof.InvNextLearnedImpliesQuorumOfAccepts (correctness) | 0.58M | 0.81M | 1.40 | 0.57..0.60M | 0.59..1.45M |
| kondo/paxos/sync | PaxosProof.InvNextLearnerValidReceivedAccepts (correctness) | 1.10M | 1.31M | 1.19 | 0.77..1.39M | 0.94..1.94M |
| kondo/paxos/sync | PaxosProof.InvNextLearnerReceivedAcceptImpliesProposed (correctness) | 6.05M | 6.26M | 1.03 | 4.96..8.47M | 3.83..8.81M |
| kondo/flexPaxos/sync | PaxosProof.InvNextChosenValImpliesLeaderOnlyHearsVal (correctness) | 2.56M | 2.36M | 0.92 | 1.89..3.71M | 1.80..2.99M |
| kondo/paxos/sync | PaxosProof.InvNextLeaderValidReceivedPromises (correctness) | 0.95M | 1.06M | 1.12 | 0.60..1.27M | 0.59..1.71M |

## Per job (proofs among the affected VCs)

| job | VCs | master | PR | PR vs master |
|---|---:|---:|---:|---:|
| kondo/flexPaxos/sync | 63 | 381.74M | 418.53M | +9.6% |
| kondo/paxos/sync | 60 | 144.55M | 195.88M | +35.5% |
| kondo/twoPhaseCommit/sync | 22 | 61.78M | 21.15M | -65.8% |
| kondo/twoPhaseCommit/manual | 18 | 2.99M | 2.99M | -0.1% |
| kondo/twoPhaseCommit/paper-version | 18 | 2.89M | 2.93M | +1.6% |

## Stability over the affected VCs (all but synth)

Flaky: some seeds pass at the job's limit and others do not. Spread: the coefficient of variation of a VC's cost across seeds, for VCs above 1M RU under master.

| prelude | flaky VCs | flaky, not under master | no longer flaky | median spread | 90th-percentile spread |
|---|---:|---:|---:|---:|---:|
| master | 8 | 0 | 0 | 0.36 | 1.01 |
| master2 | 8 | 0 | 0 | 0.36 | 1.01 |
| pr | 9 | 5 | 4 | 0.29 | 0.90 |

Flaky under the PR but not under master (seeds passing out of the run):

| job | VC | master | PR | PR mean RU |
|---|---|---:|---:|---:|
| kondo/paxos/sync | PaxosProof.InvNextAcceptorValidBundle (correctness) | 4 | 2 | 92.91M |
| kondo/flexPaxos/sync | PaxosProof.InvNextChosenImpliesProposingLeaderHearsChosenBallot (correctness) | 4 | 3 | 24.88M |
| kondo/paxos/sync | PaxosProof.InvNextChosenImpliesProposingLeaderHearsChosenBallotP1bStep (correctness) | 4 | 3 | 23.94M |
| kondo/twoPhaseCommit/paper-version | TwoPCInvariantProof.InvNextLeaderVotesValid (correctness) | 4 | 2 | 0.32M |
| kondo/twoPhaseCommit/manual | TwoPCInvariantProof.InvNextLeaderVotesValid (correctness) | 4 | 2 | 0.30M |

## Comparisons over the affected proofs (all but synth)

| comparison | programs | VCs | total | geomean over VCs | per program | verdict flips at limit |
|---|---:|---:|---|---|---|---:|
| A/A: master2 vs master (same input, another process) | 5 | 181 | +0.0% [+0.0%, +0.0%] | +0.0% [+0.0%, +0.0%] | +0.0% [+0.0%, +0.0%] | 0 |
| pr vs master | 5 | 181 | +8.0% [-61.3%, +34.5%] | +1.0% [-2.4%, +2.3%] | -0.0% [-2.9%, +2.1%] | 8 |

## Comparisons over the external programs' affected proofs

| comparison | programs | VCs | total | geomean over VCs | per program | verdict flips at limit |
|---|---:|---:|---|---|---|---:|
| A/A: master2 vs master (same input, another process) | 5 | 181 | +0.0% [+0.0%, +0.0%] | +0.0% [+0.0%, +0.0%] | +0.0% [+0.0%, +0.0%] | 0 |
| pr vs master | 5 | 181 | +8.0% [-61.3%, +34.5%] | +1.0% [-2.4%, +2.3%] | -0.0% [-2.9%, +2.1%] | 8 |

## Alternative sound encodings, over the same proofs

restrict: elements defined everywhere, `$ArbitraryBoxValue` outside the domain. domguard: the PR's axiom guarded by `Map#Domain(Map#Glue(a, b, t))`. eager: the PR's axiom plus the trigger `{ Map#Glue(a, b, t), Set#IsMember(a, bx) }`.

| encoding | programs | VCs | total vs master | geomean over VCs vs master | per program vs master | per program vs PR | verdict flips vs master at limit |
|---|---:|---:|---|---|---|---|---:|
| pr | 5 | 181 | +8.0% [-61.3%, +34.5%] | +1.0% [-2.4%, +2.3%] | -0.0% [-2.9%, +2.1%] |  | 13 |
| master2 | 5 | 181 | +0.0% [+0.0%, +0.0%] | +0.0% [+0.0%, +0.0%] | +0.0% [+0.0%, +0.0%] | +0.0% [-2.0%, +3.0%] | 0 |

master2: largest differences from the PR

| job | VC | master | PR | master2 |
|---|---|---:|---:|---:|
| kondo/flexPaxos/sync | PaxosProof.InvNextChosenImpliesProposingLeaderHearsChosenBallotP2bStep (correctness) | 29.92M | 96.50M | 29.92M |
| kondo/paxos/sync | PaxosProof.InvNextAcceptorValidBundle (correctness) | 33.23M | 92.91M | 33.23M |
| kondo/twoPhaseCommit/sync | TwoPCInvariantProof.InvNextLeaderTallyReflectsPreferences (correctness) | 58.07M | 17.66M | 58.07M |
| kondo/flexPaxos/sync | PaxosProof.InvNextAcceptorValidBundle (correctness) | 61.44M | 34.08M | 61.44M |
| kondo/flexPaxos/sync | PaxosProof.InvNextLeaderReceivedPromisesImpliesAcceptorState (correctness) | 121.78M | 95.86M | 121.78M |
| kondo/flexPaxos/sync | PaxosProof.InvNextLearnerReceivedAcceptImpliesAccepted (correctness) | 78.02M | 97.73M | 78.02M |
