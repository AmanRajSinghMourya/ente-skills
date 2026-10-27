---
name: support
description: Help answer an Ente customer support ticket. Understand the problem, find the matching help article, check the code and Sentry for the user's app version, and draft a reply Aman can send. Never sends anything. Also runs the on-demand scan for new tickets tagged or assigned to Aman. Use for /support, a pasted ticket, or "check new tickets" / "my tickets".
---

# Support ticket

1. **Get the ticket** from the Zoho Desk tools if they're connected; otherwise
   ask Aman to paste it. Customer names, emails and logs stay in this chat. Don't
   write them to files or any repo.
2. **Pin down** the app (Photos, Auth, Locker), the platform, the app version,
   and what the user is trying to do versus what happens.
3. **Help docs first.** Search `docs/docs/<app>/` in the Ente repo (FAQ,
   troubleshooting, features). The public pages are under
   https://ente.com/help. If no doc covers it, that's a gap in the docs, not
   proof the feature doesn't exist.
4. **If it looks like a bug:** read the code at the user's version (release tags
   look like `photos-v1.3.64`), check Sentry for matching errors, and read any
   logs they sent. Use `investigate` for anything deeper.
5. **Classify** it: how-to, bug, feature request, account or billing, or needs
   more information.
6. **Draft the reply** in the `copywriter` voice: plain, warm, short, no jargon.
   Include the help link and the exact steps. Don't promise features or dates.
   Ask for exactly the information you still need.
7. **Give Aman** the classification, what you found and its sources, and the
   draft. For a bug, give repro steps without personal data, ready to hand to a task.

## Ticket scan

When Aman asks to check new tickets or "my tickets", scan on demand; never
schedule it. Don't post to Discord or Zoho or edit product code during a scan.

1. **Discord.** Read Ente `#customer-issues` in the Discord desktop app from the
   requested date or the last *completed* scan, overlapping the boundary. Open
   each match to verify the @AmanRaj tag, ticket number, date and direct link.
2. **Zoho.** Check tickets assigned to Aman and verify status and assignment.
   Also check older tracked tickets for new customer replies, even without a new
   Discord tag.
3. **Merge.** Deduplicate by ticket ID, say whether each is a Discord tag, a
   Zoho assignment or both, and flag mistaken tags separately. Refresh the
   search right before reporting so late arrivals are included.
4. **Follow-ups.** Report new customer replies in chat. If a ticket has a
   related Codex chat, send it the reply and ask for a read-only reassessment;
   start a new Ente project chat only when investigation is needed and Aman has
   authorized it.
5. **Record** in `support-tickets/` in the `ente-skills` repo: one file per
   Monday-Sunday week (`YYYY-Www.md`) with the week's verified issues and the
   scan boundary, and `watchlist.md` mapping older tickets to their Codex chat
   and last checked customer reply. Record per-source verification times;
   unknown status or ownership stays unknown. Metadata only: no customer text,
   names, emails, logs or credentials. If a source is inaccessible, report the
   gap and don't advance its scan cursor.
