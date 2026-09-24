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
| `/signals` | What users say about Photos and Locker mobile: tickets, GitHub, Discord, crashes. `/today` includes it. |

The commands call these helpers when a task needs them. You can also call them
directly: `investigate`, `designer`, `migrate`, `challenge`.
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
./install.sh --switch   # also remove old ente-workflow links and link the global instructions
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
4. With `--switch`, links `~/.claude/CLAUDE.md` and `~/.codex/AGENTS.md` to
   `instructions.md`, so both apps and both Macs read the same global rules.
   Existing files are moved aside to `*.before-ente-skills-<time>` first.
   Edit `instructions.md` here and push; the other Mac gets it with `git pull`.

## Test login

Tell Codex the test account's email and password once and ask it to remember
them. Claude Code doesn't type passwords, so log in yourself once on the
simulator; the app stays logged in across new builds.

## Discord for `/signals`

Discord has no official MCP. `/signals` reads channels through a real Discord
bot and the Discord API, which is instant and needs no browser login. Don't
automate a normal user account: Discord bans "self-bots".

1. At https://discord.com/developers/applications, create an application, open
   **Bot**, turn on **Message Content Intent**, and copy the token.
2. Under **OAuth2 → URL Generator**, pick scope `bot` with only **View Channels**
   and **Read Message History**. A server admin opens the URL to add the bot and
   limits it to the channels you want read.
3. On each Mac, store the token in the Keychain (it prompts for it; never put it
   in Git): `security add-generic-password -s ente-discord-bot -a "$USER" -w`
4. Add the channel IDs to `skills/signals/channels.txt`.
