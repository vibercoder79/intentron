# Wave BY — Doc index catch-up: missing runbooks in the central index (BOO-181)

> 🌐 **Language:** English (this file) · [🇩🇪 Deutsch](wave-by-doku-index-nachzug.md)

**What is now in place:** Two runbooks that were linked from the HANDBOOK but missing from the central document index `docs/INDEX.md` have been added — `unit-tests.md` (BOO-177) and `sprint-unattended-tmux.md` (BOO-172). Both predate the three-index rule from BOO-180 (doc DoD) and slipped through it. Retroactive compliance, found during the navigability check after the "quality-gate integrity" sprint.

## Changes

- **`docs/INDEX.md` + `.en.md`:** two rows each in the documentation table (alphabetically between "Sprint run" and "Vercel") — `sprint-unattended-tmux.md` and `unit-tests.md`, both DE+EN.
- **Artefact map checked:** `docs/onboarding/artefakt-landkarte.md` does not list runbooks in general (only `audit-perspective` as an audit artefact) → no addition needed.

## Scope

- Pure docs/index hygiene, no code. Follow-up compliance for BOO-177/BOO-172 under the doc DoD convention (BOO-180) — dogfoods the new rule.
- Wave letter **by** (bx = PR hygiene BOO-175).

## References

Spec: `specs/BOO-181.md`. Branch: `tobiaschschmidt/boo-181-docs-doku-index-nachzug`. Related: BOO-180 (doc DoD), BOO-177 (unit-tests runbook), BOO-172 (tmux runbook). Operator source: Tobias, 2026-06-08 (navigability question after sprint close).
