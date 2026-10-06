//-----------------------------------------------------------------------------
//
// Copyright by the contributors to the Dafny Project
// SPDX-License-Identifier: MIT
//
//-----------------------------------------------------------------------------

using System.Collections.Generic;
using System.Diagnostics.Contracts;
using System.Linq;

namespace Microsoft.Dafny;

public class IntBoundedPool : BoundedPool {
  public readonly Expression LowerBound;
  public readonly Expression UpperBound;
  /// <summary>
  /// Further bounds that could not be compared with "LowerBound" and "UpperBound" statically. The compiled range starts at
  /// the largest of the lower bounds and ends at the smallest of the upper bounds.
  /// </summary>
  public readonly IReadOnlyList<Expression> OtherLowerBounds;
  public readonly IReadOnlyList<Expression> OtherUpperBounds;

  public IntBoundedPool(Expression lowerBound, Expression upperBound)
    : this(lowerBound, upperBound, [], []) {
  }

  public IntBoundedPool(Expression lowerBound, Expression upperBound,
    IReadOnlyList<Expression> otherLowerBounds, IReadOnlyList<Expression> otherUpperBounds) {
    Contract.Requires(lowerBound != null || upperBound != null);
    Contract.Requires(lowerBound != null || otherLowerBounds.Count == 0);
    Contract.Requires(upperBound != null || otherUpperBounds.Count == 0);
    LowerBound = lowerBound;
    UpperBound = upperBound;
    OtherLowerBounds = otherLowerBounds;
    OtherUpperBounds = otherUpperBounds;
  }

  public IEnumerable<Expression> LowerBounds => LowerBound == null ? [] : OtherLowerBounds.Prepend(LowerBound);
  public IEnumerable<Expression> UpperBounds => UpperBound == null ? [] : OtherUpperBounds.Prepend(UpperBound);

  public override PoolVirtues Virtues {
    get {
      if (LowerBound != null && UpperBound != null) {
        return PoolVirtues.Finite | PoolVirtues.Enumerable | PoolVirtues.IndependentOfAlloc | PoolVirtues.IndependentOfAlloc_or_ExplicitAlloc;
      } else {
        return PoolVirtues.Enumerable | PoolVirtues.IndependentOfAlloc | PoolVirtues.IndependentOfAlloc_or_ExplicitAlloc;
      }
    }
  }
  public override int Preference() => LowerBound != null && UpperBound != null ? 5 : 4;

  public override BoundedPool Clone(Cloner cloner) {
    return new IntBoundedPool(cloner.CloneExpr(LowerBound), cloner.CloneExpr(UpperBound),
      OtherLowerBounds.Select(cloner.CloneExpr).ToList(), OtherUpperBounds.Select(cloner.CloneExpr).ToList());
  }
}
