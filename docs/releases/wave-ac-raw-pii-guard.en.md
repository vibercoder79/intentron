# Wave AC — Raw-PII-in-Logs-Guard (BOO-93)

> 🌐 **Language:** English (this file) · [🇩🇪 Deutsch](wave-ac-raw-pii-guard.md)

**Linear:** [BOO-93](https://linear.app/owlist/issue/BOO-93/) · Source: upstream contribution privacy-proxy / PP-004 (Martin), 2026-05-31 — pattern rebuilt, **no PolyForm code adopted**

## Problem

Plaintext PII that accidentally ends up in logs (`logger.info("…", original_value=user.email)`)
is a de facto data leak (GDPR Art. 5 data minimization / Art. 32 security of processing):
logs are stored, sent to monitoring, read broadly, and rarely deleted. For the
regulated target group (CH banks/insurers) this is audit-relevant. Until now, PII-in-logs fell through
**all** layers: the Layer-0 bodyguard (BOO-86) covers secrets/eval/TLS/SQL, **not**
log sinks; the dpo skill (BOO-87) only provides review/doc guidance, no enforcement. The
expansion stage "bodyguard warning in PII paths" was only noted as an idea in `v0.5.0-overview`.

## What changes

- **Canonical guard `bootstrap/references/hooks/raw-pii-guard.py`** (single source) — a
  static **AST** check (python3 stdlib `ast`, no regex, no Semgrep):
  - Detects log/audit sinks (`log.*`, `logger.*`, `audit.*`, `logging.*`, also
    `self.audit_log.*`) via the function root name including attribute chains.
  - Reports forbidden **keyword arguments, attribute reads, and variable names**
    (`original_value`, `plaintext`, `raw_value`, `cleartext`, `decrypted`, `unmasked` …).
  - **Default blocklist** deliberately specific raw/plaintext markers — **no** generic
    field names like `email` (false-positive avoidance). AST ignores comments/strings → barely any
    false positives.
  - CLI: `[--strict] [--config PATH] [FILE …]`; without FILE the staged `*.py` are checked.
    Built-in `--self-test`. Unparseable files (SyntaxError) are skipped.
- **Default = warning** (Exit 0), hard block via `--strict` / `STRICT=1` / `RAW_PII_STRICT=1`
  (Exit 1) — consistent with BOO-86 against alarm fatigue.
- **Project overlay** `.claude/raw-pii-guard.local` (one line per entry, `#` comments,
  prefix `sink:` for additional sinks) — base-plus-overlay pattern analogous to BOO-86/BOO-87/BOO-91.
- **Opt-in scaffolding:** `migrate_boo_93()` copies the canonical source byte-identically to
  `.claude/hooks/` (idempotent, skip on byte equality), with a `log_manual` hint for
  wiring; `ALL_ISSUES` registration.
- **Docs** in `hooks-setup.md` (DE) + `hooks-setup.en.md` (EN): new section
  "Optional: raw-pii-guard.py" — what it does, activation, local pre-commit usage,
  overlay config, **optional CI workflow** `raw-pii-guard.yml` (opt-in), cross-reference dpo.
- **dpo cross-reference** in `dpo/references/privacy-patterns.md`: the guard is the optional
  automatic enforcement layer to the existing PII-in-logs review guidance.

## Design decision

- **Pattern rebuilt from PP-004, no code adopted** (hard constraint).
- **Engine = AST** instead of regex: more precise on log sinks (ignores comments/strings); deliberate
  introduction of the first AST tool in the repo (operator decision 2026-06-01).
- **Opt-in / warn default** instead of mandatory hard fail — so nothing tips toward heavyweight.
- **Single-source by construction:** the guard exists exactly **once** (canonically under
  `bootstrap/references/hooks/`) and is copied verbatim by the migration — no drift risk.
  Hooked into the existing hook/migration convention, **not** as a loose `ci/` package.
- **Dependency-free:** only python3 stdlib (`ast`).

## Verified

- `--self-test`: bad snippet yields exactly 3 hits (kwarg + attr + name), good snippet 0
  (comment/string/non-sink ignored).
- External tests: `logger.info("x", original_value=user.email)` and
  `self.audit_log.write(record.plaintext)` are detected; comment `# original_value` and string
  `"raw_value"` not; safe call `logger.info(..., user_id=user.id)` not.
- `--strict` → Exit 1 on hit; default → Exit 0 (warning).
- Overlay `.claude/raw-pii-guard.local` (additional field + `sink:`) takes effect.
- `migrate_boo_93` copies byte-identically (`cmp -s`), is idempotent (second run = skip),
  the scaffolded guard is executable.
- DE/EN scaffolding equivalent; `bash -n` for migration; `git diff --check` clean.

## Rollout

Additive and **opt-in**. Existing and new projects deliberately activate the guard via
`migrate-to-v2.sh --issue BOO-93` (copies the canonical source) and wire it into pre-commit
and/or CI. Default = warning; `--strict` for hard block. Projects without PII leave it inactive —
no effect on existing pipelines.

## Effect

The classic "raw value accidentally logged" error has, for the first time, an automatic, optional
guardian — audit-relevant for regulated projects, simply inactive for PII-free projects.

## References

- Spec: `specs/BOO-93.md`
- Release overview: `docs/releases/v0.6.0-overview.md` (Wave AC)
- Canonical guard: `bootstrap/references/hooks/raw-pii-guard.py`
- Migration: `migrate_boo_93()` in `bootstrap/scripts/migrate-to-v2.sh`
- dpo cross-reference: `dpo/references/privacy-patterns.md`
- Linear: BOO-93
