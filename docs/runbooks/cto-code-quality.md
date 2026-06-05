# Runbook: Codequalität & Tech-Debt — wie ein CTO mit INTENTRON Qualität sichert

> **Für wen.** Sie sind CTO oder Head of Engineering und prüfen, ob Sie dieses Framework einführen.
> Sie wollen in unter zehn Minuten wissen: Wenn mein Team mit KI Code schreibt — wie wird
> Codequalität sichergestellt? Wie verhindere ich, dass dabei still ein Berg Technical Debt
> wächst? Welche Quality Gates greifen, wie läuft eine Story von der Idee bis zum Merge, und wo
> nehme ich als Führungskraft Einfluss?
>
> **Was dieses Runbook ist — und was nicht.** Dies ist die Einstiegs-Lesebrille für die
> Engineering-Sicht. Es führt **keine neue Mechanik** ein — es bündelt, was bereits im Repo lebt:
> die Gates, den Story-Lifecycle, die Artefakte. Wer danach prüfen will, *welche Frage* mit
> *welchem Beleg* an *welchem Ort* beantwortet wird, liest die [Audit-Perspektive](audit-perspective.md).

## In einem Satz

INTENTRON zwingt jede KI-geschriebene Änderung durch eine Kette von Quality Gates — von der Spec
vor dem ersten Commit bis zum Required Status Check in der CI — sodass kein Code ohne dokumentierte
Absicht, ohne Linter-Lauf und ohne synchrone Doku in Ihr `main` gelangt.

## Das Big Picture

![Die vier Quality-Gate-Layer von INTENTRON](../quality-gate-four-layers.png)

Die Gates greifen in vier Schichten, von links nach rechts immer härter. Layer 0 fängt unsichere
Muster ab, **bevor** die KI sie auf die Platte schreibt. Layer 1 gibt Echtzeit-Feedback in der IDE.
Layer 2 blockt lokal beim Commit. Layer 3 ist die letzte, nicht umgehbare Instanz in der CI. Je
weiter rechts, desto verbindlicher — und desto schwerer zu umgehen.

## Ihre drei Kernsorgen

Drei Risiken treiben jede Engineering-Führungskraft um, sobald KI im Spiel ist. Das Framework
adressiert jedes mit einem konkreten Mechanismus.

### 1. „Code entsteht ohne dokumentierte Absicht."

KI liefert schnell etwas, das läuft — aber niemand weiß in sechs Monaten noch, *warum* es so gebaut
wurde. Das ist der Ursprung von Tech-Debt: undokumentierte Entscheidungen, die niemand mehr
hinterfragt.

Das Framework dreht das um: Vor jedem Commit muss eine Spec existieren (`specs/{ISSUE-ID}.md`,
**Spec-Gate**, BOO-23). Die Spec trägt Pflicht-Frontmatter — `story_id`, `change_type`, `estimate`,
`token_estimate`, `execution_mode`, `estimation_basis` — und eine **Definition of Done** als
Pflicht-Sektion. Kein Spec-File, kein Commit. Die Absicht steht fest, bevor die erste Zeile fällt.

### 2. „Niemand garantiert, dass Linter, Security-Scan und Tests gelaufen sind."

Bei manueller Arbeit verließ man sich auf Disziplin. Bei KI-Tempo reicht das nicht. Das Framework
verdrahtet die Prüfungen in vier Layern, sodass eine Umgehung auffällt.

Layer 2 (CLI / Pre-Commit) blockt lokal hart: ESLint, Semgrep (SAST), Dependency-Check, Coverage-Gate.
Wer das lokal mit `git commit --no-verify` umgeht, läuft in Layer 3 (CI / GitHub Actions): Required
Status Checks lassen sich nicht mit `--no-verify` aushebeln. Die harte Instanz sitzt serverseitig,
nicht auf dem Laptop des Entwicklers.

### 3. „Die Doku driftet von der Realität weg."

Veraltete Doku ist Tech-Debt in Textform. Sie kostet jeden neuen Entwickler Stunden und führt zu
falschen Entscheidungen.

**doc-version-sync** ist ein Hard-Gate gegen Versions-Drift: Laufen `CLAUDE.md`,
`ARCHITECTURE_DESIGN.md` und `GOVERNANCE.md` auseinander, blockt das Gate. Der CI-Workflow
`docs-drift.yml` prüft zusätzlich DE/EN-Parität und die Konsistenz zwischen Skill-Definition und
README. Doku, die nicht synchron ist, kommt nicht durch.

## Die Quality Gates — wie es ineinandergreift

Eine Story läuft durch einen festen Lebenszyklus:
`/intent` → `/ideation` → `/backlog` → `/implement` → `/architecture-review` → `/sprint-review` →
`/pitch`. An den qualitätsrelevanten Schritten hängt jeweils ein Gate oder eine Mechanik, die ein
prüfbares Artefakt hinterlässt.

