# Draft review: dafny-lang/dafny#6543 at `c24a81114`

**Event:** Approve

## Review body

Looks right: the conjunct is needed in both directions, and without type arguments on `Map` there
is no typed alternative.

- `dafny0/SubsetTypes.dfy.expect` conflicts with #6545: both change its resource total. Whichever
  merges second must regenerate it.
- Nit: the comment above `Map#Items` (line 886, and line 1028 for `IMap#Items`) says it relies on
  the two destructors for 2-tuples; it now relies on the constructor `#_System._tuple#2._#Make2` too.
