# Compact task handoff

Use the host's existing task artifact or private session storage, not another
tracking service or a committed task log. Omit inapplicable fields explicitly.
Keep sensitive configuration, identity and evidence in authorised storage.

```text
Task/request locator; stage; original scope and exclusions:
Coordinator/owning session; repository; verified workspace:
Source/runtime revision; dirty state and work to preserve:
Actual local branch; configured publishing remote/branch (if applicable):
Workbench root/revision; guidance actually read; relevant dirty state:
Selected personal profile/overlays; fingerprints only where resumption needs them:
Available vs authorised tools; explicit approvals and trusted locators:
Actual delivery authority and opt-outs; host restrictions; owning publisher:
Assigned owners/files; dependencies; independent reviewer handle:
Acceptance checks; exact executed commands/results; evidence locators:
Confirmed findings; unresolved leads; decisions needed:
Publication state; observed remote revision; verified PR identity/metadata state:
Retention decision; preservation uncertainty; cleanup approval if any:
Next action and bounded stop condition:
```

For trivial work, a few fields in the session are enough. Keep the receipt and
remaining decisions, not a repeated narrative of every tool call. Update
existing records rather than creating duplicate handoffs on each turn.
