// RUN: %testDafnyForEachCompiler --refresh-exit-code=0 "%s" -- --relax-definite-assignment --spill-translation --allow-deprecation --unicode-char false

// A generic class instantiated with a function type.

newtype i32 = x: int | -0x8000_0000 <= x < 0x8000_0000

class Box<T> {
  var v: T
  constructor(v: T) ensures this.v == v { this.v := v; }
  method Swap(w: T) returns (old_v: T) modifies this {
    old_v := v;
    v := w;
  }
}

method Main() {
  var b := new Box<i32 -> i32>(x => if x < 100 then x + 1 else x);
  var o := b.Swap(x => if x < 100 then x + 2 else x);
  print o(1), " ", b.v(1), "\n";
}
