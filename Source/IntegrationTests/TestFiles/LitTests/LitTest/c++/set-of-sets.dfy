// RUN: %testDafnyForEachCompiler --refresh-exit-code=0 "%s" -- --relax-definite-assignment --spill-translation --allow-deprecation --unicode-char false

// Sets and maps built in different orders are equal, so each is found in a set holding the other.

newtype i32 = x: int | -0x8000_0000 <= x < 0x8000_0000

method Main() {
  var a: set<i32> := {1, 2};
  var b: set<i32> := {2, 1};
  var m: map<i32, i32> := map[1 := 1, 2 := 2];
  var n: map<i32, i32> := map[2 := 2, 1 := 1];
  print b in {a}, " ", n in {m}, "\n";
}
