// RUN: %testDafnyForEachCompiler --refresh-exit-code=0 "%s"

// To break a matching loop, the trigger generator replaces j - 1 and i - 1 below with a new bound variable. The
// compiler uses the rewritten quantifier in this binding guard and these lambdas, but not in a bare quantifier.

method Main() {
  // i's bound must not mention the new variable, which is enumerated last. Declaring j before i makes that bound
  // mention j - 1.
  if j: int, i: int :| 0 <= j < 5 && 0 <= i < (j - 1) * (j - 1) + 1 && i * j == 2 {
    print i, " ", j, "\n";
  }
  var f := k => exists j: int, i: int | 0 <= j < 5 && 0 <= i < (j - 1) * (j - 1) + 1 :: i * j == k;
  // m's bound mentions the let variable n, which the rewrite renames, so the bounds still need substituting into.
  var s := [1, 2, 0, 3];
  var g := (d: int) => forall i | 0 < i < |s| ::
    (var n := i; exists m | 0 <= m < n :: s[m] == d + 1) || s[i - 1] <= s[i] + d;
  print f(2), " ", g(-1), " ", g(0), "\n";
}

// The nested forall takes the new variable from the outer one, which substituting into the bounds binds again.
lemma Sorted(s: seq<int>)
  requires |s| == 3 && s[0] <= s[1] <= s[2]
{
  assert forall i, k | 0 < i < |s| && 0 <= k <= i - 1 :: s[i - 1] <= s[i] ==> (forall m | 0 <= m < k :: s[m] <= s[k]);
}
