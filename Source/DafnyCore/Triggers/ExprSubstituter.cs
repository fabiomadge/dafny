using System;
using System.Collections.Generic;
using System.Diagnostics.Contracts;
using System.Linq;

namespace Microsoft.Dafny {
  /// <summary>
  /// Replaces the terms that the matching-loop rewrite names by new variables of the innermost quantifier being
  /// rewritten around them. The variable v of a term t is defined next to each formula A that the quantifier's body
  /// reaches through connectives and that contains t: as "v == t ==> A" where A is positive in a forall or negative in
  /// an exists, and as "v == t && A" otherwise. For any other value of v, that makes a forall's body only weaker and an
  /// exists's only stronger, so the quantifier keeps its meaning, and it evaluates t where it did if A evaluates t
  /// whenever A is evaluated.
  /// </summary>
  public class ExprSubstituter : Substituter {
    readonly List<Tuple<Expression, IdentifierExpr>> exprSubstMap;
    readonly DafnyOptions options;
    readonly Stack<Frame> frames = new();
    // The variables in scope in the body of the innermost quantifier being rewritten
    readonly HashSet<IVariable> inScope = [];

    private class Frame {
      public bool Universal;
      // The new variables that the quantifier binds: its own copies, for the terms that it uses itself
      public readonly List<(Tuple<Expression, IdentifierExpr> Entry, IdentifierExpr Variable)> Bound = [];
      // The terms in the formula whose definitions are being collected, each with its first occurrence
      public Dictionary<Tuple<Expression, IdentifierExpr>, Expression> Occurrences;
    }

    /// <summary>
    /// How many occurrences of the terms the substitution replaced
    /// </summary>
    public int Replacements { get; private set; }

    /// <summary>
    /// Whether a replaced term mentions a variable that a binder inside the quantifier binds, other than a quantifier
    /// being rewritten, or occurs where the formula around it does not evaluate it whenever it is evaluated, or in
    /// another state
    /// </summary>
    public bool Failed { get; private set; }

    public ExprSubstituter(List<Tuple<Expression, IdentifierExpr>> exprSubstMap, DafnyOptions options)
      : base(null, new Dictionary<IVariable, Expression>(), new Dictionary<TypeParameter, Type>()) {
      this.exprSubstMap = exprSubstMap;
      this.options = options;
    }

    private Tuple<Expression, IdentifierExpr> Named(Expression expr) {
      return exprSubstMap.Find(x => Triggers.ExprExtensions.ExpressionEq(expr, x.Item1));
    }

    public override Expression Substitute(Expression expr) {
      var named = Named(expr);
      if (named != null) {
        Failed |= !FreeVariablesUtil.ComputeFreeVariables(options, expr).IsSubsetOf(inScope);
        Replacements++;
        var frame = frames.Peek();
        var variable = frame.Bound.Find(b => b.Entry == named).Variable;
        if (variable == null) {
          variable = new IdentifierExpr(named.Item2.Origin, new BoundVar(named.Item2.Var.Origin, named.Item2.Var.Name, named.Item2.Var.Type));
          frame.Bound.Add((named, variable));
        }
        frame.Occurrences?.TryAdd(named, expr);
        return variable;
      }
      if (expr is QuantifierExpr e) {
        var replacements = Replacements;
        var renaming = substMap.Count != 0;
        // A new variable that a nested quantifier with triggers of its own bound would not occur in them, so its terms
        // refer to the new variables of the quantifier around it
        var result = frames.Count != 0 && HasTriggers(e) ? base.Substitute(e) : Rewrite(e);
        // A nested quantifier in which nothing changes stays the same object, so it keeps the triggers that the trigger
        // generator selects for it later
        return frames.Count != 0 && Replacements == replacements && !renaming ? e : result;
      }
      return base.Substitute(expr);
    }

    private static bool HasTriggers(QuantifierExpr quantifier) {
      return Attributes.Contains(quantifier.Attributes, "trigger");
    }

