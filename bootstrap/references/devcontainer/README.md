# Code-Crash Container-Profil (optional) — BOO-81

Reproduzierbare Toolchain im Container. **Optional** — der Default-Pfad bleibt System-Install (siehe HANDBUCH Anhang S). Dieses Profil ist fuer **Team-Setups** gedacht, wo "Tools einmal installieren" portabel und identisch fuer alle Operatoren sein soll.

## Wann nutzen?

| Situation | Empfehlung |
|-----------|------------|
| Solo-Operator, ein Mac | **System-Install** (Anhang S) — Container ist Overkill |
| Team, alle sollen identische Linter-Versionen haben | **Container** — kein "works on my machine" |
| Multi-User-VPS | meist globaler System-Pool (Anhang P Szenario 3); Container nur wenn Tool-Isolation pro User gewuenscht |
| CI | Container-Image als CI-Base wiederverwendbar |

## Was drin ist

- Node (LTS) + Python — Basis fuer JS/TS- und Python-Projekte
- `semgrep`, `ruff` (via pipx, isoliert), globales `eslint`, `jq`, `git`
- VS-Code-Extensions: ESLint, Ruff, Claude Code
- `postCreateCommand` ruft `generate-environment-json.sh`, damit die Skills die Container-Tools erkennen

## Nutzung

1. `.devcontainer/devcontainer.json` + `.devcontainer/Dockerfile` ins Projekt kopieren (Bootstrap-Option oder `migrate_boo_81`).
2. In VS Code: "Reopen in Container". Oder CLI: `devcontainer up --workspace-folder .`.
3. Im Container `bash scripts/verify-setup.sh` (Anhang T) → Toolchain-Checks gruen.

## Tradeoff

- **Pro:** identische, reproduzierbare Toolchain; kein lokales Tool-Setup; CI-wiederverwendbar.
- **Contra:** Docker-Abhaengigkeit; Image-Build-Zeit; fuer Solo-Operatoren unnoetiger Overhead.

## Anpassen

Tools im `Dockerfile` ergaenzen/entfernen wie es das Projekt braucht (z.B. SonarScanner, Go, Rust). Die Skills lesen `.claude/environment.json` — nach Tool-Aenderung `bash .claude/generate-environment-json.sh --force` laufen lassen.

Quelle: BOO-81, Operator-Entscheidung Tobias 2026-05-28 (System-Install Default, Container optional).
