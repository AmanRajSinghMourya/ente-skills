---
name: signals
description: Summarize what users are saying about the Ente Photos and Locker mobile apps. Covers new support tickets, GitHub issues and discussions, Discord, and crash spikes, grouped into themes with counts and links, plus what's assigned to Aman in Notion and which GitHub items Notion is missing. Read-only. Use for /signals, "what are users saying", or from /today.
---

# Signals

Read-only. Scope: the Photos and Locker **mobile** apps only, except Aman's
Notion assignments. Skip web, desktop, Auth, server and self-hosting items
unless they clearly hit mobile users.
Window: the last 24 hours, or what Aman asks for ("this week").

## Sources

Run the sources you can reach. Say which ones you skipped and why; a missing
source is a gap, not a quiet day.

1. **GitHub** (`ente/ente` is public; use `gh`). Take the window start as a UTC
   timestamp, for example `SINCE=$(date -u -v-24H +%Y-%m-%dT%H:%M:%SZ)`.
   - Issues opened or updated in the window:
     `gh issue list --repo ente/ente --state all --limit 500 --search "updated:>=$SINCE" --json number,title,body,labels,url,comments,createdAt,updatedAt`.
     If exactly 500 come back, there are more; say the list is incomplete.
     Keep ones labeled `photos`, `locker` or `mobile`, or whose title or body is
     about the Photos or Locker app (many new issues are unlabeled and use
     title prefixes like `[Locker]`).
   - Discussions (categories Enhancements, General, Q&A), newest update first:
     ```sh
     gh api graphql -F after= -f query='query($after:String){repository(owner:"ente",name:"ente"){discussions(first:50,after:$after,orderBy:{field:UPDATED_AT,direction:DESC}){pageInfo{hasNextPage endCursor}nodes{title url body category{name} createdAt updatedAt upvoteCount comments{totalCount}}}}}'
     ```
     If every discussion on the page is inside the window and `hasNextPage` is
     true, fetch the next page with `-F after=<endCursor>`. Stop at the first
     discussion updated before the window.
   - PRs touching Photos or Locker, for the Notion check in step 5 only (they
     aren't user feedback):
     `gh pr list --repo ente/ente --state all --limit 200 --search "updated:>=$SINCE" --json number,title,url,state,files --jq '[.[] | select(any(.files[]?; .path | test("^mobile/apps/(photos|locker)/")))]'`.
2. **Support tickets** through the Zoho Desk tools, if connected in this app:
   tickets created or updated in the window about Photos or Locker on mobile.
   Refer to tickets by ID only.
3. **Discord**, if the bot is set up: for each channel ID in
   [channels.txt](channels.txt), run
   `python3 <this skill's folder>/scripts/discord_read.py <channel id> <hours>`.
   It reads the bot token from the macOS Keychain and prints one message per
   line, each with a link you can cite. Exit code 3 means the bot isn't set up
   on this Mac; read the Notion "Internal Discord User Feedback" pages for the
   window instead, and say so.
4. **Crashes**, if the Sentry tools are connected: new or spiking Photos and
   Locker issues in the window.
5. **Notion**, if connected. Find each database by name with Notion search.
   - Assigned to Aman, any app (find his user with `get_users` and `self`):
     rows of every "<App> Roadmap Items" database whose `Owner` is Aman (a
     person in some databases, text in others), and "Issue tracker" and
     "Discussion tracker" rows whose `Assignee` is Aman. The trackers' `Owner`
     is only suggested routing; list those rows separately as suggested. Skip
     rows already Done.
   - GitHub vs Notion: match each Photos or Locker issue and discussion from
     step 1 to its tracker row by the `GitHub` URL, and each PR to the release
     or roadmap item whose page mentions its URL. Say "not in Notion" when
     nothing matches, and flag tracker rows whose GitHub item was updated after
     their `Source checked`.

## Summary

Group everything into themes, most important first. A theme is what users
experience ("backup stalls on large libraries"), not a source. For each:

- the app (Photos or Locker) and platform if known
- counts per source (for example "4 tickets, 2 issues, 1 Discord thread")
- one or two links as evidence
- whether it's a bug, a feature request, confusion (needs docs or clearer UI),
  or praise

Then list items that need a reply or feedback from the team, and the two Notion
lists from step 5. End with at most three suggested `/todo` lines. Never include
customer names, emails, ticket text or Discord usernames in the summary, and
don't write any of it to files.
