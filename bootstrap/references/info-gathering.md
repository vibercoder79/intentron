# Info-Gathering — Block A (Projekt-Kern)

Der Bootstrap-Skill sammelt in Block A **nur die Projekt-Kern-Informationen** ein. Bestehende Infrastruktur wird in Block B erkundet, Doku-Architektur in Block C, Optional-Komponenten in Block D.

**Wichtig:** Fragen **einzeln oder in kleinen Gruppen** stellen (max 3 pro Rueckfrage), nicht als Batch.

## Pflicht-Informationen

| Variable | Frage an Operator | Beispiel |
|----------|------------------|----------|
| `STACK_CHOICE` * | Stack-Frage (a/b/c/d/e) — siehe SKILL.md Phase 1 A.1 | `d) Python` |
| `PROJECT_NAME` * | Wie heisst das Projekt? | `MyAnalytics` |
| `PROJECT_DESC` * | Ein Satz: Was macht das System? | `Datenanalyse-Tool fuer Marketing-KPIs` |
| `VERSION_START` * | Start-Version | `0.1.0` |
| `ISSUE_PREFIX` * | Prefix fuer Issues | default aus Projektname abgeleitet (z.B. `MA-`) |
| `PRIMARY_LANG` * | Primaere Sprache fuer Doku | `de` oder `en` (default `de`) |
| `ADDONS` * | Add-ons (Multi-Select) | siehe unten |
| `GOVERNANCE_MODE` * | Governance-Intensitaet | `lite` / `standard` / `heavy` (default `standard`) |
| `EXECUTION_ISOLATION` * | Parallel-Agenten-Isolation | `none` / `write-scope` / `git-worktree` (default je Modus) |

> **Optionaler Bestands-Quellen-Import (A.2b, BOO-117):** Existiert bereits eine Quelle (Intent-Datei, bestehendes Repo, vorhandene Doku), kann `PROJECT_DESC` — und optional `PROJECT_NAME` sowie ein `stack_hint` (Korrektur fuer A.1) — daraus **vorgeschlagen** statt manuell erfragt werden. Variable: `SOURCE_IMPORT = {type: intent|repo|doc|none, ref, derived}`. Sauber optional: Default `none`, kein Bruch ohne Quelle, Operator bestaetigt jeden Vorschlag. Details: `SKILL.md` §A.2b.

## Add-ons (Architektur-Dimensionen)

Standard-Dimensionen (immer aktiv, nicht abwaehlbar):
- Reliability
- Data Integrity
- Security
- Performance
- Observability
- Maintainability

Optionale Add-ons — Operator waehlt je nach Projekt:

| Add-on | Wann sinnvoll | Ergaenzt |
|--------|---------------|----------|
| **Privacy / DSGVO** | Voice-Assistants, personenbezogene Daten, Tier-Modelle | Dimension "Privacy" in `ARCHITECTURE_DESIGN.md`, Privacy-Sektion in `SECURITY.md`, Tier-Konzept-Platzhalter |
| **Cost Efficiency** | LLM-lastige Projekte, SaaS-Subscriptions, Rate-Limits | Dimension "Cost Efficiency", Budget-Regeln in `GOVERNANCE.md` |
| **Signal Quality** | ML / Analytics / Signal-Systeme | Dimension "Signal Quality", Evaluation-Metriken-Slot |
| **Compliance** | Regulierte Branchen (Gesundheit, Finanz, Legal) | Compliance-Sektion in `GOVERNANCE.md` und `SECURITY.md`, Audit-Trail-Regeln |

## Governance-Intensitaet

Diese Frage wird im `/bootstrap`-Setup in Block A.5 gestellt. "Light-Modus" ist die alltagssprachliche Bezeichnung; der technische Wert heisst `lite`.

| Modus | Wann sinnvoll | Wirkung im Bootstrap |
|-------|---------------|----------------------|
| `lite` | Experimente, Lernprojekte, kleine private Skripte | Minimaler Satz: `CLAUDE.md`/`AGENTS.md`, `CONVENTIONS.md`, `specs/`, Spec-Gate, Basis-Linting |
| `standard` | serioese Solo-Projekte, kleine Produktionsservices, Kundenarbeit | Default: Security-Gates, Issue-Guidelines, CI-Lint/SAST, Sensitive-Paths, Learning-Loop L1 |
| `heavy` | regulierte, umsatzkritische, Auth/Payment/PII-lastige oder langlebige Systeme | voller Satz: Coverage, Performance, SonarQube, Branch-Protection, Audit-Trail, Mandatory Review, L2/L3 optional |

## Execution-Isolation

