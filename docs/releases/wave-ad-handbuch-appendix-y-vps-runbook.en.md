# Wave AD — HANDBUCH Anhang Y: VPS/Cloud team runbook (BOO-94)

> 🌐 **Language:** English (this file) · [🇩🇪 Deutsch](wave-ad-handbuch-appendix-y-vps-runbook.md)

**Linear:** [BOO-94](https://linear.app/owlist/issue/BOO-94/) · Follow-up from the VPS team runbook PR #16

## Problem

The VPS team setup knowledge sat as a standalone runbook (`docs/runbooks/vps-team-setup.md`, DE, from
PR #16) — valuable, but **not part of the canonical HANDBUCH**: not linked from the
table of contents, not bilingual, without a diagram. The remaining deployment/
operations topics (Anhänge P deployment scenarios, Q sovereignty, R multi-operator,
S skill installation, T verification, U multi-project, V bodyguard) are, by contrast, numbered,
DE+EN-parity appendices with cross-references. The VPS team lifecycle
(once-per-VPS → per-project → team) is exactly the link between §8d, P and U and belongs
as Anhang Y in the same series. Two parallel sources would be a drift risk.

## What changes

- **Anhang Y "VPS/Cloud-Team-Runbook"** in `HANDBUCH.md` (DE) **and** `HANDBUCH.en.md` (EN), strictly
  parity, linked in the table of contents (appendix overview). Subsections Y.1–Y.8:
  scenario/prerequisites, once-per-VPS, per-project (Git hooks per repo!), onboarding project
  2..N + brownfield (`migrate-to-v2.sh`), team (CODEOWNERS/branch protection), decisions
  (Docker vs. direct install, Git-local vs. GitHub, sovereignty), four-layer on headless VPS,
  quick reference. Synthesized in content from the runbook (appendix form, no 1:1 copy).
- **Excalidraw overview diagram** `docs/assets/vps-team-runbook.excalidraw` (+ `.en.excalidraw`
  + both `.png`, 6960×3680, style from `quality-gate-four-layers`): lifecycle VPS setup →
  project wiring → multi-project/team, with the once-per-VPS-vs-per-project separation
  ("Git hooks per repo") as the visual core. Embedded in both appendices, visually validated
  (3 render rounds).
- **Appendix index A–X → A–Y** (DE+EN parity): HANDBUCH appendix overview
  ("24 Anhaenge (A–X)" → "25 … (A–Y)", topic list extended by Y), README ("Anhaenge A–X" → "A–Y"
  including the list entry Y), CONVENTIONS ("Anhang A-X" → "A-Y").
- **Standalone runbook → pointer:** `docs/runbooks/vps-team-setup.md` reduced to a short reference to
  Anhang Y (no duplicated full text → no drift; file kept so as not to break
  PR #16 history/links — Decision 1).
- **Cross-references** §8d / Anhang P / Anhang U → Anhang Y added (DE+EN).

## Design decision

- **Anhang Y becomes canonical**, the standalone runbook becomes the pointer — no duplicate content,
  consistent with the single-source line BOO-89.
- **No content reinvention** — only promotion of the runbook content already documented in PR #16;
  all statements remain backed against appendices P/Q/R/S/T/U/V + §8d.
- **Bilingual + diagram DE+EN** (two variants + PNGs, analogous to `quality-gate-four-layers`) —
  brings the appendix to the level of P/Q/R/S/T/U/V.
- **Carry the index everywhere** (HANDBUCH overview, README, CONVENTIONS) — otherwise the
  same self-contradiction arises as before the four-layer doc sync (A–U vs. A–X).
- **Lightweight:** pure docs/diagram, no behavior change, no new dependency.

## Verified

- Anhang Y exists in HANDBUCH.md AND HANDBUCH.en.md, same H2/H3 structure, linked in the
  table of contents.
- `grep -rniE "A–X|A-X"` over README/CONVENTIONS/HANDBUCH* yields no outdated hits anymore;
  "25 Anhaenge / 25 appendices (A–Y)" consistent.
- Both diagram PNGs re-rendered, visually checked for overlap/layout.
- `docs/runbooks/vps-team-setup.md` no longer contains duplicated full text, but the
  pointer.
- Cross-references §8d/P/U → Y present (DE+EN).
- `git diff --check` clean; DE/EN parity checked.

## Rollout

Additive, pure docs/diagram. No behavior change, no migration needed. After merge, Anhang
Y is the canonical source; the standalone runbook remains as a pointer. Existing projects are
not affected.

## Effect

The operational knowledge for team VPS is now a first-class, more discoverable, bilingual
HANDBUCH component with a diagram — no longer a loose standalone doc.

## References

- Spec: `specs/BOO-94.md`
- Release overview: `docs/releases/v0.6.0-overview.md` (Wave AD)
- Anhang Y: `HANDBUCH.md` + `HANDBUCH.en.md`
- Diagram: `docs/assets/vps-team-runbook.excalidraw` (+ `.en.excalidraw` + both `.png`)
- Standalone pointer: `docs/runbooks/vps-team-setup.md`
- Builds on PR #16; index consistency ties to PR #14 (A–U → A–X)
- Linear: BOO-94
