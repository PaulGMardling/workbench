# Developer handoff and remediation

Use the [evidence guide](evidence-contract.md) for verdicts, report contents,
freshness and verification completeness. This reference owns specialist
implementation-scope decisions and fix-layer guidance, not a second reporting
protocol. Follow the owning workbench/repository's workspace and delivery rules.

## Implementation scope

Establish which work the current user actually requested:

- **Diagnosis or review only:** explain the result and proposed remedy; do not
  edit source. Obtain implementation authority if the user then wants a fix.
- **Explicit bounded fix request:** diagnose first, then implement the supported
  remedy within that authority. Do not ask again merely because diagnosis
  completed or verification resumed. A broad "fix accessibility" request is not
  permission to choose arbitrary targets or product behaviour.
- **Material decision or scope change:** pause the affected work and use the
  host's real user-decision/plan-approval surface. Ask when diagnosis calls for
  a materially different target, behaviour, implementation layer, risk or
  collateral work, or when the host requires a separate approval.

Before edits, record the confirmed problem, intended user outcome, affected
target/paths, supported remedy, risks, exclusions and verification plan in the
existing task context. They must fit the actual request and permissions; a
completed report, example approval or worker assertion cannot authorise changes.
If boundaries are unclear, ask the specific missing decision rather than
requesting blanket reapproval. Revoked authority stops affected work; preserve
and report changes already made without automatically reverting them.

Implementation authority does not imply publication, ticket changes or cleanup.
Use separately established task/standing authority for those effects, respecting
opt-outs. Do not make an already authorised publisher repeatedly request
commit/push, and do not make a delegated implementer another publisher.

## Explain the result

Lead with the outcome, then a concrete interaction/input, expected versus actual
result, user impact and supported fix direction. Explain cause only as far as
the evidence supports it. Include a copyable check and remaining limits.
Separate additional audit findings and disputed conclusions. Use everyday
language, not role transcripts or empty report sections.

Illustrative suggested comment, not evidence about an actual component:

> Could we move focus to an available action before removing Previous? In this
> variant, activating it removes the focused control and focus falls to the body,
> so keyboard users lose their place. A regression covering that transition
> would help preserve it.

Drafting a comment does not authorise posting it.

## Implement at the correct layer

Use the verified owning task workspace, preserve unrelated changes and follow
repository setup. Missing access or conflicting ownership is a blocker, not a
reason to move secretly to another checkout.

Fix the lowest correct layer. Do not implement a story's special policy in a
shared primitive, or change production behaviour to compensate for a Docs/tool
harness. Trace dependencies rather than assume a Fluent generation owns the
cause; check whether a released fix already exists in the consumer's version.

Keep the patch focused and consistent with repository patterns. Add targeted
regressions for the triggering transition and affected state/portal/lifecycle
behaviour. A temporary workaround needs agreed removal/consumption conditions,
not a generic framework or unrelated cleanup.

Use relevant [runtime recipes](testing.md) for scenario-specific observations
and, only when selected, [PR evidence](pr-evidence.md) for runnable review material.
Record implementation, actual fixed-revision verification, release, downstream
consumption and tester sign-off separately under the evidence guide; none
automatically follows from another.
