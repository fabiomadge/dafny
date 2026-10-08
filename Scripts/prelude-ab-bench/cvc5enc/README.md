# cvc5 encoding tools

`cvc5proxy.py` stands in for cvc5 under Dafny (`--solver-path cvc5proxy.py --solver-option SOLVER=cvc5`; set `CVC5`
to the solver binary) and rewrites the SMT queries on their way with `hybrid.py`:

- `HYBRID_MODE=eager HYBRID_SCOPE=all`: Dafny's arithmetic synonyms (`INTERNAL_add_boogie` and the rest, recognized by
  their definition axioms) stay in every term and trigger, and every Boolean atom that contains one gets the
  synonyms' definitions (`INTERNAL_add_boogie(a, b) == a + b`) attached in its own scope: `(and P D)` where it is
  asserted or in mixed polarity, `(=> D P)` where it is refuted. `HYBRID_SCOPE=vc` does this in the VCs only.
- without `eager`: the synonyms are also replaced by their operators inside the atoms, the triggers kept.

Both are sound: every attached definition follows from the definition axioms, which stay in the query. `qtag.py`
holds the S-expression reader and printer (and names quantifiers for instantiation profiles), `syndef2.py` the
pattern that recognizes a synonym's definition axiom. See `../results/cvc5/README.md` for what the encodings do.
