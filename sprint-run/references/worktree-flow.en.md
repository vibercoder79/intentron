# Worktree Flow — one worktree per story

Reference for `/sprint-run` step 4.2 / 4.6. Each story runs in its own `git worktree`
with its own branch — this is how the sprint isolates the stories from each other (collision protection level 2,
`docs/kollisionsschutz-drei-ebenen.md`).

## Why worktree instead of branch switching?

- **Isolation:** Each story has its own working tree — no `git checkout` back-and-forth,
  no accidental mixing of changes.
- **Parallel-capable:** With `parallel_story_limit > 1` multiple stories can run simultaneously in
  disjoint worktrees (disjoint `write_scopes` assumed).
- **Clean `main`:** The main working tree stays untouched until a merge.

## Flow per story

```bash
# 4.2 — create (own branch per story)
git worktree add ../wt-BOO-<n> -b feat/boo-<n>-<slug>

# 4.3–4.5 — in the worktree: /implement (daemon) + remote CI wait
cd ../wt-BOO-<n>
# ... /implement runs here, pushes the branch, waits for green CI ...

# 4.6 — merge ONLY on green CI, then clean up
cd <repo-root>
git merge --no-ff feat/boo-<n>-<slug>      # or PR merge via gh
git worktree remove ../wt-BOO-<n>
git branch -d feat/boo-<n>-<slug>          # after successful merge
```

## Rules

- **Branch naming:** `feat/boo-<n>-<slug>` (or the `gitBranchName` suggested by Linear).
- **Merge gate:** no merge without green remote CI (BOO-148).
- **Cleanup is mandatory:** after merge `git worktree remove` + delete branch. Orphaned
  worktrees block later runs.
- **On error:** remove the worktree per `daemon_fail_policy` (or keep it for diagnosis and
  note it in the sprint report).
- **Dirty `main`:** never merge when the main tree is not clean — STOP.

## Three levels of collision protection (classification)

- **Level 1 — Multi-User:** own clone per person.
- **Level 2 — Multi-Session:** `git worktree` per session/story ← *this is where `/sprint-run` acts*.
- **Level 3 — Multi-Agent:** execution isolation + disjoint write scopes (`/implement` step 0c).

Sketch: `docs/story-breakdown.png` + `docs/github-integration.png` (HANDBUCH Appendix AD).
