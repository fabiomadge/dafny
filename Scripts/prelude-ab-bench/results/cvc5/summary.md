26922 queries in 1387 programs (1387 jobs).

| | cvc5 unsat | cvc5 unknown | cvc5 sat | cvc5 at the CPU limit | other |
|---|---:|---:|---:|---:|---:|
| z3 proves | 24392 | 30 | 0 | 293 | 0 |
| z3 does not | 38 | 2073 | 0 | 96 | 0 |

Programs: Z3 proves every query of 917; cvc5 proves every query of 830 of those, and of 9 that Z3 does not.

Programs with at least one query cvc5 does not prove: 548 of 1387 (on unpatched master, Dafny's verification of each of these ends at the first such VC, in Boogie's model parser).

| cvc5 CPU time / Z3's, on queries both prove | queries | programs | per program [95%] | geomean over queries | total |
|---|---:|---:|---|---|---|
| all | 24392 | 1245 | 1.62x [1.58, 1.66] | 2.14x | 5.09x |
| Z3 takes at least 1 s | 92 | 26 | 1.61x [0.82, 3.07] | 2.02x | 2.26x |
| cvc5 takes at least 1 s | 1152 | 213 | 26.51x [23.13, 30.53] | 19.46x | 10.46x |
| both take at least 1 s | 84 | 22 | 3.12x [2.04, 4.85] | 2.56x | 2.35x |

z3: CPU per query, 5th percentile 0.041 s (about the fixed cost of a process and the prelude), median 0.054 s

cvc5: CPU per query, 5th percentile 0.051 s (about the fixed cost of a process and the prelude), median 0.094 s

| of the queries Z3 proves, proved within | Z3 | cvc5 |
|---|---:|---:|
| 0.1 CPU s | 84.8% | 50.5% |
| 1 CPU s | 99.4% | 94.0% |
| 10 CPU s | 99.9% | 97.8% |
| 60 CPU s | 100.0% | 98.7% |

Jobs whose queries use Z3's `bv2int` (a cvc5 parse error on unpatched master): 40 (260 queries).
Jobs run with `-proverOpt:BATCH_MODE=true` (every VC inconclusive under cvc5): 0.
