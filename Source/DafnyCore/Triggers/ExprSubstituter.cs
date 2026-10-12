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
      if (TryGetExprSubst(expr, out var ie)) {
        Contract.Assert(ie != null);
        if (quantifierDepth == 1) {
          usedAtTop.Add(ie);
        }
        return ie;
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

        // Each quantifier binds its own copies of the new variables, since nested quantifiers may bind the same ones
        var copies = new Dictionary<IVariable, Expression>();
        var variables = usedSubstMap.ConvertAll(entry => {
          var copy = new IdentifierExpr(entry.Item2.Origin, new BoundVar(entry.Item2.Var.Origin, entry.Item2.Var.Name, entry.Item2.Var.Type));
          copies.Add(entry.Item2.Var, copy);
          return copy;
        });
        var renamer = new Substituter(null, copies, new Dictionary<TypeParameter, Type>());
        newRange = newRange == null ? null : renamer.Substitute(newRange);
        newTerm = renamer.Substitute(newTerm);
        newAttrs = renamer.SubstAttributes(newAttrs);
        newBounds = [.. renamer.SubstituteBoundedPoolList(newBounds)];

        // conjoin all the new equalities to the range of the quantifier
        for (var i = 0; i < usedSubstMap.Count; i++) {
          var eq = new BinaryExpr(e.Origin, BinaryExpr.ResolvedOpcode.EqCommon, variables[i], usedSubstMap[i].Item1);
          newRange = newRange == null ? eq : new BinaryExpr(e.Origin, BinaryExpr.ResolvedOpcode.And, eq, newRange);
          newBoundVars.Add((BoundVar)variables[i].Var);
          newBounds.Add(new ExactBoundedPool(usedSubstMap[i].Item1));
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