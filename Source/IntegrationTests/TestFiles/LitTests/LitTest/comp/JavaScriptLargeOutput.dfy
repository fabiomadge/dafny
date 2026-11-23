// NONUNIFORM: JavaScript-specific regression test
// RUN: %run --target js "%s" > "%t"
// RUN: %OutputCheck --file-to-check "%t" "%s"
// CHECK: ^x{70000}$

// Must exceed the pipe buffer, 64 KB on Linux and macOS
method Main() {
  print seq(70000, _ => 'x');
}
