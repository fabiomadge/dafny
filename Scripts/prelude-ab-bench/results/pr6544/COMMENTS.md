# Draft review: dafny-lang/dafny#6544 at `9f392f16b`

**Event:** Comment

## Review body

The new guard is right: it is exactly where `o - m` is defined, and both conclusions hold there.
But the description and the test comment say that constant ordinal arithmetic is folded before it
reaches the solver, so that a program cannot state the term. It is not folded:

```dafny
lemma Undefined() ensures ((0 as ORDINAL) - 1) + 1 == 0 { }
```

On master the old axiom proves this postcondition, and only the separate well-formedness error for
`0 - 1` rejects the program. With this PR the postcondition is refused too. So "no program is known
to prove `false`" still holds, but only because well-formedness rejects every `o - m` with
`m > o.Offset`.

`dafny0/CoinductiveProofs.dfy.expect` conflicts with #6545: both change its resource counts.
Whichever merges second must regenerate it.

## Inline comments

### `Source/IntegrationTests/TestFiles/LitTests/LitTest/git-issues/git-issue-6536.dfy`, lines 1–10

The test checks only where the axiom now applies. `Undefined` checks the fix itself: its expected
output differs between master and this PR. Suggest adding it, with a one-line header. The test then
expects errors, so the RUN line needs `%exits-with 4`. On
https://github.com/fabiomadge/dafny/commit/366398279:

```suggestion
// RUN: %exits-with 4 %verify "%s" > "%t"
// RUN: %diff "%s.expect" "%t"

// The axiom for (o - m) + n applies exactly where o - m is defined, m <= o.Offset.
```

and at the end of the file:

```dafny
lemma Undefined()
  ensures ((0 as ORDINAL) - 1) + 1 == 0 // error (twice): 0 - 1 is undefined, and the postcondition does not follow
{
}
```
