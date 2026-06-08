# Release Notes - Wave X Deterministic dpo Control Catalog

> 🌐 **Language:** English (this file) · [🇩🇪 Deutsch](wave-x-dpo-control-catalog.md)

Status: 2026-05-31

## Purpose

Wave X (BOO-87) gives the dpo skill a **deterministic control catalog** plus a **runner** that checks a project against curated data-protection controls and produces an **auditor-ready report** — one status per control: **PASS / GAP / REVIEW-NEEDED**. Two catalogs cover the EU (`gdpr.yml`) and Switzerland (`ndsg.yml`). This way the framework delivers reproducible compliance evidence that an auditor (FINMA/BaFin, external auditor) can trace directly — without a database, without SaaS, local and deterministic.

## Why

Data-protection compliance in practice rarely fails for lack of knowledge, but for **lack of traceable evidence** at audit time. "We're already doing it right" is not audit proof. Regulators like FINMA (CH) and BaFin (DE) expect demonstrable, repeatable controls instead of snapshots. A deterministic runner — identical input yields an identical report — closes this gap: every control is a checkable statement (file exists / contains pattern / pattern is absent / manual check needed), every statement carries its regulatory reference (`mapsTo`) and its source (`quelle`). The report becomes part of the repo and is thus versioned and traceable.

nDSG (revised CH data-protection law) is the **unique selling point**: most compliance tools cover only GDPR/EU. A dedicated `ndsg.yml` catalog specifically addresses Swiss projects and is a differentiator in the DACH consulting context.

## Design Decision

- **Deterministic instead of heuristic.** Same input → same report. Four check types: `file-exists`, `file-contains`, `grep-absent`, `review`. No LLM in the check path, no non-reproducibility.
- **Status model PASS / GAP / REVIEW-NEEDED.** `review` controls are deliberately not automatable (e.g. "deletion concept professionally approved") and are reported as REVIEW-NEEDED — more honest than a forced PASS/FAIL.
- **Catalog + project overlay.** Framework base catalogs (`dpo/controls/gdpr.yml` + `ndsg.yml`) come with the skill and are replaced on updates. The **project overlay** `.claude/dpo/controls/` (bring-your-own-controls) belongs to the customer and **survives framework updates** — never overwritten.
- **Catalogs + runner travel with the skill, not per project.** The project migration is therefore lightweight: only overlay directory + reports dir. No duplicated scaffolding, one central maintenance point.
- **No database.** The report is a file in `dpo/reports/`, versioned in the repo. No state server, no SaaS, no data outflow — fits the framework's sovereignty claim.
- **OSCAL as a later expansion stage.** The flat schema (`id`/`titel`/`evidenz`/`check_typ`/`check_arg`/`mapsTo`/`quelle`) is deliberately simple. A mapping to OSCAL (NIST Open Security Controls Assessment Language) is foreseen as a later expansion but is not part of this wave — first prove the value, then standard mapping.

## Relation to agentic-security (PolyForm)

The idea of a deterministic control runner is modeled on the `agentic-security` pattern. `agentic-security` is under the PolyForm license; only the **idea** was adopted — **no code**. Catalogs, schema, runner, and docs are created independently from public regulatory sources (GDPR, nDSG, BDSG). Hard constraint: no PolyForm code in the repo.

## What Users Get

- **`dpo/controls/gdpr.yml`** — GDPR/EU control catalog (comes with the dpo skill v1.2.0).
- **`dpo/controls/ndsg.yml`** — nDSG/CH control catalog (CH uniqueness, comes with the skill).
- **`dpo/scripts/dpo-audit.py`** — deterministic runner: reads the framework catalogs + the project overlay, checks each control, writes the report (PASS/GAP/REVIEW-NEEDED) to `dpo/reports/`. Controlled among others via `DPO_PROJECT_ROOT`.
- **`.claude/dpo/controls/`** — project overlay (bring-your-own-controls) with an explanatory `README.md`; flat schema like the base catalogs; survives framework updates (customer property).
- **`dpo/reports/`** — target directory for the generated reports (with `.gitkeep`, versioned in the repo).
- **`migrate_boo_87`** — idempotent, additive project migration (see below).

## Migration

`bash bootstrap/scripts/migrate-to-v2.sh --issue BOO-87`

- Creates the project overlay directory `.claude/dpo/controls/` (only if not present) **with** a `README.md` that explains the BYO overlay and the flat schema.
- Creates the reports directory `dpo/reports/` (with `.gitkeep`).
- **No scaffolding** of catalog/runner/skill — those come with the dpo skill (v1.2.0). Only `[MANUAL]` hints are output that the audit runs via `DPO_PROJECT_ROOT=. python3 <dpo-skill>/scripts/dpo-audit.py` and uses the framework catalogs `dpo/controls/*.yml`.
- **Idempotent + additive:** a second run produces no diffs — existing directories/files are detected (`[SKIP]`); an existing customer overlay is **never** overwritten; `--dry-run` only logs (`[DRY]`).

Verification: `test -d .claude/dpo/controls && test -d dpo/reports` (Exit 0); `DPO_PROJECT_ROOT=. python3 <dpo-skill>/scripts/dpo-audit.py` produces a report in `dpo/reports/`. Rollback: remove the directories `.claude/dpo/controls/` and `dpo/reports/` (back up your own overlays first; catalog/runner live in the skill and are not affected).

## Concrete Changes

| Area | File |
|---|---|
| GDPR + nDSG catalogs | `dpo/controls/gdpr.yml` + `dpo/controls/ndsg.yml` (in the dpo skill) |
| Deterministic runner | `dpo/scripts/dpo-audit.py` (in the dpo skill) |
| Project migration | `migrate_boo_87` in `bootstrap/scripts/migrate-to-v2.sh` (+ `ALL_ISSUES`) |
| Migration checklist §BOO-87 (DE+EN) | `bootstrap/references/migration-checklist-v1-to-v2.md` + `.en.md` |
| Release Notes | `docs/releases/wave-x-dpo-control-catalog.md` |
| Spec | `specs/BOO-87.md` |

## Skill Version Bumps

- **dpo: 1.1.0 → 1.2.0** (catalogs `gdpr.yml` + `ndsg.yml`, runner `dpo-audit.py`, project overlay support)

## References

- Spec: `specs/BOO-87.md`
- Catalogs + runner: dpo skill `dpo/controls/*.yml` + `dpo/scripts/dpo-audit.py`
- Migration: `migrate_boo_87` in `bootstrap/scripts/migrate-to-v2.sh`
- ADR: `02 Projekte/Code-Crash Framework/Decisions/2026-05-31 agentic-security-Adoption Bodyguard + dpo-Katalog.md`
- Relation: `agentic-security` (deterministic control runner) — idea adopted, no code (PolyForm license)
- Later expansion stage: OSCAL mapping (NIST) — not part of this wave
- Linear: BOO-87
