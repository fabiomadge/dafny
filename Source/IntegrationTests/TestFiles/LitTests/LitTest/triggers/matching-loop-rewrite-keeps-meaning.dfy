// RUN: %exits-with 4 %verify --allow-warnings --rprint "%t.rprint.dfy" "%s" > "%t"
// RUN: %diff "%s.expect" "%t"
// RUN: %OutputCheck --file-to-check "%t.rprint.dfy" "%s"

// To break a matching loop, the trigger generator replaces each occurrence of a term with a variable of a new
// quantifier around the formula that uses it, which defines the variable by that occurrence. Each assertion below would
// follow if a definition were outside the occurrence's guards or in another state, or took another occurrence's value,
// or a let's right-hand side moved into another state, and all assumptions are satisfiable.

class C { var f: int }
newtype Byte = x | 0 <= x < 256
function F(x: int): int
function F2(x: int, y: int): int
function G(x: Byte): int
function G8(x: bv8): bv8
function K(x: int): int
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
// CHECK: NonNeg\(i\) ==> forall _t#0: int \{:trigger F\(_t#0\)\} \| _t#0 == i \+ Half\(i\) :: F\(i\) <= F\(_t#0\)
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

// A new quantifier is a forall where the formula around it is positive in a forall or negative in an exists, and an
// exists otherwise, so that it is universal wherever the rewritten quantifier is. An if whose test has the term is one
// formula.
// CHECK: \(exists _t#0: int \{:trigger F\(_t#0\)\} \| _t#0 == i \+ c\.f :: F\(i\) <= F\(_t#0\)\) ==> Q\(i\)
// CHECK: \| exists _t#0: int \{:trigger F\(_t#0\)\} \| _t#0 == i \+ c\.f :: F\(i\) <= F\(_t#0\) :: Q\(i\)
// CHECK: j == 2 && exists _t#0: int \{:trigger F\(_t#0\)\} \| _t#0 == i \+ c\.f :: F\(i\) <= F\(_t#0\) :: F2\(i, j\) == 0
// CHECK: !\(exists _t#0: int \{:trigger F\(_t#0\)\} \| _t#0 == i \+ c\.f :: F\(i\) > F\(_t#0\)\) \|\| Q\(i\)
// CHECK: \(exists _t#0: int \{:trigger F\(_t#0\)\} \| _t#0 == i \+ c\.f :: F\(i\) > F\(_t#0\)\) && Q\(i\)
// CHECK: \| exists _t#0: int \{:trigger F\(_t#0\)\} \| _t#0 == i \+ c\.f :: F\(i\) > F\(_t#0\) :: Q\(i\)
// CHECK: forall _t#0: int \{:trigger F\(_t#0\)\} \| _t#0 == i \+ c\.f :: if F\(i\) <= F\(_t#0\) then Q\(i\) else true
lemma Polarity(c: C)
  requires forall i :: F(i) <= F(i + c.f) ==> Q(i)
  requires forall i | F(i) <= F(i + c.f) :: Q(i)
  requires forall i :: forall j {:trigger F2(i, j)} | j == 2 && F(i) <= F(i + c.f) :: F2(i, j) == 0
  requires forall i :: !(F(i) > F(i + c.f)) || Q(i)
  requires exists i :: F(i) > F(i + c.f) && Q(i)
  requires exists i | F(i) > F(i + c.f) :: Q(i)
  requires forall i :: if F(i) <= F(i + c.f) then Q(i) else true
{
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

// i + 1 means the same everywhere, so a formula that evaluates it only sometimes may define its variable, and the
// quantifier gets a trigger that matches F(n + 1)
lemma IfBranch(c: bool, n: int)
  requires c
  requires forall i :: F(i) <= (if c then F(i + 1) else K(i))
  ensures F(n) <= F(n + 1)
{
}

// But a call's CanCall assumption would lose the guard
method CallInBranch() {
  assume {:axiom} F(0) == 0 && F(-1) == 0;
  assume {:axiom} forall i :: F(i) <= (if NonNeg(i) then F(i + Half(i)) else F(i));
  assert false;
}

// And b + 1 has a type that constrains its variable, which would have no value for b == 255
method TypeInBranch() {
  assume {:axiom} G(255) == 1;
  assume {:axiom} forall b: Byte {:trigger G(b)} :: b < 255 ==> G(b) <= G(b + 1);
  assert forall b: Byte :: G(b) <= (if b < 255 then G(b + 1) else 0);
}

trait Animal {}
class Cat extends Animal {}
class Dog extends Animal {}

// The term equality takes o is Cat for o is Dog, so the two occurrences in one formula would share one value
method TypeTests(o: Animal)
  requires o is Cat
{
  assume {:axiom} F(0) == 1 && F(1) == 2 && Q(0);
  assume {:axiom} forall i :: Q(i) ==> F(i) <= F(i + (if o is Cat then 1 else 0)) - F(i + (if o is Dog then 1 else 0));
  assert false;
}

// The loop runs through F2(i + 1, s[j + 1]), whose argument s[j + 1] kills triggers too, so the new variable would get
// no trigger, and the rewrite names nothing
// CHECK-NOT: F2\(_t#0, s\[j \+ 1\]\)
lemma SplitParts(s: seq<int>)
  requires forall i, j :: 0 <= j < |s| - 1 ==> F2(i, j) <= F2(i + 1, s[j + 1]) && F2(i, j) <= F2(i + 2, s[j + 1])
{
}

// Nor in this induction hypothesis, which so keeps its trigger
// CHECK: \{:_inductionTrigger F2\(i, j\)\}\*/ /\*\{:_induction i, j\}\*/ SplitPartsInduction
lemma {:induction i, j} SplitPartsInduction(i: nat, j: nat, s: seq<int>)
  requires j < |s| - 1 && F2(i, j) <= F2(i + 1, s[j + 1])
  ensures F2(i, j) <= F2(i + 1, s[j + 1])
{
}

// The nested quantifier, which has a trigger of its own, uses i + 1 too
ghost predicate FirstDescent(a: seq<int>) {
  exists i :: 0 <= i < |a| - 1 && a[i] > a[i + 1] && (forall j {:trigger a[j]} :: 0 <= j < i ==> a[j] <= a[i + 1])
}

// The middle and the innermost quantifier both use x + 1
ghost predicate Deep() {
  forall x :: F(x) <= 0 || (forall y :: P(y) ==> F(x + 1) > 0 || (forall z :: P(z) ==> F(x + 1) > z))
}

// The induction hypothesis loops through n + Half(n), so it gets no triggers
lemma {:induction n} Induction(n: nat)
  requires F(n) <= F(n + Half(n))
  ensures F(n) <= F(n + Half(n))
{
}

// The term occurs only in the nested quantifier
ghost function NestedOnly(k: int): bool {
  forall i :: F(i) <= k || (forall j :: P(j) ==> F(i + 1) > j)
}

lemma UseNestedOnly()
  requires NestedOnly(0)
  ensures NestedOnly(0)
{
}

// The nested quantifier does not use i - 1, so it keeps the trigger that the trigger generator selects for it
// CHECK: forall m: int \{:trigger s\[m\]\}
ghost predicate Sorted(s: seq<int>) {
  forall i | 0 < i < |s| :: s[i - 1] <= s[i] || (forall m | 0 <= m < i :: s[m] <= s[i])
}

// The nested quantifier uses i - 1 too, before the enclosing quantifier does
ghost predicate NestedFirst(s: seq<int>) {
  forall i | 0 < i < |s| :: (forall m | 0 <= m < i :: s[m] <= s[i - 1]) || s[i - 1] <= s[i]
}

// The term mentions the nested quantifier's variable
ghost predicate InnerVariable() {
  forall i :: F(i) <= 0 || (forall j :: P(j) ==> F(i + j) > 0)
}

// The term mentions the variable of a nested quantifier with a trigger of its own
method InnerBinder() {
  assume {:axiom} P(0) && P(1);
  assume {:axiom} exists i :: forall j {:trigger P(j)} :: P(j) ==> F(i) <= F(i + j);
  assert false;
}

ghost predicate R(j: int)
ghost predicate P2(i: int, j: int)
function Pow(n: nat): nat { if n == 0 then 1 else 2 * Pow(n - 1) }

// The nested quantifier's trigger has j + 1 too
ghost predicate H() {
  forall j :: R(j) ==> forall i {:trigger P2(i, j + 1)} :: P2(i, j + 1) ==> R(j + 1)
}

lemma UseH()
  requires H() && R(5)
  ensures forall i :: P2(i, 6) ==> R(6)
{
}

// The induction hypothesis has the postcondition's quantifier, with the trigger that the trigger generator selected
lemma Exponent(n: nat)
  ensures forall k :: P(k) ==> Pow(n) <= Pow(n + 1)
{
}

// The rewrite looks through the let, as the trigger generator does
// CHECK: forall _t#0: int \{:trigger s\[_t#0\]\} \| _t#0 == i \+ 1 ::
// CHECK-NEXT: s\[i\] <= s\[_t#0\]
ghost predicate ThroughLet(s: seq<int>) {
  forall i | 0 <= i < |s| - 1 :: var j := i + 1; s[i] <= s[j]
}

// But not if the right-hand side may mean something else where the variable occurs, as c.f inside the old
method LetInOld(c: C)
  requires c.f == 0
  modifies c
{
  c.f := 1;
  assume {:axiom} F(0) == 8 && F(1) == 7;
  assume {:axiom} forall i :: var x := c.f; F(i) <= F(i + 1) || old(c.f != x);
  assert false;
}

datatype Instr = Branch(m: nat)

// The match binds n, which pc + n mentions, so the rewrite names nothing
predicate WellTyped(ii: seq<Instr>, typing: seq<nat>)
  requires forall pc :: 0 <= pc < |ii| ==> match ii[pc] case Branch(n) => pc + n < |typing|
{
  forall pc :: 0 <= pc < |ii| ==> match ii[pc] case Branch(n) => typing[pc + n] == typing[pc]
}

// Nor if only the trigger term F2(i + 1, k) mentions one
lemma MatchArg(d: Option<int>)
  requires forall i, j :: F2(i, j) <= (match d case Some(k) => F2(i + 1, k) case None => 0)
{
}
