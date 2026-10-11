// RUN: %testDafnyForEachCompiler --refresh-exit-code=0 "%s"

method Main() {
  var a := new real[1];  // C# stores this default as 0/0
  var zeros := {0.0, a[0]};
  print "zeros: ", |zeros|, "\n";

  var halves := {0.5, 1.0 / 2.0};
  print "halves: ", |halves|, "\n";
}
