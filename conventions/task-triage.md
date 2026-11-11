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

- Gather enough permitted read-only context to frame the decision. Before
  implementation, consult a separate, high-level agent where available and
  permitted (a sub-agent, e.g. via the `task` tool) to validate the best path
  forward.
- Present the task and the intended approach to that agent.
- Resolve material disagreements using evidence. Escalate unresolved choices
  affecting correctness, scope or safety rather than every difference in approach.
- If consultation is unavailable or prohibited, disclose that limitation.
  Proceed sequentially only where the approach is sufficiently clear and safe.
  If independence is an explicit requirement, or a material decision remains,
  stop the affected work and request guidance. Do not invent independent approval.
- Once the path and any required decisions are resolved, proceed to execute it —
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
