# Release Notes - Wave J Privacy-by-Design

> 🌐 **Language:** English (this file) · [🇩🇪 Deutsch](wave-j-privacy-by-design.md)

As of: 2026-05-27

## Purpose

Wave J closes BOO-69. The framework anchors Privacy by Design as an optional add-on with full operationalization — 1:1 the pattern of Security by Design, but for data protection. Anyone who activates the Privacy add-on gets: a full-fledged DPO skill (standalone, analogous to `security-architect`), a `PRIVACY.md` with 8 mandatory sections, a `personal-data-paths.json` as a HARD-GATE pattern, three pipeline hooks (ideation step 0e, implement step 5.5b, sprint-review step 7c), and a HANDBUCH appendix O as a reading entry point.

**Expected effect:** Privacy-by-Design becomes a **framework guarantee** instead of best-effort. The asymmetry with Security-by-Design is resolved. The operator does not need to bring GDPR expert knowledge — the DPO skill asks the right review questions.

## Affected Stories

- BOO-69

## Important Clarification: DPO Stays Standalone

The spec originally planned "DPO into the bundle". Research during implementation showed: `security-architect` is NOT a bundle skill, but standalone under `~/.claude/skills/security-architect/`. Bootstrap installs it via the standalone skill set when security is needed. **Operator decision: DPO follows this pattern.** Advantages: non-destructive (DPO stays available globally in parallel), consistent with the existing bundle philosophy (workflow skills in the bundle, specialists standalone), updates via `publish_skill.py` without bundle intervention.

The spec `specs/BOO-69.md` contains a naming-hint block at the top documenting the decision.

## What Users Get with the New Setup

- **DPO skill** with three modes: ASSESS (story planning, writes DPIA), REVIEW (code change, checks data minimization/consent/deletion mechanics), AUDIT (every N sprints, maintains the record of processing activities). Covers GDPR (EU), BDSG (DE) and nDSG (CH). Recommended Model: opus (compliance-critical).
- **PRIVACY.md** in the project root with 8 mandatory sections: privacy principle, legal bases Art. 6 GDPR, record of processing activities Art. 30, deletion concept, data subject rights Art. 15-22, personal-data-paths, privacy-by-design workflow, incident note Art. 33/34.
- **`personal-data-paths.json`** with default patterns (`**/user*`, `**/profile*`, `**/billing/**`, etc.). HARD GATE in the `/implement` step 5.5b — no commit without a `privacy-ok` confirmation or a DPO-REVIEW report.
- **`/ideation` step 0e** pre-flight: story frontmatter `personal_data: true|false`. On `true`: DPO ASSESS recommended, backlog label `privacy`, DPIA reference.
- **`/implement` step 5.5b** personal-data-paths gate (analogous to 5.5 sensitive-paths gate). Plus step 6e extended from "security findings" to "security + privacy findings" with a mandatory privacy block on `personal_data: true`.
- **`/sprint-review` step 7c** DPO audit trigger every N sprints (default 4, configurable via `environment.json.privacy_audit_cadence`).
- **HANDBUCH appendix O** Privacy by Design as a reading entry point: trigger list, 3-mode mapping, DPO ↔ security-architect separation, migration hints, cross-reference to BOO-71 sovereignty stack.
- **Audit argument** for regulated industries: DPO stays provably on the Opus tier (compliance-critical, no auto-downgrade), combinable with the token-efficiency policy (BOO-84) without conflict.

## Concrete Changes

