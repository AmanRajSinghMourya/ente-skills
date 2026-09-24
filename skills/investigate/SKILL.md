---
name: investigate
description: Find out how Ente code works, why it's shaped that way, why something breaks (bug, crash, ANR, OOM, wrong data), or why it's slow, with evidence. Read-only. Use for /investigate, "why does X happen", "how does X work", "root cause this", "why is this slow", or a bug picked up by pickup-task.
---

# Investigate

Read-only: no worktree, no product edits. Start from the concrete thing, such as
a file, a screen, a Sentry issue, a log or a user report.

1. **How it works.** Trace the path from the user action to the effect through
   the real code, with `file:line`: UI, state, service, then API, database or
   sync. Note which app and which shared package (`mobile/packages/*`) it runs
   in.
2. **What actually happens (bugs).** Get runtime evidence before theorizing:
   - reproduce it with a test, the `verify` skill on a simulator, or the local
     server
   - for crashes, Sentry events and stack traces (Sentry tools) and any device
     logs Aman supplies

   If you can't reproduce it or the state is unclear, say exactly what's missing
   and the cheapest way to get it. Temporary logging is a code change, so propose
   it; add it only in an approved task worktree.
3. **Why it's shaped that way (when history matters).** Run `git log -L` or
   `git blame` on the lines, then read the PRs (`gh pr view <n>`) and linked
   issues. Quote what an author actually wrote. If nothing records the reason,
   say what you searched. Don't invent one.
4. **Narrow the cause.** List the candidate causes and rule each out with
   evidence until one is left. Check Aman's guess, and your own, against the
   evidence before accepting it.
5. **Answer in chat:**
   - what's happening, with a concrete example
   - the cause: what the evidence establishes and its source, what's not yet
     checked, and the concrete step that would settle it
   - what a fix would look like, and its risk
   - the next step

   Use plain words and define terms he may not know. No hedging filler.

## Slow, janky or memory-heavy

Measure before reading code. Pick one number with a unit and how you measure it:
frame times (Flutter DevTools, `flutter run --profile`), startup time, memory
(Instruments or `adb shell dumpsys meminfo`), or sync/upload time. Take a
baseline on a profile or release build, never debug, on the same device, over a
few runs. Form hypotheses from the trace. Then change one thing at a time,
measure after each, and keep only what moves the number. Report before and
after with the unit, device and build mode.

When `pickup-task` called this, go back to its plan step afterwards.
