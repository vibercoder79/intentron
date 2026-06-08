# Release Notes - Wave X Deterministischer dpo-Kontrollkatalog

> 🌐 **Sprache:** Deutsch (diese Datei) · [🇬🇧 English](wave-x-dpo-control-catalog.en.md)

Stand: 2026-05-31

## Zweck

Wave X (BOO-87) gibt dem dpo-Skill einen **deterministischen Kontrollkatalog** plus einen **Runner**, der ein Projekt gegen kuratierte Datenschutz-Kontrollen prueft und einen **auditor-ready Report** erzeugt — pro Kontrolle ein Status: **PASS / GAP / REVIEW-NEEDED**. Zwei Kataloge decken EU (`gdpr.yml`) und die Schweiz (`ndsg.yml`) ab. Damit liefert das Framework reproduzierbare Compliance-Evidenz, die ein Pruefer (FINMA/BaFin, externer Auditor) direkt nachvollziehen kann — ohne Datenbank, ohne SaaS, lokal und deterministisch.

## Warum

Datenschutz-Compliance scheitert in der Praxis selten an fehlendem Wissen, sondern an **fehlender, nachvollziehbarer Evidenz** zum Pruefzeitpunkt. "Wir machen das schon richtig" ist kein Audit-Nachweis. Regulatoren wie FINMA (CH) und BaFin (DE) erwarten belegbare, wiederholbare Kontrollen statt Momentaufnahmen. Ein deterministischer Runner — identischer Input ergibt identischen Report — schliesst diese Luecke: Jede Kontrolle ist eine pruefbare Aussage (Datei existiert / enthaelt Muster / Muster ist abwesend / manuelle Pruefung noetig), jede Aussage traegt ihren regulatorischen Bezug (`mapsTo`) und ihre Quelle (`quelle`). Der Report wird Teil des Repos und damit versioniert nachvollziehbar.

nDSG (revidiertes CH-Datenschutzgesetz) ist das **Alleinstellungsmerkmal**: Die meisten Compliance-Tools decken nur GDPR/EU ab. Ein eigener `ndsg.yml`-Katalog adressiert gezielt Schweizer Projekte und ist im DACH-Beratungskontext ein Differenzierer.

## Designentscheid

- **Deterministisch statt heuristisch.** Gleiche Eingabe → gleicher Report. Vier Check-Typen: `file-exists`, `file-contains`, `grep-absent`, `review`. Kein LLM im Pruefpfad, keine Nicht-Reproduzierbarkeit.
- **Status-Modell PASS / GAP / REVIEW-NEEDED.** `review`-Kontrollen sind bewusst nicht automatisierbar (z.B. "Loeschkonzept fachlich freigegeben") und werden als REVIEW-NEEDED ausgewiesen — ehrlicher als ein erzwungenes PASS/FAIL.
- **Katalog + Projekt-Overlay.** Framework-Basis-Kataloge (`dpo/controls/gdpr.yml` + `ndsg.yml`) kommen mit dem Skill und werden bei Updates ersetzt. Das **Projekt-Overlay** `.claude/dpo/controls/` (Bring-Your-Own-Controls) gehoert dem Kunden und **ueberlebt Framework-Updates** — wird nie ueberschrieben.
- **Kataloge + Runner reisen mit dem Skill, nicht pro Projekt.** Die Projekt-Migration ist daher leichtgewichtig: nur Overlay-Verzeichnis + Reports-Dir. Kein dupliziertes Scaffolding, ein zentraler Wartungspunkt.
- **Keine Datenbank.** Report ist eine Datei in `dpo/reports/`, versioniert im Repo. Kein State-Server, kein SaaS, keine Datenabwanderung — passt zum Souveraenitaets-Anspruch des Frameworks.
- **OSCAL als spaetere Ausbaustufe.** Das flache Schema (`id`/`titel`/`evidenz`/`check_typ`/`check_arg`/`mapsTo`/`quelle`) ist bewusst einfach. Eine Abbildung auf OSCAL (NIST Open Security Controls Assessment Language) ist als spaeterer Ausbau vorgesehen, aber nicht Teil dieser Wave — erst Nutzen beweisen, dann Standard-Mapping.

## Bezug agentic-security (PolyForm)

Die Idee eines deterministischen Control-Runners ist am `agentic-security`-Pattern angelehnt. `agentic-security` steht unter PolyForm-Lizenz; uebernommen wurde ausschliesslich die **Idee** — **kein Code**. Kataloge, Schema, Runner und Doku sind eigenstaendig aus oeffentlichen regulatorischen Quellen (GDPR, nDSG, BDSG) erstellt. Hard-Constraint: kein PolyForm-Code im Repo.

