// RUN: %testDafnyForEachCompiler --refresh-exit-code=0 --compilers cs,java,go,js,dfy,py,rs "%s"
// C++ is left out because it does not compile ranges over native newtypes yet.

// Comprehensions over native newtypes, bounded by variables rather than literals.
// NativeNewtypeRangeForms.dfy has the forms that C++ does not support.

newtype i32 = x: int | -0x8000_0000 <= x < 0x8000_0000
newtype i64 = x: int | -0x8000_0000_0000_0000 <= x < 0x8000_0000_0000_0000
newtype u64 = x: int | 0 <= x < 0x1_0000_0000_0000_0000

method Main() {
  var n: u64 := 4;
  var a := set i: u64 {:nowarn} | i < n;
  var b := set i: u64 {:nowarn} | i <= n;
  print |a|, " ", |b|, "\n";

  var c: i32, d: i32 := -2, 2;
  var e := set i: i32 {:nowarn} | c <= i < d;
  var f := set i: i32 {:nowarn} | d <= i < c;
  print |e|, " ", |f|, "\n";

  var lo: i64, hi: i64 := -0x7FFF_FFFF_FFFF_FFFF - 1, -0x7FFF_FFFF_FFFF_FFFE;
  var g := set i: i64 {:nowarn} | lo <= i <= hi;
  print |g|, " ", lo in g, "\n";

  var max: u64 := 0xFFFF_FFFF_FFFF_FFFF;
  var h := set i: u64 {:nowarn} | max - 2 <= i <= max;
  print |h|, " ", max in h, "\n";

  var mid: u64 := 0x7FFF_FFFF_FFFF_FFFF;
  var k := set i: u64 {:nowarn} | mid <= i < mid + 3;
  print |k|, "\n";

  var pairs := set i: u64, j: u64 | i < n && i <= j < n :: (i, j);
  print |pairs|, "\n";

  // A constant bound that is tighter than the type's stays in use.
  var large: u64 := 0x1_0000_0000;
  var small := set i: u64 {:nowarn} | i < 10 && i < large;
  print |small|, "\n";
}
