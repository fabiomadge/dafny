using System;
using System.Collections.Generic;
using System.Diagnostics.Contracts;

namespace Microsoft.Dafny {
  public class ExprSubstituter : Substituter {
    readonly List<Tuple<Expression, IdentifierExpr>> exprSubstMap;
    // For each quantifier being substituted into, outermost first, the replaced terms whose variables it binds
    readonly List<List<Tuple<Expression, IdentifierExpr>>> usedSubstMaps = [];

    public ExprSubstituter(List<Tuple<Expression, IdentifierExpr>> exprSubstMap)
      : base(null, new Dictionary<IVariable, Expression>(), new Dictionary<TypeParameter, Type>()) {
      this.exprSubstMap = exprSubstMap;
    }

    public bool TryGetExprSubst(Expression expr, out IdentifierExpr ie) {
      var entry = exprSubstMap.Find(x => Triggers.ExprExtensions.ExpressionEq(expr, x.Item1));
      // The innermost quantifier binds the variable, unless it or an enclosing one already does
      if (entry != null && !usedSubstMaps.Exists(used => used.Contains(entry))) {
        usedSubstMaps[^1].Add(entry);
      }
      ie = entry?.Item2;
      return entry != null;
    }

    public override Expression Substitute(Expression expr) {
      if (TryGetExprSubst(expr, out var ie)) {
        Contract.Assert(ie != null);
        return ie;
      }
      if (expr is QuantifierExpr e) {
        usedSubstMaps.Add([]);
        var newAttrs = SubstAttributes(e.Attributes);
        var newRange = e.Range == null ? null : Substitute(e.Range);
        var newTerm = Substitute(e.Term);
        var usedSubstMap = usedSubstMaps[^1];
        usedSubstMaps.RemoveAt(usedSubstMaps.Count - 1);
        if (newAttrs == e.Attributes && newRange == e.Range && newTerm == e.Term) {
          return e;
        }

        var newBoundVars = new List<BoundVar>(e.BoundVars);
        // Not substituted: a variable's bound must not mention later variables, and the added ones come last.
        var newBounds = new List<BoundedPool>(e.Bounds ?? []);

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

        newExpr.Type = expr.Type;
        return newExpr;
      }
      return base.Substitute(expr);
    }
  }
}