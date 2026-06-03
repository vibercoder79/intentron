# ADR: Design-story handling — implement against a reference, no change_type:design (BOO-126)

- **Status:** accepted (2026-06-03)
- **Type:** discovery/decision story (deliberately decided in a structured way, not immediate impl)
- **Context source:** post-trial follow-up (BKO, 2026-06-02)

## Context
How does the framework handle design-heavy stories? The choice: is "design story = implement against a
design reference" (the operator's default thesis) enough, or does it need a dedicated `change_type: design`,
a template, and/or auto-detection in `/ideation`?

Finding (v0.7.9): there is **no** design-specific story type; `change_type` types (non-code/prototype) were
only proposals, never implemented. `ARCHITECTURE_DESIGN.md` can reference a design file via §9 auto-linking —
so the "code against a design reference" mechanism already exists.

## Decision
**Default ratified:** a design story = **"implement against a design reference"** via the normal pipeline
(`/ideation` → `/implement`). **No** `change_type: design`, **no** new template, **no** auto-detection in
`/ideation`. The design reference (e.g. `DESIGN.md`, Figma export, screenshot) is linked in
`ARCHITECTURE_DESIGN.md §9`; `/implement` verifies against the reference **plus** a11y and Lighthouse gates
(BOO-45).

## Rationale (verifiability, Karpathy)
- **Code output has ground truth** (tests, Lighthouse budget, a11y checks) → auto-verifiable →
  framework-suitable. A design *implementation* can be checked against measurable gates this way.
- **Design taste has no auto-check** → no gate possible → does **not** belong in the mandatory pipeline.
- A dedicated `change_type: design` + template + auto-detection would be machinery for a single case
  without ground truth — a violation of the lightweight principle.

## Boundary (what goes where)
- **Coding framework (mandatory pipeline):** *implements* design — against a reference, with measurable
  gates (a11y, Lighthouse, tests).
- **Pure design (taste, brand, visual identity):** **opt-in external skills** — `design-md-generator`,
  the `lumen-*` brand skills, Pencil/Webflow MCP. **No** mandatory pipeline, no gate.

## Consequences
- No code/skill change needed — `/ideation` and `change_type` stay unchanged.
- If a `change_type: design` is later desired (with acceptance criteria reference-match + a11y/performance),
  that is a **new ADR** superseding this one.
- Documentation boundary anchored in HANDBUCH §6 (DE+EN).
