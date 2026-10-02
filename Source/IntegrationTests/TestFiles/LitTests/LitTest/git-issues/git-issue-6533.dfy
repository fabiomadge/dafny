// RUN: %exits-with 4 %verify "%s" > "%t"
// RUN: %diff "%s.expect" "%t"

// After the forall statement, the range's call facts (t.n is defined, so t was built by T)
// hold only of values of type T. Of r, which is an R, they would contradict its constructor;
// {r} brings r into play.

datatype T = T(n: nat)
datatype R = X | Y(k: nat)

method M(a: array<int>, s: set<T>, r: R)
  requires a.Length == 10
  modifies a
  ensures false // error: (but this was once provable, due to a bug)
{
  forall t: T | t.n < 10 && t in s {
    a[t.n] := 0;
  }
  var rs := {r};
}
