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

// Also in a match case.
method InMatch(b: bool, c: Cell, e: Cell) returns (r: Res<int>)
  modifies c, e
{
  var x: int;
  match b
  case true =>
    x, x :- Pair(); // error
    r := Ok(x);
  case false =>
    c.f, e.f :- Ok(1), 2; // error
    r := Ok(0);
}
