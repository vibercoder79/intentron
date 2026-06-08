# Release Notes - Wave M Bundle-Adoption DPO + security-architect

> 🌐 **Sprache:** Deutsch (diese Datei) · [🇬🇧 English](wave-m-bundle-adoption-dpo-security.en.md)

Stand: 2026-05-27

## Zweck

Wave M schliesst BOO-74 und **korrigiert eine Wave-J-Decision**. In Wave J (BOO-69) wurde der DPO-Skill bewusst als Standalone-Skill adoptiert — analog `security-architect`, das auch ausserhalb des Framework-Repos lag. Operator-Feedback Tobias (2026-05-27 post-Wave-L) zeigte die Inkonsistenz: wenn das Framework Privacy-by-Design **garantieren** will (HANDBUCH Anhang O), muss der DPO-Skill aus dem Framework-Repo installierbar sein, nicht aus einem Nachbar-Repo. Gleiche Logik fuer `security-architect` (Security-Dimension in Bootstrap-Frage A.4).

**Loesung:** DPO und security-architect werden **vendored Bundle-Skills** im `intentron`-Repo. Bootstrap installiert sie aus demselben Repo wie alle anderen Bundle-Skills. Master bleibt `claudecodeskills`, Framework-Repo ist Mirror.

**Erwarteter Effekt:** Das Framework wird **self-contained**. Ein `git clone` des Framework-Repos enthaelt alles, was Bootstrap braucht — inklusive Privacy- und Security-Skills. Solo-Operatoren ohne Framework beziehen DPO/security-architect weiterhin aus `claudecodeskills`.

## Betroffene Stories

- BOO-74 — DPO + security-architect als vendored Bundle-Skills (korrigiert BOO-69 Wave-J-Decision)

## Wichtige Klarstellungen

### Master bleibt claudecodeskills

`publish_skill.py` aendert sich **nicht**. DPO und security-architect werden weiterhin im `claudecodeskills`-Repo gepflegt. Das Framework-Repo bekommt eine **gespiegelte Vendored-Kopie**. Bei jedem Skill-Update gilt die Sync-Konvention (siehe `bootstrap/references/skills-setup.md` §Sync-Konvention): erst Master aktualisieren, dann Mirror nachziehen.

### Bootstrap clont nur noch Framework-Repo

Vor BOO-74 clonte Bootstrap Phase 5 das `claudecodeskills`-Repo und unterschied zwischen `intentron/`-Sub-Folder-Skills und Top-Level-Standalone-Skills. Ab v3.29.0 clont Bootstrap **nur** das Framework-Repo — alle Bundle-Skills + dpo + security-architect liegen dort flach als Top-Level-Ordner. Optionale Allzweck-Skills (research, design-md-generator, setup-checklist, skill-creator) werden via Ja/Nein-Zusatzfrage aus claudecodeskills ergaenzt.

### Solo-Use bleibt erhalten

Wer DPO oder security-architect **ohne** INTENTRON nutzt (Solo-Tool, anderes Projekt), bezieht sie unveraendert aus `claudecodeskills`. Die Vendored-Kopie im Framework-Repo ist nur fuer den Bootstrap-Installations-Pfad relevant.

### Inhaltlich unveraendert

DPO und security-architect werden durch BOO-74 **nicht** inhaltlich geaendert — kein Versions-Bump dieser Skills. Es ist reines Vendoring (File-Copy). DPO bleibt v1.1.0, security-architect bleibt v1.1.0.

## Was Nutzer mit dem neuen Setup bekommen

- **`dpo/` und `security-architect/` als Top-Level-Ordner** im `intentron`-Repo (vendored 1:1 aus claudecodeskills, inkl. References DE+EN bei DPO).
- **Bootstrap v3.29.0** clont nur das Framework-Repo. Skill-Auswahl "Standard" enthaelt jetzt dpo + security-architect. Optionale Allzweck-Skills via Zusatzfrage.
- **Bootstrap Phase 4.4n** installiert DPO + security-architect aus dem Framework-Bundle (`$SKILL_SRC/dpo/`, `$SKILL_SRC/security-architect/`) statt aus einem externen Repo.
- **HANDBUCH Anhang O** umgestellt: "DPO als Framework-Bundle-Skill" statt "Standalone-Skill". Privacy-Mechanik (3-Modi, Trigger-Punkte) unveraendert.
- **`migrate_boo_74()`** fuer Bestands-Projekte: kopiert DPO + security-architect aus dem Framework-Repo nach `~/.claude/skills/`, idempotent und nicht-destruktiv.
- **Sync-Konvention** in `bootstrap/references/skills-setup.md` (DE+EN): Master vs. Mirror, Operator-Pflicht bei Updates.

