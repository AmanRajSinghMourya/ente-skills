---
name: cleanup
description: Dispose of a finished Ente task. Close its leftover fork PR once the ente/ente PR is merged or closed, then delete its worktree (including uncommitted files) and local branch. "merged" does this for every fork PR whose ente/ente PR merged; "disk" frees simulator and build space. Use only when Aman types /cleanup or names a task to clean up.
disable-model-invocation: true
---

# Cleanup

Aman's flow: PR on the fork `AmanRajSinghMourya/ente` first; after the Codex
bot's 👍, the same branch on `ente/ente`. When the `ente/ente` PR merges, the
fork PR is closed here.

## One task: `/cleanup <task, branch or fork PR>`

1. **Name the exact target:** the branch, and its worktree path and TODO line if
   they exist on this Mac. Only that task. Never the main checkout, another
   task's worktree or any remote branch. If there's no local worktree or
   branch, only the PR steps apply.
2. **Find both PRs for the branch.** The upstream PR pushes the same `aman/…`
   branch to `ente/ente`, and the fork PR uses it on `AmanRajSinghMourya/ente`.
   (`ente-io/ente` redirects to `ente/ente`; use `ente/ente`.)
   ```sh
   gh pr list --repo ente/ente --head <branch> --state all --json number,state,url,headRefOid
   gh pr list --repo AmanRajSinghMourya/ente --head <branch> --state all --json number,state,url,headRefOid
   ```
3. **Decide:**
   - Upstream PR open: stop and tell Aman.
   - Upstream PR merged or closed: go ahead.
   - No upstream PR: go ahead if the fork PR is merged or closed. Stop if it's
     still open. With no PR anywhere, ask Aman to confirm the disposal.
4. **Close the fork PR** if it's still open: `gh pr close <n> --repo
   AmanRajSinghMourya/ente --comment "Merged upstream in <upstream PR url>"`,
   or "Closed upstream in …" when the upstream PR was closed without merging.
   Don't delete its branch.
5. **Commits that never reached a PR:** `git -C <worktree> log --oneline
   <headRefOid of the latest PR>..<branch>`. If any print, show them and ask;
   deleting the branch loses them.
6. **Remove,** from the main checkout. If this chat is inside the worktree,
   leave it first (in Claude Code, `ExitWorktree` with `keep`). Then
   `git worktree remove --force <path>`, `git branch -D <branch>`,
   `git worktree prune`. `--force` deletes uncommitted, unstaged and untracked
   files in that worktree; Aman wants them gone, not preserved. List what was
   discarded (`git -C <worktree> status --short` before removing).
7. Tick the TODO line, move it to **Done**, and tell Aman what was removed, which
   PR was closed, and which files were discarded.

## Everything merged: `/cleanup merged`

List every open fork PR whose `ente/ente` PR is merged, with the local worktree
and branch for each if they exist on this Mac. Ask once, then run steps 4 to 7
for each.

## Disk: `/cleanup disk`

Report first. Delete only what Aman picks.

- `df -h /` before and after.
- Simulators: `xcrun simctl list devices unavailable`, then
  `xcrun simctl delete unavailable`. Old runtimes: `xcrun simctl runtime list`.
- Xcode: `~/Library/Developer/Xcode/DerivedData` and
  `~/Library/Developer/Xcode/iOS DeviceSupport`.
- `build/` and `.dart_tool/` inside worktrees whose PR is merged or closed.

Show sizes with `du -sh`, then delete the chosen items. Never touch the simulator
Aman is using or anything in the main checkout.
