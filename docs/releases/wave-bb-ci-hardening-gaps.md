# Wave BB — CI-Hardening-Gaps (BOO-146–149)

**Was jetzt da ist:** Vier Lücken, die der Next.js-Erstlauf-Härtung (Wave BA) noch entgangen sind, sind im Bootstrap-SSoT geschlossen — SARIF-Findings landen wieder im Security-Tab, `/implement` verfolgt den Remote-CI-Lauf bis er grün ist, `project-CLAUDE.md` deklariert ihren Projekt-Typ, und der eigene PR lässt sich im Solo-/Agent-Flow mergen. Gefunden beim CI-Post-Mortem von `bko-widerspruch-assistent` (GWH Körting Institute, 2026-06-03), Basis Framework v0.8.2. Reine Template-/Config-/CI-/Skill-Fixes — **kein** Runtime-Code. Bestands-Projekte ziehen idempotent über `migrate_boo_146/148/149` nach.

## Was war kaputt

- **BOO-146 (BUG-3-Rest)** — Die SARIF-Upload-Workflows liefen grün, aber die Findings erschienen nie im Security-Tab: mit gehärtetem `GITHUB_TOKEN` ist die Default-Permission `contents: read`, und `github/codeql-action/upload-sarif@v4` scheitert ohne `security-events: write` **still**.
- **BOO-147 (BUG-6)** — `/implement` pushte und war fertig; ob der Remote-CI-Lauf rot wurde, prüfte niemand. Der lokale Validate-Loop deckt GitHub-spezifische Failures (Permissions, Runner-Umgebung, SARIF-Upload) nicht ab.
- **BOO-148 (FEATURE-3)** — `project-CLAUDE.md` sagte nicht, ob das Repo aktiver Code/Deployment ist oder reine Governance-Referenz. Governance-/Doku-Repos liefen durch denselben Code-/CI-Flow wie Code-Projekte.
- **BOO-149 (BUG-5)** — Branch-Protection verlangte 1 Approval; GitHub erlaubt keine Self-Approval — im Solo-/Agent-Flow blockierte der eigene PR.

## Was ist neu

- **BOO-146** — Top-Level-`permissions`-Block (`contents: read` + `security-events: write`) in `semgrep.yml`/`eslint.yml`/`ruff.yml` (SSoT-Triplikat: Templates + Heredocs). `perf.yml`/`typecheck.yml`/`sonar.yml` **nicht** betroffen (kein SARIF-Upload). Neue idempotente `migrate_boo_146` rüstet den Block in Bestands-Workflows nach.
- **BOO-147** — Neuer Sub-Step **6h Remote-CI-Loop** in `/implement` (DE+EN), nach dem Push aus Schritt 5: `gh run watch --exit-status` → bei Failure `gh run view --log-failed` → Diagnose/Fix → re-push → max 3 Iterationen → Operator-Eskalation. Graceful Degradation, wenn `gh` fehlt / nicht eingeloggt / kein Remote (Skip mit Hinweis, **kein** Hard-Fail). Remote-Pendant zum lokalen Validate-Fix-Learn-Loop.
- **BOO-148** — `{{PROJECT_TYPE_MARKER}}` als erste Zeile nach dem H1 in `project-CLAUDE.md`; `bootstrap` §4.3a entscheidet AKTIV (Default — Code + Deployment) vs GOVERNANCE-REFERENZ (nur Docs/Specs, kein Coding). Markertexte DE `PROJEKT-TYP: AKTIV` / `GOVERNANCE-REFERENZ`, EN `PROJECT TYPE: ACTIVE` / `GOVERNANCE REFERENCE`. `migrate_boo_148` rüstet Default AKTIV nach.
- **BOO-149** — `setup-branch-protection.sh` `required_approving_review_count` `1 → 0` (Solo-/Agent-Flow hat keine Fremd-Approval, GitHub erlaubt keine Self-Approval; Status-Checks bleiben Pflicht). `migrate_boo_149` wendet die Branch-Protection erneut an.

## Änderungen (DE+EN)

- **`bootstrap/SKILL.md`** (Version 3.37.0 → **3.38.0**): §4.3a Entscheidungsregel AKTIV vs GOVERNANCE-REFERENZ + `{{PROJECT_TYPE_MARKER}}`-Rendering (BOO-148).
- **`implement/SKILL.md`** (Version 2.11.1 → **2.12.0**): neuer Sub-Step 6h Remote-CI-Loop (BOO-147).
- **`bootstrap/references/file-templates.md`**: `permissions`-Block in semgrep/eslint/ruff.yml (BOO-146); `{{PROJECT_TYPE_MARKER}}` in project-CLAUDE.md (BOO-148).
- **`bootstrap/scripts/setup-branch-protection.sh`**: `required_approving_review_count` `1 → 0` (BOO-149).
- **`bootstrap/scripts/migrate-to-v2.sh`**: Heredocs auf den neuen Stand; **drei neue idempotente** `migrate_boo_146/148/149` + `ALL_ISSUES` + `migrate_all()`-Registrierung (Wave „CI-Hardening-Gaps", Bug-Fixes → laufen in `--all`).

Alle Änderungen DE+EN-paritätisch (`.en.md`-Pendants mitgezogen). Framework v0.8.2 → **v0.9.0**.

## Migration für Bestands-Projekte

`bash bootstrap/scripts/migrate-to-v2.sh --issue BOO-146` / `--issue BOO-148` / `--issue BOO-149` (bzw. `--all`) — idempotent, einmalig laufen lassen. Die CI-Workflow-Fixes aus Wave BA (BOO-140–143) ggf. vorher anwenden. Funktional getestet: zweiter Lauf = Skip, kein Doppel-Patch. (BOO-147 ist ein `/implement`-Skill-Fix ohne Migrate-Funktion — greift automatisch beim nächsten Lauf.)

## Verweise

Specs: `specs/BOO-146.md`–`specs/BOO-149.md`. Branch: `feat/boo-146-149-ci-hardening-gaps`. Anlassfall: `bko-widerspruch-assistent` (CI-Post-Mortem, 2026-06-03). Anknüpfung: Wave BA (BOO-140–143, Next.js-Erstlauf-Härtung), BOO-3/BOO-4 (Semgrep/SARIF), BOO-28 (CI-Gate).
