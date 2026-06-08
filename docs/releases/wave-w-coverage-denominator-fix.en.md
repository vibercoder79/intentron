# Release Notes - Wave W Coverage Hook Denominator Fix

> 🌐 **Language:** English (this file) · [🇩🇪 Deutsch](wave-w-coverage-denominator-fix.md)

Status: 2026-05-31

## Purpose

Wave W (BOO-88) fixes a counting bug in the diff coverage gate `coverage-check.sh` (layer from BOO-15). The denominator of the coverage ratio previously counted **all** added lines — including comments and blank lines. As a result the ratio came out too low and the gate blocked falsely. The fix now derives the denominator only from **executable statement lines**.

## Why

Field feedback from the project **privacy-proxy** (PP-001): a commit with well-documented, tested code was rejected by the coverage gate. The cause was the naive denominator — it counted every added line as a "line to be covered", including comments and blank lines that a coverage tool cannot cover at all.

Example: 8 executable lines, all tested, plus 4 comment and 2 blank lines in the same diff → naive denominator 14, numerator 8 → **57%** → gate blocks at threshold 60%. The actual diff coverage was **100%**. Whoever commented more cleanly was punished — a perverse incentive directly against the framework's AI-suitability goals.

## The Bug

The counting loop in the hook took every `+` line from the staged diff as a denominator candidate. Comment and blank lines thus landed in the denominator even though they can never be marked as "covered". Consequence: systematically too-low ratio, proportional to the comment density of the diff.

## The Fix

- **Denominator = executable statement lines.** The set of countable lines now comes directly from the coverage report:
  - **Node (c8):** from the `statementMap` of the JSON report.
  - **Python (pytest-cov):** from `executed_lines ∪ missing_lines`.
- **New functions `parse_statement_lines_*`** extract these sets per file.
- **`continue` guard** in the counting loop: added lines not in the statement set (comments, blank lines, closing brackets) are skipped — they count in neither numerator nor denominator.
- **NO regex** for comment detection — the statement sets come from the coverage tool itself. This keeps the hook **dependency-free** (only `bash` + `python3` stdlib) and language-correct (no fragile pattern matching per language).

Verified: 8 code + 4 comment + 2 blank lines → **100%** (previously 57%); 6 of 8 executable lines tested → **75%**.

## Concrete Changes

The fix is mirrored at **three source locations** (single-source principle not yet achieved — see follow-up topics):

| Area | File |
|---|---|
| Template DE | `bootstrap/references/file-templates.md` §coverage-check.sh (v2, BOO-88) |
| Template EN | `bootstrap/references/file-templates.en.md` §coverage-check.sh (v2, BOO-88) |
| Migration | Heredoc in `migrate_boo_15` in `bootstrap/scripts/migrate-to-v2.sh` |
| Migration checklist §BOO-88 (DE+EN) | `bootstrap/references/migration-checklist-v1-to-v2.md` + `.en.md` |

- **Version marker:** the script now carries `# coverage-check v2`. By this the migration recognizes an old v1 (missing marker).
- **Replacing migration with `.bak`:** `migrate_boo_15` no longer only creates the file when absent, but detects an old v1, backs it up to `.claude/hooks/coverage-check.sh.bak`, and writes the v2. Idempotent — an existing v2 is skipped (`[SKIP]`).

## Migration

`bash bootstrap/scripts/migrate-to-v2.sh --issue BOO-15`

- The fix is delivered **via the BOO-15 coverage installer** — there is **no** separate `--issue BOO-88`.
- **Existing installs must re-migrate:** projects that already had BOO-15 otherwise keep the buggy v1. `migrate_boo_15` now replaces v1 (instead of only creating it when the file is missing), backs up to `.bak`, and writes v2.
- Verification: `bash -n .claude/hooks/coverage-check.sh` (Exit 0); `grep 'coverage-check v2' .claude/hooks/coverage-check.sh` (marker present). Rollback: `mv .claude/hooks/coverage-check.sh.bak .claude/hooks/coverage-check.sh`.

## Skill Version Bumps

- none (hook template + migration + docs, no skill code change). Pure bugfix — thresholds and `/implement` workflow unchanged.

## Follow-up Topics

- **DRY / single-source:** the hook body currently lives in triplicate (template DE, template EN, migration heredoc). A bugfix must be mirrored in three places — error-prone. Follow-up topic: a canonical source from which templates and migration are generated.
- **Contribute-back loop:** the bug came from the field (privacy-proxy / PP-001). Follow-up topic: a formal path through which project findings flow back into the framework backlog in a structured way.

## References

- Migration checklist: `bootstrap/references/migration-checklist-v1-to-v2.md` §BOO-88 (+ `.en.md`)
- Canonical templates: `bootstrap/references/file-templates.md` §coverage-check.sh (v2, BOO-88)
- Migration: `migrate_boo_15` in `bootstrap/scripts/migrate-to-v2.sh`
- Field feedback: privacy-proxy / PP-001
- Linear: BOO-88
