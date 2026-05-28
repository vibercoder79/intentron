# Vault-Harvest Pattern — Config Scaffold + framework-native engine (BOO-75/77/82)

Repo docs + personal vault harvest for multi-person teams with Obsidian users. This document describes the data contract and the mechanism. The **sync engine is framework-native since BOO-77** — it lives under `bootstrap/references/vault-sync/` (`vault-sync.py`, `install-vault-sync.sh`, `post-merge.sh`, `tracked-paths.json`) and is copied into the project by bootstrap option `[e]`. No external code, no dependencies (Python stdlib + Bash). Stefan's `project-template` was the pattern impulse but is **not** the source of the engine.

> **Sibling file (German):** [`vault-sync-pattern.md`](./vault-sync-pattern.md)
> **HANDBUCH background:** Appendix R Layer 3 (vault-harvest pattern, two-flow model).

## When to use this pattern

A team works on the same GitHub repo (docs live in `docs/`), **and** individual operators want to keep seeing cross-project insights in their personal Obsidian vault. Obsidian is a solo tool — there is no shared team vault. The pattern solves this via two separate flows:

- **Flow 1 (plain Git, all, bidirectional):** `docs/` ↔ GitHub repo via `git push`/`git pull`. Team SSoT.
- **Flow 2 (harvest, per person, one-way):** a `git post-merge` hook copies selected `docs/` files into the personal vault — never back.

## Building block 1 — team contract `.vault-sync/tracked-paths.json` (versioned)

Defines which repo paths are harvestable, which `type:` frontmatter is added when mirrored, **and where the file lands in the vault by default** (`default_vault_subdir`, BOO-82). Four defaults (from the reference implementation):

```json
{
  "version": 1,
  "tracked_paths": [
    { "glob": "docs/components/*.md",            "type": "component",    "default_vault_subdir": "02 Projekte/{project_slug}/Components/" },
    { "glob": "docs/decisions/*.md",             "type": "decision",     "default_vault_subdir": "02 Projekte/{project_slug}/Decisions/" },
    { "glob": "docs/architecture-guidelines.md", "type": "architecture", "default_vault_subdir": "02 Projekte/{project_slug}/" },
    { "glob": "journal/sprint-*.md",             "type": "sprint-retro", "default_vault_subdir": "04 Ressourcen/{project_slug}/sprints/" }
  ]
}
```

- `type:` is only set when the source file does not have one yet (sprint retros bring their own `type:`).
- `default_vault_subdir` (BOO-82) carries the **default vault layout in the team contract** — so each operator no longer has to repeat the same paths in their `local.json`. The placeholders `{project_slug}` and `{slug}` are both replaced with the slug from `local.json`. Only the file name lands in the default subfolder.

This file is **versioned** (committed) — it is the team contract everyone agrees on.

## Building block 2 — personal config `.vault-sync/local.json` (gitignored)

Per operator, **never commit** (belongs in `.gitignore`). Schema:

```json
{
  "vault_path": "/Users/<operator>/Obsidian/<vault>",
  "project_slug": "<project-slug>",
  "path_mappings": {},
  "last_sync_commit": "<sha>",
  "enabled": true,
  "mode": "auto"
}
```

- `path_mappings` is, since BOO-82, an **optional override**, no longer a required field. Leave it empty (`{}`) = the vault target comes from the team contract's `default_vault_subdir`. Only operators who want to deviate add a prefix mapping here, e.g. `{ "docs/components": "My Folder/{slug}/Components" }`. On multiple matches the longest prefix wins; a matching `path_mappings` always beats the contract default.
- `mode`: `auto` (mirror silently) | `dry-run` (show only) | `ask` (ask per file).
- `enabled: false` disables the harvest for this operator without uninstalling.

## Building block 3 — mechanism (framework-native, BOO-77)

The engine lives in the framework under `bootstrap/references/vault-sync/` and is copied into the project by bootstrap option `[e]`:

- `scripts/install-vault-sync.sh` — interactive init per operator (`--force` / `--uninstall`), creates `local.json`, adds the `.gitignore` entry, symlinks the hook.
- `scripts/vault-sync.py` — sync engine (Python stdlib only, frontmatter merge with the `vault_sync_*` namespace, path-containment check, modes `auto`/`dry-run`/`ask`, reads the commit SHA directly from `.git/HEAD`).
- `.claude/hooks/post-merge.sh` — wrapper, symlinked into `.git/hooks/post-merge`, fires after each `git pull`. `exit 0` when there is no `local.json`.
- `.vault-sync/tracked-paths.json` — versioned team contract (see building block 1).

### Target resolution (BOO-82)

For each tracked file the engine determines the vault target in this order:

1. **`path_mappings` from `local.json`** — if a prefix matches (longest wins), per-operator override.
2. **`default_vault_subdir` from the team contract** — otherwise the team default; only the file name lands in it.
3. **no match** → the file is skipped (`SKIP`).

So the harvest works out of the box with an empty `path_mappings` but stays overridable per person.

### Incremental sync `--since <sha>` (BOO-82)

