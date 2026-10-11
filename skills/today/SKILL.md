---
name: today
description: Show what needs Aman's attention in Ente right now, in one report. Covers his fork and ente/ente PRs (CI, review comments, which are ready for ente/ente or cleanup), his Notion tasks, and what users say about the Photos and Locker mobile apps (support tickets, GitHub, Discord, crashes, grouped into themes). Read-only. Use for /today, "what's pending", "what needs me" or "what are users saying".
---

# Today

Read-only. Change nothing.

- `/today`: everything below, for the last 24 hours.
- `/today prs`: only PRs and worktrees (part 1).
- `/today users [window]`: only Notion and user signals (parts 2 and 3), for
  the window Aman names ("this week"), default 24 hours. "What are users
  saying" means this.

Run the sources you can reach. Say which ones you skipped and why; a missing
source is a gap, not a quiet day.

## 1. PRs

Aman opens each PR on his fork `AmanRajSinghMourya/ente` first, then opens the
same branch on `ente/ente` after the Codex review bot approves the fork PR.
Always use `ente/ente`; through the old `ente-io/ente` name, `--author @me`
returns nothing.

- **Fork PRs:** `gh pr list --repo AmanRajSinghMourya/ente --state open --json
  number,title,url,headRefName,statusCheckRollup`. For each one:
  - its `ente/ente` PR: `gh pr list --repo ente/ente --head <headRefName>
    --state all --json number,state,url`
  - the Codex bot's verdict on the head commit: `wait_review.sh
    AmanRajSinghMourya/ente <n> 1` from the `pr-feedback` skill
  - unresolved review threads, using the `reviewThreads` query from the
    `pr-feedback` skill
- **Upstream PRs:** `gh pr list --repo ente/ente --author @me --json
  number,title,url,reviewDecision,statusCheckRollup`, with the same thread
  count.
- **Worktrees:** `git worktree list` in the main Ente checkout, matched to the
  PRs above.

## 2. Notion

Find each database by name with Notion search.

- **Assigned to Aman, any app** (find his user with `get_users` and `self`):
  rows of every "<App> Roadmap Items" database whose `Owner` is Aman (a person
  in some databases, text in others), and "Issue tracker" and "Discussion
  tracker" rows whose `Assignee` is Aman. The trackers' `Owner` is only
  suggested routing; list those rows separately as suggested. Skip rows
  already Done.
- **GitHub vs Notion:** match each Photos or Locker issue and discussion from
  part 3 to its tracker row by the `GitHub` URL, and each PR to the release or
  roadmap item whose page mentions its URL. Say "not in Notion" when nothing
  matches, and flag tracker rows whose GitHub item was updated after their
  `Source checked`.

## 3. User signals

Scope: the Photos and Locker **mobile** apps. Skip web, desktop, Auth, server
and self-hosting items unless they clearly hit mobile users.

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
   - PRs touching Photos or Locker, for the Notion check only (they aren't user
     feedback):
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

## 4. Reply

Short groups, skipping empty ones:

1. **Needs you now:** red CI, changes requested, unresolved comments
   (`/pr-feedback`).
2. **Ready for ente/ente:** fork PRs the bot approved with no `ente/ente` PR
   (`/openpr upstream`).
3. **Waiting on ente/ente review.**
4. **To clean up:** merged upstream with the fork PR still open, or a worktree
   left over (`/cleanup`).
5. **Your Notion tasks,** then the suggested ones.
6. **What users say:** themes, most important first. A theme is what users
   experience ("backup stalls on large libraries"), not a source. For each:
   the app and platform if known; counts per source (for example "4 tickets,
   2 issues, 1 Discord thread"); one or two links as evidence; and whether
   it's a bug, a feature request, confusion (needs docs or clearer UI) or
   praise.
7. **Needs a team reply,** and GitHub items not in Notion.
8. **At most three suggested tasks.**

Never include customer names, emails, ticket text or Discord usernames, and
don't write any of it to files.
