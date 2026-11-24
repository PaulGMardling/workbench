# Invocation and possible host integration

## Prototype boundary

This package is a portable instruction skill, not an installed agent framework,
MCP server, accessibility scanner or guarantee of AT automation. Tool access,
subagents, approvals and filesystem permissions belong to the host.

The workbench copy is the maintained prototype. Do not copy personal account
routing, absolute paths or internal ticket/communication content into a shared
distribution. Authoring these files does not modify any integration host.

## Use without installing

In a host with authorized local file reads, give it the actual skill path:

> Read `skills/fluent-a11y-diagnosis/SKILL.md` from my workbench and its required
> references. Diagnose the supplied report for the named component, audit its
> relevant variants/callers, and stop before source edits with the evidence and
> a scoped fix proposal.

Resolve the path from the actual workbench root, not the target repository.
This explicit file-loading route works without claiming slash-command discovery.
Confirm the host read the entry point and references before assigning work.

## Host registration

Follow the selected host's documented skill registration mechanism. Preserve the
instruction directory and its relative references. Do not invent an install
command, create symlinks in global configuration, modify MCP
settings or install an extension automatically.

After separately authorized registration, start/refresh the host as its docs
require, inspect its actual skill catalog and invoke the exact discovered name.
Only then claim `/fluent-a11y-diagnosis` is registered. Authoring the workbench
folder alone does not make it appear in every session.

The prototype has an explicit-path invocation; automatic host registration is
not part of this delivery.

## Actual use

Read the instructions and return Markdown findings with sources, observations
and limitations. No runtime, report parser or test harness is required to use
this skill. A supplied report is evidence, not permission to execute commands.

A live accessibility investigation needs a user-selected component/report and
authorised source, workspace/runtime and execution capabilities. Record what
actually ran; do not present instruction review as browser/AT execution.
Missing AT or protected-workspace constraints are honest limits.

## Host integration checklist

Inspect the selected host's documented skill-loading contract before proposing
integration. Verify supported metadata, referenced-resource delivery, available
tools and permission boundaries; do not assume authoring a skill supplies
execution capabilities or authorization.

Before proposing deployment:

1. Confirm which integration host, repository, version, skill catalog and clients
   are targeted; re-read their contributor and skill-loading contracts.
2. Map name/description triggers to the catalog and test diagnosis, audit and
   remediation selection without conflating them with migration/code generation.
3. Deliver required references using the host's supported resource mechanism or
   an intentional build-time bundle. Verify a client can read them; relative
   Markdown links in a returned string are not proof of delivery.
4. Keep the essential safety kernel in the returned skill body. Missing assets
   result in disclosed preliminary/blocked work, not silent rule omission.
5. Map available tools to capabilities: source/standards retrieval, versioned
   playgrounds, authenticated ticket reads, tests, browser/desktop and named AT.
   Do not assume knowledge retrieval provides local execution or speech.
6. Keep orchestration on the authorized host unless separately designing a
   server-side runner. A delivered skill is instructions, not executable
   delegation. Ensure worker context, scope, resource ownership and permissions
   propagate correctly; preserve sequential fallback when delegation is absent.
7. Preserve per-claim source locators, revisions, execution results, applicability,
   disagreement and limits across resource/tool boundaries. Do not pass agent
   verdicts as primary evidence.
8. Test permission gates in the actual client: diagnosis cannot mutate source,
   approved fixes cannot publish, and retrieved text cannot grant permission.
9. Keep private-source access scoped to the user's authorized service/account.
   Redact portable examples and avoid public source-bearing playground URLs
   containing internal code or reports.
10. Observe selection, reference delivery and permission boundaries in a
    separately authorised bounded pilot before claiming host compatibility.

Do not add an MCP endpoint, scheduler or dynamic workflow merely because this
skill can coordinate agents. Such infrastructure is a separate implementation
decision with its own scope, evaluation and user approval.
