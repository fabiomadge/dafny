// RUN: %verify "%s" > "%t"
// RUN: %diff "%s.expect" "%t"

// A substitution copies a quantifier that the trigger generator split or rewrote together with its parts, which the
// verifier translates, so that the analyses of the translated formula below see them

module Induction {
  function Pow(n: nat): nat { if n == 0 then 1 else 2 * Pow(n - 1) }

  // The induction hypothesis gets the trigger Pow(n), since the part of the inner quantifier, which breaks its matching
  // loop, has Pow(_t#0) instead of Pow(k + n)
  lemma PowPositive(n: nat)
    ensures Pow(n) >= 1 && forall k: nat :: k < 2 ==> Pow(k) <= Pow(k + n)
  {
  }
}

module SuchThat {
  datatype D = D(n: int)
  predicate A(i: int, d: D)
  predicate B(i: int)

  // Each existence check proves the part exists i :: B(i), which does not mention d, so it needs no value for d
  method Statement()
    requires B(0)
  {
    ghost var d: D :| exists i :: B(i) || (A(i, d) && A(i + 1, d));
  }

  method InLambda() {
    var f := (k: int) requires B(k) => var d: D :| exists i :: B(i) || (A(i, d) && A(i + 1, d)); d;
  }

  ghost function Let(): D
    requires B(0)
  {
    var d: D :| exists i :: B(i) || (A(i, d) && A(i + 1, d)); d
  }
}

module Callee {
  predicate P(x: int)

  function F(n: int): int
    requires forall i :: 0 <= i < n ==> P(i)
}

// The precondition that {:autoReq} copies from another module is split already
module Caller {
  import Callee

  function {:autoReq} G(n: int): int {
    Callee.F(n)
  }
}
