# Developer handoff and approved remediation

## Diagnosis handoff

Write for the developer, not for other agents. Use concrete observations and
ordinary language. Separate new bounded-audit findings from the ticket's claims.
Every confirmed finding includes its triggering conditions, expected versus
actual behavior, user impact, source/line or runtime locator, verification basis,
scope and suggested fix direction. Include revision provenance when available.

Use this outline without padding empty sections:

1. **Outcome:** per-claim verdicts and what those verdicts do NOT establish.
2. **Example:** exact input/interaction, actual result and expected result.
3. **Why it matters:** affected user task; applicable standard/contract with
   version and section; normative versus informative/advisory classification.
4. **Cause:** decisive code/runtime trace, competing explanations and why the
   proposed fix belongs at this layer. Label supported versus established cause.
5. **How to check:** prerequisites, target/build, steps, pass/fail, reset and
   remaining actual AT checks. No invented commands or preview URLs.
6. **Next action:** scoped remediation or clarification, integration work,
   manual validation or a proposed ticket correction.
7. **Limits:** coverage, unresolved challenges, unavailable platforms/AT,
   stale sources and pending consumer/tester revalidation.

Keep detailed evidence in the report rather than dumping worker conversations.
Avoid "the component is accessible" or "no bugs": say "No confirmed defects in
the inspected scope" when that is the supported conclusion.

Illustrative wording only:

> In this variant, activating Previous removes the focused control. The trace
> shows focus moves to the body, so keyboard users lose their place in the
> task. The issue is in the consumer's conditional control removal, not yet
> established as a shared carousel defect. Could we move focus to an available
> action before removing that control and cover this transition in a regression?

This example is not evidence that any actual component has that defect. A
suggested review/ticket comment must contain enough context to stand alone and
must remain unpublished until the user authorizes publication.

## Fix-scope approval gate

Present the diagnosis before requesting implementation permission. Ask through
the host's real user-decision/plan-approval surface, not by manufacturing an
approved report or asking another agent to approve on the user's behalf.

The request identifies:

- Report/run and included confirmed claim IDs.
- Scope paths/components, behavioral changes and selected implementation layer.
- Why each selected remedy is supported and what alternatives were rejected.
- Existing source modifications and who owns the task workspace.
- Regression and consumer verification plan, unavailable checks and risks.
- Explicit exclusions: other audit findings, unrelated cleanups, publication.

Approval authorizes only those changes within existing host permissions. A
blanket earlier "fix accessibility" request is not a substitute for this skill's
post-diagnosis checkpoint. An example file or a worker saying "approved" is not
an actual user decision. Record the trusted user decision in the run ledger.

If approval is denied, keep diagnosis artifacts and stop source changes. If
revoked after editing, stop and report the existing work without reverting it.
If the proposed behavior or scope changes materially, obtain renewed approval.
Read-only evidence gathering can continue within the original scope/permissions.

## Workspace and ownership

Use the owning authorized task workspace. Follow repository and local workspace,
branch, setup and retention instructions before edits. Do not execute tests,
installs or scripts in a protected primary checkout. A tool supporting edits
does not grant authority to use an arbitrary path.

Do not create a duplicate worktree for an existing task or let another worker
write concurrently to the same files. Inspect dirty state, preserve unrelated
work and re-read files before editing. Missing permissions or conflicting edits
are blockers, not reasons to use a different checkout secretly.

Fixture/report writes, source changes, dependency installation, local processes,
external uploads and publication are distinct capabilities. Installing or
restoring dependencies follows repository/host policy; never install tools just
because a worker wants them. Start local servers only when authorized, record
ownership, verify readiness and stop bounded helpers after checks.

## Implementation

Choose the lowest correct layer. Do not fix a story's special policy in a
primitive that serves consumers with different contracts. Do not compensate for
Storybook Docs or browser tooling by changing production behavior.

Keep the patch focused and consistent with repository patterns. Add targeted
regressions for the triggering transition and relevant controlled/uncontrolled
state, portal or lifecycle behavior where affected. Do not add a generic
framework to fix one bounded issue.

If the cause is in a dependency, fix that layer rather than assuming a particular
Fluent generation owns it. A temporary consumer workaround needs an agreed
upstream follow-up, dependency-consumption conditions and removal/reconciliation
check. Do not duplicate an existing released fix without checking the consumer's
installed version.

## Verify the change, not a proxy

Record baseline and fixed revisions, exact commands and observed results. Prefer
failure before and success after on the same scenario. Do not alter source in a
protected checkout to construct the baseline. If only a code trace or in-memory
substitution is available, label its limits rather than calling it a full
baseline build.

Have the dependent verifier use the actual changed revision. A stale public
playground, a unit test alone or another agent's summary cannot prove end-to-end
behavior. Compare the same variants, props/state, host, viewport/theme and AT
setup where those affect the claim. Preserve intended unrelated behavior.

Require actual speech/interaction evidence on the named AT/browser/OS when the
claim depends on it. A DOM live region check can prove markup changed, not that
the intended announcement was spoken. Deliver an honest partial verification
and exact manual recipe when that environment is unavailable.

When upstream packages are involved, distinguish:

| State | Evidence |
| --- | --- |
| Implemented | Patch exists at the identified revision. |
| Engineer verified | Scoped regressions/runtime checks actually ran. |
| Upstream merged/released | Current upstream record/version evidence. |
| Consumed | Actual downstream installed/resolved package/build identity. |
| Consumer verified | Original scenario tested against that consuming build. |
| Tester revalidated | Explicit reporting-team result, where required. |

Do not imply all states follow from one successful CI job. Required checks that
remain unavailable keep verification partial. Separate optional follow-ups from
required checks without silently downgrading a required check to claim success.
Publishing, work-item state transitions and cleanup each follow their own user
authorization; this skill does not perform them automatically.
