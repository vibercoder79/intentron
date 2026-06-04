# ADR: Cross-Session-Nummern-/Wave-Drift — akzeptiert + dokumentiert

> Status: **Akzeptiert** (2026-06-04, BOO-153). Operator-Entscheidung: **Variante B**. EN: [`cross-session-drift.en.md`](cross-session-drift.en.md).

## Kontext

Mehrere parallele Claude-Sessions haben am 2026-06-03/04 unabhängig **BOO-Nummern** *und* **Release-Wave-Buchstaben** vergeben, ohne gegen Linear bzw. `docs/releases/` zu prüfen. Ergebnis: Repo-Spec-Nummern und Linear-Nummern sind um **+1 versetzt**, und drei Wave-Buchstaben sind doppelt belegt. Verwandt: Memory „Parallele Git-Sessions: gegen Remote verifizieren".

## Entscheidung

**Variante B** — den Versatz als Konvention **akzeptieren + dokumentieren**, gemergten „Done"-Code **nicht** umbenennen. Variante A (voller Repo==Linear-Renumber) wurde **verworfen**: sie rührt gemergte, abgeschlossene Specs/`migrate_boo_*`-Funktionen an (Audit-Spur, evtl. bereits retrofittete VPS) — Risiko ohne fachlichen Mehrwert. Ein **Prozess-Guard** stoppt künftigen Drift.

## Mapping: Repo-Spec-Nr. ↔ Linear-Nr.

| Thema | Repo-Spec | Linear |
|---|---|---|
| SARIF-Permissions | `BOO-146` | **BOO-147** |
| Remote-CI-Loop | `BOO-147` | **BOO-148** |
| Projekt-Typ-Marker | `BOO-148` | **BOO-149** |
| Branch-Protection Review-Count | `BOO-149` | **BOO-150** |
| eslint DE/EN-Basis-Block | `BOO-150` | **BOO-146** |
| Multi-User-VPS | `BOO-151` | `BOO-151` ✅ deckungsgleich |
| Klon-Portabilität | `BOO-152` | `BOO-152` ✅ deckungsgleich |
| Dieser Drift-Cleanup | `BOO-153` | `BOO-153` ✅ deckungsgleich |

→ Der +1-Versatz betrifft **nur** die CI-Hardening-Gap-Fixes (Repo 146–149 = Linear 147–150) plus die eslint-Story (Repo 150 = Linear 146). Ab BOO-151 ist alles deckungsgleich (Linear-first geprüft).

## Doppelte Wave-Buchstaben (akzeptiert, im Guard als Allowlist)

| Wave | Thema 1 | Thema 2 |
|---|---|---|
| `BA` | `maschinen-kontext` (Linear BOO-145) | `nextjs-ci-hardening` (Repo BOO-140–143) |
| `BB` | `ci-hardening-gaps` (Repo BOO-146–149) | `multi-user-vps` (Linear BOO-151) |
| `BC` | `eslint-de-en-align` (Linear BOO-146) | `klon-portabilitaet` (Linear BOO-152) |

## Prozess-Guard (verhindert Wiederholung)

1. **Automatisch:** `docs/.github/scripts/docs_drift_check.py` Check 5 — **neue** doppelte Wave-Buchstaben in `docs/releases/` → FAIL. Die drei Alt-Dopplungen oben sind als Allowlist (`ba`, `bb`, `bc`) zugelassen.
2. **Konvention (manuell):** Vor der Vergabe **(a)** einer BOO-Nummer → Linear prüfen (`list_issues`, Team „Bootstrapping Evolution"); **(b)** eines Wave-Buchstabens → `docs/releases/` prüfen (höchsten Zwei-Buchstaben-Wave +1).

## Konsequenzen

- Repo-Spec-Nrn 146–150 bleiben dauerhaft +1 zu Linear versetzt — **dokumentiert hier**, kein verstecktes Risiko.
- Keine gebrochenen Links / keine Audit-Spur-Verwirrung durch Umbenennen.
- Das PR-#48-Fehl-Attachment an Linear BOO-146 wurde entfernt (Titel-Auto-Link).
- Künftiger Nummern-/Wave-Drift wird durch den Guard abgefangen.
