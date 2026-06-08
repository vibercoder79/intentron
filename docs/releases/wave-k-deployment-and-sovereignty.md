# Release Notes - Wave K Deployment-Szenarien + Souveraenitaets-Stack

> 🌐 **Sprache:** Deutsch (diese Datei) · [🇬🇧 English](wave-k-deployment-and-sovereignty.en.md)

Stand: 2026-05-27

## Zweck

Wave K schliesst BOO-70 und BOO-71. Das Framework gibt Operatoren erstmals strukturierte Orientierung zu zwei Setup-Fragen, die bisher Beratungsthemen waren:

1. **BOO-70 — Deployment-Szenarien:** Auf welcher Geraete-Topologie laeuft INTENTRON? Anhang P beschreibt vier gelebte Patterns (Solo-Mac, Solo-VPS, Multi-User-VPS-Coding-Factory, Team-mit-Coding-Server) mit Decision-Matrix, Setup-Schritten, Skill-Installation, Secrets-Trennung, Backup-Strategie und Tradeoffs.
2. **BOO-71 — Souveraenitaets-Stack-Guide + LLM-Proxy-Hook:** Welche EU-konformen Alternativen gibt es zur Default-Stack-Zusammensetzung (GitHub, Anthropic USA, iCloud)? Anhang Q liefert die Inspirations-Schicht — fuenf Stack-Komponenten mit Tabellen-Mapping und kurzer Migrations-Anleitung — und ergaenzt das optionale Config-Feld `llm_proxy_url` als Hook-Punkt fuer Operator-betriebene Anonymisierungs-/Souveraenitaets-Proxys.

**Erwarteter Effekt:** Beide Themen werden vom "fragen-wir-die-Beratung"-Modus in den "lies-den-Anhang"-Modus ueberfuehrt. Bootstrap bleibt frictionless (Default Solo-Mac, kein neuer Interview-Schritt fuer Souveraenitaet) — aber Operatoren mit regulierten Anforderungen finden im HANDBUCH eine erste Orientierung.

## Betroffene Stories

- BOO-70 — HANDBUCH Anhang P Deployment-Szenarien + Bootstrap-Frage A.7
- BOO-71 — HANDBUCH Anhang Q Souveraenitaets-Stack-Guide + `llm_proxy_url`-Hook in `environment.json`

## Wichtige Klarstellungen

### BOO-70: Bootstrap stellt **eine** Frage, nicht vier Szenarien

Pragmatische Trennung: Operator-Entscheidung kommt aus dem HANDBUCH-Anhang, Bootstrap macht weiterhin den Default-Setup (Solo-Mac). Bei Wahl `b) anders` gibt der Bootstrap nur einen Hinweis-Block aus, kein Interview-Fork, kein szenarienspezifischer Setup-Code. So bleibt der Bootstrap-Skill schlank und der Trampelpfad fuer ~80% der Operatoren unveraendert.

### BOO-71: KEINE Anonymisierungs-Engine im Framework

Anhang Q dokumentiert EU-Alternativen pro Stack-Komponente und beschreibt den `llm_proxy_url`-Hook konzeptionell. Das Framework setzt **keinerlei** Proxy-Routing um — der Wert wird gelesen, in `meta.json.llm_routing` protokolliert und damit ist die Framework-Aufgabe erfuellt. Anonymisierung (z.B. Microsoft Presidio) ist Operator-Aufgabe und Runtime-Infrastruktur, nicht Governance. Der Hook-Punkt ist der minimale Vertrag, der Audit-Trails ermoeglicht, ohne dem Operator eine Proxy-Implementierung aufzudraengen.

### Privacy ≠ Souveraenitaet

Datensouveraenitaet (Anhang Q) und Privacy-by-Design (Anhang O, BOO-69, Wave J) sind orthogonal. Ein EU-Stack ersetzt keine DSGVO-Pflicht, und eine DSGVO-konforme Verarbeitung auf US-Cloud befreit nicht vom CLOUD-Act-Risiko. Operatoren mit beiden Anforderungen aktivieren Privacy-Add-on **und** waehlen ihre Stack-Komponenten gemaess Anhang Q.

