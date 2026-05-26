---
name: implement
recommended_model: sonnet  # BOO-84 — tier mapping in bootstrap/references/model-tiers.json
description: |
  Implementierungs-Protokoll fuer CLAW User Stories. 8-Schritte-Workflow von Issue-Identifikation
  bis Ergebnis-Tabelle inkl. Post-Implement Validation. Verwenden wenn der Operator "los" sagt,
  eine Story umsetzen will, oder "/implement" ausfuehrt. Wird auch vom Automation Daemon genutzt
  (ohne Human-in-the-Loop).
version: 2.10.0
metadata:
  hermes:
    category: coding
    tags: [code-generation, deklarativer-modus, quality-gates, token-pre-flight, codex-adapter]
    requires_toolsets: [terminal, git, eslint, semgrep]
    related_skills: [ideation, sprint-review]
---

# Implement

User Story aus dem Linear-Backlog systematisch umsetzen. 8 Schritte + Governance-Validation, keiner darf uebersprungen werden.

## Workflow (9 Schritte)

### Schritt 0: Environment laden

1. Lese `.claude/environment.json` (falls vorhanden — sonst Defaults verwenden + Warnung loggen).
2. Lese `CONVENTIONS.md` (falls vorhanden) als projektlokalen Vertrag fuer `governance_mode` und `execution_isolation`. Fallback: `governance_mode=standard`, `execution_isolation=write-scope`.
3. Bei Bedarf Pfade extrahieren aus `paths.*` (z.B. `paths.reports_local`, `paths.lessons_l3`, `paths.specs`, `paths.architecture_design`, `paths.conventions`).
4. Bei Tool-Aufruf pruefen: ist Tool in `tools_available.<tool>` aktiv (z.B. `tools_available.eslint`, `tools_available.semgrep`, `tools_available.tests`)? Bei `false` oder fehlendem Eintrag: Skill ueberspringt den Aufruf und gibt einen Hinweis im Output.
5. Lese `SECURITY.md` falls vorhanden. Bei fehlender Datei Warnung ausgeben und fuer jede Security-relevante Aenderung ein TODO in der Ergebnis-Tabelle notieren.
6. Lese `DEVELOPER_ONBOARDING.md` falls vorhanden. Bei fehlender Datei Warnung ausgeben: "Hinweis: Developer Onboarding fehlt — Projekt ist schwerer an fremde Teams oder andere Tools uebergabefaehig."
7. Fallback bei fehlender Datei: Standard-Pfade aus dem Schema annehmen (`journal/`, `journal/reports/local/`, `specs/`, `ARCHITECTURE_DESIGN.md`, `CONVENTIONS.md`, `SECURITY.md`, `DEVELOPER_ONBOARDING.md`) und im Output vermerken: "Hinweis: `.claude/environment.json` fehlt — Defaults aktiv. Empfehlung: `/bootstrap` re-rennen oder die Datei manuell anlegen."

### Schritt 0b: Token-Window-Pre-Flight (BOO-40, weich)

Vor jeder Story pruefen, ob die geschaetzte Story-Last die Sprint-Box-Grenze knackt. **Soft-Trigger** — der Operator kann immer weitermachen, der Skill warnt nur. Konvention: HANDBUCH Anhang G (BOO-38).

**Logik:**

1. **Aktuelles Context-Window messen:**
   - Bevorzugt via `/context`-Befehl ODER `claude-code measure-context` (falls verfuegbar)
   - Fallback: Schaetzung aus Chat-Laenge (sehr ungenau — Hinweis im Output)

2. **Story-Token-Schaetzung aus Spec-Frontmatter `token_estimate` lesen** (gesetzt von `/ideation` Schritt 5b — BOO-39).
   - Fallback: aus `estimate` (SP) ableiten gemaess HANDBUCH Anhang G:
     - 1 SP → 5%, 2 → 12%, 3 → 25%, 5 → 50%, 8 → "Story zu gross, splitten"

3. **Projektion berechnen:**
   ```
   projektion_prozent = aktuell_prozent + story_geschaetzt_prozent
   ```

4. **Schwellen aus `.claude/environment.json` lesen** (BOO-38 hat sie als Pflicht-Feld etabliert):
   - `thresholds.token_warn_threshold` (Default 70)
   - `thresholds.token_hard_threshold` (Default 80)

5. **Wenn `projektion > token_hard_threshold`:**

   ```
   [!warning] Token-Pre-Flight:
   - Aktuell: 65% (130k / 200k)
   - Story-Schaetzung: 25% (50k)
   - Projektion: 90% — ueber Sprint-Box-Grenze (80%)

   Empfehlung: Sprint hier abschliessen.
   Naechste Schritte:
   1. /sprint-review starten (aktuellen Sprint-Stand persistieren)
   2. Diesen Chat schliessen
   3. Neuen Chat oeffnen, Story dort starten

   Trotzdem fortfahren? [ja/nein]
   ```

6. **Bei `nein`:** Skill stoppt, gibt /sprint-review-Hinweis und Sprint-Wechsel-Anleitung aus:

   ```
   1. /sprint-review starten (Sprint-File schreiben, L3 aktualisieren)
   2. Letzte Lesson committen
   3. Diesen Chat schliessen
   4. Neuen Chat oeffnen mit:
      "Setze Sprint X fort, naechste Story: BOO-YY"
      /implement BOO-YY
   ```

7. **Bei `ja`:** Risiko-Vermerk in `journal/reports/local/{date}_{story}/meta.json` schreiben (Feld wird in Schritt 6f-bis ergaenzt):

   ```json
   "pre_flight_warning": "projection 90%, user proceeded"
   ```

   ... weiter zu Schritt 1.

8. **Bei `projektion > token_warn_threshold` aber `<= token_hard_threshold`:** weicher Hinweis ohne Block:

   ```
   [!info] Token-Pre-Flight:
   - Projektion: 78% (knapp unter Sprint-Box-Grenze 80%)
   - Hinweis: noch eine kleine Story passt rein, danach Sprint-Ende empfohlen
   ```

   Weiter zu Schritt 1.

**Begruendung Soft-Trigger:** manche Stories sind kleiner als geschaetzt; manche Sprint-Wechsel sind teurer als ein Compact. Operator behaelt Kontrolle. Wenn `pre_flight_warning` in `meta.json` ist und die Session tatsaechlich gecompacted hat → Lesson fuer L3 ("Schaetzung war zu konservativ" oder "User-Entscheid war richtig") → Kalibrierung fuer `/ideation` Token-Heuristik (BOO-39).

### Schritt 0c: Execution-Isolation-Pre-Flight (BOO-52, hart bei Parallelitaet)

Vor jeder Story pruefen, ob der Ausfuehrungsmodus zur projektlokalen `CONVENTIONS.md` passt.

**Ablauf:**

1. `CONVENTIONS.md` lesen und `execution_isolation` ermitteln:
   - `none`
   - `write-scope`
   - `git-worktree`
2. Spec-Frontmatter lesen:
   - `execution_mode`
   - `worktree_strategy`
   - `write_scopes`
   - `codex_execution_hint` (optional, nur beratend)
3. Regeln anwenden:

| `execution_mode` | Pflicht |
|---|---|
| `linear` | keine Worktree-Pflicht |
| `sub-agents` | `execution_isolation` muss `write-scope` oder `git-worktree` sein; `write_scopes` muessen konkret befuellt sein |
| `agentic` | `execution_isolation` und `worktree_strategy` muessen `git-worktree` sein |

**Codex-Adapter-Regel:** Codex darf auch bei `linear` intern planen, Tasks bilden und Sandbox-Schritte ausfuehren. Das ist kein Regelbruch, solange nur eine sequenzielle Schreibspur entsteht. `codex_execution_hint` darf die Ausfuehrung empfehlen (`single-agent`, `parallel-workers`, `worktree-required`), aber niemals `execution_mode`, `execution_isolation`, `write_scopes` oder Gates ueberschreiben.

