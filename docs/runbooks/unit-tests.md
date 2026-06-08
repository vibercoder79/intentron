# Runbook: Unit-Tests — Ablauf, Gate, Belege

> **Zielgruppe:** Operator:in, die mit `/implement` baut und verstehen will, wie Unit-Tests im Framework laufen — wo die Reports landen, wie das Test-Gate entscheidet und wie der Anti-Platzhalter-Check greift. In unter 10 Minuten. EN: [`unit-tests.en.md`](unit-tests.en.md).

## Wann dieses Runbook?

Du implementierst eine Story mit `/implement` und willst den **Unit-Test-Teil** verstehen: warum das Gate blockt, wie du Diff-Coverage hochbekommst, was ein „Platzhalter-Test" ist und wo die Test-Belege fürs Audit liegen. Für die Operator-Kurzfassung siehe [HANDBUCH Kapitel 8c-bis](../../HANDBUCH.md).

**Abgrenzung:** Hier geht es **nur um Unit-Tests** — einzelne Funktionen/Module isoliert. Integration- und E2E-Tests (mehrere Komponenten nach dem Deployment) sind ein eigenes, hier **nicht** behandeltes Thema. Es gibt bewusst keinen Integration-Test-Skill.

## In einem Satz

Unit-Tests laufen im Test-Gate **6a-quart** von `/implement`, das **zwei** Dinge prüft — *genug* Tests (Diff-Coverage ≥ 80 %) **und** *echte* Tests (Anti-Platzhalter-Check) — und jede Iteration als JUnit-XML, Coverage-JSON und `meta.json`-Zähler unter `journal/reports/local/<run>/` hinterlässt.

---

## Das Test-Gate 6a-quart im Überblick

Der Schritt läuft **im Skill, nicht im Pre-Commit-Hook** — ein Test-Lauf kann Minuten dauern und würde das 10-Sekunden-Budget des Hooks sprengen. Pro Iteration läuft dieser Loop:

1. **Iterations-Counter hochzählen** (`ITER_TESTS`, `ITER_COVERAGE` synchron).
2. **Test-Lauf** mit Coverage-Output **und** JUnit-XML (Kommandos je Stack unten).
3. **`coverage-check.sh`** korreliert die Added-Lines aus `git diff --cached -U0` mit den Coverage-Daten → Diff-Coverage.
4. **Coverage-Endstand** einmalig ins Run-Verzeichnis kopieren.
5. **Gate-Entscheidung** (Schwellen unten). Bei Block: Tests ergänzen, ab Schritt 2 wiederholen.

**Maximal 5 Iterationen.** Ist das Gate bei Iteration 5 nicht grün: STOPP, Operator-Eingriff (manueller Test-Reichweiten-Plan oder Story splitten).

### Gate-Schwellen (Diff-Coverage)

| Diff-Coverage | Verhalten |
| -- | -- |
| **≥ 80 %** | **Pass** — weiter zu Schritt 6b. |
| **60–80 %** | **Warn** — Operator entscheidet, Begründung in den Linear-Kommentar. |
| **< 60 %** | **Block** — Tests hinzufügen, Iteration wiederholen. |

Schwellwerte sind Konstanten im Skript (`COVERAGE_PASS=80`, `COVERAGE_WARN=60`) und per env-var überschreibbar: `COVERAGE_PASS=90 bash .claude/hooks/coverage-check.sh`.

### Sonderfälle (Gate übersprungen)

- **Keine Coverage-Daten** (kein `coverage-final.json` / `coverage.json`): Gate übersprungen mit Hinweis *„/bootstrap nachziehen für Test-Setup"*.
- **Diff nur Test-Files / Configs / Docs**: Gate übersprungen.
- **Diff mit 0 Added-Lines**: Gate übersprungen.

---

## Lokaler Testlauf je Stack

Die Kommandos erzeugen in einem Durchgang Coverage **und** die JUnit-XML. `RUN_DIR` ist das Run-Verzeichnis unter `journal/reports/local/<run>/`, `ITER_TESTS` der hochgezählte Iterations-Counter.

### Node (jest + c8)

```bash
npx c8 --reporter=json --reporter=text-summary \
  npx jest --reporters=default --reporters=jest-junit
# JEST_JUNIT_OUTPUT_FILE="${RUN_DIR}/tests-iter${ITER_TESTS}.junit.xml"
# Coverage-Output: coverage/coverage-final.json
cp coverage/coverage-final.json "${RUN_DIR}/coverage-final.json"
```

Die JUnit-XML schreibt `jest-junit` über die env-var `JEST_JUNIT_OUTPUT_FILE`; die Coverage liefert `c8` als `coverage/coverage-final.json`.

### Python (pytest + cov)

```bash
pytest --cov --cov-report=json \
  --junit-xml="${RUN_DIR}/tests-iter${ITER_TESTS}.junit.xml"
# Coverage-Output: coverage.json
cp coverage.json "${RUN_DIR}/coverage-final.json"
```

