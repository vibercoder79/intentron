# Wave AG — Docs-Sync-Sweep (BOO-97)

> 🌐 **Language:** English (this file) · [🇩🇪 Deutsch](wave-ag-docs-sync-sweep.md)

**Linear:** [BOO-97](https://linear.app/owlist/issue/BOO-97/)

## Problem

A repo-wide doc gap audit (6 parallel subagents, cross-verified) showed: the
skill READMEs and the repo README lagged behind the actual feature state
(version drift), plus two dead reference links and parity gaps.

## Stories

| Story | Content | Status |
|-------|--------|--------|
| **BOO-97** | Repo-wide doc gap audit (6 subagents) + fixing the high/medium gaps | ✅ done |

## What changes

- **README:** `/intent` line added in both skills tables (was missing — 12 of 13 skills);
  „What's new" block extended to v0.6.0/v0.6.1 (DE+EN).
- **Dead links removed:** `implement/references/governance-validation.md` (SKILL.md/.en +
  README tree) and `ideation/references/perplexity-api.md` (belongs to the research skill → replaced by
  the real `token-heuristik.md`).
- **architecture-review README** v1.3.0 → **v1.12.0**: AI-suitability checklist (BOO-7),
  SonarQube Cloud read block (BOO-6), feature-flag hygiene (BOO-17) caught up (DE+EN).
- **sprint-review README** v1.2.0 → **v2.6.0**: dpo audit trigger (step 7c),
  anti-pattern self-diagnosis, reports/cost aggregation caught up (DE+EN).
- **EN parity:** `security-architect/SKILL.en.md` new (the only bundle skill without EN) +
  `dpo/README.en.md` new.
- **security-architect SKILL.md:** heading „3 Modi" → „4 Modi" (SKILL-SCAN was already
  listed).
- **HANDBUCH:** DE table of contents „A bis X" → „A bis Y"; footer date + changelog (DE+EN)
  brought up to date.

## Deliberately noted as follow-up backlog (not in this sweep)

Granular `wave-ab…ag.md` (rule-1 backfill), HANDBUCH §13 „v0.2.0-Themen" framing,
claudecodeskills residual links in §3/§5/§7, intent EN templates, coverage-check in hooks-setup,
3 low version bumps (visualize/grafana/cloud-system-engineer).

## Effect

The documentation again mirrors the real feature state; no more dead links; all bundle skills
DE+EN. Pure documentation, no behavioral change.

## References / Release

- Branch `feat/boo-97-doku-sync`. Release: **v0.6.2 (Wave AG)** — see
  `docs/releases/v0.6.2-overview.md`. (Detail spec `specs/BOO-97.md` is not present in the repo;
  the source of this note is the v0.6.2 overview.)
