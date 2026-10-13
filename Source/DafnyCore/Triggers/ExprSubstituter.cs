using System;
using System.Collections.Generic;
using System.Diagnostics.Contracts;

namespace Microsoft.Dafny {
  public class ExprSubstituter : Substituter {
    readonly List<Tuple<Expression, IdentifierExpr>> exprSubstMap;
    // For each quantifier being rewritten, the new variables that it binds: its own copies, for the terms that it uses
    // itself
    readonly Stack<List<(Tuple<Expression, IdentifierExpr> Entry, IdentifierExpr Variable)>> boundHere = new();

    public ExprSubstituter(List<Tuple<Expression, IdentifierExpr>> exprSubstMap)
      : base(null, new Dictionary<IVariable, Expression>(), new Dictionary<TypeParameter, Type>()) {
      this.exprSubstMap = exprSubstMap;
    }

    public override Expression Substitute(Expression expr) {
      var named = exprSubstMap.Find(x => Triggers.ExprExtensions.ExpressionEq(expr, x.Item1));
      if (named != null) {
        var here = boundHere.Peek();
        var variable = here.Find(b => b.Entry == named).Variable;
        if (variable == null) {
          variable = new IdentifierExpr(named.Item2.Origin, new BoundVar(named.Item2.Var.Origin, named.Item2.Var.Name, named.Item2.Var.Type));
          here.Add((named, variable));
        }
        return variable;
      }
      if (expr is QuantifierExpr e) {
        if (boundHere.Count != 0 && Attributes.Contains(e.Attributes, "trigger")) {
          // The triggers of this nested quantifier would not mention a new variable that it binds
          return e;
        }
        boundHere.Push([]);
        var newAttrs = SubstAttributes(e.Attributes);
        var newRange = e.Range == null ? null : Substitute(e.Range);
        var newTerm = Substitute(e.Term);
        var newBounds = SubstituteBoundedPoolList(e.Bounds);
        var bound = boundHere.Pop();
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
        foreach (var (entry, variable) in bound) {
          var eq = new BinaryExpr(e.Origin, BinaryExpr.ResolvedOpcode.EqCommon, variable, entry.Item1);
          newRange = newRange == null ? eq : new BinaryExpr(e.Origin, BinaryExpr.ResolvedOpcode.And, eq, newRange);
          newBoundVars.Add((BoundVar)variable.Var);
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