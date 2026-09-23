---
name: support
description: Help answer an Ente customer support ticket. Understand the problem, find the matching help article, check the code and Sentry for the user's app version, and draft a reply Aman can send. Never sends anything. Use for /support or a pasted ticket.
---

# Support ticket

1. **Get the ticket** from the Zoho Desk tools if they're connected; otherwise
   ask Aman to paste it. Customer names, emails and logs stay in this chat. Don't
   write them to files, TODO or any repo.
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
   draft. For a bug, offer to `/todo` it with repro steps and no personal data.