## Konkrete Aenderungen

| Bereich | Aenderung | Datei |
|---|---|---|
| DPO vendored | 1:1-Kopie aus claudecodeskills (SKILL.md + SKILL.en.md + 5 References DE+EN) | `dpo/` (NEU im Framework-Repo) |
| security-architect vendored | 1:1-Kopie aus claudecodeskills (SKILL.md + 5 References + README + Excalidraw) | `security-architect/` (NEU im Framework-Repo) |
| Bootstrap Phase 5 | Skill-Quelle Framework-Repo statt claudecodeskills, Repo-Struktur-Doku, neue optionale Zusatzfrage, Kopier-Logik vereinfacht | `bootstrap/SKILL.md` v3.29.0 + `.en.md` |
| Bootstrap Phase 4.4n | "aus Framework-Bundle installieren" statt "Standalone" | `bootstrap/SKILL.md` + `.en.md` |
| Bootstrap A.4 Privacy-Hinweis | Wording "aus dem Framework-Bundle" | `bootstrap/SKILL.md` + `.en.md` |
| HANDBUCH Anhang O | Titel + Skill-Lokation + Aktivierungs-Schritte + Migrations-Hinweise auf Bundle umgestellt | `HANDBUCH.md` + `HANDBUCH.en.md` |
| Migration | `migrate_boo_74()` + ALL_ISSUES | `bootstrap/scripts/migrate-to-v2.sh` |
| Migration-Checklist | §BOO-74 (DE+EN) | `bootstrap/references/migration-checklist-v1-to-v2.md` + `.en.md` |
| Sync-Konvention | Master-vs-Mirror-Doku NEU | `bootstrap/references/skills-setup.md` + `.en.md` |

## Skill-Versions-Bumps

- `bootstrap` 3.28.0 → 3.29.0 (minor: Skill-Quelle umgestellt, neue Zusatzfrage)
- `dpo` unveraendert (v1.1.0 — nur vendored)
- `security-architect` unveraendert (v1.1.0 — nur vendored)

## Migration fuer Bestands-Projekte

`migrate_boo_74()` in `bootstrap/scripts/migrate-to-v2.sh`:

```bash
bash bootstrap/scripts/migrate-to-v2.sh --issue BOO-74
```

Idempotent und nicht-destruktiv. Ergebnis:

- `dpo/` + `security-architect/` aus dem Framework-Repo nach `~/.claude/skills/` kopiert (nur falls noch nicht vorhanden).
- Bestehende Installationen bleiben unveraendert.

Operator-Schritte: Bootstrap-Version >= 3.29.0 sicherstellen, Sync-Disziplin bei kuenftigen Skill-Updates merken.

## Designentscheid: Vendoring statt Submodule

Git-Submodule sind operationsschwer (`git submodule init`, `update`, Detached-HEAD-Fallen). Bei diesem Scope (2 Skills, ~25 Dateien) ist Vendoring (normales File-Copy) leichter und robuster. Tradeoff: Sync ist Operator-Pflicht bis das `sync_framework_mirror.sh`-Skript existiert (Folge-Story).

## Noch offen / Folgepunkte

- **`sync_framework_mirror.sh`** (Folge-Story): automatisiert das Mirror-Update bei `publish_skill.py dpo` / `security-architect`. Bis dahin Operator-Pflicht.
- **Weitere Skills ins Bundle?** research / design-md-generator / setup-checklist / skill-creator bleiben vorerst in claudecodeskills (Allzweck-Skills, nicht framework-spezifisch). Bei Bedarf eigene Story.
- **security-architect EN-Variante:** der Skill hat heute nur `SKILL.md` (kein `SKILL.en.md`), weil vor dem 2026-04-17-Zweisprachigkeits-Stichtag erstellt. Bei einem groesseren security-architect-Update zweisprachig nachziehen (CLAUDE.md-Regel).

## Verweise

- Spec: `specs/BOO-74.md` (lokal als BOO-73 geplant, Linear vergab BOO-74)
- HANDBUCH: Anhang O (umgestellt auf Bundle-Skill)
- Bootstrap: `bootstrap/SKILL.md` Phase 5 + Phase 4.4n
- Sync-Konvention: `bootstrap/references/skills-setup.md` §Sync-Konvention
- Migration: `bootstrap/scripts/migrate-to-v2.sh` (`migrate_boo_74`)
- Feedback-Quelle: Operator Tobias, 2026-05-27 (post-Wave-L)
- Linear: <https://linear.app/owlist/issue/BOO-74/>
- Vorherige Welle: `docs/releases/wave-l-multi-operator-coordination.md`
