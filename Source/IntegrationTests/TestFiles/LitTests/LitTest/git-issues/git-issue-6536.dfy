// RUN: %verify "%s" > "%t"
// RUN: %diff "%s.expect" "%t"

// The axiom for (o - m) + n applies exactly where o - m is defined, m <= o.Offset.

lemma MinusThenPlus(o: ORDINAL, m: nat, n: nat)
  requires m <= o.Offset && o.Offset + m < n
  ensures (o - (m as ORDINAL)) + (n as ORDINAL) == o + ((n - m) as ORDINAL)
{
}

lemma MinusThenPlusLess(o: ORDINAL, m: nat, n: nat)
  requires n <= m <= o.Offset
  ensures (o - (m as ORDINAL)) + (n as ORDINAL) == o - ((m - n) as ORDINAL)
{
}

lemma Undefined()
  ensures ((0 as ORDINAL) - 1) + 1 == 0 // error (twice): 0 - 1 is undefined, and the postcondition does not follow
{
}
