# Wave AX — Knowledge-Onboarding: route existing docs into governance artefacts (BOO-137)

**What's new:** a new framework bundle skill `knowledge-onboarding` that routes existing project knowledge (GAP analyses, legal research, README, PLAN, `docs/`-context, design files, demo storyboards, handover, prompt library) **deterministically and repeatably** into the framework governance artefacts. Determinism via **routing rubric (SSoT, 4 tiers)** + persisted **manifest** (`journal/knowledge-onboarding-map.yml`) + **pinning** for operator corrections. Source-agnostic (GitHub repo / local folder / chat). Runs **post-bootstrap**. DE: [`wave-ax-knowledge-onboarding.md`](wave-ax-knowledge-onboarding.md).

## Stories
- **BOO-137** — new bundle skill `knowledge-onboarding/` (top-level, source guarantee BOO-121): `SKILL.md`+`.en.md`, `README.md`+`.en.md`, `references/routing-rubric.md`+`.en.md`, Excalidraw overview sketch DE+EN (render loop, OWLIST colors).

## What the skill does (short)

1. **Adapter choice** — 3 source adapters (GitHub repo / local folder / chat) → unified file list.
2. **Pre-flight** — detect framework artefacts (`CLAUDE.md`/`AGENTS.md`/`CONVENTIONS.md`/`ARCHITECTURE_DESIGN.md`/…) → **Tier-0 exclusion**.
3. **Read manifest** (determinism anchor) — known files keep their routing, changed ones are re-classified, `pinned: true` protects.
4. **Classification Tier 0/1/2/3** — Tier 1 filename, Tier 2 content signals, Tier 3 ambiguous → **operator asks**, never guesses.
5. **Proposal table** — no auto-apply; operator decides.
6. **Routing-apply** — default `reference` (reference block with source link / signal / tier / as-of date), option `extract` with diff approval.
7. **Write manifest** (committed, audit trail).
8. **Coverage check** — warning when skip > 50% or Tier 3 > 30%.

## Routing rubric (10 categories + Tier 0)

| Tier | Category | Target |
|---|---|---|
| 0 | Framework artefact / code | skip |
| 1 | Intent · GAP · Scope | `intents/` + `ARCHITECTURE_DESIGN.md §1` |
| 1 | Legal · Compliance | `SECURITY.md`/`GOVERNANCE.md` + DPO + ADR |
| 1 | Design · UI · Visual | `ARCHITECTURE_DESIGN.md §5` + `DESIGN.md` + ADR |
| 2 | Decision taken | ADR `docs/domain/adrs/` |
| 1 | Architecture · Plan | `ARCHITECTURE_DESIGN.md` + Backlog |
| 1 | Vocabulary · Context | `CONTEXT.md` + Component-Docs |
| 1 | Research | `docs/project/research/` |
| 1 | Demo · Storyboard · Pitch | `docs/project/demo/` |
| 1 | Onboarding · Handover | `DEVELOPER_ONBOARDING.md` |
| 1 | Prompt library | `docs/project/prompts/` |
| 3 | Ambiguous | Operator asks (pinned) |

Full version (with keyword lists + examples): `knowledge-onboarding/references/routing-rubric.en.md`.

## Anti-fabrication rules

- No routing without match signal — never guess.
- No full-text copy without operator approval — default is `reference`.
- Source reference mandatory in every inserted block (`<!-- knowledge-onboarding · BOO-137 · source:<path> · as-of:<date> -->`).
- Coverage check mandatory.
- Manifest as audit trail; operator corrections with `pinned: true` are immutable on re-scan.

## New / changed (DE+EN)

- **New:** skill directory `knowledge-onboarding/` with 8 files (SKILL/README/References each DE+EN, Excalidraw + PNG each DE+EN), `specs/BOO-137.md`.
- **Bootstrap wiring:** `bootstrap/SKILL.md` (DE+EN) Phase 5 skill selection (Standard tier) + repo structure hint + Phase 7.6 item 7 (hint when existing docs present).
- **`bootstrap/scripts/check-skill-sources.sh`** — `knowledge-onboarding` in `BUNDLE_SKILLS` array.
- **`bootstrap/references/skills-setup.md` (DE+EN)** — skill table extended (Standard tier).
- **`bootstrap/references/existing-infra-check.md`** — `EXISTING_INFRA` output extended with flag `bestands_doku_erkannt: true|false`.
- **`docs/how-we-document.md` (DE+EN)** §4 — `/knowledge-onboarding` placed as step 0 (human docs first, then `/architecture-review`, then `framework-upgrade`).
- **HANDBUCH (DE+EN)** — new appendix AC "Knowledge-Onboarding".

## References

Spec: `specs/BOO-137.md`. Branch: `feat/boo-137-knowledge-onboarding`. ADR: SecondBrain `02 Projekte/Code-Crash Framework/Decisions/2026-06-03 Knowledge-Onboarding-Skill — Routing-Rubrik + Manifest-Determinismus.md`. Trigger case + rubric validation: `vibercoder79/bko-widerspruch-assistent`.
