// NONUNIFORM: Rust runtime regression test
// RUN: %baredafny run --target=rs --enforce-determinism "%s" > "%t"
// RUN: %diff "%s.expect" "%t"

method Main() {
  var s: seq<int> := [];
  for i := 0 to 100000
    invariant |s| == i
  {
    s := s + [i];
  }
  print s[99999], "\n";
}
