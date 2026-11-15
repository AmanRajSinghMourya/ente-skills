# Global instructions

Aman's current request takes priority. Claude Code reads these rules as `~/.claude/CLAUDE.md` and Codex as `~/.codex/AGENTS.md`. In Codex, read the global retention note in `~/.codex/memories_v2/extensions/ad_hoc/notes/` when you need the Ente test login, GitHub reporting preferences or image-handling preferences.

- Write lean code in newspaper order. Churn is fine. Reuse existing paths after checking their assumptions. Add a mechanism only for an agreed requirement or demonstrated failure. Keep legitimate error handling.
- Settle facts with the smallest decisive check and separate evidence from inference. Decide implementation details yourself. Ask Aman about product decisions and scope.
- A pasted Claude or Codex review is not an endorsement. Classify each point, look for related issues, change nothing.
- Before adding or updating a dependency, check upstream, the registry and advisories (Socket too for JS). Dry-run with scripts disabled. Ask before enabling an install script.
- In Codex, request escalation for `gh` and Flutter/Dart commands, including `cargo codegen frb`.

## Ente

Ask first:
- Before editing product code or creating a branch/worktree. Run `investigate`, give a plan (existing path, smallest change, behavior to preserve, how to verify) and wait. "Fix X" is not approval. A change Aman spells out exactly (a named string, value or line) needs neither.
- Before committing. `/openpr` is that approval, for the fork only.
- Before any Git change while Aman is managing Git state, including edits to staged files.

Work:
- At the start of an Ente chat, set the chat title (`set_thread_title` in Codex): lead the descriptive title with icons: 🏛️ server, 🌐 web or 📱 mobile, then 💚 Photos, 💙 Locker or 💜 Auth when one app is clear. Customer tickets use 🙋 in place of the first icon. Tooling chats get no icon. Keep Aman's wording, update the icons when scope becomes clear, and never repeat one.
- After approval, fetch main. Reuse the chat's own worktree, else make one (`EnterWorktree` in Claude Code, `create_worktree` in Codex) under `.worktrees/` named `B-|F-|I-<surface>-<name>` on `aman/<surface>-<short-description>`. Keep working there even if the chat can't switch folders.
- Record each choice Aman settles as one line in the worktree's Git-excluded `DECISIONS.md`. No other notes files, and no agent instruction files in the product repo.
- Done means: format and lint pass, focused checks pass, a bug's original failing check now passes, and you repeated the user's route on the real entrypoint (simulator or device for mobile, unless Aman tests). Test with the Ente test account, never Aman's own. Codex uses the stored one, and asks if it isn't stored. Claude Code asks Aman to log in once, since it doesn't type passwords. Report what is untested.
- Before commit or push, verify identity `AmanRajSinghMourya <amanrajmourya7@gmail.com>` and the push URL. For an existing PR, push to its actual head repo and branch.
- PR titles: scopes from touched paths, as in `git log`, then a sentence-case description. Mobile is `[mob][photos]`, `[mob][locker]`, `[mob][auth]`, or `[mobile]` when mixed. No scopes in commit titles, no agent or tool names anywhere, `[meta]` only with approval.
