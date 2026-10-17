using System.Collections.Generic;
using System.Diagnostics.Contracts;

namespace Microsoft.Dafny;

internal class QuantifierSplittingRewriter : IRewriter {
  private readonly ISet<QuantifierExpr> splittable;

  internal QuantifierSplittingRewriter(ErrorReporter reporter, ISet<QuantifierExpr> splittable) : base(reporter) {
    Contract.Requires(reporter != null);
    this.splittable = splittable;
  }

  internal override void PostResolveIntermediate(ModuleDefinition m) {
    var splitter = new Triggers.QuantifierSplitter(splittable);
    foreach (var decl in ModuleDefinition.AllCallables(m.TopLevelDecls)) {
      splitter.Visit(decl);
    }
  }
}