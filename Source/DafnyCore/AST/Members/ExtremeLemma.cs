using System.Collections.Generic;
using System.Diagnostics.Contracts;
using System.Linq;

namespace Microsoft.Dafny;

public abstract class ExtremeLemma : Method {
  public override string WhatKindMentionGhost => WhatKind;
  public readonly ExtremePredicate.KType TypeOfK;
  public bool KNat => TypeOfK == ExtremePredicate.KType.Nat;
  [FilledInDuringResolution] public PrefixLemma PrefixLemma;  // (name registration)

  public override IEnumerable<INode> Children => base.Children.Concat(new[] { PrefixLemma });

  public override IEnumerable<INode> PreResolveChildren => base.Children;

  public ExtremeLemma(Cloner cloner, ExtremeLemma lemma) : base(cloner, lemma) {
    TypeOfK = lemma.TypeOfK;
  }

  public ExtremeLemma(RangeToken rangeToken, Name name,
    bool hasStaticKeyword, bool isAlien, ExtremePredicate.KType typeOfK,
    List<TypeParameter> typeArgs,
    List<Formal> ins, [Captured] List<Formal> outs,
    List<AttributedExpression> req,
    Specification<FrameExpression> reads,
    [Captured] Specification<FrameExpression> mod,
    List<AttributedExpression> ens,
    Specification<Expression> decreases,
    List<(Expression, bool)> calls,
    BlockStmt body,
    Attributes attributes, IToken signatureEllipsis)
    : base(rangeToken, name, hasStaticKeyword, isAlien, true, typeArgs, ins, outs, req, reads, mod, ens, decreases, calls, body, attributes, signatureEllipsis) {
    Contract.Requires(rangeToken != null);
    Contract.Requires(name != null);
    Contract.Requires(cce.NonNullElements(typeArgs));
    Contract.Requires(cce.NonNullElements(ins));
    Contract.Requires(cce.NonNullElements(outs));
    Contract.Requires(cce.NonNullElements(req));
    Contract.Requires(mod != null);
    Contract.Requires(cce.NonNullElements(ens));
    Contract.Requires(decreases != null);
    TypeOfK = typeOfK;
  }

  public override bool AllowsAllocation => false;
}

public class LeastLemma : ExtremeLemma {
  public override string WhatKind => "least lemma";

  public LeastLemma(RangeToken rangeToken, Name name,
    bool hasStaticKeyword, bool isAlien, ExtremePredicate.KType typeOfK,
    List<TypeParameter> typeArgs,
    List<Formal> ins, [Captured] List<Formal> outs,
    List<AttributedExpression> req,
    Specification<FrameExpression> reads,
    [Captured] Specification<FrameExpression> mod,
    List<AttributedExpression> ens,
    Specification<Expression> decreases,
    List<(Expression, bool)> calls,
    BlockStmt body,
    Attributes attributes, IToken signatureEllipsis)
    : base(rangeToken, name, hasStaticKeyword, isAlien, typeOfK, typeArgs, ins, outs, req, reads, mod, ens, decreases, calls, body, attributes, signatureEllipsis) {
    Contract.Requires(rangeToken != null);
    Contract.Requires(name != null);
    Contract.Requires(cce.NonNullElements(typeArgs));
    Contract.Requires(cce.NonNullElements(ins));
    Contract.Requires(cce.NonNullElements(outs));
    Contract.Requires(cce.NonNullElements(req));
    Contract.Requires(mod != null);
    Contract.Requires(cce.NonNullElements(ens));
    Contract.Requires(decreases != null);
  }

  public LeastLemma(Cloner cloner, LeastLemma leastLemma) : base(cloner, leastLemma) {
  }
}

public class GreatestLemma : ExtremeLemma {
  public override string WhatKind => "greatest lemma";

  public GreatestLemma(RangeToken rangeToken, Name name,
    bool hasStaticKeyword, bool isAlien, ExtremePredicate.KType typeOfK,
    List<TypeParameter> typeArgs,
    List<Formal> ins, [Captured] List<Formal> outs,
    List<AttributedExpression> req,
    Specification<FrameExpression> reads,
    [Captured] Specification<FrameExpression> mod,
    List<AttributedExpression> ens,
    Specification<Expression> decreases,
    List<(Expression, bool)> calls,
    BlockStmt body,
    Attributes attributes, IToken signatureEllipsis)
    : base(rangeToken, name, hasStaticKeyword, isAlien, typeOfK, typeArgs, ins, outs, req, reads, mod, ens, decreases, calls, body, attributes, signatureEllipsis) {
    Contract.Requires(rangeToken != null);
    Contract.Requires(name != null);
    Contract.Requires(cce.NonNullElements(typeArgs));
    Contract.Requires(cce.NonNullElements(ins));
    Contract.Requires(cce.NonNullElements(outs));
    Contract.Requires(cce.NonNullElements(req));
    Contract.Requires(mod != null);
    Contract.Requires(cce.NonNullElements(ens));
    Contract.Requires(decreases != null);
  }

  public GreatestLemma(Cloner cloner, GreatestLemma greatestLemma) : base(cloner, greatestLemma) {
  }
}
