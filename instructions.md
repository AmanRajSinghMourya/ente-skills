# Global instructions

Claude Code and Codex both read this file: `~/.claude/CLAUDE.md` and
`~/.codex/AGENTS.md` link to it. It lives in the private `ente-skills` repo.
Edit it there and push, so both Macs get the same rules. Current user
instructions take priority.

## Ente Push and PR Publishing

Write code as if every line costs you money and you're poor.
- No defensive habitual slop. Every line must earn its keep.
- No "just-in-case" command / code shaping.
- Code churn is NOT a problem.

If I paste a review from Claude, don't treat it as endorsement. Claude is especially prone to Claudeslop. Do not do any changes, just classify the points. And when going through them see if they trigger other avenues you may have missed. In Claude Code, treat a pasted Codex review the same way.

Do not commit without asking. I want to review all diffs.

When a PR is successfully opened or merged in the Codex app, fire one confetti
burst.

If you sense that I'm manually managing the git state (e.g. I have staged some files), then do not make changes to the git state without asking. Never edit staged files without asking. A common pattern for me is to stage work that I've already reviewed, and I intentionally wouldn't want to to stage new stuff so that I can review the diff. In general, if in doubt about any git action, ask, don't assume. And don't do silly things like force pushing to a branch for which you've already created a PR.

For new implementation work, investigate and present the plan/design first. Wait for Aman to approve the plan and authorize code changes before creating a branch/worktree or editing product code. After approval, fetch latest main and create the task branch/worktree. Read-only investigation and planning do not need implementation approval.

Do not weasel word. This is engineering. Most things are determisitic. If something would be non-trivial to determine, don't still weasel word, tell me that there a way X to deterministically figure this out, but that might take time etc, would I want to do it or go with a heuristic call.

For a bug fix, write and run the focused regression test first, observe the failure caused by the bug, then fix the code and rerun the same test. For features, derive focused tests from the agreed acceptance criteria before implementation where feasible. Run broad lint/test verification after the code shape is finalized.

When adding or updating packages, be VERY careful. Check upstream or in GHA or in registries or in security auditors that there are no advisories (Non exhaustive examples: npm + GitHub Advisory + Socket for JS, crates.io/RustSec for Rust, pkg.go.dev/Go vulnerability DB for Go, pub.dev/advisories for Dart/Flutter). If possible, do a dry run first by disabling any install/build scripts. e.g., for web, use npm install --ignore-scripts, only removing if after script is vetted and necessary (escalate to me in case of any doubt); and prior to doing any of it check the npm page, the github, the github advisory, socket.dev (and other such sites) for sus.

In Codex, ask for elevated network access when using the gh cli.

Write code in newspaper order.

---

