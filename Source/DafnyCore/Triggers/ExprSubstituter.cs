using System;
using System.Collections.Generic;
using System.Diagnostics.Contracts;

namespace Microsoft.Dafny {
  public class ExprSubstituter : Substituter {
    readonly List<Tuple<Expression, IdentifierExpr>> exprSubstMap;
    List<Tuple<Expression, IdentifierExpr>> usedSubstMap;
    readonly DafnyOptions options;
    // The range defines a new variable in the current state, so it cannot stand for a term that reads the heap in old.
    bool inOld;

    public ExprSubstituter(List<Tuple<Expression, IdentifierExpr>> exprSubstMap, DafnyOptions options)
      : base(null, new Dictionary<IVariable, Expression>(), new Dictionary<TypeParameter, Type>()) {
      this.exprSubstMap = exprSubstMap;
      this.options = options;
      this.usedSubstMap = [];
    }

    public bool TryGetExprSubst(Expression expr, out IdentifierExpr ie) {
      var entry = usedSubstMap.Find(x => Triggers.ExprExtensions.ExpressionEq(expr, x.Item1));
      if (entry != null) {
        ie = entry.Item2;
        return true;
      }
      entry = exprSubstMap.Find(x => Triggers.ExprExtensions.ExpressionEq(expr, x.Item1));
      if (entry != null) {
        usedSubstMap.Add(entry);
        ie = entry.Item2;
        return true;
      } else {
        ie = null;
        return false;
      }
    }

    public override Expression Substitute(Expression expr) {
      if (!(inOld && ReadsHeap(expr)) && TryGetExprSubst(expr, out var ie)) {
        Contract.Assert(ie != null);
        return ie;
      }
      if (expr is OldExpr && !inOld) {
        inOld = true;
        try {
          return base.Substitute(expr);
        }
        finally {
          inOld = false;
        }
      }
      if (expr is QuantifierExpr e) {
        var newAttrs = SubstAttributes(e.Attributes);
        var newRange = e.Range == null ? null : Substitute(e.Range);
        var newTerm = Substitute(e.Term);
        var newBounds = SubstituteBoundedPoolList(e.Bounds);
        if (newAttrs == e.Attributes && newRange == e.Range && newTerm == e.Term && newBounds == e.Bounds) {
          return e;
        }

        var newBoundVars = new List<BoundVar>(e.BoundVars);
        if (newBounds == null) {
          newBounds = [];
        } else if (newBounds == e.Bounds) {
          // create a new list with the same elements, since the .Add operations below would otherwise add elements to the original e.Bounds
          newBounds = [.. newBounds];
        }

        // conjoin all the new equalities to the range of the quantifier
        foreach (var entry in usedSubstMap) {
          var eq = new BinaryExpr(e.Origin, BinaryExpr.ResolvedOpcode.EqCommon, entry.Item2, entry.Item1);
          newRange = newRange == null ? eq : new BinaryExpr(e.Origin, BinaryExpr.ResolvedOpcode.And, eq, newRange);
          newBoundVars.Add((BoundVar)entry.Item2.Var);
          newBounds.Add(new ExactBoundedPool(entry.Item1));
        }

        QuantifierExpr newExpr;
        if (expr is ForallExpr) {
          newExpr = new ForallExpr(e.Origin, newBoundVars, newRange, newTerm, newAttrs) { Bounds = newBounds };
        } else {
          Contract.Assert(expr is ExistsExpr);
          newExpr = new ExistsExpr(e.Origin, newBoundVars, newRange, newTerm, newAttrs) { Bounds = newBounds };
        }
        usedSubstMap.Clear();

        newExpr.Type = expr.Type;
        return newExpr;
      }
      return base.Substitute(expr);
    }

    bool ReadsHeap(Expression expr) {
      var usesHeap = false;
      FreeVariablesUtil.ComputeFreeVariables(options, expr, new HashSet<IVariable>(), ref usesHeap);
      return usesHeap;
    }
  }
}