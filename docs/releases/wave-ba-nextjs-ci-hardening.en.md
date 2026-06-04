# Wave BA — Next.js First-CI-Run Hardening (BOO-140–143)

**What's now in place:** A freshly bootstrapped Next.js/frontend project gets a **green first CI run** — four systematic template bugs that hit every new Next.js project are fixed in the bootstrap SSoT. Found on the first GitHub Actions run of `bko-widerspruch-assistent` (Next.js 16). Pure template/config/CI fixes — **no** runtime code. Existing projects retrofit idempotently via `migrate_boo_140/141/142/143`.

## Stories

- **BOO-140** — **Next.js `package.json` lint script**: `create-next-app` sets `"lint": "next lint"`; `next lint` doesn't understand the ESLint v9 flat config (`Invalid project directory ... /lint`). The bootstrap rewrites the script to `"lint": "eslint ."`. (The `eslint.yml` CI workflow has called `npx eslint .` since BOO-28.) Plus a regression guard in `verify-setup.sh`.
- **BOO-141** — **ESLint config React/browser globals (TSX)**: `eslint.config.mjs` gets a frontend block for stacks b/c with JSX, with `...globals.browser` **and** `React: 'readonly'` (package `globals`). Without it, `no-undef` throws `'React' is not defined` on every `.tsx`.
- **BOO-142** — **Semgrep container removed + CodeQL v4**: `semgrep.yml` ran in `container: returntocorp/semgrep`, which makes `actions/checkout` fail consistently on PRs. Container removed, Semgrep via `pip install semgrep` on `ubuntu-latest`. Plus `github/codeql-action/upload-sarif@v3 → v4` (v3 deprecated Dec 2026) + `hashFiles` guard across **all three** workflows (semgrep/eslint/ruff). Manifest-reader logic unchanged.
- **BOO-143** — **Perf gate skips on empty baseline**: `perf.yml` failed (`exit 1`) while `journal/perf-baseline.json` was still `services: []`. A new `Check prerequisites` step → empty/missing baseline = skip benchmarks, gate green. Once the baseline is filled, the gate compares normally.

## Changes (DE+EN)

- **`bootstrap/SKILL.md`** (version 3.36.0 → **3.37.0**): phase 4.4 render rules for the frontend globals block (BOO-141) and the `package.json` `lint` rewrite (BOO-140).
- **`bootstrap/references/file-templates.md`**: semgrep.yml without container + `pip install semgrep` + `upload-sarif@v4` + `hashFiles` guard (semgrep/eslint/ruff); perf.yml `Check prerequisites` skip + skip-gated steps; `eslint.config.mjs` frontend/React block; doc notes.
- **`bootstrap/scripts/migrate-to-v2.sh`**: heredocs (`migrate_boo_4`/`16`/`28`) brought up to date; **four new idempotent** `migrate_boo_140/141/142/143` + `ALL_ISSUES` + `migrate_all()` registration (bug fixes, not opt-in → run in `--all`).
- **`bootstrap/references/verify-setup.sh`**: new section 7 "CI workflow sanity" — guards for `next lint` leftovers, Semgrep container, `upload-sarif@v3`, missing perf skip.
- **`HANDBUCH.md` / `migration-checklist-v1-to-v2.md`**: SARIF-upload prose to v4.

All changes are DE+EN-parity (`.en.md` counterparts updated).

## Retrofit for existing projects

`bash bootstrap/scripts/migrate-to-v2.sh --issue BOO-142` (or `--all`) — idempotent. `migrate_boo_140/142` patch automatically (with backup), `migrate_boo_141/143` emit manual hints (operator-rendered / service-matrix-specific). Functionally tested: second run = skip, no double-patch.

## References

Specs: `specs/BOO-140.md`–`specs/BOO-143.md`. Branch: `feat/boo-140-143-nextjs-ci-template-fixes`. Trigger: `bko-widerspruch-assistent` (Next.js 16, first CI run, 2026-06-03). Related: BOO-28 (ESLint/Ruff CI gate), BOO-2 (ESLint ruleset), BOO-3/BOO-4 (Semgrep), BOO-16/BOO-45 (perf/Lighthouse gate).
