# BOO-77 — Framework-native Vault-Sync-Engine (Bootstrap [e] richtet Vault-Harvest komplett ein)

## Summary

Folge zu BOO-75 (Vault-Harvest Phase 1, dokumentierte Wahl). Statt Stefans Code zu vendoren (Blocker: Repo nicht zugaenglich), baut das Framework eine **eigene schlanke Sync-Engine** unter `bootstrap/references/vault-sync/`. Bootstrap-Option `[e]` richtet damit das Vault-Harvest **vollstaendig** ein (nicht nur dokumentiert). Python-Stdlib + Bash, keine Dependencies, kein externer Code.

## Why

Operator-Entscheidung (Tobias, 2026-05-28, AskUserQuestion): Stefans Code wird nicht gebraucht. Bei Wahl `[e]` soll Bootstrap das Setup wirklich einrichten, nicht nur auf ein Nachbar-Repo verweisen. Loest den Phase-2-Blocker (`StefanWeimarPRODOC/project-template` nicht zugaenglich) durch eine framework-native Implementierung des in BOO-75 dokumentierten Patterns.

## What

Vier Engine-Files unter `bootstrap/references/vault-sync/`:

- **`vault-sync.py`** — einseitige Sync-Engine Repo→Vault. Liest `.vault-sync/tracked-paths.json` (Team-Vertrag) + `.vault-sync/local.json` (pro Mitarbeiter, gitignored). Frontmatter-Merge mit `vault_sync_*`-Namespace (idempotent), `type:`-Injektion nur wenn Quelle keinen hat. Modi `auto` / `dry-run` / `ask`. Liest Commit-SHA direkt aus `.git/HEAD` (kein Subprozess-Zwang). Ueberspringt `.notes.md`-Sidecars.
- **`install-vault-sync.sh`** — interaktives Init pro Mitarbeiter (`--force` / `--uninstall`), legt `local.json` an, traegt `.gitignore`-Eintrag ein, symlinkt den Hook.
- **`post-merge.sh`** — Hook-Wrapper, feuert nach `git pull`, `exit 0` wenn keine `local.json` (null Reibung) oder kein python3.
- **`tracked-paths.json`** — versionierter Team-Vertrag, 4 Defaults.

Bootstrap Block B.3 Option `[e]` (DE+EN) kopiert die Files ins Projekt (`scripts/` + `.claude/hooks/` + `.vault-sync/`), traegt `.gitignore` ein, setzt DocSync=nein, ergaenzt Onboarding-Schritt. Bootstrap v3.30.0 → v3.31.0.

## Sicherheits-Posture (umgesetzt + getestet)

- **Einseitig:** schreibt NUR in den Vault, NIE ins Repo.
- **Pfad-Containment:** jedes Vault-Ziel wird via `realpath` gegen `vault_path` geprueft — `../`-Ausbruch und Symlink-Traversal werden blockiert (Smoke-Test T3 bestaetigt).
- **Dry-run-Default** in der `local.json`-Vorlage (`mode: dry-run`).
- **Keine Secrets, keine Netzwerk-Calls, Python-Stdlib-only.**
- **security-architect REVIEW** (manuell): einseitiger Datenfluss, Path-Containment, kein eval/exec, kein Shell-Injection-Vektor (Pfade werden als Path-Objekte behandelt, nicht in Shell interpoliert). Keine Findings.

## Validation (Smoke-Test, 5 Faelle gruen)

1. **dry-run:** plant 3 Dateien, schreibt 0 (Vault leer). ✓
2. **real (auto):** spiegelt 3 Dateien an korrekte PARA-Pfade; `title:` bleibt erhalten, `type:` nur injiziert wenn fehlend, `vault_sync_*` ergaenzt. ✓
3. **Containment:** `path_mapping` mit `../outside/leak` → BLOCK, 0 Dateien ausserhalb des Vaults. ✓
4. **enabled=false:** still `exit 0`. ✓
5. **keine local.json:** still `exit 0` (null Reibung). ✓
6. **`.notes.md`-Sidecar** wird nicht gesynct. ✓

## Acceptance Criteria

- [x] 4 Engine-Files unter `bootstrap/references/vault-sync/`
- [x] Lokaler Smoke-Test (dry-run / real / Containment / disabled / no-config / sidecar)
- [x] Bootstrap Block B.3 `[e]` generiert die Files + .gitignore + Hook-Symlink (DE+EN), v3.31.0
- [x] HANDBUCH Anhang R Layer 3 + `vault-sync-pattern.md` auf framework-native umgestellt (DE+EN)
- [x] security-architect REVIEW dokumentiert (keine Findings)
- [x] Spec + Release Notes + Migration + v0.2.0-overview

## Constraints

- Reine Stdlib (Python) + Bash, keine externen Dependencies (laeuft auf Mac + Linux/VPS).
- Master der Engine ist das Framework-Repo selbst (kein Mirror noetig — eigener Code, anders als BOO-74).

## Dependencies

- BOO-75 (Pattern + Scaffold + Bootstrap-Option). Macht den dort dokumentierten "Phase 2 = Vendoring von Stefans Code"-Pfad obsolet (framework-native statt vendored).

## Session-Referenz

Spec + Umsetzung Session 2026-05-28. Operator-Entscheidung Tobias (framework-native statt Stefan-Code). Linear: <https://linear.app/owlist/issue/BOO-77/>
