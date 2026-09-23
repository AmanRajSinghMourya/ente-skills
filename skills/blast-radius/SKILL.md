---
name: blast-radius
description: Before building or approving an Ente change, find what else it could break beyond the diff, and prove the one fact it's safe because of by running code. Use for new or changed behavior, contributors' PRs, or "what could this break".
---

# Blast radius

Listing callers isn't the job; grep does that. Find the breakage grep won't
show.

1. **What it does,** including what the diff doesn't spell out: changed
   defaults, ordering, timing and error paths.
2. **The one fact it's safe because of.** Most risky-looking changes are safe
   because of one fact, like "this only runs for new uploads" or "old clients
   ignore this field". Find it and prove it as far as is cheap. Each level is
   stronger than the last:
   1. point at the line
   2. walk through the failing case step by step
   3. run a test or script against the real code
   4. reproduce it in the app

   Say which level you reached.
3. **Look where grep stops in Ente:**
   - shared packages used by more than one app (`mobile/packages/*` across
     Photos, Auth and Locker)
   - old app versions still talking to the server, the API shape, and museum's
     validation
   - the local SQLite schema and migrations, and data already on users' devices
   - encryption and serialization formats (keys, nonces, file metadata)
   - background isolates, sync and upload queues, app lock
   - platform differences (iOS, Android, desktop, web) and feature flags
4. **Report** the risks you confirmed (how it breaks, `file:line`, how likely,
   how bad, how to check) and what you checked and cleared. End with the
   cheapest test that would catch the real risk.
