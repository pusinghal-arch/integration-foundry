#!/usr/bin/env bash
# Verifies every relative Markdown link in the repo points at a file that exists.
# External (http/https) and same-page (#anchor) links are skipped — see
# .github/workflows/ci.yml for external link checking via lychee.
# templates/ is excluded: its links are intentionally illustrative placeholders.
#
# Usage: ./scripts/check-links.sh   (run from anywhere; resolves repo root itself)

set -euo pipefail

repo_root="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$repo_root"

fail=0

while IFS= read -r -d '' file; do
  dir=$(dirname "$file")
  while IFS= read -r link; do
    case "$link" in
      http*|\#*) continue ;;
    esac
    link_path="${link%%#*}"
    [ -z "$link_path" ] && continue
    target="$dir/$link_path"
    if [ ! -e "$target" ]; then
      echo "MISSING: $file -> $link"
      fail=1
    fi
  done < <(grep -oE '\]\([^)]+\)' "$file" | sed -E 's/^\]\((.*)\)$/\1/')
done < <(find . -name '*.md' -not -path './.git/*' -not -path './templates/*' -print0)

if [ "$fail" -eq 0 ]; then
  echo "All relative links resolve."
else
  echo "One or more relative links are broken. See MISSING lines above."
  exit 1
fi
