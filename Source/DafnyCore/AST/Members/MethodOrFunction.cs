using System.Collections.Generic;

namespace Microsoft.Dafny;

public abstract class MethodOrFunction : MemberDecl {
  public readonly List<TypeParameter> TypeArgs;
  public readonly List<AttributedExpression> Req;
  public readonly List<AttributedExpression> Ens;
  public readonly Specification<Expression> Decreases;
  public readonly List<(Expression callable, bool recursive)> Calls;

  protected MethodOrFunction(RangeToken rangeToken, Name name, bool hasStaticKeyword, bool isAlien, bool isGhost,
    Attributes attributes, bool isRefining, List<TypeParameter> typeArgs,
    List<AttributedExpression> req,
    List<AttributedExpression> ens,
    Specification<Expression> decreases,
    List<(Expression, bool)> calls)
    : base(rangeToken, name, hasStaticKeyword, isGhost, attributes, isRefining) {
    TypeArgs = typeArgs;
    Req = req;
    Ens = ens;
    Decreases = decreases;
    Calls = calls;
    IsAlien = isAlien;
  }

  protected MethodOrFunction(Cloner cloner, MethodOrFunction original) : base(cloner, original) {
    this.TypeArgs = cloner.CloneResolvedFields ? original.TypeArgs : original.TypeArgs.ConvertAll(cloner.CloneTypeParam);
    this.Req = original.Req.ConvertAll(cloner.CloneAttributedExpr);
    this.Ens = original.Ens.ConvertAll(cloner.CloneAttributedExpr);
    this.Decreases = cloner.CloneSpecExpr(original.Decreases);
    this.Calls = original.Calls.ConvertAll((item=> (cloner.CloneExpr(item.callable), item.recursive)));
    this.IsAlien = original.IsAlien;
  }

  protected abstract bool Bodyless { get; }
  protected abstract string TypeName { get; }

  public bool IsVirtual => EnclosingClass is TraitDecl && !IsStatic;
  public bool IsAbstract => EnclosingClass.EnclosingModuleDefinition.ModuleKind != ModuleKindEnum.Concrete;
  public bool IsAlien { get; }

  public virtual void Resolve(ModuleResolver resolver) {
    ResolveMethodOrFunction(resolver);
  }

  public void ResolveMethodOrFunction(INewOrOldResolver resolver) {
    if (Bodyless && !IsVirtual && !IsAbstract && !this.IsExtern(resolver.Options) && !this.IsExplicitAxiom()) {
      foreach (var ensures in Ens) {
        if (!ensures.IsExplicitAxiom() && !resolver.Options.Get(CommonOptionBag.AllowAxioms)) {
          resolver.Reporter.Warning(MessageSource.Verifier, ResolutionErrors.ErrorId.none, ensures.Tok,
            $"This ensures clause is part of a bodyless {TypeName}. Add the {{:axiom}} attribute to it or the enclosing {TypeName} to suppress this warning");
        }
      }
    }
  }

  protected MethodOrFunction(RangeToken tok, Name name, bool hasStaticKeyword, bool isGhost, Attributes attributes, bool isRefining) : base(tok, name, hasStaticKeyword, isGhost, attributes, isRefining) {
  }
}