## Was Nutzer mit dem neuen Setup bekommen

- **HANDBUCH Anhang P "Deployment-Szenarien" (DE+EN)** mit Decision-Matrix (6 Operator-Profile) und vier vollstaendigen Szenario-Sektionen — Operator-Profil, Setup-Schritte, Skill-Installation, Secrets-Trennung, User-Isolation (wo relevant), Backup-Strategie, Tradeoffs. Backup-Empfehlungen pro Szenario explizit (Time Machine / Hetzner Storage Box / Backblaze B2 / VPS-Snapshot), nicht vage.
- **Bootstrap-Frage A.7 (`DEPLOYMENT_SCENARIO`)** mit Default Solo-Mac und Verweis-Block fuer "anders". Bootstrap-Briefing-Box zeigt jetzt "Block A — Projekt-Kern (10 Fragen)" statt 9. Bestehende Solo-Mac-Operatoren erleben Null Aenderung.
- **HANDBUCH Anhang Q "Souveraenitaets-Stack-Guide + LLM-Proxy-Hook" (DE+EN)** mit:
  - Decision-Matrix "Wann lohnt der Souveraenitaets-Switch?" (7 Trigger).
  - Tabelle EU-konformer Alternativen fuer 5 Stack-Komponenten (Code-Hosting, Vault-Sync, LLM, Issue-Tracker, CI) mit Tradeoff-Hinweisen.
  - Pro Komponente kurze Migrations-Anleitung (3-5 Schritte) plus Hinweis auf externe Doku des jeweiligen Tools.
  - LLM-Proxy-Hook-Sektion mit JSON-Schema-Snippet, Microsoft-Presidio-Konzept-Beispiel und harter Designentscheid-Klarstellung.
- **`.claude/environment.json` Schema-Erweiterung:** optionales Feld `llm_proxy_url: <url|null>` mit Default `null`. Doku im `file-templates.md` aktualisiert (DE+EN).
- **`/implement` Schritt 0 erweitert (Punkt 7):** read-only-Erklaerung des `llm_proxy_url`-Felds, Protokollierung als Audit-Spur in `meta.json.llm_routing`. Kein Routing-Code im Framework.

## Konkrete Aenderungen

| Bereich | Aenderung | Datei |
|---|---|---|
| HANDBUCH Anhang P NEU | Deployment-Szenarien Lese-Einstieg (DE+EN) | `HANDBUCH.md` + `HANDBUCH.en.md` |
| HANDBUCH Anhang Q NEU | Souveraenitaets-Stack-Guide + LLM-Proxy-Hook (DE+EN) | `HANDBUCH.md` + `HANDBUCH.en.md` |
| Bootstrap-Frage A.7 NEU | Deployment-Szenario, Default Solo-Mac, Verweis auf Anhang P | `bootstrap/SKILL.md` v3.28.0 + `.en.md` |
| Bootstrap Phase-0-Briefing | "Block A — Projekt-Kern (10 Fragen)" (war 9) | `bootstrap/SKILL.md` + `.en.md` |
| environment.json-Schema | optionales Feld `llm_proxy_url` (Default `null`) + Feld-Tabelle ergaenzt | `bootstrap/references/file-templates.md` + `.en.md` |
| `/implement` Schritt 0 Punkt 7 | Doku-Block fuer `llm_proxy_url`-Lesen + `meta.json.llm_routing`-Audit-Spur | `implement/SKILL.md` v2.11.1 + `.en.md` |
| Migration | `migrate_boo_70()` (Doku-only) + `migrate_boo_71()` (fuegt `llm_proxy_url: null` in env.json ein) | `bootstrap/scripts/migrate-to-v2.sh` |
| Migration-Checklist | §BOO-70 + §BOO-71 Bloecke (DE+EN) | `bootstrap/references/migration-checklist-v1-to-v2.md` + `.en.md` |
| ALL_ISSUES-Array | `BOO-70 BOO-71` ergaenzt | `bootstrap/scripts/migrate-to-v2.sh` |

