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
