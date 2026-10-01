// RUN: %testDafnyForEachCompiler "%s"

// A Java for statement updates its loop variable, and a Java lambda cannot capture a variable that
// is reassigned. The datatype updates and let expressions below are compiled into Java lambdas.

datatype D0 = DC1(cf1: int, cf2: int)

newtype int8 = x | -128 <= x < 128

method Main() {
  for i := 1 to 3 {
    print DC1(1, 2).(cf1 := i), " ";
  }
  print "\n"; // D0.DC1(1, 2) D0.DC1(2, 2)

  for i := 3 downto 1 {
    print (var w := 10; w + i), " ";
  }
  for i: int8 := 0 to 3 {
    if i == 1 {
      continue;
    }
    print (var w := 10; w + i), " ";
  }
  for i := 0 to *
    invariant i <= 2
    decreases 2 - i
  {
    if i == 2 {
      break;
    }
    print (var w := 10; w + i), " ";
  }
  print "\n"; // 12 11 10 12 10 11
}
