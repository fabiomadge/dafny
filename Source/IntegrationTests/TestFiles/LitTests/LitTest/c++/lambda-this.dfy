// RUN: %testDafnyForEachCompiler --refresh-exit-code=0 "%s" -- --allow-deprecation --unicode-char false

// Lambdas over `this`.

newtype i32 = x: int | -0x8000_0000 <= x < 0x8000_0000

class Counter {
  var k: i32
  const plus: i32 ~> i32 := x reads this => if -100 < x < 100 && -100 < k < 100 then x + k else 0
  constructor(k: i32) ensures this.k == k { this.k := k; }
  function Adder(): i32 ~> i32 reads this {
    x reads this => if -100 < x < 100 && -100 < k < 100 then x + k else 0
  }
  function Self(): () -> Counter { () => this }
  function Let(): i32 ~> i32 reads this {
    x reads this => var y := x; if -100 < y < 100 && -100 < k < 100 then y + k else 0
  }
  function Id(): i32 ~> i32 reads this { x reads this => x }
}

class Cell<T> {
  var v: T
  constructor(v: T) ensures this.v == v { this.v := v; }
  function Get(): () ~> T reads this { () reads this => v }
}

method MakeAdder() returns (f: i32 ~> i32)
  ensures f.requires(4)
{
  var c := new Counter(3);
  f := c.Adder();
}

method MakePlus() returns (f: i32 ~> i32)
  ensures f.requires(4)
{
  var c := new Counter(3);
  f := c.plus;
}

method Main() {
  // Lambdas that outlive every other reference to their object: one that a function returns, and one that an
  // instance const holds. The Counters made after each take the memory of a freed Counter, if there is one.
  var add := MakeAdder();
  var other := new Counter(50);
  var plus := MakePlus();
  var another := new Counter(60);
  print add(4), " ", plus(4), "\n";

  // A lambda that returns `this`.
  print other.Self()() == other, "\n";

  // A lambda whose let body uses `this`, and one that mentions `this` only in its reads clause.
  print other.Let()(4), " ", other.Id()(4), "\n";

  // A lambda over `this` in a generic class.
  var cell := new Cell<i32>(9);
  var get := cell.Get();
  print get(), "\n";
}
