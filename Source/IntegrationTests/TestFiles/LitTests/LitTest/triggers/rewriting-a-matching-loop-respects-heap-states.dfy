// RUN: %exits-with 4 %verify --show-hints --allow-warnings "%s" > "%t"
// RUN: %diff "%s.expect" "%t"
// RUN: %resolve --rprint:- "%s" > "%t.rprint"
// RUN: %OutputCheck --file-to-check "%t.rprint" "%s"

// To break a matching loop, the trigger generator replaces a term such as i + c.f with a new bound variable, which
// the quantifier's range defines in the current state. Where the same term is read in another state, it means
// something else and must stay, so each assertion false below is unprovable. Each assumption holds for F(0) == 7 and
// F(x) == 0 elsewhere.

class C { var f: int }
function F(x: int): int
twostate function G(c: C): int reads c { old(c.f) }

method InOld(c: C)
  requires c.f == 0
  modifies c
{
  c.f := 1;
  assume {:axiom} F(0) == 7 && F(1) == 0;
  assume {:axiom} forall i :: F(i) <= F(i + c.f) || old(F(i + c.f)) == 7;
  assert false;
}

method OldAtLabel(c: C)
  requires c.f == 0
  modifies c
{
  c.f := 1;
  label L:
  c.f := 2;
  assume {:axiom} F(0) == 7 && F(1) == 0;
  assume {:axiom} forall i :: F(i) <= F(i + old@L(c.f)) || F(i + old(c.f)) == 7;
  assert false;
}

method TwoStateAtLabel(c: C)
  requires c.f == 0
  modifies c
{
  c.f := 1;
  label L:
  c.f := 2;
  assume {:axiom} F(0) == 7 && F(1) == 0;
  assume {:axiom} forall i :: F(i) <= F(i + G@L(c)) || F(i + G(c)) == 7;
  assert false;
}

method FreshAtLabel() {
  var c := new C;
  label L:
  assume {:axiom} F(0) == 7 && F(1) == 0;
  assume {:axiom} forall i :: F(i) <= F(i + (if fresh(c) then 1 else 0)) || F(i + (if fresh@L(c) then 1 else 0)) == 7;
  assert false;
}

// A term that does not read the heap means the same in old, so it is still replaced there.
// CHECK: .*old\(c\.f \+ F\(_t#0\)\) == 7;
method InOldWithoutHeap(c: C) {
  assume {:axiom} forall i :: F(i) <= F(i + 1) || old(c.f + F(i + 1)) == 7;
}
