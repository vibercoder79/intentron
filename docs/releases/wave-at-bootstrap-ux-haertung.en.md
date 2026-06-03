# Wave AT — Bootstrap UX hardening (BOO-114/115/117/120/123/127)

**What's now there:** the bootstrap flow checks prerequisites *up front* (instead of at the end), guides you to the right install instructions per profile when tools are missing, is stack-/framework-/TypeScript-aware, and anchors `gh` (GitHub CLI) as a clean prerequisite with a connect runbook. First bundle of the post-trial follow-up stories (BKO, 2026-06-02).

## Stories
- **BOO-114** — Phase-0 **pre-flight gate** with a controlled abort (prerequisite check before any scaffold).
- **BOO-115** — **Tool-install guidance** with HANDBUCH deeplinks + **profile-dependent install default** (system vs. Docker from `deployment_scenario`).
- **BOO-117** — Block-A **existing-source import** (intent/repo/docs → pre-fill `PROJECT_DESC`).
- **BOO-120** — `intent` into the **Minimum** skill set (pipeline entry) + `migrate_boo_120`.
- **BOO-123** — `gh` as a **prerequisite** (HANDBUCH §3/Appendix A) + **golden image** (Dockerfile) + **GitHub-connect runbook** (gh-auth ≠ git-auth) + branch-protection fallback.
- **BOO-127** — **Guided stack discovery** + framework-aware stack options + **TypeScript-first** (`tsconfig`, `typescript-eslint`, `tsc --noEmit` gate).

## Changes (DE+EN)
- **`bootstrap/SKILL.md`:** Phase 0 → `0.1 briefing` + `0.2 pre-flight gate`; A.1 framework-aware + TS choice + `A.1a guided discovery`; new `A.2b existing-source import`; A.7 derives `INSTALL_DEFAULT`; phase 7.3b tool-install guidance; 4.4 TS branch + typecheck gate; 4.4k branch-protection fallback + Sonar decoupling; skill selection: `intent` in Minimum; 7.6 proactive GitHub connect.
- **`HANDBUCH.md`:** §3 `gh` in the required list + two-auth-layers callout; Appendix A `gh` checklist; Appendix Y.2 `gh` apt-repo block + GitHub-connect runbook; §6 Minimum set (+ `intent`).
- **`references/`:** `file-templates.md` (+ `tsconfig.json` + `tsc --noEmit` typecheck), `info-gathering.md` (`SOURCE_IMPORT`), `skills-setup.md` (`intent` = Minimum), `migration-checklist-v1-to-v2.md` (`migrate_boo_120`).
- **`bootstrap/references/devcontainer/Dockerfile`:** `gh` via the official GitHub apt repo (golden image).

## Lightweight principle
No content duplication: BOO-115 deeplinks to the existing HANDBUCH anchors (Y.2 / container profile) instead of copying install sequences. BOO-127 keeps the `a–e` letter mapping → no regression in the STACK_CHOICE follow-on phases.

## References
Specs: `specs/BOO-114.md`, `BOO-115.md`, `BOO-117.md`, `BOO-120.md`, `BOO-123.md`, `BOO-127.md`. Merged via PR #36.
