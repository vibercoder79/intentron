# Wave BD — Cross-session drift normalized + guard (BOO-153)

**What's now in place:** the **number/wave drift** caused by parallel sessions is cleanly documented and guarded against recurrence — **Option B** (operator decision): accept + document the offset instead of renaming merged code. DE+EN.

## Stories
- **BOO-153** — ADR `cross-session-drift` (mapping table repo↔Linear + wave duplicates), docs-drift **check 5** (wave-duplicate guard), PR-#48 mis-attachment removed, assignment convention.

## Changes (DE+EN)
- **New:** `docs/domain/adrs/cross-session-drift.md` (+ `.en.md`) — repo-spec↔Linear mapping (146–150 = +1 offset; aligned from 151), wave duplicates (`ba`/`bb`/`bc`), process guard, consequences.
- **`.github/scripts/docs_drift_check.py`:** check 5 — new doubly assigned wave letters → FAIL; old duplicates allowlisted. (Repo-internal gate, not shipped.)
- **Linear:** PR-#48 mis-attachment removed from BOO-146.

## Effect
The drift is now **traceably documented** (no hidden risk) and **future** drift is caught automatically: duplicate wave letters fail the docs-drift check, and BOO numbers + wave letters are checked against Linear / `docs/releases/` before assignment. This release itself uses the guard (wave **bd** = next free letter, checked).

## Scope boundary
Option A (full renumber) rejected — no touching of merged "Done" code. Pure docs/governance change, no runtime code.

## References
Spec: `specs/BOO-153.md`. Branch: `feat/boo-153-drift-normalisieren`. ADR: `docs/domain/adrs/cross-session-drift.md`. Operator source: Tobias, 2026-06-04.
