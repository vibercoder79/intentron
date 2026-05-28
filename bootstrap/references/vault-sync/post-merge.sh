#!/usr/bin/env bash
# .git/hooks/post-merge — Vault-Harvest-Trigger (BOO-77).
# Feuert nach jedem `git pull`/`git merge`. Ruft die einseitige Sync-Engine.
# Fehlt python3 oder die local.json, beendet sich die Engine still mit exit 0
# (null Reibung fuer Mitarbeiter ohne Vault-Harvest).
set -euo pipefail
REPO_ROOT="$(git rev-parse --show-toplevel 2>/dev/null || pwd)"
command -v python3 >/dev/null 2>&1 || exit 0
python3 "${REPO_ROOT}/scripts/vault-sync.py" || true
exit 0
