// RUN: %dafny /compile:0 "%s" > "%t"
// RUN: %dafny_0 /noVerify /compile:4 /compileTarget:cs "%s" >> "%t"
// RUN: %dafny_0 /noVerify /compile:4 /compileTarget:js "%s" >> "%t"
// RUN: %dafny_0 /noVerify /compile:4 /compileTarget:go "%s" >> "%t"
// RUN: %dafny_0 /noVerify /compile:4 /compileTarget:java "%s" >> "%t"
// RUN: %dafny_0 /noVerify /compile:4 /compileTarget:cpp "%s" >> "%t"
// RUN: %dafny_0 /noVerify /compile:4 /compileTarget:py "%s" >> "%t"
// RUN: %diff "%s.expect" "%t"

method Main() {
  print "XYZ"; // Checks that no extra newline is added to the output
}