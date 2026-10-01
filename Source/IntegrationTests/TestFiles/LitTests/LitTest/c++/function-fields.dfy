// RUN: %testDafnyForEachCompiler --refresh-exit-code=0 "%s" -- --allow-deprecation --unicode-char false

// Values that hold functions.

newtype i32 = x: int | -0x8000_0000 <= x < 0x8000_0000

datatype Op = Op(f: i32 -> i32, n: i32)
datatype Opt<T> = None | Some(v: T)

class Box<T> {
  var v: T
  constructor(v: T) ensures this.v == v { this.v := v; }
}

method Main() {
  var inc: i32 -> i32 := n => if n < 0x7fff_ffff then n + 1 else n;

  var op := Op(inc, 1);
  var b := new Box<i32 -> i32>(inc);
  print op.f(op.n), " ", b.v(2), "\n";

  // Compared with values that hold no functions, the only comparisons Dafny allows.
  var o: Opt<i32 -> i32> := Some(inc);
  var fs: seq<i32 -> i32> := [inc];
  print o == None, " ", fs == [], "\n";
}
