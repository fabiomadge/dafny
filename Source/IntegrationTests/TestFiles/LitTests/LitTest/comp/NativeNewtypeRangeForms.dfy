// RUN: %testDafnyForEachCompiler --refresh-exit-code=0 "%s"

// Ranges over native newtypes, bounded by variables rather than literals, in the forms besides set comprehensions.

newtype u64 = x: int | 0 <= x < 0x1_0000_0000_0000_0000

const TWO_TO_THE_64: int := 0x1_0000_0000_0000_0000
newtype uint64 = x: int | 0 <= x < TWO_TO_THE_64

method Main() {
  var n: u64 := 4;
  var m := map i: u64 | 0 <= i < n :: i * 2;
  print |m|, " ", m[3], "\n";

  print exists i: u64 {:nowarn} | 0 <= i < n :: i * i == 9, "\n";

  var arr := new u64[5];
  forall i: u64 | 0 <= i < n {
    arr[i] := i * 2;
  }
  var x: u64 :| 0 <= x < n && x * x == 9;
  print arr[3], " ", x, "\n";

  // A type bounded by a named constant, like the standard library's.
  var count: uint64 := 4;
  var u := set i: uint64 {:nowarn} | 0 <= i < count;
  print |u|, "\n";
}
