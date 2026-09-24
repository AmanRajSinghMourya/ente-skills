#!/usr/bin/env bash
set -uo pipefail
shopt -s nullglob

usage() { echo "usage: install.sh [--switch]" >&2; exit 2; }

root="$(cd "$(dirname "$0")" && pwd)"
switch=0
case "${1:-}" in
  "") ;;
  --switch) switch=1 ;;
  *) usage ;;
esac

for target in "$HOME/.claude/skills" "$HOME/.codex/skills"; do
  mkdir -p "$target"
  if [[ $switch -eq 1 ]]; then
    for link in "$target"/*; do
      if [[ -L "$link" && "$(readlink "$link")" == */ente-workflow/skills/* ]]; then
        echo "removed old link $link -> $(readlink "$link")"
        rm "$link"
      fi
    done
  fi
  for link in "$target"/*; do
    if [[ -L "$link" && "$(readlink "$link")" == "$root/skills/"* && ! -e "$link" ]]; then
      rm "$link"
      echo "removed link to deleted skill $link"
    fi
  done
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

if [[ $switch -eq 1 ]]; then
  for file in "$HOME/.claude/CLAUDE.md" "$HOME/.codex/AGENTS.md"; do
    if [[ -L "$file" && "$(readlink "$file")" == "$root/instructions.md" ]]; then
      continue
    fi
    mkdir -p "$(dirname "$file")"
    if [[ -e "$file" || -L "$file" ]]; then
      backup="$file.before-ente-skills-$(date +%Y%m%d-%H%M%S)"
      mv "$file" "$backup"
      echo "backed up $file to $backup"
    fi
    ln -s "$root/instructions.md" "$file"
    echo "linked $file"
  done
fi

mkdir -p "$root/todo"
if [[ ! -f "$root/todo/TODO.md" ]]; then
  printf '## Up next\n\n## In progress\n\n## Later\n\n## Done\n' > "$root/todo/TODO.md"
  echo "created $root/todo/TODO.md"
fi

if command -v claude >/dev/null; then
  markets="$(claude plugin marketplace list 2>/dev/null)"
  plugins="$(claude plugin list 2>/dev/null)"
  grep -q 'dart-flutter' <<<"$markets" \
    || claude plugin marketplace add flutter/skills \
    || echo "FAILED: claude marketplace flutter/skills"
  for plugin in dart-flutter@dart-flutter figma@claude-plugins-official; do
    grep -q "$plugin" <<<"$plugins" \
      || claude plugin install --scope user "$plugin" \
      || echo "FAILED: claude plugin $plugin"
  done
else
  echo "claude not found: skipped Claude plugins"
fi

if command -v codex >/dev/null; then
  markets="$(codex plugin marketplace list 2>/dev/null)"
  plugins="$(codex plugin list 2>/dev/null)"
  grep -q '^dart-flutter ' <<<"$markets" \
    || codex plugin marketplace add flutter/skills \
    || echo "FAILED: codex marketplace flutter/skills"
  for plugin in dart-flutter@dart-flutter figma@openai-curated-remote; do
    grep -qE "^$plugin +installed" <<<"$plugins" \
      || codex plugin add "$plugin" \
      || echo "FAILED: codex plugin $plugin"
  done
else
  echo "codex not found: skipped Codex plugins"
fi
