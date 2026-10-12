using System;
using System.Collections.Generic;
using System.Diagnostics.Contracts;
using System.Linq;

namespace Microsoft.Dafny {
  public class ExprSubstituter : Substituter {
    readonly List<Tuple<Expression, IdentifierExpr>> exprSubstMap;
    List<Tuple<Expression, IdentifierExpr>> usedSubstMap;
    // The variables used in the rewritten quantifier itself rather than in a nested one
    readonly HashSet<IdentifierExpr> usedAtTop = [];
    int quantifierDepth;
    // Inside old or a lambda, a term is read in another state than the range, which defines the new variables
    int inOtherState;

    public ExprSubstituter(List<Tuple<Expression, IdentifierExpr>> exprSubstMap)
      : base(null, new Dictionary<IVariable, Expression>(), new Dictionary<TypeParameter, Type>()) {
      this.exprSubstMap = exprSubstMap;
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
      if (inOtherState == 0 && TryGetExprSubst(expr, out var ie)) {
        Contract.Assert(ie != null);
        if (quantifierDepth == 1) {
          usedAtTop.Add(ie);
        }
        return ie;
      }
      if (expr is OldExpr or LambdaExpr) {
        inOtherState++;
        try {
          return base.Substitute(expr);
        }
        finally {
          inOtherState--;
        }
      }
      if (expr is QuantifierExpr e) {
        quantifierDepth++;
        var newAttrs = SubstAttributes(e.Attributes);
        var newRange = e.Range == null ? null : Substitute(e.Range);
        var newTerm = Substitute(e.Term);
        var newBounds = SubstituteBoundedPoolList(e.Bounds);
        quantifierDepth--;
        if (quantifierDepth == 0) {
          // A nested quantifier binds the variables used so far and removes them from usedSubstMap
          usedSubstMap.AddRange(exprSubstMap.Where(entry => usedAtTop.Contains(entry.Item2) && !usedSubstMap.Contains(entry)).ToList());
        }
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
  }
}