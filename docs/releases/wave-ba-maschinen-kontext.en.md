# Wave BA — Machine context at bootstrap (BOO-145)

**What's now in place:** at the end of **Block A** the bootstrap automatically writes a `## Machine context` section into the global `~/.claude/CLAUDE.md` — **idempotent** and **with no separate operator step**. Every AI session on the machine then has immediate orientation: OS type, framework version, preferred stack and available skills. The second machine-level building block alongside `PROJECTS_ROOT` (BOO-138). DE+EN.

## Stories

- **BOO-145** — Block A writes `## Machine context` (type via `uname -s`, framework `intentron <VERSION>`, stack preference from A.1, skills via `ls ~/.claude/skills/`), idempotent.

## Changes (DE+EN)

- **`bootstrap/SKILL.md`** (3.36.0 → **3.37.0**): new step **A.8 machine context** before the phase-1 checkpoint — idempotent write into `~/.claude/CLAUDE.md`, OS/version/stack/skills detection, section template.
- **`bootstrap/references/global-registry-update.md`**: new section "3b. Machine context" — read/write rule, idempotency, no secret, example.

All changes are DE+EN parity.

## Scope boundary

Pure bootstrap addition (Block A) + docs, no sketch. Builds on BOO-138 (`PROJECTS_ROOT`, `v0.8.0`).

## References

Spec: `specs/BOO-145.md`. Branch: `feat/boo-145-maschinen-kontext`. Builds on: BOO-138 (`PROJECTS_ROOT`), `global-registry-update.md`. Operator source: Tobias, 2026-06-04.
