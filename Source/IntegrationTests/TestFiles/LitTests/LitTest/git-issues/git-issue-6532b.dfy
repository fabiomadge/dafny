// RUN: %verify "%s" > "%t"
// RUN: %diff "%s.expect" "%t"

// The right-hand side of a constant field mentions its class's type parameter, and the
// constant is used outside the class

ghost function G<X>(): bool { true }

class C<T> {
  ghost const k: bool := G<T>()
}

method UseK(c: C<int>) {
  ghost var b := c.k;
  assert b;
}
