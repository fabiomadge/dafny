// NONUNIFORM: Rust runtime regression test
// RUN: %baredafny run --target=rs --enforce-determinism "%s" > "%t"
// RUN: %diff "%s.expect" "%t"

method Main() {
  var dropped := Build(100000);
  print |dropped|, "\n";
  var indexed := Build(100000);
  print indexed[99999], "\n";
}

method Build(n: nat) returns (s: seq<int>)
  ensures |s| == n
{
  s := [];
  for i := 0 to n
    invariant |s| == i
  {
    s := s + [i];
  }
}
