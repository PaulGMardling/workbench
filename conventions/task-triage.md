# Task Triage

## Purpose

Define the first decision every agent makes when a task is received,
before any workflow or convention-specific logic is loaded.

This is the entry point of the decision tree: classify the task as
simple or complex, then follow the corresponding path.

## When To Run

Always, first — before selecting or applying any workflow
(e.g. `start-task`) or other convention.

## Step 1: Classify the Task

Determine whether the task is **simple** or **complex**.

This is a judgment call for the agent. No fixed criteria (file count,
step count, etc.) are prescribed — use the overall shape of the task:
how well-understood the path to completion is, how reversible the
actions are, and how confident the agent is that a single approach is
correct.

## Step 2: Follow the Matching Path

### Simple Path

If the task is simple:

- Complete the task directly.
- No second-agent consultation is required.

### Complex Path

If the task is complex:

- Before taking any action, consult a separate, high-level agent
  (a sub-agent, e.g. via the `task` tool) to validate the best path
  forward.
- Present the task and the intended approach to that agent.
- Reconcile any disagreement between the two perspectives before
  proceeding. If the two agents cannot agree on a path forward, stop
  and surface the disagreement to the user rather than picking one
  side unilaterally.
- Only after the path forward is agreed, proceed to execute it —
  applying any relevant workflow or convention as normal.

## Change Assessment

After selecting the simple or complex path, load
[change-assessment.md](change-assessment.md) when planning implementation or
assessing a proposed change. Apply its necessity, proportionality, and scope
assessment before implementation, and revisit it when complexity grows.
Keep the assessment proportionate; it does not replace the triage or
consultation workflow above.

## Accessibility Work

After selecting the simple or complex path, load
`conventions/accessibility-triage.md` for accessibility work before delegating
implementation or preparing a patch. Its evidence gate also applies when
reassessing or advancing an existing fix. Complexity consultation does not
replace establishing the expected behavior and correct fix layer.

## Consumers

- All workflows and agent task handling.
- This convention governs the point at which any other workflow
  (e.g. `start-task`) is entered.
