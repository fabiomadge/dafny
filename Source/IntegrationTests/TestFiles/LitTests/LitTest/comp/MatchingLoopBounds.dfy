// RUN: %testDafnyForEachCompiler --refresh-exit-code=0 "%s"

// To break a matching loop, the trigger generator replaces j - 1 with a new bound variable in both quantifiers. The
// compiled code uses the rewritten quantifier in a binding guard and in this lambda, though not in a bare quantifier.
// Declaring j before i keeps j - 1 in i's bound.

method Main() {
  if j: int, i: int :| 0 <= j < 5 && 0 <= i < (j - 1) * (j - 1) + 1 && i * j == 2 {
    print i, " ", j, "\n";
  }
  var f := k => exists j: int, i: int | 0 <= j < 5 && 0 <= i < (j - 1) * (j - 1) + 1 :: i * j == k;
  print f(2), "\n";
}
