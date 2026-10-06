# cvc5 against z3

Seed 1, a per-VC time limit of 60 s for both. 2077 jobs ran under both (2077 programs), 26935 VCs.

## Runs

| variant | no rows | ok |
|---|---:|---:|
| z3 | 688 | 1389 |
| cvc5 | 690 | 1387 |

## Verdicts

A VC is *proved* when it passes within 60 s; *cap* means it ran out of time (or ran into the limit); *failed* means the solver gave up within the limit; *missing* means the run reported no result for it (it ended early).

| z3 \ cvc5 | proved | failed | cap | missing | total |
|---|---:|---:|---:|---:|---:|
| proved | 24392 | 30 | 293 | 10 | 24725 |
| failed | 35 | 2073 | 81 | 3 | 2192 |
| cap | 3 | 0 | 15 | 0 | 18 |

| kind | programs | VCs | proved by both | only z3 | only cvc5 | neither | programs z3 proves fully | of those, cvc5 too |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| dafnybench | 8 | 69 | 60 | 3 | 0 | 6 | 5 | 4 |
| kondo | 19 | 1386 | 1376 | 3 | 3 | 4 | 14 | 13 |
| libraries | 77 | 3185 | 3027 | 102 | 16 | 40 | 61 | 48 |
| lit | 1221 | 14670 | 12381 | 150 | 19 | 2120 | 775 | 714 |
| std | 64 | 7625 | 7548 | 75 | 0 | 2 | 62 | 45 |
| all | 1389 | 26935 | 24392 | 333 | 38 | 2172 | 917 | 824 |

## Time on the VCs both prove

cvc5's time over z3's; per program averages each program's own geomean. Intervals resample programs.

| kind | VCs | total | geomean over VCs | per program | cvc5 faster |
|---|---:|---|---|---|---:|
| dafnybench | 60 | +626% [+160%, +682%] | +178% [+96%, +255%] | +176% [+117%, +244%] | 0% |
| kondo | 1376 | +192% [+164%, +262%] | +98% [+83%, +113%] | +90% [+80%, +101%] | 0% |
| libraries | 3027 | +548% [+429%, +711%] | +136% [+84%, +184%] | +118% [+94%, +150%] | 1% |
| lit | 12381 | +347% [+250%, +462%] | +85% [+72%, +97%] | +54% [+50%, +58%] | 2% |
| std | 7548 | +558% [+414%, +664%] | +163% [+111%, +196%] | +139% [+109%, +177%] | 1% |
| all | 24392 | +409% [+328%, +497%] | +114% [+93%, +133%] | +62% [+58%, +66%] | 1% |

Of the 24725 VCs z3 proves, the share each variant proves within a given time:

| within | z3 | cvc5 |
|---|---:|---:|
| 1 s | 99.4% | 94.0% |
| 5 s | 99.8% | 97.1% |
| 10 s | 99.9% | 97.8% |
| 30 s | 100.0% | 98.4% |
| 60 s | 100.0% | 98.7% |

## VCs only cvc5 proves (38)

A VC that z3 *fails* quickly and cvc5 proves deserves a look: in a test that expects an error there, it would mean that cvc5 proves something false.

