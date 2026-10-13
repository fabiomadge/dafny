module Library {
  // To break a matching loop, the trigger generator rewrites this quantifier, replacing j - 1 with a new bound variable.
  predicate P(n: int) {
    exists j, i :: 0 <= j < n && 0 <= i < (j - 1) * (j - 1) + 1 && i * j == 2
  }

  function Sq(i: int): int { i * i }

  // The trigger generator splits this quantifier at the conjunction and joins the parts again, with the range in each.
  predicate Small(n: int) {
    forall i :: 0 <= i < n ==> 0 <= Sq(i) && Sq(i) < 100
  }
}
