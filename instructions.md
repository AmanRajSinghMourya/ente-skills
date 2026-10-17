# Global instructions

Claude Code and Codex both read this file: `~/.claude/CLAUDE.md` and
`~/.codex/AGENTS.md` link to it. It lives in the private `ente-skills` repo.
Edit it there and push, so both Macs get the same rules. Current user
instructions take priority.

## Ente Push and PR Publishing

Write code as if every line costs you money and you're poor.
- Code churn is NOT a problem.

If I paste a review from Claude, don't treat it as endorsement. Claude is especially prone to Claudeslop. Do not do any changes, just classify the points. And when going through them see if they trigger other avenues you may have missed. In Claude Code, treat a pasted Codex review the same way.

Do not commit without asking. I want to review all diffs. Typing `/openpr` is that ask: it commits, pushes and opens the fork PR without another approval.

When a PR is successfully opened or merged in the Codex app, fire one confetti
burst.

If you sense that I'm manually managing the git state (e.g. I have staged some files), then do not make changes to the git state without asking. Never edit staged files without asking. A common pattern for me is to stage work that I've already reviewed, and I intentionally wouldn't want to to stage new stuff so that I can review the diff. In general, if in doubt about any git action, ask, don't assume. And don't do silly things like force pushing to a branch for which you've already created a PR.

For new implementation work, use `investigate` to establish the existing behavior and context. Present a proportional plan: the intended observable result, the existing path, the smallest change needed, and how you will verify it. Include behavior that must remain unchanged and trade-offs Aman has accepted. Justify each new mechanism by naming the requirement the existing path cannot satisfy; otherwise leave it out. Wait for implementation approval before creating a branch/worktree or editing product code. After approval, fetch latest main and create the task branch/worktree. Read-only investigation and planning need no approval.

Resolve factual uncertainty with the smallest decisive source check or permitted scratch experiment. Ask Aman for product decisions or changes to agreed scope, not facts you can establish yourself. If a check is unavailable or impractical, state what remains unknown and the concrete way to settle it. Do not present an inference as proof.

Start with the existing implementation for the same behavior and check the assumptions that make it applicable before reusing it. Prefer fewer independent rules, state owners, and supported ways to perform the operation; fewer changed lines alone does not make a design simpler. Add an abstraction, dependency, retry, cache, fallback, or configuration only when an agreed requirement or demonstrated failure needs it. Preserve handling for legitimate error states. If new evidence invalidates the approach, reconsider it before adding another workaround. Bring changes to agreed behavior or trade-offs back to Aman; resolve implementation details within approved scope yourself.

Derive expected test results from agreed behavior before implementation, never from what the current code happens to do. Exercise the real entrypoint and observe the promised result. For stateful or asynchronous changes, follow the affected state through completion and the relevant transition that could invalidate it; choose transitions from the code and requirement, not a generic checklist. Each regression test must catch a concrete wrong behavior. For a bug, run it against the broken implementation, observe failure caused by the bug, fix, and rerun the same test. A broken fixture is not a reproduction. If automation cannot reproduce it reliably, establish the alternative proof before fixing. Keep meaningful error and behavior tests; remove assertions that merely repeat implementation details.

After the code shape settles, run focused checks and repeat the user's actual route on the affected surface. For mobile behavior, include the reported screen, steps and account state on a simulator or device unless Aman has chosen to test it himself. Report what the evidence establishes and what remains untested. A helper test does not establish that the application reaches it or produces the user-visible result.

When adding or updating packages, be VERY careful. Check upstream or in GHA or in registries or in security auditors that there are no advisories (Non exhaustive examples: npm + GitHub Advisory + Socket for JS, crates.io/RustSec for Rust, pkg.go.dev/Go vulnerability DB for Go, pub.dev/advisories for Dart/Flutter). If possible, do a dry run first by disabling any install/build scripts. e.g., for web, use npm install --ignore-scripts, only removing if after script is vetted and necessary (escalate to me in case of any doubt); and prior to doing any of it check the npm page, the github, the github advisory, socket.dev (and other such sites) for sus.

In Codex, ask for elevated network access when using the gh cli.

Write code in newspaper order.

---

