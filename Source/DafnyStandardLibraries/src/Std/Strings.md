# The `Strings` module

This module provides several common utilities for manipulating strings,
in particular converting values of common types such as `bool`, `nat`, and `int`
to and from their string representations.

Note that since in Dafny `string` is just an alias for `seq<char>`,
many common string operations are available in the
[`Collections.Seqs` module](../Collections.md) instead.
The `Strings` module only provides utilities more specific to sequences of characters.

## Number round trips

`LemmaNatRoundTrip` and `LemmaIntRoundTrip` prove that parsing a formatted number returns it,
including the preconditions of `ToNat` and `ToInt`:

<!-- %check-verify -->
```dafny
module NumberRoundTrips {
  import opened Std.Strings

  lemma Example(n: nat, i: int) {
    LemmaNatRoundTrip(n);
    assert ToNat(OfNat(n)) == n;
    LemmaIntRoundTrip(i);
    assert ToInt(OfInt(i)) == i;
  }
}
```

Every refinement of `ParametricConversion`, such as `HexConversion`, has the same lemmas.
