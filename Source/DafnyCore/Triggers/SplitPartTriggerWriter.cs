using System;
using System.Collections.Generic;
using System.Diagnostics.Contracts;
using System.Linq;

namespace Microsoft.Dafny.Triggers;

/// <summary>
/// Determines the triggers for a comprehension that resulted from splitting another one
/// </summary>
class SplitPartTriggerWriter {
  public ComprehensionExpr Comprehension { get; set; }
  public List<TriggerTerm> CandidateTerms { get; set; }
  public List<TriggerCandidate> Candidates { get; set; }
  private List<TriggerCandidate> RejectedCandidates { get; }
  public List<Tuple<Expression, IdentifierExpr>> NamedExpressions { get; }
  private List<TriggerMatch> loopingMatches;

  private bool AllowsLoops {
    get {
      // This is different from nowarn: it won't remove loops at all, even if another trigger is available.
      return Attributes.Contains(Comprehension.Attributes, "matchingloop");
    }
  }

  private bool CouldSuppressLoops { get; set; }

  internal SplitPartTriggerWriter(ComprehensionExpr comprehension) {
    this.Comprehension = comprehension;
    this.RejectedCandidates = [];
    this.NamedExpressions = [];
  }

  internal bool BreaksLoops => NeedsAutoTriggers() && WantsMatchingLoopRewrite();

  internal void TrimInvalidTriggers() {
    Contract.Requires(CandidateTerms != null);
    Contract.Requires(Candidates != null);
    Candidates = Candidates.Where(tr => tr.MentionsAll(Comprehension.BoundVars)).ToList();
  }

  public bool DetectAndFilterLoopingCandidates(ErrorReporter reporter) {
    var looping = new List<TriggerCandidate>();
    var loopingMatches = new List<TriggerMatch>();

    var nonLoopingCandidates = new List<TriggerCandidate>();
    foreach (var candidate in Candidates) {
      var loopingSubterms = candidate.LoopingSubterms(Comprehension, reporter.Options).ToList();
      if (loopingSubterms.Any()) {
        looping.Add(candidate);
        loopingMatches = loopingSubterms.ToList();
        candidate.Annotation = "may loop with " + string.Join(", ",
          loopingSubterms.Select(t => "\"" + Printer.ExprToString(reporter.Options, t.OriginalExpr) + "\""));
      } else {
        nonLoopingCandidates.Add(candidate);
      }
    }

    CouldSuppressLoops = nonLoopingCandidates.Count > 0;
    this.loopingMatches = loopingMatches;
    if (!AllowsLoops && CouldSuppressLoops) {
      Candidates = nonLoopingCandidates;
      RejectedCandidates.AddRange(looping);
    }

    return looping.Count > 0;
  }

  // Also names the terms requested of the part's quantifier, and asks the nested quantifiers that the requests have to
  // name others
  public bool RewriteMatchingLoop(ErrorReporter reporter, ModuleDefinition module, List<Expression> requested,
    Dictionary<Expression, List<Expression>> requests) {
    if (!BreaksLoops) {
      return false;
    }

    var triggersCollector = new TriggersCollector(new(),
      reporter.Options, module);
    // rewrite quantifier to avoid matching loops
    // before:
    //    assert forall i :: 0 <= i < a.Length-1 ==> a[i] <= a[i+1];
    // after, in the verifier's translation:
    //    assert forall i,j {:trigger a[i], a[j]} :: j == i+1 ==> 0 <= i < a.Length-1 ==> a[i] <= a[j];
    var substMap = new List<Tuple<Expression, IdentifierExpr>>();
    void Name(Expression sub) {
      if (substMap.Find(x => ExprExtensions.ExpressionEq(sub, x.Item1)) == null) {
        var newBv = new BoundVar(sub.Origin, "_t#" + substMap.Count, sub.Type);
        var ie = new IdentifierExpr(sub.Origin, newBv.Name) { Var = newBv, Type = newBv.Type };
        substMap.Add(new Tuple<Expression, IdentifierExpr>(sub, ie));
      }
    }
    foreach (var triggerMatch in loopingMatches) {
      var e = triggerMatch.OriginalExpr;
      if (triggersCollector.IsPotentialTriggerCandidate(e) && triggersCollector.IsTriggerKiller(e)) {
        foreach (var sub in e.SubExpressions) {
          if (triggersCollector.IsTriggerKiller(sub) && (!triggersCollector.IsPotentialTriggerCandidate(sub))) {
            Name(sub);
          }
        }
      }
    }
    requested.ForEach(Name);

    var expr = (QuantifierExpr)Comprehension;
    if (substMap.Count > 0) {
      // The copy only selects the triggers. The verifier binds a variable to each term in its translation of the part as
      // written, or of the nested quantifier that the substituter asks to name the term.
      var s = new NamedTermSubstituter(expr, substMap, requests, reporter.Options);
      var range = expr.Range == null ? null : s.Substitute(expr.Range);
      var term = s.Substitute(expr.Term);
      var used = substMap.FindAll(x => s.Used.Contains(x.Item2));
      NamedExpressions.AddRange(used);
      expr = Bind(expr, range, term, used);
    } else {
      expr = Bind(expr, expr.Range, expr.Term, []);
    }
    var qq = expr;

    Comprehension = qq;
    Candidates.Clear();
    CandidateTerms.Clear();
    loopingMatches.Clear();
    RejectedCandidates.Clear();
    return true;

    // don't rewrite the quantifier if we are not auto generate triggers.
    // This is because rewriting introduces new boundvars and will cause
    // user provided triggers not mention all boundvars
  }

