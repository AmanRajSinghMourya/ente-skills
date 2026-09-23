#!/usr/bin/env bash
set -euo pipefail

root="$(cd "$(dirname "$0")" && pwd)"

for target in "$HOME/.claude/skills" "$HOME/.codex/skills"; do
  mkdir -p "$target"
  for skill in "$root"/skills/*/; do
    src="${skill%/}"
    link="$target/$(basename "$src")"
    if [[ -L "$link" && "$(readlink "$link")" == "$src" ]]; then
      continue
    fi
    if [[ -e "$link" || -L "$link" ]]; then
      echo "skip $link (already exists: $(readlink "$link" 2>/dev/null || echo 'not a link'))"
      continue
    fi
    ln -s "$src" "$link"
    echo "linked $link"
  done
done
