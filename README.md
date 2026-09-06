# Fix Loop with a Real Checker

An implementer drafts a fix in its own worktree, a separate reviewer
grades it, and only `PASS` opens a PR.

## The bug

`slugify.py` doesn't collapse repeated spaces/special characters:
`slugify("Hello    World")` returns `"hello----world"` instead of
`"hello-world"`. `test_slugify.py` captures this with 3 tests, 2 of
which fail against the buggy implementation on `main`.

## Repository contents

| File | Purpose |
|---|---|
| `SKILL.md` | Fix steps for the implementer (own branch, fix impl not tests, etc.) |
| `slugify.py` / `test_slugify.py` | The buggy code + its spec, on `main` |
| `reviewer_v1.py` | A naive checker — only runs tests. **Kept as a lesson.** |
| `reviewer_v2.py` | The real, tightened checker — see below |
| `open_pr.py` | Only ever called after a `PASS`. Generates a PR file (no network here, so this simulates `gh pr create`) |
| `fix_loop.sh` | Runs review → PR-if-pass for one branch |
| `PR_fix_slugify-good.md` | The PR that got opened, proof a good fix works end to end |

## Why there are two reviewers

`reviewer_v1.py` only checks the test suite's exit code. When run
against a **deliberately bad fix** — a branch where the implementer
"fixed" the tests instead of the code (rewrote the expected values to
match the buggy output) — **it incorrectly returned PASS.** A checker
that approves everything is no checker.

`reviewer_v2.py` fixes this by checking three things, not one:
1. Tests actually pass
2. `test_slugify.py` was NOT modified on the branch (the spec can't be
   rewritten to match broken behavior)
3. `slugify.py` (the real bug) WAS modified (a real fix happened)

## Proof (both required outcomes)

**Good fix → PASS → PR opened:**
```
=== Review: fix/slugify-good ===
VERDICT: PASS
✅ PR opened: PR_fix_slugify-good.md
```

**Bad fix → FAIL, with reasons → no PR:**
```
=== Review: fix/slugify-bad ===
VERDICT: FAIL
  - test_slugify.py was modified on this branch — the spec must not be
    rewritten to match broken behavior.
  - slugify.py (the actual bug) was never modified.
🚫 No PR opened — reviewer said FAIL.
```

## Run it yourself

```bash
# Set up worktrees for each branch (isolates them from main and each other)
git worktree add ../fix-good fix/slugify-good
git worktree add ../fix-bad  fix/slugify-bad

# Run the full loop
bash fix_loop.sh ../fix-good fix/slugify-good   # -> PASS, PR opened
bash fix_loop.sh ../fix-bad  fix/slugify-bad    # -> FAIL, no PR
```

## Wiring this to a real PR

Replace the body of `open_pr.py`'s file-write with:
```bash
gh pr create --title "Fix slugify bug" --body-file pr_body.md --head <branch>
```
Everything upstream of that line (the reviewer's PASS/FAIL gate) stays
exactly the same.

## The actual lesson

The first checker looked reasonable and still let a bad fix through.
The fix wasn't "trust the LLM more" — it was adding concrete,
mechanical checks (diff scope, which files changed) that don't rely on
judgment calls. A real checker has to be hard to fool, not just
plausible-sounding.
