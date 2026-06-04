# Wave BG — "Framework update" runbook for existing projects (BOO-156)

**What's now in place:** a dedicated copy-paste runbook bundles the framework update of an existing project into one piece — update the bootstrap skill + run the `/bootstrap` upgrade (inspect → apply-safe → apply-with-confirmation). Linked from the README in EN + DE. Docs only. DE+EN.

## Stories
- **BOO-156** — new `docs/runbooks/framework-update.md` (+EN) + README link.

## Changes (DE+EN)
- **New `docs/runbooks/framework-update.md` / `.en.md`**: step 1 (update the bootstrap skill via sparse-checkout) + step 2 (`/bootstrap` detects the existing installation, mode prompt) incl. one-shot prompt, safety/idempotency, references. Structure mirrors `secondbrain-nachziehen.md`.
- **`README.md`**: runbook linked in the EN section "C) AI self-update for an old / brownfield install" and its DE counterpart.

## Effect
The question "is the framework-update path documented?" now has a single, complete guide instead of two halves to stitch together.

## Scope boundary
Docs only, no code, no skill, no sketch. Wave letter `bg` (bf = BOO-155). Builds on BOO-144 (runbook pattern) + BOO-155 (corrected upgrade docs).

## References
Spec: `specs/BOO-156.md`. Branch: `tobiaschschmidt/boo-156-docs-runbook-framework-updatemd-bestandsprojekt-auf`. Related: `docs/runbooks/secondbrain-nachziehen.md` (BOO-144). Operator source: Tobias, 2026-06-04.
