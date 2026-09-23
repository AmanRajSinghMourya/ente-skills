---
name: cleanup
description: Remove one finished Ente task's worktree and local branch, or with "disk" free space from simulators and build caches. Use only when Aman types /cleanup or names a task to clean up.
disable-model-invocation: true
---

# Cleanup

## One task: `/cleanup <task>`

1. **Name the exact target:** the worktree path, its branch and its TODO line.
   Only that task. Never the main checkout, another task's worktree or any
   remote branch.
2. **PR state:** `gh pr view <PR link from the TODO line> --json
   state,headRefOid`. Merged or closed, merged or not: go ahead. Still open:
   stop and tell Aman. No PR at all: tell Aman the task never got a PR and ask
   him to confirm the disposal.
3. **Unsaved work:** `git -C <worktree> status --porcelain`, plus commits that
   never reached the PR: `git -C <worktree> log --oneline <headRefOid>..<branch>`
   (with no PR, `git -C <worktree> log --oneline <branch> --not --remotes`). If
   anything prints, show it and ask. It's gone for good once removed.
4. **Remove,** from the main checkout. If this chat is inside the worktree, leave
   it first (in Claude Code, `ExitWorktree` with `keep`). Then
   `git worktree remove <path>`,
   `git branch -D <branch>`, `git worktree prune`. If `remove` refuses only
   because of ignored build output (`build/`, `.dart_tool/`) and step 3 was
   clean, use `git worktree remove --force <path>`.
5. Tick the TODO line, move it to **Done**, and tell Aman what was removed.

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
