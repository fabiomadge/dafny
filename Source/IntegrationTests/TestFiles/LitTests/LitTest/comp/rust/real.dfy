// NONUNIFORM: Rust-specific tests
// RUN: %baredafny run --target=rs --enforce-determinism "%s" > "%t"
// RUN: %diff "%s.expect" "%t"

newtype I8 = x: int | -128 <= x < 128
newtype {:rust_erased false} WrappedI8 = x: int | -128 <= x < 128

method Main() {
  var a: real := 0.25;
  var b: real := -0.5;
  print a + b, " ", a - b, " ", a * b, " ", a / b, "\n";
  print a < b, " ", a == 1.0 / 4.0, " ", |{0.5, 1.0 / 2.0}|, "\n";
  print 0.2, " ", 1.0 / 40.0, " ", 3.5, " ", 1.0 / 3.0, "\n";
  var i: int := 7;
  var i8: I8 := -3;
  // Conversions are exercised with owned operands (assignments) and borrowed ones (print statements)
  var r: real := i as real;
  var n: int := (r * 2.0) as int;
  var f: int := (r / 2.0).Floor;
  var w: WrappedI8 := (b * 10.0) as WrappedI8;
  print r, " ", n, " ", f, " ", (-r / 2.0).Floor, " ", i8 as real, " ", w, "\n";
}
