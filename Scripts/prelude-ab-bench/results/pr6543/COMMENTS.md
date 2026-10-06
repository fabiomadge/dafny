# Draft review: dafny-lang/dafny#6543 at `c24a81114` (Approve)

## Body

LGTM. `dafny0/SubsetTypes.dfy.expect` conflicts with #6545; whichever lands second regenerates it.

Nit: the comments above `Map#Items` and `IMap#Items` (lines 886, 1028) say they rely on the two tuple
destructors. They now rely on the constructor too.

Optional: a shorter description and commit message are at https://github.com/fabiomadge/dafny/blob/review-pr6539-bench/Scripts/prelude-ab-bench/results/pr6543/REVIEW.md#suggested-title-commit-message-and-description.
