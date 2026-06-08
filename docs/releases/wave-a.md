# Release Notes — Wave A

> 🌐 **Sprache:** Deutsch (diese Datei) · [🇬🇧 English](wave-a.en.md)

Stand: 2026-05-19

## Zweck

Wave A haertet die Codex- und Dry-Run-Lesbarkeit von INTENTRON. Der Schwerpunkt
liegt auf dem Bootstrap- und Vertragsfundament: Runtime-Auswahl, Artefakt-Baseline,
Backlog-Adapter, Postflight, Handbuch-Klarstellung und Upgrade-Pfad.

## Betroffene Stories

- BOO-52
- BOO-53
- BOO-54
- BOO-60
- BOO-61

## Wichtige Klarstellungen

### Codex-ready Framework-Erklaerung

Das Framework wird als sequenzielle Engineering-Pipeline mit Quality-Gates beschrieben, nicht als
vollautonomer Developer-Agent. Codex, Claude, Cursor oder lokale LLMs sind Adapter auf denselben
Story-Vertrag. Subagents sind spezialisierte Ausfuehrungshelfer innerhalb einer kontrollierten
Story und bleiben an Rolle, Kontext, Write-Scope, Rueckgabeformat und Gates gebunden.

### Bootstrap Skill vs. INTENTRON

Der Bootstrap Skill installiert und initialisiert ein Projekt: Governance-Dateien, lokale
Skill-Kopien, Hooks, optionale Adapter und Basis-Artefakte. INTENTRON ist die
Methodik und der Vergleichsgegenstand: Konventionen, Gates, Artefakte, Rollen und Review-Punkte.
Bootstrap bringt das Framework ins Projekt; Bootstrap ist nicht das Framework selbst.

### Lite / Standard / Heavy

Die Governance-Modi sind keine Reifegrad-Abzeichen, sondern Friktionsbudgets:

- `lite` laesst teure Teile wie schwere CI, SonarQube, Branch Protection, Performance-Baselines,
  Audit-Trails und verpflichtende Deep Reviews weg.
- `lite` laesst nicht weg: Projektvertrag, Backlog-Record, Spec, Secrets-Hygiene, lokale
  Basis-Gates und Ergebnisnotiz.
- `standard` macht die Kern-Gates produktfaehig: Issue-/Spec-Gates, Security-Basis, Lint/Test,
  CI wo vorhanden und Sprint-Review.
- `heavy` fuegt Nachweislast hinzu: Review-, Audit-, Security-, Compliance- und
  Produktionsnachweise.

### Backlog-Tool-Abstraktion

Das Framework verwendet den neutralen Begriff Backlog-Record. Linear ist der empfohlene Adapter,
aber nicht die einzige gueltige Form. GitHub Issues, Microsoft Planner oder ein Markdown-Backlog
koennen denselben Record tragen, solange Pflichtfelder und Gates erhalten bleiben.

### Upgrade-Pfad fuer bestehende Projekte

Bestehende Projekte werden nicht blind ueberschrieben. Der dokumentierte Upgrade-Pfad hat drei
Stufen:

1. `inspect`: Projektzustand lesen und Abweichungen sichtbar machen.
2. `apply-safe`: nur additive, idempotente Aenderungen anwenden.
3. `apply-with-confirmation`: jede Aenderung an bestehenden Regeln, Hooks, CI, Templates,
   Branch-Protection, Governance-Modus, Adapter-Konfiguration oder Skill-Versionen bestaetigen
   lassen.

## Referenz-Matrix

| Referenz | Wave-A-Bezug |
|---|---|
| F001 | `intent` als Core-Set/Pipeline-Einstieg bestaetigen |
| F002 | Backlog-Record neutralisieren; Linear nur als Adapter behandeln |
| F004 | Claude-first Sollstruktur um Codex-/Cross-Tool-Mapping ergaenzen |
| F005 | Governance-Modi duerfen keine Skill-/Artefakt-Baseline zerbrechen |
| F006 | `AGENTS.md`, `CLAUDE.md` und `CONVENTIONS.md` rollenrein erklaeren |
| F009 | Runtime-Abfrage und Transformationslogik fuer Claude Code/Codex/Cross-Tool verankern |
| F010 | Learning-Loop-Level als projektweiter Vertrag im Postflight sichtbar machen |
| F013 | Projekt-Personalausweis je Runtime klaeren |
| F017 | Repository-Publish-Entscheidung in den Bootstrap-Abschluss ziehen |
| F018 | Artefakte nach Bootstrap aktuell halten und in Release Notes spiegeln |
| F019 | Externe Services und Provider getrennt vom lokalen Setup verifizieren |
| Upgrade-Pfad | Bestehende Projekte mit `inspect`, `apply-safe`, `apply-with-confirmation` schuetzen |

## Geaenderte Artefakte

- `HANDBUCH.md`
- `CONVENTIONS.md`
- `bootstrap/SKILL.md`
- `bootstrap/SKILL.en.md`
- `bootstrap/README.md`
- `bootstrap/README.en.md`
- `docs/releases/wave-a.md`

## Nicht geaendert

- Keine Excalidraw- oder PNG-Dateien.
- Keine Runtime-Scripts, Hook-Scripts oder CI-Workflows.
