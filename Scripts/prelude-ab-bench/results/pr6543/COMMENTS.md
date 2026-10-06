# Draft review: dafny-lang/dafny#6543 at `c24a81114` (Approve)

## Body

LGTM. Nit: the comments above `Map#Items` and `IMap#Items` (lines 886, 1028) say they rely on the two
tuple destructors; they now rely on the constructor too.

Optional: a shorter description and commit message: https://github.com/fabiomadge/dafny/blob/review-pr6539-bench/Scripts/prelude-ab-bench/results/pr6543/REVIEW.md#suggested-title-commit-message-and-description.

## Inline

### `Source/IntegrationTests/TestFiles/LitTests/LitTest/git-issues/git-issue-6537.dfy`, lines 4–8

Suggest explaining the test rather than its history:

```suggestion
// Both assertions need the prelude to say that every item of a map or imap is a pair.
```
