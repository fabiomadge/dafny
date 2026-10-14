// RUN: %exits-with 4 %verify --allow-warnings --rprint "%t.rprint.dfy" "%s" > "%t"
// RUN: %diff "%s.expect" "%t"
// RUN: %OutputCheck --file-to-check "%t.rprint.dfy" "%s"

// To break a matching loop, the trigger generator replaces a term with a new variable, which it defines next to each
// formula that uses the term. Each assertion below would follow if a definition were outside the term's guards, in
// another state, or of the wrong polarity, or if two terms that mean different things shared a variable, and all
// assumptions are satisfiable.

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
ghost predicate Q(j: int)

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

// A definition outside the guard would assume that Half's precondition holds for every i
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

// In an antecedent, a definition is a conjunct
method Antecedent(c: C) {
  assume {:axiom} c.f == 1 && F(0) == 1 && F(1) == 0 && F(5) == 3;
  assume {:axiom} forall i :: F(i) <= F(i + c.f) ==> Q(i);
  assert Q(0);
}

// So is it in a forall's range
method Range(c: C) {
  assume {:axiom} c.f == 1 && F(0) == 1 && F(1) == 0 && F(5) == 3;
  assume {:axiom} forall i | F(i) <= F(i + c.f) :: Q(i);
  assert Q(0);
}

// And in a forall's range that is nested in a quantifier being rewritten
method NestedRange(c: C) {
  assume {:axiom} c.f == 1 && F(0) == 1 && F(1) == 0 && F(5) == 3;
  assume {:axiom} forall i :: forall j {:trigger F2(i, j)} | j == 2 && F(i) <= F(i + c.f) :: F2(i, j) == 0;
  assume {:axiom} F2(0, 2) == 1;
  assert false;
}

// A negation flips the polarity
method Negation(c: C) {
  assume {:axiom} c.f == 1 && F(0) == 0 && F(1) == 1 && F(5) == 2 && !Q(0);
  assume {:axiom} forall i :: !(F(i) > F(i + c.f)) || Q(i);
  assert false;
}

// In an exists, a definition is a conjunct
method Exists(c: C) {
  assume {:axiom} c.f == 1 && F(0) == 1 && F(1) == 1 && F(7) == 0 && Q(0);
  assert exists i :: F(i) > F(i + c.f) && Q(i);
}

// And in an exists's range
method ExistsRange(c: C) {
  assume {:axiom} c.f == 1 && F(0) == 1 && F(1) == 1 && F(7) == 0 && Q(0);
  assert exists i | F(i) > F(i + c.f) :: Q(i);
}

// An if whose test has the term is one formula, whose definition covers the test
method IfTest(c: C) {
  assume {:axiom} c.f == 1 && F(0) == 1 && F(1) == 0 && F(5) == 3;
  assume {:axiom} forall i :: if F(i) <= F(i + c.f) then Q(i) else true;
  assert Q(0);
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

  // So may a term with constants and destructors
  lemma Constants(w: Window, o: Strided?)
    requires forall i :: o != null ==> F(i) <= F(i + Step + k + h + w.offset + o.h)
  {
  }
}

datatype Option<T> = None | Some(value: T)
datatype Px = Px(x: int)
datatype Qy = Qy(y: int)
datatype D = A | B

// A definition outside the guard would make the CanCall assumptions of p.value.x and q.value.y say that None.value is
// both a Px and a Qy, once F(0) instantiates the quantifier
lemma NestedDestructors(p: Option<Px>, q: Option<Qy>)
  requires p == None && q == None
  requires forall i :: p.Some? && q.Some? ==> F(i) <= F(i + p.value.x + q.value.y)
{
  var _ := F(0);
  assert false;
}

// A formula that the connectives end at evaluates its own operands of &&, ||, ==>, if and match only sometimes, so the
// rewrite names nothing there
lemma InFormula(p: Option<Px>, q: Option<Qy>, d: D)
  requires p == None && q == None && d == B
  requires forall i :: (p.Some? && q.Some? && F(i) <= F(i + p.value.x + q.value.y)) <==> P(i)
  requires forall i :: (!(p.Some? && q.Some?) || F(i) <= F(i + p.value.x + q.value.y)) <==> Q(i)
  requires forall i :: (p.Some? && q.Some? ==> F(i) <= F(i + p.value.x + q.value.y)) <==> R(i)
  requires forall i :: F(i) <= (if p.Some? && q.Some? then F(i + p.value.x + q.value.y) else 0) + F(i)
  requires forall i {:split false} :: (p.Some? && q.Some? ==> F(i) <= F(i + p.value.x + q.value.y)) &&
                                      F(i) <= (match d case A => F(i + p.value.x + q.value.y) case B => 0) + F(i)
{
  var _ := F(0);
  assert false;
}

class Generic<T> {
  static const N: int
}
twostate function TwoState(c: C): int reads c { old(c.f) }
function Gen<T>(x: int): int

// The term equality ignores the labels of old, so a universal goal with the two terms in a disjunction would hold for
// each value of a variable that they shared
method OldLabels(c: C)
  modifies c
{
  c.f := 1;
  label A:
  c.f := 0;
  label B:
  assume {:axiom} F(0) == 1 && F(1) == 0;
  assert forall i :: F(i) <= F(i + old@A(c.f)) || F(i + old@B(c.f)) == 7;
}

