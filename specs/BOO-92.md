# BOO-92 — orphan-check: Work-Item-Dokumente vom Hub-Zwang ausnehmen

## Summary

Der optionale `orphan-check.sh`-Hook (erzwingt: jede neue `*.md` muss im Doku-Hub `ARCHITECTURE_DESIGN.md` **§9 Referenzen** registriert sein) nimmt **Story-Specs** (`specs/<PREFIX>-<NUM>.md`) und **Backlog-Records** (`docs/project/backlog/record-*.md`) über eine **konfigurierbare** Variable `ORPHAN_EXCLUDE` vom Hub-Zwang aus. Diese Work-Item-Dokumente haben bereits eigene Indizes (Backlog-`README.md`, `links.spec` im Record); ein zusätzlicher §9-Eintrag pro Story ist redundanter Pflicht-Aufwand. Quelle: Upstream-Feedback aus der Feld-Installation privacy-proxy / 2XT (Martin), 2026-05-31.

## Why

Der Hook erzwingt für **jede** neue `.md` einen Hub-Eintrag. `specs/` besteht real aus ~25 `BOO-NN.md`-Story-Dateien — jede würde den Hook auslösen und einen künstlichen §9-Eintrag in `ARCHITECTURE_DESIGN.md` verlangen, obwohl Specs über das Backlog indiziert sind. Folge: entweder Reibung bei jeder Story, oder der Operator schaltet den Hook ganz ab → der Hub-Schutz (verwaiste Dokumente verhindern) geht komplett verloren. Eine gezielte Ausnahme für Dokumente mit eigenem Index löst das, ohne den Hub-Zwang für echte Doku-Artefakte aufzuweichen.

## What

- **`bootstrap/references/hooks-setup.md` (DE) + `hooks-setup.en.md` (EN):** Der `orphan-check.sh`-Code-Block ermittelt die neuen `.md` jetzt mit einer Ausnahme. Neue, per Env überschreibbare Variable:
  ```bash
  ORPHAN_EXCLUDE="${ORPHAN_EXCLUDE:-^(docs/project/backlog/record-.*\.md|specs/[A-Z]+-[0-9]+\.md)$}"
  NEW_MDS=$(git diff --cached --name-only --diff-filter=A \
    | grep -E '\.md$' \
    | grep -vE "$ORPHAN_EXCLUDE" || true)
  ```
  Kommentar erklärt Default-Ausnahmen + Override-Mechanik. *Wichtig: orphan-check existiert nur als Doku-Snippet (nicht als kanonisch gescaffoldete `.sh`) — der Fix gehört in den Snippet.*
- **§9-Klarstellung:** Der Feld-Vorschlag nannte „§6 References"; der reale Pflicht-Abschnitt heißt **§9 Referenzen** (`doc-architecture-proposal.md`). Story zielt auf §9.
- **`migrate_boo_92()`** in `migrate-to-v2.sh`: idempotent. Falls ein Projekt bereits eine scharf installierte `.claude/hooks/orphan-check.sh` hat, wird die `NEW_MDS`-Zeile per Backup (`.bak`) auf die `ORPHAN_EXCLUDE`-Variante gepatcht — nur wenn `ORPHAN_EXCLUDE` noch nicht vorhanden ist. Wenn der Hook nicht installiert ist (Normalfall, optionaler Hub-Hook), Skip.
- **`ALL_ISSUES`-Registrierung** von `BOO-92` in `migrate-to-v2.sh`.
- **Release Notes** (DE+EN, v0.6.0).

## Constraints

- **Leichtgewicht:** eine Variable + ein `grep -vE`, keine neue Dependency.
- **Rückwärtskompatibel:** Default-Verhalten für alle anderen `.md` bleibt identisch — nur Work-Item-Docs werden ausgenommen.
- **Konfigurierbar statt hartverdrahtet** (Anmerkung des Felds): `ORPHAN_EXCLUDE` ist per Env überschreibbar, damit Projekte eigene Pfad-Konventionen ergänzen/ersetzen können.
- **DE + EN konsistent** (Snippet, Release Notes).
- **Idempotenz:** zweiter Migrations-Lauf erzeugt keine Diffs (erkennt `ORPHAN_EXCLUDE`).

## Decisions

1. **Fix im Doku-Snippet** (`hooks-setup.md`), da keine reale kanonische `.sh` existiert.
2. **Ausnahmen über eine überschreibbare Variable** (`ORPHAN_EXCLUDE`), nicht fest verdrahtet — die sauberere Upstream-Form, die das Feld selbst angeregt hat.
3. **Default-Ausnahmen = Specs (`specs/<PREFIX>-<NUM>.md`) + Backlog-Records (`docs/project/backlog/record-*.md`)** — entsprechen den INTENTRON-Konventionen.
4. **Auf §9 zielen** (Repo-Realität), nicht §6 (Feld-Vorschlag-Tippfehler).

## Agent-Pattern

**Gewähltes Pattern:** `linear` (Story Points 1).

**Begründung:** Ein Code-Block in zwei Sprach-Dateien plus eine kleine, lokal getestete Migrations-Funktion. Sub-Agent-Overhead wäre größer als der Nutzen. EN-Pass als separater Edit.

## Validation

- `specs/BOO-92.md` (diese Datei) und `docs/project/backlog/record-*.md` werden vom `ORPHAN_EXCLUDE`-Filter ausgenommen — verifiziert mit Test-Eingabe.
- Eine neue `.md` an beliebiger anderer Stelle (z.B. `docs/foo.md`, `README.md`) wird **weiterhin** gegen den Hub geprüft.
- `ORPHAN_EXCLUDE` ist per Env überschreibbar.
- `migrate_boo_92` patcht eine bestehende `orphan-check.sh` byte-sauber (Backup `.bak`), ist idempotent (zweiter Lauf = Skip), und der gepatchte Hook ist valides bash (`bash -n`).
- DE/EN-Snippet äquivalent; `git diff --check` clean.

## Acceptance Criteria

- [ ] `hooks-setup.md` (DE) + `hooks-setup.en.md` (EN): `ORPHAN_EXCLUDE`-Variable + `grep -vE` im orphan-check-Snippet, mit erklärendem Kommentar
- [ ] Default-Ausnahme deckt `specs/<PREFIX>-<NUM>.md` und `docs/project/backlog/record-*.md`
- [ ] `ORPHAN_EXCLUDE` per Env überschreibbar
- [ ] Andere neue `.md` lösen orphan-check weiterhin aus
- [ ] `migrate_boo_92()` implementiert, idempotent, in `ALL_ISSUES` registriert, lokal getestet
- [ ] Release Notes (DE+EN)
- [ ] `git diff --check` clean

## Dependencies

Bezieht sich auf die Doku-Architektur / den Hub (§9 Referenzen) und den optionalen `orphan-check.sh`-Hook (Block C Hub-Auto-Verlinkung). Keine Blocker. Verwandt mit dem Backlog-Record-Schema (eigener Index) und dem Spec-Schema (`specs/<PREFIX>-<NUM>.md`).

## Session-Referenz

Spec geschrieben in Session 2026-06-01 (Abgleich Upstream-Feedback privacy-proxy / 2XT). Linear: <https://linear.app/owlist/issue/BOO-92/>.

## Rollout

Additiv und rückwärtskompatibel. Bestands-Projekte mit installiertem `orphan-check.sh` werden via `migrate_boo_92()` idempotent gepatcht (Backup `.bak`). Projekte ohne den optionalen Hook sind nicht betroffen. Der Default-Filter entspricht den INTENTRON-Pfad-Konventionen; abweichende Projekte setzen `ORPHAN_EXCLUDE`.
