using System;
using System.Collections.Generic;
using System.Diagnostics.Contracts;

namespace Microsoft.Dafny {
  public class ExprSubstituter : Substituter {
    readonly List<Tuple<Expression, IdentifierExpr>> exprSubstMap;
    readonly DafnyOptions options;
    // For each quantifier being rewritten, the new variables that it binds: its own copies, for the terms that it uses
    // itself
    readonly Stack<List<(Tuple<Expression, IdentifierExpr> Entry, IdentifierExpr Variable)>> boundHere = new();
    // The variables in scope in the range of the innermost quantifier being rewritten
    readonly HashSet<IVariable> inScope = [];

    /// <summary>
    /// How many occurrences of the terms the substitution replaced
    /// </summary>
    public int Replacements { get; private set; }

    /// <summary>
    /// Whether a replaced term mentions a variable that a binder inside the quantifier binds, other than a quantifier
    /// being rewritten, so that no range where a new variable is defined has it in scope
    /// </summary>
    public bool Failed { get; private set; }

    public ExprSubstituter(List<Tuple<Expression, IdentifierExpr>> exprSubstMap, DafnyOptions options)
      : base(null, new Dictionary<IVariable, Expression>(), new Dictionary<TypeParameter, Type>()) {
      this.exprSubstMap = exprSubstMap;
      this.options = options;
    }

    public override Expression Substitute(Expression expr) {
      var named = exprSubstMap.Find(x => Triggers.ExprExtensions.ExpressionEq(expr, x.Item1));
      if (named != null) {
        Failed |= !FreeVariablesUtil.ComputeFreeVariables(options, expr).IsSubsetOf(inScope);
        Replacements++;
        var here = boundHere.Peek();
        var variable = here.Find(b => b.Entry == named).Variable;
        if (variable == null) {
          variable = new IdentifierExpr(named.Item2.Origin, new BoundVar(named.Item2.Var.Origin, named.Item2.Var.Name, named.Item2.Var.Type));
          here.Add((named, variable));
        }
        return variable;
      }
      if (expr is QuantifierExpr e) {
        var replacements = Replacements;
        var renaming = substMap.Count != 0;
        // A new variable that a nested quantifier with triggers of its own bound would not occur in them, so its terms
        // refer to the new variables of the quantifier around it
        var result = boundHere.Count != 0 && Attributes.Contains(e.Attributes, "trigger") ? base.Substitute(e) : Rewrite(e);
        // A nested quantifier in which nothing changes stays the same object, so it keeps the triggers that the trigger
        // generator selects for it later
        return boundHere.Count != 0 && Replacements == replacements && !renaming ? e : result;
      }
      return base.Substitute(expr);
    }

    private Expression Rewrite(QuantifierExpr e) {
      if (boundHere.Count == 0) {
        inScope.UnionWith(FreeVariablesUtil.ComputeFreeVariables(options, e));
      }
      inScope.UnionWith(e.BoundVars);
      boundHere.Push([]);
      var newAttrs = SubstAttributes(e.Attributes);
      var newRange = e.Range == null ? null : Substitute(e.Range);
      var newTerm = Substitute(e.Term);
      var newBounds = SubstituteBoundedPoolList(e.Bounds);
      var bound = boundHere.Pop();
      inScope.ExceptWith(e.BoundVars);
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
      if (e is ForallExpr) {
        newExpr = new ForallExpr(e.Origin, newBoundVars, newRange, newTerm, newAttrs) { Bounds = newBounds };
      } else {
        Contract.Assert(e is ExistsExpr);
        newExpr = new ExistsExpr(e.Origin, newBoundVars, newRange, newTerm, newAttrs) { Bounds = newBounds };
      }

      newExpr.Type = e.Type;
      return newExpr;
    }
  }
}
