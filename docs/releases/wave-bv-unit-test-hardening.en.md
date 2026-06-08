# Wave BV — Unit-test hardening: real tests, not just coverage (BOO-177)

> 🌐 **Language:** English (this file) · [🇩🇪 Deutsch](wave-bv-unit-test-hardening.md)

**What is now in place:** Placeholder tests no longer count as coverage. Until now, trivial/empty tests (`expect(true).toBe(true)`, empty body, `assert True`, unjustified `skip`/`xit`/`@pytest.mark.skip`) raised the coverage number without checking anything — nothing caught that. Sibling story to BOO-176: the same root problem "agent gamed the gate", here at the test level. Scope: **unit tests only**, not integration/E2E.

## Changes

- **Anti-placeholder check** — a new, targeted check on test files: `bootstrap/references/hooks/anti-placeholder-check.py` (AST for Python, heuristics for JS/TS, **not** a linter). Flags empty/trivial test bodies + unjustified skips. `--self-test`, warn by default, `--strict`/`STRICT=1` → hard fail (like `raw-pii-guard.py`).
- **Test-gate integration** — new step **6a-quint** in `implement/SKILL.md` (+ `.en`) right after the 6a-quart coverage run: changed test files (`git diff --cached`) are checked, findings → gate fail, documented in `meta.json` (`iterations.anti_placeholder` / `skipped_gates.anti_placeholder`). Operator override only via `override_audit` (BOO-176 discipline). Coverage = "enough tests", anti-placeholder = "real tests".
- **Explicit test block in the story template** — new section 7a (feature) / 5a (fix) in `ideation/references/story-template-feature.md` + `.en` and `story-template-fix.md` + `.en`: test cases (happy path + failure case) are defined when writing the story, with AC linkage and a placeholder ban.
- **Docs** — new HANDBUCH chapter `8c-bis. Unit tests` (+ `.en`); new runbook `docs/runbooks/unit-tests.md` (+ `.en`); audit linkage in `docs/runbooks/audit-perspective.md` (+ `.en`): test existence (JUnit XML) and test quality (anti-placeholder) as two separate audit proofs.
- **Migration** — `migrate_boo_177()` in `migrate-to-v2.sh` copies the check idempotently from the canonical source (`cp` + `cmp -s` skip, byte-identical — SSoT convention like BOO-89, no heredoc drift). Drift guard `check-hook-sources.sh` green.

## Scope

- **Unit tests ≠ integration tests** — integration/E2E is a separate topic NOT addressed here; **no** integration-test skill (and none shall be built).
- Anti-placeholder is **not** a linter concern (linters check style/types, not test meaningfulness) and **not** a new skill — `/implement` keeps the tests.
- Gate-config protection = sibling story **BOO-176** (merged, Wave BU).
- Wave letter **bv** (bu = quality-gate integrity BOO-176).

## References

Spec: `specs/BOO-177.md`. Branch: `tobiaschschmidt/boo-177-featdocs-unit-test-hartung`. Related: BOO-176 (quality-gate integrity, sibling), BOO-93 (`raw-pii-guard.py` precedent), BOO-89 (hook SSoT/drift guard), BOO-15 (coverage gate). Operator source: Tobias, TYPO3/PHP field deployment 2026-06-07.