| Area | Change | File |
|---|---|---|
| DPO skill globally normalized | Frontmatter extended by `recommended_model: opus` + `metadata.hermes`, EN variant new | `~/.claude/skills/dpo/SKILL.md` + `SKILL.en.md` (NEW) |
| DPO references EN mirror | 5 references files mirrored in EN | `~/.claude/skills/dpo/references/*.en.md` (5 NEW) |
| PRIVACY.md template NEW | 8 sections, structurally parallel to security-template.md | `bootstrap/references/privacy-template.md` + `.en.md` (NEW) |
| Bootstrap Privacy add-on upgraded | Phase A.4 with concrete setup block, new phase 4.4n privacy setup | `bootstrap/SKILL.md` v3.27.0 + `.en.md` |
| Personal-data-paths template NEW | JSON template analogous to sensitive-paths.json | `bootstrap/references/file-templates.md` + `.en.md` |
| Ideation step 0e NEW | Privacy pre-flight with heuristic table | `ideation/SKILL.md` v2.7.0 + `.en.md` |
| Implement step 5.5b NEW + 6e extended | Personal-data-paths gate as HARD GATE, privacy-findings block | `implement/SKILL.md` v2.11.0 + `.en.md` |
| Sprint-review step 7c NEW | DPO audit trigger with cadence config | `sprint-review/SKILL.md` v2.6.0 + `.en.md` |
| HANDBUCH appendix O NEW | Privacy-by-Design reading entry point (DE+EN) | `HANDBUCH.md` + `HANDBUCH.en.md` |
| Migration | `migrate_boo_69()` + migration-checklist §BOO-69 | `bootstrap/scripts/migrate-to-v2.sh`, `bootstrap/references/migration-checklist-v1-to-v2.md` + `.en.md` |

## Skill Version Bumps

- `bootstrap` 3.26.0 -> 3.27.0
- `ideation` 2.6.0 -> 2.7.0
- `implement` 2.10.0 -> 2.11.0
- `sprint-review` 2.5.0 -> 2.6.0
- `dpo` (standalone, global) 1.0.0 -> 1.1.0

## Migration for Existing Projects

`migrate_boo_69()` in `bootstrap/scripts/migrate-to-v2.sh`:

```bash
bash bootstrap/scripts/migrate-to-v2.sh --issue BOO-69
```

Idempotent and additive. Result:
- `PRIVACY.md` generated from template (skip if present)
- `.claude/personal-data-paths.json` and/or `.codex/personal-data-paths.json` created
- `environment.json` extended by `privacy_audit_cadence: 4`
- Availability check DPO + security-architect (purely informational)

Operator steps: install DPO + security-architect globally (if not yet done), fill PRIVACY.md with content, create backlog label `privacy`.

## Design Decision: Recommendation Instead of Hard Lock

Privacy is **optional**. Anyone who processes no personal data (solo tool, anonymous data) gets no additional friction point from the framework. Anyone who activates the add-on: fully operationalized, not half-baked.

Privacy findings in REVIEW mode are documentation-mandatory (mandatory block in step 6e), but not a hard block on the code change — the operator can explicitly confirm with `privacy-ok` that the change is justified despite the finding. The audit trail documents the decision.

## Still Open / Follow-ups

- **HANDBUCH appendix Q (BOO-71):** Sovereignty stack guide, complements this wave in terms of content (data sovereignty, EU alternatives, LLM proxy hook).
- **HANDBUCH appendix P (BOO-70):** Deployment scenarios — operator decision whether the project runs on Solo-Mac/Solo-VPS/Multi-User-VPS/Team-Server. Influences, among other things, where `dpia/` files are kept (private vs. committed).
- **Record-of-processing-activities skeleton:** Operator action required after bootstrap. DPO ASSESS mode supports the initial fill-in.
- **DPIA practice examples:** could be added as additional references files under `dpo/references/examples/` (own follow-up story if needed).

## References

- Spec: `specs/BOO-69.md`
- HANDBUCH: Appendix O Privacy by Design
- DPO skill: `~/.claude/skills/dpo/SKILL.md` + `.en.md`
- Feedback source: Operator Martin, 2026-05-27 (`02 Projekte/Code-Crash Framework/assets/fact-sheet-privacy-by-design_1.docx`)
- Linear: <https://linear.app/owlist/issue/BOO-69/>