## Was Nutzer bekommen

- **`dpo/controls/gdpr.yml`** — GDPR/EU-Kontrollkatalog (kommt mit dem dpo-Skill v1.2.0).
- **`dpo/controls/ndsg.yml`** — nDSG/CH-Kontrollkatalog (CH-Alleinstellung, kommt mit dem Skill).
- **`dpo/scripts/dpo-audit.py`** — deterministischer Runner: liest die Framework-Kataloge + das Projekt-Overlay, prueft jede Kontrolle, schreibt den Report (PASS/GAP/REVIEW-NEEDED) nach `dpo/reports/`. Steuerung u.a. via `DPO_PROJECT_ROOT`.
- **`.claude/dpo/controls/`** — Projekt-Overlay (Bring-Your-Own-Controls) mit erklaerender `README.md`; flaches Schema wie die Basis-Kataloge; ueberlebt Framework-Updates (Kunden-Eigentum).
- **`dpo/reports/`** — Ziel-Verzeichnis fuer die generierten Reports (mit `.gitkeep`, im Repo versioniert).
- **`migrate_boo_87`** — idempotente, additive Projekt-Migration (siehe unten).

## Migration

`bash bootstrap/scripts/migrate-to-v2.sh --issue BOO-87`

- Legt das Projekt-Overlay-Verzeichnis `.claude/dpo/controls/` an (nur falls nicht vorhanden) **mit** einer `README.md`, die das BYO-Overlay und das flache Schema erklaert.
- Legt das Reports-Verzeichnis `dpo/reports/` an (mit `.gitkeep`).
- **Kein Scaffolding** von Katalog/Runner/Skill — die kommen mit dem dpo-Skill (v1.2.0). Es werden nur `[MANUAL]`-Hinweise ausgegeben, dass der Audit via `DPO_PROJECT_ROOT=. python3 <dpo-skill>/scripts/dpo-audit.py` laeuft und die Framework-Kataloge `dpo/controls/*.yml` nutzt.
- **Idempotent + additiv:** zweiter Lauf erzeugt keine Diffs — vorhandene Verzeichnisse/Dateien werden erkannt (`[SKIP]`); vorhandenes Kunden-Overlay wird **nie** ueberschrieben; `--dry-run` loggt nur (`[DRY]`).

Verifikation: `test -d .claude/dpo/controls && test -d dpo/reports` (Exit 0); `DPO_PROJECT_ROOT=. python3 <dpo-skill>/scripts/dpo-audit.py` erzeugt einen Report in `dpo/reports/`. Rollback: Verzeichnisse `.claude/dpo/controls/` und `dpo/reports/` entfernen (eigene Overlays vorher sichern; Katalog/Runner liegen im Skill und sind nicht betroffen).

## Konkrete Aenderungen

| Bereich | Datei |
|---|---|
| GDPR + nDSG Kataloge | `dpo/controls/gdpr.yml` + `dpo/controls/ndsg.yml` (im dpo-Skill) |
| Deterministischer Runner | `dpo/scripts/dpo-audit.py` (im dpo-Skill) |
| Projekt-Migration | `migrate_boo_87` in `bootstrap/scripts/migrate-to-v2.sh` (+ `ALL_ISSUES`) |
| Migration-Checklist §BOO-87 (DE+EN) | `bootstrap/references/migration-checklist-v1-to-v2.md` + `.en.md` |
| Release Notes | `docs/releases/wave-x-dpo-control-catalog.md` |
| Spec | `specs/BOO-87.md` |

## Skill-Versions-Bumps

- **dpo: 1.1.0 → 1.2.0** (Kataloge `gdpr.yml` + `ndsg.yml`, Runner `dpo-audit.py`, Projekt-Overlay-Support)

## Verweise

- Spec: `specs/BOO-87.md`
- Kataloge + Runner: dpo-Skill `dpo/controls/*.yml` + `dpo/scripts/dpo-audit.py`
- Migration: `migrate_boo_87` in `bootstrap/scripts/migrate-to-v2.sh`
- ADR: `02 Projekte/Code-Crash Framework/Decisions/2026-05-31 agentic-security-Adoption Bodyguard + dpo-Katalog.md`
- Bezug: `agentic-security` (deterministischer Control-Runner) — Idee uebernommen, kein Code (PolyForm-Lizenz)
- Spaetere Ausbaustufe: OSCAL-Mapping (NIST) — nicht Teil dieser Wave
- Linear: BOO-87
