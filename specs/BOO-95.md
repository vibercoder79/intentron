# BOO-95 — raw-pii-guard.py ruff-clean machen + Hook-Lint-Gate

## Summary

Die kanonische `bootstrap/references/hooks/raw-pii-guard.py` (BOO-93) besteht ein gängiges striktes Ruff-Profil (`line-length = 100`, flake8-bandit `S`) nicht: **9× E501** (Zeilen >100 Zeichen, v.a. deutsche Docstrings/f-strings/argparse-Hilfetexte) + **1× S607** (`subprocess.run(["git", …])` mit partiellem Executable-Pfad). Diese Story (1) glättet die Datei an der Quelle ohne Verhaltens-Änderung und (2) führt ein **framework-eigenes Ruff-Gate** für `bootstrap/references/hooks/*.py` ein, damit ausgelieferte Hooks self-dogfooded werden. Quelle: Upstream-Feld-Feedback privacy-proxy / 2XT (Martin), 2026-06-01.

## Why

`raw-pii-guard.py` ist ein **an Downstream ausgeliefertes Quell-Artefakt**, das per `migrate_boo_93()` byte-identisch in Nutzer-Projekte kopiert wird. Bei der Feld-Installation (Projekt mit `max-line-length 100`) hat die Datei das **Pre-Commit-Gate blockiert** — das Feld musste lokal eine `per-file-ignore`-Ausnahme bauen und die Quelle bewusst unangetastet lassen. Ein Sicherheits-Wächter, der am Sicherheits-Linter scheitert, untergräbt seine eigene Vorbild-Funktion. Ursache hinter dem Symptom: das Framework lintet seine **eigenen** ausgelieferten Python-Hooks bisher **nicht** — kein Repo-weites Ruff-Profil, keine CI-Stufe. Deshalb konnten die 10 Verstöße unbemerkt ausgeliefert werden.

## What

- **Teil A — `raw-pii-guard.py` glätten** (reine Form, Logik unverändert):
  - **S607:** `git` zur Laufzeit via `shutil.which("git")` zum absoluten Pfad auflösen (`None` → leere Liste, bestehendes `FileNotFoundError`-Handling bleibt). Der verbleibende S603 (advisory, nicht autofixbar) wird per gezieltem `# noqa: S603` mit Begründung am Aufruf unterdrückt — feste argv-Liste, kein `shell=True`, kein User-Input.
  - **9× E501:** `_sink_token`-Docstring mehrzeilig; drei `findings.append(…)`-Zeilen via neuer Helfer-Methode `_record(node, sink_name, field)` gekürzt (entfernt zugleich Duplikation); langer `print` per impliziter String-Konkatenation; drei argparse-`help=`-Texte auf Fortsetzungszeilen; `strict`-Zuweisung geklammert mehrzeilig.
- **Teil B — Hook-Lint-Gate (Ursachen-Fix):**
  - `bootstrap/references/hooks/ruff.toml` (Single-Source-Profil: `line-length = 100`, `select = ["E", "F", "S"]`) — gilt auch für lokale Läufe.
  - CI-Workflow `.github/workflows/ruff-hooks.yml` (Muster `hook-sources.yml`): installiert gepinntes Ruff (`0.15.11`) und lintet `bootstrap/references/hooks/` bei jedem Push/PR, der Hooks oder das Profil berührt. Künftige `*.py`-Hooks sind automatisch erfasst.

## Constraints

- **Kein Verhaltens-Change** an `raw-pii-guard.py`: AST-Erkennungslogik, CLI, Exit-Codes, Default-Listen bleiben identisch. `--self-test` muss grün bleiben.
- **Stdlib-only:** `shutil` ist Python-Stdlib — keine neue Laufzeit-Abhängigkeit im Hook.
- **Gezieltes `# noqa` statt blanket-ignore:** genau eine begründete Zeilen-Unterdrückung (S603), kein per-file/per-dir-Ignore — das Gegenteil der Downstream-Notlösung.
- **Profil = `line-length 100` + `E,F,S`:** deckt das im Feld gemeldete Profil ab; bewusst nicht 88 (würde die deutschen Docstrings stärker zerreißen).
- **Ruff-Version gepinnt** in CI (Regeln ändern sich über Versionen → reproduzierbare Befunde).

## Decisions

1. **S607 echt fixen** (`shutil.which`) statt unterdrücken — die saubere Lösung, da ein absoluter Pfad sicherheitlich tatsächlich besser ist.
2. **S603 per gezieltem `# noqa` unterdrücken** — nicht autofixbar, advisory; der Aufruf ist nachweislich sicher. Begründung steht am Code.
3. **Gate als eigener Workflow** (`ruff-hooks.yml`) statt Erweiterung von `hook-sources.yml` — getrennte Verantwortlichkeiten (Drift-Guard vs. Lint), eigener `paths`-Trigger.
4. **Profil als `ruff.toml` im hooks-Ordner** (nicht repo-weit) — lokal + CI nutzen dieselbe Quelle; keine Annahme über die Lint-Strategie des restlichen (nicht-Python-) Repos.
5. **Zielprofil line-length 100** (Operator-/Feld-Vorgabe), nicht 88.

## Acceptance Criteria

1. `ruff check bootstrap/references/hooks/ --select E,F,S --line-length 100` → **0 Findings** (bzw. via hooks/ruff.toml: `ruff check bootstrap/references/hooks/`).
2. `python3 raw-pii-guard.py --self-test` → `SELF-TEST OK`; `python3 -m py_compile` ohne Fehler.
3. Negativ-Probe: ein eingebauter `*.py`-Verstoß im hooks-Ordner lässt `ruff-hooks` fehlschlagen (verifiziert, Wegwerf-Datei).
4. Downstream kann die `per-file-ignore`-Ausnahme zurückbauen (Rückmeldung an Feld).
5. Keine Änderung an Erkennungslogik/CLI/Exit-Codes von `raw-pii-guard.py`.

## Result

- Teil A + B umgesetzt auf Branch `feat/boo-95-ruff-clean`. Ruff `E,F,S @100` = 0 Findings; `--self-test` grün; `py_compile` OK; Negativ-Probe greift. Release Note: v0.6.0 (Wave AE).
</content>
</invoke>
