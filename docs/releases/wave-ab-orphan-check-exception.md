# Wave AB — orphan-check Work-Item-Ausnahme (BOO-92)

**Linear:** [BOO-92](https://linear.app/owlist/issue/BOO-92/) · Quelle: Upstream-Feedback Feld-Installation privacy-proxy / 2XT (Martin), 2026-05-31

## Problem

Der optionale `orphan-check.sh`-Hook erzwingt: jede neue `*.md` muss im Doku-Hub
`ARCHITECTURE_DESIGN.md` **§9 Referenzen** registriert sein. Das zwang **auch** Story-Specs
(`specs/<PREFIX>-<NUM>.md`) und Backlog-Records (`docs/project/backlog/record-*.md`) in den Hub —
obwohl die bereits eigene Indizes haben (`specs/` = ~25 `BOO-NN.md`-Dateien, Backlog-`README.md`,
`links.spec` im Record). Ein zusaetzlicher §9-Eintrag pro Story ist redundanter Pflicht-Aufwand.
Folge: entweder Reibung bei jeder Story, oder der Operator schaltet den Hook ganz ab — dann geht
der Hub-Schutz (verwaiste Dokumente verhindern) komplett verloren.

## Was sich aendert

- **`ORPHAN_EXCLUDE`-Variable** im orphan-check-Snippet (`bootstrap/references/hooks-setup.md` DE +
  `hooks-setup.en.md` EN), per Env ueberschreibbar. Der Default nimmt `specs/<PREFIX>-<NUM>.md` und
  `docs/project/backlog/record-*.md` von der Hub-Pruefung aus; alle anderen `.md` werden weiter
  gegen den Hub geprueft:
  ```bash
  ORPHAN_EXCLUDE="${ORPHAN_EXCLUDE:-^(docs/project/backlog/record-.*\.md|specs/[A-Z]+-[0-9]+\.md)$}"
  NEW_MDS=$(git diff --cached --name-only --diff-filter=A \
    | grep -E '\.md$' \
    | grep -vE "$ORPHAN_EXCLUDE" || true)
  ```
- **Konfigurierbar statt hartverdrahtet** (Anmerkung des Felds aufgegriffen) — Projekte koennen
  `ORPHAN_EXCLUDE` ueberschreiben, um eigene Pfad-Konventionen zu ergaenzen/ersetzen.
- **§9-Klarstellung:** Der Feld-Vorschlag nannte „§6 References"; der reale Pflicht-Abschnitt heisst
  **§9 Referenzen** (`doc-architecture-proposal.md`). Die Story zielt auf §9.
- **`migrate_boo_92()`** in `migrate-to-v2.sh`: patcht eine bereits installierte
  `.claude/hooks/orphan-check.sh` idempotent auf die `ORPHAN_EXCLUDE`-Variante (Backup `.bak`) — nur
  wenn `ORPHAN_EXCLUDE` noch nicht vorhanden ist. Ohne installierten Hook (Normalfall, optionaler
  Hub-Hook): Skip. Registrierung von `BOO-92` in `ALL_ISSUES`.

## Designentscheid

- **Fix im Doku-Snippet** (`hooks-setup.md`), da orphan-check nur als Doku-Snippet existiert und
  keine reale kanonische `.sh` gescaffoldet wird.
- **Ausnahmen ueber eine ueberschreibbare Variable** (`ORPHAN_EXCLUDE`), nicht fest verdrahtet — die
  sauberere Upstream-Form, die das Feld selbst angeregt hat.
- **Default-Ausnahmen = Specs + Backlog-Records** — entsprechen den INTENTRON-Pfad-Konventionen.
- **Auf §9 zielen** (Repo-Realitaet), nicht §6 (Feld-Vorschlag-Tippfehler).

## Verifiziert

- `specs/BOO-92.md` und `docs/project/backlog/record-*.md` werden vom Filter ausgenommen.
- Eine neue `.md` an beliebiger anderer Stelle (z.B. `docs/foo.md`, `README.md`) wird **weiterhin**
  gegen den Hub geprueft.
- `ORPHAN_EXCLUDE` ist per Env ueberschreibbar.
- `migrate_boo_92` patcht eine bestehende `orphan-check.sh` byte-sauber (Backup `.bak`), ist
  idempotent (zweiter Lauf = Skip), gepatchter Hook ist valides bash (`bash -n`).
- DE/EN-Snippet aequivalent; `git diff --check` clean.

## Rollout

Additiv und rueckwaertskompatibel — eine Variable + ein `grep -vE`, keine neue Dependency.
Default-Verhalten fuer alle anderen `.md` bleibt identisch; nur Work-Item-Docs werden ausgenommen.
Bestands-Projekte mit installiertem `orphan-check.sh` werden via `migrate_boo_92()` idempotent
gepatcht; Projekte ohne den optionalen Hook sind nicht betroffen.

## Effekt

Stories erzeugen keinen kuenstlichen Hub-Eintrag mehr; der Hub-Schutz fuer echte Doku-Artefakte
bleibt erhalten.

## Verweise

- Spec: `specs/BOO-92.md`
- Release-Ueberblick: `docs/releases/v0.6.0-overview.md` (Wave AB)
- Migration: `migrate_boo_92()` in `bootstrap/scripts/migrate-to-v2.sh`
- Linear: BOO-92
