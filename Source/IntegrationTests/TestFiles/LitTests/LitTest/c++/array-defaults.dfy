// RUN: %testDafnyForEachCompiler --refresh-exit-code=0 "%s" -- --allow-deprecation --unicode-char false

// A new array's elements are values of its element type: here the default function, also inside a generic
// datatype, and the witness.

newtype i32 = x: int | -0x8000_0000 <= x < 0x8000_0000
type Pos = x: i32 | x > 0 witness 1
datatype D<T> = D(a: T)

method Main() {
  var f := new (i32 -> i32)[2];
  var b := new D<i32 -> bool>[1];
  var c := new D<i32 -> char>[1];
  var p := new Pos[2];
  print f[1](5), " ", b[0].a(5), " ", c[0].a(5) == 'D', " ", p[1], "\n";
}
