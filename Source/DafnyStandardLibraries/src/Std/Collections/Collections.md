# The `Collections` module

This module includes a variety of submodules that define properties of
various collections:

- Set: functions and lemmas expressing properties of Dafny's `set<T>` type, such as  properties of subsets, unions, and intersections, filtering of sets using predicates, mapping sets to other sets using functions

- Iset: function and lemmas to manipulate `iset`s

- Seq: functions and lemmas expressing properties of Dafny's `seq<T>` type,
such as properties of subsequences, filtering of sequences,
finding elements (i.e., index-of, last-index-of),
inserting or removing elements,
reversing, repeating or combining (zipping or flattening) sequences,
sorting, and
conversion to sets.

- Map: functions and lemmas to manipulate `map`s

- Imap: functions and lemmas to manipulate `imap`s

- Array: manipulations of arrays

<!-- TODO
- LittleEndianNat: properties of sequences that represent natural numbers expressed as a given base, with the least significant digit at position 0 of the sequence and each element in the range 0 to the base.
- LittleEndianNatConversions: conversions between two little-endian representations of nats in different bases
-->
