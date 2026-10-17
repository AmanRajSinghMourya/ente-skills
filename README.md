# ente-skills

Aman's personal skills for Ente work.

## Commands

| Command | What it does |
| --- | --- |
| `/openpr` | Checks what changed, adds the changes entry, runs a cross-model review, then commits and opens the PR on the fork. `/openpr upstream` opens it on ente/ente after the Codex bot's 👍. |
| `/pr-feedback` | Review comments, bot findings and CI failures, with draft replies. Starts by itself after `/openpr`. |
| `/cleanup` | Closes fork PRs merged upstream, deletes their worktrees, branches and screenshots, and drafts the Notion update. `/cleanup <task>` does one; `/cleanup disk` frees build space. |
| `/release` | Tests main before the RC, checks the RC, reads tester feedback (`/release check`), then the changelog and help docs (`/release done`). |
| `/today` | What needs you: open PRs, red CI, comments, worktrees to clean up, your Notion tasks, and what users say about Photos and Locker. `/today prs` or `/today users [window]` for one part. |
| `/support` | Drafts an answer to a support ticket. Never sends. |
| `/review-icons` | Reviews an Auth icon PR with the preview site. |
| `/teach` | Ground-up explanation of any part of Ente, with diagrams, an interactive page and a Manim video. |
| `/learn` | Turns something you keep repeating into a check, a skill line or a memory note. |
| `/handoff` | A paste-ready message to continue a task in a fresh chat. |

Helpers the commands call, also usable directly: `investigate`, `designer`,
`challenge`, `pr-assets`, `copywriter`, `recent-code-bugfix`.

## Install

```sh
./install.sh            # link the skills and install the dart-flutter and figma plugins
./install.sh --switch   # also link instructions.md as the global rules
```

Edit `instructions.md` here and push; the other Mac gets it with `git pull`.