`python3 scripts/vault-sync.py --since <sha>` syncs only files changed since `<sha>` up to `HEAD` (`git diff --name-only <sha>..HEAD`). Faster than a full sync for large repos. If git is unavailable or the SHA is invalid, the engine falls back to a full sync with a warning (no silent data loss). The post-merge hook still uses the full sync — `--since` is for manual/optimized runs.

## Core rules

- **One-way repo → vault.** The sync never writes back to the vault.
- **Never modify the vault manually** where the sync writes — annotations go into `.notes.md` sidecar files the sync does not touch.
- **Frontmatter namespace `vault_sync_*`** (`vault_sync_project`, `vault_sync_path`, `vault_sync_commit`, `vault_sync_at`) — collision-free with source properties, filterable in Obsidian Bases.
- **Zero friction:** an operator without `local.json` → hook `exit 0` silently.
- **Delineation from DocSync (Block D.2):** DocSync is solo + bidirectional (vault ↔ repo). Vault harvest is team + one-way (repo → vault). In team mode therefore set **DocSync = no**.

## Activation in bootstrap

Bootstrap question B.3, option `[e] Repo docs + personal vault harvest`. Bootstrap copies the engine files into the project (`scripts/vault-sync.py`, `scripts/install-vault-sync.sh`, `.claude/hooks/post-merge.sh`, `.vault-sync/tracked-paths.json`), adds `.vault-sync/local.json` to `.gitignore`, sets Block D DocSync = no, and adds the onboarding step. Each operator then optionally enables the harvest with `bash scripts/install-vault-sync.sh` (default mode `dry-run`).

## Activating the vault harvest — step by step

Each operator does this **once per project clone** if they want to populate their personal vault. No one has to take part — without a `local.json` nothing happens (`exit 0`).

**Prerequisites:**
- The engine files are in the project (bootstrap option `[e]` ran, or in an existing project: `bash <skill-repo>/bootstrap/scripts/migrate-to-v2.sh --issue BOO-77`).
- Your Obsidian vault exists locally (you know the absolute path).

**1. Run the init** (in the project root):

```bash
bash scripts/install-vault-sync.sh
```

The script asks three things interactively:
- **Absolute path to your Obsidian vault** — e.g. `/Users/you/Obsidian/MyVault`.
- **Project slug** — folder name in the vault, e.g. `my-project`; replaces `{project_slug}` in the team contract.
- **Mode** — `dry-run` / `auto` / `ask` (default `dry-run`).

It then creates `.vault-sync/local.json` (gitignored), adds it to `.gitignore`, and symlinks the `post-merge` hook. (`--force` overwrites an existing `local.json`.)

**2. Check the dry run** — what would be mirrored?

```bash
python3 scripts/vault-sync.py --dry-run
```

Shows the planned vault target per file. The layout comes from the team contract's `default_vault_subdir`; only deviate by setting a `path_mappings` prefix in your `local.json`.

**3. Switch to real mirroring** — set `"mode": "auto"` in `.vault-sync/local.json` (or choose `auto` during init). `auto` = mirror silently, `ask` = confirm per file.

**4. Trigger** — `git pull` (the `post-merge` hook fires automatically). Manually any time: `python3 scripts/vault-sync.py`. For large repos, only changes since a commit: `python3 scripts/vault-sync.py --since <sha>`.

**5. Verify** — the mirrored files now sit in the vault (e.g. under `02 Projekte/<slug>/...`) with `vault_sync_*` frontmatter. Put your own notes ONLY in `.notes.md` sidecar files — the sync never touches those.

**Turn it off again:** `bash scripts/install-vault-sync.sh --uninstall` (removes the hook + `local.json`; the versioned team contract stays). Pause temporarily: `"enabled": false` in `local.json`.

## Phases

- **Phase 1 (BOO-75):** documentation + config scaffold + the bootstrap option as a documented choice.
- **Phase 2 (BOO-77, done):** **framework-native engine** under `bootstrap/references/vault-sync/` — bootstrap option `[e]` sets up the vault harvest fully. No external code needed. Smoke-tested (dry-run / real / path containment / disabled / no local.json).
- **Phase 3 (BOO-82, done):** convenience + scaling. `default_vault_subdir` in the team contract (default layout central instead of repeated per operator), `local.json path_mappings` as an optional override, incremental `--since <sha>` sync. Smoke-tested (default layout / override precedence / `--since` / containment / fallback on invalid SHA).

## Security

- One-way: writes ONLY into the vault, never into the repo.
- Path containment via `realpath`: every target must be inside `vault_path`, otherwise aborted (prevents `../` escape and symlink traversal).
- No network calls, no secrets, Python stdlib only.
- `local.json` is gitignored — the personal vault path never leaks into the repo.

## Source

Pattern impulse: operator feedback Stefan, 2026-05-27 (`StefanWeimarPRODOC/project-template`). Framework-native engine: BOO-77, operator decision Tobias 2026-05-28 (Stefan's code not needed). `default_vault_subdir` + incremental `--since` sync (BOO-82): two ideas adopted from Stefan's template, rebuilt framework-natively (operator decision 2026-05-28).
