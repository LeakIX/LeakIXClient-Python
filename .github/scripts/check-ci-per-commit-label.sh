#!/usr/bin/env bash
# Check if the ci:per-commit label is present.
#
# For pull_request events, checks labels from the event payload.
# For push events, looks up the originating PR via the GitHub API.
#
# Usage:
#   check-ci-per-commit-label.sh <event_name> <repository> <sha> [labels_json]
#
# Arguments:
#   event_name  - "pull_request" or "push"
#   repository  - e.g. "owner/repo"
#   sha         - commit SHA
#   labels_json - JSON array of label names (required for pull_request)
#
# Output:
#   Prints has_label=true or has_label=false (for GITHUB_OUTPUT)
set -euo pipefail

event_name="${1:?Usage: check-ci-per-commit-label.sh <event_name> <repository> <sha> [labels_json]}"
repository="${2:?Missing repository}"
sha="${3:?Missing sha}"
labels_json="${4:-}"

HAS_LABEL="false"

if [ "$event_name" = "pull_request" ]; then
    if echo "$labels_json" | grep -q "ci:per-commit"; then
        HAS_LABEL="true"
    fi
else
    PRS=$(gh api \
        "repos/${repository}/commits/${sha}/pulls" \
        --jq '.[].number')
    for pr in $PRS; do
        LABELS=$(gh api \
            "repos/${repository}/pulls/${pr}" \
            --jq '.labels[].name')
        if echo "$LABELS" | grep -q "^ci:per-commit$"; then
            HAS_LABEL="true"
            break
        fi
    done
fi

echo "has_label=${HAS_LABEL}"
