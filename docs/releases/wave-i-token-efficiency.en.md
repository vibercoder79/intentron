# Release Notes - Wave I Token Efficiency Policy

> 🌐 **Language:** English (this file) · [🇩🇪 Deutsch](wave-i-token-efficiency.md)

Status: 2026-05-25

## Purpose

Wave I closes BOO-84. The framework anchors a systematic token efficiency policy: a recommended model tier per skill (Haiku/Sonnet/Opus), a central tier mapping with USD pricing, prompt caching for reused blocks, and cost tracking in `meta.json`. Expected effect: 50-70% token reduction per story, ~15-25% margin lever in customer engagements.

## Affected Stories

- BOO-84

## What Users Get with the New Setup

- A **recommended model tier** per skill (`haiku | sonnet | opus`) in the frontmatter — the operator no longer has to switch the model manually before each run.
- A **central mapping file** `bootstrap/references/model-tiers.json` with tier-to-version and USD pricing. On Anthropic releases, update once centrally instead of touching 11 skill files.
- **Operator override possible at any time** — two-stage: CLI flag `/implement --model opus` (one-off) plus `model_overrides:` in CLAUDE.md (project-wide). Override audit trail in `meta.json` for compliance.
- **Prompt caching systematically active** for SKILL.md, Constitution, SECURITY.md, ARCHITECTURE_DESIGN.md, repo map — 90% discount on reused blocks.
- **Cost aggregation in the Sprint Review** — per sprint, a USD cost breakdown by model tier, cache hit rate, override count.
- **Audit argument for regulated industries** — security-relevant skills (`architecture-review`, `cloud-system-engineer`, `/implement` step 6e) remain verifiably on Opus, no auto-downgrade.

## Concrete Changes

| Area | Change | File |
|---|---|---|
| Tier mapping NEW | Central JSON with version and pricing mapping | `bootstrap/references/model-tiers.json` |
| Skill frontmatter | `recommended_model:` in all 11 bundle skills (DE+EN), tier-based | `*/SKILL.md`, `*/SKILL.en.md` |
| Bootstrap phase 4.4m | New sub-phase "Token Efficiency Setup" — writes model routing section into CLAUDE.md | `bootstrap/SKILL.md` v3.26.0 |
| CLAUDE.md template | New sections "Model Routing Policy" + "Prompt Caching" | `bootstrap/references/file-templates.md` |
| implement step 6f-bis | `meta.json` extended with 3-level token tracking + cache hit rate + override audit trail | `implement/SKILL.md` v2.10.0 |
| sprint-review step 2b | Cost aggregation per sprint with tier breakdown | `sprint-review/SKILL.md` v2.5.0 |
| HANDBUCH Appendix N NEW | Combined section model routing policy + prompt caching explained technically | `HANDBUCH.md` (DE+EN) |

## Skill Version Bumps

- `architecture-review` 1.11.0 -> 1.12.0
- `backlog` 1.4.0 -> 1.5.0
- `bootstrap` 3.25.0 -> 3.26.0
- `cloud-system-engineer` 1.0.0 -> 1.1.0
- `grafana` 1.0.0 -> 1.1.0
- `ideation` 2.5.0 -> 2.6.0
- `implement` 2.9.0 -> 2.10.0
- `intent` 1.2.0 -> 1.3.0
- `pitch` 1.0.0 -> 1.1.0
- `sprint-review` 2.4.0 -> 2.5.0
- `visualize` 2.2.0 -> 2.3.0

## Migration for Existing Projects

`migrate_boo_84()` in `bootstrap/scripts/migrate-to-v2.sh`:

1. Writes the model routing section into the project-local `CLAUDE.md` (idempotent).
2. Sets a project-wide `model_overrides:` default block (empty, operator fills it as needed).
3. Extends the `meta.json` schema documentation in `journal/reports/local/README.md` (optional).

Operator runs manually:

```bash
bash bootstrap/scripts/migrate-to-v2.sh boo_84
```

Migration is additive — existing behavior remains unchanged, new fields are added.

## Design Decision Conformity

This wave follows the INTENTRON principle "lightweight + pragmatic, without security compromises":

- **Recommendation instead of hard lock**: the operator can override the model at any time, no block on tier choice.
- **Audit trail for compliance**: every override is logged (FINMA/BaFin-capable).
- **Security-stays-Opus documented**: explicit spec requirement, no silent optimization at the expense of security.
- **Hook activation optional**: without the caching hook everything keeps working, only without the cost aggregate.

## Expected Impact

At 5 lint iterations per story: ~95% cheaper than naive Opus + no cache (Haiku routing 12x cheaper than Opus, plus caching 70% reduction on reused blocks). For a 6-month engagement with ~80 stories: 15-25% margin lever. USD cost is reported per sprint in the Sprint Review report — a FinOps argument for discovery conversations.

## Follow-Up Items

- **PostToolUse hook for auto token capture**: an optional follow-up skill that writes `.claude/last-run-tokens.json` and `.claude/last-run-overrides.json` during the run. Without the hook, the `meta.json.token_tracking` fields remain empty — no story run is blocked.
- **BOO-74 test run**: BOO-74 (Constitution refactor) is run with active routing + caching, a before/after cost table is documented in the BOO-84 PR or in the BOO-74 PR.
- **Release obligation**: check the `model-tiers.json` version and pricing entries per INTENTRON release against the Anthropic pricing page (entry in the project-internal handbook sync queue).
