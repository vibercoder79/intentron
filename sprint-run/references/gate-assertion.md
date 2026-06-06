# Gate-Assertion — Post-Story-Verifikation gegen meta.json

Referenz zu `/sprint-run` Schritt 4.5b. Maschinelle Verifikation, dass `/implement` pro Story alle
Pflicht-Gates ausgefuehrt (oder nur legitim uebersprungen) hat — die Absicherung gegen einen
**still** uebersprungenen Lint-/Test-/Security-Check.

## Quelle: meta.json (BOO-36/84)

`/implement` schreibt in Schritt 6f-bis `journal/reports/local/<YYYY-MM-DD_HHMM>_<STORY>/meta.json`.
Relevante Felder:

- `change_type` — `code` (Default) | `workflow` | `config` | `infrastructure` | `content`
- `skipped_gates` — Liste uebersprungener Gates (mit Grund)
- `override_audit` — dokumentierte Operator-Overrides (z.B. Coverage < 80 % mit Begruendung)
- `iterations` — Iterationen pro Gate

## Legitimitaets-Regel

Ein Eintrag in `skipped_gates` ist **legitim** genau dann, wenn:

1. er durch `change_type` gedeckt ist — im Non-Code-Modus (`/implement` Schritt 5.7) sind die
   Code-Gates 6a/6a-bis/6a-tris/6a-quart legitim uebersprungen; **oder**
2. er in `override_audit` mit Begruendung belegt ist (Operator-Override).

Sonst → **unbegruendeter Skip → Story-Fail**.

Zusatz fuer Non-Code-Stories: die in Non-Code **harten** Gates 6c (Architektur-Quick-Check),
6d (Smoke Test), 6e (Security-Findings) muessen Evidenz tragen — fehlt sie → Fail.

Fehlt `meta.json` komplett → Fail (Gate-Lauf nicht nachweisbar, kein „leise gruen").

## Pseudocode

```text
meta = read(journal/reports/local/<run>/meta.json)        # fehlt -> FAIL
for g in meta.skipped_gates:
    if g.gate in CODE_GATES and meta.change_type in {workflow,config,infrastructure,content}: ok
    elif g.gate in meta.override_audit: ok
    else: FAIL(story, gate=g)
if meta.change_type != "code":
    for g in [6c, 6d, 6e]:
        if not has_evidence(meta, g): FAIL(story, gate=g)
PASS   # erst dann Merge (Schritt 4.6)
```

## Bei Fail

- Story zurueck auf `Backlog` (In Progress → Backlog).
- Operator-Notify: Story-ID + welches Gate + Grund.
- Kein Merge. `daemon_fail_policy` (`stop` | `continue`) bestimmt, ob der Sprint anhaelt.

## Einordnung der drei Ebenen

- **Ebene 1** — `/implement`-Gates (Schritt 6): prompt-getrieben.
- **Ebene 2** — Remote-CI-Gate vor Merge (BOO-148): mechanisch.
- **4.5b ist die maschinelle Bruecke:** verifiziert Ebene 1 gegen den Maschinen-Output (`meta.json`),
  **bevor** Ebene 2 merged. Aendert `/implement` nicht — liest nur dessen `meta.json`.

Sketch: `docs/sprint-run-flow.png` + `docs/story-breakdown.png` (HANDBUCH Anhang AD).
