// RUN: %verify --bprint "%t.bpl" "%s" > "%t"
// RUN: %diff "%s.expect" "%t"
// RUN: %OutputCheck --file-to-check "%t.bpl" "%s"

// The loop through a[i] and a[i + 1] needs a trigger with i + 1, which no trigger may contain, so the verifier binds a
// variable to it, defined by it, and the trigger and the body have the variable where they have i + 1
// CHECK: \(forall i#[0-9]+: int, _t#[0-9]+: int ::
// CHECK-NEXT: \{ read\(\$Heap, a#0, IndexField\(_t#[0-9]+\)\), read\(\$Heap, a#0, IndexField\(i#[0-9]+\)\) \}
// CHECK-NEXT: _t#[0-9]+ == i#[0-9]+ \+ 1
// CHECK: <= \$Unbox\(read\(\$Heap, a#0, IndexField\(_t#[0-9]+\)\)\): int\);
lemma Sorted(a: array<int>, n: int)
  requires forall i :: 0 <= i < a.Length - 1 ==> a[i] <= a[i + 1]
  requires 0 <= n < a.Length - 1
  ensures a[n] <= a[n + 1]
{
}

function F(x: int): int

// So does the existence check of a :|, for the loop through F(x) and F(x + 1)
// CHECK: \(exists \$as#x0#0: int, _t#[0-9]+: int ::
// CHECK-NEXT: \{ _module.__default.F\(_t#[0-9]+\), _module.__default.F\(\$as#x0#0\) \}
// CHECK-NEXT: _t#[0-9]+ == \$as#x0#0 \+ 1
method SuchThat()
  requires F(0) <= F(1)
{
  var x :| F(x) <= F(x + 1);
}

// A named term can have binders, which the verifier compares up to the names of their variables, as each translation
// of a set comprehension names its lambda's variable anew
method Let(k: int)
  requires forall x :: F(x) <= F(x + (var z := k; z))
{
  assert F(3) <= F(3 + (var z := k; z));
}

method SetComprehension(S: set<int>)
  requires forall x :: F(x) <= F(x + |set j | j in S && j > 0|)
{
  assert F(3) <= F(3 + |set j | j in S && j > 0|);
}

// The trigger has the formal k only in the named term, which the translation binds, so the verifier inlines P also
// for an argument that no trigger may contain
ghost predicate P(k: int, n: nat) {
  if n == 0 then forall i :: F(i) <= F(i + k) else P(k, n - 1)
}

method Inlined(c: int)
  requires forall i :: F(i) <= F(i + (c + 1))
{
  assert P(c + 1, 1);
}
