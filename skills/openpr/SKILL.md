---
name: openpr
description: Commit an Ente task and open its PR on Aman's fork. Typing /openpr is the approval. Runs the final checks, adds the changes entry, gets a cross-model review, then commits, pushes, runs gh pr create, reports a summary, drafts the Notion update and waits for the Codex bot's review. With "upstream", check conflicts against current ente/ente main and open a separate upstream PR once the fork PR has the Codex bot's thumbs-up; typing it is the approval. Use only when Aman types /openpr or asks to open the PR.
disable-model-invocation: true
---

# Open the PR

Aman's flow has two steps. `/openpr` opens the PR on his fork
`AmanRajSinghMourya/ente`. Once the Codex review bot gives that PR a 👍,
`/openpr upstream` opens a separate PR from that reviewed fork branch targeting
`ente/ente:main`. Keep the fork review PR intact; never
retarget it as the upstream step. After the upstream PR merges, `/cleanup`
closes the fork PR.

The Git and PR rules are in `~/.codex/AGENTS.md`, in the sections "Ente Push and
PR Publishing", "Ente-only rules" and "GitHub PR Conventions". Read them now.
They win over this file. As Claude, skip the lines that only apply inside the
Codex app (confetti, network escalation). If that file is missing on this Mac,
stop and tell Aman.

Do all GitHub work with the `gh` CLI. Never use Codex's `yeet` skill or the
GitHub plugin/connector. They're slower, and AGENTS.md forbids them for PRs.

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
   equivalent, so skip this step there.
4. **Checks: format, lint and tests, only for what the diff touches.** Take
   the commands from the matching `.github/workflows/*` job, but run them on
   the changed packages, not the whole tree. CI runs the full suite on the PR.
   - Mobile: `dart format` on the changed Dart files, `flutter analyze` in each
     changed app or package, and `flutter test` for the tests that cover the
     change. Run `cargo clippy` only when `rust/` changed.
   - Web: `node scripts/lint.mjs` and the changed package's tests.
   - Server: `gofmt -l` and `go vet` on the changed packages, then
     `./scripts/test-with-postgres.sh host -run '<the change's tests>'`.
   - Skip builds, `staticcheck`, `govulncheck` and `npm audit`; CI runs them.
5. **Review.** Run the `challenge` skill, passing the task's new files from step 1
   as `--new-files`. Check each finding against the source,
   fix the confirmed ones within the task, and rerun the affected checks. Do at
   most one re-review, then list what's still open.
6. **No approval step.** Aman typing `/openpr` is his OK to commit, push and
   open the PR on his fork, so don't wait for another yes. It never covers
   `ente/ente`: a PR there happens only through `/openpr upstream` or when
   Aman tells you to. Stop and ask only if:
   files are staged that aren't part of this task, the review left an open
   finding that needs his call, or the fork can't be synced.

   **PR description.** Every PR gets a short body: one to three one-line
   bullets explaining the problem and resulting behavior. Fold relevant choices
   from `DECISIONS.md`, the chat and the linked Notion item into those bullets;
   add a brief trade-off or deliberate omission only when a reviewer needs it.
   No long paragraphs, empty sections or routine check lists. Don't ask merely
   because the PR has a body. Use the same description for `/openpr upstream`.

   For a visual change, use `pr-assets` for relevant screenshots: publish them
   on a separate asset branch in the public fork and add its commit-pinned
   Before/After table. Save the completed body outside the repo and pass it to
   `gh pr create --body-file <file>`; PRs are still opened with `gh`.
