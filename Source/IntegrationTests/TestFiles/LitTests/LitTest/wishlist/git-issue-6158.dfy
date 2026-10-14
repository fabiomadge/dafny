// RUN: %exits-with 4 %verify "%s" > "%t"
// RUN: %diff "%s.expect" "%t"

// The following program showed an unsoundness in the Dafny 4.10 / Boogie / Z3 4.12.1 tool stack: to
// break a matching loop, Dafny replaced j + lsb(j) with a variable whose range assumed that lsb's
// precondition holds for every j. Dafny defines that variable next to j + lsb(j), so the program fails to verify.

function lsb(i: nat): nat
  requires i > 0
  ensures 0 < lsb(i) <= i
{
  if i % 2 == 1 then 1 else 2 * lsb(i / 2)
}

opaque ghost function sum(s: seq<int>): int
{
  if |s| == 0 then 0 else s[0] + sum(s[1..])
}

method MMM(A': seq<int>)
  ensures false // easily provable from the "for" loop and its "i > 0 ==> false" invariant
{
  var A: seq<int> := A';
  var N: nat := |A|;
  var F: array<int>;

  F := new int[|A| + 1](i => if 0 < i <= |A| then A[i - 1] else 0);

  for i := 1 to F.Length
    invariant forall j :: i < j <= N && j - lsb(j) / 2 >= i ==> F[j] == A[j - 1]
    // The following invariant should not be provable if "sum" is opaque, but it should be
    // provable if `opaque` is removed or "sum" is revealed.
    invariant forall j :: 0 < j <= i <= N ==> lsb(j) > 0 && F[j] == sum(A[j - lsb(j)..j])
    invariant forall j :: 0 < j < i && i <= j + lsb(j) <= N ==>
      lsb(j) <= lsb(j + lsb(j)) &&
      F[j + lsb(j)] == A[j + lsb(j) - 1] + sum(A[j + lsb(j) - lsb(j + lsb(j))..j])
    // The following invariant should not be provable, since i is known to satisfy 1 <= i <= F.Length.
    invariant i > 0 ==> false
  {
    var j := lsb(i);
  }
}
