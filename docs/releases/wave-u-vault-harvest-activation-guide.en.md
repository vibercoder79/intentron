# Release Notes - Wave U Vault Harvest Activation Guide

> 🌐 **Language:** English (this file) · [🇩🇪 Deutsch](wave-u-vault-harvest-activation-guide.md)

Status: 2026-05-28 · **v0.2.1 line** (first docs polish after the v0.2.0 release)

## Purpose

Operator question: "Is it sufficiently described HOW to run `install-vault-sync.sh`?" — **No.** The docs explained the **What** and **Why** of the vault harvest well (pattern, security, team contract), but the **How** of carrying it out was just a one-liner (*"activate with `bash scripts/install-vault-sync.sh` (default dry-run)"*). A continuous operator walkthrough was missing.

This wave closes the execution gap — the same kind of gap as previously with Codex (Appendix J): reference present, walkthrough missing.

## What Is Now There

**`vault-sync-pattern.md` (DE+EN), new section "Activate Vault Harvest — step by step":**

1. **Prerequisites** — engine files in the project (bootstrap `[e]` or `migrate --issue BOO-77`), vault exists locally.
2. **Run init** — `bash scripts/install-vault-sync.sh` with the **three interactive prompts** (vault path, project slug, mode) explicitly named.
3. **Check dry run** — `python3 scripts/vault-sync.py --dry-run`, layout from `default_vault_subdir` vs. `path_mappings` override.
4. **Switch to `auto`** — `"mode": "auto"` in `local.json` (previously the dry-run→auto explanation was missing entirely).
5. **Trigger** — `git pull` (hook) / manual / `--since <sha>` for large repos.
6. **Verify** — mirrored files with `vault_sync_*` frontmatter; notes only in `.notes.md`.
7. **Disable** — `--uninstall` or `"enabled": false`.

**HANDBUCH Appendix R (DE+EN):** reference sentence in the activation paragraph pointing to the new walkthrough.

## Concrete Changes

| Area | Change | File |
|---|---|---|
| Config scaffold | New step-by-step section (DE) | `bootstrap/references/vault-sync-pattern.md` |
| Config scaffold | Same section (EN) | `bootstrap/references/vault-sync-pattern.en.md` |
| HANDBUCH Appendix R | Reference sentence to the walkthrough (DE) | `HANDBUCH.md` |
| HANDBUCH Appendix R | ditto (EN) | `HANDBUCH.en.md` |

## No Code Change

Pure docs. The engine (`vault-sync.py`, `install-vault-sync.sh`, `post-merge.sh`, `tracked-paths.json`) stays unchanged. No version bump.

## Follow-up Item

The **real end-to-end test** (real project against a real Obsidian vault, not just a `/tmp` smoke test) stays open — but the walkthrough now provides the step-by-step template against which it can be run through.

## References

- Config scaffold: `bootstrap/references/vault-sync-pattern.md` §"Activate Vault Harvest — step by step"
- HANDBUCH: Appendix R Layer 3 (Vault Harvest)
- Engine + pattern: BOO-77, BOO-82
- Operator feedback: Tobias, 2026-05-28
