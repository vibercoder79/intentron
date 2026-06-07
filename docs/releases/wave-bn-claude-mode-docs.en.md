# Wave BN — Claude Code mode recommendation + /sprint-run "two modes" (BOO-168)

> 🌐 **Language:** English (this file) · [🇩🇪 Deutsch](wave-bn-claude-mode-docs.md)

**What's now in place:** Clarification that **`/sprint-run` itself executes** (with a one-time plan approval) and **`--auto` only drops that approval** — both actually run the sprint, there is no "check-only" mode. Plus a new **HANDBUCH §6 section** on which **Claude Code permission mode** fits which skill, and the distinction **skill plan ≠ Claude Code plan mode** (read-only, blocks execution). Docs only — `sprint-run` stays v1.1.0. DE+EN.

## Stories
- **BOO-168** — mode recommendation + two-modes clarification.

## Changes (DE+EN)
- **HANDBUCH §6 (DE+EN)**: new section "Claude Code mode: which permission mode for which skill?" — thinking skills → `plan`; execution supervised → `acceptEdits`; unattended (`--auto`) → `dontAsk` + allowlist (`bypassPermissions` only isolated); never plan mode for execution; distinction + safety net.
- **`sprint-run/README` (DE+EN)**: "Two modes" block (default vs `--auto`, both execute) + plan-mode distinction + Claude Code mode recommendation.
- **`sprint-run/SKILL` (DE+EN)**: daemon-mode section softened (the default loop also runs through after approval) + mode blockquote.
- **`docs/runbooks/sprint-run` (DE+EN)**: "both execute" clarification + mode tip.
- **`implement/README` (DE+EN)**: Claude Code mode line (same `--auto` logic).

## Impact
No more confusion of "`/sprint-run` only checks / `--auto` executes" or of skill plan vs. Claude Code plan mode. Users know which Claude Code mode to pick per skill phase.

## Scope
Docs only, no code, **no version bump**. Mode facts verified against the official Claude Code docs (6 modes; plan mode read-only). Wave letter **bn** (bm = sprint-run-readme BOO-166).

## References
Spec: `specs/BOO-168.md`. Branch: `feat/boo-168-claude-mode-docs`. Related: BOO-157 (`/sprint-run`), BOO-165 (gate assertion), BOO-166 (README overhaul). Operator source: Tobias, 2026-06-06.
