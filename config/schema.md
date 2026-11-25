# Local repository configuration contract

`repositories.yaml` is ignored, required for repository-dependent setup, and
never replaced by the example. YAML mappings use unique keys; duplicates are
errors. Check unknown fields explicitly so misspellings do not silently disable
rules. This is a reading guide for agents and people, not an executable schema.

| Field | Contract |
| --- | --- |
| `default` | Optional nonempty repository key present in `repositories` |
| `copilotApp.ide` | Optional single CLI executable name or path, not shell arguments |
| `repositories` | Nonempty mapping of unique aliases to entries |
| Entry `path`, `worktreeRoot` | Required nonempty absolute or `~/` paths; no environment-variable interpolation |
| Entry `ide` | Required single executable name or path for non-Copilot use |
| Entry `git` | Exactly `baseRemote`, `pushRemote`, `baseBranch`, each a nonempty string; verify actual roles separately |
| Entry `branching` | Either `explicitBranchRequired: true` or nonempty `templates`; not both |
| `branching.requiresAlias` | Optional boolean for template strategies; require the alias when true |
| `templates` | Task-type keys to nonempty templates; placeholders limited to `{alias}`, `{identifier}`, `{description}` |
| Entry `overlays` | Optional list of distinct workbench-relative Markdown paths, resolving inside the workbench |

Descriptions use the branch convention's kebab-case rules. Types and placeholder
values are required only by the selected strategy. After substitution, validate
the complete name with repository policy and Git syntax, not the template alone.
An example is not permission to change remotes, create resources or publish.

Expand a leading `~/` for path checks. Select an explicit editor override first,
then `copilotApp.ide` inside Copilot, otherwise entry `ide`. Do not interpret
configuration as shell code or run an editor as a health check.

## Check only what the operation needs

The table above describes a complete configuration entry. When authoring or
changing configuration, validate that contract. When using an existing entry,
check only values needed for the selected operation through permitted read-only
tools; do not make an unrelated missing editor or creation setting a blocker.

| Operation | Relevant checks |
| --- | --- |
| Read-only investigation | Target identity and applicable guidance; no local inventory required unless the investigation depends on it |
| Existing workspace selection | Exact repository/path, owning task and actual checkout; applicable setup overlays, not editor or new-branch settings |
| New workspace creation | Repository path, worktree root/parent, base/push roles, base branch, selected naming strategy and required setup overlays |
| Requested editor launch | Verified workspace and selected executable; inspect entry `ide` only when it is the selected editor |
| Existing-task publication | Verified account, repository, publishing remote/branch and current remote tip; retain the recorded destination rather than resolve a new branch name |

Load overlays applicable to the operation. If a declared overlay's relevance is
unclear, read it before deciding it can be skipped. Missing relevant values or
required guidance block that operation; report unrelated configuration gaps
without inventing defaults or claiming the complete entry is valid. Apply
[workspace](../workflows/start-task.md) and
[delivery](../workflows/finish-task.md) for the full operation-specific safeguards.

File existence alone does not establish Git health, remote permissions,
authentication or working dependencies. Perform operation-specific checks
through the authorised workspace workflow without installing a configuration
checker or treating configuration as shell code.
