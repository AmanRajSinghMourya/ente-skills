---
name: learn
description: Turn something Aman keeps repeating to agents into a lasting fix, meaning a check, a line in an existing skill, a new skill or a memory note. Use for /learn or "stop making me say this". When Aman corrects the same thing twice in one chat, offer it but don't run it unasked.
---

# Learn

1. **Name the rule** in one sentence and quote the moments Aman said it, from
   this chat or from `/learn history`.
2. **Make sure it's real.** It must be a correction Aman repeated, or a bot or
   reviewer finding confirmed true more than once. One-offs and unverified
   reviewer claims don't count. Separate an agent mistake from a later product
   decision. Identify the decision that repeatedly went wrong.
3. **Pick the strongest home**, the first one that fits:
   1. A check that fails loudly: a script here, or a lint the Ente repo already
      runs. An Ente repo change is a normal task, not done here.
   2. The instruction where that decision is made. Replace overlapping wording
      instead of appending another reminder. Use shared instructions for a
      cross-task rule and an existing skill for a workflow-specific rule.
   3. A new skill, if it's a whole workflow. Write it with the app's built-in
      `skill-creator` (Claude Code and Codex both ship one). Put it in this
      skills repository, not the app's own folder, so both apps get it.
   4. A memory note (Claude memory or Codex memories) for a preference that
      needs judgment.

   Before writing a new skill, check whether Claude Code or Codex already ships
   one that does the job. If one does, point to it instead.
4. **Evaluate the proposal.** Replay two independent past failures and one case
   where the existing behavior was correct. Compare the current and proposed
   instructions from the same stopping point, without revealing the later
   correction to the evaluator. Check whether the mistaken decision changes
   without unnecessary work, lost safeguards or extra permission requests.
   Show the results and limits; a passing replay does not prove future behavior.
5. **Show the smallest diff** and wait for Aman's OK, unless he already approved
   applying the change.
6. **Apply.** Skill changes go in this skills repository. Stage only the files
   you changed, commit with a plain message, and push.

## `/learn history`

Look for repeated corrections in recent chats about Ente only. Claude
transcripts are in `~/.claude/projects/<folder named after the Ente checkout
path>/*.jsonl`; Codex sessions are in `~/.codex/sessions/`. Read them in a
subagent. Return the top few patterns with quotes, then continue from step 2.
Never quote customer names, emails, ticket text or logs; describe the pattern
instead.
