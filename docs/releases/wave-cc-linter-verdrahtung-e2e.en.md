# Wave CC — Linter wiring end-to-end: central picture + sketch (BOO-182)

> 🌐 **Language:** English (this file) · [🇩🇪 Deutsch](wave-cc-linter-verdrahtung-e2e.md)

**What is now in place:** **One** picture of the **whole** linter chain — `control file → trigger (hook/CI) → linter → gate → report persistence → /sprint-review` — for **both linters** (ESLint JS/TS, Semgrep/SAST) and **both layers** (local pre-commit hook, CI workflow). The wiring was fully present but scattered across many detail spots (HANDBUCH 8/8d/8d-bis, implement/README, runbook, security template, artifact map). The new HANDBUCH chapter `8d-quart` bundles those spots and answers the one question no single spot answers: **how do the local pre-commit hook and the CI workflow share the same config-reader logic, and where do the reports land?**

## Changes

- **HANDBUCH chapter `8d-quart` "How the linter wiring fits together (end-to-end)" (+ `.en`):** the whole chain in one picture, with the ground truth:
  - `.semgrep.yml` (manifest) and `eslint.config.mjs` (flat config) are read by the **same** bash reader — in the local pre-commit hook **and** in the CI workflow.
  - Gates block via **required status checks** (BOO-29); CI also catches `git commit --no-verify`.
  - Manifest subtlety: `semgrep --config=.semgrep.yml` deliberately reports "No config given" (manifest, not a native config) — expected behavior.
- **Sketch `docs/linter-verdrahtung-e2e.*` (+ `.en`, OWLIST colors):** visual chain, embedded in the chapter.
- **Cross-links** from the runbook (`stack-linter-integrieren`), `implement/README`, security template, artifact map, and HANDBUCH 8/8d/8d-bis to the new chapter — one short reference sentence each.
- **Report-persistence correction:** there are **two streams**, not one:
  - **local (BOO-36):** `/implement` writes directly to `journal/reports/local/...`.
  - **CI (BOO-32):** an aggregator copies `.ci-reports/*.sarif` → `journal/reports/ci/run-{id}/`.
  - Both are consumed by `/sprint-review`. The earlier shorthand "`.ci-reports → journal/reports/local`" was inaccurate and is corrected.

## The chain

`control file (.semgrep.yml / eslint.config.mjs)` → `trigger (pre-commit hook · CI workflow)` → `linter (Semgrep · ESLint)` → `gate (required status check, BOO-29)` → `report persistence (local BOO-36 · CI BOO-32)` → `/sprint-review`.

## Scope

- **Docs only** — no linter, config, hook, or workflow change.
- New stacks/linters stay in runbook **BOO-178** (linked only). Gate-config protection mechanics stay **BOO-176** (referenced only).
- Codex `.codex/hooks.json` is a known limit (only named in artifact lists, no schema/example in the repo) — the chapter does not present it as finished.
- No standalone explainer artifact → no new `docs/INDEX.md` entry (pure HANDBUCH chapter).
- Wave letter **cc**.

## References

Spec: `specs/BOO-182.md`. Branch: `tobiaschschmidt/boo-182-docs-zentrales-end-to-end-bild-der-linter-verdrahtung`. Related: BOO-174 (EN parity of legacy waves), BOO-176 (gate-config protection), BOO-178 (stack-linter runbook), BOO-180 (doc DoD).
