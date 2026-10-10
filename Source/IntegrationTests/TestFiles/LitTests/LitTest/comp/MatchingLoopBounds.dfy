// RUN: %testDafnyForEachCompiler --refresh-exit-code=0 "%s"

// To break a matching loop, the trigger generator replaces j - 1 with a new bound variable, which is enumerated last,
// so i's bound must not mention it. Declaring j before i makes that bound mention j - 1. The compiler uses the
// rewritten quantifier in this binding guard and this lambda, but not in a bare quantifier.

method Main() {
  if j: int, i: int :| 0 <= j < 5 && 0 <= i < (j - 1) * (j - 1) + 1 && i * j == 2 {
    print i, " ", j, "\n";
  }
  var f := k => exists j: int, i: int | 0 <= j < 5 && 0 <= i < (j - 1) * (j - 1) + 1 :: i * j == k;
  print f(2), "\n";
}
