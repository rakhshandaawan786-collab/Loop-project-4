"""
Reviewer v1 (naive) — runs the test suite inside the given worktree.
PASS if tests exit 0, FAIL otherwise. Nothing else is checked.
"""
import subprocess
import sys

def review(worktree_path):
    result = subprocess.run(
        ["python3", "-m", "unittest", "test_slugify.py"],
        capture_output=True, text=True, cwd=worktree_path
    )
    if result.returncode == 0:
        print(f"VERDICT: PASS  (worktree: {worktree_path})")
        return True
    else:
        print(f"VERDICT: FAIL  (worktree: {worktree_path})")
        print(result.stderr)
        return False

if __name__ == "__main__":
    review(sys.argv[1])
