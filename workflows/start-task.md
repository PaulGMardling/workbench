# Workspace

Use only the section needed. Selection and validation do not authorise creation,
fetching, setup, editor launches or cleanup. Apply [Git safety](../conventions/git-safety.md)
before dependent Git operations.

## Select a workspace

1. Read-only work can use permitted metadata/tools or an existing checkout.
   Never create a worktree solely for analysis or read-only delegation.
2. Continue related work in its existing owning task session. Verify repository,
   task/PR, actual branch, workspace path and owner; a similar name is not proof.
3. Use an appropriate isolated workspace already supplied by the session.
   App-managed paths may be outside the configured worktree root; do not move
   them or create a duplicate to satisfy local layout preferences.
4. New work and independent concurrent edits need their own task workspace.
   Use either the supported app provisioning path or manual creation below,
   never both. Do not repurpose another task or switch a shared checkout's branch.

Read-only workers can share the owning task's context without another worktree.
Concurrent writers need isolated workspaces and an explicit integration plan.
Keep coordination with the assigning owner. If identity or suitability is
uncertain, pause that selection and ask rather than guessing.

For an existing task, report its verified session/path/branch and stop selection.
Do not fetch, create, relocate or launch an editor merely to continue it.

## Validate a workspace

This section is independently usable as a read-only health check.
Load local configuration only when the operation depends on it. Match the exact
repository/path, never a fuzzy alias or the default for an unrelated checkout.
Use [the configuration contract](../config/schema.md) and its doctor command.
The example is a fixture, not a fallback for missing personal configuration.

Check the owning repository and task state, required remotes and configured base
through permitted read-only metadata. Check the worktree root's parent before
manual creation; the root itself may not exist yet. Load applicable declared
overlays before dependent authentication, setup or readiness decisions.
Missing required guidance blocks that decision, not unrelated read-only work.

Doctor checks paths and configuration shapes, not actual Git health, remote
permissions, authentication or runtime setup. Do not hydrate objects, invoke
hooks or fetch as read-only preflight. If metadata access itself can mutate a
protected checkout, report the limitation and use an authorised alternative.

An editor is not required for workspace readiness. Validate or launch one only
when requested or selected by the user's personal setup policy; never install
one or launch another editor as a silent fallback.

## Create a workspace

Before either provisioning path, read [branch naming](../conventions/create-branch.md),
the selected repository's configuration and applicable target-repository rules.
Resolve the exact branch/destination and required task inputs before delegation.
Existing tasks retain their branch; this procedure does not authorise renaming.
Require a task description. A configured default repository can supply an
otherwise unspecified target only when consistent with the known task context;
disclose the selection rather than overriding an identified repository.

For app provisioning, use the supported session mechanism. Its base-branch
parameter selects a starting ref, not the name of the new branch. Where local
and publishing names differ, use the branch guide's explicit mapping safeguards.
Do not also perform manual creation.

For manual provisioning:

1. Resolve repository, description and only the selected strategy's required
   type/identifier/alias or explicit branch. Verify the base/push remote roles.
   Form the path as `<worktreeRoot>/<branch>` without repeating the repository;
   preserve branch separators. Validate the complete branch with repository
   policy and `git check-ref-format --branch`, and validate the absolute path.
2. Complete read-only validation above. Show repository, base, exact branch,
   worktree path and planned commands. Obtain explicit creation-plan approval;
   no fetch or other mutation occurs before that approval.
3. After approval, fetch the configured base remote and obtain fresh conflict
   evidence for both base and push remotes. Revalidate the exact base revision,
   local/remote branch absence, worktree registration and target-path absence
   immediately before creation. Unavailable evidence or any conflict is a blocker,
   not permission to append suffixes, reuse another task or discard changes.
4. Create branch/worktree together from the verified base:

   ```sh
   git -C <repository-path> worktree add -b <branch> <worktree-path> <baseRemote>/<baseBranch>
   ```

5. Verify the actual checkout belongs to the expected repository and task, the
   branch and path exist, and worktree registration/checked-out branch agree.
   Perform required repository setup only within its separate authority.
   Report a failed/partial operation; do not invent another name or clean up
   automatically.

Output the owning session, verified repository, branch and path, distinguishing
workspace creation from completed runtime setup or an optional editor launch.

## Retain or propose cleanup

At completion, apply [delivery](finish-task.md) only within current authority.
Retain while agents/processes/PR work are active, work is uncommitted/untracked
or unpushed, or ownership/preservation is uncertain. A clean tree or merged PR
alone does not establish that everything is preserved.

For a cleanup candidate, present the exact session/repository/branch/path and
preservation evidence. Obtain approval for each deletion under Git safety.
Use the owning app's lifecycle operation for app-managed workspaces; archiving
that removes a worktree counts as deletion. Never automatically delete branches,
prune worktrees or remove directories.