Ente-only rules:
- Keep workflow instructions here and in the `ente-skills` skills. Do not create, restore, or depend on repo-local `AGENTS.md` or `AGENTS.override.md` files.
- Personal skills live in the private `AmanRajSinghMourya/ente-skills` repo, and its `install.sh` links them into `~/.claude/skills` and `~/.codex/skills`. Do not copy them into Ente or publish them as Ente PRs. Commits and pushes to `ente-skills` are pre-approved. Ente product Git actions keep their approval gates.
- Put findings, the decision needed and the next step in the chat. The only task notes file is `DECISIONS.md` in the task's worktree: one line for each choice Aman settles (decision, trade-off or thing left out), excluded from Git and deleted with the worktree.
- After plan approval, name worktree folders `B-<surface>-<bug>`, `F-<surface>-<feature>` or `I-<surface>-<improvement>` under the Ente checkout's `.worktrees/`, on the matching `aman/<surface>-<description>` branch. If the chat is already in its own Ente worktree (Codex's worktree mode), use that one instead of creating another. Claude moves into a new worktree with `EnterWorktree`; Codex attaches one with its `create_worktree` tool. Never stop because a chat can't switch folders.
- For design, UI/UX or Figma tasks, use the `designer` skill. Aman's current decisions take precedence over the imported team kit.
- PRs go through `openpr`, and finished tasks through `cleanup`. In Codex, create worktrees with `create_worktree`. To retire a Codex worktree, `cleanup` uses `archive_worktree` for an attached one, or archives the chat whose own folder it is (`set_thread_archived`), after which Codex deletes the folder. Claude Code removes worktrees with `git worktree remove -f -f`, then `rm -rf`. Aman has approved removing a worktree whatever it holds, so never stop or hand him the command. Standalone investigation and review stay read-only.
- If a step needs a tool only the other app has, say so and hand it back. Never claim it ran.
- To test the mobile apps, log in with the dedicated Ente test account Aman gave you (Codex keeps it in its memory), never his real account, and don't stop to ask. Claude Code doesn't type passwords, so there ask Aman to log in once; the app stays logged in when a new build is installed over it.
- Format and lint changed code during implementation. `/openpr` rechecks formatting and lint before publication; it does not rerun implementation tests or the full CI workflow. GitHub CI runs on the PR.
- Create a ready-to-review PR, not a draft.
- Every PR gets a short description: one to three one-line bullets on the problem and resulting behavior, including relevant decisions or trade-offs. No long paragraphs or routine check lists. `/openpr` writes it without another approval. For visual changes, use `pr-assets` to publish screenshots on a separate asset branch in the public fork and embed commit-pinned Before/After tables; never add them to the product branch.
- Prefix PR titles when applicable: [rust] / [web] / [server] / [mobile] / [infra] / [meta] / [docs]. Do not use [meta] without my explicit approval. [meta] is only for repository-level changes with no better area (e.g. changing the root README); touching multiple areas is not sufficient, and can still be e.g. [web] if it touches js files cross tree.
- Do not apply PR title prefixes to commits.
- For Flutter/Dart commands, including `cargo codegen frb`, request escalation since Flutter needs SDK cache access outside the workspace.
- When creating an Ente branch from the default branch, prefer `aman/<surface>-<short-description>` over `codex/<description>`.
- Default new Ente PRs to the fork `AmanRajSinghMourya/ente`; use `ente/ente` when Aman selects upstream. Report the exact head/target repository, API account, base, title and body in the `/openpr` summary. Verify the selected push URL instead of assuming `origin` means the selected repository.
- For the upstream step, create a separate PR from the reviewed fork branch targeting `ente/ente:main`; never retarget the fork review PR or require pushing the branch into `ente/ente`. Before publishing, check the merge against freshly fetched upstream `main` and check new server migration numbers for collisions. Follow `openpr` for the review and conflict gates.
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

Aman's Ente skills (`/name` in Claude Code, `$name` in Codex): openpr, pr-feedback, cleanup, release, today, support, review-icons,
learn, handoff, teach, copywriter, recent-code-bugfix, plus the helpers investigate, designer, challenge and pr-assets.
For diagrams, use Codex's `visualize` skill.

Aman sometimes forgets these exist. When he asks for something one of them does
and didn't use it, do the work, then end the reply with one line naming it, for
example "Tip: /pr-feedback does this." Only when one clearly fits, at most one
tip per reply, and never the same tip twice in a chat.
