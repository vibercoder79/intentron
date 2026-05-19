# Release Notes — Wave E Provider und Upgrade

Stand: 2026-05-19

## Zweck

Wave E operationalisiert BOO-58 und BOO-60. Bootstrap unterscheidet jetzt Skill-Installation von Provider-Bereitschaft und beschreibt einen sicheren Upgrade-Pfad fuer bestehende Projekte.

## Betroffene Stories

- BOO-58
- BOO-60

## Umgesetzte Schwerpunkte

### Provider-Postflight

Neu ist `bootstrap/references/provider-postflight.md` inklusive englischer Variante. Der Abschlussbericht muss GitHub, Backlog-Adapter, Research, Visualize/Miro, Monitoring und Obsidian separat ausweisen:

- `OK`: gewaehlt und verifiziert oder bewusst aktiv bestaetigt,
- `WARN`: Artefakt vorhanden, externe Verifikation fehlt,
- `SKIP`: bewusst nicht genutzt,
- `FAIL`: sollte aktiv sein, ist aber blockiert oder fehlgeschlagen.

Secrets werden nie angezeigt oder in Repo-Dateien, Chat, Logs, `.env.example` oder Abschlussberichte geschrieben.

### Monitoring, Research und Visualize

Bootstrap fragt nun operativ nach:

- zentraler oder projektlokaler Monitoring-/Logging-Plattform,
- Logging-Vertrag mit Pflichtfeldern und verbotenen Inhalten,
- Research-Quelle: Framework, Companion, global installiert oder nicht genutzt,
- Research-Provider: Perplexity MCP, Perplexity API, OpenRouter oder kein Provider,
- Visualize/Miro mit Miro-MCP-Pruefung und Fallback Excalidraw/Mermaid.

### Upgrade-Pfad

Neu ist `bootstrap/references/framework-upgrade.md` inklusive englischer Variante. Bestehende Projekte werden nicht neu bootstrapped und nicht blind ueberschrieben. Die drei Modi sind:

- `inspect`: nur lesen und Diff/Risiko/TODOs zeigen,
- `apply-safe`: nur neue Dateien oder fehlende Sektionen additiv ergaenzen,
- `apply-with-confirmation`: jede potenziell ueberschreibende Aenderung einzeln bestaetigen.

Der Upgrade-Report kann unter `journal/reports/framework-upgrade/YYYY-MM-DD.md` abgelegt werden und nutzt `docs/releases/` als Migrationsinput.

## Geaenderte Artefakte

- `bootstrap/SKILL.md`
- `bootstrap/SKILL.en.md`
- `bootstrap/README.md`
- `bootstrap/README.en.md`
- `bootstrap/references/provider-postflight.md`
- `bootstrap/references/provider-postflight.en.md`
- `bootstrap/references/framework-upgrade.md`
- `bootstrap/references/framework-upgrade.en.md`
- `bootstrap/references/optional-components.md`
- `bootstrap/references/optional-components.en.md`
- `HANDBUCH.md`

## Offene Folgearbeit

- Optional: Provider-Postflight spaeter als maschinenlesbares Template oder Script auskoppeln.
- Optional: Upgrade-Modus spaeter als dediziertes Script statt rein operativer Skill-Anweisung implementieren.
