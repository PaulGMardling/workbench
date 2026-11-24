# Opt-in scheduler and agent-host compatibility

Status: integration design and acceptance checklist, **not an installed or
verified adapter**. This applies to TEG or another selected host without copying
its private implementation or assuming a specific version.

Before activation, record the installed host version and current documented
configuration/prompt contracts in authorised local storage. Do not reuse stale
configuration recipes: unknown settings may be ignored, a brief may load
fail-open, and publication flags may constrain only the controller, not agents.
An independent review role is not necessarily a read-only tool boundary.

## Thin local adapter

Through the host's supported personal/original-root instruction mechanism,
provide a small pointer with the actual authorised workbench location:

```text
For each assignment and resumed task, read <absolute-workbench-root>/workflows/agent-entry.md
and the required stage-specific references and declared local overlays.
Record the loaded revision and relevant file hashes in the private task handoff.
If required guidance cannot be read, block dependent work; do not use cached rules.
Pass the same guidance and authority boundaries to engineers and reviewers.
```

Replace placeholders locally. Do not commit machine paths or private adapter
contents to shared repositories. Reading this template does not configure the
host. Keep one canonical set of detailed rules in workbench rather than copying
it into every prompt.

Apply the [delivery default](../workflows/finish-task.md) only to authorised
implementation assignments, including their explicit opt-outs and host limits.
Automatic commit/push is not permission for reviewers to publish or for a
controller to commit unrelated leftovers. If a host requires a conflicting
predetermined branch, exceeds that delivery scope, or cleans up without the
required per-operation approval, reconcile the conflict before use.
Do not weaken workbench gates silently. Where available,
use supported disabled controller effects and scoped credentials/execution
permissions; a prompt or `push = false` alone is not enforcement.
If the host cannot honour a required boundary, mark it incompatible and keep
that assignment interactive or on another authorised host. Do not patch the
host or invent settings as part of workbench setup.

## Bounded acceptance pilot

Use a separately authorised disposable target with synthetic tasks. No production
schedule, live publication, cleanup or fixture is authorised by this checklist.

| Case | Required observation |
| --- | --- |
| New task | Owner reads entry and routed guidance; records actual revision/hashes before dependent work |
| Review | Primary and independent reviewer receive full scope and current rules; neither edits or publishes without authority |
| Implementation delivery | Validated task changes are committed/pushed and existing PR metadata is current; no PR is created without a request |
| Delivery opt-out | "Do not commit/push" is retained across delegation/resume; denied steps remain unperformed |
| Missing entry/overlay | Assignment blocks explicitly rather than silently continuing |
| Resume | Changed guidance/overlay is detected and affected decisions revalidated |
| Scheduled request | Same routing and authority apply; ambiguous decisions become a blocked result, not guessed permission |
| Publication/cleanup denied | Both controller and agent effects remain within the actual enforced boundary |
| Workbench update | Operator deliberately selects the update; active tasks retain receipts and reconcile changes safely |

Record commands, receipts, results and limits privately. A supplied prompt or
successful launch proves neither loading nor behavioural compliance. Do not
claim compatibility until the relevant cases were observed against the installed
version. Refresh the assessment after host, adapter or material guidance changes.
