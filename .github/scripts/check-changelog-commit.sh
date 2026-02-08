#!/usr/bin/env bash
# Verify CHANGELOG.md hygiene in pull requests:
# 1. CHANGELOG.md changes must be in their own dedicated commit
# 2. Commit hashes referenced in new changelog entries must exist
# 3. Commit link URLs must match their reference keys
#
# Usage: check-changelog-commit.sh <base-sha>
set -euo pipefail

base="${1:?Usage: check-changelog-commit.sh <base-sha>}"
errors=0

# --- Check 1: CHANGELOG.md must be in dedicated commits ---

for commit in $(git log --format=%H "${base}..HEAD"); do
    files=$(git diff-tree --no-commit-id --name-only -r "$commit")
    if echo "$files" | grep -q "^CHANGELOG.md$"; then
        file_count=$(echo "$files" | wc -l | tr -d ' ')
        if [ "$file_count" -gt 1 ]; then
            echo "::error::Commit $commit modifies CHANGELOG.md alongside other files."
            echo "CHANGELOG.md changes must be in their own dedicated commit."
            errors=$((errors + 1))
        fi
    fi
done

# --- Check 2: Referenced commit hashes must exist ---

changelog_diff=$(git diff "${base}..HEAD" -- CHANGELOG.md \
    | grep "^+" | grep -v "^+++" || true)

inline_hashes=$(echo "$changelog_diff" \
    | grep -oE '\(\[([0-9a-f]{7,})\]' \
    | grep -oE '[0-9a-f]{7,}' | sort -u || true)

for hash in $inline_hashes; do
    if ! git cat-file -t "$hash" >/dev/null 2>&1; then
        echo "::error::Commit $hash referenced in CHANGELOG.md does not exist."
        errors=$((errors + 1))
    fi
done

# --- Check 3: Link URLs must match their keys ---

link_lines=$(echo "$changelog_diff" \
    | grep -E '^\+\[[0-9a-f]{7,}\]: https://.*commit/' || true)

while IFS= read -r line; do
    [ -z "$line" ] && continue
    key=$(echo "$line" \
        | grep -oE '\[([0-9a-f]{7,})\]' | head -1 \
        | tr -d '[]')
    url_hash=$(echo "$line" \
        | grep -oE 'commit/[0-9a-f]{7,}' \
        | sed 's|commit/||')
    if [ -n "$key" ] && [ -n "$url_hash" ] && [ "$key" != "$url_hash" ]; then
        echo "::error::Link [$key] points to commit/$url_hash but should point to commit/$key"
        errors=$((errors + 1))
    fi
done <<< "$link_lines"

# --- Summary ---

if [ "$errors" -gt 0 ]; then
    echo "Found $errors changelog error(s)."
    exit 1
fi

echo "All changelog checks passed."
