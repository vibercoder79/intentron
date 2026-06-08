# Release Notes - Wave Q Post-Install Verification

> 🌐 **Language:** English (this file) · [🇩🇪 Deutsch](wave-q-verification.md)

Status: 2026-05-28

## Purpose

Wave Q (BOO-79) answers the operator question "Framework installed — does everything actually work?". Both directions: an automated script `verify-setup.sh` + a manual checklist (HANDBUCH Appendix T). Resolves the long-parked **BOO-48 E2E smoke test** idea.

## Affected Stories

- BOO-79 — verify-setup.sh + HANDBUCH Appendix T + Bootstrap Phase 7.3b

## What Users Get

- **`bootstrap/references/verify-setup.sh`** (Bash, BSD+Linux, no dependencies, read-only): checks 6 groups and outputs PASS/WARN/FAIL —
  1. `.claude/environment.json` present + readable
  2. Toolchain reachable (`command -v` per `tools_available: true`; eslint via npx ok)
  3. Git hooks per repo (pre-commit, spec-gate, doc-version-sync)
  4. Core artifacts (CONVENTIONS.md, ARCHITECTURE_DESIGN.md, specs/, journal/)
  5. Privacy add-on (PRIVACY.md + personal-data-paths.json, if active)
  6. Backlog adapter
  Exit 1 on FAIL (CI-capable), `--strict` (WARN→FAIL), `--quiet`.
- **HANDBUCH Appendix T "Post-Install Verification"** (DE+EN): 7-point checklist, manual. **Check 5 (skill writes artifacts) is deliberately a manual `/implement` trial run** — the end-to-end proof that a shell script cannot deliver.
- **Bootstrap Phase 7.3b:** copies + calls `verify-setup.sh` before the final commit → the operator sees the proof immediately. bootstrap v3.31.0 → v3.32.0.

## When to Run

- directly after bootstrap (Phase 7.3b automatically)
- **after every `git clone`** on a new machine (hooks + environment.json are per repo/machine — see Appendix S)
- in CI as a gate (`--strict`)

## Concrete Changes

| Area | File |
|---|---|
| verify-setup.sh NEW | `bootstrap/references/verify-setup.sh` |
| HANDBUCH Appendix T (DE+EN) | `HANDBUCH.md` + `HANDBUCH.en.md` |
| Bootstrap Phase 7.3b (DE+EN), v3.32.0 | `bootstrap/SKILL.md` + `.en.md` |
| Migration | `migrate_boo_79` in `bootstrap/scripts/migrate-to-v2.sh` |
| Migration checklist §BOO-79 (DE+EN) | `bootstrap/references/migration-checklist-v1-to-v2.md` + `.en.md` |
| Spec | `specs/BOO-79.md` |

## Smoke Test (passed)

- Empty repo → 4 FAIL, Exit 1.
- Minimal complete project → 12 PASS, Exit 0.

## Skill Version Bumps

- `bootstrap` 3.31.0 → 3.32.0 (Phase 7.3b)

## References

- Spec: `specs/BOO-79.md`
- Script: `bootstrap/references/verify-setup.sh`
- HANDBUCH Appendix T, Bootstrap Phase 7.3b
- Resolves: BOO-48 (E2E smoke test)
- Operator question: Tobias, 2026-05-28
- Linear: BOO-79
