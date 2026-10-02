// RUN: %testDafnyForEachCompiler "%s" -- --allow-deprecation --unicode-char false

// The u8 newtype and --unicode-char false keep C++ from being skipped.

newtype u8 = x: int | 0 <= x < 256

method Main() {
  var a: set<u8> := {1, 2, 3};
  var b: set<u8> := {3, 2, 1};
  print |{a, b}|, "\n";

  var c: map<u8, u8> := map[1 := 10, 2 := 20, 3 := 30];
  var d: map<u8, u8> := map[3 := 30, 2 := 20, 1 := 10];
  print |{c, d}|, "\n";
}
