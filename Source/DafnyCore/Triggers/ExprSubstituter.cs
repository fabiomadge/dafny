using System;
using System.Collections.Generic;
using System.Linq;
using Microsoft.Dafny.Triggers;

namespace Microsoft.Dafny {
  /// <summary>
  /// Replaces each occurrence of a term t that the matching-loop rewrite names, as an argument of a trigger term P in a
  /// formula A that the quantifier's body reaches through connectives and quantifiers, by a variable v of a new
  /// quantifier around A that defines v by that occurrence: "forall v {:trigger P[v]} | v == t :: A[v]" if A is
  /// positive in a forall or negative in an exists, and "exists v {:trigger P[v]} | v == t :: A[v]" otherwise. Either
  /// is A, whatever t is, and the choice keeps the new quantifier universal wherever the rewritten one is, so that it
  /// is instantiated only for terms that exist. Its definition evaluates t next to A, and P is its trigger, so they
  /// must mention only variables bound outside A, and a term that may mean something else in another state or outside
  /// its guards must be one that A evaluates whenever A is evaluated.
  /// </summary>
  public class ExprSubstituter : Substituter {
    readonly List<Tuple<Expression, IdentifierExpr>> exprSubstMap;
    // The terms that may mean something else in another state or outside their guards
    readonly ISet<Tuple<Expression, IdentifierExpr>> local;
    readonly TriggersCollector triggersCollector;
    readonly DafnyOptions options;
    bool universal;
    // In the formula being substituted, the occurrences to replace and the trigger terms that they are arguments of, as
    // the check found them, then their new variables and the trigger terms with them
    readonly HashSet<Expression> occurrences = [];
    readonly HashSet<Expression> parents = [];
    readonly List<(BoundVar Variable, Expression Occurrence)> variables = [];
    readonly List<Expression> triggerTerms = [];

    /// <summary>
    /// How many occurrences of the terms the substitution replaced
    /// </summary>
    public int Replacements { get; private set; }

    /// <summary>
    /// Whether a trigger term with an occurrence to replace mentions a variable bound inside the formula around it, or
    /// an occurrence is of a term that may mean something else in another state or outside its guards and that formula
    /// does not evaluate it whenever it is evaluated, or in another state
    /// </summary>
    public bool Failed { get; private set; }

    internal ExprSubstituter(List<Tuple<Expression, IdentifierExpr>> exprSubstMap, ISet<Tuple<Expression, IdentifierExpr>> local,
      TriggersCollector triggersCollector, DafnyOptions options)
      : base(null, new Dictionary<IVariable, Expression>(), new Dictionary<TypeParameter, Type>()) {
      this.exprSubstMap = exprSubstMap;
      this.local = local;
      this.triggersCollector = triggersCollector;
      this.options = options;
    }

    private Tuple<Expression, IdentifierExpr> Named(Expression expr) {
      return exprSubstMap.Find(x => ExprExtensions.ExpressionEq(expr, x.Item1));
    }

    /// <summary>
    /// Whether the expression is a trigger term with arguments that the rewrite names and no other arguments that
    /// kill triggers, so that it is a trigger term with the new variables
    /// </summary>
    private bool HasNamedArguments(Expression expr) {
      return triggersCollector.IsPotentialTriggerCandidate(expr) && expr.SubExpressions.Any(e => Named(e) != null) &&
             expr.SubExpressions.All(e => Named(e) != null || !triggersCollector.IsTriggerKiller(e));
    }

    public QuantifierExpr Rewrite(QuantifierExpr e) {
      universal = e is ForallExpr;
      // A forall's range is an antecedent of its term, and an exists's range a conjunct
      var range = e.Range == null ? null : Formula(e.Range, !universal);
      var term = Formula(e.Term, true);
      return Copy(e, range, term, TriggerUtils.CopyAttributes(e.Attributes));
    }

    private static QuantifierExpr Copy(QuantifierExpr e, Expression range, Expression term, Attributes attributes) {
      QuantifierExpr copy = e is ForallExpr
        ? new ForallExpr(e.Origin, e.BoundVars, range, term, attributes)
        : new ExistsExpr(e.Origin, e.BoundVars, range, term, attributes);
      copy.Bounds = e.Bounds;
      copy.Type = e.Type;
      return copy;
    }

    /// <summary>
    /// Substitutes in a formula that is positive or negative in the body of the quantifier being rewritten
    /// </summary>
    private Expression Formula(Expression expr, bool positive) {
      switch (expr.Resolved) {
        case UnaryOpExpr { ResolvedOp: UnaryOpExpr.ResolvedOpcode.BoolNot } not: {
            var operand = Formula(not.E, !positive);
            return operand == not.E ? expr : Expression.CreateNot(not.Origin, operand);
          }
        case BinaryExpr { ResolvedOp: BinaryExpr.ResolvedOpcode.And or BinaryExpr.ResolvedOpcode.Or or BinaryExpr.ResolvedOpcode.Imp } binary: {
            var e0 = Formula(binary.E0, binary.ResolvedOp == BinaryExpr.ResolvedOpcode.Imp ? !positive : positive);
            var e1 = Formula(binary.E1, positive);
            return e0 == binary.E0 && e1 == binary.E1 ? expr : new BinaryExpr(binary.Origin, binary.ResolvedOp, e0, e1);
          }
        case ITEExpr { IsBindingGuard: false } ite when !Mentions(ite.Test): {
            var thn = Formula(ite.Thn, positive);
            var els = Formula(ite.Els, positive);
            return thn == ite.Thn && els == ite.Els ? expr : new ITEExpr(ite.Origin, false, ite.Test, thn, els) { Type = Type.Bool };
          }
        case QuantifierExpr { SplitQuantifier: not null } split: {
            // The verifier translates its parts
            var parts = Formula(split.SplitQuantifierExpression, positive);
            return parts == split.SplitQuantifierExpression ? expr : parts;
          }
        case QuantifierExpr quantifier: {
            var range = quantifier.Range == null ? null : Formula(quantifier.Range, quantifier is ForallExpr ? !positive : positive);
            var term = Formula(quantifier.Term, positive);
            return range == quantifier.Range && term == quantifier.Term ? expr : Copy(quantifier, range, term, quantifier.Attributes);
          }
        default:
          return Atom(expr, positive);
      }
    }

