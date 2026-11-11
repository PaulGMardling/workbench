# Local overlay recovery

The Git repository backs up portable guidance, not the whole workstation.
Maintain a private recovery inventory in an authorised backup location:
repository configuration; account-routing guidance; required private setup and
evidence overlays; optional browser/debugging helpers; and agent-host pointers.
Record each item's owner, backup location, sensitivity, restore prerequisites
and verification date. Never put credentials or the private inventory here.

On a new machine, clone the portable workbench, restore approved local files
without overwriting newer ones, and reconcile paths and declared overlays.
Use [the configuration contract](../config/schema.md) and read-only doctor.
Missing required files block dependent operations; optional helpers can remain
unavailable with an explicit limit. Do not discover private configuration by
searching unrelated users' directories or copying another worktree's state.

Verify account routing and repository setup separately in an authorised task
context; file existence is not authentication or working dependencies.
Finally test host loading and a resumed task with the restored guidance.
Restoration never authorises credential changes, installs, publication,
scheduler activation or deletion of old data.
