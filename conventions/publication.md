# Publication boundary

Private visibility does not authorise disclosure. Keep secrets, personal paths,
internal source/process material, task records and private overlays outside
the published history. `.gitignore` is a deliberate new-file allowlist, not
protection for already tracked content or a proof of permission.

Before adding a file, inspect its contents and dependencies, choose its exact
allowlist entry and verify the intended path is no longer ignored. Never use
force-add as a workaround. Keep generated reports and local configuration
excluded. Inspect the exact staged snapshot, including filenames, modes,
links and references, after the last staging change and before committing.
Avoid broad staging commands. Recheck account, destination and actual branch
before any publication authorised under the
[delivery default](../workflows/finish-task.md) or a task-specific request.

Run the portable [validation command](../readme.md#validation) in an authorised
execution workspace. Static pattern/link checks catch mistakes, not all secrets,
licensing issues or disclosure restrictions. Review manually as well. If a
leak is discovered, stop publication and follow the owning service's incident
process; ignore rules cannot remove existing history.