  /// <summary>
  /// A copy of the quantifier with the range and term given that also binds each name's variable to its term, as the
  /// verifier's translation does, which keeps the term's own subterms as candidates
  /// </summary>
  private static QuantifierExpr Bind(QuantifierExpr quantifier, Expression range, Expression term,
    List<Tuple<Expression, IdentifierExpr>> names) {
    foreach (var (named, variable) in names) {
      var definition = new BinaryExpr(quantifier.Origin, BinaryExpr.ResolvedOpcode.EqCommon, variable, named);
      range = range == null ? definition : new BinaryExpr(quantifier.Origin, BinaryExpr.ResolvedOpcode.And, definition, range);
    }
    var boundVars = quantifier.BoundVars.Concat(names.Select(x => (BoundVar)x.Item2.Var)).ToList();
    var bounds = quantifier.Bounds?.Concat(names.Select(x => (BoundedPool)new ExactBoundedPool(x.Item1))).ToList();
    var attributes = TriggerUtils.CopyAttributes(quantifier.Attributes);
    return quantifier is ForallExpr
      ? new ForallExpr(quantifier.Origin, boundVars, range, term, attributes) { Type = quantifier.Type, Bounds = bounds }
      : new ExistsExpr(quantifier.Origin, boundVars, range, term, attributes) { Type = quantifier.Type, Bounds = bounds };
  }

  /// <summary>
  /// Replaces each term with a variable bound where all of the term's variables are: the copy's own one, or else a fresh
  /// one of the outermost quantifier nested in the part that binds the rest and that the substituter can ask to name the
  /// term. A term that reads the heap is not replaced inside an "old" or a lambda, where it reads another heap and the
  /// verifier does not replace it either.
  /// </summary>
  private class NamedTermSubstituter : Substituter {
    // Each term with its variables and whether it reads the heap, and the variable that replaces it where the
    // substituter is
    private readonly List<(Expression Term, ISet<IVariable> Variables, bool ReadsHeap)> terms = [];
    private readonly Dictionary<Expression, IdentifierExpr> variables = [];
    // The nested quantifiers that the substituter can ask to name terms: those that break their loops and that each
    // instance of the part instantiates, as the solver gives the variables of the others a new value in each instance,
    // and their terms with it continue the loop
    private readonly HashSet<QuantifierExpr> askable = [];
    private readonly Dictionary<Expression, List<Expression>> requests;
    private ISet<IVariable> scope;
    private bool otherHeap;
    public readonly HashSet<IdentifierExpr> Used = [];

    public NamedTermSubstituter(QuantifierExpr part, List<Tuple<Expression, IdentifierExpr>> substMap,
      Dictionary<Expression, List<Expression>> requests, DafnyOptions options)
      : base(null, new Dictionary<IVariable, Expression>(), new Dictionary<TypeParameter, Type>()) {
      scope = FreeVariablesUtil.ComputeFreeVariables(options, part);
      scope.UnionWith(part.BoundVars);
      foreach (var (term, variable) in substMap) {
        var termVariables = new HashSet<IVariable>();
        var readsHeap = false;
        FreeVariablesUtil.ComputeFreeVariables(options, term, termVariables, ref readsHeap);
        terms.Add((term, termVariables, readsHeap));
        if (termVariables.IsSubsetOf(scope)) {
          variables.Add(term, variable);
        }
      }
      this.requests = requests;
      if (requests != null) {
        AddAskable(part.Range, false);
        AddAskable(part.Term, part is ForallExpr);
      }
    }

