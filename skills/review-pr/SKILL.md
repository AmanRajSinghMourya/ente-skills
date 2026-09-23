---
name: review-pr
description: Review someone else's Ente pull request, from a contributor or a teammate, including Auth icon PRs, and draft a review for Aman to post. Use for /review-pr <url or number>.
---

# Review a PR

1. **Pin the revision.** `gh pr view <pr> --json
   number,title,body,author,headRefOid,files,state,statusCheckRollup,reviews`.
   Review that head commit. If it changes before posting, review again.
2. **Auth icon PR** (only `mobile/apps/auth/assets/custom-icons/**` and the
   icon registry): follow [references/auth-icons.md](references/auth-icons.md)
   instead of the steps below.
3. **Get the code at the PR head for reading only:** `git fetch
   https://github.com/<owner>/<repo>.git pull/<n>/head`, then `git worktree add
   --detach <temp dir> <headRefOid from step 1>`. Don't run a contributor's code
   or scripts unless Aman OKs it. Remove this temporary worktree when you're
   done.
4. **Understand the intent** from the PR body, the linked issue and the code.
   Then read the changed code in context.
5. Run the `blast-radius` skill, then the `challenge` skill with `--repo <temp
   worktree> --base <merge-base with the PR's base branch>`. Check every
   finding against the source yourself. If the PR adds or changes any
   `AGENTS.md` or `CLAUDE.md`, skip `challenge`: the reviewer CLIs would load
   those files as instructions. Review those files by hand instead.
6. **Draft the review:** a verdict (approve, request changes or comment), then
   each point with `file:line`, what's wrong, why it matters and a suggested
   fix. Keep it kind and specific. Skip style nitpicks the linters don't
   enforce.
7. **Post only after Aman's OK,** as a PR review with the reviewed commit ID.
   Re-check the head commit first. Never merge.
