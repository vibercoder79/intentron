# Runbook: Audit-Perspektive — CISO/CIO/CTO verifiziert die Regel-Einhaltung

> **Zweck.** Dieses Runbook beschreibt, wie ein Auditor (CISO/CIO/CTO oder ein externer Prüfer)
> aus reiner **Audit-Perspektive** verifiziert, dass das Dev-Team die Framework-Regeln eingehalten
> hat: Haben die Linter gegriffen? Sind die GitHub Actions gelaufen und grün? Liegen Reports und
> Belege vor? Existiert ein lückenloser Audit-Trail vom Commit zurück zum Intent und zur Session?
>
> Das ist **keine neue Mechanik** — alle Belege existieren bereits im Repo. Dieses Runbook ist
> reiner **Aggregator**: Es bündelt die vorhandenen Gates, Hooks, Workflows und Reports zu einer
> prüfbaren Liste. Wer auditiert, soll hier nachschlagen können, *welche Frage* mit *welchem Beleg*
> an *welchem Ort* beantwortet wird — ohne erst das ganze HANDBUCH zu lesen.

## Auditor-Perspektive (leichtgewichtig)

Ein Auditor will nicht den Code lesen. Er will **Belege**: reproduzierbare Artefakte, die zeigen,
dass der Prozess gelaufen ist. Das Framework ist so gebaut, dass jede Governance-Regel ein
sichtbares Artefakt hinterlässt — eine Spec, einen Hook-Block, einen CI-Run, einen Report. Der
Auditor prüft die Existenz und den Status dieser Artefakte, nicht die Implementierung dahinter.

Drei Grundsätze gelten für jede Prüfung:

1. **Beleg vor Behauptung.** „Der Linter ist gelaufen" zählt nicht — der SARIF-Report im
   CI-Artifact zählt.
2. **CI ist die maßgebliche Quelle.** Lokale Reports unter `journal/reports/` sind gitignored und
   damit flüchtig. Was persistent nachweisbar sein muss, lebt im CI-Artifact (Retention 30 Tage)
   oder in committeten Artefakten (Specs, DPO-Reports).
3. **Konvention ≠ Enforcement.** Einige Schutzmaßnahmen (Vier-Augen-Prinzip) sind dokumentierte
   Operator-Disziplin, kein erzwungener Mechanismus. Der Auditor muss wissen, was *erzwungen* und
   was *vereinbart* ist (siehe Caveats).

## Audit-Frage → Beleg → Ort

| Audit-Frage | Beleg/Mechanik | Artefakt/Ort |
|---|---|---|
| Hatte jeder Change einen dokumentierten Intent? | `spec-gate.sh` blockiert Commit ohne Spec | `specs/{ISSUE-ID}.md`; `verify-setup` Check 3 |
| Jeder Commit auf Prompt/Session rückführbar? | `## Session-Referenz`-Block + `audit-trace.sh` | `specs/*.md`; `bootstrap/scripts/audit-trace.sh`; CONVENTIONS §Audit-Trail (BOO-19) |
| Haben Linter/SAST/Coverage lokal gegriffen? | `/implement` legt SARIF/JUnit/Coverage je Iteration ab | `journal/reports/local/{date}_{story}/` + `meta.json` (Anhang E). Caveat: `journal/reports/` ist gitignored → CI-Artifacts sind die persistente Quelle |
| GitHub Actions gelaufen/grün? | CI-Workflows + Aggregator lädt Reports als Artifact (Retention 30 T.) | `journal/reports/ci/run-{id}/`; Workflows `docs-drift.yml` / `hook-sources.yml` / `ruff-hooks.yml` |
| Merge ohne grüne Gates möglich? (Bypass) | Branch-Protection Required Status Checks; CI als Layer 3 gegen `--no-verify` | `bootstrap/scripts/setup-branch-protection.sh` (BOO-29) |
| Datenschutz/Compliance nachgewiesen? | `dpo-audit.py` → PASS/GAP/REVIEW-NEEDED; Sprint-Review 7c | `dpo/reports/<date>_audit.{md,json}`; Kataloge `dpo/controls/*.yml` |
| Setup selbst verifiziert (Hooks/Tools)? | `verify-setup.sh` read-only PASS/WARN/FAIL | `bootstrap/references/verify-setup.sh` (Anhang T) |
| Findings in Backlog überführt? | Sprint-Review legt pro GAP eine Story an (Label `privacy`) | `sprint-review/SKILL.md` Schritt 7/7c |
| Modell-Overrides nachvollziehbar? | `override_audit[]` in `meta.json` | `meta.json.override_audit` |
| Vier-Augen bei sensiblen Pfaden? | Konvention (NICHT erzwungen) — `git log` / `git blame`, Author Gate ≠ Author Change | HANDBUCH Anhang R §Vier-Augen |
| Lebt das Projekt seinen `governance_mode`? | Sprint-Review Schritt 1 „Governance Drift" | `sprint-review/SKILL.md`; CONVENTIONS Governance-Matrix |

## So prüfst du konkret

Die folgenden Schritte lassen sich von oben nach unten als Audit-Durchlauf abarbeiten. Alle
Kommandos sind read-only — sie ändern nichts am Repo.

### 1. Intent-Lückenlosigkeit: hat jeder Issue eine Spec?

Jeder Commit mit Issue-Referenz braucht eine Spec — erzwungen durch `hooks/spec-gate.sh`. Prüfe,
dass zu jedem im Backlog/Branch erwähnten Issue ein Spec-File existiert:

```bash
ls specs/                       # alle vorhandenen Specs
git log --oneline | head -30    # Commits mit Issue-Präfix (z.B. "BOO-42: ...")
```

