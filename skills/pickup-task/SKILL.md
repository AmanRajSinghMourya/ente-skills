---
name: pickup-task
description: Start or resume an Ente task from the local TODO list. Understand it, route it (bug, UI, new behavior, perf, migration, dependency, question), plan in chat, wait for Aman's go, then build it in a task worktree. Use for /pickup-task, "pick up the next task" or "continue <task>".
---

# Pick up a task

## 1. Choose it

Read `todo/TODO.md` in this skills repository (this skill's real directory, up
two levels, then `todo/`). Take the task Aman named, otherwise the first line
under **Up next**, and move it to **In progress**. A task already in
**In progress** is a resume: see [Resume](#resume).

## 2. Understand and route

Read the linked issue and the relevant code before asking anything. Ask only
what the code, the issue or the history can't answer.

| The task is | Also use |
| --- | --- |
| A bug, crash, ANR or wrong behavior | `investigate`. Reproduce first. |
| Slow, janky or memory-heavy | `investigate`, its measuring section |
| UI, UX, copy or a Figma link | `designer` |
| New behavior, or a change to existing behavior | [Blast radius](#blast-radius) below |
| A move to `ente_components` or a similar migration | `migrate` |
| A package added or updated | [Dependencies](#dependencies) below |
| Only a question | `investigate`. Answer in chat and stop. No worktree. |

A task can match more than one row.

## 3. Plan in chat, then wait

Tell Aman in plain words: what's wrong or wanted, with a concrete example; what
you'll change and why; how you'll prove it works; and any decision only he can
make, with your recommendation. Then wait for his go. Reading and investigating
need no approval. A worktree and code changes do.

## 4. Build

After the go:

1. **Work where the chat already is, if you can.** The app's diff view follows
   the chat's folder, and a Codex chat can't change its folder once started.
   Branch name: `aman/<surface>-<desc>` (surface: photos, auth, locker, server,
   web or infra). Run `git fetch origin` first.
   - **The chat is already in its own Ente worktree** (not the main checkout;
     for example Codex's worktree mode under `~/.codex/worktrees/`): if it's
     clean, `git switch -c aman/<surface>-<desc> origin/main` right there. Don't
     create another worktree.
   - **The chat is in the main checkout:** create
     `.worktrees/<B|F|I>-<surface>-<desc>` from `origin/main` on that branch
     (the main checkout's `.git/info/exclude` must have `/.worktrees/`), and
     move in with `EnterWorktree` and the worktree `path` (Claude Code). In
     Codex, use the app's `create_worktree` tool instead: it attaches a
     managed worktree to this chat without moving it. Then create the branch
     there and work in the returned path. Only if that tool is missing, use
     `git worktree add` and edit it by its full path.

   Never stop just because the chat can't switch folders. Add the worktree
   path to the TODO line.
2. Bug: write the focused test first and run it. It must fail because of this
   bug; a missing import or a broken fixture is not a reproduction. Fix, then
   rerun the same test. If no reliable automated reproduction exists, say what
   you'll use instead before fixing.
3. Feature: derive tests from the agreed behavior where feasible.
4. UI or runtime behavior: run the app on a simulator before and after the
   change (Claude Code's `run` skill, or Codex's computer use), unless Aman said
   he'll test it himself.
5. Once the code shape settles, run the checks the matching
   `.github/workflows/*` job runs.
6. Report in chat: what changed, what the checks and verification showed, what's
   untested. Suggest `/openpr`.

## Decisions

Keep `DECISIONS.md` in the task's worktree root. Add `/DECISIONS.md` to the
main checkout's `.git/info/exclude` (it covers every worktree), so it's never
committed. Whenever Aman settles something in the chat ("do X, not Y", a
trade-off, a product call, something left out), add one line:

```
- 2026-10-09 · Send the push only after the email succeeds, not before · so users never get a push for a failed email
```

Note trade-offs and things left out the same way, marked `Trade-off:` or
`Not in this PR:`. Read it on resume. `/openpr` turns it into the PR
description, and `/cleanup` deletes it with the worktree.

## Rules

- Never touch staged or unrelated changes in any checkout. Never commit; that's
  `/openpr`.
- If something you find changes what Aman already agreed, bring it back to him
  before building it.
- If the change heads past about 1,000 changed lines, stop and re-plan with him.
- Problems you find that aren't this task: list them at the end and offer
  `/todo`.

Apply these when they fit the task:

- Follow the existing pattern in the same app before generic Flutter or Dart
  advice. No new package, router or architecture unless asked.
- When Aman says "do what Photos does", copy Photos' shape exactly: no helper,
  endpoint or safeguard Photos lacks. Offer extras as suggestions.
- Make the smallest change that solves it. No just-in-case code.
- Fix the root cause, not the symptom.
- Tests call the code the way users do and assert a literal expected result.
- Say what's established, what isn't, and the concrete way to settle it.

## Blast radius

For new or changed behavior, find what could break beyond the diff, not just its
callers. Name the one fact the change is safe because of (for example "old
clients ignore this field") and prove it as cheaply as you can: point at the
line, or better, run a test or script against the real code. Look where grep
stops:

- shared packages used by several apps (`mobile/packages/*`)
- old app versions still talking to the server
- local SQLite schema and data already on users' devices
- encryption and serialization formats
- background isolates, sync and upload queues, app lock
- iOS, Android and desktop differences, and feature flags

Put the risks and that one fact in the plan.

## Dependencies

Adding or updating a package needs Aman's OK in the plan. Check advisories
first: pub.dev and GitHub advisories for Dart, RustSec for Rust, `govulncheck`
for Go, npm/GitHub/Socket for JS. Read the changelog for breaking changes, dry
run first (`dart pub upgrade --dry-run`, `cargo update --dry-run`, JS installs
with `--ignore-scripts`), and read the lockfile diff for surprise bumps.

## Resume

Start from Aman's `/handoff` message if he pasted one. Read the task's TODO line
for its worktree and PR, and work in that worktree (build step 1). Then run
`git -C <worktree> status`, `git -C <worktree> log origin/main..HEAD`, look at
the diff, and `gh pr view` if a PR exists. Tell Aman where it stands and what's
next. Don't redo finished work. Ask only for decisions you can't find in the
chat, the commits or the PR.
