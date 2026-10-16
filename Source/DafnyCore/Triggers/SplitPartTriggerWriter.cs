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
  // The part as written while the triggers are selected on the matching-loop rewrite's copy, and the copy's variables
  // for the terms that it names, with their terms
  private ComprehensionExpr asWritten;
  private readonly List<(BoundVar Variable, Expression Term)> names = [];

  private bool AllowsLoops {
    get {
      Contract.Requires(!(Comprehension is QuantifierExpr) || ((QuantifierExpr)Comprehension).SplitQuantifier == null); // Don't call this on a quantifier with a Split clause: it's not a real quantifier
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

  public bool RewriteMatchingLoop(ErrorReporter reporter, ModuleDefinition module) {
    if (!NeedsAutoTriggers() || !WantsMatchingLoopRewrite()) {
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
    foreach (var triggerMatch in loopingMatches) {
      var e = triggerMatch.OriginalExpr;
      if (triggersCollector.IsPotentialTriggerCandidate(e) && triggersCollector.IsTriggerKiller(e)) {
        foreach (var sub in e.SubExpressions) {
          if (triggersCollector.IsTriggerKiller(sub) && (!triggersCollector.IsPotentialTriggerCandidate(sub))) {
            var entry = substMap.Find(x => ExprExtensions.ExpressionEq(sub, x.Item1));
            if (entry == null) {
              var newBv = new BoundVar(sub.Origin, "_t#" + substMap.Count, sub.Type);
              var ie = new IdentifierExpr(sub.Origin, newBv.Name) { Var = newBv, Type = newBv.Type };
              substMap.Add(new Tuple<Expression, IdentifierExpr>(sub, ie));
            }
          }
        }
      }
    }

    var expr = (QuantifierExpr)Comprehension;
    if (substMap.Count > 0) {
      // The copy only selects the triggers. The verifier binds a variable to each term in its translation of the part as
      // written, so a term must not mention a variable that the part binds inside.
      var inScope = FreeVariablesUtil.ComputeFreeVariables(reporter.Options, Comprehension);
      inScope.UnionWith(Comprehension.BoundVars);
      var s = new NamedTermSubstituter(substMap.FindAll(x =>
        FreeVariablesUtil.ComputeFreeVariables(reporter.Options, x.Item1).IsSubsetOf(inScope)), reporter.Options);
      var range = expr.Range == null ? null : s.Substitute(expr.Range);
      var term = s.Substitute(expr.Term);
      var used = substMap.FindAll(s.Used.Contains);
      names.AddRange(used.Select(x => ((BoundVar)x.Item2.Var, x.Item1)));
      // The verifier's translation defines the variables too, which keeps the terms' own subterms as candidates
      foreach (var (named, variable) in used) {
        var definition = new BinaryExpr(expr.Origin, BinaryExpr.ResolvedOpcode.EqCommon, variable, named);
        range = range == null ? definition : new BinaryExpr(expr.Origin, BinaryExpr.ResolvedOpcode.And, definition, range);
      }
      var boundVars = expr.BoundVars.Concat(names.Select(x => x.Variable)).ToList();
      var bounds = expr.Bounds?.Concat(names.Select(x => (BoundedPool)new ExactBoundedPool(x.Term))).ToList();
      var attributes = TriggerUtils.CopyAttributes(expr.Attributes);
      expr = expr is ForallExpr
        ? new ForallExpr(expr.Origin, boundVars, range, term, attributes) { Type = expr.Type, Bounds = bounds }
        : new ExistsExpr(expr.Origin, boundVars, range, term, attributes) { Type = expr.Type, Bounds = bounds };
      NamedExpressions.AddRange(used);
    } else {
      // make a copy of the expr
      if (expr is ForallExpr) {
        expr = new ForallExpr(expr.Origin, expr.BoundVars, expr.Range, expr.Term,
          TriggerUtils.CopyAttributes(expr.Attributes)) { Type = expr.Type, Bounds = expr.Bounds };
      } else {
        expr = new ExistsExpr(expr.Origin, expr.BoundVars, expr.Range, expr.Term,
          TriggerUtils.CopyAttributes(expr.Attributes)) { Type = expr.Type, Bounds = expr.Bounds };
      }
    }
    var qq = expr;

    asWritten = Comprehension;
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
  /// Puts back the part as written once the triggers are selected on the matching-loop rewrite's copy, which only the
  /// trigger generator sees
  /// </summary>
  internal void RestoreAsWritten() {
    if (asWritten != null) {
      Comprehension = asWritten;
      asWritten = null;
    }
  }

  /// <summary>
  /// Replaces each term with its variable, except a term that reads the heap inside an "old" or a lambda, where it reads
  /// another heap and the verifier does not replace it either
  /// </summary>
  private class NamedTermSubstituter : Substituter {
    private readonly List<Tuple<Expression, IdentifierExpr>> heapFree;
    private List<Tuple<Expression, IdentifierExpr>> terms;
    public readonly HashSet<Tuple<Expression, IdentifierExpr>> Used = [];

    public NamedTermSubstituter(List<Tuple<Expression, IdentifierExpr>> terms, DafnyOptions options)
      : base(null, new Dictionary<IVariable, Expression>(), new Dictionary<TypeParameter, Type>()) {
      this.terms = terms;
      heapFree = terms.FindAll(x => {
        var usesHeap = false;
        FreeVariablesUtil.ComputeFreeVariables(options, x.Item1, new HashSet<IVariable>(), ref usesHeap);
        return !usesHeap;
      });
    }

    public override Expression Substitute(Expression expr) {
      var entry = terms.Find(x => ExprExtensions.ExpressionEq(expr, x.Item1));
      if (entry != null) {
        Used.Add(entry);
        return entry.Item2;
      }
      if (expr is OldExpr or LambdaExpr) {
        var outer = terms;
        terms = heapFree;
        var result = base.Substitute(expr);
        terms = outer;
        return result;
      }
      return base.Substitute(expr);
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
    // A trigger has each named term where the copy has its variable, and the verifier binds a variable to it
    var terms = new Substituter(null, names.ToDictionary(x => (IVariable)x.Variable, x => x.Term), new Dictionary<TypeParameter, Type>());
    foreach (var candidate in Candidates) {
      Comprehension.Attributes = new Attributes("trigger",
        candidate.Terms.ConvertAll(t =>
          Expression.WrapAsParsedStructureIfNecessary(names.Count == 0 ? t.Expr : terms.Substitute(t.Expr), systemModuleManager)),
        Comprehension.Attributes);
    }
    if (Candidates.Count != 0 && names.Count != 0) {
      Comprehension.Attributes = new Attributes("_named", names.ConvertAll(x => x.Term), Comprehension.Attributes);
    }
  }

  private bool WantsAutoTriggers() {
    bool wantsAutoTriggers = true;
    return !Attributes.ContainsBool(Comprehension.Attributes, "autotriggers", ref wantsAutoTriggers) || wantsAutoTriggers;
  }

  private bool NeedsAutoTriggers() {
    return !Attributes.Contains(Comprehension.Attributes, "trigger") && WantsAutoTriggers();
  }

  bool WantsMatchingLoopRewrite() {
    bool wantsMatchingLoopRewrite = true;
    return (!Attributes.ContainsBool(Comprehension.Attributes, "matchinglooprewrite", ref wantsMatchingLoopRewrite) || wantsMatchingLoopRewrite) && WantsAutoTriggers();
  }
}