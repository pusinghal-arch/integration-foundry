#!/usr/bin/env bash
# Extracts every ```mermaid fenced block from docs/**/*.md and renders it with
# mermaid-cli (mmdc) to confirm the syntax actually compiles. Requires mmdc on
# PATH — CI installs it via `npm install -g @mermaid-js/mermaid-cli`.
#
# Usage: ./scripts/validate-mermaid.sh

set -euo pipefail

repo_root="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$repo_root"

if ! command -v mmdc >/dev/null 2>&1; then
  echo "mmdc (mermaid-cli) not found on PATH. Install with:"
  echo "  npm install -g @mermaid-js/mermaid-cli"
  exit 1
fi

tmp=$(mktemp -d)
trap 'rm -rf "$tmp"' EXIT

fail=0
count=0

while IFS= read -r -d '' file; do
  block=""
  in_block=0
  block_index=0
  while IFS= read -r line; do
    if [ "$in_block" -eq 0 ] && [[ "$line" == '```mermaid' ]]; then
      in_block=1
      block=""
      continue
    fi
    if [ "$in_block" -eq 1 ] && [[ "$line" == '```' ]]; then
      in_block=0
      block_index=$((block_index + 1))
      count=$((count + 1))
      src="$tmp/block.mmd"
      printf '%s\n' "$block" > "$src"
      if ! mmdc -i "$src" -o "$tmp/out-$count.svg" >/tmp/mmdc-out.log 2>&1; then
        echo "FAILED to render mermaid block #$block_index in $file:"
        sed 's/^/  /' /tmp/mmdc-out.log
        fail=1
      fi
      continue
    fi
    if [ "$in_block" -eq 1 ]; then
      block="$block
$line"
    fi
  done < "$file"
done < <(find docs -name '*.md' -print0)

echo "Validated $count Mermaid block(s)."
if [ "$fail" -ne 0 ]; then
  exit 1
fi