4. Bei Regelbruch STOPP:

```
[STOP — EXECUTION ISOLATION]
Story BOO-XX ist als sub-agents/agentic markiert, aber die Isolation ist unvollstaendig.

Gefunden:
  execution_mode: sub-agents
  worktree_strategy: none
  write_scopes: leer

Naechste Schritte:
  a) Spec auf linear herunterstufen
  b) CONVENTIONS.md auf write-scope/git-worktree anheben
  c) write_scopes und Integrationsregel in specs/BOO-XX.md ergaenzen
```

5. Bei `git-worktree`: nicht automatisch Worktrees anlegen, solange kein Adapter/Skript vorhanden ist. Stattdessen den Operator-/Adapter-Plan ausgeben:

```
Empfohlener Worktree-Plan:
  git worktree add ../{repo}-{story}-{role} -b {story}-{role}
```

6. Subagents duerfen nur mit disjunktem Write-Scope gestartet werden. Mini-Briefings muessen enthalten: Rolle, Aufgabe, erlaubte Pfade, verbotene Pfade, Integrationsregel.

### Schritt 1: Issue identifizieren

- `linear.getOpenIssues()` — gesamtes Backlog laden
- Issue mit Status "In Progress" identifizieren (das ist der Auftrag)
- Falls mehrere "In Progress": aeltestes zuerst, Operator fragen bei Unklarheit
- Issue-Description vollstaendig lesen

### Schritt 1b: Schrader-Bestandteile-Gate ⛔ HARD GATE — kein Implement ohne vollstaendigen Prompt

Prueft ob das Issue ein vollstaendiger Schrader-Prompt ist (Code Crash Kap. 5). Kein Soft-Warning — harter Block.

**Ablauf:**

1. Issue-Description auf Sektion `## Schrader-Prompt-Bestandteile` pruefen (alternativ: `## Schrader Prompt Components` fuer EN-Issues)
2. Alle 4 Sub-Sections pruefen — muss mind. 20 Zeichen nicht-leeren Inhalt enthalten (kein Template-Placeholder):
   - `### Insight (Perceive)`
   - `### Constraints`
   - `### Erfolgskriterien` (oder `### Success Criteria`)
   - `### Gewuenschtes Ergebnis` (oder `### Desired Outcome`)
3. Optional: `## Definition of Done` Sektion pruefen — Existenz pruefen (Inhalt nicht tief validiert)

**Bei fehlendem Bestandteil — STOPP:**
```
[STOP] Issue BOO-XX ist kein vollstaendiger Prompt — Schrader-Bestandteil fehlt:
  - [x] Insight: vorhanden
  - [ ] Constraints: leer oder fehlt
  - [x] Erfolgskriterien: vorhanden
  - [x] Gewuenschtes Ergebnis: vorhanden

Geh zurueck zu /ideation und ergaenze den fehlenden Bestandteil bevor du /implement startest.
```

**Bei vollstaendigem Issue:** Weiter zu Schritt 2.

> Pruefung regelbasiert (kein LLM noetig). Issues vor Code Crash Governance v2 (ohne `## Schrader-Prompt-Bestandteile`) koennen den Gate-Check nicht passieren — Operator muss die Sektion nachtraeglich ergaenzen (Migrations-Schritt in `migration-checklist-v1-to-v2.md`).

### Schritt 2: Abhaengigkeits-Check

- `## Abhaengigkeiten` Sektion im Issue pruefen
- Parent-Issue und Siblings pruefen (EPIC-Kontext)
- Gesamtes Backlog auf Referenzen zum Issue durchsuchen (CLAW-XX Mentions)
- **Falls Abhaengigkeit OFFEN:** Operator warnen — "CLAW-XX haengt von CLAW-YY ab (Status: Backlog). Trotzdem fortfahren?"
- **Falls Reihenfolge abweicht:** Impact-Analyse zeigen

### Schritt 3: Kontext aufbauen

- CLAUDE.md lesen (Systemkontext)
- **`DEVELOPER_ONBOARDING.md` lesen** falls vorhanden — Handoff-Kontext fuer fremde Entwicklungsteams und Toolwechsel (Claude Code -> Codex/Cursor/GitHub Copilot/Google Antigravity/klassisches Dev-Team). Runtime-Hinweise, SSoTs, Startpunkt Umsetzung und Pflegepflicht in die Plan-Erstellung einbeziehen.
- **`ARCHITECTURE_DESIGN.md` lesen** — Lead-Dokument: ADRs, Quality Attributes, Leitprinzipien. Pruefen ob die Story gegen bestehende ADRs oder Quality Attributes verstoesst (z.B. ADR-6: Zero External Dependencies, ADR-5: Kill-Switch First). Verweist auf alle weiteren Architektur-Dokumente.
- Betroffene Code-Dateien identifizieren (aus Issue-Description + eigene Analyse)
- Verwandte abgeschlossene Issues pruefen (was wurde schon gebaut?)
- Architektur-Dimensionen pruefen die fuer diese Story relevant sind:
  Siehe [references/architecture-checklist.md](references/architecture-checklist.md)
- **Domain-Context (wenn vorhanden):** Falls `docs/domain/` im Projekt existiert, relevante `docs/domain/*.md`-Dateien laden (Schluessel-Begriffe die in der Story-Description oder den ACs vorkommen). Bei Sub-Agent-Delegation den Domain-Context als Teil des Mini-Briefings mitgeben: "Relevante Domain-Begriffe fuer diese Story: [Begriff → Pfad zur domain/*.md]"

### Schritt 3b: Governance-Validation (PFLICHT)

Vor der Plan-Erstellung die Governance-Artefakte aus dem Issue validieren.
Siehe [references/governance-validation.md](references/governance-validation.md)

1. **8-Dimensionen pruefen:** Ist die Tabelle im Issue vorhanden? Stimmt die Einschaetzung?
   Fehlt eine Dimension die durch die geplante Aenderung betroffen ist?
2. **Security-Checklist:** Security-by-Design Sektion im Issue lesen.
   SECURITY.md Checkliste fuer den Change-Type durchgehen (neue API? Webhook? externer Input?).
3. **Security Impact + Security Validation pruefen:** Jede Story muss eine Sektion `## Security Impact` enthalten. Bei Code-, Security-, Tooling-, Dependency-, CI- oder Governance-Aenderungen muss zusaetzlich `## Security Validation` befuellt sein. Fehlt eine der Sektionen, STOPP mit Hinweis auf `/ideation` oder manuelle Nachpflege.
4. **Security-Referenzstack laden:** Je nach Change-Type die passenden Referenzen laden:
   - `auth` / `api`: `SECURITY.md`, API-Inventar, sensitive-paths, OWASP/API-Checkliste falls im Projekt vorhanden
   - `data`: `SECURITY.md`, Datenfluss-/Privacy-Sektion, Schema-/Storage-Doku
   - `dependency`: `SECURITY.md`, Dependency-/Supply-Chain-Regeln, `.semgrep.yml`, Manifest-Diff
   - `ci` / `governance`: `SECURITY.md`, Hook-/CI-Regeln, `CONVENTIONS.md`
   - `none`: Begruendung aus der Story uebernehmen und nur Basis-Secret-/Logging-Check durchfuehren
5. **ADD validieren (bei Features):** Architecture Design Document gegen aktuellen Code pruefen.
   Stimmen die genannten Dateien noch? Sind die Integrationspunkte korrekt?
6. **Fehlende Artefakte:** Falls 8-Dimensionen, Security-Sektion, Security-Validation oder ACs im Issue fehlen:
   - **Operator warnen:** "Issue CLAW-XX fehlt [Sektion]. Soll ich die Sektion nachtraeglich ergaenzen?"
   - **NICHT stillschweigend weitermachen** — Governance-Luecken muessen sichtbar sein

### Schritt 3c: Spec-File Gate ⛔ HARD GATE — kein Plan ohne Spec

