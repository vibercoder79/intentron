# Wave BA — Next.js-Erstlauf-Härtung (BOO-140–143)

**Was jetzt da ist:** Ein frisch gebootstrapptes Next.js-/Frontend-Projekt bekommt seinen **ersten CI-Lauf grün** — vier systematische Template-Fehler, die jedes neue Next.js-Projekt trafen, sind im Bootstrap-SSoT behoben. Gefunden beim ersten GitHub-Actions-Lauf von `bko-widerspruch-assistent` (Next.js 16). Reine Template-/Config-/CI-Fixes — **kein** Runtime-Code. Bestands-Projekte ziehen idempotent über `migrate_boo_140/141/142/143` nach.

## Stories

- **BOO-140** — **Next.js `package.json` lint-Script**: `create-next-app` setzt `"lint": "next lint"`; `next lint` versteht die ESLint-v9-Flat-Config nicht (`Invalid project directory ... /lint`). Der Bootstrap biegt das Script auf `"lint": "eslint ."` um. (Der CI-Workflow `eslint.yml` ruft seit BOO-28 ohnehin `npx eslint .`.) Plus Regressions-Guard in `verify-setup.sh`.
- **BOO-141** — **ESLint-Config React-/Browser-Globals (TSX)**: `eslint.config.mjs` bekommt für Stacks b/c mit JSX einen Frontend-Block mit `...globals.browser` **und** `React: 'readonly'` (Paket `globals`). Ohne ihn wirft `no-undef` bei jeder `.tsx` `'React' is not defined`.
- **BOO-142** — **Semgrep-Container raus + CodeQL v4**: `semgrep.yml` lief in `container: returntocorp/semgrep`, wodurch `actions/checkout` auf PRs konsistent scheitert. Container entfernt, Semgrep via `pip install semgrep` auf `ubuntu-latest`. Zusätzlich `github/codeql-action/upload-sarif@v3 → v4` (v3 deprecated Dez 2026) + `hashFiles`-Guard in **allen drei** Workflows (semgrep/eslint/ruff). Manifest-Reader-Logik unverändert.
- **BOO-143** — **Perf-Gate skippt bei leerer Baseline**: `perf.yml` failte (`exit 1`), wenn `journal/perf-baseline.json` noch `services: []` ist. Neuer `Check prerequisites`-Step → leere/fehlende Baseline = Benchmarks skippen, Gate grün. Sobald die Baseline befüllt ist, vergleicht das Gate normal.

## Änderungen (DE+EN)

- **`bootstrap/SKILL.md`** (Version 3.36.0 → **3.37.0**): Phase-4.4-Render-Regeln für den Frontend-Globals-Block (BOO-141) und die `package.json`-`lint`-Umbiegung (BOO-140).
- **`bootstrap/references/file-templates.md`**: semgrep.yml ohne Container + `pip install semgrep` + `upload-sarif@v4` + `hashFiles`-Guard (semgrep/eslint/ruff); perf.yml `Check prerequisites`-Skip + skip-gegatete Steps; `eslint.config.mjs` Frontend/React-Block; Doku-Notes.
- **`bootstrap/scripts/migrate-to-v2.sh`**: Heredocs (`migrate_boo_4`/`16`/`28`) auf den neuen Stand; **vier neue idempotente** `migrate_boo_140/141/142/143` + `ALL_ISSUES` + `migrate_all()`-Registrierung (Bug-Fixes, kein Opt-in → laufen in `--all`).
- **`bootstrap/references/verify-setup.sh`**: neue Sektion 7 „CI-Workflow-Sanity" — Guards für `next lint`-Reste, Semgrep-Container, `upload-sarif@v3`, fehlenden Perf-Skip.
- **`HANDBUCH.md` / `migration-checklist-v1-to-v2.md`**: SARIF-Upload-Prosa auf v4.

Alle Änderungen DE+EN-paritätisch (`.en.md`-Pendants mitgezogen).

## Retrofit für Bestands-Projekte

`bash bootstrap/scripts/migrate-to-v2.sh --issue BOO-142` (bzw. `--all`) — idempotent. `migrate_boo_140/142` patchen automatisch (mit Backup), `migrate_boo_141/143` geben Manual-Hinweise (operator-gerendert bzw. service-matrix-spezifisch). Funktional getestet: zweiter Lauf = Skip, kein Doppel-Patch.

## Verweise

Specs: `specs/BOO-140.md`–`specs/BOO-143.md`. Branch: `feat/boo-140-143-nextjs-ci-template-fixes`. PR: [vibercoder79/intentron#47](https://github.com/vibercoder79/intentron/pull/47). Anlassfall: `bko-widerspruch-assistent` (Next.js 16, erster CI-Lauf, 2026-06-03). Anknüpfung: BOO-28 (ESLint/Ruff CI-Gate), BOO-2 (ESLint-Regelsatz), BOO-3/BOO-4 (Semgrep), BOO-16/BOO-45 (Perf-/Lighthouse-Gate).
