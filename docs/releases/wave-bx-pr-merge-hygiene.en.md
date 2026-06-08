# Wave BX — PR & merge hygiene: guard against duplicate PRs (BOO-175)

> 🌐 **Language:** English (this file) · [🇩🇪 Deutsch](wave-bx-pr-merge-hygiene.md)

**What is now in place:** A convention that prevents the BOO-172 double-merge from recurring. The release audit (BOO-173) found that **BOO-172 was merged to `main` via two PRs**. This story clarifies the root cause and establishes two guards.

## Analysis (read-only)

- **#69** (2026-06-07 08:32, title *"docs: Runbook … (BOO-172)"* — clean BOO number) and **#70** (09:32, generic title *"Feat/boo 172 runbook tmux vps"*) came from the **same** branch `feat/boo-172-runbook-tmux-vps`.
- **Root cause:** After #69 merged, more commits (incl. `sprint-run/README.md`/`.en`) were pushed to the **same** branch and merged as a second PR #70. #70 was a superset of #69.
- **`main` is complete** — both PRs are merged, no content lost (verified: the `sprint-run/README` changes that were only in #70 are on `main`). The problem was pure PR hygiene, not a content defect. **No** history rewrite.

## Changes

- **"PR & merge hygiene" convention in `CONVENTIONS.md` §3** (EN and DE block): *One issue → one PR → one merge.* Two guards:
  1. **Check for an existing PR before `gh pr create`** (`gh pr list --head <branch> --state all`) — no second PR per branch; if the PR was already merged, branch fresh from `main`.
  2. **The PR title must contain the issue number (`BOO-NNN`)** — generic branch titles can link the wrong/no Linear issue on merge (Linear-first, BOO-154).
  Plus a note to delete the feature branch after merge.
- **Branch cleanup:** the orphaned, fully merged branch `feat/boo-172-runbook-tmux-vps` deleted on the remote.

## Scope

- **Read-only analysis first, no revert, no history rewrite** on `main` — both contents are correctly present.
- Pure docs/convention + branch cleanup. An enforcing wrapper script (`gh pr create` guard) remains an optional follow-up — the convention is operator discipline.
- Wave letter **bx** (bw = doc DoD BOO-180).

## References

Spec: `specs/BOO-175.md`. Branch: `tobiaschschmidt/boo-175-chore-doppel-merge-guard`. Related: BOO-172 (double merge), BOO-173 (release audit, found it), BOO-154 (Linear-first), BOO-180 (doc DoD — this story follows it). Operator source: Tobias, 2026-06-07.
