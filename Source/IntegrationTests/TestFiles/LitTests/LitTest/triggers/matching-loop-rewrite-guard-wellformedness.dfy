// RUN: %verify --allow-warnings "%s" > "%t"
// RUN: %diff "%s.expect" "%t"

// To break the matching loop of each guard, the trigger generator replaces a term with a new variable, which its
// version of the guard defines ahead of the conditions under which the term is well-formed

predicate P(x: int) { 0 <= x }

method If() {
  if j :| 0 <= j < 5 && j != 1 && P(j) && P(j + 10 / (j - 1)) {
  }
}

method IfCase(a: array?<int>) {
  if
  case j :| 0 <= j < 5 && a != null && P(j) && P(a.Length - j) =>
  case true =>
}
