<a name="deutsch"></a>

# Sprint-Run — Sprint-Orchestrator fuer vollautomatische Sprint-Ausfuehrung

> Faehrt einen ganzen Sprint ohne manuelle Story-by-Story-Steuerung: waehlt Stories aus dem
> priorisierten Backlog, setzt jede per `/implement` im Daemon-Modus um (eigener `git worktree`
> + Branch), pflegt den Linear-Status, wartet auf gruene Remote-CI, merged, raeumt auf und
> triggert am 80%-Token-Boundary `/sprint-review`. Reiner Orchestrator — die orchestrierten
> Skills bleiben unveraendert.

**Version:** 1.0.0 · **Befehl:** `/sprint-run`

---

## Was der Skill tut

Ohne Orchestrator wird ein Sprint manuell gefahren: `/implement` aufrufen, Story waehlen,
warten, naechste Story, Linear nachpflegen, Worktrees von Hand verwalten. `/sprint-run`
automatisiert genau diese Mechanik.

Der Skill verkettet die bereits vorhandenen Bausteine — `/implement`-Daemon-Modus,
Execution-Isolation (Worktree), Token-Pre-Flight, Remote-CI-Loop (BOO-148) — zu einem
durchgehenden Sprint-Lauf. Er schreibt **keinen** Produktcode und veraendert `/implement`,
`/backlog`, `/sprint-review` nicht.

---

## Wie er funktioniert

| # | Schritt | Zweck |
|---|---------|-------|
| 0 | Environment + Sprint-Kontext laden | Thresholds, Adapter, Daemon-Modus erkennen |
| 1 | **Sprint-Pre-Flight** ⛔ | Backlog priorisiert? Specs vollstaendig? Gates gruen? Werkzeug bereit? |
| 2 | Sprint-Token-Budget planen | 80%-Budget, Reihenfolge nach Abhaengigkeit + Prioritaet |
| 3 | Sprint-Plan + Operator-Freigabe | Daemon-Modus ueberspringt die Freigabe |
| 4 | **Daemon-Loop pro Story** | Worktree → `/implement` → CI-Wait → Merge → Linear → Cleanup |
| 5 | Fehlerbehandlung | Story zurueck, `daemon_fail_policy` (stop/continue) |
| 6 | Sprint-Boundary → `/sprint-review` | bei 80% Token / Backlog leer / stop-on-fail |
| 7 | Sprint-Report | Tabelle: Stories, Token, CI, Worktrees |

---

## Gate-Block-Sicherheit (kritisch)

Loest `/implement` ein **Sensitive-Paths-** oder **Personal-Data-Gate** aus, **pausiert** der
Daemon und benachrichtigt den Operator (Story-ID + Grund). Resume nur nach explizitem
`review-ok` / `privacy-ok`. **Kein** automatischer Bypass, **kein** Timeout-Resume — auch im
`--auto`-Modus.

---

## Abgrenzung zu `/implement`

| | `/implement` | `/sprint-run` |
|---|---|---|
| Umfang | **eine** Story | **N** Stories (ganzer Sprint) |
| Worktrees | — (laeuft im aktuellen Baum) | eigener Worktree + Branch pro Story |
| Sprint-Ende | — | 80%-Token-Boundary → `/sprint-review` |
| Aufruf | direkt | orchestriert `/implement` pro Story |

---

## Trigger-Phrasen

- `/sprint-run`
- "Sprint laufen lassen"
- "fahr den Sprint"
- "automation-cycle"

---

## Schnittstellen zu anderen Skills

| Upstream | Was geliefert wird | Downstream | Was wir liefern |
|----------|--------------------|------------|------------------|
| `backlog` | Priorisierte Sprint-Liste | `implement` (pro Story) | Story-ID, Worktree, Daemon-Trigger |
| `ideation` | Stories + Specs + ADD | `sprint-review` (Sprint-Ende) | Aggregierte Story-Metriken |

Kette: `intent → ideation → backlog → sprint-run → ( implement )* → sprint-review`.

---

## Installation

```bash
cp -r sprint-run ~/.claude/skills/sprint-run
```

Voraussetzung: `git worktree` verfuegbar, `gh` authentifiziert (Remote-CI-Wait), und die
Geschwister-Skills `backlog`, `implement`, `sprint-review` installiert.

---

## Dateistruktur

```
sprint-run/
├── SKILL.md                                  ← Skill-Definition
├── SKILL.en.md                               ← English Mirror
├── README.md / README.en.md                  ← diese Datei (+ EN)
├── overview.excalidraw / .png (+ .en)        ← Skill-Overview-Sketch
└── references/
    ├── orchestration-checklist.md   (+ .en.md)  ← Sprint-Pre-Flight + Loop-Checks
    ├── gate-block-handling.md       (+ .en.md)  ← Pause/Resume-Protokoll
    ├── worktree-flow.md             (+ .en.md)  ← Worktree pro Story
    └── token-boundary.md            (+ .en.md)  ← 80%-Boundary-Logik
```

---

## Sketches

Alle Diagramme im Owlist Design System (siehe HANDBUCH Anhang AD):

- `overview.png` — Skill-Overview (dieser Skill auf einen Blick)
- `docs/sprint-run-flow.png` — Sprint-Run-Flow (Daemon-Loop Start → Sprint-Ende)
- `docs/story-breakdown.png` — Story-Breakdown (Worktree → Implement → CI → Merge → Cleanup)
- `docs/agent-interaction.png` — Agent-Interaktion (backlog ↔ sprint-run ↔ implement ↔ sprint-review)
- `docs/github-integration.png` — GitHub-Integration (Story → Branch → PR → CI-Run)
- `docs/gate-block-handling.png` — Gate-Block-Zustandsmaschine (laufend → Gate → pausiert → resumed)
