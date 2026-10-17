// RUN: %verify --allow-warnings "%s" > "%t"
// RUN: %diff "%s.expect" "%t"

// A substitution copies a binding guard as written, gives the copy a type, and lets the statements that the guard
// guards use the copy's variables

predicate A(x: int) { x % 2 == 0 }
predicate B(x: int) { x % 3 == 0 }
predicate P(x: int)
predicate Q<T(!new)>(y: T)

// The lambda's body reaches the verifier through a substitution, and the trigger generator splits the guard
method InLambda() {
  var f := (k: int) => forall n | 0 <= n < k ::
    calc { A(2 * n); { if case x :| B(x) || (A(x) && A(x + 1)) => case true => } true; } B(3 * n);
}

function Guarded(n: int): int
  requires (assert true by { if x :| A(x) { } if case x :| A(x) => case true => } n >= 0)
{
  0
}

// {:autoReq} copies the guards, which need a type
function {:autoReq} CallsGuarded(n: int): int {
  Guarded(n)
}

lemma GuardedLemma(n: int)
  ensures (assert true by { if x :| A(x) { } } P(n) || !P(n))
{
}

// And so does the forall statement's copy of the lemma's postcondition
method CallsGuardedLemma() {
  forall n | 0 <= n < 3 {
    GuardedLemma(n);
  }
}

function GuardedGeneric<T(!new)>(t: T): int
  requires (assert true by { if y: T :| Q(y) { assert Q(y); } if case y: T :| Q(y) => assert Q(y); case true => } true)
{
  0
}

// The copy of each guard has a y of type int, which the statement that the guard guards uses too
function {:autoReq} CallsGuardedGeneric(n: int): int {
  GuardedGeneric(n)
}
