# Accessibility Triage

## Purpose and entry point

Load after task complexity triage and before delegating accessibility
implementation, preparing a patch, or advancing an existing fix for review.
Apply it to new reports, bounded component audits and reassessment of existing
patches. Read-only investigation does not require provisioning a workspace.

The reusable protocol now lives in
[the Fluent accessibility diagnosis skill](../skills/fluent-a11y-diagnosis/SKILL.md).
Read its entry point and required references before a full run. Maintain the
diagnostic rules there rather than keeping a second copy in this convention.
This pointer does not require skill installation: explicitly reading the package
is supported when the host has not registered its name.

The protocol requires an explicit evidence-backed verdict on whether each claim
is a real accessibility defect before selecting a fix. It includes isolated
reproduction, W3C WAI standards applicability, optional sister-component
comparisons, bounded auditing, independent challenge, developer explanation and
approval-gated remediation. Reproduced behavior is not automatically wrong;
failed reproduction is not "not an issue". Apply it across Fluent websites,
v0, v8, v9, headless and other implementations; do not assume a fix layer.

## Personal workflow overlay

The skill is portable; these personal rules stay in workbench:

- Follow `task-triage.md` for complexity consultation and
  `worktree-lifecycle.md` before selecting or delegating local workspaces.
  Follow `workflows/start-task.md` and its dependencies when provisioning is
  actually needed. Do not create a workspace solely for read-only analysis.
- Read repository instructions and the configured branch/account/setup
  conventions before approved implementation. Use the owning authorized task
  workspace, never a protected primary checkout for execution.
- Complete the skill's per-claim validity and evidence gate before advancing
  each fix. Preserve existing patches while reconsidering their assumptions.
  Do not advance multiple uncertain fixes simply to create parallel activity.
- Follow **Personal Accessibility PR Reproductions** in
  `worktree-lifecycle.md` for runnable playground/fixture recipes, baseline and
  fixed revisions, human/agent reproduction, and actual consumer verification.
  Keep screenshots conditional on reviewer value, not a universal readiness gate.
- Diagnosis and component audit do not authorize fixes. Approve the specific
  diagnosis/remediation scope first. Implementation approval does not authorize
  comments, commits, pushes, PRs, ticket disposition changes or cleanup.
- Individual tickets, colleague conversations, assignments and transient PR
  states belong in authorized task records, not the portable skill.

Repository/host restrictions and user permissions remain controlling; neither
this convention nor the skill grants access or authorizes publication.
