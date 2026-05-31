# BOO-90 — Contribute-Back-Schleife fuer Feld-Fixes

## Summary

Wenn ein deployter Factory-Nutzer einen Bug in einem kopierten Governance-Artefakt lokal fixt (wie BOO-88 / `coverage-check` aus dem privacy-proxy-Projekt), gibt es heute keinen Mechanismus, der den Fix zurueck in die Factory-Quelle bringt. Jedes Projekt fixt denselben Bug erneut; der Master bleibt buggy. Diese Story entwirft eine leichtgewichtige Contribute-Back-Schleife, die Feld-Fixes zurueck an die Quelle bringt — ohne Auto-Push aus Kundenprojekten.

## Why

BOO-88 lief als manuelle Schleife: Nutzer entdeckt Bug → meldet an Tobias → Fix wird ins Framework eingepflegt. Das funktioniert genau einmal und haengt an einer Person. Sobald mehr als ein deploytes Projekt existiert, skaliert das nicht und ist fuer regulierte Kunden nicht audit-tauglich (keine nachvollziehbare Herkunft des Fixes, kein dokumentierter Ruecklauf-Pfad).

Konsequenzen ohne diese Story:

- Jedes deployte Projekt fixt denselben Master-Bug neu — Mehrfacharbeit
- Master-Quelle bleibt buggy, neue Bootstraps scaffolden den Bug weiter
- Ruecklauf haengt an manueller Mensch-zu-Mensch-Weitergabe (Bus-Faktor 1)
- Kein audit-tauglicher Herkunfts-Nachweis fuer Fixes — Blocker bei regulierten Kunden

## What

Folge-/Refactor-Story — finale Loesung wird in der Umsetzung entschieden. Optionen:

- **(a) Konvention/Skill `/contribute-fix`:** Erzeugt aus einem lokalen Patch in einem Kundenprojekt einen sauberen, vom Projektkontext entkoppelten Patch plus einen Issue-Vorschlag zurueck an die Factory-Quelle. Operator reviewt und entscheidet, ob er ihn einreicht — kein automatischer Push.
- **(b) Versions-Marker verallgemeinern:** Den Versions-Marker-Ansatz aus BOO-88 (`coverage-check v2`) auf alle gescaffoldeten Artefakte ausweiten, damit Migrationen alte Staende zuverlaessig erkennen und ersetzen koennen. Schafft die Grundlage, einen Master-Fix gezielt in Bestands-Projekte zu ziehen.
- **(c) Verbindung zu Master/Mirror:** Anbindung an die geplante `sync_framework_mirror.sh` (Master ↔ Mirror) und an `framework-upgrade.md` (BOO-60), sodass Contribute-Back und Upgrade-Pfad denselben Kanal nutzen statt zweier paralleler Mechanismen.

In der Umsetzung entscheiden, ob (a)/(b)/(c) einzeln, kombiniert oder gestaffelt umgesetzt werden.

## Constraints

- **Leichtgewichtig, kein Zwang:** Kein verpflichtender Schritt im Nutzer-Workflow. Wer keinen Fix beitragen will, wird nicht blockiert.
- **Operator behaelt Kontrolle:** Kein Auto-Push aus Kundenprojekten. Der Ruecklauf erzeugt einen Vorschlag (Patch + Issue), die Einreichung ist eine bewusste Operator-Entscheidung.
- **Audit-Tauglichkeit:** Herkunft des Fixes (Quell-Projekt, Anlass) muss im Vorschlag nachvollziehbar sein — fuer regulierte Kunden.
- **Pragma-Check:** Schmaler Einstieg ist eine reine Konvention plus Helfer, der einen sauberen Patch erzeugt — keine eigene Sync-Infrastruktur bauen, solange `sync_framework_mirror.sh`/BOO-60 den Transportweg liefern koennen.
- **Security-Check:** Patch-Export darf keine Projekt-Secrets, Kundendaten oder lokalen Pfade mitschleppen (Scrubbing/Review-Pflicht vor Ausgabe). Kein automatischer Netzwerk-Push aus dem Kundenprojekt — Exfiltrations-Oberflaeche bewusst vermeiden. Eingereichte Patches durchlaufen denselben Review wie jeder andere Master-Change.
- **Mittelweg-Begruendung:** Voll-automatischer Upstream-Sync aus jedem Kundenprojekt waere zu invasiv (Security/Kontroll-Risiko, verletzt "Operator behaelt Kontrolle"); die rein manuelle Mensch-Schleife skaliert nicht. Mittelweg: assistierter, reviewbarer Vorschlag mit Operator als Gate.