> **Diese Sperre wird zusaetzlich durch `.claude/hooks/spec-gate.sh` maschinell erzwungen.**
> Der Hook blockiert jeden `git commit CLAW-XXX` wenn `specs/CLAW-XXX.md` fehlt.

**Ablauf:**

1. Pruefen: Existiert `specs/CLAW-XXX.md`?

2. **Falls JA:** Spec lesen — stimmt der Inhalt mit dem aktuellen Issue ueberein?
   Falls veraltet: Spec aktualisieren, dann weiter zu Schritt 4.

3. **Falls NEIN → STOPP. Spec jetzt erstellen:**
   a. `specs/TEMPLATE.md` lesen
   b. `specs/CLAW-XXX.md` vollstaendig befuellen:
      - Why (aus Issue uebernehmen)
      - What (Deliverable + Done-Kriterien)
      - Constraints (Must / Must Not / Out of Scope)
      - Current State (betroffene Dateien + bestehende Patterns)
      - Tasks (T1, T2... — max 3 Files/Task, konkreter Verify-Step)
   c. Spec in Git committen: `git commit -m "docs: specs/CLAW-XXX.md erstellt"`
   d. **Operator explizit bestaetigen lassen:**
      Ausgabe: `"Spec-File erstellt: specs/CLAW-XXX.md — bitte prüfen und bestätigen, dann geht es weiter."`
   e. **Warten auf Operator-OK** — erst danach weiter zu Schritt 4
   f. Backlog-Record-/Adapter-Kommentar: Link zum Spec-File

4. **Keine Ausnahmen** — auch bei kleinen Fixes, Hotfixes, Config-Aenderungen.
   Einzige Ausnahme: reine Doku-Commits ohne Code-Aenderungen.

### Schritt 4: Plan erstellen + Operator-Freigabe

- Konkreten Implementierungsplan praesentieren
- Dateien, Aenderungen, Risiken, Test-Strategie
- **Warten auf Operator-Freigabe** (Human-in-the-Loop)
- Bei Daemon-Ausfuehrung (Auto-Execute): diesen Schritt ueberspringen

### Schritt 5: Implementation (nach Freigabe)

- Sub-Tasks: Vor Implementation → "In Progress", nach Abschluss → "Done"
- Plan vollstaendig umsetzen
- Alle neuen Funktionen, Methoden und Code-Pfade mit Kommentar `// AI-generated: {STORY_ID}` markieren (Rollback-Identifikation, BOO-17). Fuer Python: `# AI-generated: {STORY_ID}`.
- Alle Doku-Files aktualisieren (CLAUDE.md, SYSTEM_ARCHITECTURE.md, etc.)
- Git Commit + Push
- **Session-Referenz ins Spec-File schreiben (BOO-19):**
  ```bash
  # Commit-SHA holen
  COMMIT_SHA=$(git rev-parse HEAD)
  # Neueste Session-Datei fuer dieses Projekt (best-effort)
  SESSION_FILE=$(ls -t ~/.claude/projects/*/sessions/*.jsonl 2>/dev/null | head -1)
  SESSION_ID=$(basename "${SESSION_FILE}" .jsonl 2>/dev/null || echo "unbekannt")
  SESSION_TS=$(date -u +%Y-%m-%dT%H:%M:%SZ)
  ```
  In `specs/CLAW-XXX.md` unter `## Session-Referenz` eintragen:
  ```markdown
  ## Session-Referenz

  **Session-Timestamp:** {SESSION_TS}
  **Session-ID:** `{SESSION_ID}` (best-effort — neueste Session beim Commit)
  **Session-Log:** `~/.claude/projects/.../sessions/{SESSION_ID}.jsonl`
  **Commit-SHA:** `{COMMIT_SHA}`
  **Audit-Trace:** `bash .claude/scripts/audit-trace.sh {SPEC_ID}` (braucht jq)
  ```
  Danach Spec-File committen: `git commit -m "docs: specs/CLAW-XXX.md Session-Referenz (BOO-19)"`

  > Wenn SESSION_FILE leer bleibt (keine Session-Datei gefunden): Nur COMMIT_SHA + SESSION_TS eintragen, SESSION_ID als "unbekannt" markieren — kein STOPP.

- Rueckfragen NUR bei echten Blockern

### Schritt 5.5: Sensitive-Paths-Gate ⛔ STOP BEI SENSITIVEM PFAD (BOO-18)

> Dieser Schritt laeuft NUR wenn `.claude/sensitive-paths.json` im Projekt existiert.
> Ohne diese Datei: sofort weiter zu Schritt 6.

**Ablauf:**

1. `.claude/sensitive-paths.json` lesen — `patterns`-Array laden.
2. Geaenderte Dateien ermitteln:
   ```bash
   git diff --name-only HEAD
   ```
3. Jede geaenderte Datei gegen die Pattern-Liste pruefen (Glob-Matching, `**` = rekursiv):
   - `auth/**` trifft auf `auth/token.js`, `auth/middleware/jwt.js`, etc.
   - `**/*pii*` trifft auf `lib/pii-handler.js`, `src/models/pii.js`, etc.
4. **Kein Treffer → Gate bestanden**, weiter zu Schritt 6.
5. **Treffer vorhanden → PFLICHT-STOPP:**

```
[STOP — SENSITIVE PATH] Die folgenden geaenderten Dateien beruehren sensible Bereiche:
  - auth/token.js  (Pattern: auth/**)
  - lib/pii-handler.js  (Pattern: **/*pii*)

Mandatory Human Review erforderlich (BOO-18, Schrader Kap. 3 §Enterprise Governance).

VOLLSTAENDIGER DIFF ZUR REVIEW:
[diff output hier]

Bitte prüfe den Diff Zeile-für-Zeile und bestätige mit:
  review-ok: {dein-name} - {kurzer Kommentar was geprüft wurde}

Ohne explizite Bestätigung wird der Commit nicht durchgeführt.
```

6. **Auf Review-Bestätigung warten** — Operator antwortet mit `review-ok: ...`
7. **Nach Bestätigung:**
   a. Review-Kommentar ins Spec-File eintragen unter `## Human Review`:
      ```markdown
      ## Human Review
      - **Date:** {{TODAY}}
      - **Reviewer:** {{REVIEWER_NAME}}
      - **Comment:** {{REVIEW_COMMENT}}
      - **Sensitive Paths Touched:** {{LIST_OF_SENSITIVE_FILES}}
      ```
   b. Spec-File committen: `git commit -m "docs: specs/CLAW-XXX.md Human Review dokumentiert (BOO-18)"`
   c. Danach regulaerer Commit mit dem Code.

> **Ohne `review-ok`-Bestätigung:** Schritt 6 wird NICHT erreicht. Keine Ausnahme, kein Auto-Bypass.

### Schritt 5.7: Change-Type-Verzweigung (BOO-68)

Vor dem Eintritt in die Quality Gates wird der `Change-Type` aus dem Spec-Frontmatter
(Sektion 8 Security Impact der Story; im Spec-File als `change_type` im Frontmatter)
gelesen und das Gate-Verhalten entsprechend gesetzt.

**Hintergrund:** Stories ohne klassischen Code-Diff (n8n/Make/Zapier-Workflow, Terraform/Pulumi/
CloudFormation-IaC, reine Cloud-/App-Configs, CMS-Content) wuerden ohne diese Verzweigung
alle Code-Gates leer durchlaufen und `final_status: passed` melden — obwohl niemand die
echten Risiken (Webhook-Auth, Credentials, IAM-Drift, oeffentliche Buckets) geprueft hat.
Schrader-Prinzip: "kein Output ohne Verify". Details siehe
[references/non-code-flow.md](references/non-code-flow.md).

**Ablauf:**

1. `change_type` aus Spec-Frontmatter lesen. Fallback wenn fehlt: `none` (Default = code-strict).
2. Pruefen, ob `change_type` in der Non-Code-Menge liegt:
   `{workflow, config, infrastructure, content}`.
