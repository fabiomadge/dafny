# Draft review: dafny-lang/dafny#6540 at `c61bf8b9a`

**Event:** Comment (the PR is approved; none of this blocks it)

## Review body

Non-blocking suggestions.

The description's scope is too narrow: the axiom was false for every single-constructor datatype,
not only "whenever the constructor takes every value of its fields' types". Boogie's constructor
functions are total, so `datatype S = S(n: nat)` is refuted the same way: master's axioms plus the
term `S#Equal(X, S(S.n(X)))` are `unsat`.

## Inline comments

### `Source/DafnyCore/Verifier/Datatypes/BoogieGenerator.DataTypes.cs`, lines 81–84

Worth saying why the first conjunct stays unguarded, or someone will fold this case into the
general one:

```suggestion
    /// Dt#Equal is equality (see AddExtensionalityAxiom), so the first conjunct holds of all values and needs
    /// no antecedent; giving it one anyway makes proofs about tuples far costlier (Std's
    /// LittleEndianNat.LemmaSeqAdd runs out of resources). The second one does need it: a and b range over
    /// all of DatatypeType, the sort that every datatype shares, and without the antecedent it would make
    /// equal any two values, of any datatypes, whose projections agree.
```

### `Source/DafnyCore/Verifier/Datatypes/BoogieGenerator.DataTypes.cs`, line 126

`dt.Ctors.Count == 1` is now tested twice, at line 109 for the trigger and here for the body. One
`if`/`else` after `eqs` computes both and reads as the two cases. The generated Boogie is the same
byte for byte:

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

`Contradiction` tests nothing: it verifies from `Bad`'s specification whatever the axiom says.
Without it, master still proves `Bad` at 8 of 8 seeds, and this PR refuses it at 8 of 8. What
matters is the `forall` statement and `{:induction false}`: without either, master no longer proves
`Bad`, so the test would stop detecting the bug. Suggest dropping `Contradiction` (lines 31–34) and
saying that here:

```suggestion
// Bad's postcondition is false; the old equality axiom of Unit, applied to values of R, proved it.
// Keep the forall statement and {:induction false}: without either, the old axiom no longer proves it.
```
