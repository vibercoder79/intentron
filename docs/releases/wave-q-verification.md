# Release Notes - Wave Q Post-Install-Verifikation

> 🌐 **Sprache:** Deutsch (diese Datei) · [🇬🇧 English](wave-q-verification.en.md)

Stand: 2026-05-28

## Zweck

Wave Q (BOO-79) beantwortet die Operator-Frage "Framework installiert — funktioniert auch alles?". Beide Richtungen: ein automatisiertes Skript `verify-setup.sh` + eine manuelle Checkliste (HANDBUCH Anhang T). Loest den lange geparkten **BOO-48 E2E-Smoke-Test**-Gedanken.

## Betroffene Stories

- BOO-79 — verify-setup.sh + HANDBUCH Anhang T + Bootstrap Phase 7.3b

## Was Nutzer bekommen

- **`bootstrap/references/verify-setup.sh`** (Bash, BSD+Linux, keine Dependencies, read-only): prueft 6 Gruppen und gibt PASS/WARN/FAIL aus —
  1. `.claude/environment.json` vorhanden + lesbar
  2. Toolchain erreichbar (`command -v` pro `tools_available: true`; eslint via npx ok)
  3. Git-Hooks pro Repo (pre-commit, spec-gate, doc-version-sync)
  4. Kern-Artefakte (CONVENTIONS.md, ARCHITECTURE_DESIGN.md, specs/, journal/)
  5. Privacy-Add-on (PRIVACY.md + personal-data-paths.json, falls aktiv)
  6. Backlog-Adapter
  Exit 1 bei FAIL (CI-tauglich), `--strict` (WARN→FAIL), `--quiet`.
- **HANDBUCH Anhang T "Post-Install-Verifikation"** (DE+EN): 7-Punkte-Checkliste manuell. **Check 5 (Skill schreibt Artefakte) ist bewusst ein manueller `/implement`-Probelauf** — der End-to-End-Beweis, den ein Shell-Skript nicht liefert.
- **Bootstrap Phase 7.3b:** kopiert + ruft `verify-setup.sh` vor dem finalen Commit → der Operator sieht sofort den Proof. bootstrap v3.31.0 → v3.32.0.

## Wann ausfuehren

- direkt nach Bootstrap (Phase 7.3b automatisch)
- **nach jedem `git clone`** auf einer neuen Maschine (Hooks + environment.json sind pro Repo/Maschine — siehe Anhang S)
- in CI als Gate (`--strict`)

## Konkrete Aenderungen

| Bereich | Datei |
|---|---|
| verify-setup.sh NEU | `bootstrap/references/verify-setup.sh` |
| HANDBUCH Anhang T (DE+EN) | `HANDBUCH.md` + `HANDBUCH.en.md` |
| Bootstrap Phase 7.3b (DE+EN), v3.32.0 | `bootstrap/SKILL.md` + `.en.md` |
| Migration | `migrate_boo_79` in `bootstrap/scripts/migrate-to-v2.sh` |
| Migration-Checklist §BOO-79 (DE+EN) | `bootstrap/references/migration-checklist-v1-to-v2.md` + `.en.md` |
| Spec | `specs/BOO-79.md` |

## Smoke-Test (bestanden)

- Leeres Repo → 4 FAIL, Exit 1.
- Minimal vollstaendiges Projekt → 12 PASS, Exit 0.

## Skill-Versions-Bumps

- `bootstrap` 3.31.0 → 3.32.0 (Phase 7.3b)

## Verweise

- Spec: `specs/BOO-79.md`
- Skript: `bootstrap/references/verify-setup.sh`
- HANDBUCH Anhang T, Bootstrap Phase 7.3b
- Loest: BOO-48 (E2E-Smoke-Test)
- Operator-Frage: Tobias, 2026-05-28
- Linear: BOO-79
