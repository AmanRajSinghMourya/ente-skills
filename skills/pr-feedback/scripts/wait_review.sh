#!/usr/bin/env bash
# Waits for the Codex bot's review of a PR's latest commit or `@codex review`
# request, then prints one word and exits: feedback, approved, closed or timeout.
set -euo pipefail

[[ $# -ge 2 ]] || { echo "usage: wait_review.sh <owner/repo> <pr> [seconds]" >&2; exit 2; }
repo="$1" pr="$2" limit="${3:-1800}"
end=$((SECONDS + limit))

while ((SECONDS < end)); do
  read -r state since review < <(gh pr view "$pr" --repo "$repo" --json state,commits,comments,reviews --jq '
    ([.commits[-1].committedDate] + [.comments[] | select(.body | contains("@codex review")) | .createdAt] | max) as $since
    | [.state, $since, ([.reviews[] | select((.author.login | startswith("chatgpt-codex-connector"))
        and .submittedAt > $since) | .submittedAt] | max // "-")] | @tsv')
  [[ $state == OPEN ]] || { echo closed; exit 0; }
  thumbs="$(gh api "repos/$repo/issues/$pr/reactions" --jq "[.[]
    | select(.user.login == \"chatgpt-codex-connector[bot]\" and .content == \"+1\" and .created_at > \"$since\")
    | .created_at] | max // \"-\"")"
  if [[ $thumbs != - && ($review == - || $thumbs > $review) ]]; then echo approved; exit 0; fi
  [[ $review != - ]] && { echo feedback; exit 0; }
  sleep 60
done
echo timeout
