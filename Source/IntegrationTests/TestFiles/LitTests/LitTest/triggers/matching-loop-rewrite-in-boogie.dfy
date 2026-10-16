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
