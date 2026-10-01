// RUN: %exits-with 4 %verify "%s" > "%t"
// RUN: %diff "%s.expect" "%t"

// The induction hypothesis of each lemma below quantifies over sequences s'.
// Its precondition's "can call" facts say that every element of s' is an A,
// so they must be assumed only for an s' of type seq<A>. Otherwise, the
// hypothesis instantiated at t (an s' of the same length) says that the
// elements of t are A's, contradicting their type.

datatype A = A(x: int)
datatype B = B(y: int)

lemma {:induction s} Explicit(s: seq<A>, t: seq<B>)
  requires |t| == |s|
  requires forall i | 0 <= i < |s| :: s[i].x == 0 && t[i].y == 0
  ensures |t| > 0 ==> t[0].y == 1 // error: (but this was once provable, due to a bug)
{
}

function Count(s: seq<A>): nat {
  if |s| == 0 then 0 else 1 + Count(s[1..])
}

// Same, with the default (automatic) choice of induction variables
lemma Auto(s: seq<A>, t: seq<B>)
  requires |t| == |s|
  requires forall i | 0 <= i < |s| :: s[i].x == 0 && t[i].y == 0
  ensures |t| > 0 ==> Count(s) == 7 && t[0].y == 1 // error (x2): (but this was once provable, due to a bug)
{
}
