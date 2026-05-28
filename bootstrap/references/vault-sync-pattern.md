# Vault-Harvest-Pattern — Config-Scaffold + framework-native Engine (BOO-75/77)

Repo-Docs + persoenlicher Vault-Harvest fuer Multi-Person-Teams mit Obsidian-Nutzern. Dieses Dokument beschreibt den Daten-Vertrag und die Mechanik. Die **Sync-Engine ist seit BOO-77 framework-nativ** — sie liegt unter `bootstrap/references/vault-sync/` (`vault-sync.py`, `install-vault-sync.sh`, `post-merge.sh`, `tracked-paths.json`) und wird von Bootstrap-Option `[e]` direkt ins Projekt kopiert. Kein externer Code, keine Dependencies (Python-Stdlib + Bash). Stefans `project-template` war der Pattern-Impuls, ist aber **nicht** die Quelle der Engine.

> **Schwesterdatei (Englisch):** [`vault-sync-pattern.en.md`](./vault-sync-pattern.en.md)
> **HANDBUCH-Hintergrund:** Anhang R Layer 3 (Vault-Harvest-Pattern, 2-Fluss-Modell).

## Wann dieses Pattern?

Ein Team arbeitet am selben GitHub-Repo (Doku lebt in `docs/`), **und** einzelne Operatoren wollen projektuebergreifende Insights weiterhin im persoenlichen Obsidian-Vault sehen. Obsidian ist ein Solo-Werkzeug — es gibt keinen geteilten Team-Vault. Das Pattern loest das ueber zwei getrennte Fluesse:

- **Fluss 1 (normales Git, alle, bidirektional):** `docs/` ↔ GitHub-Repo via `git push`/`git pull`. Team-SSoT.
- **Fluss 2 (Harvest, pro Person, einseitig):** `git post-merge`-Hook kopiert ausgewaehlte `docs/`-Dateien in den persoenlichen Vault — nie zurueck.

## Baustein 1 — Team-Vertrag `.vault-sync/tracked-paths.json` (versioniert)

Definiert, welche Repo-Pfade harvest-bar sind und welches `type:`-Frontmatter beim Mirror in den Vault ergaenzt wird. Vier Defaults (aus der Referenz-Implementierung):

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

`type:` wird nur gesetzt, wenn die Quelldatei noch keinen hat (Sprint-Retros bringen ihren eigenen `type:` mit). Diese Datei ist **versioniert** (committed) — sie ist der Team-Vertrag, worauf sich alle einigen.

## Baustein 2 — Persoenliche Konfig `.vault-sync/local.json` (gitignored)

Pro Mitarbeiter, **niemals committen** (gehoert in `.gitignore`). Schema:

```json
{
  "vault_path": "/Users/<operator>/Obsidian/<vault>",
  "project_slug": "<projekt-slug>",
  "path_mappings": {
    "docs/components": "02 Projekte/{slug}/Components",
    "journal": "04 Ressourcen/{slug}/sprints"
  },
  "last_sync_commit": "<sha>",
  "enabled": true,
  "mode": "auto"
}
```

- `path_mappings` PARA-konform: `02 Projekte/{slug}/...` fuer Komponenten/Decisions, `04 Ressourcen/{slug}/sprints/` fuer Sprint-Retros.
- `mode`: `auto` (still mirroren) | `dry-run` (nur anzeigen) | `ask` (pro Datei fragen).
- `enabled: false` deaktiviert den Harvest fuer diesen Operator ohne Deinstallation.

## Baustein 3 — Mechanik (framework-native, BOO-77)

Die Engine liegt im Framework unter `bootstrap/references/vault-sync/` und wird von Bootstrap-Option `[e]` ins Projekt kopiert:

- `scripts/install-vault-sync.sh` — interaktives Init pro Mitarbeiter (`--force` / `--uninstall`), legt `local.json` an, traegt `.gitignore`-Eintrag ein, symlinkt den Hook.
- `scripts/vault-sync.py` — Sync-Engine (Python-Stdlib-only, Frontmatter-Merge mit `vault_sync_*`-Namespace, Pfad-Containment-Check, Modi `auto`/`dry-run`/`ask`, liest Commit-SHA direkt aus `.git/HEAD`).
- `.claude/hooks/post-merge.sh` — Wrapper, via Symlink in `.git/hooks/post-merge`, feuert nach jedem `git pull`. `exit 0` wenn keine `local.json`.
- `.vault-sync/tracked-paths.json` — versionierter Team-Vertrag (siehe Baustein 1).

## Kernregeln

- **Einseitig Repo → Vault.** Der Vault wird NIE vom Sync zurueckgeschrieben.
- **Vault nie manuell veraendern,** wo der Sync hinschreibt — Annotationen laufen ueber `.notes.md`-Schwesterdateien, die der Sync nicht anfasst.
- **Frontmatter-Namespace `vault_sync_*`** (`vault_sync_project`, `vault_sync_path`, `vault_sync_commit`, `vault_sync_at`) — kollisionsfrei mit Quell-Properties, in Obsidian-Bases filterbar.
- **Null Reibung:** Mitarbeiter ohne `local.json` → Hook `exit 0` stillschweigend.
- **Abgrenzung DocSync (Block D.2):** DocSync ist solo + bidirektional (Vault ↔ Repo). Vault-Harvest ist team + einseitig (Repo → Vault). Im Team-Modus daher **DocSync = nein** setzen.

## Aktivierung im Bootstrap

Bootstrap-Frage B.3, Option `[e] Repo-Docs + persoenlicher Vault-Harvest`. Bootstrap kopiert die Engine-Files ins Projekt (`scripts/vault-sync.py`, `scripts/install-vault-sync.sh`, `.claude/hooks/post-merge.sh`, `.vault-sync/tracked-paths.json`), traegt `.vault-sync/local.json` in `.gitignore` ein, setzt Block D DocSync = nein und ergaenzt den Onboarding-Schritt. Danach aktiviert jeder Mitarbeiter den Harvest optional mit `bash scripts/install-vault-sync.sh` (Default-Modus `dry-run`).

## Phasen

- **Phase 1 (BOO-75):** Dokumentation + Config-Scaffold + Bootstrap-Option als dokumentierte Wahl.
- **Phase 2 (BOO-77, done):** **framework-native Engine** unter `bootstrap/references/vault-sync/` — Bootstrap-Option `[e]` richtet das Vault-Harvest vollstaendig ein. Kein externer Code noetig. Smoke-getestet (dry-run / real / Pfad-Containment / disabled / keine local.json).

## Sicherheit

- Einseitig: schreibt NUR in den Vault, nie ins Repo.
- Pfad-Containment via `realpath`: jedes Ziel muss innerhalb `vault_path` liegen, sonst Abbruch (verhindert `../`-Ausbruch und Symlink-Traversal).
- Keine Netzwerk-Calls, keine Secrets, Python-Stdlib-only.
- `local.json` ist gitignored — der persoenliche Vault-Pfad leakt nie ins Repo.

## Quelle

Pattern-Impuls: Operator-Feedback Stefan, 2026-05-27 (`StefanWeimarPRODOC/project-template`). Framework-native Engine: BOO-77, Operator-Entscheidung Tobias 2026-05-28 (Stefans Code nicht benoetigt).