    /// <summary>
    /// Adds the askable quantifiers in expr, where a forall is universal wherever the part is if universalForall holds,
    /// and an exists is if it does not
    /// </summary>
    private void AddAskable(Expression expr, bool universalForall) {
      switch (expr) {
        case QuantifierExpr nested:
          if (nested is ForallExpr == universalForall && requests.ContainsKey(nested)) {
            askable.Add(nested);
          }
          AddAskable(nested.Range, nested is ForallExpr ? !universalForall : universalForall);
          AddAskable(nested.Term, universalForall);
          break;
        case UnaryOpExpr { ResolvedOp: UnaryOpExpr.ResolvedOpcode.BoolNot } not:
          AddAskable(not.E, !universalForall);
          break;
        case BinaryExpr { ResolvedOp: BinaryExpr.ResolvedOpcode.And or BinaryExpr.ResolvedOpcode.Or or BinaryExpr.ResolvedOpcode.Imp } binary:
          AddAskable(binary.E0, binary.ResolvedOp == BinaryExpr.ResolvedOpcode.Imp ? !universalForall : universalForall);
          AddAskable(binary.E1, universalForall);
          break;
        case ITEExpr ite:
          AddAskable(ite.Thn, universalForall);
          AddAskable(ite.Els, universalForall);
          break;
        case LetExpr let:
          AddAskable(let.Body, universalForall);
          break;
        case ConcreteSyntaxExpression syntax:
          AddAskable(syntax.ResolvedExpression, universalForall);
          break;
      }
    }

    public override Expression Substitute(Expression expr) {
      foreach (var (term, _, readsHeap) in terms) {
        if (variables.TryGetValue(term, out var variable) && !(readsHeap && otherHeap) && ExprExtensions.ExpressionEq(expr, term)) {
          Used.Add(variable);
          return variable;
        }
      }
      switch (expr) {
        case OldExpr or LambdaExpr: {
            var outer = otherHeap;
            otherHeap = true;
            var result = base.Substitute(expr);
            otherHeap = outer;
            return result;
          }
        case QuantifierExpr nested: {
            var outer = scope;
            scope = new HashSet<IVariable>(scope.Concat(nested.BoundVars));
            var result = askable.Contains(nested) ? Ask(nested) : base.Substitute(expr);
            scope = outer;
            return result;
          }
        default:
          return base.Substitute(expr);
      }
    }

    /// <summary>
    /// A copy of the nested quantifier that binds a variable to each term that it uses and binds the rest of the
    /// variables of, which the substituter asks the quantifier to name
    /// </summary>
    private QuantifierExpr Ask(QuantifierExpr nested) {
      var fresh = terms.Where(t => !variables.ContainsKey(t.Term) && t.Variables.IsSubsetOf(scope))
        .Select(t => new Tuple<Expression, IdentifierExpr>(t.Term,
          new IdentifierExpr(t.Term.Origin, new BoundVar(t.Term.Origin, "_t", t.Term.Type))))
        .ToList();
      fresh.ForEach(x => variables.Add(x.Item1, x.Item2));
      var range = nested.Range == null ? null : Substitute(nested.Range);
      var term = Substitute(nested.Term);
      fresh.ForEach(x => variables.Remove(x.Item1));
      var names = fresh.FindAll(x => Used.Contains(x.Item2));
      requests[nested].AddRange(names.Select(x => x.Item1));
      return Bind(nested, range, term, names);
    }
  }

  // TODO Check whether this makes verification faster
  public void FilterStrongCandidates() {
    var newCandidates = new List<TriggerCandidate>();
    foreach (var candidate in Candidates) {
      var weakerCandidates = Candidates.Where(candidate.IsStrongerThan).ToList();
      if (weakerCandidates.Any()) {
        RejectedCandidates.Add(candidate);
        candidate.Annotation = "more specific than " + string.Join(", ", weakerCandidates);
      } else {
        newCandidates.Add(candidate);
      }
    }
    Candidates = newCandidates;
  }

