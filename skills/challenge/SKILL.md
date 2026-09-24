---
name: challenge
description: Get an independent read-only review of the current Ente change from the other model (Codex when Claude is working, Claude when Codex is working), or from both. Use for /challenge, before /openpr, and inside /review-pr.
---

# Cross-model review

This exists only to get the other model's opinion. For a same-model review, use
the built-ins: `/code-review` in Claude Code, `codex review` or the
`review-agent` skill in Codex.

1. Write a short context file for the reviewer: what the change must do (the
   agreed behavior), what you verified and how, and what's untested. Put it
   outside the repo. The script copies it, so the reviewer sees only that copy.
2. Run the script, saying who you are. It lives at `scripts/challenge.sh` in
   this skill's real directory. The skill is usually reached through a link, so
   use the base directory shown when the skill loads, or resolve the link.

   ```sh
   <skill dir>/scripts/challenge.sh --from claude|codex --repo <worktree> --base <commit or branch> \
     --context <file> [--reviewer codex|claude|both]
   ```

   - The reviewer defaults to the other model. Use `both` for risky changes
     (server, migrations, encryption, sync) or when Aman asks.
   - A review takes several minutes. Run it in the background or with a long
     timeout.
   - The reviewer gets the base, the full diff including untracked files, and
     your context file. It's read-only and can't start another review. Codex
     reviews in a read-only sandbox. Claude can read files and run only
     `git log`, `show`, `blame`, `diff` and `grep`, so it can't run tests.
   - Each attempt writes its own file. The script prints the path and whether
     the review completed. An empty output or a non-zero exit means the review
     is incomplete. Say so; never present it as a pass.
   - From inside Codex, the first run of `claude` may need network or keychain
     permission.
3. Check every finding against the source yourself. Tell Aman the ones that
   matter and what you did with each: fixed, rejected with the reason, or needs
   his call. Then delete the review folder the script printed; it holds a copy
   of the diff.

A review Aman pastes into chat is only classified, not acted on, unless he asks
for changes.
