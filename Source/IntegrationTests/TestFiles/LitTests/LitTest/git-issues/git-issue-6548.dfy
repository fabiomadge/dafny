// RUN: %testDafnyForEachCompiler "%s"

// Tail calls reassign the receiver of a tail-recursive member. A Java lambda cannot capture a
// variable that is reassigned, and the quantifiers, comprehensions, and let expressions below are
// compiled into Java lambdas. In any target language, a lambda that outlives the iteration that
// created it must not capture the receiver by reference.

datatype Tree = Nil | Tree(trunk: Tree, branches: set<Tree>)
{
  predicate HasSubtree(other: Tree)
  {
    match this {
      case Nil => other.Nil?
      case Tree(trunk, branches) =>
        this == other ||
        trunk.HasSubtree(other) ||
        exists b | b in branches :: b.HasSubtree(other)
    }
  }

  // Ascends the trunk as far as possible without passing a subtree
  function ShortTrunk(other: Tree): Tree
    requires HasSubtree(other)
  {
    if this == other then
      this
    else if exists b | b in branches :: b.HasSubtree(other) then
      this
    else
      trunk.ShortTrunk(other)
  }
}

const Digits: set<nat> := {0, 1, 2, 3, 4}

class C {
  var data: nat

  constructor (data: nat) {
    this.data := data;
  }

  function Loop(n: nat, acc: int): int
    reads this
  {
    if n == 0 then
      acc
    else
      var b := forall i | i in Digits :: i <= this.data + 4;
      var s := set i | i in Digits && i <= this.data;
      var m := map i | i in Digits && i <= this.data :: this;
      var z :| z in {this.data};
      Loop(n - 1, acc + (if b then 1 else 0) + |s| + |m| + z)
  }

  method CountUp(n: nat, acc: int) returns (r: int) {
    if n == 0 {
      return acc;
    }
    var b := exists i | i in Digits :: i == this.data;
    r := CountUp(n - 1, acc + if b then 1 else 0);
  }
}

datatype Option<T> = None | Some(value: T)

datatype D = D(f: int) {
  // The lambdas outlive the iterations that create them
  function Last(n: nat, acc: () -> int): int
    decreases n
  {
    if n == 0 then acc() else D(f + 1).Last(n - 1, () => n * 10 + this.f)
  }

  function LetInLambda(n: nat, acc: int): int {
    if n == 0 then acc else LetInLambda(n - 1, acc + (() => (var z := n; z + this.f))())
  }

  function Patterns(n: nat, acc: int): int {
    if n == 0 then
      acc
    else
      Patterns(n - 1, acc + (var (a, b) := (n, 1); a + b + this.f) + match Some(n) { case Some(v) => v + this.f case None => 0 })
  }
}

trait T {
  function Value(): int

  function Count(n: nat, acc: int): int {
    if n == 0 then acc else Count(n - 1, acc + |set i | i in Digits && i <= this.Value()|)
  }
}

class K extends T {
  constructor () {}

  function Value(): int { 2 }
}

newtype N = x: int | 0 <= x < 10 {
  function Count(n: nat, acc: int): int {
    if n == 0 then acc else Count(n - 1, acc + (if exists i | i in Digits :: i == this as int then 1 else 0) + (() => this as int)())
  }
}

method Main() {
  var leaf := Tree(Nil, {});
  var t := Tree(Tree(leaf, {}), {});
  var u := Tree(Nil, {leaf});
  print t.ShortTrunk(leaf) == leaf, " ", u.ShortTrunk(leaf) == u, "\n"; // true true

  var c := new C(2);
  var r := c.CountUp(3, 0);
  print c.Loop(3, 0), " ", r, "\n"; // 27 3

  print D(0).Last(3, () => -1), " ", D(2).LetInLambda(3, 0), " ", D(2).Patterns(3, 0), "\n"; // 12 12 27

  var k := new K();
  var x: N := 2;
  print k.Count(3, 0), " ", x.Count(3, 0), "\n"; // 9 9
}
