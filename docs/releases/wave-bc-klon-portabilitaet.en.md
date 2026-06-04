# Wave BC — Clone portability for multi-user (BOO-152)

**What's now in place:** a bootstrapped project is **clone-portable** — the prerequisite for the multi-user VPS scenario (BOO-151) to work technically. Previously `settings.json` + hook scripts carried **absolute paths**; a foreign clone inherited the creator's paths and the hooks ran into the void. Now: paths via **`$CLAUDE_PROJECT_DIR`** (portable) + an **`install-hooks.sh`** for the native `pre-commit` + a ready onboarding prompt. DE+EN.

## Stories
- **BOO-152** — clone portability: `$CLAUDE_PROJECT_DIR` in settings.json + hook scripts, `scripts/install-hooks.sh` (`.githooks/` + `core.hooksPath`), onboarding prompt, checklist update.

## Changes (DE+EN)
- **`bootstrap/SKILL.md`** (3.39.0 → **3.40.0**): settings.json hook commands → `$CLAUDE_PROJECT_DIR`; phase 4.6 native `pre-commit` → `.githooks/` + `install-hooks.sh`.
- **`references/file-templates.md`:** `WORKSPACE` portable (`${CLAUDE_PROJECT_DIR:-…}`); new section `scripts/install-hooks.sh`.
- **`docs/runbooks/multi-user-vps.md`:** ready operator prompt for self-setup (steps C+D).
- **HANDBUCH Appendix U + Y:** per-project checklist hook step = `install-hooks.sh`.

All changes are DE+EN parity.

## Effect
A new team member now sets up their clone with **one** command (`bash scripts/install-hooks.sh`), and the committed `settings.json` works unchanged in **every** home — no path rewrite needed. This makes the BOO-151 multi-user docs technically sound.

## Scope boundary
Runtime hooks (`spec-gate`, `bodyguard`, …) already come with the clone via `$CLAUDE_PROJECT_DIR` + committed `.claude/`. `install-hooks.sh` only activates the native `pre-commit`.

## References
Spec: `specs/BOO-152.md`. Branch: `feat/boo-152-klon-portabilitaet`. Builds on: BOO-151 (multi-user VPS), `docs/kollisionsschutz-drei-ebenen.md`. Operator source: Tobias, 2026-06-04.
