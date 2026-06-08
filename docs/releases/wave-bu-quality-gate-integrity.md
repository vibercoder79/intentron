# Wave BU — Quality-Gate-Integrität: der Agent senkt die Messlatte nicht selbst (BOO-176)

> 🌐 **Sprache:** Deutsch (diese Datei) · [🇬🇧 English](wave-bu-quality-gate-integrity.en.md)

**Was jetzt da ist:** Ein KI-Agent kann die Qualitäts-Messlatte nicht mehr selbst absenken. Auslöser war ein realer Feldeinsatz (TYPO3/PHP, 2026-06-07): ein Agent weicht Gates auf — PHPStan-Level runter, Coverage-Schwelle gesenkt, Linter-Regeln deaktiviert — statt den Code zu fixen, und verkauft das als „pragmatisch". Leitprinzip jetzt verankert: **Die Messlatte ändert nur der Operator, nie der Agent als Workaround. Code fixen ✅, Gate aufweichen ❌.** Leichtgewicht gilt für den Prozess, nicht für die Code-Qualitäts-Schwelle.

## Änderungen

- **Gate-Configs unter Bodyguard-Schutz** — die Gate-Config-Dateien (`eslint.config.*`, `.eslintrc*`, `ruff.toml`, `pyproject.toml`, `.semgrep.yml/.yaml`, `phpstan.neon(.dist)`, `.coveragerc`, `jest.config.*`, `vitest.config.*`, `sonar-project.properties`) stehen jetzt im `.claude/sensitive-paths.json`-Default. Jede Änderung löst eine Gate-Block-Pause mit Operator-Freigabe aus. (`bootstrap/references/file-templates.md` + `.en`, `hooks-setup.md` + `.en`.)
- **Neues Bodyguard-Pattern `gate-configs.yml`** (Layer-0, immer geladen) — flaggt Regel-Deaktivierung schon beim Schreiben: datei-/blockweites `eslint-disable`, `@ts-nocheck`, nacktes `# noqa` / `# type: ignore`, modulweite Test-Skips, sowie das Editieren von Schwellen-Zeilen (`level:`, `fail_under`, `coverageThreshold`). Warn-Level (mit `BODYGUARD_STRICT=1` → Block).
- **Post-Story-Gate-Assertion erweitert** (`sprint-run/references/gate-assertion.md` + `.en`) um zwei deterministische Prüfungen gegen den Story-Diff:
  - **AC3a — Gate-Config-Diff:** eine gesenkte Schwelle / deaktivierte Regel (alt→neu verglichen) **ohne** dokumentierten `override_audit`-Eintrag → **Fail**.
  - **AC3b — change_type-Plausibilität:** `change_type` auf Non-Code (`workflow|config|infrastructure|content`), aber der Diff enthält echten App-Code → **Fail** (Code-Gates dürfen nicht über einen falschen `change_type` umgangen werden).
- **Governance-Doku** — Prinzip „Messlatte nur Operator" in `CONVENTIONS.md` (DE+EN-Block); neues Kapitel `change_type: Wann Code-Prüfungen legitim übersprungen werden` in `HANDBUCH.md` + `.en` (Operator-Sicht: was `change_type` ist, wer es setzt, wie die zwei Sperren Missbrauch verhindern).
- **Migration** — `migrate_boo_176()` in `migrate-to-v2.sh` rüstet Bestandsprojekte idempotent nach (Gate-Config-Pfade in `sensitive-paths.json` + `gate-configs.yml` installieren, `.bak`-Backup, nicht-destruktiv). Das Pattern-Template ist **byte-identisch** zur kanonischen Quelle in `file-templates.md` (SSoT).

## Abgrenzung

- **Allgemeingültig** für alle Stacks; die abgedeckten Gate-Config-Pfade (JS/TS/Python/PHP) gibt das Framework vor, nicht-abgedeckte Stacks tragen ihre Pfade via Stack-Runbook (BOO-178) nach.
- **Deterministisch** — Hooks/Assertion/Diff-Vergleich, kein Prompt.
- Test-Qualität (leere/Platzhalter-Tests) = Schwester-Story **BOO-177**; nicht-abgedeckte-Stack-Pfade = **BOO-178**.
- Wave-Buchstabe **bu** (bt = Release-Index BOO-173).

## Verweise

Spec: `specs/BOO-176.md`. Branch: `tobiaschschmidt/boo-176-feat-quality-gate-integritat`. Verwandt: BOO-86 (Layer-0-Bodyguard), BOO-165 (Post-Story-Gate-Assertion), BOO-68 (change_type / non-code-flow), BOO-177/178. Operator-Quelle: Tobias, Feldeinsatz TYPO3/PHP 2026-06-07.
