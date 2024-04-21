using System.Collections.Generic;

namespace Microsoft.Dafny;

public class SpecialFunction : Function, ICallable {
  readonly ModuleDefinition Module;
  public SpecialFunction(RangeToken rangeToken, string name, ModuleDefinition module, bool hasStaticKeyword, bool isGhost,
    List<TypeParameter> typeArgs, List<Formal> formals, Type resultType,
    List<AttributedExpression> req, Specification<FrameExpression> reads, List<AttributedExpression> ens, Specification<Expression> decreases, List<(Expression, bool)> calls,
    Expression body, Attributes attributes, IToken signatureEllipsis)
    : base(rangeToken, new Name(name), hasStaticKeyword, false, isGhost, false, typeArgs, formals, null, resultType, req, reads, ens, decreases, calls, body, null, null, attributes, signatureEllipsis) {
    Module = module;
  }
  ModuleDefinition IASTVisitorContext.EnclosingModule { get { return this.Module; } }
  string ICallable.NameRelativeToModule { get { return Name; } }
}