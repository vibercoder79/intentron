# Release Notes - Wave R Multi-Projekt-Betrieb

> 🌐 **Sprache:** Deutsch (diese Datei) · [🇬🇧 English](wave-r-multi-project-operation.en.md)

Stand: 2026-05-28

## Zweck

Wave R (BOO-80) beantwortet "mehrere Projekte auf einer Maschine — pro Projekt bootstrappen, oder gibt es einen Basis-schon-da-Pfad?". HANDBUCH-Anhang U trennt Maschinen-Ebene (einmal) von Projekt-Ebene (jedes Mal) und beschreibt drei Onboarding-Wege. Reine Doku + Sketch.

## Betroffene Stories

- BOO-80 — HANDBUCH Anhang U Multi-Projekt-Betrieb

## Was Nutzer bekommen

- **HANDBUCH Anhang U** (DE+EN) mit Sketch `docs/assets/multi-project-onboarding.png`:
  - **Maschinen-Ebene (einmal):** System-Tools, globaler Skill-Pool, `~/.claude` — gilt fuer alle Projekte.
  - **Projekt-Ebene (jedes Mal):** CLAUDE.md, Git-Hooks (pro Repo!), environment.json, specs/, Doku-SSoT.
  - **Drei Onboarding-Wege:** (1) neues Projekt = voller `/bootstrap`; (2) Projekt 2..N = Bootstrap-Schnellpfad (Block B erkennt Basis → Phase 5 Skip, nur Projekt-Ebene); (3) bestehendes Projekt = bootstrap Merge-Modus + `migrate-to-v2.sh` (kein neuer Skill).
  - **Pro-Projekt-Minimal-Checkliste:** CLAUDE.md / Git-Hooks / environment.json / Doku-SSoT / verify-setup.sh.

## Designentscheid

Existing-Project-Onboarding bleibt ein **dokumentierter Pfad** (bootstrap Merge-Modus + migrate-to-v2.sh), **kein neuer Skill** — die Mechanik existiert bereits, ein Skill waere Doppelung. Damit bleibt das Framework leichtgewichtig.

## Konkrete Aenderungen

| Bereich | Datei |
|---|---|
| HANDBUCH Anhang U (DE+EN) + Sketch | `HANDBUCH.md` + `HANDBUCH.en.md`, `docs/assets/multi-project-onboarding.png` |
| Migration | `migrate_boo_80` (Doku-only) in `bootstrap/scripts/migrate-to-v2.sh` |
| Migration-Checklist §BOO-80 (DE+EN) | `bootstrap/references/migration-checklist-v1-to-v2.md` + `.en.md` |
| Spec | `specs/BOO-80.md` |

## Skill-Versions-Bumps

- keine (reine Doku)

## Verweise

- Spec: `specs/BOO-80.md`
- HANDBUCH Anhang U, Anhang S (was einmal vs pro Projekt), Anhang T (verify)
- Operator-Frage: Tobias, 2026-05-28
- Linear: BOO-80
