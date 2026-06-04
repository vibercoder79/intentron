# Wave BD — Cross-Session-Drift normalisiert + Guard (BOO-153)

**Was jetzt da ist:** Der durch parallele Sessions entstandene **Nummern-/Wave-Drift** ist sauber dokumentiert und gegen Wiederholung abgesichert — **Variante B** (Operator-Entscheidung): Offset akzeptieren + dokumentieren statt gemergten Code umzubenennen. DE+EN.

## Stories
- **BOO-153** — ADR `cross-session-drift` (Mapping-Tabelle Repo↔Linear + Wave-Dopplungen), docs-drift **Check 5** (Wave-Dopplungs-Guard), PR-#48-Fehl-Attachment entfernt, Vergabe-Konvention.

## Änderungen (DE+EN)
- **Neu:** `docs/domain/adrs/cross-session-drift.md` (+ `.en.md`) — Repo-Spec↔Linear-Mapping (146–150 = +1-Offset; ab 151 deckungsgleich), Wave-Dopplungen (`ba`/`bb`/`bc`), Prozess-Guard, Konsequenzen.
- **`.github/scripts/docs_drift_check.py`:** Check 5 — neue doppelte Wave-Buchstaben → FAIL; Alt-Dopplungen als Allowlist. (Repo-internes Gate, nicht ausgeliefert.)
- **Linear:** PR-#48-Fehl-Attachment von BOO-146 entfernt.

## Wirkung
Der Drift ist jetzt **nachvollziehbar dokumentiert** (kein verstecktes Risiko) und **künftiger** Drift wird automatisch gefangen: doppelte Wave-Buchstaben failen den docs-drift-Check, BOO-Nummern + Wave-Buchstaben werden vor Vergabe gegen Linear bzw. `docs/releases/` geprüft. Dieser Release nutzt selbst den Guard (Wave **bd** = nächster freier Buchstabe, geprüft).

## Abgrenzung
Variante A (voller Renumber) verworfen — kein Anfassen gemergten Done-Codes. Reine Doku-/Governance-Änderung, kein Runtime-Code.

## Verweise
Spec: `specs/BOO-153.md`. Branch: `feat/boo-153-drift-normalisieren`. ADR: `docs/domain/adrs/cross-session-drift.md`. Operator-Quelle: Tobias, 2026-06-04.
