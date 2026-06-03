# Wave AV — Docs/runbooks, lightweight SecondBrain & design-story decision (BOO-118/119/126/128/129)

**What's now there:** the GitHub runbook covers HTTPS→SSH, SonarCloud has its own two-scenario setup runbook, the operator can check their setup anytime, `repo-docs` becomes a usable lightweight SecondBrain (session-start routine), and design-story handling is recorded as a decision. Third and final bundle of the post-trial follow-up stories (BKO, 2026-06-02).

## Stories
- **BOO-118** — SSH runbook: `git remote set-url` HTTPS→SSH as step 5 + connection test.
- **BOO-128** — Phase 7.6: `verify-setup.sh` re-run hint (`--strict`, read-only) + ready-made operator prompt.
- **BOO-119** — HANDBUCH **Appendix AA**: SonarCloud setup runbook (scenario A: account exists / B: from zero); bootstrap D.5 + provider postflight (BOO-58) deeplink to it.
- **BOO-129** — `repo-docs` **lightweight SecondBrain**: session-start routine in the generated `CLAUDE.md` (read PMO hub + meetings/decisions, write back) + DE/EN sketch.
- **BOO-126** — **design-story decision** ratified: "implement against a reference", no `change_type:design` (ADR + boundary, Karpathy verifiability).

## Changes (DE+EN)
- **`HANDBUCH.md`:** §3 SSH step 5 (BOO-118); new **Appendix AA** SonarCloud runbook (BOO-119); §6 design-story boundary (BOO-126).
- **`bootstrap/SKILL.md`:** phase 7.6 verify-setup re-run + prompt (BOO-128); D.5 Appendix-AA deeplink (BOO-119).
- **`references/file-templates.md`:** CLAUDE.md template session-start routine (BOO-129).
- **`references/project-documentation-ssot.md`:** lightweight SecondBrain loop + sketch embed (BOO-129).
- **`references/provider-postflight.md`:** SonarCloud runbook deeplink (BOO-119).
- **New:** ADRs `docs/domain/adrs/design-story-handling(.en).md` (BOO-126); sketch `docs/assets/boo-129-leichtgewicht-secondbrain.{excalidraw,png}` (+ `.en`).

## References
Specs: `specs/BOO-118.md`, `BOO-119.md`, `BOO-126.md`, `BOO-128.md`, `BOO-129.md`. Merged via PR #38. Doc-review (#39) added the bootstrap-phases sketch refresh + HANDBUCH appendix-index fixes (DE+EN).

## Note
The DE wave notes (`wave-at/au/av.md`) and these EN counterparts are the bilingual release notes for the BOO-114–129 work; the HANDBUCH footer "Last updated" was bumped to 2026-06-03.
