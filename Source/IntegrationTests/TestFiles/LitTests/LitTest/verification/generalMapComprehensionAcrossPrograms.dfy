// RUN: %verify "%s" > "%t"
// RUN: %baredafny measure-complexity --mutations 2 --use-basename-for-filename "%s" > "%t.mc"
// RUN: %diff "%s.expect" "%t"

// The map comprehensions with key expressions in A are translated into A's Boogie program and into
// B's, whose verification conditions use C and M's postcondition; measure-complexity translates
// them once per mutation. Their keys have types that the Boogie prelude declares.

module A {
  datatype D = D(x: int)

  const C: map<seq<int>, int> := map i: int | 0 <= i < 3 :: [i] := i

  method M(n: nat) returns (m: map<D, int>)
    ensures m == map i: int | 0 <= i < n :: D(i) := i
  {
    m := map i: int | 0 <= i < n :: D(i) := i;
  }
}

module B {
  import A

  method N() {
    var c := A.C;
    var m := A.M(3);
  }
}
