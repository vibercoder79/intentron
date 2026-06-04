# Global Registry Update — Neues Projekt registrieren

Nach dem Setup eines neuen Projekts werden diese Register-Stellen aktualisiert:

## 1. SecondBrain (Obsidian) — Projekt-Hub anlegen

**Nur wenn `OBSIDIAN_VAULT` in Block B gesetzt wurde.**

Pfad: `{OBSIDIAN_VAULT}/02 Projekte/{PROJECT_NAME}/`

Ordner-Struktur:
```
{OBSIDIAN_VAULT}/02 Projekte/{PROJECT_NAME}/
├── {PROJECT_NAME} - PMO HUB.md        ← Projekt-Hub mit Phase-Tabelle, Status, Referenzen
├── Architektur-Vorgaben.md            ← Skelett (wird bei /ideation gefuellt)
├── Components/                        ← lebende Doku pro Komponente (wenn Block C = ja)
├── Decisions/                         ← ADRs (wird beim ersten ADR gefuellt)
├── Meetings/                          ← Meeting-Protokolle
└── Research/                          ← Deep-Research-Outputs (/research)
```

**PMO HUB Template:**

```markdown
---
tags: [projekt, {{PROJECT_NAME_LOWER}}]
status: aktiv
phase: konzeption
erstellt: {{TODAY}}
aktualisiert: {{TODAY}}
language: {{PRIMARY_LANG}}
source: bootstrap
---

# {{PROJECT_NAME}} — PMO Hub

> {{PROJECT_DESC}}

## Projektziel

[Ein-Satz-Ziel — vom Operator zu verfeinern]

## Status

**Phase:** Konzeption → Phase 0

## Stack

Siehe `ARCHITECTURE_DESIGN.md` im Repo ({{GITHUB_REPO}}).

## Repositories & Code

| Was | Pfad / URL |
|-----|------------|
| GitHub Repo | {{GITHUB_REPO}} |
| Lokaler Pfad | `{{PROJECT_PATH}}` |
| Backlog | {{BACKLOG_URL}} |
| Issue-Prefix | `{{ISSUE_PREFIX}}` |

## Aktivierte Add-ons

{{ADDONS_LIST}}

## Installierte Skills

{{SKILLS_LIST}}

## Doku-Architektur (3 Schichten + Hub)

- **Hub (Repo):** `ARCHITECTURE_DESIGN.md` — zentraler Einstieg, §9 Referenzen
- **Story-Specs (Repo):** `specs/{{ISSUE_PREFIX}}XXX.md`
- **Component-Docs (Obsidian):** `Components/*.md`
- **Architektur-Vorgaben (Obsidian):** diese Seite → `Architektur-Vorgaben.md`

## Learning-Loop

Level: {{LEARNING_LOOP_LEVEL}}
Pfad: `{{PROJECT_PATH}}/journal/` + `04 Ressourcen/{{PROJECT_NAME}}/learnings.md` (Cross-Link)

## Offene Punkte

- [ ] Erste Story via /ideation
- [ ] ggf. Linear-Labels anpassen
- [ ] ggf. Obsidian-Projekt-Ordner mit Research fuellen

## Verknuepfungen

- [[Architektur-Vorgaben]]
- [[../../../../../04 Ressourcen/{{PROJECT_NAME}}/learnings]]
```

## 2. Projekt-Index (Obsidian)

**Nur wenn `OBSIDIAN_VAULT` gesetzt.**

Datei: `{OBSIDIAN_VAULT}/00 Kontext/Projekte.md`

Falls existiert: Zeile ergaenzen in der Projekt-Tabelle. Falls nicht: Datei anlegen mit Basis-Struktur.

```markdown
| {{PROJECT_NAME}} | [[02 Projekte/{{PROJECT_NAME}}/{{PROJECT_NAME}} - PMO HUB\|Hub]] | {{PROJECT_PATH}} | {{VERSION_START}} | aktiv |
```

## 3. Globale CLAUDE.md (optional)

**Nur wenn der Operator eine globale `~/.claude/CLAUDE.md` mit Projekt-Tabelle hat.**

Der Skill zeigt den neuen Eintrag vor:

```markdown
| **{{PROJECT_NAME}}** | `{{PROJECT_PATH}}` | {{GITHUB_REPO}} | {{OBSIDIAN_PROJECT_PATH}} |
```

Operator bestaetigt Einfuegepunkt. Skill schreibt dann die Zeile — oder zeigt sie zum manuellen Einfuegen.

### 3a. Standard-Projektpfad `PROJECTS_ROOT` (BOO-138)

Auf einer Maschine, die mehrere Projekte hostet (Developer-VPS), legt der Bootstrap **einmal** fest, wo Projekte standardmaessig liegen — und liest diesen Pfad danach bei jedem weiteren Bootstrap als Default vor. Das ist die Maschinen-Ebene-Voraussetzung fuer reibungsarmen Multi-Projekt-Betrieb (HANDBUCH Anhang U Weg 2).

**Lesen (jeder Bootstrap, Block B Frage 1):** Skill prueft `~/.claude/CLAUDE.md` auf einen `PROJECTS_ROOT`-Eintrag. Ist er gesetzt, wird Frage 1 mit `<PROJECTS_ROOT>/<projektname>` vorbelegt; Operator bestaetigt mit Enter oder ueberschreibt mit eigenem Pfad.

**Schreiben (nur erstes Projekt der Maschine):** Ist kein `PROJECTS_ROOT` hinterlegt, fragt der Skill einmalig und traegt ihn — nach Operator-Bestaetigung — in `~/.claude/CLAUDE.md` ein. Vorgeschlagener Block:

```markdown
## Projekt-Standardpfad

- `PROJECTS_ROOT`: `~/projects` — neue Projekte werden standardmaessig hier angelegt (`<PROJECTS_ROOT>/<projektname>`).
- Pro Projekt gilt die Standard-Struktur (PMO-Hub, `specs/`, `journal/daily/`, `docs/project/`) + die Session-Routinen aus der Projekt-`CLAUDE.md` (BOO-129/139).
```

Regeln: Operator-Bestaetigung Pflicht (kein stilles Schreiben); **kein Secret**; Override bleibt jederzeit moeglich (Operator kann ein Projekt bewusst ausserhalb `PROJECTS_ROOT` anlegen). Kein projektuebergreifendes Cockpit — der Tagesstand entsteht beim Oeffnen des jeweiligen Projekts (PMO-Hub + letzte `journal/daily/`-Notiz).

### 3b. Maschinen-Kontext (BOO-145)

Der Bootstrap schreibt am Ende von **Block A** (A.8) automatisch einen `## Maschinen-Kontext`-Abschnitt in die globale `~/.claude/CLAUDE.md` — **idempotent + ohne separaten Operator-Schritt**. Er gibt jeder KI-Session auf der Maschine sofort Orientierung (OS, Framework-Version, bevorzugter Stack, verfuegbare Skills). Zusammen mit `PROJECTS_ROOT` (§3a) bildet er den **Maschinen-Ebene-Kontext** der globalen `~/.claude/CLAUDE.md`.

**Lesen (jeder Bootstrap, A.8):** Skill prueft `~/.claude/CLAUDE.md` auf einen `## Maschinen-Kontext`-Abschnitt. Ist er vorhanden, **nichts tun** (nicht ueberschreiben — der Operator kann ihn frei anpassen).

**Schreiben (nur wenn der Abschnitt fehlt):** Werte ermitteln und anhaengen:

- **Typ:** `uname -s` → `Darwin` = `macOS`, `Linux` = `Linux` (Fallback `$OSTYPE`).
- **Framework-Version:** `git -C <intentron-repo> describe --tags --abbrev=0` (z.B. `v0.8.1`); Fallback `bootstrap`-Skill-Version.
- **Stack-Praeferenz:** aus `STACK_CHOICE`/`LANG_VARIANT` (A.1), Klartext.
- **Verfuegbare Skills:** `ls ~/.claude/skills/` (kommasepariert).

```markdown
## Maschinen-Kontext
- Typ: macOS
- Framework: intentron v0.8.1 — Skills unter ~/.claude/skills/ + pro Projekt
- Stack-Praeferenz: Node.js / Next.js / TypeScript
- Verfuegbare Skills: anti-slop, content-veredler, projekt-init, research, ...
```

Regeln: kein Secret; nicht ueberschreiben (idempotent); fehlt die globale `~/.claude/CLAUDE.md`, wird sie angelegt. Akzeptanz: nach `/bootstrap` ist der Maschinen-Kontext vorhanden, **ohne** separaten Nutzer-Schritt.

## 4. Lokales Projekt-Memory (optional)

**Nur wenn der Operator `~/.claude/projects/` als Memory nutzt.**

Die Memory-Strategie ist je nach Setup unterschiedlich. Der Skill legt optional eine Memory-Datei an:

Pfad: `~/.claude/projects/<sanitized-project-path>/memory/project_init.md`

```markdown
---
name: {{PROJECT_NAME}} — Initial Setup
description: Setup-Status und Quick Reference
type: project
---

**Projekt:** {{PROJECT_NAME}}
**Pfad:** {{PROJECT_PATH}}
**GitHub:** {{GITHUB_REPO}}
**Obsidian:** {{OBSIDIAN_PROJECT_PATH}}
**Backlog:** {{BACKLOG_TOOL}} ({{BACKLOG_URL}})
**Version:** {{VERSION_START}}
**Setup-Datum:** {{TODAY}}

## Installierte Skills
{{SKILLS_LIST}}

## Aktivierte Add-ons
{{ADDONS_LIST}}

## Governance-Hooks
- spec-gate.sh: aktiv
- doc-version-sync.sh: aktiv
{{ORPHAN_CHECK_NOTE}}

## Learning-Loop
Level: {{LEARNING_LOOP_LEVEL}}

## Ausstehend
- [ ] Erste Story via /ideation
{{OUTSTANDING_ITEMS}}
```

## 5. Abschluss-Check

Nach der Registry-Aktualisierung zeigt der Skill eine Zusammenfassung:

```
Registry-Update abgeschlossen:
  ✅ Obsidian Projekt-Hub: {{OBSIDIAN_PROJECT_PATH}}
  ✅ Obsidian Projekt-Index: 00 Kontext/Projekte.md
  [✅ / ⏭]  Globale CLAUDE.md-Zeile hinzugefuegt
  [✅ / ⏭]  Projekt-Memory angelegt: ~/.claude/projects/.../project_init.md
```

Wenn Obsidian-Vault nicht gesetzt wurde, werden die Obsidian-Teile uebersprungen — dann ist die `PMO HUB`-Funktion teilweise im Repo selbst abgedeckt (via `ARCHITECTURE_DESIGN.md` Hub).
