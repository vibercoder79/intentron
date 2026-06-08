# Wave BZ — Integrate a new stack/linter: runbook + HANDBOOK chapter (BOO-178)

> 🌐 **Language:** English (this file) · [🇩🇪 Deutsch](wave-bz-stack-linter-runbook.md)

**What is now in place:** A documented, **verifiable** path to integrate a **non-covered stack** (e.g. TYPO3/PHP, Go) into the framework. Bootstrap knew `e) Other` with a linter hint table (BOO-116) + guided discovery (BOO-127), but no "how". Driven by a real field deployment (TYPO3/PHP). Deliberate design decision: **don't build every language into the framework** (bloat) — instead a guide whose guarantee comes from a **verification step**, not a prompt.

## Changes

- **Runbook `docs/runbooks/stack-linter-integrieren.md` (+ `.en`):** canonical linter path table (JS/TS, Python, **PHP**, Java/Kotlin, Go → linter · formatter · typecheck · coverage · gate config) + step-by-step along the **5 places**, plus:
  - **Mandatory bridge to BOO-176** — add the new gate-config files (e.g. `phpstan.neon`) to `.claude/sensitive-paths.json`, otherwise "only the operator moves the bar" doesn't cover the new stack.
  - **Verification step** (the central one): deliberately introduce a lint/type error → the gate must go **red** → remove it → green. Manual test, no prompt — this is where the guarantee comes from.
  - **Copy templates:** PHP/TYPO3 (PHPStan + `phpstan.yml` CI + PHPUnit coverage + sensitive-paths entry) and Go (golangci-lint).
  - **knowledge-onboarding hint** for external stack/version docs (e.g. TYPO3).
- **HANDBOOK chapter `8d-bis. Integrating a stack linter` (+ `.en`):** concept (why not every language is built in) + the 5 places with substance → points to the runbook.
- **Bootstrap `e)` path** (`bootstrap/SKILL.md` + `.en`): reference to the HANDBOOK chapter + runbook (pure reference sentence, **no** version bump).

## The 5 places

`environment.json tools_available` · CI workflow `.github/workflows/` · `.semgrep.yml` pack · coverage tool (wired to 6a-quart) · ADR in `docs/domain/adrs/` — plus the mandatory entry in `sensitive-paths.json`.

## Scope

- **No new skill** (stack integration too variable — PHPStan ≠ golangci ≠ ruff) and **no "prompt that ensures"** — the runbook IS the guide + prompt template, the guarantee is the verification step.
- Gate-config protection mechanics = sibling story **BOO-176** (here only the entry step). The runbook is a **living document** — more stacks later.
- Wave letter **bz** (by = doc index catch-up BOO-181).

## References

Spec: `specs/BOO-178.md`. Branch: `tobiaschschmidt/boo-178-docs-stack-linter-runbook`. Related: BOO-116/127 (bootstrap `e)` path), BOO-176 (gate-config protection), BOO-180 (doc DoD). Operator source: Tobias, TYPO3/PHP field deployment 2026-06-07.
