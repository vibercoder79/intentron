# Vault-Harvest Pattern — Config Scaffold + framework-native engine (BOO-75/77)

Repo docs + personal vault harvest for multi-person teams with Obsidian users. This document describes the data contract and the mechanism. The **sync engine is framework-native since BOO-77** — it lives under `bootstrap/references/vault-sync/` (`vault-sync.py`, `install-vault-sync.sh`, `post-merge.sh`, `tracked-paths.json`) and is copied into the project by bootstrap option `[e]`. No external code, no dependencies (Python stdlib + Bash). Stefan's `project-template` was the pattern impulse but is **not** the source of the engine.

> **Sibling file (German):** [`vault-sync-pattern.md`](./vault-sync-pattern.md)
> **HANDBUCH background:** Appendix R Layer 3 (vault-harvest pattern, two-flow model).

## When to use this pattern

A team works on the same GitHub repo (docs live in `docs/`), **and** individual operators want to keep seeing cross-project insights in their personal Obsidian vault. Obsidian is a solo tool — there is no shared team vault. The pattern solves this via two separate flows:

- **Flow 1 (plain Git, all, bidirectional):** `docs/` ↔ GitHub repo via `git push`/`git pull`. Team SSoT.
- **Flow 2 (harvest, per person, one-way):** a `git post-merge` hook copies selected `docs/` files into the personal vault — never back.

## Building block 1 — team contract `.vault-sync/tracked-paths.json` (versioned)

Defines which repo paths are harvestable and which `type:` frontmatter is added when mirrored into the vault. Four defaults (from the reference implementation):

```json
{
  "tracked_paths": [
    { "glob": "docs/components/*.md",        "type": "component" },
    { "glob": "docs/decisions/*.md",         "type": "decision" },
    { "glob": "docs/architecture-guidelines.md", "type": "architecture" },
    { "glob": "journal/sprint-*.md",         "type": "sprint-retro" }
  ]
}
```

`type:` is only set when the source file does not have one yet (sprint retros bring their own `type:`). This file is **versioned** (committed) — it is the team contract everyone agrees on.

## Building block 2 — personal config `.vault-sync/local.json` (gitignored)

Per operator, **never commit** (belongs in `.gitignore`). Schema:

```json
{
  "vault_path": "/Users/<operator>/Obsidian/<vault>",
  "project_slug": "<project-slug>",
  "path_mappings": {
    "docs/components": "02 Projekte/{slug}/Components",
    "journal": "04 Ressourcen/{slug}/sprints"
  },
  "last_sync_commit": "<sha>",
  "enabled": true,
  "mode": "auto"
}
```

- `path_mappings` PARA-conform: `02 Projekte/{slug}/...` for components/decisions, `04 Ressourcen/{slug}/sprints/` for sprint retros.
- `mode`: `auto` (mirror silently) | `dry-run` (show only) | `ask` (ask per file).
- `enabled: false` disables the harvest for this operator without uninstalling.

## Building block 3 — mechanism (framework-native, BOO-77)

The engine lives in the framework under `bootstrap/references/vault-sync/` and is copied into the project by bootstrap option `[e]`:

- `scripts/install-vault-sync.sh` — interactive init per operator (`--force` / `--uninstall`), creates `local.json`, adds the `.gitignore` entry, symlinks the hook.
- `scripts/vault-sync.py` — sync engine (Python stdlib only, frontmatter merge with the `vault_sync_*` namespace, path-containment check, modes `auto`/`dry-run`/`ask`, reads the commit SHA directly from `.git/HEAD`).
- `.claude/hooks/post-merge.sh` — wrapper, symlinked into `.git/hooks/post-merge`, fires after each `git pull`. `exit 0` when there is no `local.json`.
- `.vault-sync/tracked-paths.json` — versioned team contract (see building block 1).

## Core rules

- **One-way repo → vault.** The sync never writes back to the vault.
- **Never modify the vault manually** where the sync writes — annotations go into `.notes.md` sidecar files the sync does not touch.
- **Frontmatter namespace `vault_sync_*`** (`vault_sync_project`, `vault_sync_path`, `vault_sync_commit`, `vault_sync_at`) — collision-free with source properties, filterable in Obsidian Bases.
- **Zero friction:** an operator without `local.json` → hook `exit 0` silently.
- **Delineation from DocSync (Block D.2):** DocSync is solo + bidirectional (vault ↔ repo). Vault harvest is team + one-way (repo → vault). In team mode therefore set **DocSync = no**.

## Activation in bootstrap

Bootstrap question B.3, option `[e] Repo docs + personal vault harvest`. Bootstrap copies the engine files into the project (`scripts/vault-sync.py`, `scripts/install-vault-sync.sh`, `.claude/hooks/post-merge.sh`, `.vault-sync/tracked-paths.json`), adds `.vault-sync/local.json` to `.gitignore`, sets Block D DocSync = no, and adds the onboarding step. Each operator then optionally enables the harvest with `bash scripts/install-vault-sync.sh` (default mode `dry-run`).

## Phases

- **Phase 1 (BOO-75):** documentation + config scaffold + the bootstrap option as a documented choice.
- **Phase 2 (BOO-77, done):** **framework-native engine** under `bootstrap/references/vault-sync/` — bootstrap option `[e]` sets up the vault harvest fully. No external code needed. Smoke-tested (dry-run / real / path containment / disabled / no local.json).

## Security

- One-way: writes ONLY into the vault, never into the repo.
- Path containment via `realpath`: every target must be inside `vault_path`, otherwise aborted (prevents `../` escape and symlink traversal).
- No network calls, no secrets, Python stdlib only.
- `local.json` is gitignored — the personal vault path never leaks into the repo.

## Source

Pattern impulse: operator feedback Stefan, 2026-05-27 (`StefanWeimarPRODOC/project-template`). Framework-native engine: BOO-77, operator decision Tobias 2026-05-28 (Stefan's code not needed).
