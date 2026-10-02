// RUN: %testDafnyForEachCompiler "%s"

// A let-such-that expression is compiled into a target-language lambda, which cannot capture
// a variable that is reassigned (Java) or an out-parameter (C#).

method Locals() {
  var x := 1;
  x := 2;
  var y := var z :| z in {x}; z;
  print y, "\n"; // 2
}

method OutParameters() returns (r: int, s: int) {
  r := 5;
  s := var z :| z in {r}; z + 1;
}

method LoopIndex() {
  for i := 0 to 3 {
    print (var z :| z in {i}; z);
  }
  print "\n"; // 012
}

// Tail calls reassign the parameters
function Sum(n: nat, acc: int): int {
  if n == 0 then acc else Sum(n - 1, acc + var z :| z in {n}; z)
}

method Main() {
  Locals();
  var r, s := OutParameters();
  print r, " ", s, "\n"; // 5 6
  LoopIndex();
  print Sum(3, 0), "\n"; // 6
}
