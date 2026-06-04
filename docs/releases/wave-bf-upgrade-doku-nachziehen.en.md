# Wave BF — Upgrade docs catch-up: misleading `/bootstrap --update` removed (BOO-155)

**What's now in place:** the entry-point docs for framework upgrades match the real mechanism again. The misleading `/bootstrap --update` command (a flag that never existed) is gone; `framework-upgrade.md` now lists the new required artifacts and the `migrate-to-v2.sh` path. Docs only, no runtime code. DE+EN.

## Stories
- **BOO-155** — fixed the HANDBUCH FAQ (`/bootstrap` instead of `/bootstrap --update`) + extended `framework-upgrade.md` with artifact / migrate / provider references.

## Changes (DE+EN)
- **`HANDBUCH.md` / `.en.md`** (FAQ "How do I update skills"): `/bootstrap --update` → `/bootstrap`; the comment explains auto-detection of the existing installation + mode prompt (inspect / apply-safe / apply-with-confirmation), referencing `framework-upgrade.md`.
- **`bootstrap/references/framework-upgrade.md` / `.en.md`**:
  - "File categories" table extended with `CONTEXT.md`, `solution-artefakte.md`, `DEVELOPER_ONBOARDING.md`, `.claude/environment.json` (+ generator) and `docs/kollisionsschutz-drei-ebenen.md`.
  - User flow anchors `bash bootstrap/scripts/migrate-to-v2.sh --issue BOO-NN` as the idempotent existing-project migration path.
  - Provider postflight step links `bootstrap/references/provider-postflight.md`.

## Effect
Anyone pulling an existing project up to the current framework state now follows instructions that match actual skill behavior: `/bootstrap` in the project → auto-detection → mode prompt. No dead commands, no missing artifacts.

## Scope boundary
No real `--update` flag built (remove instead of build — §7.5a covers it). `bootstrap/README.md` version header ("Version 3.0") deliberately left as-is (major label, gate-irrelevant). No migration-script code changed.

## References
Spec: `specs/BOO-155.md`. Branch: `tobiaschschmidt/boo-155-docs-upgrade-doku-nachziehen-irrefuhrendes-bootstrap-update`. Builds on: BOO-60 (upgrade mode §7.5a), BOO-91/108/138/139 (the caught-up artifacts). Operator source: Tobias, 2026-06-04.
