# Wave BI — /sprint-run: sprint orchestrator for fully automatic sprints (BOO-157)

**What's now in place:** A new orchestrator skill `/sprint-run` runs a whole sprint fully automatically — it picks stories from the prioritized backlog, implements each via `/implement` in daemon mode (its own `git worktree` + branch), maintains Linear status, waits for green remote CI, merges, cleans up and triggers `/sprint-review` at the 80% token boundary. Pure orchestrator — `/implement`, `/backlog`, `/sprint-review` stay unchanged. Full docs incl. HANDBUCH chapter, runbook and 5 Owlist sketches. DE+EN.

## Stories
- **BOO-157** — new skill `sprint-run/` + full docs (HANDBUCH Appendix AD, runbook, 5 sketches, README cross-refs).

## Changes (DE+EN)
- **New `sprint-run/SKILL.md` / `.en.md`** (v1.0.0): workflow steps 0–7 — environment, sprint pre-flight (HARD GATE), token budget (80%), daemon loop per story (worktree → `/implement` → remote CI → merge → Linear → cleanup), gate-block pause, sprint boundary → `/sprint-review`, sprint report. Daemon mode (`--auto`).
- **New `sprint-run/README.md` / `.en.md`** + `references/` (orchestration-checklist, gate-block-handling, worktree-flow, token-boundary; DE+EN each).
- **New 5 Owlist sketches** (`.excalidraw` + `.png`, DE+EN) + `overview`: sprint-run flow, story breakdown, agent interaction, GitHub integration, gate-block handling.
- **`HANDBUCH.md` / `.en.md`**: `/sprint-run` entry in §6 + new **Appendix AD** with all 5 sketches and the mandatory texts (what/when/flow/gate-block/token-boundary/GitHub/errors/configuration).
- **New `docs/runbooks/sprint-run.md` / `.en.md`**: full skill chain `intent → ideation → backlog → sprint-run → implement → sprint-review`, example session, pre-sprint checklist, failure scenarios.
- **READMEs** of `/backlog`, `/implement`, `/sprint-review`, `/ideation`: cross-reference to `/sprint-run` (no version bump, DE+EN).

## Impact
A sprint no longer has to be steered story by story. The operator starts `/sprint-run`, the daemon runs the whole sprint — with worktree isolation per story, automatic Linear status, CI wait and a clean sprint wrap-up. Governance stays strict: gate blocks pause and are never bypassed automatically, no merge without green CI.

## Scope
- Pure orchestrator: the orchestrated skill logic stays unchanged (README cross-ref only).
- `change_type: tooling` — framework-internal developer tool, no user data, no external API.
- Wave letter **bi** (bf = BOO-155, bg = BOO-156). Repo slot BOO-157 = Linear BOO-157 (Linear-first, no offset).
- BOO-148 (remote-CI loop) = non-blocking dependency, already Done (v0.9.0).

## References
Spec: `specs/BOO-157.md`. Branch: `feat/boo-157-sprint-run`. Skill: `sprint-run/SKILL.md`. Runbook: `docs/runbooks/sprint-run.en.md`. HANDBUCH Appendix AD. Related: BOO-148 (remote-CI loop), Appendix G (sprint sizing). Operator source: Tobias, 2026-06-05.
