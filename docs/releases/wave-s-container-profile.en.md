# Release Notes - Wave S Optional Container Profile

> 🌐 **Language:** English (this file) · [🇩🇪 Deutsch](wave-s-container-profile.md)

Status: 2026-05-28

## Purpose

Wave S (BOO-81) gives the framework an **optional** container profile for the toolchain — for team setups that want an identical, reproducible toolchain. **System install stays the default** (INTENTRON lightweight principle); the container is opt-in.

## Background: the container decision

The operator (Tobias, 2026-05-28) wanted the tools/container setup clarified. Important clarification: **there was no prior container decision in the repo.** Made via AskUserQuestion: **system install as default, document the container as an optional profile** — not enforced.

## Affected Stories

- BOO-81 — optional devcontainer + Dockerfile template + HANDBUCH Appendix S container section

## What Users Get

- **`bootstrap/references/devcontainer/Dockerfile`** — lean Debian base (Node LTS + Python) with Semgrep, Ruff (via pipx), global ESLint, jq, git.
- **`bootstrap/references/devcontainer/devcontainer.json`** — VS Code/CLI dev container; `postCreateCommand` calls `generate-environment-json.sh` so the skills detect the container tools; extensions ESLint/Ruff/Claude Code.
- **`bootstrap/references/devcontainer/README.md`** — when to use (solo=no, team/CI=yes), usage, tradeoff.
- **HANDBUCH Appendix S section "Container Profile (optional)"** (DE+EN): system-install-vs-container table, opt-in decision.
- **`migrate_boo_81`** copies `.devcontainer/` into the project (opt-in, idempotent).

## Design Decision

System install stays the default. The container is **opt-in**, not a new mandatory bootstrap step. Pro: identical toolchain for everyone, CI-reusable. Con: Docker dependency, build time — overkill for solo operators.

## Concrete Changes

| Area | File |
|---|---|
| Container template NEW | `bootstrap/references/devcontainer/` (Dockerfile, devcontainer.json, README.md) |
| HANDBUCH Appendix S §Container Profile (DE+EN) | `HANDBUCH.md` + `HANDBUCH.en.md` |
| Migration | `migrate_boo_81` (opt-in) in `bootstrap/scripts/migrate-to-v2.sh` |
| Migration checklist §BOO-81 (DE+EN) | `bootstrap/references/migration-checklist-v1-to-v2.md` + `.en.md` |
| Spec | `specs/BOO-81.md` |

## Skill Version Bumps

- none (template + docs, no skill code change)

## References

- Spec: `specs/BOO-81.md`
- Template: `bootstrap/references/devcontainer/`
- HANDBUCH Appendix S §Container Profile
- Operator decision: Tobias, 2026-05-28
- Linear: BOO-81
