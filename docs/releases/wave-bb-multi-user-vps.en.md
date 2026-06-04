# Wave BB — Multi-user VPS + three-level collision protection (BOO-151)

**What's now in place:** the docs for **several people on one project on a shared VPS** are sharpened and consolidated — plus an explicit **three-level model** of how the framework prevents parallel work from overwriting itself. Clear separation: bootstrap setup ≠ development governance ≠ Git best practices. DE+EN + sketch.

## Stories

- **BOO-151** — multi-user VPS doc sharpening, team-member checklist (runbook), three-level collision-protection model, Appendix P §3 terminology fix, bootstrap A.7 sharpening, `journal/daily` `.gitignore` convention.

## The three levels (newly consolidated)

1. **Multi-USER** (several people, one project) → own clone per user home, sync via GitHub.
2. **Multi-SESSION** (one person, 2 sessions, one clone) → `git worktree` / session hint.
3. **Multi-AGENT** (one session, several sub-agents) → `EXECUTION_ISOLATION` (already exists, BOO-52).

## Changes (DE+EN)

- **New:** `docs/kollisionsschutz-drei-ebenen.md` (+ `.en.md`) — the three-level model in one place.
- **New:** `docs/runbooks/multi-user-vps.md` (+ `.en.md`) — team-member checklist (once VPS / once GitHub / once Claude / per repo) + sketch.
- **New:** sketch `docs/assets/multi-user-vps.{excalidraw,png}` (+ `.en.*`) — multi-user clone model, OWLIST, render loop, Read-verified.
- **`HANDBUCH.md` Appendix P §3:** step 7 — "clone" vs. "git worktree" cleanly separated + references.
- **`bootstrap/SKILL.md`** (3.38.0 → **3.39.0**): A.7 — solo lock hint (level 2) + multi-user VPS runbook reference + `journal/daily` `.gitignore` hint.
- **`bootstrap/references/file-templates.md`:** `.gitignore` template — commented `journal/daily/` line (enable for multi-user; solo keeps it committed).

All changes are DE+EN parity.

## Scope boundary

Multi-AGENT (level 3) is not part — already built (`EXECUTION_ISOLATION`, `implement` step 0c). Builds on BOO-138/139/145.

## References

Spec: `specs/BOO-151.md`. Branch: `feat/boo-151-multi-user-vps`. Builds on: HANDBUCH Appendix P §3 / U / Y, `docs/how-we-document.md`. Operator source: Tobias, 2026-06-04.