    private Expression Rewrite(QuantifierExpr e) {
      if (frames.Count == 0) {
        inScope.UnionWith(FreeVariablesUtil.ComputeFreeVariables(options, e));
      }
      inScope.UnionWith(e.BoundVars);
      var frame = new Frame { Universal = e is ForallExpr };
      frames.Push(frame);
      var newAttrs = SubstAttributes(e.Attributes);
      // A forall's range is an antecedent of its term, and an exists's range a conjunct
      var newRange = e.Range == null ? null : Formula(e.Range, !frame.Universal);
      var newTerm = Formula(e.Term, true);
      frames.Pop();
      inScope.ExceptWith(e.BoundVars);
      if (newAttrs == e.Attributes && newRange == e.Range && newTerm == e.Term) {
        return e;
      }

      var newBoundVars = new List<BoundVar>(e.BoundVars);
      var newBounds = e.Bounds == null ? new List<BoundedPool>() : new List<BoundedPool>(e.Bounds);
      foreach (var (entry, variable) in frame.Bound) {
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

    /// <summary>
    /// Substitutes in a formula that is positive or negative in the body of the innermost quantifier being rewritten
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
            var test = Substitute(ite.Test);
            var thn = Formula(ite.Thn, positive);
            var els = Formula(ite.Els, positive);
            return test == ite.Test && thn == ite.Thn && els == ite.Els ? expr : new ITEExpr(ite.Origin, false, test, thn, els) { Type = Type.Bool };
          }
        case QuantifierExpr { SplitQuantifier: not null } split when HasTriggers(split): {
            // The verifier translates its parts, which have its triggers
            var parts = Formula(split.SplitQuantifierExpression, positive);
            return parts == split.SplitQuantifierExpression ? expr : parts;
          }
        case QuantifierExpr quantifier when HasTriggers(quantifier): {
            var newAttrs = SubstAttributes(quantifier.Attributes);
            var newRange = quantifier.Range == null ? null : Formula(quantifier.Range, quantifier is ForallExpr ? !positive : positive);
            var newTerm = Formula(quantifier.Term, positive);
            if (newAttrs == quantifier.Attributes && newRange == quantifier.Range && newTerm == quantifier.Term) {
              return expr;
            }
            QuantifierExpr copy = quantifier is ForallExpr
              ? new ForallExpr(quantifier.Origin, quantifier.BoundVars, newRange, newTerm, newAttrs)
              : new ExistsExpr(quantifier.Origin, quantifier.BoundVars, newRange, newTerm, newAttrs);
            copy.Bounds = quantifier.Bounds;
            copy.Type = quantifier.Type;
            return copy;
          }
        default:
          return Atom(expr, positive);
      }
    }

    /// <summary>
    /// Substitutes in a formula that the connectives end at, and defines next to it the new variables of its terms
    /// </summary>
    private Expression Atom(Expression expr, bool positive) {
      var frame = frames.Peek();
      CheckOccurrences(expr, true);
      frame.Occurrences = new();
      var result = Substitute(expr);
      var occurrences = frame.Occurrences;
      frame.Occurrences = null;
      Expression definitions = null;
      foreach (var (entry, occurrence) in occurrences) {
        var variable = frame.Bound.Find(b => b.Entry == entry).Variable;
        var definition = new BinaryExpr(occurrence.Origin, BinaryExpr.ResolvedOpcode.EqCommon, variable, occurrence);
        definitions = definitions == null ? definition : Expression.CreateAnd(definitions, definition, false);
      }
      if (definitions == null) {
        return result;
      }
      return frame.Universal == positive ? Expression.CreateImplies(definitions, result, false) : Expression.CreateAnd(definitions, result, false);
    }

    /// <summary>
    /// Fails if a term occurs in the formula where the formula does not evaluate it whenever it is evaluated, or in
    /// another state
    /// </summary>
    private void CheckOccurrences(Expression expr, bool unconditional) {
      if (Named(expr) != null) {
        Failed |= !unconditional;
        return;
      }
      switch (expr) {
        case ConcreteSyntaxExpression { ResolvedExpression: { } resolved }:
          CheckOccurrences(resolved, unconditional);
          return;
        case QuantifierExpr quantifier when !HasTriggers(quantifier):
          // Rewritten as a quantifier of its own
          return;
        case ITEExpr ite:
          CheckOccurrences(ite.Test, unconditional);
          CheckOccurrences(ite.Thn, false);
          CheckOccurrences(ite.Els, false);
          return;
        case BinaryExpr { ResolvedOp: BinaryExpr.ResolvedOpcode.And or BinaryExpr.ResolvedOpcode.Or or BinaryExpr.ResolvedOpcode.Imp } binary:
          CheckOccurrences(binary.E0, unconditional);
          CheckOccurrences(binary.E1, false);
          return;
        case LetExpr { Exact: true } let:
          foreach (var rhs in let.RHSs) {
            CheckOccurrences(rhs, unconditional);
          }
          CheckOccurrences(let.Body, unconditional);
          return;
      }
      var inner = unconditional && expr is not (ComprehensionExpr or OldExpr or StmtExpr or MatchExpr or NestedMatchExpr or
        LetExpr or UnchangedExpr or FreshExpr or DecreasesToExpr);
      foreach (var sub in expr.SubExpressions) {
        CheckOccurrences(sub, inner);
      }
    }

    private bool Mentions(Expression expr) {
      return Named(expr) != null || expr.SubExpressions.Any(Mentions);
    }
  }
}
