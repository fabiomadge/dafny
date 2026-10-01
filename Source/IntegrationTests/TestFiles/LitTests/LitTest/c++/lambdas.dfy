// RUN: %testDafnyForEachCompiler --refresh-exit-code=0 "%s" -- --relax-definite-assignment --spill-translation --allow-deprecation --unicode-char false

newtype i32 = x: int | -0x8000_0000 <= x < 0x8000_0000

method Main() {
  // A function value stored in a variable and applied.
  var inc: i32 -> i32 := (n: i32) => if n < 0x7fff_ffff then n + 1 else n;
  print inc(41), "\n";

  // Two parameters.
  var eq: (i32, i32) -> bool := (a: i32, b: i32) => a == b;
  print eq(21, 21), " ", eq(21, 22), "\n";

  // A function value passed to another function.
  var twice := ApplyTwice(inc, 40);
  print twice, "\n";

  // A lambda captures collections when it is created, and applies their operations.
  var s: set<i32> := {1};
  var q: seq<i32> := [1];
  var m: map<i32, i32> := map[1 := 2];
  var t: (i32, i32) := (3, 4);
  var c := Two(5);
  var ops := (n: i32) =>
    n in s + {2} && n in s * {1} && n !in s - {1} && s < {1, 2} && n in (set y | y in s) &&
    q + [n] == [1, n] &&
    n in m.Keys && 2 in m.Values && m[n := 3][n] == 3 && n in m + map[4 := 5] && n !in m - {n} &&
    t.1 == 4 && c.v == 5;
  s, q, m := {}, [], map[];
  print ops(1), " ", ops(2), "\n";

  // The default function value returns the default result.
  var d: i32 -> i32;
  print d(5), "\n";

  // A lambda that ignores its parameter.
  var zero: i32 -> i32 := _ => 0;
  print zero(9), "\n";

  // A match inside an expression compiles to a C++ lambda too.
  print (match c case One => 0 case Two(v) => v) + 1, "\n";
}

datatype Choice = One | Two(v: i32)

function ApplyTwice(f: i32 -> i32, x: i32): i32 {
  f(f(x))
}
