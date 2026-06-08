# Wave Y — coverage-check.sh Single-Source + Drift Guard (BOO-89)

> 🌐 **Language:** English (this file) · [🇩🇪 Deutsch](wave-y-hook-single-source.md)

**Linear:** [BOO-89](https://linear.app/owlist/issue/BOO-89/) · Follow-up story from BOO-88

## Problem

`coverage-check.sh` was maintained **in triplicate**: as an inline body in `file-templates.md` (DE),
in `file-templates.en.md` (EN), and as an embedded heredoc in `migrate-to-v2.sh`
(`migrate_boo_15`). The BOO-88 bugfix therefore needed three synchronous edits — drift is only
a matter of time. Potentially applies to all scaffolded hooks.

## What Changes

- **Canonical source:** `bootstrap/references/hooks/coverage-check.sh` (v2, incl. BOO-88 fix) —
  **one** file instead of three copies.
- **Migration copies instead of embedding:** `migrate_boo_15` does a `cp` from the canonical
  file (no more `COVCHECK_EOF` heredoc). The v1→v2 replace with `.bak` stays unchanged.
- **Templates point to the source:** `file-templates.md` + `.en.md` contain, instead of the
  inline script, a pointer to `references/hooks/coverage-check.sh` (bootstrap renders
  verbatim from it).
- **Drift guard:** `bootstrap/scripts/check-hook-sources.sh` checks the single-source convention
  (canonical valid; not additionally embedded; freshly migrated == canonical) and lists
  the still-embedded hooks as follow-up candidates. Runs locally **and in CI**
  (`.github/workflows/hook-sources.yml`).

## Verified

- Fresh install + v1 replace + idempotency: the installed `coverage-check.sh` is byte-identical
  to the canonical source.
- Drift guard exit 0 on the current state; `bash -n` on all affected scripts.

## Design Decision

"Both" (operator choice): real single-source **plus** drift guard as a safety net.
First migration to `coverage-check.sh` (the story that bit us); the remaining
scaffolded hooks (spec-gate, dependency-check, pre-edit-bodyguard, …) are listed as
follow-up candidates and are pulled in incrementally.

## Note

`coverage-check.sh` still requires bash 4+ (`declare -A`, pre-existing since BOO-15).
bootstrap 3.33.0 → 3.34.0.
