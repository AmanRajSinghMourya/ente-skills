---
name: handoff
description: Write a short handoff message Aman can paste into a fresh chat or the other agent (Claude or Codex) to continue an Ente task. Use for /handoff, "prepare a handoff" or "I'll continue this in a new chat".
---

# Handoff

To continue in the same app, the built-ins are enough: `/resume` or `/branch`
in Claude Code, `codex resume` or `codex fork` in Codex. Say so if that fits.

Otherwise, write the handoff in the chat, ready to paste, and don't save it to a
file:

- the goal, in one or two sentences
- the worktree, branch, and PR links
- the decisions Aman made, quoted
- what's done and how it was verified
- what's left, and the next step
- how to check the result

Keep it short. The new chat reads the code, commits and PR itself.
