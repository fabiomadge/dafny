// RUN: %testDafnyForEachCompiler --refresh-exit-code=0 "%s" -- --allow-deprecation --unicode-char false

// Instance, static and generic functions used as values.

newtype i32 = x: int | -0x8000_0000 <= x < 0x8000_0000

class C {
  var k: i32
  constructor(k: i32) ensures this.k == k { this.k := k; }
  function Get(x: i32): i32 reads this { if -100 < x < 100 && -100 < k < 100 then x + k else 0 }
  // C++ can't deduce T from the arguments.
  function Empty<T>(): seq<T> { [] }
  method Self() returns (f: i32 ~> i32) ensures f.requires(1) { f := Get; }
}

class Box<T> {
  var v: T
  constructor(v: T) ensures this.v == v { this.v := v; }
  function Get(): T reads this { v }
  static function Same(x: T): T { x }
  method Read() returns (r: T) { var f := Get; r := f(); }
}

function Id<T>(x: T): T { x }

// Function values that outlive every other reference to their object.
method MakeGetter() returns (f: i32 ~> i32)
  ensures f.requires(1)
{
  var c := new C(10);
  f := c.Get;
}

method MakeSelf() returns (f: i32 ~> i32)
  ensures f.requires(1)
{
  var c := new C(20);
  f := c.Self();
}

method Main() {
  var getter := MakeGetter();
  var self := MakeSelf();
  // Takes the memory of a freed C, if there is one.
  var other := new C(50);
  print getter(1), " ", self(1), "\n";

  var c := new C(3);
  var empty := c.Empty<bool>;
  var id := Id<i32>;
  var same := Box<i32>.Same;
  var box := new Box<i32>(7);
  var read := box.Read();
  print empty() == [], " ", id(5), " ", same(8), " ", read, "\n";
}
