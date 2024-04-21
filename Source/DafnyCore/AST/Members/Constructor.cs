using System.Collections.Generic;
using System.Diagnostics.Contracts;
using OmniSharp.Extensions.LanguageServer.Protocol.Models;

namespace Microsoft.Dafny;

public class Constructor : Method {
  public override string WhatKind => "constructor";
  [ContractInvariantMethod]
  void ObjectInvariant() {
    Contract.Invariant(Body == null || Body is DividedBlockStmt);
  }

  public override SymbolKind Kind => SymbolKind.Constructor;
  protected override string GetQualifiedName() {
    return EnclosingClass.Name;
  }

  public List<Statement> BodyInit {  // first part of Body's statements
    get {
      if (Body == null) {
        return null;
      } else {
        return ((DividedBlockStmt)Body).BodyInit;
      }
    }
  }
  public List<Statement> BodyProper {  // second part of Body's statements
    get {
      if (Body == null) {
        return null;
      } else {
        return ((DividedBlockStmt)Body).BodyProper;
      }
    }
  }
  public Constructor(RangeToken rangeToken, Name name,
    bool isAlien,
    bool isGhost,
    List<TypeParameter> typeArgs,
    List<Formal> ins,
    List<AttributedExpression> req,
    Specification<FrameExpression> reads,
    [Captured] Specification<FrameExpression> mod,
    List<AttributedExpression> ens,
    Specification<Expression> decreases,
    List<(Expression, bool)> calls,
    DividedBlockStmt body,
    Attributes attributes, IToken signatureEllipsis)
    : base(rangeToken, name, false, isAlien, isGhost, typeArgs, ins, new List<Formal>(), req, reads, mod, ens, decreases, calls, body, attributes, signatureEllipsis) {
    Contract.Requires(rangeToken != null);
    Contract.Requires(name != null);
    Contract.Requires(cce.NonNullElements(typeArgs));
    Contract.Requires(cce.NonNullElements(ins));
    Contract.Requires(cce.NonNullElements(req));
    Contract.Requires(mod != null);
    Contract.Requires(cce.NonNullElements(ens));
    Contract.Requires(decreases != null);
  }

  public Constructor(Cloner cloner, Constructor original) : base(cloner, original) {
  }

  public bool HasName {
    get {
      return Name != "_ctor";
    }
  }
}