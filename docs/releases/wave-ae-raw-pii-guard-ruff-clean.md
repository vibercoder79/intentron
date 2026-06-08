# Wave AE — raw-pii-guard ruff-clean + Hook-Lint-Gate (BOO-95)

> 🌐 **Sprache:** Deutsch (diese Datei) · [🇬🇧 English](wave-ae-raw-pii-guard-ruff-clean.en.md)

**Linear:** [BOO-95](https://linear.app/owlist/issue/BOO-95/) · Quelle: Upstream-Feld-Feedback privacy-proxy / 2XT (Martin), 2026-06-01

## Problem

Die in Wave AC ausgelieferte `bootstrap/references/hooks/raw-pii-guard.py` (BOO-93) bestand ein
gaengiges striktes Ruff-Profil (`line-length 100`, flake8-bandit `S`) **nicht** — **9× E501**
(deutsche Docstrings/f-strings/argparse-Hilfetexte) + **1× S607** (`subprocess.run(["git", …])`
mit partiellem Executable-Pfad). Die Datei wird per `migrate_boo_93()` byte-identisch in
Nutzer-Projekte kopiert; bei der Feld-Installation (Projekt mit `max-line-length 100`)
blockierte sie das **Pre-Commit-Gate** — das Feld musste lokal eine `per-file-ignore`-Ausnahme
bauen. Ironie: der Security-Guard scheitert am Security-Linter. Ursache hinter dem Symptom: das
Framework lintet seine **eigenen** ausgelieferten Python-Hooks bisher **nicht** — kein
Repo-weites Ruff-Profil, keine CI-Stufe.

## Stories

| Story | Inhalt | Status |
|-------|--------|--------|
| **BOO-95** | raw-pii-guard.py ruff-clean machen (Quelle glaetten) + framework-eigenes Hook-Lint-Gate | ✅ done |

## Was sich aendert

- **Teil A — Quelle geglaettet (kein Verhaltens-Change):**
  - **S607:** `git` zur Laufzeit via `shutil.which("git")` zum absoluten Pfad aufgeloest
    (`None` → leere Liste, bestehendes `FileNotFoundError`-Handling bleibt). Verbleibendes
    **S603** (advisory, nicht autofixbar) per gezieltem `# noqa: S603` mit Begruendung am Aufruf
    unterdrueckt — feste argv-Liste, kein `shell=True`, kein User-Input.
  - **9× E501 umbrochen:** `_sink_token`-Docstring mehrzeilig; drei `findings.append(…)`-Zeilen
    via neuer Helfer-Methode `_record(node, sink_name, field)` gekuerzt (entfernt zugleich
    Duplikation); langer `print` per impliziter String-Konkatenation; drei argparse-`help=`-Texte
    auf Fortsetzungszeilen; `strict`-Zuweisung geklammert mehrzeilig. `--self-test` weiter gruen.
- **Teil B — Hook-Lint-Gate (Ursachen-Fix):**
  - `bootstrap/references/hooks/ruff.toml` (Single-Source-Profil: `line-length = 100`,
    `select = ["E", "F", "S"]`, lokal + CI).
  - CI-Workflow `.github/workflows/ruff-hooks.yml` (gepinntes Ruff `0.15.11`), der die
    kanonischen Hooks bei jedem Hook-/Profil-Touch lintet. Kuenftige `*.py`-Hooks automatisch
    erfasst.

## Designentscheid

- **S607 echt fixen** (`shutil.which`) statt unterdruecken — ein absoluter Pfad ist
  sicherheitlich tatsaechlich besser.
- **S603 per gezieltem `# noqa` unterdruecken** statt blanket-ignore — das Gegenteil der
  Downstream-Notloesung. Begruendung steht am Code.
- **Gate als eigener Workflow** (`ruff-hooks.yml`) statt Erweiterung von `hook-sources.yml`
  — getrennte Verantwortlichkeiten (Drift-Guard vs. Lint), eigener `paths`-Trigger.
- **Profil als `ruff.toml` im hooks-Ordner** (nicht repo-weit) — lokal + CI nutzen dieselbe
  Quelle, keine Annahme ueber die Lint-Strategie des restlichen (nicht-Python-) Repos.
- **Zielprofil `line-length 100`** (Feld-Vorgabe), bewusst nicht 88 (wuerde die deutschen
  Docstrings staerker zerreissen).

## Verifiziert

- `ruff check bootstrap/references/hooks/` (E,F,S @100) → **0 Findings**.
- `python3 raw-pii-guard.py --self-test` → `SELF-TEST OK`; `py_compile` ohne Fehler.
- Negativ-Probe: eingebauter `*.py`-Verstoss laesst `ruff-hooks` fehlschlagen (Wegwerf-Datei).
- Keine Aenderung an Erkennungslogik/CLI/Exit-Codes von `raw-pii-guard.py`.

## Effekt

Der ausgelieferte Guard besteht jetzt selbst ein striktes Bandit-Profil; Downstream braucht keine
`per-file-ignore`-Ausnahme mehr und kann sie zurueckbauen. Self-Dogfooding via CI verhindert
Wiederholung.

## Verweise / Release

- Branch `feat/boo-95-ruff-clean`. Release: **v0.6.0 (Wave AE)** — siehe
  `docs/releases/v0.6.0-overview.md`, Detail-Spec `specs/BOO-95.md`.
