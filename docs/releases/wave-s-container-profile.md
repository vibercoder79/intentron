# Release Notes - Wave S Optionales Container-Profil

Stand: 2026-05-28

## Zweck

Wave S (BOO-81) gibt dem Framework ein **optionales** Container-Profil fuer die Toolchain — fuer Team-Setups, die eine identische, reproduzierbare Toolchain wollen. **System-Install bleibt der Default** (Code-Crash-Leichtgewicht-Prinzip); der Container ist opt-in.

## Hintergrund: die Container-Entscheidung

Operator (Tobias, 2026-05-28) wollte das Tools-/Container-Setup geklaert. Wichtige Klarstellung: **vorher gab es keine Container-Entscheidung im Repo.** Per AskUserQuestion getroffen: **System-Install Default, Container als optionales Profil dokumentieren** — nicht erzwingen.

## Betroffene Stories

- BOO-81 — optionales devcontainer + Dockerfile-Template + HANDBUCH Anhang S Container-Sektion

## Was Nutzer bekommen

- **`bootstrap/references/devcontainer/Dockerfile`** — schlankes Debian-base (Node LTS + Python) mit Semgrep, Ruff (via pipx), globalem ESLint, jq, git.
- **`bootstrap/references/devcontainer/devcontainer.json`** — VS-Code/CLI-DevContainer; `postCreateCommand` ruft `generate-environment-json.sh`, sodass die Skills die Container-Tools erkennen; Extensions ESLint/Ruff/Claude Code.
- **`bootstrap/references/devcontainer/README.md`** — wann nutzen (Solo=nein, Team/CI=ja), Nutzung, Tradeoff.
- **HANDBUCH Anhang S Sektion "Container-Profil (optional)"** (DE+EN): System-Install-vs-Container-Tabelle, Opt-in-Entscheid.
- **`migrate_boo_81`** kopiert `.devcontainer/` ins Projekt (opt-in, idempotent).

## Designentscheid

System-Install bleibt der Default. Container ist **opt-in**, kein neuer Pflicht-Bootstrap-Schritt. Pro: identische Toolchain fuer alle, CI-wiederverwendbar. Contra: Docker-Abhaengigkeit, Build-Zeit — fuer Solo-Operatoren Overkill.

## Konkrete Aenderungen

| Bereich | Datei |
|---|---|
| Container-Template NEU | `bootstrap/references/devcontainer/` (Dockerfile, devcontainer.json, README.md) |
| HANDBUCH Anhang S §Container-Profil (DE+EN) | `HANDBUCH.md` + `HANDBUCH.en.md` |
| Migration | `migrate_boo_81` (opt-in) in `bootstrap/scripts/migrate-to-v2.sh` |
| Migration-Checklist §BOO-81 (DE+EN) | `bootstrap/references/migration-checklist-v1-to-v2.md` + `.en.md` |
| Spec | `specs/BOO-81.md` |

## Skill-Versions-Bumps

- keine (Template + Doku, kein Skill-Code-Change)

## Verweise

- Spec: `specs/BOO-81.md`
- Template: `bootstrap/references/devcontainer/`
- HANDBUCH Anhang S §Container-Profil
- Operator-Entscheidung: Tobias, 2026-05-28
- Linear: BOO-81
