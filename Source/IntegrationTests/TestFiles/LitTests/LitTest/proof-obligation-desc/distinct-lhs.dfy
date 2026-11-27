// RUN: %exits-with 4 %verify --show-proof-obligation-expressions "%s" > "%t"
// RUN: %diff "%s.expect" "%t"

method AssignArray(i: nat, j: nat, a: array<int>, x: int)
    requires 0 <= i < a.Length
    requires 0 <= j < a.Length
    modifies a
{
  a[i], a[j] := x, x + 1;
}
 
method AssignMultiArray(i0: nat, i1: nat, j0: nat, j1: nat, a: array2<int>, x: int)
    requires 0 <= i0 < a.Length0
    requires 0 <= i1 < a.Length1
    requires 0 <= j0 < a.Length0
    requires 0 <= j1 < a.Length1
    modifies a
{
     a[i0, i1], a[j0, j1] := x, x + 1;
}

class C { var f: int }
method AssignField(c: C, x: int)
    modifies c
{
    c.f, c.f := x, x + 1;
}

datatype Res<T> = Ok(v: T) | Fail {
  predicate IsFailure() { Fail? }
  function PropagateFailure<U>(): Res<U> requires IsFailure() { Fail }
  function Extract(): T requires !IsFailure() { v }
}
method Pair() returns (r: Res<int>, y: int)
method AssignOrReturn(b: bool, c: C, e: C) returns (r: Res<int>)
    modifies c, e
{
  match b
  case true =>
    c.f, e.f :- Pair();
    r := Ok(0);
  case false =>
    c.f, e.f :- Ok(1), 2;
    r := Ok(0);
}
