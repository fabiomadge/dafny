# Draft review: dafny-lang/dafny#6544 at `9f392f16b` (Comment)

## Body

The new guard is right. But the description and the test say that constant ordinal arithmetic is
folded before it reaches the solver, and that is false:

```dafny
lemma Undefined() ensures ((0 as ORDINAL) - 1) + 1 == 0 { }
```

On master the old axiom proves this postcondition; only the well-formedness error for `0 - 1`
rejects the program. With this PR the postcondition fails too.

`dafny0/CoinductiveProofs.dfy.expect` conflicts with #6545; whichever lands second regenerates it.

## Inline

### `Source/IntegrationTests/TestFiles/LitTests/LitTest/git-issues/git-issue-6536.dfy`, lines 1–10

Suggest adding `Undefined` as the test of the fix itself; the current lemmas test only where the
axiom now applies. The RUN line then needs `%exits-with 4`
(https://github.com/fabiomadge/dafny/commit/366398279):

```suggestion
// RUN: %exits-with 4 %verify "%s" > "%t"
// RUN: %diff "%s.expect" "%t"

// The axiom for (o - m) + n applies exactly where o - m is defined, m <= o.Offset.
```

and at the end:

```dafny
lemma Undefined()
  ensures ((0 as ORDINAL) - 1) + 1 == 0 // error (twice): 0 - 1 is undefined, and the postcondition does not follow
{
}
```
