# ente-skills

Aman's personal skills for Ente work. Claude Code and Codex both read them
(`/name` in Claude, `$name` in Codex).

## Commands

| Command | What it does |
| --- | --- |
| `/todo` | Add a task to this Mac's `TODO.md`. |
| `/pickup-task` | Start or resume a task: understand it, plan, wait for your go, build in a worktree. |
| `/openpr` | Final checks, changes entry, cross-model review, one approval, then commit and open the PR on the fork. `/openpr upstream` opens it on ente/ente after the Codex bot's 👍. |
| `/pr-feedback` | Work through review comments, bot findings and CI failures on your PR. |
| `/support` | Draft an answer to a support ticket. Never sends. |
| `/review-icons` | Review an Auth icon PR with the preview site. Posts only after your OK. |
| `/cleanup` | After ente/ente merges: close the fork PR, delete the worktree and local branch. `/cleanup merged` does all of them; `/cleanup disk` frees simulator and build space. |
| `/learn` | Turn something you keep repeating into a check, a skill line or a memory note. |
| `/today` | What needs you: open PRs, red CI, comments, tasks in progress, worktrees to clean up. |
| `/handoff` | A paste-ready message to continue a task in a fresh chat or the other agent. |

The commands call these helpers when a task needs them. You can also call them
directly: `investigate`, `designer`, `verify`, `migrate`, `challenge`.
`copywriter` and `recent-code-bugfix` are kept from the old setup.

## Built-ins we use instead of writing our own

| Job | Claude Code | Codex |
| --- | --- | --- |
| Review someone else's PR | `/code-review <PR number>` (`--comment` posts) | `codex review`, `review-agent` skill |
| Review your own diff, same model | `/code-review` | `codex review --base main` |
| Simplify your diff | `/simplify` (`/openpr` runs it) | none |
| Security pass | `/security-review` | none |
| Diagrams (data flow, before/after) | ask for a Mermaid diagram | `visualize` skill |
| Run and drive the app | `run` skill, simulator tools | `computer-use`, `browser` plugins |
| Continue a chat | `/resume`, `/branch` | `codex resume`, `codex fork` |
| Write a new skill | `skill-creator` | `skill-creator` |
| Flutter, Dart, Figma | `dart-flutter`, `figma` plugins | `dart-flutter`, `figma` plugins |

Not used: Codex's `yeet` and GitHub-plugin skills (they go through the slower
connector; every PR step here uses the `gh` CLI, and AGENTS.md forbids `yeet`),
and Claude's `commit-commands` plugin (`/commit-push-pr` knows nothing about
the fork-then-ente/ente flow).

## Rules every skill keeps

- Plan in chat and wait for Aman's go before a worktree or code changes.
- Bugs: failing test first, then the fix, then the same test passes.
- Never touch staged or unrelated changes.
- One approval of the exact commits and PR before anything is committed.
- Git and PR rules live in `~/.codex/AGENTS.md`.
- The chat is the record. No task notes files.

## TODO list

`todo/TODO.md` stays on this Mac and is not in Git. In Obsidian, open the
`todo/` folder as the vault so it shows only the list. Sections: Up next,
In progress, Later, Done.

## Worktrees

Task worktrees live inside the Ente checkout, under `.worktrees/`. The chat
moves into the worktree before editing, so the Claude or Codex diff view shows
the task's changes.

## Install on a Mac

```sh
./install.sh            # add these skills next to whatever is installed
./install.sh --switch   # also remove the old ente-workflow skill links
```

It does four things:

1. Links every skill here into `~/.claude/skills` and `~/.codex/skills`. It
   skips names that already exist. `--switch` first removes links that point
   into the old `ente-workflow/skills` folder. They're links, so no files are
   deleted.
2. Creates `todo/TODO.md` if it's missing.
3. Installs the official plugins into each app: `dart-flutter` (Flutter and Dart
   skills plus the Dart MCP server, from `flutter/skills`) and `figma`. Each app
   keeps its own copy and updates it, so they aren't stored here.
4. With `--switch`, writes the short block in `reminder.md` into
   `~/.claude/CLAUDE.md` and `~/.codex/AGENTS.md` between
   `<!-- ente-skills:start -->` markers, and replaces it on later runs. It lists
   these skills and tells the agent to end a reply with a one-line tip when you
   did by hand something a skill does.
