# Release Notes — Wave D Sketches

Stand: 2026-05-19

## Zweck

Wave D schliesst BOO-59 visuell ab. Die bisher textlich beschriebenen Codex-, Cross-Tool-, Validate-Fix-Learn-, Provider- und Upgrade-Sichten liegen jetzt als Excalidraw-Quellen im Olli Corporate Design vor.

## Betroffene Story

- BOO-59

## Umgesetzte Schwerpunkte

### Runtime-spezifische Artifact Maps

Die Codex Artifact Map trennt klar zwischen:

- `AGENTS.md`, `CONVENTIONS.md` und `ARCHITECTURE_DESIGN.md` als Projektvertrag,
- `.codex/skills`, `.codex/hooks.json` und `.codex/config.toml` als Codex-Runtime,
- `CLAUDE.md` und `.claude/*` als Kompatibilitaetsbruecke,
- `specs/`, `intents/`, `journal/` und `docs/releases/` als Evidenzspur.

Die Cross-Tool Map zeigt denselben Vertrag als gemeinsame Mitte fuer Claude Code, Codex und weitere Tool-Adapter.

### Validate-Fix-Learn als sichtbarer Loop

Der Implement-Workflow ist jetzt nicht nur textlich, sondern auch visuell als Schleife dokumentiert:

`Validate -> Interpret -> Decide -> Fix -> Re-Validate -> PASS/FAIL -> Learn`

Damit ist sichtbar, dass `/implement` nicht nach dem ersten Toollauf endet. Abschluss gibt es erst bei PASS oder dokumentierter Operator-Freigabe.

### Folge-Sichten fuer BOO-58 und BOO-60 vorbereitet

BOO-59 liefert ausserdem die visuellen Grundlagen fuer die naechsten operativen Schritte:

- Provider-Postflight-Matrix fuer BOO-58,
- Upgrade-Pfad bestehender Projekte fuer BOO-60,
- Runtime-Entscheidungsbaum fuer toolneutrale Bootstrap-Entscheidungen,
- Backlog-Record/Adapter-Modell fuer Linear, GitHub Issues und lokale Backlogs.

## Neue Artefakte

Deutsch:

- `docs/artifact-map-codex.excalidraw`
- `docs/artifact-map-cross-tool.excalidraw`
- `docs/runtime-decision-tree.excalidraw`
- `docs/backlog-record-adapter-model.excalidraw`
- `docs/validate-fix-learn.excalidraw`
- `docs/provider-postflight-matrix.excalidraw`
- `docs/upgrade-path-existing-projects.excalidraw`

Englisch:

- `docs/artifact-map-codex.en.excalidraw`
- `docs/artifact-map-cross-tool.en.excalidraw`
- `docs/runtime-decision-tree.en.excalidraw`
- `docs/backlog-record-adapter-model.en.excalidraw`
- `docs/validate-fix-learn.en.excalidraw`
- `docs/provider-postflight-matrix.en.excalidraw`
- `docs/upgrade-path-existing-projects.en.excalidraw`

## Offene Folgearbeit

- PNG-Exports erzeugen, wenn die Sketches direkt in README, GitHub Preview oder Praesentationen eingebettet werden sollen.
- Provider-Postflight aus BOO-58 als maschinenlesbare Checkliste operationalisieren.
- Upgrade-Pfad aus BOO-60 als konkreten `inspect/apply-safe/apply-with-confirmation`-Ablauf operationalisieren.
