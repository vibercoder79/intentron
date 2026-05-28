# BOO-50 — Codex-Onboarding-Walkthrough (HANDBUCH Anhang J)

## Summary

**Umgeschnitten 2026-05-28** (Operator-Entscheidung Tobias, AskUserQuestion). Urspruenglicher Scope: eine fertige Codex-Daily-Bug-Scanner-Automation (TOML-Template + Bootstrap-Frage D.7 + Anhang J Setup). Neuer Scope: ein **durchgehender Codex-Onboarding-Walkthrough** als HANDBUCH **Anhang J** — "Framework unter Codex einfuehren".

Grund fuer den Umschnitt: Die Codex-*Einfuehrung* war die eigentliche Luecke, nicht eine spezifische Automation. Der Bootstrap fragt die Ziel-Runtime bereits ab (A.1c / BOO-53/54: `RUNTIME_TARGET = claude-code | codex | cross-tool | unknown`) und legt `AGENTS.md` + `CONVENTIONS.md` an. Anhang K (BOO-49) beschreibt die Codex-Nutzung als **Referenz** (Mappings, tool-agnostische Komponenten). Was fehlte: ein **durchgehender Schritt-fuer-Schritt-Pfad** von null zu einem laufenden Code-Crash-Projekt unter Codex. Die Bug-Scanner-Automation ist jetzt ein **optionales Beispiel** am Ende des Walkthroughs, kein eigenes Feature.

## Why

Operator-Erinnerung (Tobias 2026-05-28): "Ich dachte der Bootstrap fragt das heute ab und macht die Uebersetzung fuer andere KIs?" — korrekt (A.1c + AGENTS.md). Daraus die Frage: statt einer Codex-Automation lieber beschreiben, *wie man das Framework unter Codex einfuehrt*. Anhang K ist Referenz, kein Onboarding-Pfad; "Anhang J (geplant)" war eine offene Doku-Schuld mit toten Verweisen.

## What

**HANDBUCH Anhang J "Framework unter Codex einfuehren" (DE+EN), zwischen Anhang I und K:**

1. Voraussetzungen (Codex CLI, ChatGPT-Abo fuer Cloud-Sandbox, Framework-Repo als Skill-Quelle).
2. **Schritt 1 — Bootstrap mit Codex-Runtime:** A.1c `RUNTIME_TARGET = codex`/`cross-tool` → `AGENTS.md` + `CONVENTIONS.md` + `.codex/`. Bootstrap selbst am besten einmalig in Claude Code; ohne Claude Code: Einstiegs-Dateien aus Templates anlegen.
3. **Schritt 2 — Skills verfuegbar machen:** `ln -s ~/.claude/skills ~/.codex/skills`; Codex liest `name` + `description` aus dem Frontmatter.
4. **Schritt 3 — AGENTS.md/CONVENTIONS.md verstehen:** was Codex beim Session-Start liest (kein MCP noetig).
5. **Schritt 4 — Erster Story-Durchlauf:** Backlog-Record/Spec → `@Codex` im Issue ODER `codex run-task` → Codex-Plan/Breakdown → PR zurueck → Gates feuern tool-unabhaengig. Harte Gates bleiben (`write_scopes`, `execution_isolation`, Tests/Lint/Security/Review). Optionaler `codex_execution_hint`.
6. **Schritt 5 — Kontext-Bruecke (kein MCP):** `CONVENTIONS.md` + `specs/<ISSUE>.md` + `AGENTS.md`; optional n8n-Export.
7. **Schritt 6 — Verifikation:** `verify-setup.sh` (Anhang T) laeuft tool-unabhaengig; Hooks sind pro Repo auch unter Codex; 5-Schritte-E2E-Protokoll analog mit `codex run-task`.
8. **Optionales Beispiel — recurring Task (Daily Bug-Scanner):** `.codex/automations/<name>.toml`-Snippet (Cron + memory.md), Setup-Hinweise (Linear-Codex-Integration, GitHub-Auth, `$CODEX_HOME`-Workaround), Datenschutz-Tier (OpenAI US vs. Azure OpenAI Switzerland North → Verweis Anhang Q).
9. Grenzen: strategische Skills (`/intent`, `/ideation`, `/architecture-review`, `/sprint-review`) bleiben Claude-Code-empfohlen; Codex = execution-heavy/async.

**Verweis-Korrekturen:** Anhang K "Anhang J (geplant) — BOO-50" → "Anhang J — Framework unter Codex einfuehren"; "Siehe BOO-50" → Anhang J; "Codex aktivieren (BOO-50)" → Anhang J. DE + EN. README-Anhang-Liste um J ergaenzt.

## Out of Scope (verworfen aus Original-BOO-50)

- Eigenstaendige Bootstrap-Frage D.7 (Codex ist via A.1c-Runtime-Wahl bereits abgedeckt).
- `migrate_boo_50()` — reine Doku, kein Migrations-Patch.
- Voll-operationalisierte Bug-Scanner-Automation als Pflicht-Feature (jetzt optionales Beispiel-Snippet).
- Phasen B (PR-Review-Automation) + C (Worktree-Delegation) bleiben separate Folge-Ideen, falls je gebraucht.

## Acceptance Criteria

- [x] HANDBUCH Anhang J (DE+EN), durchgehender Walkthrough, ohne Anhang-K-Duplikation
- [x] Bug-Scanner-TOML als optionales Beispiel (nicht als Pflicht-Feature)
- [x] Anhang-K-Verweise + Footer korrigiert (DE+EN), keine toten "Anhang J geplant"-Verweise
- [x] README-Anhang-Liste um J ergaenzt
- [x] Spec + v0.2.0-overview-Erwaehnung + SecondBrain-Sync
- [x] Reine Doku, kein Versions-Bump, kein Migrations-Patch

## Constraints

- Keine erfundenen Codex-Features — alle Mechanik (`@Codex`, `codex run-task`, `.codex/automations/*.toml`, `$CODEX_HOME`-Workaround, Azure OpenAI Switzerland North, `codex_execution_hint`) stammt aus Anhang K + Original-BOO-50.
- Anhang J = Onboarding-Pfad, Anhang K = Referenz. J verweist auf K, dupliziert nicht.

## Dependencies

- BOO-49 (Tool-Adapter / Anhang K), BOO-53/54 (Runtime-Target + AGENTS.md/CONVENTIONS.md). Baut darauf auf.

## Session-Referenz

Umschnitt + Umsetzung Session 2026-05-28. Operator-Entscheidung Tobias (AskUserQuestion: "Anhang J = Codex-Onboarding-Walkthrough"). Linear: <https://linear.app/owlist/issue/BOO-50/>
