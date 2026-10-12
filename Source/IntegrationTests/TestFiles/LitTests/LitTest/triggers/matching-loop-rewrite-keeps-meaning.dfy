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

// The range would divide by zero and dereference null where the guards rule that out
method Guards(a: array?<int>) {
  if j :| 0 <= j < 5 && j != 1 && NonNeg(j) && NonNeg(j + 10 / (j - 1)) {
  }
  if j :| 0 <= j < 5 && a != null && NonNeg(j) && NonNeg(a.Length - j) {
  }
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
