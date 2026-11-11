# Git Safety

## Purpose

Define mandatory Git safety requirements that all workflows must follow.

The goal is to:

- Prevent accidental data loss
- Prevent accidental modification of shared branches
- Prevent accidental pushes to upstream repositories
- Ensure operations are predictable and reversible

## Protected Actions

The following actions must never be performed without explicit user approval:

- Delete branches
- Delete worktrees
- Reset commits
- Discard uncommitted changes
- Force push
- Rebase shared branches
- Modify Git remotes
- Change branch tracking configuration

Approval must be requested every time.

Previous approval does not carry forward to future operations.

---

## Repository Validation

Before a workflow performs Git operations, use permitted read-only metadata
to verify:

1. The intended target directory is the verified owning Git repository
2. The repository is in a valid state
3. Required remotes exist
4. The task, branch, workspace and operation have the expected identity and owner
5. The action is authorised under current host and repository restrictions

Workflow execution must stop if validation fails.

---

## Remote Safety

Remote roles are configured per repository in `config/repositories.yaml`:

- `baseRemote` supplies the configured base branch.
- `pushRemote` receives the development branch.
- `baseBranch` is the branch used to create a task worktree.

Workflows must:

- For new task creation, fetch from the configured `baseRemote` only after
  approval of the execution plan, then revalidate the base and conflicts.
- Create a new task branch from `<baseRemote>/<baseBranch>`.
- Push only to the configured `pushRemote`.
- Stop if either configured remote or the configured base branch is missing.

Do not infer remote roles from their names or require a `myfork` remote. The
local clones may intentionally push to `origin`.

---

## Branch Safety

Before creating a branch, after approval of the execution plan:

1. Fetch remote references
2. Check local branches
3. Check remote branches on the configured `baseRemote` and `pushRemote`
4. Verify target branch does not already exist

If a branch already exists:

- Do not generate an alternative name
- Do not append suffixes
- Do not modify the requested branch name

Workflow execution must stop and report the conflict.

### Updating an Existing Task Branch

Existence is a collision during creation, not during verified continuation.
Before each separately authorised push, verify the recorded task owner, local
branch and exact publishing repository/branch. Observe its current remote tip
through the authorised account/transport; unavailable evidence is a blocker,
not evidence that the branch is absent.

For the first publication, stop if the destination branch already exists unless
ownership and intended continuation have been explicitly reconciled. For later
pushes, retain the recorded destination and verify that the observed remote tip
belongs to this task and is an ancestor of the proposed local head. Use a normal
non-force push, which also rejects a concurrent non-fast-forward change.
Unexpected remote commits or ownership changes require reconciliation; never
rename the destination, force push or change tracking as an automatic repair.
This procedure grants no push or merge authority.

---

## Worktree Safety

Before creating a worktree:

1. Verify target path does not exist
2. Verify worktree is not already registered
3. Verify target branch is valid

If a worktree already exists:

- Do not generate an alternative path
- Do not modify the requested path

Workflow execution must stop and report the conflict.

---

## Change Safety

Uncommitted changes must be treated as protected.

Workflows must never automatically:

- Stash changes
- Reset changes
- Discard changes
- Clean untracked files

Workflow execution must stop and require user direction.

---

## Transparency

Before making changes, workflows must display:

- Repository
- Base branch
- Target branch
- Target worktree path
- Commands that will be executed

Users must be able to understand the planned action before execution.

---

## Verification

After branch/worktree creation:

1. Verify branch exists
2. Verify worktree exists
3. Verify branch is checked out
4. Verify worktree is attached correctly

Workflow execution is not complete until verification succeeds.

After an update, verify the actual remote branch points to the intended commit.
After read-only operations, report the facts obtained rather than applying
creation-only postconditions. A successful command alone is not delivery proof.

---

## Consumers

This convention may be consumed by:

- start-task
- finish-task
- prepare-pr
- future workflows

Consumers must not weaken or bypass these safety requirements.