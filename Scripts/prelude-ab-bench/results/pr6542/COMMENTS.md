# Draft review: dafny-lang/dafny#6542 at `939b457d9`

**Event:** Approve

## Review body

Looks right: the type antecedent now encloses the range's call facts, the shape #6367 gave the call
form. One suggestion on the test.

## Inline comments

### `Source/IntegrationTests/TestFiles/LitTests/LitTest/git-issues/git-issue-6533.dfy`, lines 4–6

The `// error:` marker already says this was once provable. What a reader needs is why the test
is shaped this way, especially `var rs := {r};`, which looks removable but isn't: without it, or
without the parameter `r`, master no longer proves `false`.

```suggestion
// After the forall statement, the range's call facts (t.n is defined, so t was built by T)
// hold only of values of type T. Of r, which is an R, they would contradict its constructor;
// {r} brings r into play.
```
