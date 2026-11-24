# Branch naming and publishing identity

For new task provisioning, load the selected entry's `branching` strategy in
ignored `config/repositories.yaml` and check it against the target repository's
contribution policy. Do not apply a default repository's policy to another task.

## Resolve the name

- `explicitBranchRequired: true` requires the exact user-supplied branch.
- Otherwise select a configured task type and supply every placeholder it uses:
  `{alias}`, `{identifier}`, `{description}`. Do not invent identifiers, substitute
  PR numbers for work-item identifiers, or use an unsupported type/prefix.
- Descriptions are concise lowercase kebab-case subjects, not filler sentences.
  An illustrative `fix/{identifier}-{description}` yields `fix/123-focus-dismissal`.
- A GitHub head label's `owner:` names a fork, not a branch prefix.
- Validate the complete result against repository policy and
  `git check-ref-format --branch`; Git syntax alone does not establish policy.

Resolve the exact name before provisioning or delegating new implementation.
Verify the actual owning checkout/branch before edits or commits.
Keep review-only work on the PR's actual branch. Never rename an active/published
branch, change tracking/PRs or create duplicate workspaces to repair a mismatch.
Such migrations need a separate decision and applicable protected-action approval.

## Host-specific local branch mapping

Only when the selected host cannot provision the configured name, distinguish
its actual local task branch from the configured publishing branch. Prefer a
supported exact-name option; never misuse a base-branch parameter for naming.
An app-generated local branch may remain unchanged in its verified task worktree.
Record both names in the owning context and delegated assignment.

When publication is authorised, use the recorded exact publishing repository,
remote and branch, not an inferred upstream or generated local name:

```sh
git push <pushRemote> HEAD:refs/heads/<configured-branch>
```

Apply [Git safety](git-safety.md#updating-an-existing-task-branch) before the
first and every subsequent publication. Do not add `-u`, change tracking,
rename destinations or publish another branch to accommodate an app tool.
PR creation must target the actual published head; report scope limitations
if a tool cannot select it. Branch mapping grants no push or PR authority.
