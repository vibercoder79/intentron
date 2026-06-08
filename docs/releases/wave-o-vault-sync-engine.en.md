# Release Notes - Wave O Framework-native Vault-Sync Engine

> 🌐 **Language:** English (this file) · [🇩🇪 Deutsch](wave-o-vault-sync-engine.md)

Status: 2026-05-28

## Purpose

Wave O closes BOO-77 and turns the documented vault harvest pattern (BOO-75) into a **working setup**. On bootstrap option `[e] Repo docs + personal vault harvest` the framework now sets up the complete vault harvest — with its **own, lean sync engine**, no longer just a reference to a neighbouring repo.

**Expected effect:** Anyone working in a team who wants to use their personal Obsidian vault as a cross-project read view picks `[e]` in bootstrap and then has everything set up with a single `bash scripts/install-vault-sync.sh`. No external code, no dependencies.

## Affected Stories

- BOO-77 — framework-native vault-sync engine + bootstrap `[e]` wiring

## Background: why framework-native instead of vendored

BOO-75 (Wave N) documented the vault harvest pattern and pointed to Stefan's `StefanWeimarPRODOC/project-template` for the engine. Phase 2 (vendoring his code) was blocked because the repo is not accessible. Operator decision (Tobias, 2026-05-28): **Stefan's code is not needed** — the framework builds its own lean implementation of the documented pattern. This resolves the blocker and the framework stays self-contained.

## What Users Get with the New Setup

Four engine files under `bootstrap/references/vault-sync/` that bootstrap option `[e]` copies into the project:

- **`vault-sync.py`** — one-way sync engine repo→vault (Python stdlib). Reads the versioned team contract `.vault-sync/tracked-paths.json` + the gitignored `.vault-sync/local.json` per team member. Frontmatter merge with `vault_sync_*` namespace (idempotent), `type:` injection only when the source has none. Modes `auto` / `dry-run` / `ask`. Skips `.notes.md` sidecars.
- **`install-vault-sync.sh`** — interactive init per team member (`--force` / `--uninstall`), creates `local.json`, adds the `.gitignore` entry, symlinks the hook.
- **`post-merge.sh`** — hook wrapper, fires after `git pull`, `exit 0` without `local.json` (zero friction).
- **`tracked-paths.json`** — versioned team contract, 4 defaults.

## Security (implemented + tested)

- **One-way:** writes ONLY into the vault, NEVER into the repo.
- **Path containment:** every vault target is checked via `realpath` against `vault_path` — `../` escape and symlink traversal are blocked.
- **Dry-run default**, no secrets, no network calls, Python stdlib only.
- **security-architect REVIEW** (manual): one-way data flow, no eval/exec, no shell-injection vector. No findings.
- **Smoke test (6 cases green):** dry-run / real-auto / containment block / enabled=false / no local.json / sidecar protection.

## Concrete Changes

| Area | Change | File |
|---|---|---|
| Engine files NEW | vault-sync.py + install-vault-sync.sh + post-merge.sh + tracked-paths.json | `bootstrap/references/vault-sync/` |
| Bootstrap Block B.3 `[e]` | reworked from "documented choice" to "generate engine files + .gitignore + hook" (DE+EN), v3.31.0 | `bootstrap/SKILL.md` + `.en.md` |
| Config scaffold | mechanics section + phases + security reworked to framework-native (DE+EN) | `bootstrap/references/vault-sync-pattern.md` + `.en.md` |
| HANDBUCH Appendix R Layer 3 | activation sentence reworked to framework-native engine (DE+EN) | `HANDBUCH.md` + `.en.md` |
| Migration | `migrate_boo_77` (copies engine files into existing project) + ALL_ISSUES | `bootstrap/scripts/migrate-to-v2.sh` |
| Migration checklist | §BOO-77 (DE+EN) | `bootstrap/references/migration-checklist-v1-to-v2.md` + `.en.md` |
| Spec | `specs/BOO-77.md` | specs/ |

## Skill Version Bumps

- `bootstrap` 3.30.0 → 3.31.0 (option `[e]` now generates engine files)

## Migration for Existing Projects

```bash
bash bootstrap/scripts/migrate-to-v2.sh --issue BOO-77
```

Idempotent + non-destructive: copies the engine files only if not present, does NOT write into the vault. Afterwards, per team member, `bash scripts/install-vault-sync.sh`.

## Reference to BOO-75

Wave O resolves the "Phase 2 = vendoring Stefan's code" path documented in BOO-75 **differently** than originally intended: framework-native instead of vendored. Stefan's `project-template` remains the pattern impulse, but is not the code source. No master/mirror sync needed (own code, unlike with DPO/BOO-74).

## References

- Spec: `specs/BOO-77.md`
- Engine: `bootstrap/references/vault-sync/`
- HANDBUCH: Appendix R Layer 3 (vault harvest), `bootstrap/references/vault-sync-pattern.md`
- Previous wave: `docs/releases/wave-n-vault-harvest-and-skill-location.md`
- Consolidated overview: `docs/releases/v0.2.0-overview.md`
- Operator decision: Tobias, 2026-05-28
- Linear: BOO-77
