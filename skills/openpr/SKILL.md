---
name: openpr
description: Commit an Ente task and open its PR after one approval from Aman. Runs the final checks, adds the changes entry, gets a cross-model review, then commits, pushes and runs gh pr create. Use only when Aman types /openpr or asks to open the PR.
disable-model-invocation: true
---

# Open the PR

The Git and PR rules are in `~/.codex/AGENTS.md`, in the sections "Ente Push and
PR Publishing", "Ente-only rules" and "GitHub PR Conventions". Read them now.
They win over this file. As Claude, skip the lines that only apply inside the
Codex app (confetti, network escalation). If that file is missing on this Mac,
stop and tell Aman.

1. **Scope.** In the task worktree, check `git status` and the diff against
   `origin/main`. Only this task's changes go in. Never restage or edit files
   Aman staged.
2. **Changes entry.** For a user-facing change in an app with a `changes/`
   folder (for example `mobile/apps/photos/changes/`; read its README), add
   `<slug>.md` with one past-tense bullet like the existing files. Skip it for
   internal-only work such as refactors, tests or CI.
3. **Checks.** Run the lints and tests from the matching `.github/workflows/*`
   job on the final content. For the server, use
   `./scripts/test-with-postgres.sh host`.
4. **Review.** Run the `challenge` skill. Check each finding against the source,
   fix the confirmed ones within the task, and rerun the affected checks. Do at
   most one re-review, then list what's still open.
5. **Ask once.** One message with:
   - what changed, in plain words
   - what the review found and what you did about it
   - the checks you ran, their results, and what's untested
   - commit groups with messages, tests beside the code they cover
   - the PR title (prefix from the touched paths, per AGENTS.md), head
     repo/branch, base, target repo (the fork `AmanRajSinghMourya/ente` unless
     Aman picks `ente-io/ente`), gh account, and body (none unless needed)
   - the changes-entry wording

   Wait for yes. If the content changes afterwards, ask again.
6. **Publish.** Check the repo-local commit identity per AGENTS.md. If anything
   is already staged that isn't part of the agreed groups, stop and ask. Stage
   each group by explicit path and commit it; never use `git add -A`,
   `git commit -a` or `git stash`. Push to the remote that matches the target, and run
   `gh pr create` (ready, not draft). Confirm head and base with `gh pr view`.
   Add the PR link to the task's TODO line and give Aman the link.
7. For a mobile change, ask whether to start the simulator so he can check it
   himself.
