// RUN: %testDafnyForEachCompiler "%s"

// The lower bound is -129, so T needs more than 8 bits
newtype T = x: int | -129 + (-4 % 2) <= x < 100

method Main() {
  var t: T := -128;
  t := t - 1;
  print t, "\n";
}
