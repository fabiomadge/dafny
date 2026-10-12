// RUN: %testDafnyForEachCompiler --refresh-exit-code=0 "%s"

// To break a matching loop, the trigger generator rewrites each exists j, i below, replacing j - 1 with a new bound
// variable. The compiler must compile such a quantifier as written, also where it substitutes into it, as in each
// context below.

function h(x: int): int { x + 2 }

datatype D = Make {
  // Tail recursion makes the compiler substitute for this in the lambda.
  function F(n: nat): bool {
    if n == 0 then
      var f := k => exists j, i | 0 <= j < 5 && 0 <= i < (j - 1) * (j - 1) + 1 :: i * j == k;
      f(2)
    else
      F(n - 1)
  }
}

method Main() {
  // Binding guards, one of them around such a quantifier
  if j, i :| 0 <= j < 5 && 0 <= i < (j - 1) * (j - 1) + 1 && i * j == 2 {
    print i, " ", j, "\n";
  }
  if {
    case c :| 0 <= c < 3 && exists j, i | 0 <= j < 5 && 0 <= i < (j - 1) * (j - 1) + 1 :: i * j == h(c) + 3 =>
      print c, "\n";
    case true => print "none\n";
  }
  // A lambda that captures n
  var n := 5;
  var f := k => exists j, i | 0 <= j < n && 0 <= i < (j - 1) * (j - 1) + 1 :: i * j == k;
  // The bounds of x and z
  var x :| x in {if exists j, i | 0 <= j < 5 && 0 <= i < (j - 1) * (j - 1) + 1 :: i * j == 2 then 1 else 0};
  var b := exists z |
    0 <= z < (if exists j, i | 0 <= j < 5 && 0 <= i < (j - 1) * (j - 1) + 1 :: i * j == 2 then 3 else 0) :: h(z) == 4;
  print f(2), " ", f(7), " ", x, " ", b, " ", Make.F(3), "\n";
  // A set and a map comprehension, whose ranges the compiler splits into conjuncts, here of a negation
  var s := set c | 0 <= c < 3 && !(exists j, i | 0 <= j < 5 && 0 <= i < (j - 1) * (j - 1) + 1 :: i * j == h(c) + 3);
  var m := map c |
    0 <= c < 3 && !(exists j, i | 0 <= j < 5 && 0 <= i < (j - 1) * (j - 1) + 1 :: i * j == h(c) + 3) :: 2 * c;
  print s == {0, 2}, " ", m == map[0 := 0, 2 := 4], "\n";
}
