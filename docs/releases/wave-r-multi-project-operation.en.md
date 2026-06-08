# Release Notes - Wave R Multi-Project Operation

> 🌐 **Language:** English (this file) · [🇩🇪 Deutsch](wave-r-multi-project-operation.md)

Status: 2026-05-28

## Purpose

Wave R (BOO-80) answers "multiple projects on one machine — bootstrap per project, or is there a base-already-present path?". HANDBUCH Appendix U separates the machine level (once) from the project level (every time) and describes three onboarding paths. Pure docs + sketch.

## Affected Stories

- BOO-80 — HANDBUCH Appendix U Multi-Project Operation

## What Users Get

- **HANDBUCH Appendix U** (DE+EN) with sketch `docs/assets/multi-project-onboarding.png`:
  - **Machine level (once):** system tools, global skill pool, `~/.claude` — applies to all projects.
  - **Project level (every time):** CLAUDE.md, Git hooks (per repo!), environment.json, specs/, docs SSoT.
  - **Three onboarding paths:** (1) new project = full `/bootstrap`; (2) project 2..N = bootstrap fast path (Block B detects base → skip Phase 5, project level only); (3) existing project = bootstrap merge mode + `migrate-to-v2.sh` (no new skill).
  - **Per-project minimal checklist:** CLAUDE.md / Git hooks / environment.json / docs SSoT / verify-setup.sh.

## Design Decision

Existing-project onboarding stays a **documented path** (bootstrap merge mode + migrate-to-v2.sh), **no new skill** — the mechanics already exist, a skill would be duplication. This keeps the framework lightweight.

## Concrete Changes

| Area | File |
|---|---|
| HANDBUCH Appendix U (DE+EN) + sketch | `HANDBUCH.md` + `HANDBUCH.en.md`, `docs/assets/multi-project-onboarding.png` |
| Migration | `migrate_boo_80` (docs-only) in `bootstrap/scripts/migrate-to-v2.sh` |
| Migration checklist §BOO-80 (DE+EN) | `bootstrap/references/migration-checklist-v1-to-v2.md` + `.en.md` |
| Spec | `specs/BOO-80.md` |

## Skill Version Bumps

- none (pure docs)

## References

- Spec: `specs/BOO-80.md`
- HANDBUCH Appendix U, Appendix S (what once vs per project), Appendix T (verify)
- Operator question: Tobias, 2026-05-28
- Linear: BOO-80
