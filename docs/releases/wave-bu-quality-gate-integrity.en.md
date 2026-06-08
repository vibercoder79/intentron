# Wave BU — Quality-gate integrity: the agent cannot lower the bar itself (BOO-176)

> 🌐 **Language:** English (this file) · [🇩🇪 Deutsch](wave-bu-quality-gate-integrity.md)

**What is now in place:** An AI agent can no longer lower the quality bar by itself. Trigger was a real field deployment (TYPO3/PHP, 2026-06-07): an agent softens gates — drops the PHPStan level, lowers the coverage threshold, disables linter rules — instead of fixing the code, and sells it as "pragmatic". Guiding principle now anchored: **only the operator moves the bar, never the agent as a workaround. Fix the code ✅, soften the gate ❌.** Lightweight applies to the process, not to the code-quality threshold.

## Changes

- **Gate configs under bodyguard protection** — the gate-config files (`eslint.config.*`, `.eslintrc*`, `ruff.toml`, `pyproject.toml`, `.semgrep.yml/.yaml`, `phpstan.neon(.dist)`, `.coveragerc`, `jest.config.*`, `vitest.config.*`, `sonar-project.properties`) are now in the `.claude/sensitive-paths.json` default. Any change triggers a gate-block pause requiring operator sign-off. (`bootstrap/references/file-templates.md` + `.en`, `hooks-setup.md` + `.en`.)
- **New bodyguard pattern `gate-configs.yml`** (Layer 0, always loaded) — flags rule-disabling at write time: file-/block-wide `eslint-disable`, `@ts-nocheck`, bare `# noqa` / `# type: ignore`, module-wide test skips, plus edits to threshold lines (`level:`, `fail_under`, `coverageThreshold`). Warn level (with `BODYGUARD_STRICT=1` → block).
- **Post-story gate assertion extended** (`sprint-run/references/gate-assertion.md` + `.en`) with two deterministic checks against the story diff:
  - **AC3a — gate-config diff:** a lowered threshold / disabled rule (old→new comparison) **without** a documented `override_audit` entry → **Fail**.
  - **AC3b — change_type plausibility:** `change_type` set to non-code (`workflow|config|infrastructure|content`) but the diff contains real app code → **Fail** (code gates may not be bypassed via a false `change_type`).
- **Governance docs** — principle "only the operator moves the bar" in `CONVENTIONS.md` (DE+EN block); new chapter `change_type: when code checks are legitimately skipped` in `HANDBUCH.md` + `.en` (operator view: what `change_type` is, who sets it, how the two locks prevent abuse).
- **Migration** — `migrate_boo_176()` in `migrate-to-v2.sh` retrofits existing projects idempotently (add gate-config paths to `sensitive-paths.json` + install `gate-configs.yml`, `.bak` backup, non-destructive). The pattern template is **byte-identical** to the canonical source in `file-templates.md` (SSoT).

## Scope

- **Stack-agnostic** concept; the covered gate-config paths (JS/TS/Python/PHP) are provided by the framework, non-covered stacks add their paths via the stack runbook (BOO-178).
- **Deterministic** — hooks/assertion/diff comparison, no prompt.
- Test quality (empty/placeholder tests) = sibling story **BOO-177**; non-covered stack paths = **BOO-178**.
- Wave letter **bu** (bt = release index BOO-173).

## References

Spec: `specs/BOO-176.md`. Branch: `tobiaschschmidt/boo-176-feat-quality-gate-integritat`. Related: BOO-86 (Layer-0 bodyguard), BOO-165 (post-story gate assertion), BOO-68 (change_type / non-code flow), BOO-177/178. Operator source: Tobias, TYPO3/PHP field deployment 2026-06-07.
