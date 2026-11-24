# Git safety

## Authority and protected actions

Current user/host authority controls every operation. An explicit standing
delivery instruction can cover ordinary task-scoped commits, pushes and existing
PR metadata updates; [delivery](../workflows/finish-task.md) explains the boundary.
Reading this repository never supplies another person's consent.

Obtain explicit approval each time before deleting branches/worktrees,
resetting commits, discarding changes, force pushing, rebasing shared branches,
modifying remotes or changing tracking. Earlier approval and ordinary delivery
authority do not cover these protected actions. App archiving that removes a
worktree is deletion too.

## Identity and preservation

Before a Git operation, verify the intended repository, task/owner, actual
branch/workspace, valid state and operation-specific remotes through permitted
read-only metadata. Do not run mutation-capable metadata access in a protected
checkout. Stop dependent work when identity or authority cannot be established.

Preserve pre-existing staged/unstaged/untracked work. Do not automatically stash,
reset, clean or discard it. Unrelated dirt alone does not authorise repairs or
require abandoning an otherwise separable task; pause for user direction when
ownership, overlapping hunks or the required operation cannot be reconciled.

## Creation

The [workspace guide](../workflows/start-task.md#create-a-workspace) owns the
creation sequence and approval gate. Use configured remote roles, never names
inferred from convention: `baseRemote` supplies `baseBranch`; `pushRemote`
receives the development branch. They may be the same remote.

Fetch only after creation-plan approval. Obtain fresh conflict evidence for
both remotes, then verify the exact base, branch absence, target path absence
and worktree registration immediately before creation. An existing branch/path
is a conflict during creation, not permission to repurpose it or invent suffixes.
Verify actual checkout/registration afterwards. Failed creation grants no cleanup.

## Updating an existing task branch

Existence is expected during continuation, not a creation collision. Before each
authorised push, verify the recorded task owner and exact publishing repository,
remote and branch. Observe the current remote tip using the authorised
account/transport; unavailable evidence is a blocker, not proof of absence.

For first publication, stop if the destination exists unless ownership and
intended continuation have been explicitly reconciled. For later pushes, retain
the recorded destination and verify that the observed remote tip belongs to the
task and is an ancestor of the proposed local head. Use a normal non-force push;
it also rejects concurrent non-fast-forward changes. Unexpected remote commits
or ownership changes require reconciliation, not automatic rebasing, renaming,
force pushes or tracking changes.

Verify that the actual remote branch points to the intended committed revision.
A successful command alone is not delivery proof. For read-only operations,
report observed facts instead of applying creation postconditions.
