---
name: pickup-task
description: Start or resume an Ente task from the local TODO list. Understand it, route it (bug, UI, new behavior, perf, migration, dependency, question), plan in chat, wait for Aman's go, then build it in a task worktree. Use for /pickup-task, "pick up the next task" or "continue <task>".
---

# Pick up a task

## 1. Choose it

Read `TODO.md` at the root of this skills repository (this skill's real
directory, up two levels). Take the task Aman named, otherwise the first line
under **Up next**, and move it to **In progress**. A task already in
**In progress** is a resume: see [Resume](#resume).

## 2. Understand and route

Read the linked issue and the relevant code before asking anything. Ask only
what the code, the issue or the history can't answer.

| The task is | Also use |
| --- | --- |
| A bug, crash, ANR or wrong behavior | `investigate`. Reproduce first. |
| UI, UX, copy or a Figma link | `designer` |
| New behavior, or a change to existing behavior | `blast-radius` |
| Slow, janky or memory-heavy | `perf` |
| A move to `ente_components` or a similar migration | `migrate` |
| A package added or updated | `deps` |
| Only a question | `investigate`. Answer in chat and stop. No worktree. |

A task can match more than one row.

## 3. Plan in chat, then wait

Tell Aman in plain words: what's wrong or wanted, with a concrete example; what
you'll change and why; how you'll prove it works; and any decision only he can
make, with your recommendation. Then wait for his go. Reading and investigating
need no approval. A worktree and code changes do.

## 4. Build

After the go:

1. `git fetch origin`. From the main Ente checkout, create the worktree under
   `.worktrees/` from `origin/main`: `B-<surface>-<desc>` for a bug, `F-` for a
   feature, `I-` for an improvement, on branch `aman/<surface>-<desc>`. Surface
   is photos, auth, locker, server, web or infra. Add the worktree name to the
   TODO line.
2. Bug: write the focused test first and run it. It must fail because of this
   bug; a missing import or a broken fixture is not a reproduction. Fix, then
   rerun the same test. If no reliable automated reproduction exists, say what
   you'll use instead before fixing.
3. Feature: derive tests from the agreed behavior where feasible.
4. UI or runtime behavior: use `verify` before and after, unless Aman said he'll
   test it himself.
5. Once the code shape settles, run the checks the matching
   `.github/workflows/*` job runs.
6. Report in chat: what changed, what the checks and verification showed, what's
   untested. Suggest `/openpr`.

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

## Resume

Read the task's TODO line for its worktree and PR. Then run
`git -C <worktree> status`, `git -C <worktree> log origin/main..HEAD`, look at
the diff, and `gh pr view` if a PR exists. Tell Aman where it stands and what's
next. Don't redo finished work. Ask only for decisions you can't find in the
chat, the commits or the PR.
