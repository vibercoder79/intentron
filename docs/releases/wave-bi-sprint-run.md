# Wave BI — /sprint-run: Sprint-Orchestrator für vollautomatische Sprints (BOO-157)

**Was jetzt da ist:** Ein neuer Orchestrator-Skill `/sprint-run` fährt einen ganzen Sprint vollautomatisch — er wählt Stories aus dem priorisierten Backlog, setzt jede per `/implement` im Daemon-Modus um (eigener `git worktree` + Branch), pflegt den Linear-Status, wartet auf grüne Remote-CI, merged, räumt auf und triggert am 80%-Token-Boundary `/sprint-review`. Reiner Orchestrator — `/implement`, `/backlog`, `/sprint-review` bleiben unverändert. Vollständige Doku inkl. HANDBUCH-Kapitel, Runbook und 5 Owlist-Sketches. DE+EN.

## Stories
- **BOO-157** — neuer Skill `sprint-run/` + Doku-Vollausbau (HANDBUCH Anhang AD, Runbook, 5 Sketches, README-Cross-Refs).

## Änderungen (DE+EN)
- **Neu `sprint-run/SKILL.md` / `.en.md`** (v1.0.0): Workflow Schritte 0–7 — Environment, Sprint-Pre-Flight (HARD GATE), Token-Budget (80%), Daemon-Loop pro Story (worktree → `/implement` → Remote-CI → Merge → Linear → Cleanup), Gate-Block-Pause, Sprint-Boundary → `/sprint-review`, Sprint-Report. Daemon-Modus (`--auto`).
- **Neu `sprint-run/README.md` / `.en.md`** + `references/` (orchestration-checklist, gate-block-handling, worktree-flow, token-boundary; je DE+EN).
- **Neu 5 Owlist-Sketches** (`.excalidraw` + `.png`, DE+EN) + `overview`: Sprint-Run-Flow, Story-Breakdown, Agent-Interaktion, GitHub-Integration, Gate-Block-Handling.
- **`HANDBUCH.md` / `.en.md`**: `/sprint-run`-Eintrag in §6 + neues **Anhang AD** mit allen 5 Sketches und den Pflicht-Texten (Was/Wann/Ablauf/Gate-Block/Token-Boundary/GitHub/Fehler/Konfiguration).
- **Neu `docs/runbooks/sprint-run.md` / `.en.md`**: komplette Skill-Kette `intent → ideation → backlog → sprint-run → implement → sprint-review`, Beispiel-Session, Pre-Sprint-Checkliste, Fehlerszenarien.
- **READMEs** von `/backlog`, `/implement`, `/sprint-review`, `/ideation`: Cross-Reference auf `/sprint-run` (ohne Versions-Bump, DE+EN).

## Wirkung
Ein Sprint muss nicht mehr Story für Story von Hand gesteuert werden. Der Operator startet `/sprint-run`, der Daemon fährt den ganzen Sprint — mit Worktree-Isolation pro Story, automatischem Linear-Status, CI-Wait und sauberem Sprint-Abschluss. Governance bleibt strikt: Gate-Blocks pausieren und werden nie automatisch überbrückt, kein Merge ohne grüne CI.

## Abgrenzung
- Reiner Orchestrator: die orchestrierten Skill-Logiken bleiben unverändert (nur README-Cross-Ref).
- `change_type: tooling` — Framework-internes Developer-Tool, keine User-Daten, keine externe API.
- Wave-Buchstabe **bi** (bf = BOO-155, bg = BOO-156). Repo-Slot BOO-157 = Linear BOO-157 (Linear-first, kein Offset).
- BOO-148 (Remote-CI-Loop) = nicht-blockierende Abhängigkeit, bereits Done (v0.9.0).

## Verweise
Spec: `specs/BOO-157.md`. Branch: `feat/boo-157-sprint-run`. Skill: `sprint-run/SKILL.md`. Runbook: `docs/runbooks/sprint-run.md`. HANDBUCH Anhang AD. Verwandt: BOO-148 (Remote-CI-Loop), Anhang G (Sprint-Sizing). Operator-Quelle: Tobias, 2026-06-05.