3. Wenn **Code-Strict** (alle anderen Werte einschliesslich `none`): kein Verhaltenswechsel,
   weiter zu Schritt 6 wie bisher.
4. Wenn **Non-Code**: Gate-Modus auf `non-code` setzen. Wirkung:

| Gate | Code-Strict (Default) | Non-Code (`workflow`/`config`/`infrastructure`/`content`) |
|---|---|---|
| 6a ESLint/Ruff | Iterations-Loop, Hard | **Skip mit Begruendung in meta.json** |
| 6a-bis Semgrep | Iterations-Loop, Hard | **Skip mit Begruendung in meta.json** |
| 6a-tris Dependency | Hard bei Manifest-Diff | **Skip ausser Manifest tatsaechlich im Diff** |
| 6a-quart Coverage | Hard >=80% | **Skip mit Begruendung in meta.json** |
| 6b Akzeptanzkriterien | Hard | Hard (unveraendert) |
| 6c Architektur-Check | Soft | **Hard — Pflicht-Dokumentation** |
| 6d Smoke Test | Soft | **Hard — Pflicht-Ausfuehrung in Test-Env** |
| 6e Security-Findings | Dokumentation | **Hard — Pflicht-Dokumentation pro Domain-Risiko** |
| 5.5 Sensitive-Paths | Hard bei Treffer | Hard bei Treffer (unveraendert — Pattern fuer n8n/IaC/Config erweitern) |

5. **Skip-Begruendung in meta.json:** Skip ist NICHT stillschweigend. Jeder uebersprungene
   Code-Gate erscheint in `meta.json.skipped_gates` mit Grund:

   ```json
   "skipped_gates": {
     "eslint": "non-code: change_type=workflow",
     "semgrep": "non-code: change_type=workflow",
     "dependency": "non-code: no manifest in diff",
     "coverage": "non-code: change_type=workflow"
   }
   ```

6. **Optionale Domain-Gates (best-effort, nur wenn `tools_available.<tool>` aktiv):**
   - `change_type=workflow`: `tools_available.n8n_lint`, `tools_available.workflow_jsonschema`
   - `change_type=infrastructure`: `tools_available.tflint`, `tools_available.tfsec`, `tools_available.checkov`
   - `change_type=config`: `tools_available.yamllint`, `tools_available.jsonschema`, `tools_available.opa`
   - `change_type=content`: `tools_available.markdownlint`, `tools_available.broken_links`

   Fehlt das Tool: Skip mit Hinweis "Domain-Gate fuer change_type=X empfohlen — `tools_available.X` nicht aktiv".
   Konkrete Tool-Integrationen sind eigene Folge-Stories — diese Story etabliert nur den Mechanismus.

7. **meta.json bekommt zusaetzliches Feld `change_type`** (Audit-Spur fuer `/sprint-review`):

   ```json
   {
     "story_id": "BOO-XX",
     "change_type": "workflow",
     "iterations": { "eslint": 0, "tests": 0, "semgrep": 0, "coverage": 0 },
     "skipped_gates": { "eslint": "non-code: change_type=workflow", ... },
     "final_status": "passed"
   }
   ```

8. **PASS-Kriterien Non-Code (ueberschreiben validation-checklist.md PASS):**
   - 6b: alle ACs mit Evidenz abgehakt
   - 6c: Architektur-Quick-Check mit konkretem Befund dokumentiert (nicht leer)
   - 6d: Smoke Test ausgefuehrt + Output dokumentiert (Workflow getriggert, Plan/Apply gelaufen, Config angewendet)
   - 6e: Security-Findings pro Domain (Webhook-Auth / Credentials / IAM / Public Surface) dokumentiert oder explizit als "n/a — Begruendung" markiert
   - 5.5: bei Treffer `review-ok` vorhanden (unveraendert)

9. **FAIL-Kriterien Non-Code (ueberschreiben):**
   - 6c leer / "n/a" ohne Begruendung
   - 6d nicht ausgefuehrt oder Output nicht dokumentiert
   - 6e leer / "keine Pruefung" ohne Begruendung

> **Diese Verzweigung ersetzt nicht die `tools_available`-Logik aus Schritt 0.4** — sie ergaenzt
> sie. `tools_available` regelt "Tool da oder nicht", Schritt 5.7 regelt "Story-Natur Code oder
> nicht". Beide Mechanismen koennen denselben Gate skippen — `meta.json.skipped_gates`
> dokumentiert den Grund eindeutig.

### Schritt 6: Post-Implement Validation — Validate-Fix-Learn

Validierung BEVOR das Issue auf "Done" gesetzt wird. Siehe [references/validation-checklist.md](references/validation-checklist.md)

Dieser Schritt ist eine Schleife, kein einmaliger Check:

```text
Validate -> Interpret -> Decide -> Fix -> Re-Validate -> PASS/FAIL -> Learn
```

Regeln:
- Jeder fehlgeschlagene Gate-Lauf wird interpretiert, bevor Code gepatcht wird.
- Fixes werden nur fuer erkannte Ursachen gemacht, nicht blind fuer Symptome.
- Nach jedem Fix muss derselbe Gate erneut laufen.
- `Done` ist erst erlaubt, wenn alle blockierenden Gates gruen sind oder ein Operator eine dokumentierte Ausnahme bestaetigt.
- Nach PASS/FAIL wird ein Learning geschrieben, wenn ein wiederholbares Muster sichtbar wurde.

**6-Prelude) Iteration-Run-Setup — Persistenz-Verzeichnis fuer raw Tool-Outputs (BOO-36)**

Bevor die einzelnen Gates (6a/6a-bis/6a-quart/...) iterieren, wird **einmal pro Implement-Run** ein Persistenz-Verzeichnis fuer die raw Tool-Outputs angelegt. Alle Iterations-Outputs (ESLint, Semgrep, Tests, Coverage) landen parallel zur deklarativen Iteration auch dort — `/sprint-review` liest spaeter aus diesem Verzeichnis und aggregiert L2-Lessons. **`/implement` schreibt nur raw Outputs**, NICHT direkt in `journal/learnings.db` (L3). Die Trennung ist hart: Implement persistiert, Sprint-Review aggregiert.

```bash
# Default-Pfad (kann via paths.reports_local aus .claude/environment.json ueberschrieben werden)
REPORTS_BASE="journal/reports/local"
STAMP=$(date -u +%Y-%m-%d_%H%M)
STORY_ID="${ISSUE_KEY}"   # z.B. BOO-36
RUN_DIR="${REPORTS_BASE}/${STAMP}_${STORY_ID}"
mkdir -p "${RUN_DIR}"

# Start-Zeitstempel und Iterationen-Counter initialisieren (Shell-Variablen fuer meta.json)
RUN_STARTED_AT=$(date -u +%Y-%m-%dT%H:%M:%SZ)
ITER_ESLINT=0
ITER_TESTS=0
ITER_SEMGREP=0
ITER_COVERAGE=0
RUN_FINAL_STATUS="in_progress"
```

**Pfad-Konvention:**
- Default: `journal/reports/local/{YYYY-MM-DD_HHMM}_{STORY-ID}/` (lebend unter Projekt-Root)
- gitignored (Bootstrap legt den Eintrag in `.gitignore` an — siehe `references/file-templates.md` §.gitignore)
- Dateien pro Run:
  - `eslint-iter{N}.sarif` — pro ESLint-Iteration (`--format @microsoft/eslint-formatter-sarif --output-file ...` oder `--format json --output-file ...` als Fallback)
  - `tests-iter{N}.junit.xml` — pro Test-Iteration (`pytest --junit-xml=...` / `jest --reporters=default --reporters=jest-junit` mit `JEST_JUNIT_OUTPUT_FILE`)
  - `coverage-final.json` — Coverage-Endstand (c8 / pytest-cov, JSON-Reporter, einmaliger Lopy am Iterations-Ende)
  - `semgrep-final.sarif` — Semgrep-Endstand (`semgrep --sarif --output ...`, einmaliger Copy am Iterations-Ende)
  - `meta.json` — Run-Metadaten (Schema siehe Schritt 6-Closeout)

