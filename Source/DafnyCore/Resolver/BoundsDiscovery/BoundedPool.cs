//-----------------------------------------------------------------------------
//
// Copyright by the contributors to the Dafny Project
// SPDX-License-Identifier: MIT
//
//-----------------------------------------------------------------------------

using System;
using System.Collections.Generic;
using System.Diagnostics.Contracts;
using System.Linq;
using System.Numerics;

namespace Microsoft.Dafny;

public abstract class BoundedPool : ICloneable<BoundedPool> {
  [Flags]
  public enum PoolVirtues {
    None = 0,
    Finite = 1,
    Enumerable = 2,
    IndependentOfAlloc = 4,
    IndependentOfAlloc_or_ExplicitAlloc = 8
  }

  public abstract PoolVirtues Virtues { get; }

  /// <summary>
  /// A higher preference is better.
  /// A preference below 2 is a last-resort bounded pool. Bounds discovery will not consider
  /// such a pool to be final until there are no other choices.
  ///
  /// For easy reference, here is the BoundedPool hierarchy and their preference levels:
  ///
  /// 0: AllocFreeBoundedPool
  /// 0: ExplicitAllocatedBoundedPool
  /// 0: SpecialAllocIndependenceAllocatedBoundedPool
  /// 0: OlderBoundedPool
  ///
  /// 1: WiggleWaggleBound
  ///
  /// 2: SuperSetBoundedPool
  /// 2: DatatypeInclusionBoundedPool
  ///
  /// 3: SubSetBoundedPool
  ///
  /// 4: IntBoundedPool with one bound
  /// 5: IntBoundedPool with both bounds
  /// 5: CharBoundedPool
  ///
  /// 8: DatatypeBoundedPool
  ///
  /// 10: CollectionBoundedPool
  ///     - SetBoundedPool
  ///     - MultiSetBoundedPool
  ///     - MapBoundedPool
  ///     - SeqBoundedPool
  ///
  /// 14: BoolBoundedPool
  ///
  /// 15: ExactBoundedPool
  /// </summary>
  public abstract int Preference(); // higher is better

  public static BoundedPool GetBest(List<BoundedPool> bounds) {
    Contract.Requires(bounds != null);
    bounds = CombineIntegerBounds(bounds);
    BoundedPool best = null;
    foreach (var bound in bounds) {
      if (best is IntBoundedPool ibp0 && bound is IntBoundedPool ibp1) {
        var lowerBounds = ChooseIntegerBounds(ibp0.LowerBounds.Concat(ibp1.LowerBounds), true);
        var upperBounds = ChooseIntegerBounds(ibp0.UpperBounds.Concat(ibp1.UpperBounds), false);
        best = new IntBoundedPool(lowerBounds.FirstOrDefault(), upperBounds.FirstOrDefault(),
          lowerBounds.Skip(1).ToList(), upperBounds.Skip(1).ToList());
      } else if (best == null || bound.Preference() > best.Preference()) {
        best = bound;
      }
    }
    return best;
  }

  /// <summary>
  /// Returns the bounds, all on one side of a variable, that its enumeration has to take the largest ("pickMax") or the
  /// smallest of at run time. Of the constant bounds, only the tightest is kept; the other bounds cannot be compared
  /// statically, so they are all kept. The constant is kept even where the type of another bound seems to imply it,
  /// since that bound need not lie in its type: bounds discovery moves terms across an inequality, and substitutes for
  /// a bound variable a bound that the variable itself never reaches.
  /// </summary>
  static List<Expression> ChooseIntegerBounds(IEnumerable<Expression> bounds, bool pickMax) {
    Expression constantBound = null;
    BigInteger constant = default;
    var others = new List<Expression>();
    foreach (var bound in bounds) {
      if (ConstantFolder.TryFoldInteger(bound) is not { } value) {
        others.Add(bound);
      } else if (constantBound == null || (pickMax ? constant < value : value < constant)) {
        constantBound = bound;
        constant = value;
      }
    }
    if (constantBound != null) {
      others.Insert(0, constantBound);
    }
    return others;
  }

  public static List<VT> MissingBounds<VT>(List<VT> vars, List<BoundedPool> bounds, PoolVirtues requiredVirtues) where VT : IVariable {
    Contract.Requires(vars != null);
    Contract.Requires(bounds == null || vars.Count == bounds.Count);
    Contract.Ensures(Contract.Result<List<VT>>() != null);
    var missing = new List<VT>();
    for (var i = 0; i < vars.Count; i++) {
      if (bounds == null || bounds[i] == null ||
          (bounds[i].Virtues & requiredVirtues) != requiredVirtues ||
          ((requiredVirtues & PoolVirtues.Enumerable) != 0 && !bounds[i].IsCompilable(vars[i].Type))) {
        missing.Add(vars[i]);
      }
    }
    return missing;
  }

  public static List<bool> HasBounds(List<BoundedPool> bounds, PoolVirtues requiredVirtues = PoolVirtues.None) {
    Contract.Requires(bounds != null);
    Contract.Ensures(Contract.Result<List<bool>>() != null);
    Contract.Ensures(Contract.Result<List<bool>>().Count == bounds.Count);
    return bounds.ConvertAll(bound => bound != null && (bound.Virtues & requiredVirtues) == requiredVirtues);
  }

  static List<BoundedPool> CombineIntegerBounds(List<BoundedPool> bounds) {
    var lowerBounds = new List<IntBoundedPool>();
    var upperBounds = new List<IntBoundedPool>();
    var others = new List<BoundedPool>();
    foreach (var b in bounds) {
      var ib = b as IntBoundedPool;
      if (ib != null && ib.UpperBound == null) {
        lowerBounds.Add(ib);
      } else if (ib != null && ib.LowerBound == null) {
        upperBounds.Add(ib);
      } else {
        others.Add(b);
      }
    }
    // pair up the bounds
    var n = Math.Min(lowerBounds.Count, upperBounds.Count);
    for (var i = 0; i < n; i++) {
      others.Add(new IntBoundedPool(lowerBounds[i].LowerBound, upperBounds[i].UpperBound,
        lowerBounds[i].OtherLowerBounds, upperBounds[i].OtherUpperBounds));
    }
    for (var i = n; i < lowerBounds.Count; i++) {
      others.Add(lowerBounds[i]);
    }
    for (var i = n; i < upperBounds.Count; i++) {
      others.Add(upperBounds[i]);
    }
    return others;
  }

  public virtual bool IsCompilable(Type boundVariableType) =>
    ExpressionTester.IsTypeTestCompilable(boundVariableType.NormalizeToAncestorType(), boundVariableType);

  public abstract BoundedPool Clone(Cloner cloner);
}