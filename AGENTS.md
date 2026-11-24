# Workbench agent entry

For every new task, review and resumed assignment, read
[agent entry](workflows/agent-entry.md) before choosing the workflow.
This is the routing entry point, not permission to change files or publish.

For authorised implementation, load [delivery](workflows/finish-task.md):
commit, push and refresh an existing open PR by default unless the user opts out.
New PR creation remains opt-in; reviews remain read-only.

Keep personal configuration and internal overlays local. Read
[publication checks](conventions/publication.md) before adding tracked files.
Do not install, activate or alter scheduler integrations merely by reading them.
