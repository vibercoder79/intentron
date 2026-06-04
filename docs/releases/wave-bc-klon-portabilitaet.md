# Wave BC — Klon-Portabilität für Multi-User (BOO-152)

**Was jetzt da ist:** Ein gebootstrapptes Projekt ist **klon-portabel** — die Voraussetzung, damit das Multi-User-VPS-Szenario (BOO-151) technisch sauber funktioniert. Vorher trugen `settings.json` + Hook-Scripts **absolute Pfade**; ein fremder Klon erbte die Pfade des Erstellers und die Hooks liefen ins Leere. Jetzt: Pfade über **`$CLAUDE_PROJECT_DIR`** (portabel) + ein **`install-hooks.sh`** für den nativen `pre-commit` + fertiger Onboarding-Prompt. DE+EN.

## Stories
- **BOO-152** — Klon-Portabilität: `$CLAUDE_PROJECT_DIR` in settings.json + Hook-Scripts, `scripts/install-hooks.sh` (`.githooks/` + `core.hooksPath`), Onboarding-Prompt, Checklisten-Update.

## Änderungen (DE+EN)
- **`bootstrap/SKILL.md`** (3.39.0 → **3.40.0**): settings.json-Hook-Commands → `$CLAUDE_PROJECT_DIR`; Phase 4.6 nativer `pre-commit` → `.githooks/` + `install-hooks.sh`.
- **`references/file-templates.md`:** `WORKSPACE` portabel (`${CLAUDE_PROJECT_DIR:-…}`); neue Sektion `scripts/install-hooks.sh`.
- **`docs/runbooks/multi-user-vps.md`:** fertiger Operator-Prompt für die Selbst-Einrichtung (Schritte C+D).
- **HANDBUCH Anhang U + Y:** Pro-Projekt-Checkliste Hook-Schritt = `install-hooks.sh`.

Alle Änderungen DE+EN-paritätisch.

## Wirkung
Ein neues Teammitglied richtet seinen Klon jetzt mit **einem** Befehl ein (`bash scripts/install-hooks.sh`), und die committete `settings.json` funktioniert in **jedem** Home unverändert — kein Pfad-Rewrite mehr nötig. Damit ist die BOO-151-Multi-User-Doku auch technisch gedeckt.

## Abgrenzung
Runtime-Hooks (`spec-gate`, `bodyguard`, …) kommen schon via `$CLAUDE_PROJECT_DIR` + committetem `.claude/` mit dem Klon. `install-hooks.sh` aktiviert nur den nativen `pre-commit`.

## Verweise
Spec: `specs/BOO-152.md`. Branch: `feat/boo-152-klon-portabilitaet`. Anknüpfung: BOO-151 (Multi-User-VPS), `docs/kollisionsschutz-drei-ebenen.md`. Operator-Quelle: Tobias, 2026-06-04.
