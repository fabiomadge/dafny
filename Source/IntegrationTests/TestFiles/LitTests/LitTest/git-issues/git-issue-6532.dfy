// RUN: %exits-with 4 %verify "%s" > "%t"
// RUN: %diff "%s.expect" "%t"

type Empty = x: int | false witness *

function Never(): bool
  requires false
  ensures false
{ false }

lemma Candidate()
  ensures false
{
  forall x: Empty
    ensures Never()
  { }
  assert Never(); // error: (but this was once provable, due to a bug)
}

lemma ViaLambda()
  ensures false
{
  var f := (x: Empty) => Never();
  assert Never(); // error: (but this was once provable, due to a bug)
}

// Control: over a type that is not empty, the precondition is checked
type NonEmpty = x: int | x == 0 witness 0

lemma Control()
  ensures false
{
  forall x: NonEmpty
    ensures Never() // error: function precondition
  { }
  assert Never();
}