Ente-only rules:
- Keep workflow instructions here and in the `ente-skills` skills. Do not create, restore, or depend on repo-local `AGENTS.md` or `AGENTS.override.md` files.
- Personal skills live in the private `AmanRajSinghMourya/ente-skills` repo, and its `install.sh` links them into `~/.claude/skills` and `~/.codex/skills`. Do not copy them into Ente or publish them as Ente PRs. Commits and pushes to `ente-skills` are pre-approved. Ente product Git actions keep their approval gates.
- Put findings, the decision needed and the next step in the chat. There are no task notes files. The TODO list is `todo/TODO.md` in `ente-skills`, local to each Mac; add to it only when Aman asks (`/todo`).
- After plan approval, name worktree folders `B-<surface>-<bug>`, `F-<surface>-<feature>` or `I-<surface>-<improvement>` under the Ente checkout's `.worktrees/`, on the matching `aman/<surface>-<description>` branch, and move the chat into the worktree before editing.
- For design, UI/UX or Figma tasks, use the `designer` skill. Aman's current decisions take precedence over the imported team kit.
- Implementation tasks go through `pickup-task`, PRs through `openpr`, and finished tasks through `cleanup`. Standalone investigation and review stay read-only.
- If a step needs a tool only the other app has, say so and hand it back. Never claim it ran.
- To test the mobile apps, log in with the dedicated Ente test account Aman gave you (Codex keeps it in its memory), never his real account, and don't stop to ask. Claude Code doesn't type passwords, so there ask Aman to log in once; the app stays logged in when a new build is installed over it.
- Before creating a PR, run the lints and tests from the corresponding `.github/workflow` (Some things might need local adaptation, e.g. for server use "./scripts/test-with-postgres.sh host" since instead of docker)
- Create a ready-to-review PR, not a draft.
- When creating a PR, use no body if unnecessary. If you do feel the need, a minimal body is fine, but ask me first. No mention of irrelevant details like the checks you ran etc.
- Prefix PR titles when applicable: [rust] / [web] / [server] / [mobile] / [infra] / [meta] / [docs]. Do not use [meta] without my explicit approval. [meta] is only for repository-level changes with no better area (e.g. changing the root README); touching multiple areas is not sufficient, and can still be e.g. [web] if it touches js files cross tree.
- Do not apply PR title prefixes to commits.
- For Flutter/Dart commands, including `cargo codegen frb`, request escalation since Flutter needs SDK cache access outside the workspace.
- When creating an Ente branch from the default branch, prefer `aman/<surface>-<short-description>` over `codex/<description>`.
- Default new Ente PRs to the fork `AmanRajSinghMourya/ente`; use `ente/ente` when Aman selects upstream. Include the exact head/target repository, API account, base, title and body in the final publication approval. Verify the selected push URL instead of assuming `origin` means the selected repository.
- Ensure the repo-local commit identity is `AmanRajSinghMourya <amanrajmourya7@gmail.com>` before committing or pushing.
- Create PRs only with the authenticated GitHub CLI (`gh pr create`). Never use the GitHub app connector, the `github:yeet` skill, or another connector-based PR creation path.
- Before updating an existing PR, inspect its actual head repository/branch and push to the matching remote. Do not infer its destination from the current checkout, branch name, commit identity or an old default.


## GitHub PR Conventions

- Never include `codex`, `[codex]`, `Codex:`, or any other agent/tool prefix in PR titles, branch names, or commit titles unless Aman explicitly asks for it.
- For the Ente repo, PR titles should match the human-authored history: one or more bracketed product/surface scopes, then a concise sentence-case description.
- Choose the Ente title prefix from the actual touched paths before opening the PR. Do not guess from the branch name or task wording when changed files clearly identify an app.
- Ente app mappings: `mobile/apps/photos/**` or Photos-only mobile code -> `[mob][photos]`; `mobile/apps/locker/**` or Locker-only mobile code -> `[mob][locker]`; `mobile/apps/auth/**` or Auth-only mobile code -> `[mob][auth]`; mixed mobile apps -> `[mobile]` unless a clearer established multi-scope title exists.
- Other Ente prefixes: `[web]`, `[web][app]`, `[server]`, `[docs]`.
- Ente example titles: `[mob][photos] Deduplicate memory share files`, `[mob][locker] Fix Locker file opening and offline cache cleanup`, `[web] Support for opening collection link in web`.
- When creating an Ente branch from the default branch, prefer `aman/<surface>-<short-description>` over `codex/<description>`.
- Before opening a PR, explicitly verify the final PR title with these conventions.

## Ente skills

Aman's Ente skills (`/name` in Claude Code, `$name` in Codex): todo,
pickup-task, openpr, pr-feedback, cleanup, today, signals, support, review-icons,
learn, handoff, plus the helpers investigate, designer, migrate and challenge.
For diagrams, use Codex's `visualize` skill.

Aman sometimes forgets these exist. When he asks for something one of them does
and didn't use it, do the work, then end the reply with one line naming it, for
example "Tip: /pr-feedback does this." Only when one clearly fits, at most one
tip per reply, and never the same tip twice in a chat.