    /// <summary>
    /// Substitutes in a formula that the connectives and quantifiers end at, and puts the quantifier for the new
    /// variables around it
    /// </summary>
    private Expression Atom(Expression expr, bool positive) {
      occurrences.Clear();
      parents.Clear();
      variables.Clear();
      triggerTerms.Clear();
      // The trigger generator finds the terms in inlined lets
      var inlined = new LetInliner().Substitute(expr);
      CheckOccurrences(inlined, true, FreeVariablesUtil.ComputeFreeVariables(options, inlined));
      if (occurrences.Count == 0) {
        return expr;
      }
      var result = Substitute(inlined);
      var definitions = variables.Select(x => (Expression)new BinaryExpr(x.Occurrence.Origin, BinaryExpr.ResolvedOpcode.EqCommon,
        new IdentifierExpr(x.Occurrence.Origin, x.Variable), x.Occurrence)).Aggregate((a, b) => Expression.CreateAnd(a, b, false));
      var trigger = new Attributes("trigger", triggerTerms.ToList(), null);
      QuantifierExpr quantifier = universal == positive
        ? new ForallExpr(expr.Origin, variables.ConvertAll(x => x.Variable), definitions, result, trigger)
        : new ExistsExpr(expr.Origin, variables.ConvertAll(x => x.Variable), definitions, result, trigger);
      quantifier.Bounds = variables.ConvertAll(x => (BoundedPool)new ExactBoundedPool(x.Occurrence));
      quantifier.Type = Type.Bool;
      return quantifier;
    }

    public override Expression Substitute(Expression expr) {
      if (occurrences.Contains(expr)) {
        Replacements++;
        var name = Named(expr).Item2.Var.Name;
        while (variables.Exists(x => x.Variable.Name == name)) {
          name += "'";
        }
        var variable = new BoundVar(expr.Origin, name, expr.Type);
        variables.Add((variable, expr));
        return new IdentifierExpr(expr.Origin, variable);
      }
      if (parents.Contains(expr)) {
        var result = base.Substitute(expr);
        triggerTerms.Add(result);
        return result;
      }
      return base.Substitute(expr);
    }

    /// <summary>
    /// Finds the occurrences to replace, and fails if a trigger term with one mentions a variable that is not free in
    /// the formula, or one is of a term that may mean something else in another state or outside its guards and the
    /// formula does not evaluate it whenever it is evaluated, or in another state
    /// </summary>
    private void CheckOccurrences(Expression expr, bool unconditional, ISet<IVariable> free) {
      if (HasNamedArguments(expr)) {
        Failed |= !FreeVariablesUtil.ComputeFreeVariables(options, expr).IsSubsetOf(free);
        foreach (var argument in expr.SubExpressions) {
          var named = Named(argument);
          if (named == null) {
            CheckOccurrences(argument, unconditional, free);
          } else {
            Failed |= !unconditional && local.Contains(named);
            occurrences.Add(argument);
          }
        }
        parents.Add(expr);
        return;
      }
      switch (expr) {
        case ConcreteSyntaxExpression { ResolvedExpression: { } resolved }:
          CheckOccurrences(resolved, unconditional, free);
          return;
        case ITEExpr ite:
          CheckOccurrences(ite.Test, unconditional, free);
          CheckOccurrences(ite.Thn, false, free);
          CheckOccurrences(ite.Els, false, free);
          return;
        case BinaryExpr { ResolvedOp: BinaryExpr.ResolvedOpcode.And or BinaryExpr.ResolvedOpcode.Or or BinaryExpr.ResolvedOpcode.Imp } binary:
          CheckOccurrences(binary.E0, unconditional, free);
          CheckOccurrences(binary.E1, false, free);
          return;
      }
      var inner = unconditional && expr is not (ComprehensionExpr or OldExpr or StmtExpr or MatchExpr or NestedMatchExpr or
        LetExpr or UnchangedExpr or FreshExpr or DecreasesToExpr);
      foreach (var sub in expr.SubExpressions) {
        CheckOccurrences(sub, inner, free);
      }
    }

    private bool Mentions(Expression expr) {
      return Named(expr) != null || expr.SubExpressions.Any(Mentions);
    }

    /// <summary>
    /// Inlines the lets that the trigger generator inlines whose right-hand sides mean the same in every state and
    /// outside their guards, so that they mean the same wherever the inlining puts them
    /// </summary>
    private class LetInliner : Substituter {
      public LetInliner() : base(null, new Dictionary<IVariable, Expression>(), new Dictionary<TypeParameter, Type>()) {
      }

      public override Expression Substitute(Expression expr) {
        return expr is LetExpr { Exact: true } let && let.LHSs.All(p => p.Var != null) &&
               let.RHSs.All(SplitPartTriggerWriter.CanBeNamed)
          ? Substitute(BoogieGenerator.InlineLet(let))
          : base.Substitute(expr);
      }
    }
  }
}
