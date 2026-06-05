# Wave BH — Knowledge-Onboarding: explainer sketches (v1.1.0)

**What's there now:** the bundle skill `knowledge-onboarding` (introduced in Wave AX / BOO-137) gains **5 explainer Excalidraw sketches** in OWLIST design, **DE + EN** each, that visually explain individual core concepts — in addition to the existing overall overview. Embedded in README and SKILL (DE+EN) at the matching spots. Skill version `1.0.0 → 1.1.0`. DE: [`wave-bh-knowledge-onboarding-sketches.md`](wave-bh-knowledge-onboarding-sketches.md).

## Changes

- **5 sketches** in `knowledge-onboarding/references/sketches/`, `.excalidraw` + `.png` (DE) and `.en` variant (EN) each — 20 files, OWLIST colours, render-loop validated:
  1. `01-problem-loesung` — Problem → Solution: deterministic, not LLM whim (side-by-side comparison).
  2. `02-adapter-funnel` — 3 adapters → one normalised `files[]` list (convergence/funnel).
  3. `03-tier-wasserfall` — classification cascade Tier 0/1/2/3 (decision waterfall, hero sketch).
  4. `04-manifest-determinismus` — re-scan reads the manifest first: re-read, not re-infer.
  5. `05-anti-fabrikation` — propose, don't blindly apply + coverage check (operator gate).
- **Embedded:** `README.md`/`README.en.md` (new section "Sketches — explained visually") and `SKILL.md`/`SKILL.en.md` (each sketch at its matching workflow step: intro · step 1 · step 4 · re-scan · anti-fabrication).
- **Version:** `knowledge-onboarding/SKILL.md`+`.en.md` to `version: 1.1.0`; README `**Version:** 1.1.0` line added (sibling consistency + docs-drift version parity).
- **HANDBUCH (DE+EN):** Appendix AC extended with a sketch note.
- **SecondBrain:** skill doc `03 Bereiche/Skills/knowledge-onboarding.md`+`.en.md` newly created.

## Migration

None. Pure docs/asset addition — no change to skill workflow behaviour, no new dependencies.

## References

Skill: `knowledge-onboarding/`. Origin wave: [`wave-ax-knowledge-onboarding.en.md`](wave-ax-knowledge-onboarding.en.md) (BOO-137). Sketch source: `knowledge-onboarding/references/sketches/`. Render pipeline: `~/.claude/skills/excalidraw-diagram/references/render_excalidraw.py`.
