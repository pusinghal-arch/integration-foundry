#!/usr/bin/env bash
# Scaffolds a new reference architecture doc from templates/architecture-template.md,
# numbered to sort after the existing ones.
#
# Usage: ./scripts/new-architecture.sh "some-short-slug"
# Creates: docs/architectures/0N-some-short-slug.md

set -euo pipefail

repo_root="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$repo_root"

slug="${1:-}"
if [ -z "$slug" ]; then
  echo "Usage: $0 <short-slug-no-spaces>"
  exit 1
fi

arch_dir="docs/architectures"
last_num=$(find "$arch_dir" -maxdepth 1 -name '[0-9][0-9]-*.md' -printf '%f\n' 2>/dev/null \
  | sed -E 's/^([0-9]+)-.*/\1/' | sort -n | tail -1)
last_num=${last_num:-0}
next_num=$(printf "%02d" $((10#$last_num + 1)))

target="$arch_dir/${next_num}-${slug}.md"
if [ -e "$target" ]; then
  echo "Refusing to overwrite existing file: $target"
  exit 1
fi

cp templates/architecture-template.md "$target"
echo "Created $target"
echo "Next steps:"
echo "  1. Fill it in — problem, diagram, decisions, when it fits / doesn't."
echo "  2. Add a row for it in the README.md reference architectures table."
echo "  3. Run ./scripts/check-links.sh before committing."
