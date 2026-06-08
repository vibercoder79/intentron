# Release Notes - Wave P README-Aktualisierung + Toolchain-Doku

> 🌐 **Sprache:** Deutsch (diese Datei) · [🇬🇧 English](wave-p-readme-and-toolchain-doc.en.md)

Stand: 2026-05-28

## Zweck

Wave P (BOO-78) ist eine Doku-Korrektur-Welle: die README war nach den Waves J-O nicht mehr auf Stand, und die wiederkehrende Toolchain-Frage ("muss ich Linter/Tools/Hooks pro Projekt oder einmal installieren?") hatte keinen dokumentierten Ort.

## Betroffene Stories

- BOO-78 — README v0.2.0-Stand + Anhang S Toolchain-Sektion

## Was korrigiert wurde

### README (EN+DE)

- **`dpo` + `security-architect` als Framework-Bundle-Skills** gelistet (eigene Tabelle "Specialist bundle skills", vendored seit BOO-74) — vorher fehlte `dpo` ganz und `security-architect` stand faelschlich als externer Companion-Skill (`../security-architect/`).
- **HANDBUCH-Beschreibung aktualisiert:** Split in `HANDBUCH.md` (DE, ~190 KB) + `HANDBUCH.en.md` (EN, ~165 KB), Anhaenge A-S benannt (vorher "bilingual, ~95 KB").
- **"Was ist neu (v0.2.0)"-Verweis** auf `docs/releases/v0.2.0-overview.md`.
- **Governance-Gates-Liste ergaenzt:** sensitive-paths (BOO-18), personal-data-paths (BOO-69), post-merge Vault-Harvest (BOO-77) — vorher nur spec-gate + doc-version-sync.
- **"Operating at scale / Im Team"-Hinweis** auf Anhaenge P/Q/R/S/O.

### HANDBUCH Anhang S — neue Sektion "Was einmal installieren, was pro Projekt?"

Beantwortet die Toolchain-Frage mit einer Matrix:

| Komponente | Einmal | Pro Projekt |
|---|---|---|
| System-Linter/Tools (Semgrep, Ruff, global ESLint) | ✅ einmal pro Maschine | — |
| Projekt-Dev-Deps (eslint/prettier in package.json) | — | ✅ npm install pro Projekt |
| Skills (globaler Pool) | ✅ einmal | nur bei Audit-Pinning |
| **Git-Hooks** (spec-gate, doc-version-sync, post-merge) | ❌ | ✅ **pro Repo** (`.git/hooks/` wird nicht geklont) |
| environment.json | — | ✅ pro Projekt (Manifest) |

**Kern-Korrektur:** Git-Hooks sind **pro Repo**, nicht einmal — `.git/` wird nicht geklont. Bootstrap installiert sie pro Projekt; Ausnahme `core.hooksPath` global.

## Konkrete Aenderungen

| Bereich | Datei |
|---|---|
| README EN+DE | `README.md` |
| HANDBUCH Anhang S Toolchain-Sektion (DE+EN) | `HANDBUCH.md` + `HANDBUCH.en.md` |
| Spec | `specs/BOO-78.md` |

## Skill-Versions-Bumps

- keine (reine Doku, kein Skill-Code-Change)

## Noch offen / Folgepunkte (aus der Diskussion 2026-05-28)

Operator-Themen, die als eigene Stories anstehen:

- **Multi-Projekt-Onboarding:** wie ein zweites/drittes Projekt auf einer Maschine aufsetzen, wenn die Basis (Tools, Skills) schon installiert ist — leichtgewichtiger pro-Projekt-Pfad vs. vollem Bootstrap. Braucht Doku + Sketch.
- **Projekt-Verification-Checkliste:** "Framework installiert — jetzt der Proof, dass alles funktioniert" (Linter da, Hooks feuern, Skills schreiben Artefakte, Artefakte existieren). Doku-Checkliste + ggf. automatisierender Skill.
- **Existing-Project-Onboarding-Skill:** ein bestehendes Projekt fuer INTENTRON vorbereiten.
- **Tools-/Container-Setup:** wie die Toolchain konkret eingebunden wird (Container-Entscheidung klaeren).

## Verweise

- Spec: `specs/BOO-78.md`
- README, HANDBUCH Anhang S
- Konsolidierter Ueberblick: `docs/releases/v0.2.0-overview.md`
- Operator-Beobachtung: Tobias, 2026-05-28
- Linear: BOO-78
