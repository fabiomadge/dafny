// RUN: %run --target cpp --unicode-char false --input ExternDefs.h "%s" > "%t"
// RUN: %diff "%s.expect" "%t"

newtype uint32 = i:int | 0 <= i < 0x100000000
type Pos = x: uint32 | x > 0 witness 1

class Holder {
  var t: (Pos, uint32 -> uint32)
  constructor() {}
}

method ReturnTuple() returns (x:(uint32,uint32))
{
  return (1, 2);
}

function EmptyTuple() : () {
  ()
}

function GetEmptyTuple() : () {
  EmptyTuple()
}

function Test() : (bool, bool) {
  (false, true)
}

method BoolCallee(a:bool) returns (a0:bool, a1:bool)
{
  return a, a;
}

method BoolCaller(a:bool)
{
  var a0, a1 := BoolCallee(a);
}

method GenericCallee<A>(a:A) returns (a0:A, a1:A)
{
  return a, a;
}

method GenericCaller<A>(a:A)
{
  var a0, a1 := GenericCallee(a);
}

method Main() {
  var x := ReturnTuple();
  var y := x.0;
  print y, "\n";

  // A tuple's default holds each element type's default: the witness and the default function.
  var h := new Holder();
  print h.t.0, " ", h.t.1(5), "\n";
}
