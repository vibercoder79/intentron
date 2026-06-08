# Release Notes - Wave T Vault Sync Improvements

> 🌐 **Language:** English (this file) · [🇩🇪 Deutsch](wave-t-vault-sync-improvements.md)

Status: 2026-05-28

## Purpose

Wave T closes BOO-82 and makes the framework-native vault harvest engine (BOO-77) **more team-capable and faster**. Two improvements, both from the review of Stefan's `project-template` (now accessible) — **rebuilt framework-native, no code taken over**:

1. **`default_vault_subdir` in the team contract** — the default vault layout now lives centrally in the versioned `tracked-paths.json`, no longer per employee in `local.json`.
2. **Incremental `--since <sha>` sync** — mirrors only files changed since `<sha>`, for large repos.

**Expected effect:** onboarding a new team member becomes trivial — `bash scripts/install-vault-sync.sh`, leave `path_mappings` empty, done. The vault layout is a team convention instead of a copy-paste obligation. Anyone who wants to deviate still overrides per person.

## Affected Stories

- BOO-82 — `default_vault_subdir` in the team contract + incremental `--since` sync

## Background: Stefan's Template as Model Consumer

Stefan's `StefanWeimarPRODOC/project-template` is a consumer fork that validates our appendices. During the review (Tobias, 2026-05-28) two genuine improvements stood out, which we adopt — the rest (GitHub Issues workflow, quality-gate.yml, fork-specific rules) deliberately stays out. **Stefan's code is not vendored** — both ideas are implemented framework-native, consistent with the BOO-77 decision.

## What Users Get With the Improvements

### 1. Default Vault Layout in the Team Contract

`tracked-paths.json` now carries a `default_vault_subdir` per entry with a `{project_slug}` placeholder:

```json
{ "glob": "docs/components/*.md", "type": "component", "default_vault_subdir": "02 Projekte/{project_slug}/Components/" }
```

The engine resolves the vault target in this order:

1. **`path_mappings` from `local.json`** — if a prefix matches (longest wins), per-employee override.
2. **`default_vault_subdir` from the team contract** — otherwise the team default.
3. **no match** → file is skipped (`SKIP`).

`local.json` thereby starts with `path_mappings: {}` — empty = contract default applies. Both placeholders `{project_slug}` and `{slug}` are substituted (backwards-compatible with old `{slug}` mappings).

### 2. Incremental Sync

```bash
python3 scripts/vault-sync.py --since <sha>
```

Syncs only files from `git diff --name-only <sha>..HEAD`. If git is not available or the SHA is invalid → WARN + full-sync fallback (no silent data loss). The post-merge hook still uses the full sync; `--since` is for manual/optimized runs.

## Backwards Compatibility

- Old `local.json` with a filled `path_mappings` (also `{slug}`) runs unchanged — the override stays first priority.
- Old `tracked-paths.json` without `default_vault_subdir`: entries without a default fall back to `path_mappings`; without either → `SKIP` (as before).
- Path containment check (`realpath` against `vault_path`) stays active unchanged.

## Validation (Smoke Test, 8 cases green)

1. `default_vault_subdir` without `path_mappings` → 3 files to default paths. ✓
2. `path_mappings` override wins; rest via default. ✓
3. `--since <sha>` → only the one changed file. ✓
4. Containment: `../ausbruch` mapping → BLOCK, 0 files outside. ✓
5. Frontmatter: `type:` only injected when missing, `title:` stays, `vault_sync_*` added. ✓
6. Invalid `--since` SHA → WARN + full sync. ✓
7. No `local.json` → quiet `exit 0`. ✓
8. `py_compile` OK. ✓

## Concrete Changes

| Area | Change | File |
|---|---|---|
| Engine | `_map_target` default fallback + `{project_slug}`/`{slug}`, `_changed_since` + `--since`, `_process_file` factored out | `bootstrap/references/vault-sync/vault-sync.py` |
| Team contract | `version: 1`, `_comment`, `default_vault_subdir` across 4 entries | `bootstrap/references/vault-sync/tracked-paths.json` |
| Installer | `local.json` template `path_mappings: {}` + explanatory `_comment` | `bootstrap/references/vault-sync/install-vault-sync.sh` |
| Config scaffold | Building block 1/2 + target resolution + `--since` + Phase 3 (DE+EN) | `bootstrap/references/vault-sync-pattern.md` + `.en.md` |
| HANDBUCH Appendix R | Team contract / local.json bullets + activation sentence extended (DE+EN) | `HANDBUCH.md` + `.en.md` |
| Spec | `specs/BOO-82.md` | specs/ |

## Skill Version Bumps

- None. Pure engine template + docs change; bootstrap copies the updated files unchanged via option `[e]`.

## Migration for Existing Projects

Projects that already activated the vault harvest pull the new engine + the extended team contract by re-copying the files from `bootstrap/references/vault-sync/` (or `bash bootstrap/scripts/migrate-to-v2.sh --issue BOO-77` re-copies the engine). Then add `default_vault_subdir` to the existing `tracked-paths.json` (team decision). An existing `local.json` with `path_mappings` keeps running without change.

## References

- Spec: `specs/BOO-82.md`
- Engine: `bootstrap/references/vault-sync/`
- HANDBUCH: Appendix R Layer 3 (Vault Harvest), `bootstrap/references/vault-sync-pattern.md`
- Previous vault wave: `docs/releases/wave-o-vault-sync-engine.md`
- Consolidated overview: `docs/releases/v0.2.0-overview.md`
- Operator decision: Tobias, 2026-05-28 (two ideas from Stefan's template, not the code)
- Linear: BOO-82
