---
name: todo
description: Add a task to Aman's local Ente TODO list. Use for /todo, "add this to todo", "track this for later", or a GitHub issue, Sentry issue or support ticket to queue.
---

# Add to TODO

The list is `todo/TODO.md` in this skills repository: resolve this skill's
real directory (it is usually reached through a link), go up two levels, then
into `todo/`. It stays on this Mac. If it doesn't exist, create it with:

```markdown
## Up next

## In progress

## Later

## Done
```

1. Write one line: `- [ ] <short title> · <source link>`. The title says the
   outcome in plain words ("Fix album picker keyboard overlap"), not a ticket
   number.
2. Given a link, read it first to get the title: `gh issue view <url> --json
   title,body` for GitHub, the Sentry tools for a Sentry issue, the pasted text
   for a ticket. Keep customer names, emails and logs out of the line.
3. Add it under **Up next**, or **Later** when Aman says later, someday or
   backlog.
4. If the task or link is already listed, say so instead of adding it again.
5. Change only that line. Reply with the line you added.

Adding a task is not approval to start it.
