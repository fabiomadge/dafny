// RUN: %testDafnyForEachCompiler "%s"

// A loop guard that contains a let or match expression, at any depth, must read the current
// values of variables on every iteration.

datatype Box = Box(v: int)

method LetInGuard() {
  var n := 3;
  var k := 0;
  while 0 <= k && (var e := n; k < e)
    decreases n - k
  {
    print k, " ";
    k := k + 1;
    if k > 5 { print "BUG "; break; }
  }
  print "| let\n";
}

method MatchInGuard() {
  var b := Box(3);
  var k := 0;
  while (match b case Box(e) => k < e)
    decreases 3 - k
  {
    print k, " ";
    k := k + 1;
    if k > 5 { print "BUG "; break; }
  }
  print "| match\n";
}

method LetInCaseGuard() {
  var n := 3;
  var k := 0;
  while
    decreases n - k
  {
    case (var e := n; k < e) =>
      print k, " ";
      k := k + 1;
      if k > 5 { print "BUG "; break; }
  }
  print "| while-case\n";
}

method LabeledContinue() {
  var n := 3;
  var i := 0;
  label outer: while (var e := n; i < e)
    decreases n - i
  {
    i := i + 1;
    if i > 5 { print "BUG "; break; }
    var j := 0;
    while j < 3
      decreases 3 - j
    {
      j := j + 1;
      if j == 2 { continue outer; }
    }
    print "unreachable ";
  }
  print i, " | labeled continue\n";
}

method Main() {
  LetInGuard();
  MatchInGuard();
  LetInCaseGuard();
  LabeledContinue();
}
