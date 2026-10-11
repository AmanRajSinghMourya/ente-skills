---
name: today
description: Show what needs Aman's attention in Ente right now. Covers fork and upstream PRs (CI, review comments, which fork PRs are ready for ente/ente, which to close), and worktrees ready for cleanup. Read-only. Use for /today, "what's pending" or "what needs me".
---

# Today

Read-only. Change nothing.

Aman opens each PR on his fork `AmanRajSinghMourya/ente` first, then opens the
same branch on `ente/ente` after the Codex review bot approves the fork PR.
Always use `ente/ente`; through the old `ente-io/ente` name, `--author @me`
returns nothing.

1. **Fork PRs:** `gh pr list --repo AmanRajSinghMourya/ente --state open --json
   number,title,url,headRefName,statusCheckRollup`. For each one:
   - its `ente/ente` PR: `gh pr list --repo ente/ente --head <headRefName>
     --state all --json number,state,url`
   - the Codex bot's verdict on the head commit: `wait_review.sh
     AmanRajSinghMourya/ente <n> 1` from the `pr-feedback` skill
   - unresolved review threads, using the `reviewThreads` query from the
     `pr-feedback` skill
2. **Upstream PRs:** `gh pr list --repo ente/ente --author @me --json
   number,title,url,reviewDecision,statusCheckRollup`, with the same thread
   count.
3. **Tasks:** Aman's assigned Notion items come from the `signals` run in step 6.
4. **Worktrees:** `git worktree list` in the main Ente checkout, matched to the
   PRs above.
5. **Reply** in short groups, skipping empty ones:
   - Needs you now: red CI, changes requested, unresolved comments
     (`/pr-feedback`).
   - Ready for ente/ente: fork PRs the bot approved and no `ente/ente` PR
     (`/openpr upstream`).
   - Waiting on ente/ente review.
   - Merged upstream, fork PR still open, or worktree left over (`/cleanup`).
6. **Signals:** run the `signals` skill for the last 24 hours and add its theme
   summary at the end. Skip it if Aman asked for PRs only.