## Decisions

1. Kein Auto-Push aus Kundenprojekten — Ruecklauf ist immer ein Operator-Gate.
2. Contribute-Back nutzt nach Moeglichkeit denselben Kanal wie der Upgrade-Pfad (Master/Mirror, BOO-60) statt eigener Parallel-Infrastruktur.
3. Versions-Marker werden verallgemeinert, damit Migrationen alte Staende erkennen+ersetzen koennen (Basis fuer gezielten Master→Projekt-Rueckfluss).
4. Audit-Herkunft ist Pflichtbestandteil jedes erzeugten Fix-Vorschlags.

## Agent-Pattern

**Gewaehltes Pattern:** sub-agents (sequentiell).

**Begruendung:** Abgegrenzte, aufeinander aufbauende Brocken (Patch-/Scrubbing-Konvention, Versions-Marker-Verallgemeinerung, Anbindung an Master/Mirror+Upgrade-Pfad). Sequentiell, weil die Marker- und Sync-Anbindung auf der zuvor definierten Patch-Konvention aufsetzen. Hard-Constraint pro Sub-Agent: keinen Auto-Push und keine eigene Transport-Infrastruktur erfinden, sondern an BOO-60/BOO-74 andocken (Memory feedback_subagent_spec_fabrication).

## Validation

- `/contribute-fix` (bzw. Konvention) erzeugt aus einem lokalen Patch einen sauberen, kontext-entkoppelten Patch ohne Projekt-Secrets/Pfade
- Erzeugter Vorschlag enthaelt Herkunfts-/Anlass-Angabe (audit-tauglich)
- Kein automatischer Push aus dem Kundenprojekt — Ausgabe ist ein Vorschlag, kein Commit am Master
- Versions-Marker erlauben einer Migration, einen alten Artefakt-Stand zu erkennen und zu ersetzen
- Contribute-Back-Kanal deckt sich mit Master/Mirror+Upgrade-Pfad (kein zweiter paralleler Mechanismus)

## Acceptance Criteria

- [ ] Contribute-Back-Konvention/Skill `/contribute-fix` entworfen (Patch + Issue-Vorschlag zurueck an Quelle)
- [ ] Patch-Export scrubbt Secrets, Kundendaten und lokale Pfade vor Ausgabe
- [ ] Kein Auto-Push aus Kundenprojekten — Operator-Gate vor jeder Einreichung
- [ ] Herkunfts-/Anlass-Angabe im Vorschlag (audit-tauglich)
- [ ] Versions-Marker-Ansatz aus BOO-88 verallgemeinert (Migration erkennt+ersetzt alte Staende)
- [ ] Anbindung an `sync_framework_mirror.sh` (BOO-74) und `framework-upgrade.md` (BOO-60) geklaert
- [ ] Migrations-/Release-Notiz

## Dependencies

- **BOO-88** — Ursprung der manuellen Feld-Fix-Schleife (Ausloeser dieser Story)
- **BOO-74** — Master/Mirror-Konvention (`sync_framework_mirror.sh`)
- **BOO-60** — Upgrade-Pfad (`framework-upgrade.md`)

## Session-Referenz

Folge-Story aus BOO-88 plus agentic-security-Auswertung, Session 2026-05-31. Linear: <https://linear.app/owlist/issue/BOO-90/>.

## Rollout

Additiv und optional. Bestands-Projekte sind nicht betroffen, solange kein Fix beigetragen wird. Die Schleife greift erst, wenn ein Operator bewusst `/contribute-fix` ausloest. Verallgemeinerte Versions-Marker werden ueber den bestehenden Migrations-Pfad nachgezogen.
