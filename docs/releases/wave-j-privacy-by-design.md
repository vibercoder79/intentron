# Release Notes - Wave J Privacy-by-Design

> 🌐 **Sprache:** Deutsch (diese Datei) · [🇬🇧 English](wave-j-privacy-by-design.en.md)

Stand: 2026-05-27

## Zweck

Wave J schliesst BOO-69. Das Framework verankert Privacy by Design als optionales Add-on mit voller Operationalisierung — 1:1 das Pattern von Security by Design, aber fuer Datenschutz. Wer das Privacy-Add-on aktiviert, bekommt: einen vollwertigen DPO-Skill (Standalone, analog `security-architect`), eine `PRIVACY.md` mit 8 Pflicht-Sektionen, ein `personal-data-paths.json` als HARD-GATE-Pattern, drei Pipeline-Hooks (ideation Schritt 0e, implement Schritt 5.5b, sprint-review Schritt 7c) und einen HANDBUCH-Anhang O als Lese-Einstieg.

**Erwarteter Effekt:** Privacy-by-Design wird **Framework-Garantie** statt Best-Effort. Asymmetrie zu Security-by-Design ist behoben. Operator muss kein DSGVO-Expertenwissen mitbringen — der DPO-Skill stellt die richtigen Pruef-Fragen.

## Betroffene Stories

- BOO-69

## Wichtige Klarstellung: DPO bleibt Standalone

In der Spec war ursprünglich "DPO ins Bundle" geplant. Recherche während der Umsetzung zeigte: `security-architect` ist KEIN Bundle-Skill, sondern Standalone unter `~/.claude/skills/security-architect/`. Bootstrap installiert ihn ueber das Standalone-Skill-Set, wenn Security gebraucht wird. **Operator-Entscheidung: DPO folgt diesem Pattern.** Vorteile: nicht-destruktiv (DPO bleibt parallel global verfuegbar), konsistent mit existierender Bundle-Philosophie (Workflow-Skills im Bundle, Spezialisten Standalone), Updates via `publish_skill.py` ohne Bundle-Eingriff.

Die Spec `specs/BOO-69.md` enthaelt einen Naming-Hinweis-Block oben, der die Entscheidung dokumentiert.

## Was Nutzer mit dem neuen Setup bekommen

- **DPO-Skill** mit drei Modi: ASSESS (Story-Planung, schreibt DPIA), REVIEW (Code-Aenderung, prueft Datenminimierung/Consent/Loeschmechanik), AUDIT (alle N Sprints, pflegt Verarbeitungsverzeichnis). Deckt DSGVO/GDPR (EU), BDSG (DE) und nDSG (CH) ab. Recommended Model: opus (Compliance-kritisch).
- **PRIVACY.md** im Projekt-Root mit 8 Pflicht-Sektionen: Privacy-Grundsatz, Rechtsgrundlagen Art. 6 DSGVO, Verarbeitungsverzeichnis Art. 30, Loeschkonzept, Betroffenenrechte Art. 15-22, Personal-Data-Paths, Privacy-by-Design-Ablauf, Incident-Notiz Art. 33/34.
- **`personal-data-paths.json`** mit Default-Patterns (`**/user*`, `**/profile*`, `**/billing/**`, etc.). HARD GATE im `/implement` Schritt 5.5b — kein Commit ohne `privacy-ok`-Bestaetigung oder DPO-REVIEW-Report.
- **`/ideation` Schritt 0e** Pre-Flight: Story-Frontmatter `personal_data: true|false`. Bei `true`: DPO ASSESS empfohlen, Backlog-Label `privacy`, DPIA-Verweis.
- **`/implement` Schritt 5.5b** Personal-Data-Paths-Gate (analog 5.5 Sensitive-Paths-Gate). Plus Schritt 6e erweitert von "Security-Findings" auf "Security + Privacy-Findings" mit Pflicht-Privacy-Block bei `personal_data: true`.
- **`/sprint-review` Schritt 7c** DPO-Audit-Trigger alle N Sprints (Default 4, konfigurierbar via `environment.json.privacy_audit_cadence`).
- **HANDBUCH Anhang O** Privacy by Design als Lese-Einstieg: Trigger-Liste, 3-Modi-Mapping, DPO ↔ security-architect-Trennung, Migrations-Hinweise, Cross-Reference auf BOO-71 Souveraenitaets-Stack.
- **Audit-Argument** fuer regulierte Branchen: DPO bleibt nachweisbar auf Opus-Tier (Compliance-kritisch, kein Auto-Downgrade), kombinierbar mit Token-Effizienz-Policy (BOO-84) ohne Konflikt.

## Konkrete Aenderungen

