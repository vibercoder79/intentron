# BOO-89 — DRY: coverage-check.sh Single-Source-of-Truth

## Summary

`coverage-check.sh` existiert dreifach: als Heredoc-Template in `file-templates.md` (DE), in `file-templates.en.md` (EN) und eingebettet in `migrate-to-v2.sh` (Funktion `migrate_boo_15`). Jeder Fix am Hook bedeutet drei synchrone, byte-identische Edits (zuletzt BOO-88 fuer einen Ein-Zeilen-Bug). Diese Story stellt eine Single-Source-of-Truth fuer den Hook-Body her, damit ein Fix nur an einer Stelle passiert.

## Why

BOO-88 brauchte drei identische Edits fuer einen einzigen Ein-Zeilen-Bug. Dasselbe Drift-Risiko gilt fuer alle anderen gescaffoldeten Hooks (spec-gate, dependency-check, pre-edit-bodyguard), die nach demselben Triple-Copy-Muster verteilt sind. Solange der Hook-Body an drei Stellen dupliziert liegt, ist jeder Fix eine manuelle Sync-Aufgabe ohne Sicherung.

Konsequenzen ohne diese Story:

- Kopien driften auseinander, sobald ein Edit eine der drei Stellen vergisst
- Bugfixes werden an einem Ort gemacht, an den anderen vergessen — stiller Versionsunterschied
- Frisch gescaffoldete Projekte erhalten veraltete Hook-Staende, je nachdem welche Kopie zuletzt gepflegt wurde
- Reviewer koennen Hook-Aenderungen nicht mehr an einer Stelle pruefen — Audit-Aufwand steigt pro Hook

## What

Folge-/Refactor-Story — finale Loesung wird in der Umsetzung entschieden. Optionen:

- **(a) Hook-Body als eigene Datei:** Hook-Bodies nach `bootstrap/references/hooks/*.sh` auslagern (z.B. `coverage-check.sh`). `file-templates.md`, `file-templates.en.md` und `migrate-to-v2.sh` referenzieren die Datei statt sie zu duplizieren (Include/Read-Source statt Heredoc-Copy). Pruefen, ob das Scaffolding den Datei-Read ohne Netzwerk leisten kann.
- **(b) CI-/Build-Check auf Byte-Identitaet:** Falls Auslagerung das dependency-freie Bootstrap bricht, stattdessen ein Check-Script, das die drei Kopien auf Byte-Identitaet vergleicht und bei Drift mit Fehler bricht (lokal + im spec-gate/CI-Lauf).
- **Verallgemeinerung:** Gewaehltes Muster gilt potenziell fuer alle gescaffoldeten Hooks (spec-gate, dependency-check, pre-edit-bodyguard), nicht nur coverage-check. In der Umsetzung entscheiden, ob direkt mitgezogen oder als Folge-Story isoliert.

## Constraints

- **Dependency-frei:** Keine externen Tools, keine Package-Manager. Bootstrap-Scaffolding muss ohne Netzwerk funktionieren.
- **Reiner Refactor:** Keine Verhaltensaenderung am Hook-Output. Der erzeugte `coverage-check.sh` im Zielprojekt muss byte-identisch zum bisherigen Stand bleiben.
- **DE + EN konsistent:** Beide Template-Sprachen muessen denselben Single-Source ziehen.
- **Pragma-Check:** Variante (b) ist der pragmatische Minimal-Eingriff, wenn (a) das dependency-freie Bootstrap gefaehrdet — kein Over-Engineering eines Include-Systems, wenn ein Identitaets-Check reicht.
- **Security-Check:** Ausgelagerte Hook-Bodies oder Check-Scripts duerfen keine neue Ausfuehrungs-Oberflaeche schaffen (kein `eval`, kein Pfad aus Variablen, kein Schreibzugriff ausserhalb des Scaffolding-Ziels). Hook-Body bleibt statischer, reviewbarer Quelltext.
- **Mittelweg-Begruendung:** Volle Template-Engine waere Over-Engineering (verletzt dependency-frei); drei Kopien einfach so lassen waere die Drift-Schuld weitertragen. Mittelweg: eine Quelle plus — falls Include nicht moeglich — ein automatischer Identitaets-Wachhund, der Drift hart bricht.

## Decisions

1. Single-Source-of-Truth ist das Ziel, nicht "mehr Disziplin beim manuellen Sync".
2. Auslagerung (a) wird bevorzugt, solange sie das dependency-freie Bootstrap nicht bricht — sonst Fallback auf Identitaets-Check (b).
3. Verhalten bleibt unveraendert (reiner Refactor) — der erzeugte Hook im Zielprojekt darf sich nicht aendern.
4. Muster wird so gebaut, dass es auf die anderen gescaffoldeten Hooks uebertragbar ist.

## Agent-Pattern

**Gewaehltes Pattern:** sub-agents (sequentiell).

**Begruendung:** Abgegrenzte, voneinander abhaengige Brocken (erst Quelle/Check entwerfen, dann die drei Referenz-Stellen umstellen, dann EN-Pass). Sequentiell statt parallel, weil die Referenz-Umstellungen auf der zuvor festgelegten Quelle aufbauen. EN-Pass als eigener Schritt (kein langes Heredoc im selben Sub-Agent, Memory feedback_subagent_long_heredoc_timeout). Hard-Constraint pro Sub-Agent: kein neues Hook-Verhalten erfinden, nur die Duplikation aufloesen (Memory feedback_subagent_spec_fabrication).

## Validation

- `coverage-check.sh` aus frischem Bootstrap byte-identisch zum Stand vor dem Refactor (Diff leer)
- Bootstrap-Lauf ohne Netzwerk erzeugt den Hook korrekt (Variante (a) oder (b))
- Bei kuenstlich eingefuegter Drift bricht der Check (Variante (b)) bzw. existiert nur noch eine Quelle (Variante (a))
- DE- und EN-Scaffolding erzeugen identischen Hook-Body
- `migrate_boo_15` erzeugt weiterhin denselben Hook
- `git diff --check` clean

## Acceptance Criteria

- [ ] Single-Source-of-Truth fuer `coverage-check.sh` hergestellt (Auslagerung (a) oder Identitaets-Check (b))
- [ ] Alle drei bisherigen Kopien (`file-templates.md`, `file-templates.en.md`, `migrate-to-v2.sh`/`migrate_boo_15`) ziehen aus der einen Quelle bzw. werden vom Check abgesichert
- [ ] Erzeugter Hook byte-identisch zum bisherigen Stand (kein Verhaltens-Drift)
- [ ] Bootstrap bleibt dependency-frei und netzwerklos lauffaehig
- [ ] DE + EN konsistent
- [ ] Uebertragbarkeit auf weitere gescaffoldete Hooks dokumentiert (mind. als Folge-Hinweis)
- [ ] Migrations-/Release-Notiz, falls Hook-Pfad oder Check neu eingefuehrt

## Dependencies

- **BOO-88** — deckte das Triple-Copy-Drift-Problem auf (Ausloeser dieser Story)
- **BOO-15** — Ursprung von coverage-check (`migrate_boo_15`)

## Session-Referenz

Folge-Story aus BOO-88, Session 2026-05-31. Linear: <https://linear.app/owlist/issue/BOO-89/>.

## Rollout

Reiner Refactor, additiv. Bestands-Projekte sind nicht betroffen (ihr bereits gescaffoldeter Hook bleibt). Neue Bootstrap-Laeufe ziehen automatisch die Single-Source. Bei Variante (b) laeuft der Identitaets-Check kuenftig in spec-gate/CI mit.
