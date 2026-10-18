using System.Collections.Generic;
using System.Diagnostics.Contracts;

namespace Microsoft.Dafny;

public class TriggerGeneratingRewriter : IRewriter {
  private readonly SystemModuleManager systemModuleManager;
  private readonly ISet<QuantifierExpr> splittable;
  internal TriggerGeneratingRewriter(ErrorReporter reporter, SystemModuleManager systemModuleManager,
    ISet<QuantifierExpr> splittable) : base(reporter) {
    Contract.Requires(reporter != null);
    this.systemModuleManager = systemModuleManager;
    this.splittable = splittable;
  }

  internal override void PostCyclicityResolve(ModuleDefinition definition) {
    var finder = new Triggers.QuantifierCollector(Reporter, splittable);

    foreach (var decl in ModuleDefinition.AllCallablesIncludingPrefixDeclarations(definition.TopLevelDecls)) {
      finder.Visit(decl, null);
    }

    var triggersCollector = new Triggers.TriggersCollector(finder.exprsInOldContext, Reporter.Options, definition);
    foreach (var quantifierCollection in finder.quantifierCollections) {
      quantifierCollection.ComputeTriggers(triggersCollector);
      quantifierCollection.CommitTriggers(systemModuleManager);
    }

    finder.ApplyPostActions();
  }
}