**Wichtig:** Schreib-Pfad ist eigenstaendig — wenn ein Gate uebersprungen wird (z.B. kein `eslint.config.mjs`), erscheint die entsprechende Datei nicht im Run-Verzeichnis. `meta.json.iterations.<gate>` bleibt dann auf `0`.

**Bei `tools_available.<tool> == false`** (aus `.claude/environment.json`): Persistenz fuer dieses Gate wird ebenfalls uebersprungen — das Verhalten passt zur regulaeren Gate-Logik, der raw Output entsteht ja gar nicht erst.

**6a) Code Quality Gate — ESLint + SonarLint + Error Lens (deklarative Iteration)**

> **Tool-Kette:** `eslint.config.mjs` definiert Regeln (Industriestandard seit BOO-2:
> ESLint Recommended + Airbnb Base + Security + SonarJS) → ESLint CLI prueft →
> SonarQube for IDE zeigt Tiefenanalyse → Error Lens zeigt beides inline in VS Code.

**Deklarativer Modus (Schrader Code Crash Z. 2105-2141, Compound Engineering Mechanik #1):**
Der Skill iteriert ueber den ESLint-Output bis 0 Errors — der Skill formuliert Code-Fixes
basierend auf den Findings, prueft erneut, und stoppt erst wenn das Gate gruen ist oder
das Iterations-Limit erreicht ist.

```bash
# Alle in diesem Commit geaenderten JS-Dateien pruefen — Pflicht-Run + SARIF-Persistenz pro Iteration
ITER_ESLINT=$((ITER_ESLINT + 1))
git diff --name-only HEAD | grep -E '\.(js|mjs)$' | \
  xargs npx eslint --max-warnings=0 \
    --format @microsoft/eslint-formatter-sarif \
    --output-file "${RUN_DIR}/eslint-iter${ITER_ESLINT}.sarif"
# Fallback ohne SARIF-Formatter: --format json --output-file "${RUN_DIR}/eslint-iter${ITER_ESLINT}.json"
```

> **SARIF vs JSON:** Wenn `@microsoft/eslint-formatter-sarif` als devDependency vorhanden ist, SARIF-Format nutzen (CI-tauglich, GitHub-Action-kompatibel). Sonst Built-in `--format json` als Fallback — dann heisst die Datei `eslint-iter{N}.json`. ESLint nativen SARIF-Support gibt es aktuell nicht; der `@microsoft/eslint-formatter-sarif`-Plugin ist der etablierte Weg.

**Iterations-Loop (Pflicht):**

1. ESLint auf geaenderten Dateien ausfuehren — Output landet IMMER auch in `${RUN_DIR}/eslint-iter${ITER_ESLINT}.sarif` (oder `.json` im Fallback).
2. Wenn `errors > 0`:
   a. Code-Fixes basierend auf Output formulieren (Skill liest Findings, schlaegt Patches vor)
   b. Patches anwenden (Edit-Tool)
   c. `ITER_ESLINT` erhoehen, erneut Schritt 1 pruefen (neuer Iterations-Output landet in `eslint-iter{N+1}.sarif`)
3. Wenn `errors == 0`: Gate bestanden — weiter zu Schritt 6b.
4. **Maximal 5 Iterationen.** Bei Iteration 5 ohne gruen: STOPP mit klarem Hinweis an
   den Operator: welche Findings persistieren, welche Fixes versucht wurden, warum sie
   nicht gegriffen haben. Operator entscheidet (manueller Fix, Regel-Ausnahme, oder Story
   als Carry-Over markieren).

**Gate-Verhalten:**
- **0 Errors + 0 Warnings:** Gate bestanden — weiter zu Schritt 6b.
- **Errors vorhanden + Iterationen verbleibend:** weiter iterieren.
- **Errors vorhanden + Iterations-Limit erreicht:** STOPP, Operator-Eingriff.
- **Nur Warnings:** Operator entscheidet ob akzeptabel (mit Begruendung im Linear-Kommentar).
- Kein `eslint.config.mjs` im Projekt: Gate ueberspringen + Operator hinweisen dass Regeldatei fehlt (BOO-2-Migration).

**Python-Aequivalent:** dasselbe Schema mit `npx eslint` -> `ruff check`, `eslint.config.mjs`
-> `pyproject.toml`. Ruff-Iteration laeuft mit demselben 5-Iterations-Limit. SARIF-Persistenz analog: `ruff check --output-format sarif --output-file "${RUN_DIR}/ruff-iter${ITER_ESLINT}.sarif"` (Ruff hat nativen SARIF-Support seit `ruff` 0.4.x). Counter-Variable bleibt `ITER_ESLINT`, der Datei-Name spiegelt den Linter (`ruff-iter{N}.sarif` statt `eslint-iter{N}.sarif`).

**6a-bis) Security Gate — Semgrep (deklarative Iteration, BOO-4)**

> **Tool-Kette:** `.semgrep.yml` (Manifest aus BOO-3) → Hook-Skript liest aktive Packs
> und konstruiert `--config p/...`-Flags → Semgrep CLI prueft → Findings im Output.
> Zweiter Quality-Gate nach ESLint, gleiche Iterations-Mechanik.

**Manifest-Reader (gleiche Logik wie im Pre-Commit-Hook und der GitHub Action):**

```bash
# Aktive Packs aus .semgrep.yml extrahieren
PACKS=$(grep -E '^[[:space:]]*-[[:space:]]+p/' .semgrep.yml | sed -E 's/^[[:space:]]*-[[:space:]]+//')
ARGS=""
for pack in $PACKS; do
    ARGS="$ARGS --config $pack"
done

# Semgrep auf geanderten Dateien — SARIF-Persistenz fuer den Final-Lauf
ITER_SEMGREP=$((ITER_SEMGREP + 1))
git diff --name-only HEAD | xargs semgrep $ARGS --error --quiet \
    --sarif --output "${RUN_DIR}/semgrep-final.sarif"
```

> **Semgrep-Persistenz-Konvention:** Wir schreiben pro Iteration NACH `${RUN_DIR}/semgrep-final.sarif` — der File-Name `-final` reflektiert, dass nur der Endstand fuer Sprint-Review interessant ist (Semgrep iteriert seltener als ESLint und das letzte File gewinnt durch Ueberschreiben). Counter `ITER_SEMGREP` wird trotzdem hochgezaehlt fuer `meta.json.iterations.semgrep`.

**Iterations-Loop (gleiche Mechanik wie 6a):**

1. Manifest-Reader laedt aktive Packs aus `.semgrep.yml`.
2. Semgrep auf geanderten Dateien ausfuehren mit konstruierten Flags — Output ueberschreibt `${RUN_DIR}/semgrep-final.sarif`.
3. Wenn Findings vorhanden:
   a. Code-Fixes basierend auf Output formulieren
   b. Patches anwenden (Edit-Tool)
   c. `ITER_SEMGREP` erhoehen, erneut Schritt 2 pruefen
4. Wenn 0 Findings: Gate bestanden — weiter zu 6b.
5. **Maximal 5 Iterationen.** Bei Iteration 5 ohne gruen: STOPP, Operator-Eingriff.

**Gate-Verhalten:**
- 0 Findings: Gate bestanden — weiter zu 6b.
- High/Critical Findings + Iterationen verbleibend: weiter iterieren.
- High/Critical Findings + Iterations-Limit erreicht: STOPP, Operator-Eingriff.
- Nur Medium/Low: Operator entscheidet (mit Begruendung im Linear-Kommentar).
- Kein `.semgrep.yml`: Gate ueberspringen + Operator hinweisen "Regeldatei fehlt — /bootstrap erneut" (BOO-3-Migration).
- Keine aktiven Packs in `.semgrep.yml` (alle auskommentiert): Gate ueberspringen + Hinweis.