| Wert | Wann sinnvoll | Regel |
|------|---------------|-------|
| `none` | nur lineare Arbeit, keine parallelen Agenten | `execution_mode: linear` only |
| `write-scope` | Subagents mit klar getrennten Datei-/Modul-Scopes | `sub-agents` erlaubt, wenn `write_scopes` in Spec stehen |
| `git-worktree` | parallele Agenten oder agentische Backlog-Abarbeitung | `agentic` erlaubt, jeder Agent eigener Worktree/Branch |

Default-Kopplung:
- `lite` → `none`
- `standard` → `write-scope`
- `heavy` → `git-worktree`

## Block B — Bestehende Infrastruktur

Siehe separates Dokument: `existing-infra-check.md`. Kurzfassung:

| Variable | Frage | Optionen |
|----------|-------|----------|
| `PROJECT_PATH` * | Projekt-Verzeichnis | existiert + Pfad / neu anlegen |
| `GITHUB_REPO` | GitHub-Repo | URL / spaeter / keines |
| `DOCUMENTATION_SSOT` * | Documentation-SSoT | Obsidian Vault / Repo docs / externes DMS / unentschieden |
| `OBSIDIAN_VAULT` | Obsidian-Vault fuer Doku | Pfad / nein (nur wenn SSoT Obsidian) |
| `EXTERNAL_DMS` | Externes DMS fuer Doku | System + Einstiegspunkt (nur wenn SSoT externes DMS) |
| `BACKLOG_TOOL` | Backlog-System | Linear + Slug / M365 / GitHub Issues / keines |
| `HAS_ENV` | .env existiert? | ja / nein |

## Block C — Doku-Architektur

Siehe `project-documentation-ssot.md` und `doc-architecture-proposal.md`. Der Skill legt zuerst den Documentation-SSoT-Contract aus Block B fest und praesentiert danach einen 3-Schichten-Vorschlag:
- Story-Specs (Repo)
- Project-Docs (Obsidian, `docs/project/`, externes DMS mit lokaler Verweisdatei oder Repo-Fallback)
- Component-Docs (Obsidian oder `docs/components/`)
- Architektur-Vorgaben (Obsidian, `docs/` oder externes DMS mit Repo-Verweis)
- Hub: `ARCHITECTURE_DESIGN.md` im Repo mit §9-Referenzen-Auto-Verlinkung

Obsidian ist die Best-Practice, aber nicht Voraussetzung. Bei externem DMS werden keine Inhalte dupliziert; `docs/project/README.md` dokumentiert nur Einstiegspunkt, Link-Konvention und Standard-Artefakte. Bei `undecided` erzeugt der Bootstrap den Repo-Fallback `docs/project/`, markiert ein TODO und setzt Postflight auf `WARN`. Operator bestaetigt oder passt an.

## Block D — Optional-Komponenten

Siehe `optional-components.md`. Kurzfassung:

| Variable | Frage | Default |
|----------|-------|---------|
| `SELF_HEALING` | Cron-Agent einrichten? | nein |
| `DOC_SYNC_OBSIDIAN` | DocSync zum Obsidian-Vault? | ja (wenn Vault) / nein (sonst) |
| `AUTOMATION_DAEMON` | Linear-Webhook-Daemon? | nein |
| `LEARNING_LOOP` | Learning-Loop-Level | L1 / L2 / L3 / nein (default L1) |

## Label-Taxonomie

Projektspezifische Labels fuer das Backlog-System. Minimum (immer):
- `architecture`, `bug`, `feature`, `refactor`, `docs`, `infra`

Abhaengig von aktivierten Add-ons:
- Privacy aktiv → `privacy`
- Compliance aktiv → `compliance`

Domain-Beispiele (Operator kann je nach Projekt erweitern):
- Web-App: `frontend`, `backend`, `api`, `ux`
- KI-System: `model`, `prompt`, `evaluation`, `data`
- Voice-Assistant: `voice`, `brain`, `memory`, `tools`, `interfaces`
- Research-Projekt: `research`, `analyse`, `hypothese`
- Backend-Service: `service`, `infra`, `api`, `db`

## Hook-Konfiguration

Governance-Hooks werden automatisch in Phase 4 installiert. Siehe `hooks-setup.md`.

Keine projekt-spezifische Anpassung noetig — nur `PROJECT_PATH` und `ISSUE_PREFIX` in den Hook-Scripts.

## Keine Agent-/Signal-Pflicht

Der Skill hat keine Annahmen ueber autonome Agent-Systeme oder Signal-Files. Wenn das Projekt autonome Agents braucht, wird das per Story im Projekt geklaert — nicht im Bootstrap.
