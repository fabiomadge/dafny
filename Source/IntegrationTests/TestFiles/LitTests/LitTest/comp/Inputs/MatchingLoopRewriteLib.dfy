module Library {
  // To break a matching loop, the trigger generator rewrites this quantifier, replacing j - 1 with a new bound variable.
  predicate P(n: int) {
    exists j, i :: 0 <= j < n && 0 <= i < (j - 1) * (j - 1) + 1 && i * j == 2
  }
}
