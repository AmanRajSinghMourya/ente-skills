# ente-skills

Aman's personal skills for Ente work. Claude Code and Codex both read them
(`/name` in Claude, `$name` in Codex).

## Commands

| Command | What it does |
| --- | --- |
| `/todo` | Add a task to this Mac's `TODO.md`. |
| `/pickup-task` | Start or resume a task: understand it, plan, wait for your go, build in a worktree. |
| `/openpr` | Final checks, changes entry, cross-model review, one approval, then commit and open the PR. |
| `/pr-feedback` | Work through review comments, bot findings and CI failures on your PR. |
| `/support` | Draft an answer to a support ticket. Never sends. |
| `/review-pr` | Review someone else's PR, including Auth icon PRs. Posts only after your OK. |
| `/cleanup` | Remove a finished task's worktree and local branch; `/cleanup disk` frees simulator and build space. |
| `/learn` | Turn something you keep repeating into a check, a skill line or a memory note. |
| `/today` | What needs you: open PRs, red CI, comments, tasks in progress, worktrees to clean up. |

The commands call these helpers when a task needs them. You can also call them
directly: `investigate`, `blast-radius`, `designer`, `verify`, `perf`,
`migrate`, `deps`, `challenge`. `copywriter` and `recent-code-bugfix` are kept
from the old setup.

## Rules every skill keeps

- Plan in chat and wait for Aman's go before a worktree or code changes.
- Bugs: failing test first, then the fix, then the same test passes.
- Never touch staged or unrelated changes.
- One approval of the exact commits and PR before anything is committed.
- Git and PR rules live in `~/.codex/AGENTS.md`.
- The chat is the record. No task notes files.

## TODO list

`TODO.md` sits at the root of this folder, stays on this Mac and is not in Git.
Obsidian can open it. Sections: Up next, In progress, Later, Done.

## Install on a Mac

```sh
./install.sh
```

It links every skill into `~/.claude/skills` and `~/.codex/skills`, and skips
names that already exist there. To switch off the old workflow, remove its links
(they are links, so this deletes nothing):

```sh
rm ~/.claude/skills/{ente-task-workflow,ente-task-queue,ente-mobile-ui-pr-workflow}
rm ~/.codex/skills/{ente-task-workflow,ente-task-queue,ente-mobile-ui-pr-workflow}
```
