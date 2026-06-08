# Release Notes - Wave P README Update + Toolchain Doc

> 🌐 **Language:** English (this file) · [🇩🇪 Deutsch](wave-p-readme-and-toolchain-doc.md)

Status: 2026-05-28

## Purpose

Wave P (BOO-78) is a documentation-correction wave: the README was no longer up to date after Waves J-O, and the recurring toolchain question ("do I have to install linters/tools/hooks per project or once?") had no documented place.

## Affected Stories

- BOO-78 — README v0.2.0 state + Appendix S toolchain section

## What Was Corrected

### README (EN+DE)

- **`dpo` + `security-architect` listed as framework bundle skills** (own table "Specialist bundle skills", vendored since BOO-74) — previously `dpo` was missing entirely and `security-architect` was wrongly listed as an external companion skill (`../security-architect/`).
- **HANDBUCH description updated:** split into `HANDBUCH.md` (DE, ~190 KB) + `HANDBUCH.en.md` (EN, ~165 KB), appendices A-S named (previously "bilingual, ~95 KB").
- **"What's new (v0.2.0)" reference** to `docs/releases/v0.2.0-overview.md`.
- **Governance gates list extended:** sensitive-paths (BOO-18), personal-data-paths (BOO-69), post-merge vault harvest (BOO-77) — previously only spec-gate + doc-version-sync.
- **"Operating at scale / In a team" hint** to appendices P/Q/R/S/O.

### HANDBUCH Appendix S — new section "What to install once, what per project?"

Answers the toolchain question with a matrix:

| Component | Once | Per project |
|---|---|---|
| System linters/tools (Semgrep, Ruff, global ESLint) | ✅ once per machine | — |
| Project dev deps (eslint/prettier in package.json) | — | ✅ npm install per project |
| Skills (global pool) | ✅ once | only on audit pinning |
| **Git hooks** (spec-gate, doc-version-sync, post-merge) | ❌ | ✅ **per repo** (`.git/hooks/` is not cloned) |
| environment.json | — | ✅ per project (manifest) |

**Core correction:** Git hooks are **per repo**, not once — `.git/` is not cloned. Bootstrap installs them per project; exception `core.hooksPath` global.

## Concrete Changes

| Area | File |
|---|---|
| README EN+DE | `README.md` |
| HANDBUCH Appendix S toolchain section (DE+EN) | `HANDBUCH.md` + `HANDBUCH.en.md` |
| Spec | `specs/BOO-78.md` |

## Skill Version Bumps

- none (pure documentation, no skill code change)

## Still Open / Follow-ups (from the 2026-05-28 discussion)

Operator topics queued up as own stories:

- **Multi-project onboarding:** how to set up a second/third project on a machine when the base (tools, skills) is already installed — lightweight per-project path vs. full bootstrap. Needs doc + sketch.
- **Project verification checklist:** "framework installed — now the proof that everything works" (linter present, hooks fire, skills write artifacts, artifacts exist). Doc checklist + possibly an automating skill.
- **Existing-project onboarding skill:** prepare an existing project for INTENTRON.
- **Tools/container setup:** how the toolchain is concretely integrated (clarify container decision).

## References

- Spec: `specs/BOO-78.md`
- README, HANDBUCH Appendix S
- Consolidated overview: `docs/releases/v0.2.0-overview.md`
- Operator observation: Tobias, 2026-05-28
- Linear: BOO-78
