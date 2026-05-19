# Release Notes — Wave B

Stand: 2026-05-19

## Zweck

Wave B haertet Tooling, Architektur und Security-by-Design. Die Aenderungen machen aus den bisherigen Hinweisen verbindliche Story- und Implementierungsregeln: Security Impact muss in Stories sichtbar sein, Security Validation muss vor `Done` belegt werden, und Post-Implement-Validation wird als Validate-Fix-Learn-Schleife beschrieben.

## Betroffene Stories

- BOO-55
- BOO-56
- BOO-57

## Umgesetzte Schwerpunkte

### Hook-Layer statt Git-Hook-Verkuerzung

`bootstrap/references/hooks-setup.md` und die englische Variante erklaeren jetzt drei Layer:

- KI-Runtime-Hook,
- lokaler Git-Hook,
- CI-Gate.

Damit ist klar: Governance-Hooks sind Coding-/Runtime-Hooks des jeweiligen Werkzeugs. Git-Hooks und CI koennen dieselbe Regel spiegeln, ersetzen aber nicht den Projektvertrag in `CONVENTIONS.md`.

### Architektur-Kontextvalidierung

`ARCHITECTURE_DESIGN.md` bekommt im Template eine Kontextvalidierung. Blueprint-Regeln sind damit nicht mehr nur generisch, sondern muessen zur konkreten Projektlage passen: kritische Dimensionen, leichtgewichtige Dimensionen, externe Provider, Security-/Privacy-Grenzen und Annahmen fuer den ersten echten Implementierungsdurchlauf.

### Security-by-Design in Stories

Feature- und Fix-Templates enthalten jetzt:

- `Security Impact`,
- `Security Validation`.

Jede Story muss ihren Change-Type deklarieren. Bei Code-, Security-, Tooling-, Dependency-, CI- oder Governance-Aenderungen muss vor `Done` konkrete Validation-Evidenz dokumentiert werden.

### Implement als Validate-Fix-Learn

`implement/SKILL.md` und `implement/SKILL.en.md` beschreiben Post-Implement-Validation jetzt explizit als Schleife:

```text
Validate -> Interpret -> Decide -> Fix -> Re-Validate -> PASS/FAIL -> Learn
```

Wichtig: Ein fehlgeschlagenes Gate wird erst interpretiert, dann gezielt gefixt, dann erneut validiert. Wiederholbare Muster werden in den aktiven Learning-Loop geschrieben.

## Referenz-Matrix

| Referenz | Wave-B-Bezug |
|---|---|
| F007 | Architektur-Template um Kontextvalidierung ergaenzt |
| F008 | Hook-Begriff als Runtime-/Coding-Hook geklaert |
| F012 | Architektur-Template bleibt Ort fuer KI-Architektur-Prinzipien und Anti-Patterns |
| F014 | Tooling-/Gate-Schichten klarer getrennt |
| F015 | Standard-Dimensionen bleiben Vertrag, Kontextvalidierung macht sie projektspezifisch |
| F016 | Drei-Layer-Gate Logik geschärft |
| F023 | `implement` liest/prueft `SECURITY.md` und Security-Referenzstack verbindlicher |
| F024 | Security Impact / Security Validation in Story-Templates verankert |
| F025 | Architektur-/Security-Blueprints muessen gegen Projektkontext validiert werden |

## Geaenderte Artefakte

- `bootstrap/references/architecture-design-template.md`
- `bootstrap/references/architecture-design-template.en.md`
- `bootstrap/references/hooks-setup.md`
- `bootstrap/references/hooks-setup.en.md`
- `bootstrap/references/security-template.md`
- `bootstrap/references/security-template.en.md`
- `ideation/references/story-template-feature.md`
- `ideation/references/story-template-feature.en.md`
- `ideation/references/story-template-fix.md`
- `ideation/references/story-template-fix.en.md`
- `implement/SKILL.md`
- `implement/SKILL.en.md`

## Migrationshinweis

Bestehende Projekte muessen nicht blind ueberschrieben werden. Beim naechsten Upgrade sollten sie ihre Story-Templates um `Security Impact` und `Security Validation` ergaenzen und pruefen, ob `SECURITY.md` sowie sensitive-paths-Dateien vorhanden sind.
