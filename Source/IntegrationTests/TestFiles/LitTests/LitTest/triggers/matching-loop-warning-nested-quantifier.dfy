// RUN: %verify --allow-warnings "%s" > "%t"
// RUN: %diff "%s.expect" "%t"

// The warning about a matching loop through a term with the variable of a nested quantifier says how to break the loop

predicate P(j: int)
function F(x: int): int

// The advice keeps the nested quantifier's range and names a variable that the quantifier does not use
lemma Taken(n: int, t: int)
  requires forall i :: F(i) <= t || (forall j | 0 <= j < 10 :: P(j) ==> F(i + j) > 1)
  requires F(n) > t && P(1)
  ensures F(n + 1) > 1
{
}

// Following it breaks the loop
lemma TakenFixed(n: int, t: int)
  requires forall i :: F(i) <= t || (forall j, t1 | 0 <= j < 10 && t1 == i + j :: P(j) ==> F(t1) > 1)
  requires F(n) > t && P(1)
  ensures F(n + 1) > 1
{
}