  public void CommitTrigger(ErrorReporter errorReporter, int? splitPartIndex, SystemModuleManager systemModuleManager) {
    bool suppressWarnings = Attributes.Contains(Comprehension.Attributes, "nowarn");
    var reportingToken = Comprehension.Origin;
    var warningLevel = suppressWarnings ? ErrorLevel.Info : ErrorLevel.Warning;

    if (!WantsAutoTriggers()) {
      // NOTE: split and autotriggers attributes are passed down to Boogie
      errorReporter.Message(MessageSource.Rewriter, ErrorLevel.Info, null, reportingToken,
        "The attribute {:autotriggers false} may cause brittle verification. " +
        "It's better to remove this attribute, or as a second option, manually define a trigger using {:trigger}. " +
        "For more information, see the section on quantifier instantiation rules in the reference manual.");
    }

    if (!NeedsAutoTriggers()) {
      DisableEmptyTriggers(Comprehension.Attributes, "trigger");
      return;
    }

    AddTriggerAttribute(systemModuleManager);

    if (Attributes.Contains(Comprehension.Attributes, "auto_generated")) {
      return;
    }

    string InfoFirstLineEnd(int count) {
      return count < 2 ? " " : "\n  ";
    }

    var messages = new List<string>();
    if (splitPartIndex != null) {
      messages.Add($"Part #{splitPartIndex} is '{Comprehension.Term}'");
    }
    if (Candidates.Any()) {
      var subst = Util.Comma("", NamedExpressions, pair => $" where {pair.Item2} := {pair.Item1}");
      messages.Add($"Selected triggers:{InfoFirstLineEnd(Candidates.Count)}{string.Join(", ", Candidates)}{subst}");
    }
    if (RejectedCandidates.Any()) {
      messages.Add($"Rejected triggers:{InfoFirstLineEnd(RejectedCandidates.Count)}{string.Join("\n  ", RejectedCandidates)}");
    }

    if (messages.Any()) {
      errorReporter.Message(MessageSource.Rewriter, ErrorLevel.Info, null, reportingToken, string.Join("\n", messages));
    }

    const string hint = "To silence this warning, add an explicit trigger using the {:trigger} attribute. " +
                        "For more information, see the section on quantifier instantiation rules in the reference manual.";
    if (!CandidateTerms.Any() || !Candidates.Any()) {
      if (Attributes.Contains(Comprehension.Attributes, "_delayTriggerWarning")) {
        // Just record the fact that no auto-trigger was found
        Comprehension.Attributes = new Attributes("_noAutoTriggerFound", new List<Expression>(), Comprehension.Attributes);
      } else {
        errorReporter.Message(MessageSource.Rewriter, warningLevel, null, reportingToken,
          "Could not find a trigger for this quantifier. Without a trigger, the quantifier may cause brittle verification. " + hint);
      }
    } else if (!CouldSuppressLoops && !AllowsLoops) {
      errorReporter.Message(MessageSource.Rewriter, warningLevel, null, reportingToken,
        "Triggers were added to this quantifier that may introduce matching loops, which may cause brittle verification. " + hint);
    }
  }

  public static void DisableEmptyTriggers(Attributes attribs, String attrName) {
    foreach (var attr in attribs.AsEnumerable()) {
      if (attr.Name == attrName && attr.Args.Count == 0) {
        // Remove an empty trigger attribute, so it does not crash Boogie,
        // and effectively becomes a way to silence a Dafny warning
        attr.Name = $"deleted-{attrName}";
      }
    }
  }

  private void AddTriggerAttribute(SystemModuleManager systemModuleManager) {
    // A trigger has each named term where the copy has its variable. Only a translation that binds a variable to each
    // term can use such a trigger, so it is internal, as the terms are
    var terms = new Substituter(null, NamedExpressions.ToDictionary(x => x.Item2.Var, x => x.Item1),
      new Dictionary<TypeParameter, Type>());
    foreach (var candidate in Candidates) {
      Comprehension.Attributes = new Attributes(NamedExpressions.Count == 0 ? "trigger" : "_trigger",
        candidate.Terms.ConvertAll(t => Expression.WrapAsParsedStructureIfNecessary(
          NamedExpressions.Count == 0 ? t.Expr : terms.Substitute(t.Expr), systemModuleManager)),
        Comprehension.Attributes);
    }
    if (Candidates.Count != 0 && NamedExpressions.Count != 0) {
      Comprehension.Attributes = new Attributes("_named", NamedExpressions.ConvertAll(x => x.Item1), Comprehension.Attributes);
    }
  }

  private bool WantsAutoTriggers() {
    bool wantsAutoTriggers = true;
    return !Attributes.ContainsBool(Comprehension.Attributes, "autotriggers", ref wantsAutoTriggers) || wantsAutoTriggers;
  }

  private bool NeedsAutoTriggers() {
    return !Attributes.Contains(Comprehension.Attributes, "trigger") && !Attributes.Contains(Comprehension.Attributes, "_trigger") &&
           WantsAutoTriggers();
  }

  bool WantsMatchingLoopRewrite() {
    bool wantsMatchingLoopRewrite = true;
    return (!Attributes.ContainsBool(Comprehension.Attributes, "matchinglooprewrite", ref wantsMatchingLoopRewrite) || wantsMatchingLoopRewrite) && WantsAutoTriggers();
  }
}