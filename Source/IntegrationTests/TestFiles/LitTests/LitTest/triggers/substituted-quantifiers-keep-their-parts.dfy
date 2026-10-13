// RUN: %verify --show-hints --allow-warnings --rprint "%t.rprint.dfy" "%s" > "%t"
// RUN: %diff "%s.expect" "%t"
// RUN: %OutputCheck --file-to-check "%t.rprint.dfy" "%s"

// The analyses below of the formula that the verifier translates see the parts of a quantifier that the trigger
// generator split or rewrote, also where a substitution copied it

module Induction {
  function Pow(n: nat): nat { if n == 0 then 1 else 2 * Pow(n - 1) }

  // The induction hypothesis gets the trigger Pow(n), since the part of the inner quantifier, which breaks its matching
  // loop, has Pow(_t#0) instead of Pow(k + n)
  lemma PowPositive(n: nat)
    ensures Pow(n) >= 1 && forall k: nat :: k < 2 ==> Pow(k) <= Pow(k + n)
  {
  }

  predicate P(k: int)

  // The induction hypothesis copies the postcondition's quantifier, whose trigger P(k) the trigger generator selected,
  // and the rewrite of its matching loop replaces n + 1 in the copy too
  lemma PowMonotone(n: nat)
    ensures forall k :: P(k) ==> Pow(n) <= Pow(n + 1)
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

module TriggerCopies {
  function Pow(n: nat): nat { if n == 0 then 1 else 2 * Pow(n - 1) }
  function h(n: nat): nat

  // The triggers of a :| and of a quantifier with a let in its body are selected on a copy, whose hints name k + n once
  method SuchThat()
    requires Pow(5) == 32 && forall k: nat :: k < 2 ==> Pow(k) <= Pow(k + 5)
  {
    ghost var n: nat :| Pow(n) == 32 && forall k: nat :: k < 2 ==> Pow(k) <= Pow(k + n);
  }

  method Let()
    requires forall n: nat :: var m := n; h(n) == 0 && forall k: nat :: k < 2 ==> h(k) <= h(k + m)
  {
    assert h(3) == 0;
  }
}

module Callee {
  predicate P(i: int, n: int)

  function F(n: int): int
    requires forall i :: 0 <= i < 5 ==> P(i, n) && P(i + 1, n)
    requires |set i | 0 <= i < n && P(i, i + 1)| <= n
}

// {:autoReq} copies the preconditions with the parts and triggers that the other module selected, which the trigger
// generator would not find in terms that have n + 1, and does not select triggers, or warn about them, again
module Caller {
  import Callee

  function {:autoReq} G(n: int): int {
    Callee.F(n + 1)
  }

  predicate R(j: int)

  // The rewrite of H's existential, which breaks the matching loop of R(j) and R(j + 1), keeps the parts of the copy in
  // it and their triggers
  // CHECK: \{:trigger P\(i, j\)\}
  ghost predicate {:autoReq} H() {
    exists j :: R(j) && Callee.F(j) == 0 && R(j + 1)
  }
}

module SplitGuards {
  predicate A(x: int) { x % 2 == 0 }
  predicate B(x: int) { x % 3 == 0 }
  predicate P(x: int)

  // The trigger generator splits each case's binding guard into two parts, which are no binding guard, and a copy that
  // replaces quantifiers by their parts, of a quantifier in a lambda or with an inlined let, keeps the guard
  method InLambda() {
    var f := (k: int) => forall n | 0 <= n < k ::
      calc { A(2 * n); { if case x :| B(x) || (A(x) && A(x + 1)) => case true => } true; } B(3 * n);
  }

  lemma InLet()
    requires forall x :: var z := x + 1; (assert true by { if case y :| A(y) || B(y + z) => case true => } P(z))
  {
  }

  function Guarded(n: int): int
    requires (assert true by { if x :| A(x) { } } n >= 0)
  {
    0
  }

  // The splitter visits the copy of the binding guard that {:autoReq} makes, which needs a type
  function {:autoReq} CallsGuarded(n: int): int {
    Guarded(n)
  }

  lemma GuardedLemma(n: int)
    ensures (assert true by { if x :| A(x) { } } P(n) || !P(n))
  {
  }

  // And the copy that a forall statement makes of the lemma's postcondition
  method CallsGuardedLemma() {
    forall n | 0 <= n < 3 {
      GuardedLemma(n);
    }
  }

  predicate Q<T(!new)>(y: T)

  function GuardedGeneric<T(!new)>(t: T): int
    requires (assert true by { if y: T :| Q(y) { assert Q(y); } if case y: T :| Q(y) => assert Q(y); case true => } true)
  {
    0
  }

  // The copy of each binding guard has a y of type int, which the statement that it guards uses too
  function {:autoReq} CallsGuardedGeneric(n: int): int {
    GuardedGeneric(n)
  }
}
