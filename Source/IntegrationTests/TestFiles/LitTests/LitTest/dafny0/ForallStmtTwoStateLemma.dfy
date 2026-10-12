// RUN: %exits-with 4 %verify "%s" > "%t"
// RUN: %diff "%s.expect" "%t"

class C { var f: int }
function F(x: int): int

twostate lemma L(c: C, x: int)
  requires old(c.f) == 1 && F(x) == 1
  ensures F(x) == old(c.f)
{
}

// Each call's "old" is the method's entry, where c.f == 1, so the forall statement gives F(0) == 1
method Unlabeled(c: C)
  requires c.f == 1
  modifies c
{
  c.f := 0;
  assume {:axiom} F(0) == 1;
  forall x | 0 <= x < 1 && F(x) == 1 {
    L(c, x);
  }
  assert F(0) == 1;
  assert false; // error
}

// With a label, "old" is the state at the label, where c.f == 1
method Labeled(c: C)
  requires c.f == 0
  modifies c
{
  c.f := 1;
  label A:
  c.f := 0;
  assume {:axiom} F(0) == 1;
  forall x | 0 <= x < 1 && F(x) == 1 {
    L@A(c, x);
  }
  assert F(0) == 1;
  assert false; // error
}

lemma K(c: C, x: int)
  requires F(x) == c.f
  ensures F(x) == old(c.f)
{
}

// An ordinary lemma's "old" is the state before the forall statement, where c.f == 0
method Ordinary(c: C)
  requires c.f == 1
  modifies c
{
  c.f := 0;
  assume {:axiom} F(0) == 0;
  forall x | 0 <= x < 1 && F(x) == 0 {
    K(c, x);
  }
  assert false; // error
}

twostate lemma Same(a: array<int>, i: int)
  requires 0 <= i < a.Length && unchanged(a)
  ensures old(a[i]) == a[i]
{
}

// The argument c.f + x is evaluated where the call is, where c.f == 1, so the forall statement gives a[1] == a[1]
method Argument(a: array<int>, c: C)
  requires a.Length == 2 && a[0] == 0 && a[1] == 1 && c.f == 0
  modifies c
{
  c.f := 1;
  forall x | x == 0 {
    Same(a, c.f + x);
  }
  assert false; // error
}

lemma Holds(b: bool, x: int)
  requires b
  ensures b
{
}

// In an argument, "fresh" refers to the method's entry, where o did not exist, so the forall statement gives true
method FreshArgument() {
  var o := new C;
  forall x | x == 0 {
    Holds(fresh(o), x);
  }
  assert false; // error
}

ghost predicate T(x: Node?, n: int) { true }

class Node {
  var next: Node?

  // The induction hypothesis covers only receivers allocated in the previous state, so instantiating it at next,
  // which the assertion does, does not give !fresh(next)
  twostate lemma {:induction this, n} InductionOnReceiver(n: nat)
    requires n != 0 ==> next != null && fresh(next)
    ensures T(this, n) && !fresh(this) && n == 0
    decreases n
  {
    if n != 0 { // error: n == 0 does not hold
      assert T(next, 0);
    }
  }
}

// The induction hypothesis covers only arguments allocated in the previous state, so instantiating it at x.next, which
// the assertion does, does not give !fresh(x.next)
twostate lemma {:induction x, n} InductionOnParameter(x: Node, n: nat)
  requires n != 0 ==> x.next != null && fresh(x.next)
  ensures T(x, n) && !fresh(x) && n == 0
  decreases n
{
  if n != 0 { // error: n == 0 does not hold
    assert T(x.next, 0);
  }
}

ghost function Count(n: nat): nat {
  if n == 0 then 0 else 1 + Count(n - 1)
}

// A "new" parameter need not be allocated in the previous state, so the induction hypothesis covers o, at which the
// assertion instantiates it
twostate lemma {:induction o, n} InductionOnNewParameter(new o: Node, n: nat)
  ensures T(o, n) && Count(n) == n
  decreases n
{
  if n != 0 {
    assert T(o, n - 1);
  }
}

ghost predicate G(n: int) { true }

// In the induction hypothesis, "old" is the lemma's previous state, so instantiating it at n - 1, which the assertion
// does, does not give c.f == 1
twostate lemma {:induction n} InductionOld(c: C, n: nat)
  requires old(c.f) == 1
  ensures G(n) && old(c.f) == 1 && (n == 0 || c.f == 1)
  decreases n
{
  if n != 0 { // error: c.f == 1 does not hold
    assert G(n - 1);
  }
}
