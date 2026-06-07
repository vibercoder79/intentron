# Wave BT — Release notes networked: central wave index + DE↔EN language switch (BOO-173)

> 🌐 **Language:** English (this file) · [🇩🇪 Deutsch](wave-bt-release-index.md)

**What's there now:** The release notes (wave docs) are now **networked** instead of sitting loosely side by side. Triggered by an operator audit: "Are there DE+EN release notes for every merge, and are they networked?" — DE+EN was satisfied, the networking was missing.

## Changes
- **New `docs/releases/README.md` (+ `.en.md`):** central **release index** — lists **all waves** chronologically (newest first) with title + link (DE, EN where available). Explains the wave convention and how to add a new wave. With a DE↔EN language switch.
- **DE↔EN language switch** (`🌐`) added to the **6 most recent** wave pairs (wave-bn…bs, DE+EN) — analogous to the README/runbook convention.

## Audit finding (as of 2026-06-07)
- Release notes per merge of the last days (BOO-167…172): **complete DE+EN** (wave-bn…bs).
- Very early waves (wave-a…as) are **German only** — from before DE+EN parity; marked *(DE only)* in the index, EN backfill deliberately not part of this story.

## Scope
- Docs only, no code. No EN backfill of the old waves (separate optional follow-up). The index is static — new waves are added at the top manually (note is in the index). Wave letter **bt** (bs = tmux runbook BOO-172).

## References
Spec: `specs/BOO-173.md`. Branch: `feat/boo-173-release-index`. Related: BOO-167 (doc networking), BOO-172. Operator source: Tobias, 2026-06-07.
