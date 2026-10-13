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

// The trigger of the nested quantifier would not mention a new variable, so the rewrite leaves that quantifier as it is
ghost predicate FirstDescent(a: seq<int>) {
  exists i :: 0 <= i < |a| - 1 && a[i] > a[i + 1] && (forall j {:trigger a[j]} :: 0 <= j < i ==> a[j] <= a[j + 1])
}

// The middle quantifier binds the new variable for x + 1 as well, which the innermost one takes
ghost predicate Deep() {
  forall x :: F(x) <= 0 || (forall y :: P(y) ==> F(x + 1) > 0 || (forall z :: P(z) ==> F(x + 1) > z))
}

// The induction hypothesis loops through n + Half(n), so it gets no triggers, although that term cannot be named
lemma {:induction n} Induction(n: nat)
  requires F(n) <= F(n + Half(n))
  ensures F(n) <= F(n + Half(n))
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

// The nested quantifier binds the new variable for i - 1 as well, which the enclosing quantifier still needs, and in a
// function body, which the verifier substitutes into, the two quantifiers must not bind the same variable.
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
