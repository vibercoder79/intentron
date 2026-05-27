---
story_id: BOO-68
title: Non-Code Change-Types — Workflow / Config / Infrastructure / Content
change_type: governance
execution_mode: linear
worktree_strategy: none
write_scopes:
  - ideation/
  - implement/
  - bootstrap/
  - CONVENTIONS.md
  - HANDBUCH.md
  - specs/
estimate: 5
token_estimate: 30
---

# BOO-68 — Non-Code Change-Types fuer Implement-Stage

## Schrader-Prompt-Bestandteile

### Insight (Perceive)

Das Code-Crash Framework geht heute implizit davon aus, dass jede Story Code produziert. Die Quality-Gates 6a (ESLint/Ruff), 6a-bis (Semgrep), 6a-tris (Dependency-Check) und 6a-quart (Coverage) sind alle code-zentriert und werden via `tools_available.<tool>` skippt, wenn die Tools fehlen oder kein passender Diff vorliegt.

Das ist ok fuer "kein Code wegen reiner Doku-Aenderung". Es ist NICHT ok fuer Implementierungen, die echte Risiken tragen, aber kein Code-Diff erzeugen — z.B. n8n-Workflows, Terraform/IaC-Modules, Cloud-Configs (IAM, DNS, CORS), Content-Migrationen in CMS-Systemen, Webhook-Konfigurationen.

Konkret: Wenn ein Operator eine Story implementiert, die einen n8n-Workflow mit Webhook-Trigger, externer API-Call und Credentials-Node baut, durchlaeuft `/implement` heute alle Code-Gates leer ("kein passender Diff") und meldet `final_status: passed` — obwohl niemand geprueft hat, ob der Webhook Auth hat, ob Credentials nicht im Klartext stehen, ob die Error-Branches sauber sind. Das verletzt das Schrader-Prinzip "kein Output ohne Verify" und das Code-Crash-Versprechen "Quality Gates sind Pflicht".

### Constraints

**Must:**
- `change_type` als Feld bleibt im Spec-Frontmatter (existiert schon, wird nur erweitert)
- Bestehende Werte (`none | api | auth | data | dependency | ci | governance | external-provider`) bleiben gueltig — additiv, kein Breaking Change
- Implement-Skill verzweigt nach `change_type` bevor die Code-Gates laufen (Schritt 5.7 oder als Block in 6-Prelude)
- Bei Non-Code-Types werden die Code-Gates **nicht stillschweigend skippt**, sondern explizit als "n/a fuer change_type=X" in `meta.json` vermerkt
- Soft-Gates 6c / 6d / 6e werden bei Non-Code-Types zu **Hard Gates** (kein PASS ohne dokumentierte Evidenz)
- DE + EN gleichberechtigt aktualisiert (gilt seit 2026-04-17 fuer alle Doku-Aenderungen)
- Spec-Gate bleibt unveraendert — Specs sind Pflicht, egal welcher change_type

**Must Not:**
- Keine neuen Tool-Abhaengigkeiten erzwingen (n8n-lint, tflint, tfsec bleiben optional via `tools_available`)
- Kein Auto-Bypass fuer "kein change_type gesetzt" (Default bleibt code-strict)
- Keine Excalidraw-Diagramme in diesem Commit blind ueberschreiben — overview.excalidraw bleibt, non-code-flow kommt separat dazu

**Out of Scope:**
- Konkrete Tool-Integrationen (n8n-Lint-Wrapper, tfsec-Hook) — eigene Folge-Stories
- Linear-Mirror-Update — der Nutzer macht das nach Merge selbst
- Migration bestehender alter Stories ohne `change_type` — bleibt Operator-Entscheidung

### Erfolgskriterien

