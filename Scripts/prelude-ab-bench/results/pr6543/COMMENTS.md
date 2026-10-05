# Draft review: dafny-lang/dafny#6543 at `c24a81114` (Approve)

## Body

LGTM. `dafny0/SubsetTypes.dfy.expect` conflicts with #6545; whichever lands second regenerates it.

Nit: the comments above `Map#Items` and `IMap#Items` (lines 886, 1028) say they rely on the two tuple
destructors. They now rely on the constructor too.