**Laufzeit-Budget:** muss unter 10 Sekunden bleiben. Bei groesseren Repos Optimierung via `--baseline-ref HEAD~1` statt voller Scan.

**6a-tris) Dependency Gate — Slopsquatting-Schutz (BOO-12)**

> **Tool-Kette:** `git diff --cached` -> `hooks/dependency-check.sh` -> Registry-Lookup
> (npm view / pip / curl-Fallback) -> Existenz + Age + CVE-Check.
> Schrader Code Crash Kap. 3-4: KI-Halluzinationen sind eigener Angriffsvektor.

**Trigger:** Lauft NUR wenn `package.json`, `requirements.txt`, `pyproject.toml` oder
`Cargo.toml` im Diff sind. Sonst sofort Exit 0 (Performance).

**Drei Checks pro neu hinzugefuegter Dependency:**

1. **Existenz-Check** — Registry-Lookup (npmjs/pypi). 404 → BLOCKIERT (Halluzination?).
2. **Age-Check** — Package <30 Tage alt? Warnung (Typosquatter-Risiko, manuelle Verifikation).
3. **CVE-Check** — `npm audit --audit-level=high` / `pip-audit`. High/Critical → BLOCKIERT.

**Gate-Verhalten:**
- 0 Findings: Gate bestanden — weiter zu 6b.
- Existenz-404 / High/Critical CVE: Gate BLOCKIERT, Operator muss verifizieren oder Paket entfernen.
- Age-Warning: Gate bestanden, aber Hinweis im Output. Operator entscheidet ob das ein Risiko ist.
- Cargo-Diff: Hinweis "Cargo-Vollunterstuetzung in zukuenftiger Iteration", Operator laeuft `cargo audit` manuell.
- Tool-Fallback: Bei fehlendem `npm` / `pip-audit` wird auf curl gegen Registry zurueckgefallen.

**Laufzeit-Budget:** mit Registry-Lookup ueblicherweise 2-5 Sekunden. Bei vielen neuen
Dependencies parallelisierbar — heute serielle Implementation, optimierbar bei Bedarf.

**6a-quart) Coverage Gate — Diff-Coverage >=80% fuer neuen Code (BOO-15)**

> **Tool-Kette:** Test-Lauf (c8 / pytest-cov) -> coverage.json -> hooks/coverage-check.sh
> -> korreliert git diff --added mit Coverage-Daten -> Gate-Entscheidung.
> Schrader Code Crash Kap. 3: Gesamt-Coverage auf Legacy-Repos ist unfair —
> nur Diff-Coverage auf neu hinzugefuegten Zeilen.

**Wichtig:** Dieser Schritt laeuft im Skill, NICHT im Pre-Commit-Hook (Tests
dauern zu lange — wuerde 10s-Budget des Hooks sprengen).

**Iterations-Loop:**

1. Test-Lauf mit Coverage-Output und JUnit-XML pro Iteration:
   - Node: `npx c8 --reporter=json --reporter=text-summary npx jest --reporters=default --reporters=jest-junit` mit `JEST_JUNIT_OUTPUT_FILE="${RUN_DIR}/tests-iter${ITER_TESTS}.junit.xml"`. Coverage-Output landet in `coverage/coverage-final.json`.
   - Python: `pytest --cov --cov-report=json --junit-xml="${RUN_DIR}/tests-iter${ITER_TESTS}.junit.xml"`. Coverage-Output landet in `coverage.json`.
   - Iterations-Counter zuvor hochzaehlen: `ITER_TESTS=$((ITER_TESTS + 1))`.
   - Bei Iteration: `ITER_COVERAGE=$((ITER_COVERAGE + 1))` synchron.
2. `bash .claude/hooks/coverage-check.sh` aufrufen — vergleicht Added-Lines
   aus `git diff --cached -U0` mit Coverage-Daten.
3. Coverage-Endstand nach Run-Verzeichnis kopieren (einmaliger Copy am Iterations-Ende):
   - Node: `cp coverage/coverage-final.json "${RUN_DIR}/coverage-final.json"`
   - Python: `cp coverage.json "${RUN_DIR}/coverage-final.json"`
4. Gate-Verhalten:
   - **>=80% (Pass):** Gate bestanden — weiter zu 6b.
   - **60-80% (Warn):** Operator entscheidet, Begruendung im Linear-Kommentar.
   - **<60% (Block):** Tests hinzufuegen + Iterations-Schritt 1 wiederholen.
5. **Maximal 5 Iterationen.** Bei Iteration 5 ohne gruen: STOPP, Operator-Eingriff
   (manueller Test-Reichweiten-Plan oder Story splitten).

> **JUnit-XML-Konvention:** Sowohl pytest (`--junit-xml=...`) als auch jest-junit (env-var `JEST_JUNIT_OUTPUT_FILE`) schreiben JUnit-XML — Standardformat fuer Test-Reports, von `/sprint-review` parsbar. Wenn der Test-Runner kein JUnit-XML kann (z.B. Mocha ohne Reporter): Persistenz fuer Tests uebersprungen, `ITER_TESTS` wird nicht erhoeht, `meta.json.iterations.tests` bleibt 0 — der Coverage-Lauf selbst laeuft weiter.

**Gate-Verhalten Sonderfaelle:**
- Keine Coverage-Daten (kein `coverage-final.json` / `coverage.json`): Gate
  uebersprungen mit Hinweis "/bootstrap nachziehen fuer Test-Setup".
- Diff hat nur Test-Files / Configs / Docs: Gate uebersprungen.
- Diff hat 0 added lines: Gate uebersprungen.

**Konfiguration:** Schwellwerte sind als Konstanten im Skript (`COVERAGE_PASS=80`,
`COVERAGE_WARN=60`). Operator kann via env-vars override:
`COVERAGE_PASS=90 bash .claude/hooks/coverage-check.sh`.

**Laufzeit-Budget:** Skript-Lauf <2 Sekunden. Test-Lauf selbst kann mehrere
Minuten dauern — daher NICHT im Pre-Commit-Hook.

Schritt 2 — Syntax & Laufzeit:
- `node --check` auf alle geaenderten .js Files (Syntax-Fehler?)
- Falls Agent: 1x ausfuehren im DRY_RUN/TEST_MODE — laeuft er durch ohne Crash?
- Falls Library/Modul: Wird es korrekt importiert von allen Consumern?

**Hintergrund der 6 Tools:**
| Tool | Rolle | Wann aktiv |
|------|-------|-----------|
| **ESLint** (`.eslintrc.js`) | Definiert + prueft Coding-Regeln (Syntax, Security, Style) | CLI in Schritt 6a + passiv in VS Code |
| **Semgrep** (`.semgrep.yml`) | Pre-Commit-SAST mit Pack-basiertem Regelset | CLI in Schritt 6a-bis + Pre-Commit-Hook + CI-Layer |
| **Slopsquatting-Hook** (`.claude/hooks/dependency-check.sh`) | Supply-Chain-Pruefung (Existenz + Age + CVE) | Pre-Commit-Hook nach Semgrep, nur bei Manifest-Diff |
| **Coverage-Hook** (`.claude/hooks/coverage-check.sh`) | Diff-Coverage-Gate (>=80% added lines) | Wann aktiv: /implement Schritt 6a-quart, NICHT Pre-Commit-Hook |
| **SonarQube for IDE** (SonarLint) | Tiefere Security-Analyse, Code Smells, Bug-Patterns | Passiv im Editor waehrend Coding |
| **Error Lens** | Zeigt ESLint + SonarLint Findings inline in der Zeile | Passiv im Editor — kein Verstecken von Fehlern |

