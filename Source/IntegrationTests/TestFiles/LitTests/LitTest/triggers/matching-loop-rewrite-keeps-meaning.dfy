// RUN: %exits-with 4 %verify --allow-warnings "%s" > "%t"
// RUN: %diff "%s.expect" "%t"

// To break a matching loop, the trigger generator replaces a term such as i + c.f below with a new bound variable,
// which the quantifier's range defines in the current state. Where the same term is read in another state, or is only
// equal on the surface, it means something else and must stay, so no assertion false below can be proved, although
// each would follow from the assumptions if the term were replaced. All assumptions are satisfiable.

class C { var f: int }
class D { var g: int }
trait T {}
class A extends T {}
class B extends T {}
function F(x: int): int
function F2(x: int, y: int): int
function G8(x: bv8): bv8
function Size<X>(): int
twostate function Old(c: C): int reads c { old(c.f) }
function Lam(i: int): int ~> int
predicate P(j: int)

method InOld(c: C)
  requires c.f == 0
  modifies c
{
  c.f := 1;
  assume {:axiom} F(0) == 7 && F(1) == 0;
  assume {:axiom} forall i :: F(i) <= F(i + c.f) || old(F(i + c.f)) == 7;
  assert false;
}

method InLambda(c: C)
  modifies c
{
  c.f := 1;
  assume {:axiom} F(0) == 7 && F(1) == 0;
  assume {:axiom} forall i :: F(i) <= F(i + c.f) || Lam(i) == ((x: int) reads c => F(i + c.f));
  c.f := 0;
  assume {:axiom} Lam(0).requires(0) && Lam(0)(0) == 7;
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
  assume {:axiom} forall i :: F(i) <= F(i + Old@L(c)) || F(i + Old(c)) == 7;
  assert false;
}

method FreshAtLabel() {
  var c := new C;
  label L:
  assume {:axiom} F(0) == 7 && F(1) == 0;
  assume {:axiom} forall i :: F(i) <= F(i + (if fresh(c) then 1 else 0)) || F(i + (if fresh@L(c) then 1 else 0)) == 7;
  assert false;
}

method TypeArguments() {
  assume {:axiom} F(0) == 7 && F(1) == 0 && Size<int>() == 1 && Size<bool>() == 0;
  assume {:axiom} forall i :: F(i) <= F(i + Size<int>()) || F(i + Size<bool>()) == 7;
  assert false;
}

method TypeTests(o: T)
  requires o is B
{
  assume {:axiom} F(0) == 7 && F(1) == 7 && F(2) == 0;
  assume {:axiom} forall i :: F(i) <= F(if o is A then i + 1 else i + 2) || F(if o is B then i + 1 else i + 2) == 7;
  assert false;
}

method LiteralTypes(b: bool) {
  assume {:axiom} forall i, k :: F2(i, k) <= F2(i + 1, if b then 1 else 0) || G8(if b then 1 else 0) == 3;
  assert false;
}

// The term occurs only inside the lambda, so the quantifier, whose range would then read c.f against the predicate's
// reads clause, must not define a variable for it.
ghost predicate OnlyInLambda(c: C, d: D)
  reads d
{
  forall i :: F(i) <= F(i + 1) || Lam(i) == ((x: int) reads c => F(i + c.f))
}

method UsesOnlyInLambda(c: C, d: D)
  requires c.f == 0
  modifies c
{
  assume {:axiom} F(0) == 7 && F(1) == 0;
  assume {:axiom} OnlyInLambda(c, d);
  c.f := 1;
  assert OnlyInLambda(c, d);
  assume {:axiom} Lam(0).requires(0);
  ghost var v := Lam(0)(0);
  assert false;
}

// The nested quantifier binds the new variable for i + 1 as well, which the enclosing quantifier still needs.
method NestedQuantifier(s: seq<int>)
  requires forall i :: 0 <= i < |s| - 1 ==> s[i] <= s[i + 1] || (forall j :: 0 <= j < i ==> s[j] == 0)
{
}

// The term occurs only in the nested quantifier, which binds the variable for it, so the enclosing one must not.
ghost function NestedOnly(k: int): bool {
  forall i :: F(i) <= k || (forall j :: P(j) ==> F(i + 1) > j)
}

lemma UseNestedOnly()
  requires NestedOnly(0)
  ensures NestedOnly(0)
{
}
