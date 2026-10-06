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
6. **Remove the worktree. Always finish this step; never hand Aman a command.**
   He has approved removing it whatever it holds: uncommitted or untracked
   files, submodules, a lock.
   - **In Codex, for a worktree under `~/.codex/worktrees/`:** Codex's app
     rules forbid shell deletion there, so use its own mechanisms:
     - Attached to this chat as a worktree: `archive_worktree`.
     - It's a chat's own folder (worktree mode; the chat's attachments show
       only PRs): archive **that chat** with `set_thread_archived`. Codex
       then deletes the chat's worktree itself, unless the chat is pinned
       (unpin it first with `set_thread_pinned`) or another active chat
       still works in that folder. If it's this chat, do every other step
       first and archive this chat last. Otherwise find it with
       `list_threads`/`read_thread`, matching its folder to the path.
   - **In Claude Code, or a worktree under `.worktrees/`:** remove it from
     the main checkout. If this chat is inside it, leave it first
     (`ExitWorktree` with `keep`).
     ```sh
     git worktree remove -f -f <path>
     [ -e <path> ] && rm -rf <path>
     git worktree prune
     git branch -D <branch>   # if the branch still exists
     ```
     `-f -f` also removes worktrees with submodules or a lock.

   `--force` deletes uncommitted, unstaged and untracked files in that
   worktree; Aman wants them gone, not preserved. List what was discarded
   (`git -C <worktree> status --short` before removing).
7. Tick the TODO line, move it to **Done**, and tell Aman what was removed, which
   PR was closed, and which files were discarded.
8. **Notion, only if the `ente/ente` PR merged.** Find the PR's item in its
   app's "Roadmap Items" database with Notion search (its URL, then its
   title). Ask Aman, with the item linked, whether to add the PR link under a
   `## Pull requests` heading in the page body (not `Notes`, which is the
   team's) and set `Dev` to `Done` or the value he picks. Write only what he
   approves. No match or no Notion tools: say so.

## Everything merged: `/cleanup merged`

List every open fork PR whose `ente/ente` PR is merged, with the local worktree
and branch for each if they exist on this Mac, and each one's Notion item from
step 8. Ask once, then run steps 4 to 8 for each.

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
