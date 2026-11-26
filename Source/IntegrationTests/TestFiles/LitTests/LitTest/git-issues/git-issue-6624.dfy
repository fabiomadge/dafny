// RUN: %exits-with 4 %verify "%s" > "%t"
// RUN: %diff "%s.expect" "%t"
// RUN: %exits-with 4 %verify --type-system-refresh=false --general-newtypes=false "%s" > "%t"
// RUN: %diff "%s.expect" "%t"

datatype Res<T> = Ok(v: T) | Fail {
  predicate IsFailure() { Fail? }
  function PropagateFailure<U>(): Res<U> requires IsFailure() { Fail }
  function Extract(): T requires !IsFailure() { v }
}

class Cell { var f: int }

method Pair() returns (r: Res<int>, y: int)

// The LHS that receives Extract() must differ from the other LHSs, even if the values are equal.
method ExpressionList(c: Cell, e: Cell) returns (r: Res<int>)
  requires c != e
  modifies c, e
{
  c.f, e.f :- Ok(1), 2;
  var x: int;
  x, x :- Ok(1), 1; // error
  r := Ok(x);
}

// Also in a match case, for a receiver declared in the case.
method InMatch(b: bool, e: Cell) returns (r: Res<int>)
  modifies e
{
  match b
  case true =>
    var c := e;
    c.f, e.f :- Pair(); // error
    r := Ok(0);
  case false =>
    var c := e;
    c.f, e.f :- Ok(1), 2; // error
    r := Ok(0);
}
