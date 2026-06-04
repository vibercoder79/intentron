# Wave AZ — Runbook „SecondBrain nachziehen" (BOO-144)

**Was jetzt da ist:** ein eigenes, aus dem HANDBUCH verlinktes Runbook für den **vierten Onboarding-Weg** — „Framework schon installiert, will aber **nur** das Leichtgewicht-SecondBrain-Setup (BOO-138/139) nachziehen, ohne `/bootstrap` neu zu fahren". Kern ist ein fertiger, **idempotenter Operator-Prompt** (Read-vor-Edit, Pfad-Bestätigung, kein Secret), der die globale `~/.claude/CLAUDE.md` um `PROJECTS_ROOT` ergänzt und bestehende Projekte um `journal/daily/` + Session-Start-/Ende-Routine nachrüstet. Kundentauglicher Self-Service-Pfad. DE+EN + Sketch.

## Stories

- **BOO-144** — Runbook `docs/runbooks/secondbrain-nachziehen.md` (+ `.en.md`) mit Operator-Prompt; HANDBUCH Anhang U „Weg 4"; Sketch (DE+EN).

## Änderungen (DE+EN)

- **Neu:** `docs/runbooks/secondbrain-nachziehen.md` + `.en.md` — Kontext, „Was es bewirkt" (Maschinen-Ebene `PROJECTS_ROOT` + Projekt-Ebene `journal/daily/`), fertiger Operator-Prompt (DE-Prompt / EN-Prompt), Sicherheit & Idempotenz, „Danach", Verweise.
- **Neu:** Sketch `docs/assets/secondbrain-nachziehen.{excalidraw,png}` (+ `.en.*`) — VORHER → Operator-Prompt → NACHHER (2 Ebenen) + Daily-Note-Loop; OWLIST-Farben, Render-Loop, Read-verifiziert.
- **`HANDBUCH.md` Anhang U:** neuer „Weg 4 — Nur SecondBrain nachziehen (ohne Re-Bootstrap)" + Runbook in den Verwandten Anhängen.

Alle Änderungen DE+EN-paritätisch.

## Abgrenzung

Kein neuer Skill, keine Skill-Logik-Änderung — reine Doku + Sketch + ein Operator-Prompt. Baut auf BOO-138/139 (`v0.8.0`) auf.

## Verweise

Spec: `specs/BOO-144.md`. Branch: `feat/boo-144-secondbrain-nachziehen`. Anknüpfung: BOO-138/139 (`v0.8.0`), HANDBUCH Anhang U (Multi-Projekt-Betrieb), `docs/how-we-document.md`. Operator-Quelle: Tobias, 2026-06-04.
