# Workbench

Personal development workflows, conventions and reusable agent skills.
Workflows orchestrate, conventions define behaviour, and local configuration
defines workstation-specific settings. Shared contribution policy stays in the
target repository.

## Published and local content

This repository contains a sanitised, portable subset of the local workbench.
Private visibility is not permission to upload company information or secrets.

Tracked content:

- General task, change-assessment, review, accessibility and Git conventions.
- The workspace-selection and task-start workflow.
- The portable Fluent accessibility diagnosis skill and synthetic examples.
- An illustrative repository configuration, not a real workstation inventory.

Local-only content remains excluded by a publication allowlist in `.gitignore`:
the real `config/repositories.yaml`, account-routing instructions, specialist
internal setup and assessment material, browser/debugging helpers, original
documents under `.local/originals/`, and machine-generated files. Existing local
files were retained during repository setup; Git is not their backup.

New files are ignored until explicitly reviewed and allowed. Do not use
`git add -f` to bypass this boundary. Ignore rules do not protect files that are
already tracked, and scanners cannot establish permission to disclose content.
Inspect staged filenames and contents before every publication.

## Local configuration

On a new machine, inspect `config/repositories.example.yaml` and create an
ignored `config/repositories.yaml` with verified repository paths, worktree roots,
editors, remote roles, base branches and branch strategies. Do not overwrite an
existing configuration or invent contribution policies from the example.

The workflows deliberately require the local configuration. Stop with a clear
error if it is missing; the example is not a fallback. Keep any required private
setup or authentication guidance in an authorised local location and load it
explicitly. A clone alone does not recreate local overlays or install tools.

## Entry points

Agents start at [AGENTS.md](AGENTS.md) and
[agent entry](workflows/agent-entry.md). Hosts in other repositories need an
explicit personal pointer; this repository does not activate itself elsewhere.

| Task | Guidance |
| --- | --- |
| Task complexity | [Task triage](conventions/task-triage.md) |
| Implementation planning or review | [Change assessment](conventions/change-assessment.md) |
| Pull request review | [Code review](conventions/code-review.md) |
| Workspace selection and retention | [Worktree lifecycle](conventions/worktree-lifecycle.md) |
| Task workspace setup | [Start task](workflows/start-task.md) and its dependencies |
| Branch and worktree creation | [Branch naming](conventions/create-branch.md), [worktree creation](conventions/create-worktree.md), [Git safety](conventions/git-safety.md) |
| Configuration checks | [Configuration validation](conventions/config-validation.md) |
| Accessibility investigation | [Accessibility triage](conventions/accessibility-triage.md) |
| Related CSS states | [CSS nesting](conventions/css-nesting.md) |

Load only the guidance relevant to the task. Reuse an appropriate existing task
workspace rather than creating another checkout. Diagnosis and review remain
read-only unless implementation is separately authorised; publication and
cleanup keep their existing approval boundaries.

## Skills

[Fluent accessibility diagnosis](skills/fluent-a11y-diagnosis/SKILL.md) verifies
reported behaviour, establishes whether it is a defect, challenges conclusions
and records evidence. Remediation requires approval of the diagnosis and scope.
W3C WAI is the primary accessibility standards reference.

The package includes coordination, testing and reporting guidance, synthetic
examples and structural validation. It does not contain real ticket evidence.
It is not automatically installed in an agent host or MCP server. Read its
entry point and required references explicitly unless host discovery has been
verified; do not assume a slash command exists.

Run its existing structural checks from the workbench root:

```sh
PYTHONDONTWRITEBYTECODE=1 python3 skills/fluent-a11y-diagnosis/scripts/evaluate.py
PYTHONDONTWRITEBYTECODE=1 python3 skills/fluent-a11y-diagnosis/scripts/validate_report.py skills/fluent-a11y-diagnosis/examples/report.json
```

These checks do not prove accessibility conformance, diagnostic accuracy or
actual browser/assistive-technology execution.

## Validation

Use Python 3.9+ and the development dependencies in `requirements-dev.txt` in an
authorised execution workspace. CI installs them in its disposable runner;
local doctor never installs or repairs anything.

```sh
PYTHONDONTWRITEBYTECODE=1 python3 scripts/doctor.py
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tests -v
PYTHONDONTWRITEBYTECODE=1 python3 skills/fluent-a11y-diagnosis/scripts/evaluate.py
```

Default doctor checks portable links, disclosure patterns and example config.
To explicitly inspect local readiness without executing target Git or editors:

```sh
python3 scripts/doctor.py --config config/repositories.yaml --repository example --environment --host copilot
```

Replace `example` with an actual configured alias. Exit 0 means these static
checks passed; exit 1 means a content/configuration/readiness failure; malformed
CLI usage exits 2. Passing does not prove remote permissions or runtime setup.
See the [configuration contract](config/schema.md),
[publication boundary](conventions/publication.md), and
[private overlay recovery](conventions/local-recovery.md).

## Agent-host integration

This repository is a workflow library, not an automatically loaded configuration
layer. Personal agent instructions must explicitly reference relevant entry
points using the actual absolute path of the local clone. Do not copy personal
or private workstation rules into shared target repositories.

Reference task triage for new work, change assessment during planning and review,
code review for PRs, and worktree lifecycle before selecting or provisioning a
local workspace. Load specialist guidance only when applicable. Editing a
document here does not establish that a running agent has read the change.

Scheduler and agent-host integration is a separate setup step. This initial
repository does not configure schedules, permissions, automatic reviews,
publication or cleanup.

Use the [scheduler compatibility checklist](integrations/scheduler.md) before
proposing activation. The [compact handoff](workflows/task-handoff.md) records
loaded guidance, actual authority and remaining checks without adding another
tracking system.
