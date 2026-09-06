# Skill: Fixing a Failing Bug (Implementer)

Steps to follow when fixing a bug in this repo:

1. **Create your own worktree/branch.** Never fix directly on `main`.
   ```
   git checkout -b fix/<short-bug-name>
   ```

2. **Reproduce the bug first.** Run the test suite and read the actual
   failure output before touching any code:
   ```
   python3 -m unittest test_slugify.py -v
   ```

3. **Fix the implementation, not the test.** The tests describe the
   correct behavior. If a test looks wrong, that's a conversation to
   have — never edit a test just to make it pass.

4. **Make the smallest correct change.** Don't refactor unrelated code
   in the same commit.

5. **Run the full test suite again locally** before committing, to
   avoid wasting the reviewer's time — but your own local pass does
   NOT decide anything. The separate reviewer's run is what counts.

6. **Commit with a clear message** describing what was actually broken
   and what changed.

7. **Do not open a PR yourself.** Submit the branch for review. A PR is
   opened only if the reviewer returns `PASS`.
