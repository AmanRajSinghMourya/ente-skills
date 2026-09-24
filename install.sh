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
    python3 - "$file" "$root/reminder.md" <<'EOF'
import os, re, sys
path, reminder = sys.argv[1], open(sys.argv[2]).read().strip()
block = f"<!-- ente-skills:start -->\n{reminder}\n<!-- ente-skills:end -->"
text = open(path).read() if os.path.exists(path) else ""
pattern = re.compile(r"<!-- ente-skills:start -->.*?<!-- ente-skills:end -->", re.S)
if pattern.search(text):
    new = pattern.sub(lambda _: block, text)
else:
    new = text.rstrip("\n") + ("\n\n" if text.strip() else "") + block + "\n"
if new != text:
    os.makedirs(os.path.dirname(path), exist_ok=True)
    open(path, "w").write(new)
    print(f"updated skill reminder in {path}")
EOF
  done
fi

mkdir -p "$root/todo"
if [[ ! -f "$root/todo/TODO.md" ]]; then
  printf '## Up next\n\n## In progress\n\n## Later\n\n## Done\n' > "$root/todo/TODO.md"
  echo "created $root/todo/TODO.md"
fi

if command -v claude >/dev/null; then
  claude plugin marketplace list 2>/dev/null | grep -q 'dart-flutter' \
    || claude plugin marketplace add flutter/skills \
    || echo "FAILED: claude marketplace flutter/skills"
  for plugin in dart-flutter@dart-flutter figma@claude-plugins-official; do
    claude plugin list 2>/dev/null | grep -q "$plugin" \
      || claude plugin install --scope user "$plugin" \
      || echo "FAILED: claude plugin $plugin"
  done
else
  echo "claude not found: skipped Claude plugins"
fi

if command -v codex >/dev/null; then
  codex plugin marketplace list 2>/dev/null | grep -q '^dart-flutter ' \
    || codex plugin marketplace add flutter/skills \
    || echo "FAILED: codex marketplace flutter/skills"
  for plugin in dart-flutter@dart-flutter figma@openai-curated-remote; do
    codex plugin list 2>/dev/null | grep -qE "^$plugin +installed" \
      || codex plugin add "$plugin" \
      || echo "FAILED: codex plugin $plugin"
  done
else
  echo "codex not found: skipped Codex plugins"
fi
