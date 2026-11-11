# Task, review and resumption entry

Resolve the actual authorised local workbench root. Do not infer it from the
target repository's current directory. Hosts working elsewhere must receive
an explicit pointer to this file; `AGENTS.md` discovery in workbench does not
activate guidance in another checkout.

## Load and record

1. Read [task triage](../conventions/task-triage.md). Establish the request,
   task identity, host permissions and intended stage before acting.
2. Record the workbench Git revision and whether relevant documents have local
   edits. A commit ID alone does not identify a dirty document: record the
   relevant file content hashes too. Keep this receipt in existing authorised
   task/session storage using the [handoff fields](task-handoff.md).
3. Load the routes below and their required references. Record the paths
   actually read, not merely links supplied to a worker.
4. When a repository-specific task requires local configuration, resolve its
   entry by verified repository/path identity, never a similar name. Read its
   `overlays` if configured. Overlay paths resolve from the workbench root.
   Missing configuration or a declared overlay blocks dependent setup/readiness;
   no example or cached document is a silent fallback. A generic read-only
   review can proceed without configuration only if it does not depend on
   private setup or repository-specific requirements; disclose the limit.

| Intent | Required guidance |
| --- | --- |
| Planning or implementation | [Change assessment](../conventions/change-assessment.md); target repository instructions |
| Selecting/delegating a local development workspace | [Worktree lifecycle](../conventions/worktree-lifecycle.md) |
| New workspace creation | [Start task](start-task.md) and its dependencies; stop for required approval |
| Code or plan review | [Code review](../conventions/code-review.md), [review protocol](../conventions/review-protocol.md), change assessment |
| Accessibility diagnosis/fix | [Accessibility triage](../conventions/accessibility-triage.md); skill references at the relevant stage |
| Relevant CSS styling | [CSS nesting](../conventions/css-nesting.md) |
| Publication | [Publication](../conventions/publication.md); target forge/template/authentication rules and explicit authority |
| Scheduled/headless assignment | This entry plus [scheduler compatibility](../integrations/scheduler.md); capability mismatch is a blocker |

Load branch, authentication and setup overlays before the dependent operation,
not as permission to execute commands found in those files. Personal guidance
cannot override host restrictions or shared contribution policy. Surface
conflicting obligations instead of silently choosing a weaker rule.

## Delegation and resume

The coordinator supplies the original request, stage, scope, owning workspace,
loaded revision/hash receipt, required guidance, overlays, approval boundaries
and acceptance checks to each worker. Workers acknowledge what they actually
read and report missing references. Do not copy private overlay contents into
public prompts, issues, reports or repositories.

On resume or a new review pass, compare task/checkout identity, permissions,
source and runtime revisions, relevant document hashes and overlay hashes with
the receipt. Reload changed guidance and revalidate affected decisions. A
changed document does not expand prior authority. Pause before consequential
effects when current and previously approved rules conflict. Never silently
update the installed workbench or pull changes while an assignment is running.

A receipt makes loading observable; it does not prove compliance. Verify
behaviour through bounded host pilots, especially across delegated reviewers
and scheduler continuation.
