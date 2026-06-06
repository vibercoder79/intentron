# Wave BM — /sprint-run README overhaul (BOO-166)

**What's now in place:** The `sprint-run/README` now explains the skill in depth, **embeds the Owlist sketches inline** (instead of just listing them), cross-links **DE↔EN**, has **plain-language prerequisites** and a **realistic installation** (bootstrap/update instead of a bare `cp -r`). README ↔ HANDBUCH Appendix AD ↔ runbook point at each other. Docs only — `sprint-run` stays **v1.1.0**. DE+EN.

## Stories
- **BOO-166** — README overhaul + sketch embedding + cross-linking.

## Changes (DE+EN)
- **`sprint-run/README.md` / `.en.md`**: new structure (what /sprint-run does · how a sprint runs · one story in detail · three safety layers · prerequisites · installation · configuration · related); `overview` + `sprint-run-flow` + `story-breakdown` + `gate-block-handling` **embedded inline**; DE↔EN language switch in the header; plain-language prerequisites; realistic installation (normal case `/bootstrap`/update, single skill via sparse-checkout).
- **HANDBUCH Anhang/Appendix AD (DE+EN)**: back-link to the `sprint-run/README`.

## Impact
Anyone opening the README understands what `/sprint-run` does without prior knowledge, sees the diagrams inline, and reaches the EN version, the HANDBUCH deep-dive chapter and the runbook with one click. Follows the embed/cross-link convention of `knowledge-onboarding`.

## Scope
Docs only, no code, no functional change (`sprint-run` stays v1.1.0, no version bump). wave letter **bm** (bk = gate-assertion BOO-165). Repo slot BOO-166 = Linear BOO-166.

## References
Spec: `specs/BOO-166.md`. Branch: `feat/boo-166-readme-overhaul`. Model: `knowledge-onboarding` (embed convention). Related: BOO-157 (HANDBUCH §6 + Appendix AD), BOO-165 (gate assertion). Operator source: Tobias, 2026-06-06.
