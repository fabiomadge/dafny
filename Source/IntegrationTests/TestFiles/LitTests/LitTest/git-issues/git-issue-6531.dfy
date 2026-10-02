// RUN: %exits-with 4 %verify "%s" > "%t"
// RUN: %diff "%s.expect" "%t"

// Bad's postcondition is false, and the equality axiom of the single-constructor datatype Unit,
// applied to values of R, must not prove it. The forall statement and {:induction false} are what
// lead the solver to that axiom.

datatype Unit = U
datatype R = X | Y(n: nat)
datatype S = S(n: nat)

function F(u: Unit, s: S): R {
  if u == U then (if s.n == 0 then X else Y(0)) else Y(1)
}

function G(us: seq<Unit>, s: S): seq<R> {
  if |us| == 0 then [] else [F(us[0], s)] + G(us[1..], s)
}

// False: G([U], S(1)) == [Y(0)].
lemma {:induction false} Bad(us: seq<Unit>, s: S)
  requires 0 < |us| && s.n <= 1
  ensures G(us, s)[0].X? // error: (but this was once provable, due to a bug)
{
  forall us': seq<Unit>, s': S | 0 < |us'| && s'.n <= 1
    ensures G(us', s') != []
  { }
}
