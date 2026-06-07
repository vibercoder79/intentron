# Wave BS — Runbook: run a sprint unattended on the VPS with tmux (BOO-172)

**What's there now:** A new runbook explains how to start `/sprint-run` (or any long-running Claude work) on the VPS inside **`tmux`** so it **survives closing the laptop / an SSH drop**. Deliberately **instead of** a fully executable VPS daemon (too big an overhaul for the benefit) — built-in tools are enough.

## Stories
- **BOO-172** — runbook "run a sprint unattended with tmux" (DE+EN + sketch).

## Changes
- **New `docs/runbooks/sprint-unattended-tmux.md` (+ `.en.md`):** problem (session tied to SSH → laptop closed = agent dead) → fix (tmux) → 5 steps → cheatsheet → "when needed" → deliberate limit (no daemon).
- **New sketch `sprint-unattended-tmux.{excalidraw,png}` (+ `.en.*`):** "without tmux (dies) vs. with tmux (keeps running)", built in the render loop + embedded.
- **Linked:** from `docs/runbooks/sprint-run.{md,en.md}` (references) + `docs/onboarding/artefakt-landkarte.{md,en.md}` (runbook list).

## Scope decisions
- **Only the simple tmux recommendation** — the SSH host-alias / auto-tmux configuration was deliberately left out (too fiddly, and it breaks VS Code Remote-SSH).
- Mac terminal **or** VS Code terminal are equivalent; applies to any long-running remote work, not just sprints.

## Effect
A clear, linked guide for "start the sprint, close the Mac, it keeps running" — no daemon, no config fiddling.

## Scope
Docs only. The fully executable VPS daemon (variant B, cron/systemd: scheduled auto-start, self-healing, reboot persistence) stays **deliberately unbuilt** — only if genuinely needed. Wave letter **bs** (br = implement haiku loops BOO-171).

## References
Spec: `specs/BOO-172.md`. Branch: `feat/boo-172-runbook-tmux-vps`. Related: BOO-170/171 (model-routing chain), BOO-157 (sprint-run), `hostinger-vps-setup`/`multi-user-vps` (VPS basics). Operator source: Tobias, 2026-06-07.
