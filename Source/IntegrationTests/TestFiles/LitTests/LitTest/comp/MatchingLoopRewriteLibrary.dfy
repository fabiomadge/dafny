// RUN: %dafny /compileTarget:cs /useRuntimeLib /out:%S/Output/MatchingLoopRewriteLib.dll %S/Inputs/MatchingLoopRewriteLib.dfy > "%t"
// RUN: %dafny /compile:3 "%s" %binaryDir/DafnyRuntime.dll %S/Output/MatchingLoopRewriteLib.dll >> "%t"
// RUN: %diff "%s.expect" "%t"

// The library's assembly embeds the library's Dafny source, which Dafny parses again here.

module Client {
  import Library

  method Main() {
    print Library.P(2), " ", Library.P(3), " ", Library.Small(10), " ", Library.Small(11), "\n";
  }
}
