# Wave BB — CI Hardening Gaps (BOO-146–149)

**What's now in place:** Four gaps that the Next.js first-CI-run hardening (Wave BA) still missed are closed in the bootstrap SSoT — SARIF findings reach the Security tab again, `/implement` follows the remote CI run until it's green, `project-CLAUDE.md` declares its project type, and your own PR is mergeable in the solo/agent flow. Found on the CI post-mortem of `bko-widerspruch-assistent` (GWH Körting Institute, 2026-06-03), framework base v0.8.2. Pure template/config/CI/skill fixes — **no** runtime code. Existing projects retrofit idempotently via `migrate_boo_146/148/149`.

## What was broken

- **BOO-146 (BUG-3 remainder)** — The SARIF-upload workflows ran green, but the findings never showed up in the Security tab: with a hardened `GITHUB_TOKEN` the default permission is `contents: read`, and `github/codeql-action/upload-sarif@v4` fails **silently** without `security-events: write`.
- **BOO-147 (BUG-6)** — `/implement` pushed and was done; nobody checked whether the remote CI run went red. The local validate loop doesn't cover GitHub-specific failures (permissions, runner environment, SARIF upload).
- **BOO-148 (FEATURE-3)** — `project-CLAUDE.md` didn't state whether the repo is active code/deployment or a pure governance reference. Governance/docs repos ran through the same code/CI flow as code projects.
- **BOO-149 (BUG-5)** — Branch protection required 1 approval; GitHub doesn't allow self-approval — in the solo/agent flow your own PR was blocked.

## What's new

- **BOO-146** — Top-level `permissions` block (`contents: read` + `security-events: write`) in `semgrep.yml`/`eslint.yml`/`ruff.yml` (SSoT triplicate: templates + heredocs). `perf.yml`/`typecheck.yml`/`sonar.yml` **not** affected (no SARIF upload). New idempotent `migrate_boo_146` retrofits the block into existing workflows.
- **BOO-147** — New sub-step **6h Remote CI Loop** in `/implement` (DE+EN), after the push from step 5: `gh run watch --exit-status` → on failure `gh run view --log-failed` → diagnose/fix → re-push → max 3 iterations → operator escalation. Graceful degradation when `gh` is missing / not logged in / no remote (skip with a hint, **no** hard fail). Remote counterpart to the local validate-fix-learn loop.
- **BOO-148** — `{{PROJECT_TYPE_MARKER}}` as the first line after the H1 in `project-CLAUDE.md`; `bootstrap` §4.3a decides ACTIVE (default — code + deployment) vs GOVERNANCE REFERENCE (docs/specs only, no coding). Marker texts DE `PROJEKT-TYP: AKTIV` / `GOVERNANCE-REFERENZ`, EN `PROJECT TYPE: ACTIVE` / `GOVERNANCE REFERENCE`. `migrate_boo_148` retrofits default ACTIVE.
- **BOO-149** — `setup-branch-protection.sh` `required_approving_review_count` `1 → 0` (the solo/agent flow has no external approval, GitHub doesn't allow self-approval; status checks stay mandatory). `migrate_boo_149` re-applies branch protection.

## Changes (DE+EN)

- **`bootstrap/SKILL.md`** (version 3.37.0 → **3.38.0**): §4.3a decision rule ACTIVE vs GOVERNANCE REFERENCE + `{{PROJECT_TYPE_MARKER}}` rendering (BOO-148).
- **`implement/SKILL.md`** (version 2.11.1 → **2.12.0**): new sub-step 6h Remote CI Loop (BOO-147).
- **`bootstrap/references/file-templates.md`**: `permissions` block in semgrep/eslint/ruff.yml (BOO-146); `{{PROJECT_TYPE_MARKER}}` in project-CLAUDE.md (BOO-148).
- **`bootstrap/scripts/setup-branch-protection.sh`**: `required_approving_review_count` `1 → 0` (BOO-149).
- **`bootstrap/scripts/migrate-to-v2.sh`**: heredocs brought up to date; **three new idempotent** `migrate_boo_146/148/149` + `ALL_ISSUES` + `migrate_all()` registration (wave "CI Hardening Gaps", bug fixes → run in `--all`).

All changes are DE+EN-parity (`.en.md` counterparts updated). Framework v0.8.2 → **v0.9.0**.

## Migration for existing projects

`bash bootstrap/scripts/migrate-to-v2.sh --issue BOO-146` / `--issue BOO-148` / `--issue BOO-149` (or `--all`) — idempotent, run once. Apply the Wave BA CI-workflow fixes (BOO-140–143) first if needed. Functionally tested: second run = skip, no double-patch. (BOO-147 is an `/implement` skill fix without a migrate function — it takes effect automatically on the next run.)

## References

Specs: `specs/BOO-146.md`–`specs/BOO-149.md`. Branch: `feat/boo-146-149-ci-hardening-gaps`. Trigger: `bko-widerspruch-assistent` (CI post-mortem, 2026-06-03). Related: Wave BA (BOO-140–143, Next.js first-CI-run hardening), BOO-3/BOO-4 (Semgrep/SARIF), BOO-28 (CI gate).
