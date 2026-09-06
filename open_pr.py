"""
Opens a PR — but only ever called after reviewer_v2 returns PASS.
Since this environment has no network/GitHub access, "opening a PR" is
simulated as generating a PR description + diff file. In a real setup,
swap the write-to-file step for `gh pr create --title ... --body ...`.
"""
import subprocess
import sys
from datetime import datetime


def open_pr(branch, worktree_path):
    diff = subprocess.run(
        ["git", "diff", "main", branch], capture_output=True, text=True
    ).stdout

    pr_content = f"""# PR: Fix slugify bug

**Branch:** `{branch}`
**Date:** {datetime.now().strftime("%Y-%m-%d")}
**Reviewer verdict:** PASS

## Summary
slugify() didn't collapse repeated spaces/special characters into a
single hyphen. Fixed by replacing the naive `.replace(" ", "-")` with
a regex that collapses any run of non-alphanumeric characters into one
hyphen, and trims leading/trailing hyphens.

## Diff
```diff
{diff}
```
"""
    filename = f"PR_{branch.replace('/', '_')}.md"
    with open(filename, "w") as f:
        f.write(pr_content)
    print(f"✅ PR opened: {filename}")


if __name__ == "__main__":
    open_pr(sys.argv[1], sys.argv[2])
