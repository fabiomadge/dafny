// RUN: %testDafnyForEachCompiler --refresh-exit-code=0 "%s"

// To break a matching loop, the trigger generator replaces j - 1 below, and i - 1 in Sorted, with a new bound
// variable, which is enumerated last. The compiler uses the rewritten quantifier in this binding guard and this
// lambda, but not in a bare quantifier.

method Main() {
  // i's bound must not mention the new variable. Declaring j before i makes that bound mention j - 1.
  if j: int, i: int :| 0 <= j < 5 && 0 <= i < (j - 1) * (j - 1) + 1 && i * j == 2 {
    print i, " ", j, "\n";
  }
  // Nor may the nested forall take the new variable from the exists.
  var f := k => exists j: int, i: int | 0 <= j < 5 && 0 <= i < (j - 1) * (j - 1) + 1 &&
    (forall m: int | 0 <= m < i :: m * m < 9) :: i * j == k;
  print f(2), "\n";
}

// The nested forall must not take the new variable from the enclosing one.
ghost predicate Sorted(s: seq<int>) {
  forall i | 0 < i < |s| :: s[i - 1] <= s[i] || (forall m | 0 <= m < i :: s[m] <= s[i])
}
