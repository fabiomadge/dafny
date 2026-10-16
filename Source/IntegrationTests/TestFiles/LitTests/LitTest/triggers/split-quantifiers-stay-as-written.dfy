// RUN: %exits-with 4 %verify --show-hints --allow-warnings --rprint "%t.rprint.dfy" "%s" > "%t"
// RUN: %diff "%s.expect" "%t"
// RUN: %OutputCheck --file-to-check "%t.rprint.dfy" "%s"

// The trigger generator splits these quantifiers at their conjunctions and disjunctions, but only the verifier's
// translation has the parts, so a copy that a substitution makes is the quantifier as written

// The lambda's body reaches the well-formedness check through a substitution. Given the first part, which holds for
// every i, the second is well-formed, but the quantifier as written is not.
method WellFormedness(s: seq<int>, t: seq<int>)
  requires |t| == |s|
{
  var f := (k: int) => forall i | 0 <= i < |s| :: s[i] > 0 && 10 / s[(i + 1) % |s|] > t[i]; // error: division by zero
}

datatype D = D(n: int)
predicate A(i: int, d: D)
predicate B(i: int)

// The existence check takes the part exists i :: B(i), which does not mention d, for a disjunct of its own, so it
// needs no value for d
method SuchThat()
  requires B(0)
{
  ghost var d: D :| exists i :: B(i) || (A(i, d) && A(i + 1, d));
}

ghost function LetSuchThat(): D
  requires B(0)
{
  var d: D :| exists i :: B(i) || (A(i, d) && A(i + 1, d)); d
}

predicate P(x: int)
function H(x: int): int

// The verifier translates each part with its own triggers
// CHECK: \(forall x: int \{:trigger P\(x\)\} ::
// CHECK-NEXT: P\(x\)\) &&
// CHECK-NEXT: forall x: int \{:trigger H\(x \+ 1\), H\(x\)\} /\*\{:_named x \+ 1\}\*/ ::
ghost predicate Parts() {
  forall x :: P(x) && H(x) <= H(x + 1)
}

function G(x: int): int

// The trigger generator joins the two parts again, as they get the same trigger, and the verifier makes the joined part
// from both
method Joined()
  requires forall x :: 0 <= G(x)
{
  assert forall x :: 0 <= G(x) && G(x) < 10; // error: assertion might not hold
}

module Callee {
  ghost predicate P(x: int)

  function F(b: bool): int
    requires forall x :: P(x) ==> b
  {
    0
  }
}

// {:autoReq} copies F's precondition, whose quantifier has one part, into G's for c && d, which has two conjuncts, so
// the verifier takes the copy for one part. The trigger generator does not select the copy's triggers again.
module Caller {
  import Callee

  function {:autoReq} G(c: bool, d: bool): int {
    Callee.F(c && d)
  }

  method Call(c: bool)
    requires forall x :: Callee.P(x) ==> c
  {
    var y := G(c, false); // error: precondition might not hold
  }
}
