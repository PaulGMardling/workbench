# Config Validation

## Purpose

Verify that `repositories.yaml` is internally consistent and that
every configured repository actually resolves on disk, before any
workflow relies on it.

This exists so config drift (e.g. a renamed folder that no longer
matches the configured path) is caught proactively, rather than
failing partway through a workflow after a branch has already been
created.

## When To Run

- As a standalone health check, on demand.
- As the first action of any workflow that loads `repositories.yaml`
  (e.g. `start-task`), scoped to just the repository being used.

## Checks

For each configured repository (or just the one in scope, when run
from within another workflow):

1. `default` (if set) refers to a repository that exists in
   `repositories`.
2. `path` is set and exists on disk.
3. `path` is a Git repository.
4. `worktreeRoot` is set. If it does not yet exist on disk, this is
   not itself an error (it may be created on first use), but its
   parent directory must exist.
5. The selected editor is set: an explicit user choice, otherwise
   `copilotApp.ide` inside the Copilot desktop app, otherwise the repository's
   `ide`. It must resolve as a CLI executable in `PATH` or be executable at
   its configured path. Expand a leading `~` before checking a path.
   Keep each repository's `ide` set for use outside Copilot.
6. `git.baseRemote`, `git.pushRemote`, and `git.baseBranch` are set; both
   configured remotes and the base branch exist in the local repository.
7. `branching` defines either `explicitBranchRequired: true` or one or more
   branch templates.

## Validation

Workflow execution must stop and report the specific failing check
and repository if any of the above fail.

Do not attempt to auto-correct paths (e.g. fuzzy-matching a similarly
named folder). Config errors must be fixed explicitly by the user in
`repositories.yaml`.

## Consumers

- start-task
- future workflow automation
