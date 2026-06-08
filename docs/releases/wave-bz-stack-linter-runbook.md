# Wave BZ — Neuen Stack/Linter integrieren: Runbook + HANDBUCH-Kapitel (BOO-178)

> 🌐 **Sprache:** Deutsch (diese Datei) · [🇬🇧 English](wave-bz-stack-linter-runbook.en.md)

**Was jetzt da ist:** Ein dokumentierter, **verifizierbarer** Pfad, um einen **nicht-abgedeckten Stack** (z.B. TYPO3/PHP, Go) ins Framework zu integrieren. Der Bootstrap kannte `e) Anderes` mit Linter-Hinweistabelle (BOO-116) + Guided Discovery (BOO-127), aber kein „Wie". Getrieben aus echtem Feldeinsatz (TYPO3/PHP). Bewusste Design-Entscheidung: **nicht jede Sprache ins Framework einbauen** (Aufblähung) — stattdessen eine Anleitung, deren Garantie aus einem **Verifikations-Schritt** kommt, nicht aus einem Prompt.

## Änderungen

- **Runbook `docs/runbooks/stack-linter-integrieren.md` (+ `.en`):** kanonische Linter-Pfad-Tabelle (JS/TS, Python, **PHP**, Java/Kotlin, Go → Linter · Formatter · Typecheck · Coverage · Gate-Config) + Schritt-für-Schritt entlang der **5 Stellen**, plus:
  - **Pflicht-Brücke zu BOO-176** — die neuen Gate-Config-Dateien (z.B. `phpstan.neon`) in `.claude/sensitive-paths.json` eintragen, sonst greift „Messlatte nur Operator" für den neuen Stack nicht.
  - **Verifikations-Schritt** (der zentrale): absichtlich einen Lint-/Typ-Fehler einbauen → Gate muss **rot** werden → entfernen → grün. Manueller Test, kein Prompt — hier kommt die Garantie her.
  - **Kopiervorlagen:** PHP/TYPO3 (PHPStan + `phpstan.yml`-CI + PHPUnit-Coverage + sensitive-paths-Eintrag) und Go (golangci-lint).
  - **knowledge-onboarding-Hinweis** für externe Stack-/Versions-Doku (z.B. TYPO3).
- **HANDBUCH-Kapitel `8d-bis. Stack-Linter integrieren` (+ `.en`):** Konzept (warum nicht jede Sprache eingebaut wird) + die 5 Stellen mit Substanz → verweist aufs Runbook.
- **Bootstrap `e)`-Pfad** (`bootstrap/SKILL.md` + `.en`): Verweis auf HANDBUCH-Kapitel + Runbook (reiner Verweis-Satz, **kein** Versions-Bump).

## Die 5 Stellen

`environment.json tools_available` · CI-Workflow `.github/workflows/` · `.semgrep.yml`-Pack · Coverage-Tool (an 6a-quart) · ADR in `docs/domain/adrs/` — plus der Pflicht-Eintrag in `sensitive-paths.json`.

## Abgrenzung

- **Kein neuer Skill** (Stack-Integration zu variabel — PHPStan ≠ golangci ≠ ruff) und **kein „Prompt der sicherstellt"** — das Runbook IST die Anleitung + Prompt-Vorlage, die Garantie ist der Verifikations-Schritt.
- Gate-Config-Schutz-Mechanik = Schwester-Story **BOO-176** (hier nur der Eintrag-Schritt). Runbook ist **lebendes Dokument** — weitere Stacks später.
- Wave-Buchstabe **bz** (by = Index-Nachzug BOO-181).

## Verweise

Spec: `specs/BOO-178.md`. Branch: `tobiaschschmidt/boo-178-docs-stack-linter-runbook`. Verwandt: BOO-116/127 (Bootstrap-`e)`-Pfad), BOO-176 (Gate-Config-Schutz), BOO-180 (Doku-DoD). Operator-Quelle: Tobias, Feldeinsatz TYPO3/PHP 2026-06-07.
