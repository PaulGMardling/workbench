# Workbench

A portable workflow library with optional specialist skills and separate personal
configuration. Target repositories remain the authority for shared contribution
policy. This is not an installed agent framework or scheduler.

## Start here

Read [AGENTS.md](AGENTS.md) and [agent entry](workflows/agent-entry.md). Entry
contains proportionate triage and routes to three operational guides:

| Need | Guide |
| --- | --- |
| Select, validate, create or retain a workspace | [Workspace](workflows/start-task.md) |
| Implement, commit/push or maintain an existing PR | [Delivery](workflows/finish-task.md) |
| Review code or a plan | [Review](conventions/review-protocol.md) |

Load only the applicable sections. The short legacy convention files remain
compatibility pointers for existing host instructions; they are not extra
prerequisites. Reviews and planning remain read-only. Protected Git effects,
new PRs, review submission, scheduler activation and cleanup need their own
authority. A clone does not grant publication consent.

## Personal use versus team adoption

For team use, select the shared entry point and the capabilities actually needed.
Each person supplies their own repository configuration and explicit authority.
Do not copy the owner's private files or presume their automatic delivery,
editor, review-depth or styling preferences apply to somebody else.

A trusted personal host instruction can explicitly designate this checkout as
the current user's personal workbench. Only that selection enables loading an
ignored `.local/agent-profile.md`, if present. Merely contributing to this
repository or finding the file does not select it.

For example, configure the selected host through its supported personal settings:

```text
Use <absolute-workbench-root> as my personal workbench.
Read its workflows/agent-entry.md for each new task, review and resumed assignment.
```

Replace the placeholder locally. This example does not change host settings,
create a profile or establish consent on anyone's behalf. Preserve already
explicit standing instructions and task opt-outs across delegation/resumption;
do not make an opted-in user repeatedly request ordinary delivery.

For repository-dependent setup, inspect
[the example](config/repositories.example.yaml) and create an ignored
`config/repositories.yaml` with verified paths, remote roles and branch strategy.
Never overwrite existing configuration or use the example as a fallback.
The [schema](config/schema.md) defines the contract. Generic read-only work does
not require a workstation inventory.

## Optional capabilities

[Fluent accessibility diagnosis](skills/fluent-a11y-diagnosis/SKILL.md) contains
evidence-backed diagnosis, supervised remediation and structural reporting.
W3C WAI is its primary standards reference. Its detailed reporting protocol is
for users/consumers that need it, not a prerequisite for ordinary development.
[Runnable PR evidence](skills/fluent-a11y-diagnosis/references/pr-evidence.md)
is required only when selected by task, repository or personal policy.

Skills are not automatically registered. Explicitly load their entry and
stage-specific references, or verify the host's supported registration.
Synthetic checks do not prove diagnostic accuracy or browser/AT execution.

The [scheduler checklist](integrations/scheduler.md) is an optional design,
not an installed or verified adapter. Start with one selected host and bounded
trials of loading, delegation, resume and opt-outs. Do not activate integrations
merely to read these documents.

## Publication and private state

Tracked files contain sanitised shared guidance, checks, the optional skill and
synthetic fixtures. The explicit `.gitignore` allowlist excludes real config,
profiles, account/setup overlays, internal assessment material, browser/debugging
helpers, originals and task history. New files require deliberate review and an
exact allowlist entry; never force-add them.

Private visibility and passing scanners do not establish disclosure permission.
Inspect staged filenames, modes, links and contents; already tracked files are
not protected by ignore rules. Follow [publication](conventions/publication.md).
Git is not a backup of ignored state: use [private recovery](conventions/local-recovery.md).

## Validation

Use Python 3.9+ with `requirements-dev.txt` installed in an authorised execution
environment. CI uses a disposable runner; doctor never installs or repairs.
PyYAML reads configuration and markdown-it-py parses Markdown destinations.

```sh
PYTHONDONTWRITEBYTECODE=1 python3 scripts/doctor.py
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tests -v
PYTHONDONTWRITEBYTECODE=1 python3 skills/fluent-a11y-diagnosis/scripts/evaluate.py
PYTHONDONTWRITEBYTECODE=1 python3 skills/fluent-a11y-diagnosis/scripts/validate_report.py skills/fluent-a11y-diagnosis/examples/report.json
```

Doctor checks the publication boundary, disclosure patterns, rendered Markdown
links/images (including references and HTML `href`/`src`) and example config.
It ignores link-shaped code examples, does not fetch remote URIs or validate
anchors, and requires local targets to be published files. It is not a complete
secret, HTML or URL-safety scanner.

For explicitly selected local health checks:

```sh
python3 scripts/doctor.py --config config/repositories.yaml --repository example --environment --host copilot
```

Replace `example` with a verified configured alias. Environment mode includes
the configured editor's availability; distinguish an editor-only failure from
workspace validity when editor setup was not requested. No target Git, network,
authentication or runtime verification is performed.

Exit 0 means the selected static checks passed, 1 means content/configuration/
readiness failure, and 2 means invalid CLI usage. Neither these checks nor a
[handoff receipt](workflows/task-handoff.md) proves agent compliance or host
enforcement. Host setup and compatibility claims need observed behavioural trials.
