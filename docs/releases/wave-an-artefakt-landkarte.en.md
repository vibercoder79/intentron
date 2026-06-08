# Wave AN — Artifact & sign-off map (BOO-108)

> 🌐 **Language:** English (this file) · [🇩🇪 Deutsch](wave-an-artefakt-landkarte.md)

**What is there now:** a third onboarding document that closes the bridge between the discovery arcs and the phase artifacts — plus bootstrap coupling, migration, HANDBUCH appendix and sketch.

## Stories
- **BOO-108** — Artifact & sign-off map: RACI matrix artifact → sign-off role → rule sink.

## Changes
- `docs/onboarding/artefakt-landkarte.md` + `.en.md` — master matrix across all 13 skills/phases in 4 blocks (Setup/Governance · Product/Architecture · Security/Privacy · Delivery/Operations/Compliance). Columns: Artifact · Path · Phase · Default template · Trigger · Sign-off role · Rule sink · Status.
- **7 rule sinks** as the target column: `CLAUDE.md`, `CONVENTIONS.md`, `ARCHITECTURE_DESIGN.md §5`, `SECURITY.md`, `dpo/controls/`, `.claude/environment.json`, `DEVELOPER_ONBOARDING.md`.
- **DESIGN.md pattern:** Frontend design (colors/typo/components) is architecture — `§5` always points to `DESIGN.md` (no specs = explicit statement); sign-off Design/Brand.
- **Bootstrap 4.3c** (`bootstrap/SKILL.md`): yes/no question, seeds a filtered `solution-artefakte.md` (idempotent), triggers off the block-A answers.
- **HANDBUCH Anhang Z / Appendix Z** (DE+EN) + footer; **README** section "Customer onboarding — the three checklists" (DE+EN).
- **Sketch** `docs/assets/onboarding-flow.png` / `.en.png` (+ `.excalidraw` sources), OWLIST colors, created in the render loop: three checklists → artifacts×sign-offs → 7 rule sinks → autonomous team.

## Migration (existing projects)
```bash
bash bootstrap/scripts/migrate-to-v2.sh --issue BOO-108
```
`migrate_boo_108()` seeds `solution-artefakte.md` from the master template (idempotent — an existing operator instance stays untouched). Then filter to the solution manually.

## Smoke test
- `bash -n bootstrap/scripts/migrate-to-v2.sh` → OK; `--list` contains `BOO-108`; `--issue BOO-108 --dry-run` shows the seed step.
- Both sketches rendered + visually checked (no overlap/clipping).

## References
Spec: `specs/BOO-108.md`. Docs: `docs/onboarding/artefakt-landkarte.md`. Release: v0.7.5.
