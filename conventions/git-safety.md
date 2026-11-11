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

Before any workflow performs Git operations it must verify:

1. The current directory is a Git repository
2. The repository is in a valid state
3. Required remotes exist
4. The target branch does not already exist
5. The target worktree does not already exist

Workflow execution must stop if validation fails.

---

## Remote Safety

Remote roles are configured per repository in `config/repositories.yaml`:

- `baseRemote` supplies the configured base branch.
- `pushRemote` receives the development branch.
- `baseBranch` is the branch used to create a task worktree.

Workflows must:

- Fetch from the configured `baseRemote`.
- Create the task branch from `<baseRemote>/<baseBranch>`.
- Push only to the configured `pushRemote`.
- Stop if either configured remote or the configured base branch is missing.

Do not infer remote roles from their names or require a `myfork` remote. The
local clones may intentionally push to `origin`.

---

## Branch Safety

Before creating a branch:

1. Fetch remote references
2. Check local branches
3. Check remote branches on the configured `baseRemote` and `pushRemote`
4. Verify target branch does not already exist

If a branch already exists:

- Do not generate an alternative name
- Do not append suffixes
- Do not modify the requested branch name

Workflow execution must stop and report the conflict.

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

After completing Git operations:

1. Verify branch exists
2. Verify worktree exists
3. Verify branch is checked out
4. Verify worktree is attached correctly

Workflow execution is not complete until verification succeeds.

---

## Consumers

This convention may be consumed by:

- start-task
- finish-task
- prepare-pr
- future workflows

Consumers must not weaken or bypass these safety requirements.