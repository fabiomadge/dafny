// RUN: %exits-with 4 %verify --allow-warnings "%s" > "%t"
// RUN: %diff "%s.expect" "%t"

predicate P(x: int) { 0 <= x }

// To break the matching loop of each guard and quantifier, the trigger generator replaces a term with a new variable,
// which its version defines ahead of the conditions under which the term is well-formed

method If() {
  if j :| 0 <= j < 5 && j != 1 && P(j) && P(j + 10 / (j - 1)) {
  }
}

method IfCase(a: array?<int>) {
  if
  case j :| 0 <= j < 5 && a != null && P(j) && P(a.Length - j) =>
  case true =>
}

// A quantifier inside another binder reaches the well-formedness check through a substitution

method InLet() {
  assume {:axiom} var m := 5; forall j | 0 <= j < m && j != 1 && P(j) :: P(j + 10 / (j - 1)) || P(j);
}

method InLambda() {
  var f := (k: int) => forall j | 0 <= j < 5 && j != 1 && P(j) :: P(j + 10 / (j - 1)) || P(j);
}

// The trigger generator splits this quantifier at the conjunction. Given the first part, which holds for every i, the
// second is well-formed, but the quantifier as written is not
method Split(s: seq<int>, t: seq<int>)
  requires |t| == |s|
{
  var f := (k: int) => forall i | 0 <= i < |s| :: s[i] > 0 && 10 / s[(i + 1) % |s|] > t[i]; // error: division by zero
}