7. **Publish.** First bring the fork's `main` up to date, so the fork PR shows
   only this task's commits: `gh repo sync AmanRajSinghMourya/ente --branch
   main`. It only fast-forwards; never add `--force`. Then check that
   `gh api repos/AmanRajSinghMourya/ente/branches/main --jq .commit.sha` equals
   the same for `ente/ente`. If the sync fails because the histories diverged,
   stop and tell Aman. Aman has approved this sync; it needs no extra question.
   Check the repo-local commit identity per AGENTS.md. If anything
   is already staged that isn't part of the agreed groups, stop and ask. Stage
   each group by explicit path and commit it; never use `git add -A`,
   `git commit -a` or `git stash`. Push to the remote that matches the target, and run
   `gh pr create` (ready, not draft). Confirm head and base with `gh pr view`.
8. **Summary.** Give Aman the PR link and one short message: what changed,
   what the review found and what you fixed, the checks you ran and what's
   untested, the commits, the PR title and target, and the changes-entry
   wording. He can still ask for changes; push them to the same branch.
9. **Notion draft.** In the same message, show the update for the task's
   Notion item: the PR link under a `## Pull requests` heading in the page body
   (not `Notes`, which is the team's), and the `Dev` status (a fork PR is "in
   review", not done). Write it after Aman's OK. No item or no Notion tools:
   say so.
10. **Wait for the Codex bot** on the fork PR, as in the `pr-feedback` skill.
    Its review goes straight into `pr-feedback`; don't wait for Aman to ask.

## `/openpr upstream`

1. **Find the fork PR** for this branch: `gh pr list --repo
   AmanRajSinghMourya/ente --head <branch> --json number,url,title,body,headRefOid`.
2. **Check the 👍.** It's a `+1` reaction from `chatgpt-codex-connector[bot]`:
   `gh api repos/AmanRajSinghMourya/ente/issues/<n>/reactions`. It must be newer
   than the PR's last commit (`gh pr view <n> --repo AmanRajSinghMourya/ente
   --json commits --jq '.commits[-1].committedDate'`). If it's missing or older,
   stop and tell Aman. Open review comments go through `/pr-feedback` first.
3. The local branch head must equal the fork PR's `headRefOid`. Otherwise stop.
4. **Check current upstream.** Fetch `main` from the verified `ente/ente` remote,
   or from `https://github.com/ente/ente.git` if no such remote exists. Use the
   fetched commit SHA, not the fork's `origin/main`.
   Run `git merge-tree --write-tree <upstream-main-sha> HEAD`. Exit 0 means no
   Git conflicts, 1 means conflicts, and any other exit means the check failed.
   This checks the merge without changing the index or worktree. Inspect the
   PR diff with `git diff <upstream-main-sha>...HEAD` for unrelated changes.

   If this task adds server migrations, compare their numeric versions in
   `server/migrations/` with current upstream `main` and the migration files
   added by other open `ente/ente` PRs. List them with `gh pr list --repo
   ente/ente --state open --limit 100 --json number,files,changedFiles`; inspect
   only `server/migrations/` paths. If the listing hits the limit or a PR's
   file count exceeds its returned files, paginate the affected API results
   before claiming the check is complete. Different filenames with the same
   version can merge cleanly but collide when migrations run; an up/down pair
   is one migration. Stop publication on a collision, Git conflict or failed
   check and report the files or PRs involved.
   A pending PR's version isn't reserved; recheck before merge if main or the
   competing PR changes. Resolve conflicts only within the authorized scope,
   rerun affected checks and get a fresh fork review for any new head, then
   restart this upstream sequence at step 1. Never rebase or force-push the
   published review branch to pass this gate.
5. **No question.** Aman typing `/openpr upstream` is the OK. The target is
   `ente/ente`, base `main`, head repository `AmanRajSinghMourya/ente`, the
   fork branch, and the same title and body as the fork PR. It changes the
   PR's target, not the source repository; it needs no push access to
   `ente/ente`.
6. **Publish a new upstream PR.** The reviewed head is already on the fork.
   Run `gh pr create --repo ente/ente --head AmanRajSinghMourya:<branch>
   --base main --title <title> --body-file <file>` (ready, not draft). Use the
   same short description and asset tables as the fork PR.
7. **Verify the result.** Read `gh api repos/ente/ente/pulls/<number>` and check
   `base.repo.full_name == ente/ente`, `base.ref == main`,
   `head.repo.full_name == AmanRajSinghMourya/ente`, the branch name and the
   reviewed head SHA.
   Leave the fork PR open; `/cleanup` closes it once `ente/ente` merges.
8. **Wait for the Codex bot** on the `ente/ente` PR, as in the `pr-feedback`
   skill. Human reviews come later; Aman runs `/pr-feedback` for those.
