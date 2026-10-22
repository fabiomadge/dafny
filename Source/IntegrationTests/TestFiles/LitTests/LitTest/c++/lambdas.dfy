// RUN: %testDafnyForEachCompiler --refresh-exit-code=0 "%s" -- --relax-definite-assignment --spill-translation --allow-deprecation --unicode-char false

// Native newtypes only, since the c++ target rejects unbounded `int`.

newtype i32 = x: int | -0x8000_0000 <= x < 0x8000_0000

method Main() {
  // A function value stored in a variable and applied.
  var inc: i32 -> i32 := (n: i32) => if n < 0x7fff_ffff then n + 1 else n;
  print inc(41), "\n";

  // A predicate (lambda returning bool).
  var pos: i32 -> bool := (n: i32) => n > 0;
  print pos(4), " ", pos(-7), "\n";

  // Two arguments, with a bool lambda to avoid overflow reasoning.
  var eq: (i32, i32) -> bool := (a: i32, b: i32) => a == b;
  print eq(21, 21), " ", eq(21, 22), "\n";

  // A function value passed to another function.
  var twice := ApplyTwice(inc, 40);
  print twice, "\n";

  // A lambda captures `s` when it is created, and applies a set operation to it.
  var s: set<i32> := {1};
  var inS := (n: i32) => n in s + {2};
  s := {};
  print inS(1), " ", inS(2), " ", inS(3), "\n";

  // The default function value returns the default result.
  var d: i32 -> i32;
  print d(5), "\n";

  // A lambda that ignores its parameter.
  var zero: i32 -> i32 := _ => 0;
  print zero(9), "\n";

  // A datatype with a function-typed field.
  var op := Op(inc, 1);
  print op.f(op.n), "\n";

  // A lambda over `this` outlives every other reference to its object.
  var add := MakeAdder();
  var other := new Counter(50);
  print add(4), "\n";

  // An instance const holding a lambda over `this`.
  print other.plus(4), "\n";

  // A lambda over `this` in a generic class.
  var cell := new Cell<i32>(9);
  var get := cell.Get();
  print get(), "\n";
}

class Cell<T> {
  var v: T
  constructor(v: T) ensures this.v == v { this.v := v; }
  function Get(): () ~> T reads this { () reads this => v }
}

datatype Op = Op(f: i32 -> i32, n: i32)

class Counter {
  var k: i32
  const plus: i32 ~> i32 := x reads this => if -100 < x < 100 && -100 < k < 100 then x + k else 0
  constructor(k: i32) ensures this.k == k { this.k := k; }
  function Adder(): i32 ~> i32 reads this {
    x reads this => if -100 < x < 100 && -100 < k < 100 then x + k else 0
  }
}

method MakeAdder() returns (f: i32 ~> i32)
  ensures f.requires(4)
{
  var c := new Counter(3);
  f := c.Adder();
}

function ApplyTwice(f: i32 -> i32, x: i32): i32 {
  f(f(x))
}