**6b) Akzeptanzkriterien + Linear-Kommentar** (PFLICHT)
- Jedes Akzeptanzkriterium aus der Issue-Description einzeln durchgehen
- Checkbox-fuer-Checkbox: Ist das Kriterium erfuellt? Evidenz notieren
- Falls ein Kriterium NICHT erfuellt: Fix implementieren oder Operator informieren
- **Linear-Kommentar schreiben** mit AC-Verification:
  ```
  ## AC-Verification
  - [x] AC 1: [Beschreibung] — ✅ [Evidenz]
  - [x] AC 2: [Beschreibung] — ✅ [Evidenz]
  - [ ] AC 3: [Beschreibung] — ❌ [Grund / was fehlt]
  ```

**6c) Architektur-Quick-Check**
- Nur die relevanten Dimensionen pruefen (siehe architecture-checklist.md)
- Fokus: Wurde etwas eingefuehrt das gegen bestehende Patterns verstoesst?
- Config-SSoT verletzt? Hardcoded Values statt config.js?
- Error Handling vorhanden wo noetig? (API-Calls, File I/O)

**6d) Smoke Test**
- Agent/Feature 1x real ausfuehren (nicht nur Syntax-Check)
- Output plausibel? Signal-File korrekt geschrieben?
- Keine unerwarteten Seiteneffekte auf andere Agents/Signals?

**6e) Security-Findings dokumentieren**
- Was wurde geprueft? (aus Schritt 3b Security-Checklist)
- Was ist sicher? Was wurde mitigiert?
- Offene Risiken die akzeptiert wurden?
- Bei LOW-Risk Stories genuegt: "Security: Keine neuen Angriffsvektoren"
- Abgleich mit `## Security Validation` aus der Story: Jede versprochene Validierung braucht Evidenz oder eine dokumentierte Ausnahme.
- Pruefen ob `SECURITY.md`, `API_INVENTORY.md`, `.semgrep.yml`, `.claude/sensitive-paths.json`, `.codex/hooks.json`, `ARCHITECTURE_DESIGN.md` oder `CONVENTIONS.md` durch die Aenderung aktualisiert werden muessen.
- **Onboarding-/Hub-Impact pruefen:** Pruefen ob `DEVELOPER_ONBOARDING.md` oder der Project Hub / PMO-Hub aktualisiert werden muessen. Trigger: neue Runtime-/Tool-Hinweise, geaenderte Zielarchitektur, neue Pflichtlektuere, geaenderte Backlog-/Issue-Arbeitsweise, neue Security-Regeln, neue Startpunkte fuer Umsetzung oder Handoff-relevante Annahmen. Ergebnis dokumentieren: aktualisiert oder "keine Aktualisierung noetig".

**6f) Ergebnis**
- **PASS:** Weiter zu Schritt 7 (Backlog-Record/Adapter → Done, Change-Log, Push)
- **FAIL:** Zurueck zu Schritt 5, Fix implementieren, erneut validieren
- Validation-Ergebnis als Kommentar/Ergebnisnotiz im Backlog-Record oder Adapter dokumentieren

**6g) Learn**
- Wenn ein Gate mehrfach fehlschlug, eine knappe Lesson in den aktiven Learning-Loop schreiben (`journal/learnings.md`, L2 oder L3 je nach `.learning-loop`).
- Wenn kein Learning-Loop aktiv ist: im Abschlussbericht notieren `Learning: SKIP bewusst — Learning-Loop nicht aktiviert`.
- Lesson-Format: Ursache, erprobter Fix, kuenftige Vorbeugung, betroffene Gate-/Tool-Kategorie.

Nach erfolgreicher Validation:
- Backlog-Record/Adapter → Done + Kommentar/Ergebnisnotiz (inkl. Validation-Ergebnis)
- Obsidian Change-Log via `linear.writeChangeLog()`

**6f-bis) meta.json schreiben (BOO-36, erweitert um BOO-84 Token-Tracking)**

Am Ende des Runs — egal ob PASS, FAIL oder STOP — wird `meta.json` ins Run-Verzeichnis geschrieben. Audit-Spur fuer `/sprint-review`.

Seit BOO-84 enthaelt das Schema zusaetzlich **drei Ebenen Token-Tracking** (pro Iteration, pro Skill-Aufruf, pro Story) plus **Cache-Hit-Rate** und einen **Override-Audit-Trail**. Tatsaechliche Token-Werte werden idealerweise via Claude-Code-PostToolUse-Hook in `.claude/last-run-tokens.json` zwischengespeichert und beim meta.json-Schreiben gemerged. Wenn Hook nicht aktiv: Operator paste die Token-Counts manuell ein (Claude Code zeigt sie am Session-Ende an), oder die Felder bleiben `null` (kein Cost-Aggregat im Sprint-Review fuer diese Story).

```bash
RUN_COMPLETED_AT=$(date -u +%Y-%m-%dT%H:%M:%SZ)
# RUN_FINAL_STATUS aus Schritt 6f setzen: "passed" | "failed" | "stopped_iteration_limit"
# ENVIRONMENT aus .claude/environment.json laden (mac/vps/ci) — Default "unknown" wenn Datei fehlt
ENVIRONMENT=$(jq -r .environment .claude/environment.json 2>/dev/null || echo "unknown")
# CHANGE_TYPE aus Spec-Frontmatter (Schritt 5.7) — Default "none" wenn nicht gesetzt
# SKIPPED_GATES_JSON wird in Schritt 5.7 / 6 pro uebersprungenem Gate gefuellt — Default "{}"

# BOO-84: Token-Tracking-Daten aus optionalem Hook-Cache laden, sonst leeres Skelett
TOKEN_CACHE=".claude/last-run-tokens.json"
if [ -f "$TOKEN_CACHE" ]; then
  TOKENS_JSON=$(cat "$TOKEN_CACHE")
else
  TOKENS_JSON='{"iterations": [], "skill_invocations": [], "story_totals": null, "cache_hit_rate": null}'
fi

# BOO-84: Override-Audit-Trail aus optionalem Cache laden, sonst leeres Array
OVERRIDE_CACHE=".claude/last-run-overrides.json"
if [ -f "$OVERRIDE_CACHE" ]; then
  OVERRIDE_JSON=$(cat "$OVERRIDE_CACHE")
else
  OVERRIDE_JSON='[]'
fi

cat > "${RUN_DIR}/meta.json" <<EOF
{
  "story_id": "${STORY_ID}",
  "change_type": "${CHANGE_TYPE:-none}",
  "started_at": "${RUN_STARTED_AT}",
  "completed_at": "${RUN_COMPLETED_AT}",
  "iterations": {
    "eslint": ${ITER_ESLINT},
    "tests": ${ITER_TESTS},
    "semgrep": ${ITER_SEMGREP},
    "coverage": ${ITER_COVERAGE}
  },
  "skipped_gates": ${SKIPPED_GATES_JSON:-"{}"},
  "final_status": "${RUN_FINAL_STATUS}",
  "environment": "${ENVIRONMENT}",
  "token_tracking": ${TOKENS_JSON},
  "override_audit": ${OVERRIDE_JSON}
}
EOF

# Nach erfolgreichem Schreiben: Caches loeschen, damit naechster Run frisch startet
rm -f "$TOKEN_CACHE" "$OVERRIDE_CACHE"
```

**Schema (erweitert durch BOO-68 change_type + skipped_gates und BOO-84 token_tracking + override_audit):**

```json
{
  "story_id": "BOO-15",
  "change_type": "api",
  "started_at": "2026-04-27T14:30:00Z",
  "completed_at": "2026-04-27T14:34:00Z",
  "iterations": {
    "eslint": 3,
    "tests": 2,
    "semgrep": 1,
    "coverage": 1
  },
  "skipped_gates": {},
  "final_status": "passed",
  "environment": "mac"
}
```

**Non-Code Beispiel (`change_type: workflow`):**

