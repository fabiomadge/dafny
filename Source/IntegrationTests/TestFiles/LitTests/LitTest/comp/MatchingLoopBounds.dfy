// RUN: %testDafnyForEachCompiler --refresh-exit-code=0 "%s"

// To break a matching loop, the trigger generator replaces j - 1 with a new bound variable, which comes last, so the
// bounds of the other variables must not mention it.

method Main() {
  if j: int, i: int :| 0 <= j < 5 && 0 <= i < (j - 1) * (j - 1) + 1 && i * j == 2 {
    print i, " ", j, "\n";
  }
  var s := set x: int {:nowarn} | 0 <= x < 2 && (exists j: int, i: int | 0 <= j < 5 && 0 <= i < (j - 1) * (j - 1) + 1 :: i * j == 2);
  print |s|, "\n";
}
