# Worktree Lifecycle

## Purpose

Use one workspace per active task by default, not one per agent or conversation.
Preserve isolation for independent edits without accumulating unnecessary local
worktrees.

## When To Load

After task triage, before selecting, provisioning, or delegating a local
development session. Apply this convention before the creation workflow in
`workflows/start-task.md`.

## Workspace Selection

1. For read-only investigation, use available read-only tools or an existing
   checkout within the current permissions. Do not provision a worktree solely
   for analysis or read-only delegation.
2. For related work, prefer continuing the existing task session. Inspect
   available session metadata and, where permitted, read-only Git metadata to
   confirm the repository, task or PR, branch, worktree path, and active owner.
   A similar branch name or an existing directory alone is not sufficient.
3. If the current session already has an appropriate isolated worktree, use it.
   App-provisioned worktrees may live outside the configured workbench root;
   do not relocate them or run the creation workflow to make a second worktree.
4. Provision a separate workspace for a new task or independent concurrent edits
   that need isolation. Follow the supported app provisioning path or the
   workbench creation workflow, not both for the same task.

Before either provisioning path for new implementation work, resolve the
branch through `conventions/create-branch.md` and
`config/repositories.yaml`. App-generated branch names do not override that
strategy for publishing. App-managed worktrees may keep their generated local
branch and proceed without another naming confirmation. Record and verify both
the actual local branch and configured publishing branch when delegating;
publish only through the explicit refspec in `create-branch.md` when separately
authorized. Follow its existing-branch safeguards; do not rename an active
branch or create another worktree merely to correct an app-generated name.

If task identity, ownership, or workspace suitability is uncertain, ask the user
before selecting or creating a workspace. Do not switch a shared checkout's
branch or repurpose another task's worktree to avoid creating a new one.
Respect tool access restrictions; reuse does not grant write access.

## Editor Inside Copilot

In the Copilot desktop app, prefer terminal-code in an embedded terminal
canvas instead of launching an external IDE. Read `copilotApp.ide` from
`config/repositories.yaml`; an explicit user editor choice takes precedence.
Outside the app, retain each repository's configured `ide`.

Use the verified worktree of the owning task session, not the primary
checkout or a general chat's scratch directory. Workspace selection alone
does not launch an editor. When the user requests code viewing or task setup,
open the editor in that session's terminal with the absolute launcher path
and quoted absolute worktree path. Expand `~` to the user's home directory
before quoting. Reuse an existing editor terminal for that task; do not send
shell commands into a terminal running an installer or another interactive
program. Do not create a worktree just to open the editor.

For terminal-code, launch `<launcher> "<worktree-path>"`; for source-control
viewing, use `<launcher> --review "<worktree-path>"`. Prefer a terminal canvas
alongside the conversation rather than terminal-code's own split option.
Verify that the editor renders using the terminal canvas's screen output.
If the launcher is missing or the terminal cannot render it, report the
problem; do not install software or silently launch an external IDE.
Do not import VS Code settings or extensions unless requested.

## Delegation

Delegation alone does not require another worktree. Keep related work in the
owning task session and use read-only subagents without new checkouts when
supported. Route continuation through the existing session rather than starting
another writer against its checkout.

Independent concurrent writers require isolated worktrees and an explicit
integration plan. The coordinator records the owning session, task, repository,
branch, and workspace path in its task context and coordinates dependent work.
If the tool cannot safely reuse a session, report that limitation rather than
silently creating duplicates or sharing a mutable checkout.

## Creation and Safety

Workspace selection is distinct from creation. Once creation is selected,
`workflows/start-task.md`, `conventions/create-worktree.md`, and
`conventions/git-safety.md` retain their existing approval, naming, validation,
and conflict rules. An existing branch or path discovered during creation is
a conflict, not permission to silently switch to reuse or invent another name.

This convention does not authorize Git mutations or weaken protected-action
and uncommitted-change safeguards. Preserve existing changes; when the safety
rules require user direction, stop rather than stash, reset, or clean.

## Completion and Retention

### PR Description Style

Keep PR descriptions concise and focused on the problem, the change, and what
reviewers need to check. Follow the repository's required template without
turning the description into an investigation log.

Never include commit hashes in PR descriptions, including abbreviated hashes
or hashes embedded in links and image filenames. Keep revision identifiers in
a separate evidence comment or artifact when traceability is needed. Refer to
the PR branch or named baseline in the description instead.

### Personal Accessibility PR Reproductions

Before implementing or advancing an accessibility fix, load
`conventions/accessibility-triage.md` and complete its evidence gate: establish
expected behavior, reproduce in isolation, compare relevant implementations,
explicitly assess whether each reported claim is a real accessibility defect,
and identify the correct fix layer. The requirements below describe how to
make that evidence runnable for reviewers; they do not establish that the
ticket's requested behavior or proposed patch is correct.

For my accessibility fixes, include a focused, runnable reproduction in the PR
description when preparing or updating the PR. Prefer an editable playground
link for supported components. Apply this to GitHub and Azure DevOps PRs;
this is a personal workflow requirement, not shared repository policy.
Load this section before preparing PR evidence or declaring the task ready
for review. A playground supplements regression tests; it does not replace them.

