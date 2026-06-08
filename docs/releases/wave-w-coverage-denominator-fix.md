# Release Notes - Wave W Coverage-Hook-Nenner-Fix

> 🌐 **Sprache:** Deutsch (diese Datei) · [🇬🇧 English](wave-w-coverage-denominator-fix.en.md)

Stand: 2026-05-31

## Zweck

Wave W (BOO-88) behebt einen Zaehl-Bug im Diff-Coverage-Gate `coverage-check.sh` (Layer aus BOO-15). Der Nenner der Coverage-Quote zaehlte bisher **alle** hinzugefuegten Zeilen — inklusive Kommentaren und Leerzeilen. Dadurch fiel die Quote zu niedrig aus und das Gate blockte faelschlich. Der Fix bezieht den Nenner jetzt nur noch aus **ausfuehrbaren Statement-Zeilen**.

## Warum

Feld-Feedback aus dem Projekt **privacy-proxy** (PP-001): Ein Commit mit gut dokumentiertem, getestetem Code wurde vom Coverage-Gate abgelehnt. Ursache war der naive Nenner — er zaehlte jede hinzugefuegte Zeile als "abzudeckende Zeile", auch Kommentare und Leerzeilen, die ein Coverage-Tool gar nicht abdecken kann.

Beispiel: 8 ausfuehrbare Zeilen, davon alle getestet, plus 4 Kommentar- und 2 Leerzeilen im selben Diff → naiver Nenner 14, Zaehler 8 → **57 %** → Gate blockt bei Schwelle 60 %. Die tatsaechliche Diff-Coverage betrug **100 %**. Wer sauberer kommentiert, wurde bestraft — ein Fehlanreiz direkt gegen die KI-Tauglichkeits-Ziele des Frameworks.

## Der Bug

Die Zaehlschleife im Hook nahm jede `+`-Zeile aus dem staged Diff als Nenner-Kandidat. Kommentar- und Leerzeilen landeten so im Nenner, obwohl sie nie als "covered" markiert werden koennen. Folge: systematisch zu niedrige Quote, proportional zur Kommentar-Dichte des Diffs.

## Der Fix

- **Nenner = ausfuehrbare Statement-Zeilen.** Die Menge der zaehlbaren Zeilen kommt jetzt direkt aus dem Coverage-Report:
  - **Node (c8):** aus der `statementMap` des JSON-Reports.
  - **Python (pytest-cov):** aus `executed_lines ∪ missing_lines`.
- **Neue Funktionen `parse_statement_lines_*`** extrahieren diese Mengen pro Datei.
- **`continue`-Guard** in der Zaehlschleife: hinzugefuegte Zeilen, die nicht in der Statement-Menge liegen (Kommentare, Leerzeilen, schliessende Klammern), werden uebersprungen — sie zaehlen weder in Zaehler noch Nenner.
- **KEINE Regex** zur Kommentar-Erkennung — die Statement-Mengen kommen aus dem Coverage-Tool selbst. Damit bleibt der Hook **dependency-frei** (nur `bash` + `python3`-Stdlib) und sprach-korrekt (kein fragiles Pattern-Matching pro Sprache).

Verifiziert: 8 Code + 4 Kommentar + 2 Leerzeilen → **100 %** (vorher 57 %); 6 von 8 ausfuehrbaren Zeilen getestet → **75 %**.

## Konkrete Aenderungen

Der Fix ist an **drei Quellstellen** gespiegelt (Single-Source-Prinzip noch nicht erreicht — siehe Folge-Themen):

| Bereich | Datei |
|---|---|
| Template DE | `bootstrap/references/file-templates.md` §coverage-check.sh (v2, BOO-88) |
| Template EN | `bootstrap/references/file-templates.en.md` §coverage-check.sh (v2, BOO-88) |
| Migration | Heredoc in `migrate_boo_15` in `bootstrap/scripts/migrate-to-v2.sh` |
| Migration-Checklist §BOO-88 (DE+EN) | `bootstrap/references/migration-checklist-v1-to-v2.md` + `.en.md` |

- **Versions-Marker:** Das Skript traegt jetzt `# coverage-check v2`. Daran erkennt die Migration eine alte v1 (fehlender Marker).
- **Ersetzende Migration mit `.bak`:** `migrate_boo_15` legt die Datei nicht mehr nur bei Abwesenheit an, sondern erkennt eine alte v1, sichert sie nach `.claude/hooks/coverage-check.sh.bak` und schreibt die v2. Idempotent — eine vorhandene v2 wird uebersprungen (`[SKIP]`).

## Migration

`bash bootstrap/scripts/migrate-to-v2.sh --issue BOO-15`

- Der Fix wird **ueber den BOO-15-Coverage-Installer** ausgeliefert — es gibt **kein** separates `--issue BOO-88`.
- **Bestands-Installs muessen erneut migrieren:** Projekte, die BOO-15 bereits hatten, behalten sonst die buggy v1. `migrate_boo_15` ersetzt jetzt v1 (statt nur bei fehlender Datei anzulegen), sichert nach `.bak` und schreibt v2.
- Verifikation: `bash -n .claude/hooks/coverage-check.sh` (Exit 0); `grep 'coverage-check v2' .claude/hooks/coverage-check.sh` (Marker vorhanden). Rollback: `mv .claude/hooks/coverage-check.sh.bak .claude/hooks/coverage-check.sh`.

## Skill-Versions-Bumps

- keine (Hook-Template + Migration + Doku, kein Skill-Code-Change). Reiner Bugfix — Schwellwerte und `/implement`-Workflow unveraendert.

## Folge-Themen

- **DRY / Single-Source:** Der Hook-Body liegt aktuell dreifach (Template DE, Template EN, Migration-Heredoc). Ein Bugfix muss an drei Stellen gespiegelt werden — fehleranfaellig. Folge-Thema: eine kanonische Quelle, aus der Templates und Migration generiert werden.
- **Contribute-Back-Schleife:** Der Bug kam aus dem Feld (privacy-proxy / PP-001). Folge-Thema: ein formaler Pfad, ueber den Projekt-Findings strukturiert zurueck ins Framework-Backlog fliessen.

## Verweise

- Migration-Checklist: `bootstrap/references/migration-checklist-v1-to-v2.md` §BOO-88 (+ `.en.md`)
- Kanonische Templates: `bootstrap/references/file-templates.md` §coverage-check.sh (v2, BOO-88)
- Migration: `migrate_boo_15` in `bootstrap/scripts/migrate-to-v2.sh`
- Feld-Feedback: privacy-proxy / PP-001
- Linear: BOO-88
