---
name: openpr
description: Commit an Ente task and open its PR on Aman's fork after one approval. Runs the final checks, adds the changes entry, gets a cross-model review, then commits, pushes and runs gh pr create. With "upstream", open the same PR on ente/ente once the fork PR has the Codex bot's thumbs-up. Use only when Aman types /openpr or asks to open the PR.
disable-model-invocation: true
---

# Open the PR

Aman's flow has two steps. `/openpr` opens the PR on his fork
`AmanRajSinghMourya/ente`. Once the Codex review bot gives that PR a 👍,
`/openpr upstream` opens the same PR on `ente/ente`. After the `ente/ente` PR
merges, `/cleanup` closes the fork PR.

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
3. **Built-in cleanups, in Claude Code only.** Run `/simplify` on the diff
   (simpler code, reuse, no waste; it edits files). For changes to encryption,
   auth, sharing or the server, also run `/security-review`. Codex has no
   equivalent, so skip this step there. Never use Codex's `yeet` skill;
   AGENTS.md forbids it.
4. **Checks.** Run the lints and tests from the matching `.github/workflows/*`
   job on the final content. For the server, use
   `./scripts/test-with-postgres.sh host`.
5. **Review.** Run the `challenge` skill. Check each finding against the source,
   fix the confirmed ones within the task, and rerun the affected checks. Do at
   most one re-review, then list what's still open.
6. **Ask once.** One message with:
   - what changed, in plain words
   - what the review found and what you did about it
   - the checks you ran, their results, and what's untested
   - commit groups with messages, tests beside the code they cover
   - the PR title (prefix from the touched paths, per AGENTS.md), head
     repo/branch, base, target repo (the fork `AmanRajSinghMourya/ente` unless
     Aman picks upstream `ente/ente`, which AGENTS.md calls `ente-io/ente`),
     gh account, and body (none unless needed)
   - the changes-entry wording

   Wait for yes. If the content changes afterwards, ask again.
7. **Publish.** Check the repo-local commit identity per AGENTS.md. If anything
   is already staged that isn't part of the agreed groups, stop and ask. Stage
   each group by explicit path and commit it; never use `git add -A`,
   `git commit -a` or `git stash`. Push to the remote that matches the target, and run
   `gh pr create` (ready, not draft). Confirm head and base with `gh pr view`.
   Add the PR link to the task's TODO line and give Aman the link.
8. For a mobile change, ask whether to start the simulator so he can check it
   himself.

## `/openpr upstream`

1. **Find the fork PR** for this branch: `gh pr list --repo
   AmanRajSinghMourya/ente --head <branch> --json number,url,title,body,headRefOid`.
2. **Check the 👍.** It's a `+1` reaction from `chatgpt-codex-connector[bot]`:
   `gh api repos/AmanRajSinghMourya/ente/issues/<n>/reactions`. It must be newer
   than the PR's last commit (`gh pr view <n> --repo AmanRajSinghMourya/ente
   --json commits --jq '.commits[-1].committedDate'`). If it's missing or older,
   stop and tell Aman. Open review comments go through `/pr-feedback` first.
3. The local branch head must equal the fork PR's `headRefOid`. Otherwise stop.
4. **Ask once:** target `ente/ente`, base `main`, the push remote for
   `ente/ente` (check the push URL per AGENTS.md; `ente-io/ente` redirects to
   it), the branch, and the same title and body as the fork PR.
5. After yes, push the branch to that remote. Then run `gh pr create --repo
   ente/ente --head <branch> --base main` with the same title and body (ready,
   not draft), and confirm with `gh pr view`. Add the upstream link to the TODO
   line. Leave the fork PR open; `/cleanup` closes it once `ente/ente` merges.
