# Release Notes - Wave L Multi-Operator Coordination

> 🌐 **Language:** English (this file) · [🇩🇪 Deutsch](wave-l-multi-operator-coordination.md)

As of: 2026-05-27

## Purpose

Wave L closes BOO-72. The framework gets a HANDBUCH appendix R that delivers the honest answer to a previously unanswered operator question: "If 20 developers work at the same time in the same GitHub repo and pull docs from Obsidian (or Jira/Confluence/Notion) — does the framework still work then?". Appendix R splits the question into three layers (Code / Coordination / Docs), shows per layer "what scales natively, what doesn't, which options the operator has", and gives a concrete 10-step guide for INTENTRON in a 20-person team. **Pure docs story** — no new skill, no new bootstrap question, no framework convention. Including 1 high-quality Excalidraw sketch (`docs/assets/boo-72-multi-operator-3-layer.png`).

**Expected effect:** Appendix R closes the last big sales argument on team mandates — "does that scale to 20 people?" now has a clear HANDBUCH answer. Appendix P (Wave K) covers 2-5 operators, Appendix R extends to 5-20+.

## Affected Stories

- BOO-72 — HANDBUCH appendix R Multi-operator coordination + Excalidraw sketch

## Important Clarification: No Four-Eyes Enforcement

Appendix R documents the four-eyes convention for `review-ok` (sensitive-paths gate) and `privacy-ok` (personal-data-paths gate) as **operator discipline**, not as a framework gate. Theoretically an author comparison in the gate would be checkable (author of the gate commit != author of the change), but that would increase framework complexity without a clearly measurable benefit. The audit trail runs via `git blame` — the convention is observable, not enforced. BOO-72 explicitly excludes enforcement.

## What Users Get with the New Setup

- **HANDBUCH appendix R "Multi-operator coordination" (DE+EN)** with:
  - 3-layer model (code layer / coordination layer / docs layer) — per layer a table "what scales, what doesn't, options".
  - **Branch strategy comparison:** Trunk-Based / Feature-Branches / GitFlow with a recommendation per team size.
  - **CODEOWNERS example:** concrete `.github/CODEOWNERS` pattern for critical paths (`SECURITY.md`, `PRIVACY.md`, `ARCHITECTURE_DESIGN.md`) + domain areas.
  - **Team topologies:** Pool / Squad / Hybrid with tradeoffs and a concrete 15-person example.
  - **Docs SSoT choice matrix** over 7 options × 4 team sizes (Solo / Small / Medium / Large) with scaling indicators.
  - **Four-eyes convention** for `review-ok` / `privacy-ok` with an audit-trace example.
  - **Skill pool governance** with a maintenance-owner role, drift audits, skill quarantine for external skills.
  - **Conflict escalation** with 3 stages (CODEOWNERS → squad lead → lead architect veto).
  - **10-step setup guide** "How do you set up INTENTRON in a 20-person team?" — extends Appendix P scenario 3 (Multi-User-VPS coding factory).
  - "What Appendix R does not do" section with hard delimitations.
- **Excalidraw sketch `docs/assets/boo-72-multi-operator-3-layer.png`** with OWLIST colors — visualizes the 3-layer model with fan-in (code), Kanban strip (coordination) and side-by-side trio (docs SSoT choice). The bootstrap callout shows the link to question B.3 (docs SSoT) and A.7 (deployment).

## Concrete Changes

| Area | Change | File |
|---|---|---|
| HANDBUCH appendix R NEW | Multi-operator coordination (DE) | `HANDBUCH.md` from line 3491 |
| HANDBUCH Appendix R NEW | Multi-operator coordination (EN) | `HANDBUCH.en.md` from line 2974 |
| Sketch NEW | Excalidraw + PNG export | `docs/assets/boo-72-multi-operator-3-layer.excalidraw` + `.png` |
| Spec NEW (committed in Wave K `213bd46`) | Spec BOO-72 with operator question + 3-layer model + decision matrix | `specs/BOO-72.md` |
| Migration | `migrate_boo_72()` (doc-only hint block, idempotent) | `bootstrap/scripts/migrate-to-v2.sh` |
| Migration checklist | §BOO-72 (DE+EN) | `bootstrap/references/migration-checklist-v1-to-v2.md` + `.en.md` |
| ALL_ISSUES array | `BOO-72` added | `bootstrap/scripts/migrate-to-v2.sh` |

## Skill Version Bumps

None. Wave L is a pure docs story.

## Migration for Existing Projects

`migrate_boo_72()` in `bootstrap/scripts/migrate-to-v2.sh`:

```bash
bash bootstrap/scripts/migrate-to-v2.sh --issue BOO-72
```

Doc-only, no file operation. The auto-step outputs operator hints:

- Read HANDBUCH appendix R / Appendix R
- Note team size + pattern choice in `migration-status.md` under §BOO-72
- From 5 operators: create `.github/CODEOWNERS`
- From 10 operators: document the four-eyes convention + conflict escalation path in `CONVENTIONS.md`

Operator action: read HANDBUCH appendix R once, apply the conventions depending on team size. For solo or teams under 5: entry with status `✗ — team size below the Appendix-R threshold`.

## Design Decision: Inspiration Layer, Not Framework Enforcement

Appendix R closes a real docs gap (sales obstacle on team mandates), **without** extending the framework. That is the INTENTRON philosophy "lightweight + pragmatic":

- No new skill, no new bootstrap question — the framework already does enough.
- Pattern options are tradeoff tables, not recommendation verdicts.
- Four-eyes enforcement deliberately NOT implemented — operator discipline stays operator discipline.
- No "best practice" determination for Confluence vs. Notion vs. SharePoint — the operator chooses.

## Still Open / Follow-ups

- **Wave M (BOO-73):** Take DPO + security-architect into the framework bundle (vendored copies). Correction of the Wave-J decision "DPO stays standalone" — if the framework wants to guarantee Privacy-by-Design, the DPO skill must be installable from the framework repo. The spec is created directly following Wave L.
- **Example audit:** a real 15+ operator setup (consulting mandate? in-house?) would be a good "show, don't tell" follow-up step to verify Appendix R. Own spec due.

## References

- Spec: `specs/BOO-72.md` (committed in Wave K `213bd46`)
- HANDBUCH: Appendix R Multi-operator coordination (DE+EN)
- Sketch: `docs/assets/boo-72-multi-operator-3-layer.png`
- Migration: `bootstrap/scripts/migrate-to-v2.sh` (`migrate_boo_72`)
- Migration checklist: §BOO-72 (DE+EN)
- Feedback source: Operator Tobias, 2026-05-27 (post-Wave-K session)
- Linear: <https://linear.app/owlist/issue/BOO-72/>
- Previous wave: `docs/releases/wave-k-deployment-and-sovereignty.md`
