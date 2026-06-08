# Wave BW — Documentation Definition of Done as a convention (BOO-180)

> 🌐 **Language:** English (this file) · [🇩🇪 Deutsch](wave-bw-doku-definition-of-done.md)

**What is now in place:** The lived documentation duty is now an **explicit convention** rather than just habit. New/changed documents must be cross-linked, propagated to the three index levels, bilingual (DE+EN), and shipped with a release note per issue. Until now the Definition of Done only said "bilingual (DE+EN)" — cross-linking, index updates and the touchpoint quartet existed only as practice, undocumented. This story frames the documentation discipline that BOO-176/177 already followed.

## Changes

- **Documentation Definition-of-Done checklist** — new in the canonical guidelines template `bootstrap/references/issue-writing-guidelines-template.md` (EN) + `.de.md` (DE), as a separate block **in addition** to the unchanged canonical 5-item DoD (BOO-30): cross-linking · three indices (`docs/INDEX.md`, `docs/onboarding/artefakt-landkarte.md`, `docs/releases/README.md`, each + `.en`) · DE+EN parity · release note per issue · sketch where helpful · `docs-drift` green.
- **Short version in `CONVENTIONS.md` §3** (EN and DE block) — new subsection "Documentation Definition of Done (BOO-180)" with the **touchpoint quartet**: keep HANDBOOK/doc · release note · spec · Linear in sync per "Done". Links to the guidelines template.
- **Template triplicate** — `migrate_boo_180()` in `migrate-to-v2.sh` (registered in `migrate_all` + `ALL_ISSUES`): a non-destructive note that existing projects re-pull their local `docs/issue-writing-guidelines.md` to inherit the doc DoD. New projects inherit it via the guidelines copy at bootstrap.

## Scope

- **Pure docs/convention, no code behaviour.** No new hook, no gate — the DoD is operator discipline, flanked by `docs-drift` (DE+EN parity, dead links).
- The canonical 5-item DoD (BOO-30) stays **unchanged** — the doc DoD is an additional block that only applies when the story touches docs.
- **Self-compliant:** this story satisfies its own DoD (DE+EN, cross-links guidelines ↔ CONVENTIONS, release note in the index, docs-drift green).
- Wave letter **bw** (bv = unit-test hardening BOO-177).

## References

Spec: `specs/BOO-180.md`. Branch: `tobiaschschmidt/boo-180-docs-doku-definition-of-done`. Related: BOO-30 (canonical DoD), BOO-173 (release index), BOO-176/177 (follow the doc DoD). Operator source: Tobias, 2026-06-07.
