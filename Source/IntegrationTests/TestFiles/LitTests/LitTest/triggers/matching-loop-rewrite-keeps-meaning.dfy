// RUN: %exits-with 4 %verify --allow-warnings "%s" > "%t"
// RUN: %diff "%s.expect" "%t"

// To break a matching loop, the trigger generator replaces a term with a new variable, which the quantifier's range
// defines outside the term's guards and possibly in another state. Each assertion false below would follow if it
// replaced the term in question, and all assumptions are satisfiable.

class C { var f: int }
newtype Byte = x | 0 <= x < 256
function F(x: int): int
function F2(x: int, y: int): int
function G(x: Byte): int
function G8(x: bv8): bv8
function Half(x: int): int
  requires 0 <= x
  ensures 0 <= Half(x) <= x
{
  x / 2
}
predicate NonNeg(x: int) { 0 <= x }
ghost predicate P(j: int)

// old reads c.f in another state
method InOld(c: C)
  requires c.f == 0
  modifies c
{
  c.f := 1;
  assume {:axiom} F(0) == 7 && F(1) == 0;
  assume {:axiom} forall i :: F(i) <= F(i + c.f) || old(F(i + c.f)) == 7;
  assert false;
}

// The range would assume that Half's precondition holds for every i
method CanCall() {
  assume {:axiom} F(0) == 0 && F(-1) == 0;
  assume {:axiom} forall i :: NonNeg(i) ==> F(i) <= F(i + Half(i));
  assert false;
}

ghost function Lam(i: int): int ~> int

// The lambda reads c.f when it is applied, after c.f changed
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

lemma Lem(c: C, x: int)
  requires c.f == 0
  ensures F(x) <= F(x + old(c.f))
{
}

// In the forall statement's postcondition, old is the state before the statement, but not in its range
method InForallStatement(c: C)
  requires c.f == 1
  modifies c
{
  c.f := 0;
  assume {:axiom} F(0) == 7 && F(1) == 0;
  forall x | 0 <= x < 1 {
    Lem(c, x);
  }
  assert false;
}

// The trigger generator's term equality ignores the labels of old
method OldLabels(c: C)
  modifies c
{
  c.f := 1;
  label A:
  c.f := 0;
  label B:
  assume {:axiom} F(0) == 7 && F(1) == 0;
  assume {:axiom} forall i :: F(i) <= F(i + old@A(c.f)) || F(i + old@B(c.f)) == 7;
  assert false;
}

// A variable of type Byte would make b + 1 a Byte also where it is not evaluated
method VariableType() {
  assume {:axiom} exists b: Byte :: (b == 255 || G(b) <= G(b + 1)) && b == 255;
  assert false;
}

// The int term if b then 1 else 0 is not the bv8 one
lemma LiteralTypes(b: bool)
  requires forall i, k :: F2(i, k) <= F2(i + 1, if b then 1 else 0) || G8(if b then 1 else 0) == 3
{
}

// The term may be replaced, so this quantifier gets no matching-loop warning
lemma Replaced(s: seq<int>, S: set<int>, M: multiset<int>, m: map<int, int>, a: array<int>, b: bool, r: real, x: bv8)
  requires forall i :: F(i) <= F(if !b && r < 1.0 && (!x & 1) == 0 then |s| + |S| - i else |M| * |m| - a.Length + i)
{
}

const Step := 2
datatype Window = Window(offset: int)

class Strided {
  const k: int
  const h: int := k + Step

  // Constants and destructors mean the same in every state, so the rewrite may replace the term and this quantifier
  // gets no matching-loop warning
  lemma Constants(w: Window, o: Strided)
    requires forall i :: F(i) <= F(i + Step + k + h + w.offset + o.h)
  {
  }
}

class Generic<T> {
  static const N: int := 3
}

// The initializer of o.h is known to be well-formed only for a non-null o, and the term equality may not tell
// Generic<int>.N from Generic<nat>.N, so the rewrite leaves these quantifiers as they are
lemma NotReplaced(o: Strided?)
  requires forall i :: o != null ==> F(i) <= F(i + o.h)
  requires forall i :: F(i) <= F(i + Generic<int>.N)
{
}

datatype Option<T> = None | Some(value: T)
datatype Px = Px(x: int)
datatype Qy = Qy(y: int)

// For None, the CanCall assumptions of p.value.x and q.value.y would say that one value is both a Px and a Qy, once
// F(0) instantiates the quantifier
lemma NestedDestructors(p: Option<Px>, q: Option<Qy>)
  requires p == None && q == None
  requires forall i :: p.Some? && q.Some? ==> F(i) <= F(i + p.value.x + q.value.y)
{
  var _ := F(0);
  assert false;
}

// Each part of the split quantifier binds its own new variable, and neither part gets a trigger
lemma SplitParts(s: seq<int>)
  requires forall i, j :: 0 <= j < |s| - 1 ==> F2(i, j) <= F2(i + 1, s[j + 1]) && F2(i, j) <= F2(i + 2, s[j + 1])
{
}

// Naming only i + 1 would leave no trigger, so the rewrite names neither term
lemma PartialNaming(c: C)
  requires forall i, j :: F2(i, j) <= F2(i + 1, c.f + j)
  ensures F2(0, 0) <= F2(1, c.f)
{
}

// The nested quantifier uses i + 1 too, but its own trigger would not mention a new variable that it bound, so the
// rewrite leaves it as it is
ghost predicate FirstDescent(a: seq<int>) {
  exists i :: 0 <= i < |a| - 1 && a[i] > a[i + 1] && (forall j {:trigger a[j]} :: 0 <= j < i ==> a[j] <= a[i + 1])
}

// The middle and the innermost quantifier both use x + 1, and each binds its own new variable for it
ghost predicate Deep() {
  forall x :: F(x) <= 0 || (forall y :: P(y) ==> F(x + 1) > 0 || (forall z :: P(z) ==> F(x + 1) > z))
}

// The induction hypothesis loops through n + Half(n), so it gets no triggers, although that term cannot be named
lemma {:induction n} Induction(n: nat)
  requires F(n) <= F(n + Half(n))
  ensures F(n) <= F(n + Half(n))
{
}

// The term occurs only in the nested quantifier, which binds the variable for it, so the enclosing one must not
ghost function NestedOnly(k: int): bool {
  forall i :: F(i) <= k || (forall j :: P(j) ==> F(i + 1) > j)
}

lemma UseNestedOnly()
  requires NestedOnly(0)
  ensures NestedOnly(0)
{
}

// The enclosing quantifier needs the new variable for i - 1, which the nested quantifier does not use, and in a function
// body, which the verifier substitutes into, the two quantifiers must not bind the same variable
ghost predicate Sorted(s: seq<int>) {
  forall i | 0 < i < |s| :: s[i - 1] <= s[i] || (forall m | 0 <= m < i :: s[m] <= s[i])
}

// The nested quantifier uses i - 1 too, before the enclosing quantifier does, and each binds its own new variable for it
ghost predicate NestedFirst(s: seq<int>) {
  forall i | 0 < i < |s| :: (forall m | 0 <= m < i :: s[m] <= s[i - 1]) || s[i - 1] <= s[i]
}

// The term mentions the nested quantifier's variable, so only the nested quantifier can bind the new variable for it
ghost predicate InnerVariable() {
  forall i :: F(i) <= 0 || (forall j :: P(j) ==> F(i + j) > 0)
}
