# Release Notes - Wave V Layer-0 Edit Bodyguard

> 🌐 **Language:** English (this file) · [🇩🇪 Deutsch](wave-v-layer0-bodyguard.md)

Status: 2026-05-31

## Purpose

Wave V (BOO-86) gives the framework a new **Layer 0**: a Claude Code PreToolUse hook on `Edit|Write|MultiEdit` that catches unsafe patterns (secrets, `eval`, disabled TLS check, SQL concatenation) **before** the AI writes them to disk. Sibling hook to `spec-gate.sh` (which fires on `Bash`/`git commit`). This anchors security **from generation** instead of only from commit.

## Why

Today, linters check only **after** implementation (Layer 2: CLI linter before commit) or in CI (Layer 3). The **generation gap** — the moment when unsafe code first comes into being — stayed open. But Schrader's core is "secure from generation", not "secure from commit". An already-written secret must be detected, removed, and possibly rotated — costly rollback compared to "never come into being at all". The bodyguard sits in front of the AI's write operation and blocks/warns before the pattern lands on disk. That is the USP "security from generation".

## Design Decision

- **Default = warning, hard block opt-in.** Curated + low-false-positive. With too many false alarms, alarm fatigue sets in → operators turn off the hook → protection at zero. Hard block only via `BODYGUARD_STRICT=1` for projects with higher compliance pressure.
- **Reflex instead of deep check.** Layer 0 is a fast, deterministic reflex on a small curated set of patterns — **not** a full Semgrep run per edit. The depth (data flow, full scan) stays at Layer 2/3.
- **Base + overlay.** Framework base patterns + project overlay `.claude/bodyguard.local.yml` (customer extends/overrides per `name`, survives framework updates — customer property, never overwritten).
- **Source per pattern is mandatory.** Each pattern carries its evidence in the `quelle` field (CWE / OWASP / gitleaks / Semgrep registry / Bandit / eslint-plugin-security) — audit proof, no "magic" regexes.
- **Dependency-free.** Only `bash` + `python3` stdlib; a mini YAML parser in the hook (no PyYAML needed).

## Relation to agentic-security (PolyForm)

The pattern was **rebuilt** from `agentic-security` ("pre-edit-bodyguard") — **no code taken over**. `agentic-security` is under the PolyForm license; only the **idea** of a Layer-0 edit hook was adopted. Patterns, schema, hook logic, and docs are created independently from public catalogs (CWE/OWASP/gitleaks/Semgrep). Hard constraint of the story: no PolyForm code in the repo.

## What Users Get

- **`.claude/hooks/pre-edit-bodyguard.sh`** — the hook: reads stdin JSON (`tool_input` with `file_path` + `content`/`new_string`/`edits`), selects the pattern file by file extension, matches. Exit 1 = blocked (reason to Claude), Exit 0 = allowed.
- **`.claude/hooks/bodyguard/patterns/_universal.yml`** — secrets, language-independent (AWS key, private-key block, Slack/GitHub token, generic secret assignment).
- **`.claude/hooks/bodyguard/patterns/{python,javascript,java,c-cpp}.yml`** — language-specific unsafe-code patterns (e.g. `subprocess shell=True`, `verify=False`, `rejectUnauthorized: false`, `Runtime.exec`, `gets`/`strcpy`).
- **`.claude/hooks/bodyguard/SOURCES.md`** — origin, source table, and maintenance convention (keep curated + small, no auto-merge of external patterns).
- **`.claude/bodyguard.local.yml`** — optional project overlay (customer property, survives updates).
- **`migrate_boo_86`** — idempotent, additive migration for existing projects (see below).

## Migration

`bash bootstrap/scripts/migrate-to-v2.sh --issue BOO-86`

- Creates the hook, pattern catalogs, and `SOURCES.md` (only if not present), `chmod +x` on the hook.
- Creates the overlay `.claude/bodyguard.local.yml` **only** if it is missing — an existing customer overlay is **never** overwritten.
- Registers the `Edit|Write|MultiEdit` matcher in `.claude/settings.json` **and** `.claude/settings.local.json` — idempotent, additive only; existing `Bash` matchers (e.g. `spec-gate.sh`) stay untouched.
- **Idempotent:** a second run produces no diffs (files + registration are detected, `[SKIP]`).

Verification: `bash -n .claude/hooks/pre-edit-bodyguard.sh` (Exit 0); smoke test with a test secret in a `.py`/`.js` → Exit 1 (`[BODYGUARD] BLOCKIERT`); clean code → Exit 0. Rollback: delete the hook + `bodyguard/` directory and remove the `Edit|Write|MultiEdit` block from both settings files.

## Concrete Changes

| Area | File |
|---|---|
| Hook + pattern catalogs + SOURCES + overlay (templates) | `bootstrap/references/file-templates.md` §hooks/pre-edit-bodyguard.sh |
| Migration | `migrate_boo_86` in `bootstrap/scripts/migrate-to-v2.sh` (+ `ALL_ISSUES`) |
| Migration checklist §BOO-86 (DE+EN) | `bootstrap/references/migration-checklist-v1-to-v2.md` + `.en.md` |
| Spec | `specs/BOO-86.md` |

## Skill Version Bumps

- none (hook templates + migration + docs, no skill code change)

## References

- Spec: `specs/BOO-86.md`
- Canonical templates: `bootstrap/references/file-templates.md` §hooks/pre-edit-bodyguard.sh
- Pattern sources: `.claude/hooks/bodyguard/SOURCES.md` (CWE/OWASP/gitleaks/Semgrep)
- ADR: `02 Projekte/Code-Crash Framework/Decisions/2026-05-31 agentic-security-Adoption Bodyguard + dpo-Katalog.md`
- Relation: `agentic-security` ("pre-edit-bodyguard") — pattern rebuilt, no code (PolyForm license)
- Linear: BOO-86