`pytest` schreibt die JUnit-XML direkt über `--junit-xml=…`, die Coverage als `coverage.json`.

> **JUnit-XML-Konvention:** Sowohl `pytest` als auch `jest-junit` schreiben Standard-JUnit-XML — von `/sprint-review` parsbar. Kann der Test-Runner kein JUnit-XML (z. B. Mocha ohne Reporter), wird die Tests-Persistenz übersprungen: `ITER_TESTS` wird nicht erhöht, `meta.json.iterations.tests` bleibt 0 — der Coverage-Lauf selbst läuft trotzdem weiter.

---

## Wo die Reports landen

Alles unter `journal/reports/local/<run>/`:

| Datei | Inhalt |
| -- | -- |
| `tests-iter{N}.junit.xml` | Test-Ergebnisse pro Iteration (welche Tests, Pass/Fail) |
| `coverage-final.json` | Diff-Coverage des neuen Codes (Endstand) |
| `meta.json` | u. a. `iterations.tests` (Test-Loop-Zähler), `skipped_gates` |

Diese Dateien liegen in **Persistenz-Zone C** (lokal, gitignored) — flüchtiges Arbeitssignal, **kein** Audit-Beleg für sich. Der belastbare Nachweis kommt aus den CI-Artifacts (Zone B) bzw. dem Coverage-Trend im Sprint-Frontmatter (Zone A). Details: [`audit-perspective.md`](audit-perspective.md).

---

## Anti-Platzhalter-Check (BOO-177) — echte Tests statt nur Coverage

Coverage misst, **ob** eine Zeile von einem Test berührt wurde — nicht, **ob der Test etwas prüft**. Triviale Tests heben die Zahl, ohne etwas zu testen:

- leerer Testkörper,
- `expect(true).toBe(true)` / `assert True`,
- `it.skip` / `xit` / `@pytest.mark.skip` **ohne** Begründung.

Der **Anti-Platzhalter-Check** ist deshalb ein **eigener, gezielter Check auf Test-Dateien** (der Hook `anti-placeholder-check.py` — AST für Python, Heuristik für JS/TS; **kein** Linter — Linter prüfen Stil/Typen, nicht Test-Sinnhaftigkeit). Er greift im selben Test-Gate 6a-quart und flaggt genau diese Muster. So ergänzt er die Coverage-Zahl um die fehlende Dimension: Coverage = *„genug Tests"*, Anti-Platzhalter = *„echte Tests"*. Hintergrund: dasselbe Grundproblem wie BOO-176 (*„Agent gamed das Gate"*), hier auf der Test-Ebene. Quelle: [`specs/BOO-177.md`](../../specs/BOO-177.md).

**Was tun, wenn der Check flaggt:** Den geflaggten Test mit echten Assertions füllen (Eingabe → erwartete Ausgabe prüfen). Ist ein Skip **bewusst** gewollt, eine Begründung am Skip ergänzen — dann ist es ein dokumentierter, nachvollziehbarer Skip statt eines stillen Platzhalters.

---

## Fehlerbehebung

| Symptom | Ursache | Behebung |
| -- | -- | -- |
| Gate blockt mit `< 60 %` | Neuer Code ohne Test | Tests für die Added-Lines schreiben, Iteration wiederholen (max. 5). |
| Gate „Warn" (60–80 %) | Teilabdeckung | Entweder Tests ergänzen oder Warn akzeptieren — Begründung in den Linear-Kommentar. |
| `meta.json.iterations.tests` bleibt 0 | Runner ohne JUnit-XML-Reporter (z. B. Mocha) | JUnit-Reporter konfigurieren (Coverage läuft trotzdem). |
| „Gate übersprungen — Test-Setup fehlt" | Kein `coverage-final.json`/`coverage.json` | `/bootstrap` für das Test-Setup nachziehen. |
| Anti-Platzhalter-Check flaggt einen echten Test | Test ohne Assertion / leerer Body | Echte Assertions ergänzen; Skips begründen. |
| 5 Iterationen ohne grün | Reichweite zu groß für eine Story | STOPP → Operator: Test-Reichweiten-Plan oder Story splitten. |

---

## Weiterlesen

| Thema | Quelle |
|---|---|
| Operator-Kurzfassung Unit-Tests | [HANDBUCH Kapitel 8c-bis](../../HANDBUCH.md) |
| Test-Evidenz aus Audit-Sicht (Existenz **und** Qualität) | [`audit-perspective.md`](audit-perspective.md) |
| Reports-Konvention, `meta.json`-Schema, Persistenz-Zonen | [HANDBUCH Anhang E](../../HANDBUCH.md) |
| Vollständiger Gate-Ablauf von `/implement` | [`implement/SKILL.md`](../../implement/SKILL.md) Schritt 6a-quart |
| Begriffe nachschlagen | [`../glossar.md`](../glossar.md) |

---

> *Englische Fassung: [`unit-tests.en.md`](unit-tests.en.md).*
