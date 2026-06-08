# Release Notes — Wave G Security-Workflow-Sketch

> 🌐 **Sprache:** Deutsch (diese Datei) · [🇬🇧 English](wave-g-security-workflow-sketch.en.md)

Stand: 2026-05-19

## Zweck

Wave G ergaenzt BOO-63. Das Security-Dokumentationsmodell aus Wave F ist jetzt auch visuell als Excalidraw-Sketch vorhanden.

## Betroffene Story

- BOO-63

## Neue Artefakte

- `docs/security-workflow.excalidraw`
- `docs/security-workflow.en.excalidraw`

## Inhalt des Sketches

Der Sketch zeigt:

- `ARCHITECTURE_DESIGN.md` als Lead-Vertrag,
- `SECURITY.md` als operativen Security-Vertrag,
- Security-Unterartefakte wie `API_INVENTORY.md`, `.semgrep.yml`, Runtime-Hooks, sensitive paths, Threat Models und Privacy-/Compliance-Dokumente,
- die Skill-Pipeline `/ideation` -> `/implement` -> `/security-architect` -> `/architecture-review` -> `/sprint-review`,
- den Rueckfluss wiederkehrender Findings in den Learning Loop,
- die harte Regel, dass Secrets, Tokens, Cookies und private Session-Daten nie geschrieben werden.

## Handbuch

`HANDBUCH.md` verweist im Abschnitt Security-Dokumentationsmodell auf die DE/EN-Excalidraw-Quellen.

## Offene Folgearbeit

- Optional: PNG-Exports erzeugen, wenn der Sketch direkt im GitHub-README oder in Praesentationen eingebettet werden soll.