1. Story-Template (`ideation/references/story-template-feature.md` + EN) listet die vier neuen Werte: `workflow | config | infrastructure | content`
2. Implement-Skill (`implement/SKILL.md` + EN) enthaelt einen neuen Schritt zwischen 5.5 und 6, der `change_type` aus dem Spec liest und das Gate-Verhalten entsprechend setzt
3. `validation-checklist.md` hat eine Non-Code-Spalte oder einen Non-Code-Block, der pro Gate ausweist: "Code-strict" vs. "Non-Code"
4. `change-checklist.md` (DE+EN) enthaelt Spezial-Checklisten fuer Workflow, IaC und Config (n8n-spezifisch, Terraform-spezifisch, generisch-Config)
5. Implement-README erklaert das Verhalten user-facing in DE+EN
6. Sketch in `implement/references/non-code-flow.md` mit ASCII-Flow + (optional) Excalidraw-Beilage
7. Bootstrap-Defaults fuer `.claude/sensitive-paths.json` enthalten Non-Code-Patterns (`n8n/**`, `infra/**`, `**/*.tf`, `workflows/**/*.json`)
8. CONVENTIONS.md / HANDBUCH.md geprueft und ergaenzt, wo `change_type`-Enum oder Implement-Flow erklaert wird
9. Spec-File-Frontmatter dieser Story selbst verwendet `change_type: governance` als Referenz-Beispiel

### Gewuenschtes Ergebnis

Ein Operator, der eine Story mit `change_type: workflow` implementiert, erlebt:
- `/implement` skippt die Code-Gates **explizit und nachvollziehbar** (in `meta.json.skipped_gates`)
- 6c Architektur-Check, 6d Smoke Test, 6e Security-Findings werden **erzwungen** (kein PASS ohne Evidenz)
- Bei Treffer in `sensitive-paths.json` (z.B. `n8n/**`) greift 5.5 weiterhin und verlangt `review-ok`
- Der Skill loggt im Linear-Kommentar / Backlog-Adapter ein klares "Non-Code-Path executed: gates X/Y/Z, skipped A/B/C"

Effekt fuers Framework: Non-Code-Implementierungen sind erst-klassige Buerger, nicht nur Edge-Cases. Risiken werden sichtbar statt versteckt.

## Definition of Done

- [ ] Alle 9 Erfolgskriterien erfuellt
- [ ] DE + EN konsistent
- [ ] Spec-Gate gruen (diese Datei existiert)
- [ ] PR erstellt, beschreibt das Schliessen der Luecke
- [ ] Operator kann nach Merge ein Test-Projekt mit `change_type: workflow` durchlaufen und sieht das neue Verhalten

## Security Impact

- **Change-Type:** governance
- **Angriffsoberflaeche:** Keine direkte Veraenderung der Code-Surface. Aber: die Aenderung _erhoeht_ die Sicherheit fuer eine ganze Klasse von Stories, die bisher unter dem Quality-Radar liefen.
- **Sensitive Pfade:** Beruehrt `implement/SKILL.md` (verhaltenssteuernd), `bootstrap/` (Default-Patterns). Beide sind Governance-relevant.
- **Referenzen zu lesen:** `SECURITY.md`, `CONVENTIONS.md`, bestehende Implement-References

## Security Validation

- Lokale Checks: `git diff --check`, manuelle Review der Skill-Verzweigungslogik auf Auto-Bypass-Risiken
- Sensitive Pfade: implement/SKILL.md selbst — Hard Review Pflicht
- Evidenz vor Done: Diff-Walkthrough im PR, dokumentierter Default-Test-Case (Story mit `change_type: workflow` durchlaeuft Skill ohne stilles PASS)
- Akzeptierte Risiken: keine — die Aenderung ist additiv und reduziert Risiko

## Akzeptanzkriterien

- [ ] AC1: `change_type`-Enum in Story-Templates (DE+EN) um `workflow | config | infrastructure | content` erweitert
- [ ] AC2: Implement-SKILL.md (DE+EN) hat neuen Schritt 5.7 "Change-Type-Verzweigung"
- [ ] AC3: validation-checklist.md zeigt Gate-Verhalten pro change_type
- [ ] AC4: change-checklist.md (DE+EN) hat Spezial-Sektionen fuer Workflow / IaC / Config
- [ ] AC5: Implement-README (DE+EN) erklaert Non-Code-Verhalten
- [ ] AC6: non-code-flow.md mit ASCII-Sketch existiert
- [ ] AC7: bootstrap/ Default-Patterns fuer sensitive-paths enthalten Non-Code-Patterns
- [ ] AC8: CONVENTIONS.md / HANDBUCH.md gepruefte/ergaenzte Stellen dokumentiert
- [ ] AC9: PR erstellt und linked