| Bereich | Aenderung | Datei |
|---|---|---|
| DPO-Skill global normalisiert | Frontmatter um `recommended_model: opus` + `metadata.hermes` erweitert, EN-Variante neu | `~/.claude/skills/dpo/SKILL.md` + `SKILL.en.md` (NEU) |
| DPO-References EN-Spiegel | 5 References-Files in EN gespiegelt | `~/.claude/skills/dpo/references/*.en.md` (5 NEU) |
| PRIVACY.md-Template NEU | 8 Sektionen, strukturparallel zu security-template.md | `bootstrap/references/privacy-template.md` + `.en.md` (NEU) |
| Bootstrap Privacy-Add-on aufgewertet | Phase A.4 mit konkretem Setup-Block, neue Phase 4.4n Privacy-Setup | `bootstrap/SKILL.md` v3.27.0 + `.en.md` |
| Personal-Data-Paths-Template NEU | JSON-Template analog sensitive-paths.json | `bootstrap/references/file-templates.md` + `.en.md` |
| Ideation Schritt 0e NEU | Privacy-Pre-Flight mit Heuristik-Tabelle | `ideation/SKILL.md` v2.7.0 + `.en.md` |
| Implement Schritt 5.5b NEU + 6e erweitert | Personal-Data-Paths-Gate als HARD GATE, Privacy-Findings-Block | `implement/SKILL.md` v2.11.0 + `.en.md` |
| Sprint-Review Schritt 7c NEU | DPO-Audit-Trigger mit Cadence-Konfig | `sprint-review/SKILL.md` v2.6.0 + `.en.md` |
| HANDBUCH Anhang O NEU | Privacy-by-Design Lese-Einstieg (DE+EN) | `HANDBUCH.md` + `HANDBUCH.en.md` |
| Migration | `migrate_boo_69()` + migration-checklist §BOO-69 | `bootstrap/scripts/migrate-to-v2.sh`, `bootstrap/references/migration-checklist-v1-to-v2.md` + `.en.md` |

## Skill-Versions-Bumps

- `bootstrap` 3.26.0 -> 3.27.0
- `ideation` 2.6.0 -> 2.7.0
- `implement` 2.10.0 -> 2.11.0
- `sprint-review` 2.5.0 -> 2.6.0
- `dpo` (Standalone, global) 1.0.0 -> 1.1.0

## Migration fuer Bestands-Projekte

`migrate_boo_69()` in `bootstrap/scripts/migrate-to-v2.sh`:

```bash
bash bootstrap/scripts/migrate-to-v2.sh --issue BOO-69
```

Idempotent und additiv. Ergebnis:
- `PRIVACY.md` aus Template erzeugt (Skip falls vorhanden)
- `.claude/personal-data-paths.json` und/oder `.codex/personal-data-paths.json` angelegt
- `environment.json` um `privacy_audit_cadence: 4` erweitert
- Verfuegbarkeits-Check DPO + security-architect (rein informativ)

Operator-Schritte: DPO + security-architect global installieren (falls noch nicht), PRIVACY.md inhaltlich fuellen, Backlog-Label `privacy` anlegen.

## Designentscheid: Empfehlung statt Hard-Lock

Privacy ist **optional**. Wer keine personenbezogenen Daten verarbeitet (Solo-Tool, anonyme Daten), bekommt durch das Framework keinen zusaetzlichen Reibungspunkt. Wer das Add-on aktiviert: voll operationalisiert, kein halbgar.

Privacy-Findings im REVIEW-Modus sind dokumentations-pflichtig (Pflicht-Block in Schritt 6e), aber nicht Hard-Block auf Code-Aenderung — Operator kann mit `privacy-ok` explizit bestaetigen, dass die Aenderung trotz Finding gerechtfertigt ist. Audit-Trail dokumentiert die Entscheidung.

## Noch offen / Folgepunkte

- **HANDBUCH Anhang Q (BOO-71):** Souveraenitaets-Stack-Guide, ergaenzt diese Welle inhaltlich (Datensouveraenitaet, EU-Alternativen, LLM-Proxy-Hook).
- **HANDBUCH Anhang P (BOO-70):** Deployment-Szenarien — Operator-Entscheidung, ob das Projekt auf Solo-Mac/Solo-VPS/Multi-User-VPS/Team-Server laeuft. Beeinflusst u.a. wo `dpia/`-Dateien gehalten werden (privat vs. committed).
- **Verarbeitungsverzeichnis-Skelett:** Operator-Aktion nach Bootstrap erforderlich. DPO ASSESS-Modus unterstuetzt beim Erstausfuellen.
- **DPIA-Praxis-Beispiele:** koennten als zusaetzliche References-Files unter `dpo/references/examples/` ergaenzt werden (eigene Folge-Story falls Bedarf).

## Verweise

- Spec: `specs/BOO-69.md`
- HANDBUCH: Anhang O Privacy by Design
- DPO-Skill: `~/.claude/skills/dpo/SKILL.md` + `.en.md`
- Feedback-Quelle: Operator Martin, 2026-05-27 (`02 Projekte/Code-Crash Framework/assets/fact-sheet-privacy-by-design_1.docx`)
- Linear: <https://linear.app/owlist/issue/BOO-69/>