## Skill-Versions-Bumps

- `bootstrap` 3.27.0 → 3.28.0 (minor: neue Frage A.7, neues optionales env.json-Feld)
- `implement` 2.11.0 → 2.11.1 (patch: Schritt 0 Doku-Block, kein Verhaltens-Lock)

## Migration fuer Bestands-Projekte

`migrate_boo_70()` und `migrate_boo_71()` in `bootstrap/scripts/migrate-to-v2.sh`:

```bash
bash bootstrap/scripts/migrate-to-v2.sh --issue BOO-70
bash bootstrap/scripts/migrate-to-v2.sh --issue BOO-71
```

Beide Auto-Schritte idempotent und additiv. Ergebnis:

- **BOO-70:** nur Hinweis-Block (Doku-only). Operator vermerkt sein Deployment-Szenario in `migration-status.md`.
- **BOO-71:** `llm_proxy_url: null` in `.claude/environment.json` einfuegen (falls Feld noch fehlt). Fehlt die Datei: Hinweis auf `bash .claude/generate-environment-json.sh`.

Operator-Schritte: HANDBUCH Anhang P + Q einmal lesen, Status in `migration-status.md` setzen, ggf. Souveraenitaets-Switch planen. Default Solo-Mac + Default-Stack bleiben unveraendert.

## Designentscheid: Inspirations-Schicht, kein Setup-Generator

INTENTRON bleibt fuer ~80% der Operatoren (Solo-Mac, Default-Stack) frictionless. Wave K fuegt **keinen** Pflicht-Schritt hinzu — beide Anhaenge sind Lese-Material plus 1 Bootstrap-Frage (mit Default-Pfad) plus 1 optionales Config-Feld. Operatoren mit regulierten Anforderungen haben jetzt eine Anlaufstelle im HANDBUCH, statt Beratungsgespraeche zu brauchen. Wer den Souveraenitaets-Switch tatsaechlich vollzieht, folgt externer Tool-Doku (Codeberg, Mistral, etc.) — das Framework macht dort keine eigenen Setup-Vorgaben.

## Noch offen / Folgepunkte

- **DPO-Skill SecondBrain-Doku** (Folge-Aufgabe aus Wave J): `03 Bereiche/Skills/dpo.md` + `dpo.en.md` befuellen analog `security-architect.md`-Doku. In dieser Welle nachgezogen.
- **Souveraenitaets-Stack-Praxis-Beispiel:** ein konkretes Owlist-Projekt vollstaendig auf EU-Stack umstellen (z.B. INTENTRON selbst nach Codeberg spiegeln) waere ein guter "show, don't tell"-Folgeschritt. Eigene Spec faellig.
- **`meta.json.llm_routing`-Aggregation im `/sprint-review`:** wenn Operatoren `llm_proxy_url` aktiv nutzen, koennte das Sprint-Review eine `proxy_active`-Quote ausweisen. Eigene Spec faellig.
- **Anhang R (INTENTRON Multi-Tool-Adoption):** parallel laufende Beratungsidee — wie kombinieren Operator-Teams INTENTRON mit Spec Kit, Cursor und anderen Tools? Eigene Welle.

## Verweise

- Specs: `specs/BOO-70.md`, `specs/BOO-71.md`
- HANDBUCH: Anhang P Deployment-Szenarien, Anhang Q Souveraenitaets-Stack-Guide
- Bootstrap-Frage: `bootstrap/SKILL.md` §A.7
- environment.json-Schema: `bootstrap/references/file-templates.md` §`.claude/environment.json`
- implement-Skill: `implement/SKILL.md` Schritt 0 Punkt 7
- Migration: `bootstrap/scripts/migrate-to-v2.sh` (`migrate_boo_70`, `migrate_boo_71`)
- Migration-Checklist: §BOO-70, §BOO-71
- Feedback-Quelle: Operator Martin, 2026-05-27
- Linear: <https://linear.app/owlist/issue/BOO-70/> + <https://linear.app/owlist/issue/BOO-71/>
- Vorherige Welle: `docs/releases/wave-j-privacy-by-design.md`
