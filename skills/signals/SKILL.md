---
name: signals
description: Summarize what users are saying about the Ente Photos and Locker mobile apps. Covers new support tickets, GitHub issues and discussions, Discord, and crash spikes, grouped into themes with counts and links. Read-only. Use for /signals, "what are users saying", or from /today.
---

# Signals

Read-only. Scope: the Photos and Locker **mobile** apps only. Skip web, desktop,
Auth, server and self-hosting items unless they clearly hit mobile users.
Window: the last 24 hours, or what Aman asks for ("this week").

## Sources

Run the sources you can reach. Say which ones you skipped and why; a missing
source is a gap, not a quiet day.

1. **GitHub** (`ente/ente` is public; use `gh`):
   - Issues opened or updated in the window:
     `gh issue list --repo ente/ente --state all --limit 100 --search "updated:>=<YYYY-MM-DD>" --json number,title,labels,url,comments,createdAt`.
     Keep ones labeled `photos`, `locker` or `mobile`, or whose title or body is
     about the Photos or Locker app (many new issues are unlabeled and use
     title prefixes like `[Locker]`).
   - Discussions (categories Enhancements, General, Q&A):
     ```sh
     gh api graphql -f query='{repository(owner:"ente",name:"ente"){discussions(first:50,orderBy:{field:UPDATED_AT,direction:DESC}){nodes{title url category{name} createdAt updatedAt upvoteCount comments{totalCount}}}}}'
     ```
2. **Support tickets** through the Zoho Desk tools, if connected in this app:
   tickets created or updated in the window about Photos or Locker on mobile.
   Refer to tickets by ID only.
3. **Discord**, if the bot is set up: for each channel ID in
   [channels.txt](channels.txt), run
   `python3 <this skill's folder>/scripts/discord_read.py <channel id> <hours>`.
   It reads the bot token from the macOS Keychain and prints one message per
   line. Exit code 3 means the bot isn't set up on this Mac; skip it and say so.
4. **Crashes**, if the Sentry tools are connected: new or spiking Photos and
   Locker issues in the window.

## Summary

Group everything into themes, most important first. A theme is what users
experience ("backup stalls on large libraries"), not a source. For each:

- the app (Photos or Locker) and platform if known
- counts per source (for example "4 tickets, 2 issues, 1 Discord thread")
- one or two links as evidence
- whether it's a bug, a feature request, confusion (needs docs or clearer UI),
  or praise

Then list items that need a reply or feedback from the team. End with at most
three suggested `/todo` lines. Never include customer names, emails, ticket
text or Discord usernames in the summary, and don't write any of it to files.
