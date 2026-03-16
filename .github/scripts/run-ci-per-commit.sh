#!/usr/bin/env bash
# Run the full CI checks on each commit in the given range, sequentially.
# Stops at the first commit that fails.
#
# Usage:
#   run-ci-per-commit.sh <base_sha> <head_sha>
#
# Arguments:
#   base_sha - the base commit (exclusive)
#   head_sha - the head commit (inclusive)
set -euo pipefail

base="${1:?Usage: run-ci-per-commit.sh <base_sha> <head_sha>}"
head="${2:?Missing head_sha}"

commits=$(git rev-list --reverse "${base}..${head}")
total=$(echo "$commits" | wc -l | tr -d ' ')
current=0

for commit in $commits; do
    current=$((current + 1))
    short=$(git rev-parse --short "$commit")
    subject=$(git log -1 --format=%s "$commit")
    echo ""
    echo "=== [$current/$total] Testing ${short}: ${subject} ==="
    echo ""

    git checkout --quiet "$commit"
    make install
    make lint
    make check-format
    make test

    echo ""
    echo "=== [$current/$total] PASSED: ${short} ==="
done

echo ""
echo "All ${total} commit(s) passed CI checks."
