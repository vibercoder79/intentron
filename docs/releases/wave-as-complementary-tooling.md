# Wave AS — Komplementäres Tooling: setup-checklist (BOO-113)

**Was jetzt da ist:** die Best-Practice-Setup-Checkliste fuer Claude Code ist als eigenes oeffentliches Repo verfuegbar, und intentron verweist mit klarer Reihenfolge-Regel darauf.

## Stories
- **BOO-113** — setup-checklist als eigenes oeffentliches Repo + Verweis aus intentron.

## Aenderungen
- **Neues oeffentliches Repo:** https://github.com/vibercoder79/claude-code-setup-checklist (MIT, Skill im Root, DE+EN).
- **intentron README (DE+EN):** Abschnitt „Komplementäres Tooling — Maschinen-Setup" mit Link + Reihenfolge `global → /bootstrap → audit/additiv` + Faustregel.
- **HANDBUCH Anhang Z.4 (DE+EN):** derselbe Verweis + Regel.
- **Sync (ausserhalb intentron):** `publish_skill.py` um Fan-out erweitert — ein Publish schreibt nach `claudecodeskills` (privat) UND ins oeffentliche Repo; Skill-README traegt die Komplementaritaets-Notiz als Quelle.

## Reihenfolge-Regel
1. `setup-checklist global` — Maschinen-Best-Practice.
2. `/bootstrap` — Projekt-Governance (besitzt Projekt-CLAUDE.md + Hooks).
3. optional `setup-checklist audit`/`projekt` additiv (`.claudeignore`, `.gitignore`, `CLAUDE.local.md`).

Faustregel: Maschine + Hygiene = Checkliste · Projekt-Governance = bootstrap. Keine Datei doppelt.

## Verweise
Spec: `specs/BOO-113.md`. Release: v0.7.9.
