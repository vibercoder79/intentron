# Wave AT — Bootstrap-UX-Härtung (BOO-114/115/117/120/123/127)

**Was jetzt da ist:** der Bootstrap-Flow prüft Voraussetzungen *vorab* (statt am Ende), führt bei fehlenden Tools profil-abhängig auf die richtige Install-Anleitung, ist stack-/framework-/TypeScript-bewusst und verankert `gh` (GitHub CLI) als saubere Voraussetzung mit Connect-Runbook. Erstes Bündel der Probelauf-Folge-Stories (BKO, 2026-06-02).

## Stories
- **BOO-114** — Phase-0 **Pre-Flight-Gate** mit kontrolliertem Abbruch (Voraussetzungs-Check vor jedem Scaffold).
- **BOO-115** — **Tool-Install-Führung** mit HANDBUCH-Deeplinks + **profil-abhängiger Install-Default** (System vs. Docker aus `deployment_scenario`).
- **BOO-117** — Block-A **Bestands-Quellen-Import** (Intent/Repo/Doku → `PROJECT_DESC` vorbefüllen).
- **BOO-120** — `intent` ins **Minimum**-Skill-Set (Pipeline-Einstieg) + `migrate_boo_120`.
- **BOO-123** — `gh` als **Voraussetzung** (HANDBUCH §3/Anhang A) + **Golden Image** (Dockerfile) + **GitHub-Connect-Runbook** (gh-auth ≠ git-auth) + Branch-Protection-Fallback.
- **BOO-127** — **Guided Stack-Discovery** + framework-aware Stack-Optionen + **TypeScript-first** (`tsconfig`, `typescript-eslint`, `tsc --noEmit`-Gate).

## Änderungen (DE+EN)
- **`bootstrap/SKILL.md`:** Phase 0 → `0.1 Briefing` + `0.2 Pre-Flight-Gate`; A.1 framework-aware + TS-Wahl + `A.1a Guided-Discovery`; neuer `A.2b Bestands-Quellen-Import`; A.7 leitet `INSTALL_DEFAULT` ab; Phase 7.3b Tool-Install-Führung; 4.4 TS-Branch + Typecheck-Gate; 4.4k Branch-Protection-Fallback + Sonar-Entkopplung; Skill-Auswahl: `intent` im Minimum; 7.6 proaktiver GitHub-Connect.
- **`HANDBUCH.md`:** §3 `gh` in Pflichtliste + Zwei-Auth-Ebenen-Callout; Anhang A `gh`-Checkliste; Anhang Y.2 `gh`-apt-Repo-Block + GitHub-Connect-Runbook; §6 Minimum-Set (+ `intent`).
- **`references/`:** `file-templates.md` (+ `tsconfig.json` + `tsc --noEmit Typecheck`), `info-gathering.md` (`SOURCE_IMPORT`), `skills-setup.md` (`intent` = Minimum), `migration-checklist-v1-to-v2.md` (`migrate_boo_120`).
- **`bootstrap/references/devcontainer/Dockerfile`:** `gh` via offizielles GitHub-apt-Repo (Golden Image).

## Leichtgewicht-Prinzip
Keine Content-Duplikation: BOO-115 deeplinkt auf bestehende HANDBUCH-Anker (Y.2 / Container-Profil) statt Install-Sequenzen zu kopieren. BOO-127 erhält das Buchstaben-Mapping `a–e` → keine Regression in den STACK_CHOICE-Folgephasen.

## Verweise
Specs: `specs/BOO-114.md`, `BOO-115.md`, `BOO-117.md`, `BOO-120.md`, `BOO-123.md`, `BOO-127.md`. Branch: `feat/boo-bootstrap-flow-hardening`.
