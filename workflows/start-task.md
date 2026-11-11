# Start Task

## Purpose

Select a ready-to-use development workspace for a task, creating one only
when an appropriate task workspace is not already available.

A completed selection identifies the existing task session and workspace, or
enters the creation flow. A completed creation flow results in:

- A branch being created.
- A worktree being created.
- The worktree being opened in the selected IDE.
- Verification that the workspace is ready for development.

## Inputs

### Required for Creation

- Description

### Optional

- Identifier
- Repository
- IDE
- Alias
- Explicit branch name
- Type (required only when selecting a configured template)

## Defaults

If Repository is not specified, use the default repository from `repositories.yaml`.

If IDE is not specified, use `copilotApp.ide` inside the Copilot desktop app
and the repository's configured `ide` elsewhere. Follow the editor rules in
`conventions/worktree-lifecycle.md`.

## Dependencies

- conventions/worktree-lifecycle.md
- conventions/create-branch.md
- conventions/create-worktree.md
- conventions/git-safety.md
- conventions/config-validation.md
- config/repositories.yaml

## Process

### 0. Select Workspace

Load `conventions/worktree-lifecycle.md` before provisioning anything.
Apply its workspace-selection rules to distinguish read-only work, continuation
of an existing task session, an already-provisioned isolated workspace, and
work that needs a new workspace.

For continuation or an already-provisioned workspace, report the verified
repository, branch, path, and owning session. Continue through that session
within its permissions and stop this creation workflow here. Do not fetch,
create a branch or worktree, move the workspace, or relaunch its IDE as part
of selection. An editor requested during task setup or code viewing may be
opened separately in the owning session using the editor rules in
`worktree-lifecycle.md`. Read-only work also stops here without provisioning.

If new workbench-managed provisioning is needed, proceed with steps 1-9.
These steps and their required inputs apply only to creation. If using app
provisioning instead, use its supported session mechanism and do not also run
steps 1-9. Selection does not waive creation safety checks or turn a creation
conflict into implicit permission to reuse a workspace.

Before either creation path, load `create-branch.md` and the selected
repository's `branching` configuration, resolve the exact publishing branch,
and apply its app-provisioning/delegation safeguards. Record that destination
alongside the actual local branch. An app-managed worktree may retain its
generated account-prefixed local branch and proceed with implementation
without another naming question. Verify task ownership and the checked-out
local branch before edits or commits; when publishing is separately authorized,
use an explicit refspec to the configured remote branch and verify it before
PR creation. Do not misuse the app's base-branch parameter as a new-branch
name or rename/provision a duplicate worktree to repair a naming mismatch.

### 1. Load Configuration

Load repository configuration from `repositories.yaml`.

Resolve:

- Repository
- Repository path
- Worktree root
- Default IDE

Apply `config-validation.md`, scoped to the resolved repository, to
confirm the repository path exists on disk, is a Git repository, its
worktree root's parent directory exists, and the IDE launcher is
resolvable in `PATH` or executable at its configured path. Expand a leading
`~` before checking a configured path. Abort if validation fails.

### 2. Validate Inputs

Verify the description is provided, then require only the selected branch
strategy's inputs. An explicit-branch strategy requires the exact branch name,
not an unused task type. A template strategy requires its configured type and
every placeholder it uses, including alias/identifier where applicable.

Abort if validation fails.

### 3. Apply Branching Convention

Load `create-branch.md`.

Generate:

- Branch name
- Base remote and base branch

### 4. Apply Worktree Convention

Load `create-worktree.md`.

Generate:

- Worktree path

### 5. Read-Only Safety Preflight

Load `git-safety.md`.

Perform the permitted nonmutating identity, ownership, local state and path
checks. Do not fetch, hydrate objects, invoke hooks or perform other mutations
as preflight. If even metadata access can mutate the checkout, report that
restriction and use an authorised alternative.

Read-only results are preliminary: remote freshness and race-sensitive
conditions are revalidated after approval. Loading Git safety does not execute
all its action-specific procedures before their approval gate.

Abort if validation fails.

### 6. Present Execution Plan

Display:

- Repository
- Repository path
- Branch name
- Worktree path
- IDE
- Planned commands

No changes are performed before the plan is presented.

Wait for explicit user approval before continuing.

### 7. Approved Fetch, Revalidation and Creation

Only after explicit approval, fetch the configured base remote and obtain
fresh branch-conflict evidence for both configured remotes. Revalidate the
base revision, local/remote branch absence, worktree registration and exact
target path immediately before creation. Any failure or conflicting state
stops execution; approval does not permit discarding changes or inventing names.

Create the branch and worktree together from the verified configured base:

```sh
git -C <repository-path> worktree add -b <branch> <worktree-path> <base-remote>/<base-branch>
```

If the operation fails, do not retry with an alternative branch or path.
Report the error and leave any cleanup to explicit user direction, per the
Protected Actions rules in `git-safety.md`.

### 8. Open IDE

Inside the Copilot desktop app, follow the embedded-terminal launch and
screen-verification rules in `worktree-lifecycle.md`. A terminal editor stays
running, so do not wait for it to exit to declare the launch successful.

For an external IDE:

Open the worktree using the selected IDE by invoking the IDE's CLI
launcher (e.g. `code-insiders <worktree-path>`) with the worktree path
as its target, quoted so paths containing spaces are passed correctly.

Launch verification is best-effort:

- Verify the launcher command exits with a zero status code.
- A zero exit code confirms the launcher was invoked successfully; it
  does not guarantee the IDE window fully opened, since most IDE CLI
  launchers return immediately after handing off to a background
  process.
- If the launcher exits with a non-zero status, report the error and
  stop the workflow.

### 9. Verify Workspace

Verify:

- Branch exists
- Worktree exists
- Worktree is attached to the expected branch
- Embedded editor rendered in the terminal, or the external IDE launcher
  exited with a zero status code (best-effort signal only; see step 8)

## Outputs

For read-only work: no new workspace.

For continuation or an already-provisioned workspace:

- Repository, branch, and verified worktree path
- Owning task session
- Existing workspace selected; nothing provisioned

For creation:

- Repository
- Branch
- Worktree
- IDE launch command completed successfully (best-effort signal, see
  step 8/9)
- Ready-to-use development workspace