| Lebenszyklus-Schritt | Mechanik / Gate | Artefakt / Beleg |
|---|---|---|
| `/ideation` (Story formen) | Liest die **Learning Loop** und warnt vor bekannten Anti-Patterns aus früheren Sprints | `journal/learnings.md` (L1) → in die Story eingearbeitet |
| Vor jedem Commit | **Spec-Gate** (BOO-23): blockt Commit ohne `specs/{ISSUE-ID}.md`; Pflicht-Frontmatter + Definition of Done | `specs/{ISSUE-ID}.md` |
| Beim Schreiben (KI-Edit) | **Layer 0 — Edit-Bodyguard** (BOO-86): Pre-Write-Check auf Secrets und unsichere Patterns | abgefangener Edit (Warnung, vor dem Schreiben) |
| Beim Tippen (IDE) | **Layer 1 — IDE**: Echtzeit-Feedback | Inline-Markierungen im Editor |
| `git commit` (lokal) | **Layer 2 — CLI / Pre-Commit**: ESLint, Semgrep (SAST), Dependency-Check, Coverage-Gate — **Hard Block** | SARIF / JUnit / Coverage in `journal/reports/` |
| `/implement` (pro Run) | Schreibt **Audit-Trail**-Block (BOO-19): `## Session-Referenz` mit Commit-SHA + Session-ID + Log-Pfad in die Spec | `## Session-Referenz` in `specs/{ID}.md`; `meta.json` je Run |
| Push / Merge | **Layer 3 — CI / GitHub Actions**: Required Status Checks gegen `git commit --no-verify` | grüner CI-Run; Reports in `journal/reports/` |
| Push (Doku) | **doc-version-sync** (Hard-Gate): blockt bei Versions-Drift über `CLAUDE.md` / `ARCHITECTURE_DESIGN.md` / `GOVERNANCE.md`; `docs-drift.yml` prüft DE/EN + Skill↔README | grüner `docs-drift.yml`-Run |
| `/architecture-review` | Prüft die aktiven Quality-Dimensionen (`ARCHITECTURE_DESIGN.md` §5) und Tech-Debt-Risiken | Review-Notizen gegen die aktiven Dimensionen |
| `/sprint-review` | Governance-Drift-Check (lebt das Projekt seinen `governance_mode`?), Anti-Pattern-Selbstdiagnose, Lessons L1/L2/L3 | Sprint-Report; Learning-Eintrag |

### Wie der Audit-Trail die Lücke schließt

Der wichtigste Baustein gegen „undokumentierten KI-Code" ist der Audit-Trail (BOO-19). Jeder
`/implement`-Run schreibt einen `## Session-Referenz`-Block in die Spec — Commit-SHA, Session-ID,
Log-Pfad. Damit lässt sich später jeder Commit zurückverfolgen: vom Commit zur Spec zum Intent zur
KI-Session. Das Script `audit-trace.sh` rekonstruiert diese Kette. Sie sehen nicht nur *was* geändert
wurde, sondern *aus welcher Absicht heraus*.

### Wie die Learning Loop Tech-Debt-Wiederholung verhindert

Ein Anti-Pattern, das einmal Schmerzen verursacht hat, soll nicht zweimal entstehen. Die Learning
Loop hält das fest und spielt es zurück:

| Level | Speicher | Wann |
|---|---|---|
| **L1** | `journal/learnings.md` (Default) | nach jedem Sprint-Review angehängt |
| **L2** | `journal/learnings/` (quartalsweise) | strukturiertere Konsolidierung |
| **L3** | SQLite | ab vielen Sprints, für Cross-Sprint-Trends |

`/ideation` liest die Learnings beim Formen einer neuen Story und warnt, wenn ein bekanntes
Anti-Pattern droht. So fließt gestern Gelerntes in die heutige Story-Definition ein.

### `governance_mode` — die Gate-Strenge skaliert mit dem Risiko

Nicht jedes Projekt braucht die volle Härte. `governance_mode` in der `CONVENTIONS.md` skaliert die
Gates entlang des Risikos.

| Modus | Ergänzt gegenüber dem Vorgänger |
|---|---|
| `lite` | leichtester Modus |
| `standard` | Security-Gates, CI-Lint/SAST, Sensitive-Paths, Learning Loop L1 |
| `heavy` | Coverage-/Performance-Gates, SonarQube, Branch-Protection, Audit-Trail, Mandatory Review, Learning Loop L2/L3 |

Ein Wegwerf-Skript läuft `lite`. Ein regulierter Produktiv-Service läuft `heavy`. Sie wählen die
Schärfe pro Projekt — die Mechanik bleibt dieselbe.

## Artefakte & Skills

Jedes Gate hinterlässt einen prüfbaren Beleg. Das sind die Artefakte, die Codequalität dokumentieren:

