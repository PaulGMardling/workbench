# Finish implementation and deliver

## Standing delivery default

This records the user's standing instruction across their repositories:
completed implementation work includes committing the task changes, pushing
them and keeping an existing open PR's title and description current. Do not
stop at "ready to commit" or request another commit/push instruction.

Delivery is opt-out: an explicit "do not commit", "do not push", "keep local"
or narrower instruction limits the affected operation for that task. Record
the restriction and carry it through delegation and resumption. Otherwise
repeat delivery for completed follow-up fixes within the same approved scope.
Creating a PR is opt-in: create one only when the user requests it.
Skip opted-out steps without repeatedly asking to perform them. PR metadata
must describe the published head, not claim that local-only work was delivered.

The owning coordinator/publisher performs delivery once for the task. Delegated
workers return their changes and evidence to that owner; this default does not
make every implementation worker an independent committer or publisher.

This default applies to authorised implementation, not review, diagnosis,
planning or suggestions. It does not authorise unrelated edits, merging,
approving/submitting reviews, posting comments, changing draft/ready state,
destructive Git actions, changing remotes/tracking, or activating a scheduler.
The host's permissions and repository policies still control. If they require
a task-specific permission that this standing instruction cannot satisfy,
report the exact restriction and obtain that permission rather than bypassing
it or silently skipping delivery.

Load this workflow before implementation, together with
[Git safety](../conventions/git-safety.md), the target repository's instructions
and applicable authentication/setup overlays. Apply
[publication checks](../conventions/publication.md) before uploading content.

## Establish ownership and destination

Record initial staged/unstaged changes and task-owned hunks before editing.
Keep unrelated changes and pre-existing staged content out of the commit.
A file path alone does not establish ownership: if edits overlap and cannot
be separated confidently, pause the affected commit rather than stage the
whole file or rewrite another person's work.

Verify the owning task/session, actual checked-out branch, account, configured
publishing remote/repository/branch and any existing PR identity. Use the
recorded explicit user-approved destination for an existing task where
applicable; otherwise resolve local configuration through
[branch naming](../conventions/create-branch.md). The standing default supplies
authority, not missing configuration or destination evidence. Do not infer the
push target from an upstream or similar branch name, switch branches, provision
a duplicate worktree or choose a default/protected branch automatically.

Resolve a task's existing PR from the recorded locator or a unique verified
match for its exact head repository and publishing branch, confirming task
scope and intended base. Record that identity. Ambiguous matches block PR
metadata editing, not independently safe commit/push steps. A closed/merged PR
is not an edit target or permission to create a replacement.

## Delivery sequence

1. Complete repository-required and task-relevant validation. Distinguish new
   failures from established baseline failures and optional/unavailable checks.
   Do not claim completion or silently waive required failing/unavailable checks;
   explain the blocker and obtain direction if delivery needs an exception.
2. Inspect the final task diff. Stage only owned changes using explicit paths
   or hunks, then inspect the exact index, including filenames and modes.
   Commit the completed task changes with the repository's message/trailer
   rules. Do not amend or create an empty/duplicate commit on a resumed run.
3. Recheck account, destination, local branch and current remote tip. Apply
   [existing-task push checks](../conventions/git-safety.md#updating-an-existing-task-branch);
   push normally with the explicit publishing refspec. Do not force push,
   rename destinations or change tracking to repair a failure. Verify the
   remote branch equals the intended committed revision.
4. If the task has an existing open PR, synchronise its metadata below against
   the final net diff and intended base. No PR is a normal outcome when its
   creation was not requested; it is not a reason to stop before commit/push.
5. Verify the saved metadata and report the actual delivery state concisely:
   committed/pushed revision, existing PR if any, or exact blocked steps.
   Retain the workspace under [worktree lifecycle](../conventions/worktree-lifecycle.md);
   delivery never authorises cleanup.

## Keep an existing PR current

Re-read the PR's live state, head/base and title/body after pushing and
immediately before editing. Confirm the remote PR head is the intended revision.
Review the final net change, not just the latest commit or the original task
description. Update a stale title to describe the actual scope while retaining
required prefixes, issue references and deliberate author wording where accurate.
Do not rewrite an already accurate title merely to show activity.

Refresh the task-owned summary, relevant validation/limitations and evidence.
Preserve the live repository template, headings, comments, checklists,
unrelated author content, attachments and draft/ready state. Reconcile
concurrent edits using the host/provider's guarded edit mechanism; re-read and
merge on a conflict rather than overwrite newer content. Follow the provider's
supported metadata tools and authentication rules.

Where the host requires an Agent assessment, refresh its single versioned block
at the top using the host's exact schema, current final head revision and
observed evidence. Honour an explicit opt-out. Never fabricate scores or CI
results, duplicate the block or introduce a GitHub-only format into another
provider without a requirement. The exact required assessment revision field
is the only exception to the personal no-commit-hashes-in-description rule.

If publication or metadata editing fails or has an uncertain result, inspect
the remote/PR before retrying. Do not repeat successful steps or create
another commit/PR to recover. Report partial delivery explicitly, for example
"pushed; PR description update blocked by authentication", with the remaining
action. Never turn a metadata failure into an assertion that nothing was pushed.
