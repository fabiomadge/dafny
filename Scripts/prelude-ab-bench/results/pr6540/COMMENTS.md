# Draft review: dafny-lang/dafny#6540 at `c61bf8b9a` (Comment; already approved, nothing blocking)

## Body

The description's scope is too narrow. Every single-constructor datatype was affected, because
Boogie's constructor functions are total. For example, take `datatype S = S(n: nat)` and a value `A`
of another datatype. Master's axioms refute both `S#Equal(A, S(S.n(A)))` and its negation; with this
PR, only the term itself.

Description and commit message: a minimal version with the corrected scope is at https://github.com/fabiomadge/dafny/blob/review-pr6539-bench/Scripts/prelude-ab-bench/results/pr6540/REVIEW.md#suggested-title-commit-message-and-description.

## Inline

### `Source/DafnyCore/Verifier/Datatypes/BoogieGenerator.DataTypes.cs`, lines 81–84

Worth saying why the first conjunct stays unguarded, so that nobody folds it into the general case:

```suggestion
    /// Dt#Equal is equality (see AddExtensionalityAxiom), so the first conjunct holds of all values and needs
    /// no antecedent (one makes tuple proofs far costlier, e.g. Std's LittleEndianNat.LemmaSeqAdd). The second
    /// one does: a and b range over all of DatatypeType, the sort that every datatype shares, and without the
    /// antecedent it would make equal any two values, of any datatypes, whose projections agree.
```

### `Source/DafnyCore/Verifier/Datatypes/BoogieGenerator.DataTypes.cs`, line 126

`dt.Ctors.Count == 1` is tested twice, here and at line 109. One `if`/`else` after `eqs` reads
better and generates the same Boogie:

```csharp
        Bpl.Trigger trigger;
        Bpl.Expr body;
        if (dt.Ctors.Count == 1) {
          trigger = BplTrigger(dtEqual);
          body = BplAnd(BplImp(dtEqual, eqs), BplImp(BplAnd(ante, eqs), dtEqual));
        } else {
          trigger = new Bpl.Trigger(ctor.Origin, true, new List<Bpl.Expr> { dtEqual, ctorQa },
            new Bpl.Trigger(ctor.Origin, true, new List<Bpl.Expr> { dtEqual, ctorQb }));
          body = BplImp(ante, BplIff(dtEqual, eqs));
        }
```

### `Source/IntegrationTests/TestFiles/LitTests/LitTest/git-issues/git-issue-6531.dfy`, lines 4–7

`Contradiction` (lines 31–34) tests nothing: it follows from `Bad`'s specification under any
prelude. The `forall` statement and `{:induction false}` do matter: without either, master no
longer proves `Bad`. Suggest dropping `Contradiction` and saying that here:

```suggestion
// Bad's postcondition is false. The old equality axiom of Unit held of any two datatype values, and
// proved it. Keep the forall statement and {:induction false}: without either, it no longer does.
```
