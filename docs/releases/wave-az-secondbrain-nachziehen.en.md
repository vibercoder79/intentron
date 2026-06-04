# Wave AZ — Runbook "Retrofit the SecondBrain" (BOO-144)

**What's now in place:** a dedicated, HANDBUCH-linked runbook for the **fourth onboarding path** — "framework already installed, but I want to retrofit **only** the lightweight SecondBrain setup (BOO-138/139), without re-running `/bootstrap`". At its core is a ready, **idempotent operator prompt** (Read-before-Edit, path confirmation, no secret) that adds `PROJECTS_ROOT` to the global `~/.claude/CLAUDE.md` and retrofits existing projects with `journal/daily/` + session-start/end routine. A customer-ready self-service path. DE+EN + sketch.

## Stories

- **BOO-144** — runbook `docs/runbooks/secondbrain-nachziehen.md` (+ `.en.md`) with the operator prompt; HANDBUCH Appendix U "path 4"; sketch (DE+EN).

## Changes (DE+EN)

- **New:** `docs/runbooks/secondbrain-nachziehen.md` + `.en.md` — context, "what it does" (machine level `PROJECTS_ROOT` + project level `journal/daily/`), ready operator prompt (DE prompt / EN prompt), safety & idempotency, "afterwards", references.
- **New:** sketch `docs/assets/secondbrain-nachziehen.{excalidraw,png}` (+ `.en.*`) — BEFORE → operator prompt → AFTER (two levels) + daily-note loop; OWLIST colours, render loop, Read-verified.
- **`HANDBUCH.md` Appendix U:** new "path 4 — retrofit just the SecondBrain (no re-bootstrap)" + runbook in the related appendices.

All changes are DE+EN parity.

## Scope boundary

No new skill, no skill-logic change — pure docs + sketch + one operator prompt. Builds on BOO-138/139 (`v0.8.0`).

## References

Spec: `specs/BOO-144.md`. Branch: `feat/boo-144-secondbrain-nachziehen`. Builds on: BOO-138/139 (`v0.8.0`), HANDBUCH Appendix U (multi-project operation), `docs/how-we-document.md`. Operator source: Tobias, 2026-06-04.
