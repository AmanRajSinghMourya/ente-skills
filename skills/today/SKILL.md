---
name: today
description: Show what needs Aman's attention in Ente right now. Covers his open PRs with CI and review state, TODO tasks in progress, and worktrees ready for cleanup. Read-only. Use for /today, "what's pending" or "what needs me".
---

# Today

Read-only. Change nothing.

1. **PRs.** For `ente-io/ente` and `AmanRajSinghMourya/ente`:
   `gh pr list --author @me --repo <repo> --json
   number,title,url,reviewDecision,statusCheckRollup`. For each PR, get the CI
   state (pass, fail or pending), the review decision, and the unresolved thread
   count using the `reviewThreads` query from the `pr-feedback` skill.
2. **TODO.** Lines under **In progress**, and how many are under **Up next**.
   The list is `todo/TODO.md` in this skills repository.
3. **Worktrees.** `git worktree list` in the main Ente checkout. For each
   `aman/*` branch, look up its PR state. Merged or closed means it's ready for
   `/cleanup`.
4. **Reply** in three short groups:
   - Needs you now: red CI, changes requested, unanswered comments.
   - In progress.
   - Ready for cleanup.