| Artefakt | Was es belegt |
|---|---|
| `specs/{ID}.md` | Dokumentierte Absicht je Story + Definition of Done + Audit-Trail-Block |
| `ARCHITECTURE_DESIGN.md` | Zentraler Hub: aktive Quality-Dimensionen (§5), Architektur-Entscheidungen |
| [`CONVENTIONS.md`](../../CONVENTIONS.md) | Gate-Architektur, `governance_mode`, `execution_isolation`, aktive Gates |
| `GOVERNANCE.md` | Governance-Regelwerk des Projekts |
| `journal/reports/` | SARIF (Linter/SAST), JUnit (Tests), Coverage je Run |
| `meta.json` | Run-Metadaten je `/implement`-Lauf |
| `DEVELOPER_ONBOARDING.md` | Übergabe-Wissen für autonome Teams und Tool-Wechsel |

> Die als Code gesetzten Artefakte (`specs/`, `ARCHITECTURE_DESIGN.md`, `GOVERNANCE.md`, `DEVELOPER_ONBOARDING.md` …) entstehen **in Ihrem Projekt** beim Bootstrap — sie liegen nicht im Framework-Repo. Die Vorlagen dazu finden Sie unter `bootstrap/references/`.

Die qualitätsrelevanten Lifecycle-Schritte sind als Skills umgesetzt: `/ideation`, `/implement`,
`/architecture-review`, `/sprint-review`. Die Gate-Architektur (4 Layer, Spec-Gate,
`governance_mode`) ist in der [`CONVENTIONS.md`](../../CONVENTIONS.md) verankert.

## Wo Sie Einfluss nehmen

Das Framework ist nicht starr. Diese Stellschrauben legen Sie als CTO fest — pro Projekt, passend
zum Risiko:

| Stellschraube | Was Sie damit steuern |
|---|---|
| **`governance_mode`** (`lite` / `standard` / `heavy`) | die Grund-Strenge aller Gates auf einen Schlag |
| **Coverage-Schwellen** | wie streng das Coverage-Gate blockt |
| **Aktive Quality-Dimensionen** (`ARCHITECTURE_DESIGN.md` §5) | welche Qualitätsattribute `/architecture-review` und `/sprint-review` prüfen |
| **Learning-Loop-Level** (L1 / L2 / L3) | wie tief das Framework aus vergangenen Sprints lernt |
| **`execution_isolation`** | wie KI-Worker beim parallelen Arbeiten gegeneinander isoliert sind |

Faustregel: Je höher das Risiko des Projekts, desto höher `governance_mode`, desto strenger die
Coverage-Schwelle, desto mehr aktive Quality-Dimensionen.

## Grenzen — was das Framework NICHT tut

Eine ehrliche Erwartungshaltung schützt vor Enttäuschung. Drei Dinge leistet das Framework bewusst
nicht.

- **Gates erzwingen die *Existenz* von Belegen, nicht deren *inhaltliche Qualität*.** Das Spec-Gate
  prüft, dass eine Spec da ist — nicht, ob sie gut geschrieben ist. Das Coverage-Gate prüft, dass
  der Linter lief — nicht, ob die Tests sinnvoll sind. doc-version-sync prüft, dass die Doku
  synchron ist — nicht, ob sie verständlich ist. Den inhaltlichen Anspruch setzen weiterhin
  Menschen.
- **Keine Geschwindigkeits- oder Velocity-Metriken.** Das ist Absicht, nicht Lücke. Die
  Code-Crash-Haltung nach Schrader: Velocity als Steuerungsgröße ist überholt. Das Framework misst
  Belege und Qualität, nicht Story Points pro Sprint.
- **Vier-Augen ist Konvention, nicht erzwungen** (BOO-72). Das Framework dokumentiert das
  Vier-Augen-Prinzip als Operator-Disziplin, erzwingt es aber heute nicht maschinell. Wer es
  verbindlich braucht, prüft manuell oder über Branch-Protection im `heavy`-Modus.

## Weiterlesen

- [`CONVENTIONS.md`](../../CONVENTIONS.md) — die Gate-Architektur (4 Layer, Spec-Gate),
  `governance_mode`, `execution_isolation`, aktive Gates im Detail.
- [`HANDBUCH.md`](../../HANDBUCH.md) — das vollständige Setup- und Betriebshandbuch.
- [`ARCHITECTURE_DESIGN`-Vorlage](../../bootstrap/references/architecture-design-template.md) — die
  Template-Basis des Architektur-Hubs (im Projekt entsteht daraus `ARCHITECTURE_DESIGN.md` mit den
  aktiven Quality-Dimensionen §5).
- [`audit-perspective.md`](audit-perspective.md) — wie ein Auditor die Belege prüft
  (Frage → Beleg → Ort).
- [`../quality-gate-four-layers.excalidraw`](../quality-gate-four-layers.excalidraw) — die Quelle
  zum Big-Picture-Diagramm.
- [`../how-we-document.md`](../how-we-document.md) — wie die Doku-Schichten zusammenhängen.
- [`../glossar.md`](../glossar.md) — die Begriffe (Spec, Quality-Gate, `governance_mode` …).
