# Release Notes — Wave F Security-Dokumentationsmodell

Stand: 2026-05-19

## Zweck

Wave F schliesst BOO-62. Das Framework erklaert Security jetzt nicht nur ueber einzelne Gates, sondern als zusammenhaengendes Dokumentationsmodell: `ARCHITECTURE_DESIGN.md` fuehrt, `SECURITY.md` operationalisiert, Unterartefakte liefern Evidenz und technische Durchsetzung.

## Betroffene Story

- BOO-62

## Umgesetzte Schwerpunkte

### Architecture verweist auf Security

`bootstrap/references/architecture-design-template.md` und `.en.md` enthalten nun:

- `SECURITY.md` in der Referenzen-Tabelle,
- ein Security-Referenzmodell,
- die Erklaerung, dass `ARCHITECTURE_DESIGN.md` Security als Qualitaetsdimension und Grenze fuehrt, waehrend `SECURITY.md` der operative Security-Vertrag ist.

### Security verweist auf Unterartefakte

`bootstrap/references/security-template.md` und `.en.md` enthalten nun:

- Security-Unterartefakte mit Zweck und Update-Anlass,
- `API_INVENTORY.md`,
- `.semgrep.yml`,
- `.codex/hooks.json` / `.claude/settings.json`,
- `.claude/sensitive-paths.json` / `.codex/sensitive-paths.json`,
- Threat Models,
- Privacy-/Compliance-Dokumente,
- Security-by-Design-Ablauf.

### Handbuch-Lesefuehrung

`HANDBUCH.md` enthaelt jetzt ein zusammenhaengendes Kapitel zum Security-Dokumentationsmodell in DE und EN:

`ARCHITECTURE_DESIGN.md -> SECURITY.md -> Security-Unterartefakte`

Die Rollen von `/ideation`, `/implement`, `/security-architect`, `/architecture-review` und `/sprint-review` sind darin erklaert.

## Geaenderte Artefakte

- `HANDBUCH.md`
- `bootstrap/references/architecture-design-template.md`
- `bootstrap/references/architecture-design-template.en.md`
- `bootstrap/references/security-template.md`
- `bootstrap/references/security-template.en.md`

## Offene Folgearbeit

- Optional: spaeter einen eigenen Security-Flow-Sketch im Olli Corporate Design ergaenzen, wenn das Handbuch-Kapitel visuell noch staerker gefuehrt werden soll.