| job | VC | z3 | cvc5 |
|---|---|---|---|
| kondo/paxos/sync | Impl__PaxosProof.__default.InvNextLeaderReceivedPromisesImpliesAcceptorState_split0 | cap 60.0 s | 6.3 s |
| kondo/paxos/sync | Impl__PaxosProof.__default.InvNextLearnerReceivedAcceptImpliesAccepted_split0 | cap 60.0 s | 28.6 s |
| lit/dafny2/SnapshotableTrees.dfy:refresh | Impl__SnapTree.Iterator.Push_split12 | cap 60.0 s | 0.8 s |
| kondo/shardedKv/sync | Impl__ShardedKVProof.__default.InvNextSafety_split0 | failed 0.7 s | 3.6 s |
| libraries/Collections/Sequences/LittleEndianNat.dfy | Impl__LittleEndianNat.__default.LemmaSeqLen1_split0 | failed 0.0 s | 0.1 s |
| libraries/Collections/Sequences/LittleEndianNat.dfy | Impl__LittleEndianNat.__default.LemmaSeqLen2_split0 | failed 0.1 s | 0.6 s |
| libraries/Collections/Sequences/LittleEndianNat.dfy | Impl__LittleEndianNat.__default.LemmaSeqPrefix_split35 | failed 0.1 s | 0.1 s |
| libraries/NonlinearArithmetic/DivMod.dfy | Impl__DivMod.__default.LemmaMultiplyDivideLt_split0 | failed 0.2 s | 25.8 s |
| libraries/NonlinearArithmetic/Internals/ModInternals.dfy | Impl__ModInternals.__default.LemmaDivAddDenominator_split0 | failed 0.1 s | 6.5 s |
| libraries/NonlinearArithmetic/Internals/ModInternals.dfy | Impl__ModInternals.__default.LemmaDivSubDenominator_split0 | failed 0.1 s | 0.3 s |
| libraries/NonlinearArithmetic/Internals/ModInternals.dfy | Impl__ModInternals.__default.LemmaModAddDenominator_split0 | failed 0.0 s | 0.6 s |
| libraries/NonlinearArithmetic/Internals/ModInternals.dfy | Impl__ModInternals.__default.LemmaModSubDenominator_split0 | failed 0.0 s | 0.3 s |
| libraries/NonlinearArithmetic/Mul.dfy | Impl__Mul.__default.LemmaMulOrderingAuto_split0 | failed 0.0 s | 0.1 s |
| libraries/dafny/Collections/LittleEndianNat.dfy | Impl__Dafny_mCollections_mLittleEndianNat.__default.LemmaSeqLen1_split0 | failed 0.0 s | 0.1 s |
| libraries/dafny/Collections/LittleEndianNat.dfy | Impl__Dafny_mCollections_mLittleEndianNat.__default.LemmaSeqLen2_split0 | failed 0.1 s | 0.6 s |
| libraries/dafny/Collections/LittleEndianNat.dfy | Impl__Dafny_mCollections_mLittleEndianNat.__default.LemmaSeqPrefix_split35 | failed 0.1 s | 0.2 s |
| libraries/dafny/NonlinearArithmetic/Internals/ModInternals.dfy | Impl__Dafny_mModInternals.__default.LemmaDivAddDenominator_split0 | failed 0.0 s | 46.6 s |
| libraries/dafny/NonlinearArithmetic/Internals/ModInternals.dfy | Impl__Dafny_mModInternals.__default.LemmaDivSubDenominator_split0 | failed 0.1 s | 0.2 s |
| libraries/dafny/NonlinearArithmetic/Internals/ModInternals.dfy | Impl__Dafny_mModInternals.__default.LemmaModSubDenominator_split0 | failed 0.1 s | 0.2 s |
| libraries/dafny/NonlinearArithmetic/Multiply.dfy | Impl__Dafny_mMultiply.__default.LemmaMulOrderingAuto_split0 | failed 0.0 s | 0.1 s |
| lit/HigherOrderIntrinsicSpecification/ReadPreconditionBypass1.dfy:refresh | Impl___module.__default.Main_split0 | failed 0.1 s | 0.4 s |
| lit/HigherOrderIntrinsicSpecification/ReadPreconditionBypass2.dfy:refresh | Impl___module.__default.Main_split0 | failed 0.1 s | 0.8 s |
| lit/HigherOrderIntrinsicSpecification/ReadPreconditionBypass3.dfy:refresh | Impl___module.__default.Main_split0 | failed 0.1 s | 1.3 s |
| lit/HigherOrderIntrinsicSpecification/ReadPreconditionBypass4.dfy:refresh | Impl___module.__default.M2_split0 | failed 0.1 s | 1.7 s |
| lit/HigherOrderIntrinsicSpecification/ReadPreconditionBypass4.dfy:refresh | Impl___module.__default.M_split0 | failed 0.1 s | 1.5 s |
| lit/dafny0/DefiniteAssignment.dfy:refresh | Impl__AssignSuchThatReference.__default.BadCompiled1_split0 | failed 0.0 s | 0.1 s |
| lit/dafny0/Fuel.dfy:refresh | Impl__TestModule2.__default.test3_split0 | failed 0.0 s | 0.1 s |
| lit/dafny0/Fuel.dfy:refresh | Impl__TestModule4.__default.test3_split0 | failed 0.0 s | 0.2 s |
| lit/dafny0/Fuel.dfy:refresh | Impl__TestModule4.__default.test4_split0 | failed 0.1 s | 0.1 s |
| lit/dafny0/FunctionSpecifications.dfy:refresh | CheckWellformed___module.__default.GoodPost_split0 | failed 56.6 s | 0.1 s |
| lit/dafny0/IndexIntoUpdate.dfy:refresh | Impl___module.__default.M_split0 | failed 0.0 s | 0.1 s |
| lit/git-issues/git-issue-1163.dfy:refresh | Impl___module.MyClass.SuchThat_split0 | failed 0.0 s | 0.1 s |
| lit/triggers/emptyTrigger.dfy:refresh | Impl___module.__default.M_split0 | failed 0.1 s | 0.1 s |
| lit/triggers/splitting-triggers-recovers-expressivity.dfy:refresh | Impl___module.__default.exists__0_split0 | failed 0.1 s | 0.1 s |
| lit/triggers/splitting-triggers-recovers-expressivity.dfy:refresh | Impl___module.__default.forall__0_split0 | failed 0.0 s | 0.1 s |
| lit/wishlist/git-issue-6158.dfy:refresh | Impl___module.__default.MMM_split0 | failed 0.1 s | 14.5 s |
| lit/wishlist/sequences-literals.dfy:refresh | Impl___module.__default.LargeList0_split0 | failed 0.1 s | 6.0 s |
| lit/wishlist/sequences-literals.dfy:refresh | Impl___module.__default.LargeList4_split0 | failed 0.1 s | 10.5 s |

## VCs only z3 proves (333), by how cvc5 ends

| cvc5 | VCs | median z3 time | programs |
|---|---:|---:|---:|
| failed | 30 | 0.05 s | 17 |
| cap | 293 | 0.12 s | 113 |
| missing | 10 | 0.05 s | 8 |

Programs with the most such VCs:

- std/Actions/Producers.dfy: 19
- libraries/dafny/NonlinearArithmetic/DivMod.dfy: 13
- libraries/NonlinearArithmetic/DivMod.dfy: 11
- libraries/Collections/Sequences/LittleEndianNat.dfy: 10
- libraries/dafny/Collections/LittleEndianNat.dfy: 10
- std/Arithmetic/DivMod.dfy: 10
- lit/concurrency/12-MutexLifetime-short.dfy: 8
- lit/dafny0/StatementExpressions.dfy: 8
- lit/dafny1/Induction.legacy.dfy: 8
- std/Base64.dfy: 8
- libraries/NonlinearArithmetic/Power.dfy: 6
- libraries/dafny/NonlinearArithmetic/Power.dfy: 6
- lit/git-issues/git-issue-1619.dfy: 6
- lit/git-issues/git-issue-3855.dfy: 6
- std/Arithmetic/Internal/ModInternals.dfy: 6

