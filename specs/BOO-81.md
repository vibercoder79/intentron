# BOO-81 — Optionales Container-Profil: devcontainer + Dockerfile-Template

## Summary

Optionales Container-Profil fuer die Toolchain unter `bootstrap/references/devcontainer/` (Dockerfile + devcontainer.json + README). Macht die "Tools einmal reproduzierbar"-Idee (Anhang S) portabel fuer Team-Setups — **ohne Docker-Zwang**. System-Install bleibt der Default. Plus HANDBUCH Anhang S Sektion "Container-Profil (optional)".

## Why

Operator (Tobias, 2026-05-28): Tools-/Container-Setup sauber beschreiben. AskUserQuestion-Entscheidung: **System-Install Default, Container optional dokumentieren** (Leichtgewicht-Prinzip). Klargestellt: vorher keine Container-Entscheidung im Repo. Container loest das "works on my machine" fuer Teams mit Versions-Gleichschritt.

## What

- **`bootstrap/references/devcontainer/Dockerfile`** — schlankes Debian-base mit Node (LTS) + Python, Semgrep + Ruff (pipx), globales ESLint, jq, git. Kommentiert, anpassbar.
- **`bootstrap/references/devcontainer/devcontainer.json`** — DevContainer-Definition, `postCreateCommand` ruft `generate-environment-json.sh`, VS-Code-Extensions (ESLint/Ruff/Claude Code).
- **`bootstrap/references/devcontainer/README.md`** — wann nutzen (Solo=nein, Team/CI=ja), Nutzung, Tradeoff.
- **HANDBUCH Anhang S Sektion "Container-Profil (optional)"** (DE+EN): System-Install vs Container Tabelle, Opt-in-Entscheid.
- **`migrate_boo_81`** kopiert `.devcontainer/` ins Projekt (idempotent, opt-in).

## Constraints

- **System-Install bleibt Default.** Container opt-in, kein neuer Pflicht-Bootstrap-Schritt.
- Nur real existierende Tools im Dockerfile (Semgrep, Ruff, ESLint, jq, Node, Python).
- DE+EN fuer HANDBUCH-Sektion.

## Validation

- `devcontainer.json` ist gueltiges JSON (python json.load). ✓
- `migrate_boo_81 --dry-run` zeigt korrekten Kopier-Plan. ✓
- Image-Build selbst nicht ausgefuehrt (kein Docker im Verifikations-Kontext) — Dockerfile nutzt etabliertes `mcr.microsoft.com/devcontainers/base:debian` + Standard-Installationswege (apt, pipx, npm -g).

## Acceptance Criteria

- [x] `bootstrap/references/devcontainer/` mit Dockerfile + devcontainer.json + README
- [x] HANDBUCH Anhang S Sektion "Container-Profil (optional)" (DE+EN)
- [x] migrate_boo_81 + Migration-Checklist (DE+EN)
- [x] Release Notes + v0.2.0-overview

## Dependencies

- Anhang S (BOO-76, Toolchain-Verortung), Anhang P (BOO-70, Deployment-Szenarien), generate-environment-json.sh (BOO-34).

## Session-Referenz

Session 2026-05-28. Operator-Entscheidung Tobias (System-Install Default, Container optional). Linear: <https://linear.app/owlist/issue/BOO-81/>
