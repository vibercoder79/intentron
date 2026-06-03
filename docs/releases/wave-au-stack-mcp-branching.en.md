# Wave AU — Stack polish, MCP, Sonar warning & branching standard (BOO-116/121/122/124/125)

**What's now there:** on "other", the stack question no longer falls silently to ESLint; the bootstrap asks for project-specific MCPs on frontend/full-stack; it warns about the SonarCloud merge gate; it guarantees the bundle-skill source (intentron) mechanically; and it names a positioned branching standard. Second bundle of the post-trial follow-up stories (BKO, 2026-06-02).

## Stories
- **BOO-116** — stack `e) other` → free-text follow-up "which technology?" + linter hint (Go/Rust/Java/PHP/Ruby) instead of silent ESLint.
- **BOO-125** — Block-D step **D.7**: project-specific MCP question (Vercel/Apify/custom) on frontend/full-stack + Vercel-deploy clarification + frontend combo.
- **BOO-121** — **source guarantee**: all bundle skills (incl. `intent`) from intentron; regression check `check-skill-sources.sh` + CI `skill-sources.yml`; skills-setup docs corrected; re-pull hint.
- **BOO-122** — warning on D.5=yes: SonarCloud becomes a required check (first PR blocked without setup) + removal path + optional question.
- **BOO-124** — **branching standard** named (Trunk-Based + protected `main` + PR + required checks) + sales one-liner + DE/EN sketch + ADR; options table reframed as "alternatives".

## Changes (DE+EN)
- **`bootstrap/SKILL.md`:** A.1 e) free-text + linter hint (BOO-116); D.7 MCP question (BOO-125); D.5 Sonar warning callout (BOO-122); phase-5 re-pull hint (BOO-121).
- **`HANDBUCH.md` Appendix R:** named branching default + sales one-liner + sketch embed + ADR reference; options table = "alternatives" (BOO-124).
- **`references/skills-setup.md`:** §repo structure corrected to the flat intentron structure + source guarantee (BOO-121).
- **New:** `bootstrap/scripts/check-skill-sources.sh`, `.github/workflows/skill-sources.yml` (BOO-121); `docs/domain/adrs/branching-standard.md` (+ `.en`); `docs/assets/boo-124-branching-standard.{excalidraw,png}` (+ `.en`).

## Lightweight principle
BOO-116 is cleanly delimited against BOO-127/A.1a (tech free-text vs. unsure→suggestion). BOO-124 doesn't duplicate the options table but reframes it as alternatives. The BOO-121 check is dependency-free (bash+git).

## References
Specs: `specs/BOO-116.md`, `BOO-121.md`, `BOO-122.md`, `BOO-124.md`, `BOO-125.md`. Merged via PR #40 (replacing the auto-closed #37).
