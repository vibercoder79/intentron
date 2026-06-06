# Wave BK — /sprint-run: Post-Story-Gate-Assertion (BOO-165)

**Was jetzt da ist:** `/sprint-run` verifiziert nach jedem Story-Lauf **maschinell** gegen die `meta.json`, dass kein Pflicht-Gate still übersprungen wurde — neuer **Schritt 4.5b** zwischen Remote-CI-Wait und Merge. Härtet die bisher rein prompt-getriebene Gate-Durchsetzung. `sprint-run` v1.0.0 → v1.1.0. DE+EN.

## Stories
- **BOO-165** — Schritt 4.5b Post-Story-Gate-Assertion + Doku-/Sketch-Nachzug.

## Änderungen (DE+EN)
- **`sprint-run/SKILL.md` (+EN)**: neuer Schritt 4.5b (Tabellenzeile + Abschnitt + Legitimitäts-Matrix); Daemon-Modus-Hinweis; **v1.0.0 → 1.1.0**.
- **Neu `sprint-run/references/gate-assertion.md` (+EN)**: Assertion-Logik, Legitimitäts-Regel, Pseudocode.
- **`sprint-run/README.md` (+EN)**: Gate-Assertion-Abschnitt + Schritt-Tabelle; v1.1.0.
- **HANDBUCH Anhang/Appendix AD (DE+EN)**: 4.5b in der Daemon-Loop-Tabelle, Abschnitt „Gate-Assertion", Fehlerbehandlung erweitert.
- **`docs/runbooks/sprint-run.md` (+EN)**: Fehlerszenario „unbegründeter Gate-Skip → Story zurück".
- **Sketches aktualisiert (DE+EN)**: `sprint-run-flow` + `story-breakdown` — Assertion-Knoten zwischen CI und Merge.

## Wirkung
Ein still übersprungener Lint-/Test-/Security-Check kann den Sprint nicht mehr unbemerkt passieren: zur prompt-getriebenen Gate-Ausführung (Ebene 1) und zum Remote-CI-Gate (BOO-148, Ebene 2) kommt die maschinelle Verifikation gegen `meta.json` als Backstop für Ebene 1.

## Abgrenzung
Reiner Orchestrator-Zusatz; `/implement`, `/backlog`, `/sprint-review` unverändert (es wird nur `meta.json` gelesen). `change_type: tooling`. Non-Code-Skips bleiben legitim (change_type-aware). Wave-Buchstabe **bk** (bi = sprint-run BOO-157, bj = role-runbooks BOO-158, bh = knowledge-onboarding-sketches). Enthält zusätzlich den Hotfix `wave bi→bj` für role-runbooks (Cross-Session-Kollision mit dem bereits released `wave-bi-sprint-run` aufgelöst).

## Verweise
Spec: `specs/BOO-165.md`. Branch: `feat/boo-165-gate-assertion`. Skill: `sprint-run/SKILL.md` (4.5b) + `references/gate-assertion.md`. HANDBUCH Anhang AD. Verwandt: BOO-157 (`/sprint-run`), BOO-148 (Remote-CI-Loop), BOO-36/84 (`meta.json`). Operator-Quelle: Tobias, 2026-06-06.
