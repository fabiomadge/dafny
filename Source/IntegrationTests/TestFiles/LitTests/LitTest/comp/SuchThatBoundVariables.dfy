// RUN: %testDafnyForEachCompiler "%s"

// A such-that search assigns its bound variables more than once, and a Java lambda cannot capture a
// variable that is reassigned. The let expressions, match expressions, and datatype updates below are
// compiled into Java lambdas.

datatype Option<T> = None | Some(value: T)
datatype P = P(a: int, b: int)

method LetSuchThat(s: set<int>)
  requires s == {5}
{
  var a := var z :| z in s; (var w := 1; w + z);
  var b := var z :| z in s; match Some(1) { case Some(v) => v + z case None => 0 };
  var c := var z :| z in s; P(1, 2).(a := z).a;
  var d := var z :| z in s && (var w := 1; z + w == 6); z;
  var e := var x, y :| x in s && y in (var w := 1; {x + w}); x + y;
  print a, " ", b, " ", c, " ", d, " ", e, "\n"; // 6 6 5 5 11
}

method Guards(s: set<int>)
  requires s == {5}
{
  if x :| x in s {
    print (var w := 1; w + x), " "; // 6
  }
  if x :| x in s && (var w := 1; x + w == 6) {
    print x, " "; // 5
  }
  if
  case x :| x in s => print P(1, 2).(a := x).a, "\n"; // 5
  case s == {} => print "unreachable\n";
}

method Main() {
  LetSuchThat({5});
  Guards({5});
}