// It ignores the label of a two-state function's call too
method TwoStateLabels(c: C)
  modifies c
{
  c.f := 1;
  label A:
  c.f := 0;
  label B:
  assume {:axiom} F(0) == 1 && F(1) == 0;
  assert forall i :: F(i) <= F(i + TwoState@A(c)) || F(i + TwoState@B(c)) == 7;
}

// It may not tell Generic<int>.N from Generic<nat>.N
method StaticOfGeneric() {
  assume {:axiom} Generic<int>.N == 1 && Generic<nat>.N == 0 && F(0) == 1 && F(1) == 0;
  assert forall i :: F(i) <= F(i + Generic<int>.N) || F(i + Generic<nat>.N) == 7;
}

// And it ignores a call's type arguments, so an exists with the two terms in a conjunction would need one value for both
method TypeArguments() {
  assume {:axiom} forall k {:trigger Gen<nat>(k)} :: Gen<nat>(k) != Gen<int>(k);
  assume {:axiom} Gen<nat>(0) == 1 && Gen<int>(0) == 0 && F(0) == 7 && F(1) == 0;
  assume {:axiom} exists i :: F(i) > F(i + Gen<nat>(i)) && F(i + Gen<int>(i)) == 7;
  assert false;
}

// Each part of the split quantifier binds its own new variable, and neither part gets a trigger
lemma SplitParts(s: seq<int>)
  requires forall i, j :: 0 <= j < |s| - 1 ==> F2(i, j) <= F2(i + 1, s[j + 1]) && F2(i, j) <= F2(i + 2, s[j + 1])
{
}

// Naming only i + 1 would leave no trigger, so the rewrite names neither term
lemma PartialNaming()
  requires forall i, j :: F2(i, j) <= F2(i + 1, j + Gen<nat>(j))
  ensures F2(0, 0) <= F2(1, Gen<nat>(0))
{
}

// The nested quantifier uses i + 1 too, but its own trigger would not mention a new variable that it bound, so it
// refers to the enclosing quantifier's
ghost predicate FirstDescent(a: seq<int>) {
  exists i :: 0 <= i < |a| - 1 && a[i] > a[i + 1] && (forall j {:trigger a[j]} :: 0 <= j < i ==> a[j] <= a[i + 1])
}

// The middle and the innermost quantifier both use x + 1, and each binds its own new variable for it
ghost predicate Deep() {
  forall x :: F(x) <= 0 || (forall y :: P(y) ==> F(x + 1) > 0 || (forall z :: P(z) ==> F(x + 1) > z))
}

// The induction hypothesis loops through n + Half(n), so it gets no triggers
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
// body, which the verifier substitutes into, the two quantifiers must not bind the same variable. The nested quantifier
// keeps the trigger that the trigger generator selects for it.
// CHECK: forall m: int \{:trigger s\[m\]\}
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

// The nested quantifier has a trigger of its own, so the enclosing quantifier would bind the new variable, and a
// definition in the nested quantifier would give each j its own value of it
method InnerBinder() {
  assume {:axiom} P(0) && P(1);
  assume {:axiom} exists i :: forall j {:trigger P(j)} :: P(j) ==> F(i) <= F(i + j);
  assert false;
}

ghost predicate R(j: int)
ghost predicate P2(i: int, j: int)
function Pow(n: nat): nat { if n == 0 then 1 else 2 * Pow(n - 1) }

// The nested quantifier's trigger gets the enclosing quantifier's new variable for j + 1 too, which breaks the loop of
// R(j) and R(j + 1)
ghost predicate H() {
  forall j :: R(j) ==> forall i {:trigger P2(i, j + 1)} :: P2(i, j + 1) ==> R(j + 1)
}

lemma UseH()
  requires H() && R(5)
  ensures forall i :: P2(i, 6) ==> R(6)
{
}

// The nested quantifier mentions the let's variable, which the rewritten quantifier renames
ghost predicate LetAround() {
  forall i :: (var v :| v == i; exists w {:trigger P2(w, v)} :: P2(w, v)) || F(i) <= F(i + 1)
}

// The induction hypothesis has the postcondition's quantifier, with the trigger that the trigger generator selected
lemma Exponent(n: nat)
  ensures forall k :: P(k) ==> Pow(n) <= Pow(n + 1)
{
}

// The trigger generator sees Pow(n + 1) through the let, but the induction hypothesis has no n + 1 to replace, so the
// rewrite leaves it as it is
lemma ThroughLet(n: nat)
  ensures forall k :: P(k) ==> Pow(n) <= (var m := n; Pow(m + 1))
{
}

datatype Instr = Branch(m: nat)

// The match binds n, which pc + n mentions, so the rewrite names nothing
predicate WellTyped(ii: seq<Instr>, typing: seq<nat>)
  requires forall pc :: 0 <= pc < |ii| ==> match ii[pc] case Branch(n) => pc + n < |typing|
{
  forall pc :: 0 <= pc < |ii| ==> match ii[pc] case Branch(n) => typing[pc + n] == typing[pc]
}
