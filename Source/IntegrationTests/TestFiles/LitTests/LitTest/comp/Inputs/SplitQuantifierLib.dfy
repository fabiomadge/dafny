module Library {
  function Sq(i: int): int { i * i }

  // The trigger generator splits this quantifier at the conjunction and joins the parts again, each with the range
  predicate Small(n: int) {
    forall i :: 0 <= i < n ==> 0 <= Sq(i) && Sq(i) < 100
  }
}
