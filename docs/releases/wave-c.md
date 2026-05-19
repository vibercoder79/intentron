# Release Notes — Wave C

Stand: 2026-05-19

## Zweck

Wave C dokumentiert die offenen Provider-, Diagramm- und Upgrade-Aspekte aus dem Dry-Run so, dass sie in der naechsten Umsetzung nicht wieder verschwimmen. Der erste Schnitt hielt die visuellen Artefakte als Folgearbeit fest; BOO-59 ergaenzt jetzt die Excalidraw-Quellen im Olli Corporate Design.

## Betroffene Stories

- BOO-58
- BOO-59
- BOO-60

## Umgesetzte Schwerpunkte

### Provider sind nicht automatisch einsatzbereit

Bootstrap darf lokale Skill-Dateien nicht mit externen Provider-Verbindungen verwechseln. GitHub, Linear, Jira, Azure DevOps, Planner, SonarQube, Grafana, Miro, Telegram, Obsidian-Sync, Research-Provider und Hosting-Plattformen brauchen eigene Statuswerte:

- `OK`
- `WARN`
- `SKIP bewusst`
- `FAIL`

Secrets werden dabei nie angezeigt oder in Dateien geschrieben.

### Upgrade-Pfad fuer bestehende Projekte

Bestehende Projekte werden nicht ueberschrieben. Der sichere Pfad lautet:

1. `inspect` — Bestand lesen, Diff und Risiken zeigen.
2. `apply-safe` — nur additive, idempotente Aenderungen einspielen.
3. `apply-with-confirmation` — bestehende Regeln, Hooks, CI, Templates, Adapter und Skill-Versionen nur nach Bestaetigung aendern.

### Diagramm-Folgearbeit

BOO-59 zieht die visuellen Sichten als Excalidraw-Quellen nach:

- Codex Artifact Map: `docs/artifact-map-codex.excalidraw`
- Cross-Tool Artifact Map: `docs/artifact-map-cross-tool.excalidraw`
- Runtime-Entscheidungsbaum: `docs/runtime-decision-tree.excalidraw`
- Backlog-Record/Adapter-Modell: `docs/backlog-record-adapter-model.excalidraw`
- Validate-Fix-Learn-Schleife: `docs/validate-fix-learn.excalidraw`
- Provider-Postflight-Matrix: `docs/provider-postflight-matrix.excalidraw`
- Upgrade-Pfad bestehender Projekte: `docs/upgrade-path-existing-projects.excalidraw`

Alle sieben Skizzen liegen auch als englische `.en.excalidraw`-Varianten vor. PNG-Exports bleiben ein optionaler Publishing-Schritt, wenn die Bilder fuer README, GitHub oder Praesentationen gerendert werden sollen.

## Referenz-Matrix

| Referenz | Wave-C-Bezug |
|---|---|
| F003 | Monitoring/Logging braucht Plattform- und Provider-Kontext |
| F011 | Artifact Maps muessen Claude-, Codex- und Cross-Tool-Sicht unterscheiden |
| F020 | Research muss als Framework-Bestandteil oder Companion mit Providerstatus beschrieben werden |
| F021 | Visualize/Miro braucht MCP-Abfrage und Abschlussverifikation |
| F022 | Validate-Fix-Learn braucht eigene operative und visuelle Darstellung |
| BOO-60 | Upgrade-Pfad fuer bestehende Projekte dokumentiert |

## Geaenderte Artefakte in diesem Schnitt

- `HANDBUCH.md`
- `bootstrap/SKILL.md`
- `bootstrap/SKILL.en.md`
- `docs/*.excalidraw` fuer BOO-59
- `docs/releases/wave-c.md`

## Offene Folgearbeit

- Provider-Postflight ggf. als eigenes maschinenlesbares Template aus `bootstrap/SKILL.md` herausziehen.
- Upgrade-Report als Template in `bootstrap/references/` anlegen, sobald die Upgrade-Funktion nicht nur dokumentiert, sondern skriptbar wird.
