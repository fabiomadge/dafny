// RUN: %exits-with 4 %verify "%s" > "%t"
// RUN: %diff "%s.expect" "%t"

datatype Res<T> = Ok(v: T) | Fail {
  predicate IsFailure() { Fail? }
  function PropagateFailure<U>(): Res<U> requires IsFailure() { Fail }
  function Extract(): T requires !IsFailure() { v }
}

class Cell { var f: int }

method Pair() returns (r: Res<int>, y: int)

// The LHS that receives Extract() must differ from the other LHSs also in a match case.
method Aliased(b: bool, e: Cell) returns (r: Res<int>)
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

// No error for distinct locations, also when the receiver of that LHS is a match or :| expression.
method Distinct(b: bool, c: Cell, e: Cell) returns (r: Res<int>)
  requires c != e
  modifies c, e
{
  match b
  case true =>
    (match b case true => c case false => c).f, e.f :- Ok(1), 2;
    r := Ok(0);
  case false =>
    (var z :| z == c; z).f, e.f :- Ok(1), 2;
    r := Ok(0);
}