Fehlt zu einem referenzierten Issue die `specs/{ISSUE-ID}.md`, hätte der Commit gar nicht
durchlaufen dürfen — oder das Gate wurde umgangen (siehe Schritt 5).

### 2. Audit-Trail rekonstruieren: Commit → Intent → Session

Für jede Spec rekonstruiert `audit-trace.sh` den Pfad vom Commit zurück zum Konversations-Log:

```bash
bash bootstrap/scripts/audit-trace.sh BOO-42
```

Das Script liest den `## Session-Referenz`-Block aus `specs/BOO-42.md` (Commit-SHA + Session-ID +
Log-Pfad), zeigt den Git-Commit-Diff und rendert die Session-Turns. Fehlende Felder werden explizit
als `unbekannt` ausgewiesen — das ist selbst ein Audit-Signal.

### 3. Lokale Gate-Belege sichten (mit Vorbehalt)

`/implement` legt pro Iteration SARIF (Linter/SAST), JUnit (Tests) und Coverage ab:

```bash
ls journal/reports/local/        # falls vorhanden — gitignored, also nur auf der Operator-Maschine
cat journal/reports/local/*/meta.json   # Iterations-Metadaten je Story
```

Wichtig: `journal/reports/local/` ist gitignored und damit nicht der maßgebliche Audit-Beleg.
Für den persistenten Nachweis gehe direkt zu den CI-Artifacts (Schritt 4).

### 4. CI-Status und CI-Artifacts prüfen

Die GitHub Actions sind die maßgebliche, persistente Quelle. Prüfe Lauf und Status:

```bash
gh run list --limit 20
gh run view <run-id>
gh run download <run-id> --name ci-reports-<run-id>   # SARIF/JUnit/Coverage als Artifact (Retention 30 Tage)
```

Die Workflows `docs-drift.yml`, `hook-sources.yml` und `ruff-hooks.yml` liegen unter
`.github/workflows/`. Jeder Tool-Workflow endet mit Collect-into-`run-{id}/` + Upload-Artifact.

### 5. Bypass-Prüfung: konnte jemand an den Gates vorbei mergen?

Lokale Hooks lassen sich mit `git commit --no-verify` umgehen. Die Abwehr dagegen ist
Branch-Protection mit Required Status Checks (CI als Layer 3). Prüfe die aktive Konfiguration:

```bash
gh api repos/{owner}/{repo}/branches/main/protection
```

Erwartet werden `required_status_checks` (die CI-Checks) und `required_pull_request_reviews`.
Gesetzt wird das durch `bootstrap/scripts/setup-branch-protection.sh` (BOO-29). Fehlt der Schutz,
ist ein lokaler `--no-verify`-Bypass nicht durch CI abgefangen.

### 6. Datenschutz-Compliance nachweisen

Der DPO-Audit-Runner produziert ein reproduzierbares, committetes Report-Paar:

```bash
ls dpo/reports/                              # <date>_audit.md + <date>_audit.json
cat dpo/reports/<date>_audit.md              # PASS / GAP / REVIEW-NEEDED je Control
ls dpo/controls/                             # versionierte Kataloge: gdpr.yml, ndsg.yml
```

`dpo/scripts/dpo-audit.py` arbeitet den Katalog deterministisch ab: mechanische Checks ergeben
PASS/GAP, Urteils-Checks ergeben REVIEW-NEEDED. Der Auditor prüft die GAP-Liste und ob die
REVIEW-NEEDED-Punkte vom Operator bestätigt wurden.

### 7. Findings-Verfolgung und Governance-Drift

Sprint-Review schließt den Loop: pro offenem GAP eine Backlog-Story (Label `privacy`,
`sprint-review/SKILL.md` Schritt 7c), und Schritt 1/1b prüft, ob das Projekt seinen deklarierten
`governance_mode` (CONVENTIONS Governance-Matrix) tatsächlich lebt — Abweichungen werden als
`Governance Drift` im Sprint-Report dokumentiert.

```bash
verify-setup.sh   # read-only PASS/WARN/FAIL über Hooks, Toolchain, Kern-Artefakte (Anhang T)
git blame -- path/to/sensitive/file   # Vier-Augen-Indiz: Author des review-ok-Gates ≠ Author der Änderung
```

## Caveats

- **`journal/reports/` ist gitignored — CI-Artifacts sind maßgeblich.** Lokale Reports unter
  `journal/reports/local/` sind kurzlebiges Signal und liegen nur auf der Operator-Maschine. Für
  einen belastbaren Audit-Nachweis gelten die CI-Artifacts unter `journal/reports/ci/run-{id}/`
  (GitHub-Actions-Artifact, **Retention 30 Tage** — danach nicht mehr abrufbar, rechtzeitig
  herunterladen/archivieren).
- **Session-Log-Retention.** `audit-trace.sh` rekonstruiert das Konversations-Log nur, solange das
  Session-Log existiert. Empfehlung im Script: Session-Logs 90 Tage aufbewahren, dann archivieren
  oder löschen. Ältere Logs lassen sich nicht mehr rendern; Commit-SHA und Spec bleiben erhalten,
  der Prompt-Verlauf nicht.
- **Vier-Augen ist Konvention, nicht erzwungen.** Das Framework erzwingt das Vier-Augen-Prinzip für
  Sensitive- und Personal-Data-Paths heute **nicht** (BOO-72 schließt Enforcement explizit aus). Es
  ist dokumentierte Operator-Disziplin (HANDBUCH Anhang R §Vier-Augen). Der Auditor prüft es
  manuell über `git log` / `git blame` — Indiz ist: Author des `review-ok`/`privacy-ok`-Gates ≠
  Author der eigentlichen Änderung.
