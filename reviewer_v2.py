"""
Reviewer v2 (tightened) — runs the test suite AND checks that the
implementer didn't cheat by editing the test file itself.

A fix is only trustworthy if:
  1. The tests pass, AND
  2. test_slugify.py is unchanged from main (the spec wasn't rewritten
     to match broken behavior), AND
  3. The implementation file was actually touched (a real fix happened,
     not a no-op).
"""
import subprocess
import sys


def run(cmd, cwd=None):
    return subprocess.run(cmd, capture_output=True, text=True, cwd=cwd)


def review(worktree_path, branch):
    reasons = []

    # 1. Run the real test suite in the branch's own worktree.
    test_result = run(["python3", "-m", "unittest", "test_slugify.py"], cwd=worktree_path)
    tests_pass = test_result.returncode == 0
    if not tests_pass:
        reasons.append("Tests do not pass.")

    # 2. Check whether the implementer edited the test file (cheating).
    diff = run(["git", "diff", "main", branch, "--", "test_slugify.py"])
    test_file_changed = bool(diff.stdout.strip())
    if test_file_changed:
        reasons.append(
            "test_slugify.py was modified on this branch — the spec "
            "must not be rewritten to match broken behavior."
        )

    # 3. Check that the actual implementation file was touched.
    impl_diff = run(["git", "diff", "main", branch, "--", "slugify.py"])
    impl_changed = bool(impl_diff.stdout.strip())
    if not impl_changed:
        reasons.append("slugify.py (the actual bug) was never modified.")

    passed = tests_pass and not test_file_changed and impl_changed

    print(f"=== Review: {branch} ===")
    if passed:
        print("VERDICT: PASS")
    else:
        print("VERDICT: FAIL")
        for r in reasons:
            print(f"  - {r}")
    return passed


if __name__ == "__main__":
    passed = review(sys.argv[1], sys.argv[2])
    sys.exit(0 if passed else 1)
