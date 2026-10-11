#!/usr/bin/env bash
# Waits for the Codex bot to finish reviewing a fork PR's head commit, after
# the latest `@codex review` request, then prints one word and exits:
# feedback, approved, closed or timeout. Pass 1 as the seconds to check once.
set -euo pipefail

[[ $# -ge 2 ]] || { echo "usage: wait_review.sh <owner/repo> <pr> [seconds]" >&2; exit 2; }
repo="$1" pr="$2" limit="${3:-1800}"
end=$((SECONDS + limit))

# The bot keeps one summary comment up to date with the commit it last reviewed.
read -r -d '' filter <<'EOF' || true
def bot: .author.login | startswith("chatgpt-codex-connector");
.headRefOid as $head
| ([.comments[] | select((bot | not) and (.body | contains("@codex review"))) | .createdAt]
    | max // "") as $asked
| ([.comments[] | select(bot) | .body
    | capture("Completed\\*\\* <relative-time datetime=\"(?<at>[^\"]+)\">[^|]*\\| `(?<commit>[0-9a-f]+)`")]
    | last) as $done
| if .state != "OPEN" then "closed"
  elif $done == null or ($head | startswith($done.commit) | not) or $done.at < $asked then "waiting"
  elif any(.reviews[]; bot and .commit.oid == $head and .submittedAt > $asked) then "feedback"
  else "approved" end
EOF

while :; do
  result="$(gh pr view "$pr" --repo "$repo" --json state,headRefOid,comments,reviews --jq "$filter")"
  [[ $result != waiting ]] && { echo "$result"; exit 0; }
  ((SECONDS + 60 < end)) || break
  sleep 60
done
echo timeout
