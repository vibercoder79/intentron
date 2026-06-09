# Wave CC — Linter-Verdrahtung end-to-end: zentrales Bild + Sketch (BOO-182)

> 🌐 **Sprache:** Deutsch (diese Datei) · [🇬🇧 English](wave-cc-linter-verdrahtung-e2e.en.md)

**Was jetzt da ist:** **Ein** Bild der **ganzen** Linter-Kette — `Kontrolldatei → Trigger (Hook/CI) → Linter → Gate → Report-Persistenz → /sprint-review` — für **beide Linter** (ESLint JS/TS, Semgrep/SAST) und **beide Layer** (lokaler Pre-Commit-Hook, CI-Workflow). Die Verdrahtung war vollständig vorhanden, aber über viele Detailstellen verstreut (HANDBUCH 8/8d/8d-bis, implement/README, Runbook, Security-Template, Artefakt-Landkarte). Das neue HANDBUCH-Kapitel `8d-quart` bündelt diese Stellen und beantwortet die eine Frage, die keine Einzelstelle beantwortet: **Wie teilen lokaler Pre-Commit-Hook und CI-Workflow dieselbe Config-Reader-Logik, und wo landen die Reports?**

## Änderungen

- **HANDBUCH-Kapitel `8d-quart` „So greift die Linter-Verdrahtung ineinander (End-to-End)" (+ `.en`):** die ganze Kette in einem Bild, mit der Ground-Truth:
  - `.semgrep.yml` (Manifest) und `eslint.config.mjs` (Flat Config) werden von **demselben** Bash-Reader gelesen — im lokalen Pre-Commit-Hook **und** im CI-Workflow.
  - Gates blocken via **Required Status Checks** (BOO-29); CI fängt auch `git commit --no-verify` ab.
  - Manifest-Feinheit: `semgrep --config=.semgrep.yml` liefert bewusst „No config given" (Manifest, kein nativer Config) — erwartetes Verhalten.
- **Sketch `docs/linter-verdrahtung-e2e.*` (+ `.en`, OWLIST-Farben):** visuelle Kette, im Kapitel eingebettet.
- **Cross-Links** von Runbook (`stack-linter-integrieren`), `implement/README`, Security-Template, Artefakt-Landkarte und HANDBUCH 8/8d/8d-bis auf das neue Kapitel — je ein knapper Verweis-Satz.
- **Korrektur Report-Persistenz:** sind **zwei Ströme**, nicht einer:
  - **lokal (BOO-36):** `/implement` schreibt direkt nach `journal/reports/local/...`.
  - **CI (BOO-32):** Aggregator kopiert `.ci-reports/*.sarif` → `journal/reports/ci/run-{id}/`.
  - Beide werden von `/sprint-review` konsumiert. Die frühere Kurzform „`.ci-reports → journal/reports/local`" war ungenau und ist korrigiert.

## Die Kette

`Kontrolldatei (.semgrep.yml / eslint.config.mjs)` → `Trigger (Pre-Commit-Hook · CI-Workflow)` → `Linter (Semgrep · ESLint)` → `Gate (Required Status Check, BOO-29)` → `Report-Persistenz (lokal BOO-36 · CI BOO-32)` → `/sprint-review`.

## Abgrenzung

- **Reine Doku** — kein Linter-, Config-, Hook- oder Workflow-Change.
- Neue Stacks/Linter bleiben im Runbook **BOO-178** (nur verlinkt). Gate-Config-Schutz-Mechanik bleibt **BOO-176** (nur referenziert).
- Codex `.codex/hooks.json` ist eine bekannte Grenze (nur in Artefaktlisten genannt, kein Schema/Beispiel im Repo) — im Kapitel nicht als fertig dargestellt.
- Kein eigenständiges Explainer-Artefakt → kein neuer `docs/INDEX.md`-Eintrag (reines HANDBUCH-Kapitel).
- Wave-Buchstabe **cc**.

## Verweise

Spec: `specs/BOO-182.md`. Branch: `tobiaschschmidt/boo-182-docs-zentrales-end-to-end-bild-der-linter-verdrahtung`. Verwandt: BOO-174 (EN-Parität Alt-Waves), BOO-176 (Gate-Config-Schutz), BOO-178 (Stack-Linter-Runbook), BOO-180 (Doku-DoD).