```json
{
  "story_id": "BOO-72",
  "change_type": "workflow",
  "started_at": "2026-05-22T10:00:00Z",
  "completed_at": "2026-05-22T10:08:00Z",
  "iterations": {
    "eslint": 0,
    "tests": 0,
    "semgrep": 0,
    "coverage": 0
  },
  "skipped_gates": {
    "eslint": "non-code: change_type=workflow",
    "semgrep": "non-code: change_type=workflow",
    "dependency": "non-code: no manifest in diff",
    "coverage": "non-code: change_type=workflow"
  },
  "final_status": "passed",
  "environment": "mac",
  "token_tracking": {
    "iterations": [
      {
        "iteration_label": "step-6a-eslint-1",
        "skill_invoked": "implement-iterations",
        "model_used": "claude-haiku-4-5-20251001",
        "model_tier": "haiku",
        "input_tokens": 4500,
        "output_tokens": 800,
        "cache_creation_input_tokens": 0,
        "cache_read_input_tokens": 12000
      }
    ],
    "skill_invocations": [
      {
        "skill_invoked": "implement-iterations",
        "model_tier_default": "haiku",
        "iterations_count": 3,
        "input_tokens_total": 13500,
        "output_tokens_total": 2400,
        "cache_creation_tokens_total": 0,
        "cache_read_tokens_total": 36000
      }
    ],
    "story_totals": {
      "input_tokens": 28000,
      "output_tokens": 5400,
      "cache_creation_tokens": 4500,
      "cache_read_tokens": 72000,
      "estimated_cost_usd": 0.18
    },
    "cache_hit_rate": 0.85
  },
  "override_audit": [
    {
      "skill": "implement-iterations",
      "recommended_tier": "haiku",
      "actual_model": "claude-sonnet-4-6",
      "override_origin": "cli-flag",
      "operator": "tobias",
      "timestamp": "2026-04-27T14:32:00Z"
    }
  ]
}
```

**Feld-Konvention:**
- `story_id`: Issue-Key aus Linear (z.B. `BOO-36`)
- `change_type`: aus Spec-Frontmatter (Schritt 5.7). Werte: `none | api | auth | data | dependency | ci | governance | external-provider | workflow | config | infrastructure | content` (BOO-68)
- `started_at` / `completed_at`: ISO-8601 UTC (`date -u +%Y-%m-%dT%H:%M:%SZ`)
- `iterations.<gate>`: Anzahl Iterationen pro Gate, 0 wenn Gate uebersprungen
- `skipped_gates.<gate>`: Grund pro uebersprungenem Gate (z.B. `"non-code: change_type=workflow"` oder `"tools_available.eslint == false"`). Leer `{}` wenn nichts geskippt.
- `final_status`: `passed` (Gate alle gruen) | `failed` (Gate-Block ohne Iterations-Limit) | `stopped_iteration_limit` (Iteration 5 erreicht ohne gruen)
- `environment`: `mac` | `vps` | `ci` | `unknown` (aus `.claude/environment.json`)
- `token_tracking.iterations[]`: pro Iteration eine Zeile — feinster Drill-Down
- `token_tracking.skill_invocations[]`: pro Skill-Aufruf aggregiert
- `token_tracking.story_totals`: gesamte Story-Summe + USD-Cost (Pricing aus `bootstrap/references/model-tiers.json`)
- `token_tracking.cache_hit_rate`: `cache_read_tokens / (input_tokens + cache_read_tokens)` — Optimierungs-Effekt
- `override_audit[]`: jedes Mal wenn der Operator das empfohlene Modell uebergeht (CLI-Flag oder CLAUDE.md), wird hier protokolliert
- `override_audit[].override_origin`: `cli-flag` | `claude-md` | `none` (none bedeutet: empfohlenes Tier wurde genutzt, normalerweise kein Eintrag)

**Verantwortlichkeiten (BOO-84):**
- Claude-Code-PostToolUse-Hook (optional, Folge-Setup) schreibt `.claude/last-run-tokens.json` und `.claude/last-run-overrides.json` waehrend des Runs.
- `/implement` Schritt 6f-bis mergt diese in `meta.json` und loescht die Caches.
- Wenn Hook nicht aktiv: Felder bleiben leer (`token_tracking: { ... cache_hit_rate: null }` und `override_audit: []`). Kein Story-Lauf blockiert, aber Sprint-Review zeigt fuer diese Story kein Cost-Aggregat.
- USD-Cost-Berechnung passiert OPTIONAL im `/sprint-review`-Skill mittels `bootstrap/references/model-tiers.json` — Pricing zentral, nicht in jeder meta.json dupliziert.

**Wichtig — Verantwortlichkeits-Trennung:**
- `/implement` schreibt NUR raw Outputs nach `journal/reports/local/` — inkl. `meta.json`.
- `/sprint-review` LIEST `journal/reports/local/` + `ci/` und aggregiert zu `journal/sprint-{date}.md` (L2). In einer zweiten Phase parsed `/sprint-review` die aggregierten Daten in `journal/learnings.db` (L3).
- **`/implement` schreibt NICHT direkt in `learnings.db`.** Diese Trennung haelt Implement schnell (kein DB-Lock, kein Schema-Wissen) und macht Sprint-Review zum Single Writer der Learnings-DB.

**6g) Intent-Verifikation**

> Dieser Schritt wird nur ausgefuehrt wenn `intents/INTENT-XX.md` im Projekt existiert.

1. Aktive `intents/INTENT-XX.md` laden
2. Pro Metrik im Intent:
   - Aktuellen Wert messen (Monitoring, Tests, Logs — je nach Metrik-Typ)
   - Ins Spec-File eintragen (unter `## Intent-Verifikation`):
     ```
     - Metrik: [Name]. Ziel: [Zielwert]. Messung: [Ist-Wert] [✅/⚠/❌]
     ```
3. Wenn alle Metriken ✅ → im Linear-Kommentar als "Intent: alle Metriken erreicht" notieren
4. Wenn Metriken ⚠ oder ❌ → Hinweis: "Intent-Metrik [X] nicht erreicht — neue Story zur Nacharbeit empfohlen?"

**Blockt nicht.** Selbst wenn eine Metrik schlechter geworden ist, geht der Commit durch. Der Measure-Loop dokumentiert nur, damit die naechste Story gezielt gegensteuern kann. (Schrader: "Nach jedem KI-Output fragt sich das Team: Erfuellt das unseren Intent?")

### Schritt 7: Backlog-Update

- Pruefen ob durch die Umsetzung andere Issues im Backlog betroffen sind
- Falls ja: Descriptions aktualisieren (neue Abhaengigkeiten, geaenderte Voraussetzungen)
- Falls Issues obsolet geworden sind: Operator informieren

### Schritt 8: Ergebnis-Tabelle (PFLICHT)

Nach Abschluss IMMER eine Zusammenfassungs-Tabelle ausgeben:

```markdown
| Was | Status |
|-----|--------|
| Config-Aenderung | ✅ Detail |
| Code-Aenderung | ✅ Detail |
| Tests/Verifikation | ✅ Detail |
| Dokumentation | ✅ Detail |
| Onboarding / Project Hub | ✅ aktualisiert oder keine Aktualisierung noetig |
| Git Push | ✅ Commit-Hash |
| Linear → Done | ✅ |
| Obsidian Change-Log | ✅ |
```

Zeilen je nach Umsetzung anpassen. Jede Zeile mit Checkmark und kurzem Detail.
Der Operator soll auf einen Blick sehen was gemacht wurde, ohne nachfragen zu muessen.

Danach: **`## Zusammenfassung` im Spec-File befuellen** (`specs/CLAW-XXX.md`).
Kein Fachjargon — so erklaert als wuerde man es einem Laien erzaehlen der das System nicht kennt.
3 Absaetze: (1) Was war das Problem? (2) Was wurde gebaut / wie funktioniert es? (3) Was aendert sich dadurch?
Dann committen: `git commit -m "docs: specs/CLAW-XXX.md Zusammenfassung ergaenzt"`

## Aenderungs-Checkliste (PFLICHT nach jeder Code-Aenderung)

Siehe [references/change-checklist.md](references/change-checklist.md)
