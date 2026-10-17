---
name: investigate
description: Investigate Ente behavior, bugs, performance, and implementation context using code and existing GitHub, Notion, and linked discussions. Read-only. Use for /investigate, "why does X happen", "how does X work", "root cause this", or before planning a change.
---

# Investigate

Read-only: no worktree, no product edits. Start from the concrete thing, such as
a file, a screen, a Sentry issue, a log or a user report.

## Existing context

Read supplied GitHub issues or PRs, then look for the matching Notion roadmap or
issue-tracker item. Search by issue/PR URL first, then title or the affected
behavior. Check related GitHub issues, PR discussions and history for earlier
attempts, fixes, reverts and accepted trade-offs. Follow relevant Discord or
testing-thread links for decisions and reports. Reuse context already verified
in this chat; do not repeat broad searches for every follow-up.

Use connectors, APIs or computer use as available. Keep the search bounded to
this issue. Capture the description, owner, status, decisions and linked work
that affect the answer. Read the actual discussion before treating a search hit
or summary as a decision, and distinguish historical intent from current code.
Report inaccessible sources separately from searches with no matches. If no
matching item exists, work from the request and source evidence. Do not create
or update records, post replies, or change statuses during investigation.

## Trace and verify

1. **How it works.** Trace the path from the user action to the effect through
   the real code, with `file:line`: UI, state, service, then API, database or
   sync. Note which app and which shared package (`mobile/packages/*`) it runs
   in.
2. **What actually happens (bugs).** Get runtime evidence before theorizing:
   - reproduce it with a test, on a simulator, or on the local server
   - for crashes, Sentry events and stack traces (Sentry tools) and any device
     logs Aman supplies

   If you can't reproduce it or the state is unclear, say exactly what's missing
   and the cheapest way to get it. Temporary logging is a code change, so propose
   it; add it only in an approved task worktree.
3. **Why it's shaped that way (when history matters).** Use `git log -L` or
   `git blame` to connect the code to the decisions and prior attempts above.
   Quote what an author actually wrote. If nothing records the reason, say
   what you searched. Don't invent one.
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
few runs. Form hypotheses from the trace. Test one variable at a time using
existing controls or permitted scratch experiments. Product edits need separate
implementation approval. Report measurements with the unit, device and build
mode, and distinguish a measured cause from an untested proposed fix.
