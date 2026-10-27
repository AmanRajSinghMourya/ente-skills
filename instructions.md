# Global instructions

Claude Code (`~/.claude/CLAUDE.md`) and Codex (`~/.codex/AGENTS.md`) both link
to this file in the private `ente-skills` repo. Edit it there and push, so both
Macs get the same rules. Current user instructions take priority.

## Code

- Write code as if every line costs you money and you're poor. Code churn is
  not a problem.
- Write code in newspaper order.
- Format and lint changed code as you go.
- If I paste a review from Claude or Codex, it is not an endorsement (Claude is
  especially prone to Claudeslop). Change nothing; classify each point and note
  any avenue it opens that you missed.

## Git

- Don't commit without asking; I review every diff. Typing `/openpr` is that ask.
- If I'm managing the git state myself (e.g. I've staged files), don't change it
  without asking, and never edit staged files: staged means reviewed. When in
  doubt about any git action, ask. Never force-push a branch that has a PR.
- Commit identity (repo-local): `AmanRajSinghMourya <amanrajmourya7@gmail.com>`.
- Branches are `aman/<surface>-<short-description>`. No `codex` or other
  agent/tool name in branch names, commit titles or PR titles unless I ask.

## Planning and implementation

- For new implementation work, use `investigate` first. Present a proportional
  plan: the observable result, the existing path, the smallest change, behavior
  that must stay unchanged, trade-offs I've accepted, and how you'll verify it.
  Justify each new mechanism by the requirement the existing path can't meet.
  Wait for approval before creating a branch/worktree or editing product code;
  read-only investigation and planning need none. After approval, fetch latest
  main and create the task branch.
- Settle factual uncertainty yourself with the smallest decisive source check or
  scratch experiment. Ask me only for product decisions or scope changes. If a
  check isn't possible, say what's unknown and how to settle it. Don't present
  an inference as proof.
- Start from the existing implementation of the same behavior, after checking it
  applies. Prefer fewer rules, state owners and ways to do the operation; fewer
  changed lines alone isn't simpler. Add an abstraction, dependency, retry,
  cache, fallback or config only for an agreed requirement or a demonstrated
  failure. Keep handling for legitimate error states. If evidence invalidates
  the approach, rethink it instead of adding a workaround. Bring changes to
  agreed behavior or trade-offs back to me; settle implementation details
  yourself.

## Testing

- Derive expected results from the agreed behavior, never from what the code
  currently does. Exercise the real entrypoint. For stateful or async changes,
  follow the state through completion and the transition that could invalidate
  it, chosen from the code and requirement, not a generic checklist.
- Each regression test must catch a concrete wrong behavior. For a bug, run it
  against the broken code, see it fail because of the bug, fix, rerun. A broken
  fixture is not a reproduction; if automation can't reproduce it reliably,
  establish another proof before fixing. Drop assertions that only restate the
  implementation.
- Once the code settles, run focused checks and repeat the user's actual route
  on the affected surface: for mobile, the reported screen, steps and account
  state on a simulator or device, unless I've chosen to test it myself. Report
  what the evidence shows and what's untested. A helper test doesn't prove the
  app reaches it.
- Test mobile apps with the dedicated Ente test account, never my real one, and
  don't stop to ask (Codex keeps it in memory). Claude Code doesn't type
  passwords, so ask me to log in once; installing a new build keeps the login.

## Packages

Be very careful adding or updating packages. First check the registry page,
upstream repo and advisory databases (e.g. npm + GitHub Advisory + Socket,
crates.io/RustSec, Go vulnerability DB, pub.dev advisories). Dry-run with
install/build scripts disabled where possible (`npm install --ignore-scripts`);
enable a script only after vetting it. Escalate any doubt to me.

## Ente workflow

- Workflow rules live here and in the `ente-skills` skills, which its
  `install.sh` links into both apps. Never create or depend on repo-local
  `AGENTS.md`/`AGENTS.override.md`, and never copy skills into Ente. Commits and
  pushes to `ente-skills` are pre-approved; Ente product git actions are not.
- Findings, the decision needed and the next step go in chat. The only notes
  file is `DECISIONS.md` in the task worktree (excluded from git): one line per
  choice I settle.
- Worktrees: after plan approval, create `.worktrees/<B|F|I>-<surface>-<name>`
  (bug/feature/improvement) on the matching branch; Codex uses
  `create_worktree`. If the chat already has its own worktree, use it. In the
  Claude desktop app, branch in the folder the chat launched in instead (its
  diff pane only shows that folder). Never stop because a chat can't switch
  folders.
- Design, UI/UX or Figma: use `designer`; my current decisions beat the team kit.
- PRs go through `openpr`, finished tasks through `cleanup`. Standalone
  investigation and review stay read-only.
- If a step needs a tool only the other app has, say so and hand it back. Never
  claim it ran.
- Flutter/Dart commands, including `cargo codegen frb`, need escalation for SDK
  cache access. In Codex, ask for elevated network access for `gh`.
- When a PR opens or merges in the Codex app, fire one confetti burst.
- Diagrams: Codex's `visualize` skill.

## PRs

`openpr` owns the publishing steps (description, screenshots, upstream PR,
migration checks). In addition:

- Create PRs only with `gh pr create`, never a connector or `github:yeet`.
  Ready for review, not draft.
- New PRs target the fork `AmanRajSinghMourya/ente` unless I choose `ente/ente`.
  Verify the push URL instead of assuming `origin` is the target. Before
  updating an existing PR, check its actual head repo and branch and push there.
- Title: bracketed scopes chosen from the touched paths (not the branch name or
  task wording), then a concise sentence-case description. `mobile/apps/photos`
  → `[mob][photos]`, `locker` → `[mob][locker]`, `auth` → `[mob][auth]`, several
  mobile apps → `[mobile]`; otherwise `[web]`, `[web][app]`, `[server]`,
  `[rust]`, `[infra]`, `[docs]`. `[meta]` only with my approval, for repo-level
  changes with no better area; touching several areas isn't enough. No scopes
  on commits. Check the final title against this before opening. Examples:
  `[mob][photos] Deduplicate memory share files`, `[web] Support for opening
  collection link in web`.

## Skills

When I ask to check new tickets or "my tickets", follow the `support` skill's
ticket scan.

I sometimes forget my skills exist. When I ask for something one clearly does
and you didn't use it, do the work, then end with one line naming it, e.g.
"Tip: /pr-feedback does this." At most one tip per reply, never the same one
twice in a chat.
