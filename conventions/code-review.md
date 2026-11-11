# Code Review

## Scope

This personal convention applies to code reviews across all repositories.
Load it when reviewing a pull request.

For the complete review procedure, load
[review protocol](review-protocol.md). Its independence, evidence, deduplication
and publication boundaries apply to initial and follow-up reviews.

Load [change-assessment.md](change-assessment.md) as part of every code review.
Assess necessity, proportionality, and scope alongside correctness before
recommending approval, keeping the detailed assessment rules in that convention.

## Approval Message When No Issues Are Found

When a completed review finds no actionable issues and no unresolved material
concerns about necessity, proportionality, architecture, or scope, suggest a
concise, polite approval message tailored to the PR. Use everyday language
and avoid claiming that the change is proven correct.

Keep the message proportional to the evidence. Do not imply that tests
were run locally when only CI results were inspected. If review blockers
or unresolved leads or material change-assessment concerns remain, explain
them rather than suggesting an unqualified approval. Finding no confirmed
defects is not, by itself, a recommendation to approve.

Example:

> Looks good to me. The refactor preserves the existing behavior and keeps
> the component wrappers consistent. Thanks for the cleanup!

Suggesting or drafting the message does not authorize posting it,
submitting a review, or approving the PR. Wait for explicit authorization
to submit and the user's selected review outcome.
