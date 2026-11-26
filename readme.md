# Workbench

A portable workflow library with optional specialist skills and separate personal
configuration. Target repositories remain the authority for shared contribution
policy. Read the Markdown directly: there is no runtime, dependency installation,
test suite or validation CI required to use this library. This is not an
installed agent framework or scheduler.

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
prerequisites. See [retiring pointers](#retiring-compatibility-pointers) before
removing one. Reviews and planning remain read-only. Protected Git effects,
new PRs, review submission, scheduler activation and cleanup need their own
authority. A clone does not grant publication consent.

## Personal use versus team adoption

For team use, select the shared entry point and the capabilities actually needed.
Each person supplies their own repository configuration and explicit authority.
Do not copy the owner's private files or presume their automatic delivery,
editor, review-depth or styling preferences apply to somebody else.

A trusted personal host instruction can explicitly designate this checkout as
the current user's personal workbench. Only that selection enables loading an
ignored `.local/agent-profile.md`, unless that instruction explicitly chooses
use without a profile. Missing/unreadable profiles are disclosed, not silently
skipped; expected profiles block only decisions that depend on them, as defined
in [entry](workflows/agent-entry.md#personal-selection-and-authority).
Merely contributing to this repository or finding the file does not select it.

For example, configure the selected host through its supported personal settings:

```text
Use <absolute-workbench-root> as my personal workbench.
Read its workflows/agent-entry.md for each new task, review and resumed assignment.
Load my .local/agent-profile.md; if unavailable, report it and pause dependent work.
```

Replace the placeholder locally. This example does not change host settings,
create a profile or establish consent on anyone's behalf. Preserve already
explicit standing instructions and task opt-outs across delegation/resumption;
do not make an opted-in user repeatedly request ordinary delivery.

For repository-dependent setup, inspect
[the example](config/repositories.example.yaml) and create an ignored
`config/repositories.yaml` with verified paths, remote roles and branch strategy.
Never overwrite existing configuration or use the example as a fallback.
The [configuration guide](config/schema.md) explains the settings. Generic
read-only work does not require a workstation inventory.

## Optional capabilities

### Reviewer agent

[Reviewer](.github/agents/reviewer.agent.md) is an optional
Copilot custom-agent definition. It reads the existing entry and review protocol
rather than duplicating them. Its tool list permits read/search, not shell,
editing or posting. The caller supplies complete diff, PR-comment and execution
evidence and coordinates any required independent second pass.

The `.github/agents/` location supports repository-scoped discovery in compatible
Copilot hosts; it does not install the agent globally or expose it automatically
in other repositories. For cross-repository use, explicitly provide the actual
authorised Workbench root and use the selected host's documented loading
mechanism. Keep the referenced guides available alongside the definition.

Before relying on it, verify the agent appears in the host's catalog, the guides
can be read and the effective tools match the declared list. Definition creation
is not a live compatibility or permission-enforcement test. No plugin, runner or
automatic review pipeline is included.

### Specialist skills and host guidance

[Fluent accessibility diagnosis](skills/fluent-a11y-diagnosis/SKILL.md) contains
evidence-backed diagnosis and supervised remediation, with plain-language
Markdown findings. W3C WAI is its primary standards reference.
[Runnable PR evidence](skills/fluent-a11y-diagnosis/references/pr-evidence.md)
is required only when selected by task, repository or personal policy.

Skills are not automatically registered. Explicitly load their entry and
stage-specific references, or verify the host's supported registration.
Instructions alone do not prove diagnostic accuracy or browser/AT execution.

The [scheduler checklist](integrations/scheduler.md) is optional guidance,
not an installed or verified adapter. Start with one selected host and bounded
trials of loading, delegation, resume and opt-outs. Do not activate integrations
merely to read these documents.

## Publication and private state

Tracked files contain sanitised shared guidance, optional skill instructions and
an illustrative configuration. The explicit `.gitignore` allowlist excludes
real config, profiles, account/setup overlays, internal assessment material,
browser/debugging helpers, originals and task history. New files require
deliberate review and an exact allowlist entry; never force-add them.

Private visibility and passing scanners do not establish disclosure permission.
Inspect staged filenames, modes, links and contents; already tracked files are
not protected by ignore rules. Follow [publication](conventions/publication.md).
Git is not a backup of ignored state: use [private recovery](conventions/local-recovery.md).

## Keeping instructions useful

Read changed guidance in context, follow its references and confirm it agrees
with the current user/host permissions and target repository policy. Check local
configuration only when the operation depends on it. Do not install tooling
merely to read or maintain these instructions.

For code changes in a target project, its own relevant tests and validation still
apply; this instruction library does not replace them. Neither a
[handoff receipt](workflows/task-handoff.md) nor polished instructions prove
agent compliance or host enforcement. Those claims need observed behaviour.

## Retiring compatibility pointers

These are aliases, not separate policy owners:

| Legacy convention | Canonical guidance |
| --- | --- |
| `task-triage.md`, `change-assessment.md` | [Entry decisions](workflows/agent-entry.md#decision-and-proportionality) |
| `code-review.md` | [Review](conventions/review-protocol.md) |
| `worktree-lifecycle.md`, `create-worktree.md` | [Workspace](workflows/start-task.md) |
| `config-validation.md` | [Workspace validation](workflows/start-task.md#validate-a-workspace) and [configuration](config/schema.md) |

Keep the current pointers: configured host instructions still use legacy paths.
When changing a host configuration with its owner's permission, point new
references at the canonical guide. Remove an alias only after positively
accounting for its configured host/user/overlay references and relevant active
or resumable tasks, migrating them with permission. Repository search alone
cannot establish that external callers are gone. Retaining a tiny alias is
preferable to breaking an unknown caller; no deadline requires deletion.
