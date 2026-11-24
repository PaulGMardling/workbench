# Runnable accessibility PR evidence

This reference is optional for general workbench users. Once selected by the
current user's personal profile, task scope or repository policy, its applicable
requirements are normative. It does not activate itself or grant publication
authority. Load it before preparing applicable PR evidence or declaring readiness.

## Reproduction and fix verification

Use the [evidence guide](evidence-contract.md) for verdicts, freshness and
verification limits, and [implementation scope](remediation-and-delivery.md#implementation-scope)
for edit authority. Reconsider existing patches without discarding them.
This reference adds reviewer-runnable material, not another diagnosis approval.

Include a focused runnable reproduction when preparing/updating an applicable
accessibility PR on GitHub or Azure DevOps. Prefer an editable playground for
supported components, otherwise a faithful repository story/fixture. It
supplements regression tests, not replaces them.

Keep controlled state, slots, portals, keys, styling and keyboard interactions
needed for the defect; use supported imports/CSS. Do not add workaround handlers
that hide it. Never place private source, internal reports or credentials in
public playgrounds or source-bearing URLs. Disclose protected preview access.

Include a copyable **Reproduction and fix verification** recipe usable without
the originating conversation:

- Identify the defect and bounded scenario; state setup, browser/platform,
  relevant assistive technology and initial state.
- Give numbered interactions, including moving keyboard focus into the preview.
  State concrete expected/actual observations and a clear pass/fail condition:
  active element, popup visibility, accessible name/role or ID-reference target.
- Identify runtime and baseline/fixed revisions, and which revision each link
  executes. Observe any selected personal restriction on hashes in PR prose;
  preserve exact revisions in a durable authorised evidence artifact instead.
  Deployed baseline code does not prove that an unmerged PR works.
- Provide a verified PR-preview playground or repository fixture/story ID,
  working directory, actual repository-supported setup/run commands and local
  URL for exercising the fix. Include targeted test commands/assertions when
  available; a unit test alone is not a manual interaction recipe.
- Record commands actually run, observations, verification date/revisions and
  remaining limits. Distinguish DOM/accessibility-tree evidence from actual
  screen-reader speech and consumer verification.

Before publication, open the exact serialized link in a fresh page/reload,
confirm code/CSS load without runtime errors and exercise the stated steps.
Where feasible, observe failure on baseline and success on the fixed revision.
Never claim a fixed result from a deployed baseline, generated untested link,
placeholder or in-memory simulation. If either side cannot run, label it
unverified and state the remaining check. Preserve fixtures in the PR or another
durable permitted location, not only session files or retained agent context.

If a playground is unfaithful or inaccessible, provide the repository fixture
and recipe instead and report the limitation. Bound coverage honestly: Tab-out
alone does not establish shadow-root, cross-origin, controlled-state or
screen-reader correctness.

## Description updates and screenshots

Apply the owning task's delivery rules for authority, live-state checks and
concurrent edits. Preserve templates, unrelated content and PR state; verify
saved evidence links and recheck the recipe/fixed revision after relevant changes.

Load applicable repository-specific personal evidence overlays from the selected
configuration. Missing required guidance blocks the affected readiness decision;
do not silently omit it or substitute a backup.

Supply paired **Before**/**After** screenshots only when needed and useful.
Capture the same scenario, viewport, theme, platform and interaction state;
label them and retain baseline/fixed evidence revisions. If the comparison
disables a fix in memory, say so; it does not prove an unexecuted platform issue.

For semantic/screen-reader fixes without a visible change, prefer relevant
DOM/tree assertions, keyboard steps or actual speech. Do not attach identical
UI captures or imply screenshots prove spoken output/conformance. When images
are required, verify uploaded images render for PR readers and remain linked;
local-only captures/placeholders do not satisfy the requirement. Otherwise
record screenshots as inapplicable rather than blocking on their absence.