Keep the example small but faithful to the defect: preserve the relevant
controlled state, slots, portals, keys, styling, and keyboard interaction.
Use imports supported by the target playground and include any required CSS.
Do not add workaround handlers that mask the bug. Never put private source,
internal report details, credentials, or other sensitive data in public
playgrounds or source-bearing URLs. For protected deployments, disclose
sign-in requirements and what could not be verified.

Include a copyable **Reproduction and fix verification** recipe alongside
the link, usable by a person or an agent without this conversation:

- Identify the defect and the bounded scenario being tested.
- State setup prerequisites, browser/platform, relevant assistive technology,
  initial state, and exact numbered interaction steps. Include how to move
  keyboard focus into the preview.
- State expected versus actual behavior with concrete observations: active
  element, popup visibility, accessible name, role, or ID-reference target.
  Define a clear pass/fail condition rather than "check accessibility."
- Identify the runtime and baseline/fixed revisions. Keep commit hashes in a
  separate evidence comment or artifact, never in the PR description. Explain
  which revision each link actually executes. A playground using deployed code
  is a bug repro, not proof that an unmerged PR works; deployments may change over time.
- Provide a way to exercise the same scenario against the fix: a verified
  PR-preview playground when available, otherwise the in-repository fixture
  or story, its path/story ID, working directory, exact repository-supported
  setup and run commands, and local URL. Identify the targeted regression-test
  command and assertions when available; a unit test alone is not a manual
  interaction recipe. Do not invent commands, preview URLs, or test results.
- Record commands actually run, observations, verification date and revisions,
  and remaining limits. Distinguish browser/DOM/accessibility-tree evidence
  from actual screen-reader speech; do not claim one proves the other.

Before publishing, open the exact serialized link in a fresh page or reload
it, confirm the submitted code and CSS load without runtime errors, and
exercise the stated steps. Where feasible, run the same scenario on the
baseline and fixed revisions and record failure before and success after.
Do not claim a fixed result from a deployed baseline or an in-memory
simulation. If either side cannot be executed, label it unverified and give
the exact remaining check. Preserve the runnable fixture in the PR or
another durable, permitted location; do not rely on session-only files or
an agent's retained context.

If a playground cannot faithfully run the example, provide a runnable
repository story/fixture and the same recipe instead, explaining the
limitation. A generated but untested link, placeholder, or inaccessible
preview does not satisfy the reproduction requirement; report the blocker.
Keep coverage claims bounded: a simple Tab-out repro does not establish
cross-origin, shadow-root, controlled-state, or screen-reader correctness.

Agents following the recipe must use the owning authorized task workspace,
not a protected primary checkout, and follow repository setup instructions.
The recipe grants no permission to edit source, publish comments, change PR
state, or install tools outside existing permissions. Request missing
permissions or manual assistive-technology input rather than substituting
an unverified success claim.

Preserve the live PR template, unrelated description text, attachments, and
draft/ready state when adding evidence. Re-read before editing to avoid
overwriting concurrent changes, then verify the saved links and recipe.
Publishing or updating a PR still requires authorization; this convention
alone does not grant it. Recheck the recipe and fixed revision after relevant
PR changes. Keep screenshots conditional on meaningful reviewer value,
as described below.

### Repository-Specific Accessibility PR Evidence

Where the local repository policy calls for paired evidence, supply **Before**
and **After** screenshots
only when they are needed and add meaningful evidence for reviewers. Do not
require screenshots for every accessibility PR, including drafts. When useful,
attach clearly labelled images in the PR description and capture the same
scenario, viewport, theme, browser/platform, and interaction state so the pair
demonstrates the defect and its correction.
Record reproduction steps and the baseline and fixed revisions, keeping commit
hashes in separate evidence rather than the PR description. If a
comparison disables the fix in memory rather than running the baseline,
label that method explicitly and do not claim it reproduces an untested
platform-specific issue.

For semantic or screen-reader fixes with no visible UI change, prefer
DOM/accessibility-tree assertions, keyboard steps, or actual screen-reader
output as appropriate. Include screenshots of accessible names, ownership,
or focus state only when they add value beyond that evidence. Do not attach
identical UI-only captures or screenshots that merely repeat assertions.
Screenshots alone do not prove spoken output or accessibility conformance.

When screenshots are needed, local-only captures and placeholders do not
satisfy the evidence requirement. Verify uploaded images render for PR readers
and remain linked after description updates; report capture/upload blockers.
When screenshots add no value, state that they are not applicable rather than
blocking readiness on their absence. Apply this to existing open a11y PRs as
well as new ones, without changing their draft state automatically.
This is my personal workflow gate, not a shared repository or branch policy.

### Workspace Retention

At task completion, identify whether the workspace should be retained or
proposed for cleanup. Check its owning session and ongoing PR work, active
agents or processes, uncommitted and untracked files, and unpushed commits.
Do not infer that work is safely preserved solely because the tree is clean
or the PR is merged.

Retain the workspace while work is active or its contents are not confirmed
preserved. If ownership or preservation cannot be established, report the
uncertainty and retain it.

For a cleanup candidate, present the exact session, repository, branch, and
worktree path, together with the evidence that it is no longer needed.
Obtain explicit approval for each deletion under `conventions/git-safety.md`.
App archiving that removes a worktree is also a deletion for this purpose.
Use the owning app's supported lifecycle operation for app-managed workspaces.
Do not automatically delete branches, prune worktrees, or remove directories.

## Consumers

- Local Copilot instructions
- start-task
- Agent delegation and task completion
