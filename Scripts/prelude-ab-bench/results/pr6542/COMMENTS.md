# Draft review: dafny-lang/dafny#6542 at `939b457d9` (Approve)

## Body

LGTM: the same shape as #6367's fix of the call form.

Optional: a shorter description and commit message: https://github.com/fabiomadge/dafny/blob/review-pr6539-bench/Scripts/prelude-ab-bench/results/pr6542/REVIEW.md#suggested-title-commit-message-and-description.

## Inline

### `Source/IntegrationTests/TestFiles/LitTests/LitTest/git-issues/git-issue-6533.dfy`, lines 4–6

Suggest explaining the test instead, especially why `var rs := {r};` must stay:

```suggestion
// After the forall statement, the range's call facts (t.n is defined, so t was built by T)
// hold only of values of type T. Of r, which is an R, they would contradict its constructor;
// {r} brings r into play.
```
