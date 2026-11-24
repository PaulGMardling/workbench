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

Before relying on an entry, check its required values against this guide and
confirm paths, repository identity and declared overlay readability through
permitted read-only tools. For creation, check the worktree root's parent;
for requested editor setup, check the selected executable separately.
Do not waive missing required overlays or repository/path failures.

File existence alone does not establish Git health, remote permissions,
authentication or working dependencies. Perform operation-specific checks
through the authorised workspace workflow without installing a configuration
checker or treating configuration as shell code.
