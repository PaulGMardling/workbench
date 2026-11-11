# Create Branch

## Purpose

Create a branch name from a task definition using the selected repository's
configured strategy.

`config/repositories.yaml` is the source of truth for local branch generation.
It records each repository's shared contribution policy without placing
personal workstation workflow rules in the repository.

## Inputs

### Required

- Repository
- Description

### Optional

- Type
- Identifier
- Alias
- Explicit branch name

## Branch Strategy

Load the selected repository's `branching` configuration before generating a
branch name.

- When `explicitBranchRequired` is set, require an explicit branch name. Do not
  invent a prefix or infer a template.
- When a template is selected, substitute `{alias}`, `{identifier}`, and
  `{description}`. Required template values must be provided.
- Use only configured task types. Do not substitute another prefix when a type
  is unsupported.

## Repository Rules and Examples

Repository-specific strategies, paths and remote roles stay in the ignored
local configuration. Verify them against the target repository's contribution
instructions rather than inferring a universal upstream naming policy.

For an illustrative `fix/{identifier}-{description}` template and a synthetic
task identifier `123`, the branch is:

```text
fix/123-focus-dismissal
```

Not:

```text
account-123-focus-dismissal
```

In a GitHub head label such as
`owner:fix/123-focus-dismissal`, `owner:` identifies
the fork owner; it is not part of the branch name. Do not add another
account/alias prefix to the configured branch.

Use the actual assigned issue/work-item identifier, not an invented number
or a PR number substituted for the task identifier. If a required identifier
is genuinely missing, resolve it before provisioning rather than silently
dropping it from the template.

## App Provisioning and Delegation

These rules apply to both workbench-created and app-created implementation
sessions. Resolve the exact configured branch name before provisioning or
delegating new implementation work. For app-managed worktrees, distinguish
the app's local branch from this configured publishing branch. Include both
names in delegated task context and verify the actual checked-out branch and
owning workspace before edits or commits.

Use a supported exact-branch provisioning option when available. Do not pass
the desired new branch as an app tool's base branch: a base branch selects
the starting ref, not the new branch name.

If the app creates or retains an account-prefixed local branch, keep that
branch and continue implementation in the verified task worktree. This is
the default, not an exception requiring another naming question. Do not
rename the app's branch, modify app metadata, or create a duplicate worktree
merely to match the configured publishing name.

When a push is separately authorized, publish `HEAD` to the exact configured
branch on the configured push remote using an explicit refspec:

```sh
git push <pushRemote> HEAD:refs/heads/<configured-branch>
```

For the same synthetic task, with `origin` explicitly configured as its push
remote:

```sh
git push origin HEAD:refs/heads/fix/123-focus-dismissal
```

Validate the destination repository and branch using the first-publication or
existing-task update checks in `git-safety.md`. Do not infer the destination
from the local branch name or its upstream. Do not use `-u` or change tracking
as part of this default. Any later push must use the same explicit destination.
PR creation must use that published head branch; if an app tool cannot select
it, report that tool's scope limitation rather than publishing a second branch.
This convention does not itself authorize a push or PR.

Existing active or published branches are not automatically renamed by
this convention. Report a mismatch and obtain separate approval for a
migration that changes existing branches, upstream tracking, PRs, or app
session metadata. Keep review-only sessions on the PR's actual branch.

## Description Rules

Descriptions must:

- Use lowercase kebab-case
- Be concise and recognizable
- Remove punctuation
- Remove filler words
- Focus on the subject of the work

Good:

- popover-group-role
- axios-upgrade
- start-task-workflow

Bad:

- fix-the-popover-group-role-bug
- work-on-accessibility-issue
- misc-changes

## Type Definitions

### bug

Work fixes an existing defect.

### feat

Work introduces or enhances functionality.

### chore

Work supports the codebase without changing functionality.

### docs

Work updates documentation without changing implementation behavior.

## Validation

Before creating a branch:

1. Verify the selected repository and required template inputs are present.
2. Verify the generated or explicitly supplied branch name conforms to the
   selected repository's configuration.

Git accepting a name through `git check-ref-format --branch` checks syntax,
not the configured naming convention; both must be satisfied. Recheck the
actual task branch before the first commit. For app-managed worktrees, also
verify the recorded local-to-publishing mapping before any push or PR creation;
the remote destination must satisfy the configured naming convention even
when the local app branch does not.

Existence checks (local and remote) are defined once in `git-safety.md`
and must not be duplicated here.

Workflows must fail rather than generate alternative branch names or substitute
an unsupported branch convention.

## Consumers

- start-task
- future workflow automation