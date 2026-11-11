# Worktree Creation

## Purpose

Define where worktrees are created and how
worktree paths are generated.

## Inputs

Required:
- Repository
- Branch

## Dependencies

- Repository configuration

## Worktree Root

All worktrees are created beneath the configured
worktree root.

Example:

~/dev/worktrees/<repository>

## Worktree Format

The worktree path is the configured `worktreeRoot` followed by the branch name:

```text
<worktreeRoot>/<branch>
```

The repository is not repeated in this path because `worktreeRoot` is already
repository-specific. Preserve branch separators so the directory layout mirrors
the repository's branch strategy:

```text
~/dev/worktrees/<repository>/user/<alias>/<description>
~/dev/worktrees/<repository>/fix/<issue>-<description>
```

## Validation

Before creating a worktree:

- Resolve repository configuration
- Verify repository exists
- Verify the worktree root's parent directory exists

Existence checks (target path does not exist; worktree is not already
registered) are defined once in `git-safety.md` and must not be
duplicated here.

Workflows must fail rather than generate
alternative paths.

## Consumers

- start-task
- finish-task
- future workflow automation