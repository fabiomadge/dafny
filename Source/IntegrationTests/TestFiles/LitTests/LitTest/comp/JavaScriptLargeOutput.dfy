// NONUNIFORM: JavaScript-specific regression test
// RUN: %run --target js "%s" > "%t"
// RUN: %OutputCheck --file-to-check "%t" "%s"
// CHECK: 1999 0123456789012345678901234567890123456789

// Prints about 90 KB, more than a pipe's buffer holds
method Main() {
  for i := 0 to 2000 {
    print i, " 0123456789012345678901234567890123456789\n";
  }
}
