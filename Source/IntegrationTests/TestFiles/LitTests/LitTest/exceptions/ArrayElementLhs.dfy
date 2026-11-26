// RUN: %verify "%s" > "%t"
// RUN: %diff "%s.expect" "%t"

datatype Res<T> = Ok(v: T) | Fail {
  predicate IsFailure() { Fail? }
  function PropagateFailure<U>(): Res<U> requires IsFailure() { Fail }
  function Extract(): T requires !IsFailure() { v }
}

// An array element can receive the result of Extract().
method M(a: array<int>, m: array2<int>) returns (r: Res<int>)
  requires a.Length > 0 && m.Length0 > 0 && m.Length1 > 0
  modifies a, m
{
  a[0] :- Ok(1);
  m[0, 0] :- Ok(2);
  assert a[0] == 1 && m[0, 0] == 2;
  r := Ok(0);
}
