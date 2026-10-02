// RUN: %exits-with 4 %verify "%s" > "%t"
// RUN: %diff "%s.expect" "%t"

// Opt<int> and Opt<bool> values share a Boogie type, so the solver may instantiate the second
// precondition at x, y and z, which unboxes 0, 1 and 2 as bools.
datatype Opt<T> = None | Some(v: T)

function F(b: bool): int { if b then 1 else 0 }

lemma Bad(x: Opt<int>, y: Opt<int>, z: Opt<int>)
  requires x == Some(0) && y == Some(1) && z == Some(2)
  requires forall o: Opt<bool> :: o.Some? ==> F(o.v) <= 1
  ensures false // error: must not be provable
{
  assert x.v == 0 && y.v == 1 && z.v == 2;
}

// Each postcondition is about the box of the value just stored in a field.
class Node {
  var next: Node?
  constructor ()
  {
    next := null;
  }
}

class Queue {
  var head: Node
  ghost var spine: set<Node>

  constructor ()
    ensures head in spine
  {
    var n := new Node();
    head := n;
    spine := {n};
  }
}

class Booleans {
  var b: bool
  ghost var bs: set<bool>

  constructor (c: bool)
    ensures b in bs
  {
    b := c;
    bs := {c};
  }
}

// Field values of several types, boxed into collections.
class Cell {
  var i: int
  var b: bool
  var next: Cell?
}

method Vacuity(c: Cell)
  modifies c
{
  c.i := c.i + 1;
  c.b := !c.b;
  var s: seq<int> := [c.i];
  var t: set<bool> := {c.b};
  var u: set<Cell?> := {c.next};
  assert s[0] == c.i && c.b in t && c.next in u;
  assert false; // error: must not be provable
}
