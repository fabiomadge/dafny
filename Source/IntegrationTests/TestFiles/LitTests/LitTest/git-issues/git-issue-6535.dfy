// RUN: %exits-with 4 %verify "%s" > "%t"
// RUN: %diff "%s.expect" "%t"

lemma Bad(k: int)
  ensures false // error: (but this was once provable, due to a bug)
{
  var s: set<int> := {};
  var m1 := map x: int | x in s :: 1;
  var m2 := map x: int | x in s :: 2;
  assert m1 == m2; // both are empty
  var e := if k in m1 then m1[k] else 1; // a lookup outside the domain, never executed
}
