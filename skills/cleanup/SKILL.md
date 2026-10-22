---
name: cleanup
description: >-
  Dispose of finished Ente tasks: every one by default, or the one Aman names.
  Close each leftover fork PR once the ente/ente PR is merged or closed, then
  delete its worktree (including uncommitted files), local branch and local
  screenshots, and draft the Notion and Discord updates. "disk" frees simulator
  and build space. Also release idle task resources. Use only when Aman types
  /cleanup or names a task to clean up.
disable-model-invocation: true
---

# Cleanup

Aman's flow: PR on the fork `AmanRajSinghMourya/ente` first; after the Codex
bot's 👍, the same branch on `ente/ente`. When the `ente/ente` PR merges, the
fork PR is closed here.

## `/cleanup`: every finished task

Typing it is the OK; ask nothing. Take every `aman/…` branch that has a
worktree in `git worktree list` on this Mac or an open PR on
`AmanRajSinghMourya/ente`. Run the steps below for each one that step 3
clears. List the others with the reason, such as "upstream PR still open",
"no PR anywhere" or "commits that never reached a PR" (step 5); don't ask
about them here. End with one combined report and
set of drafts.

`/cleanup <task, branch or fork PR>` does the same for that one task only.

## Steps for one task

1. **Name the exact target:** the branch, and its worktree path if it exists on
   this Mac. Only that task. Never the main checkout, another
   task's worktree or any remote branch except its `pr-assets` branch
   (step 7). If there's no local worktree or
   branch, only the PR steps apply.
2. **Find both PRs for the branch.** Both use the same reviewed `aman/…` branch
   on `AmanRajSinghMourya/ente`; their targets are `ente/ente:main` and the fork.
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
   Don't delete its remote branch.
5. **Commits that never reached a PR:** `git -C <worktree> log --oneline
   <headRefOid of the latest PR>..<branch>`. If any print, show them and ask;
   deleting the branch loses them.
6. **Remove the worktree and local branch. Always finish this step; never hand Aman a command.**
   He has approved removing it whatever it holds: uncommitted or untracked
   files, submodules, a lock.
   - **In Codex, for a worktree under `~/.codex/worktrees/`:** Codex's app
     rules forbid shell deletion there, so use its own mechanisms:
     - Attached to this chat as a worktree: `archive_worktree`.
     - It's a chat's own folder (worktree mode; the chat's attachments show
       only PRs): archive **that chat** with `set_thread_archived`. Codex
       then deletes the chat's worktree itself, unless the chat is pinned
       (unpin it first with `set_thread_pinned`) or another active chat
       still works in that folder. If it's this chat, do steps 7 and 8
       first, then archive this chat and finish local branch deletion below.
       Otherwise find it with
       `list_threads`/`read_thread`, matching its folder to the path.
   - **In Claude Code, or a worktree under `.worktrees/`:** remove it from
     the main checkout. If this chat is inside it, leave it first
     (`ExitWorktree` with `keep`).
     ```sh
     git worktree remove -f -f <path>
     [ -e <path> ] && rm -rf <path>
     git worktree prune
     ```
     `-f -f` also removes worktrees with submodules or a lock.

   **After either removal path, delete the local task branch from the main
   checkout.** Record the branch before archiving. For Codex, wait for archival
   to complete. Confirm the worktree folder is gone and its path is absent from
   `git -C <main-checkout> worktree list --porcelain`. If removal is blocked,
   report it and leave the branch intact. If the local branch still exists, run
   `git -C <main-checkout> branch -D <branch>` and verify that
   `git -C <main-checkout> show-ref --verify refs/heads/<branch>` no longer finds
   it. Skip branch deletion for a detached HEAD with no local task branch.
   Keep remote task branches and remote-tracking refs unchanged.

   `--force` deletes uncommitted, unstaged and untracked files in that
   worktree; Aman wants them gone, not preserved. List what was discarded
   (`git -C <worktree> status --short` before removing).
7. **Screenshots.** `trash ~/.cache/ente-pr-assets/<slug>` (see `pr-assets`;
   the slug is the branch without `aman/`). If no PR merged, also
   delete the fork's asset branch: `gh api -X DELETE
   repos/AmanRajSinghMourya/ente/git/refs/heads/pr-assets/<slug>`. After a
   merge, keep it: the merged PR's images point at its commit.
8. **Report and drafts, in one message.** What was removed, which PR was
   closed, and which files were discarded. Then, if the `ente/ente` PR merged,
   drafts Aman can paste or tell you to post:
   - **Notion:** the task's item in its app's "Roadmap Items" (found with
     Notion search, by the PR URL and then the title), linked. The draft adds
     the upstream PR link under the page body's `## Pull requests` heading
     (not `Notes`, which is the team's) and sets `Dev` to `Done`.
   - **Discord:** a short message for the task's thread or channel: what
     shipped, in plain words, with the PR link, and which release it lands in
     (the next one cut from `main`).

   Post nothing until he says so. No Notion item or no Notion tools: say so.

## Disk: `/cleanup disk`

Report first. Delete only what Aman picks.

- `df -h /` before and after.
- Simulators: `xcrun simctl list devices unavailable`, then
  `xcrun simctl delete unavailable`. Old runtimes: `xcrun simctl runtime list`.
- Xcode: `~/Library/Developer/Xcode/DerivedData` and
  `~/Library/Developer/Xcode/iOS DeviceSupport`.
- `build/` and `.dart_tool/` inside worktrees whose PR is merged or closed.
- Rust `target/` directories, Cargo registry and Git crate caches, and rustup
  temporary downloads. Discover configured or shared target directories too.
  Preserve Cargo binaries, installed toolchains, source, and lockfiles.

Before deleting repository outputs, verify each path is ignored and contains
no tracked files or submodule source. Recheck active builds and open handles
before deleting outputs or shared caches. Skip anything in use or uncertain.
For Codex storage, distinguish generated worktree outputs from source, chat
history, app databases, and installed plugins. Do not delete those to free space.

Show sizes with `du -sh`, then delete the chosen items. Never touch the simulator
Aman is using or anything in the main checkout.

## Release idle resources

After task or disk cleanup, inspect process command lines, parents, working
directories, open handles, and memory use. Recheck each process immediately
before stopping it. A large RSS, an old process, or a `.snapshot` name alone
does not prove that a process is disposable.

- Stop idle Gradle or Kotlin build daemons only after confirming that no build,
  test, or install uses them. Prefer the matching Gradle stop command.
- Stop orphaned Dart analysis or frontend servers only when their owning task
  has ended and no editor, Flutter run, test, or MCP client uses them. Then clear
  `~/.dartServer/.analysis-driver` if no remaining process uses that cache.
- For manual cleanup, gracefully stop Android test emulators with
  `adb -s <emulator-serial> emu kill` after confirming that no active build,
  test, install, or Flutter session uses them. Preserve AVD definitions and data
  unless their deletion is separately authorized. Never stop a physical device.
- Prefer graceful shutdown or `SIGTERM` for an exact verified PID. Do not use
  blanket `pkill java`, `pkill dart`, or forced termination. Preserve active
  sessions, MCP servers, Codex, Claude, VMs, and unrelated services.

Report which processes stopped and their observed memory use. Do not equate
their summed RSS with measured free RAM. Leave macOS memory management alone.
These manual cleanup rules do not change the nightly automation, which still
preserves running emulators and active processes.
