#!/bin/bash
# The full maker-checker loop for one branch.
# Usage: bash fix_loop.sh <worktree_path> <branch_name>

WORKTREE=$1
BRANCH=$2

echo "=== Fix loop: $BRANCH ==="
python3 reviewer_v2.py "$WORKTREE" "$BRANCH"

if [ $? -eq 0 ]; then
  python3 open_pr.py "$BRANCH" "$WORKTREE"
else
  echo "🚫 No PR opened — reviewer said FAIL."
fi
