# Kollisionsschutz: Die drei Ebenen der Parallelität

> Wie dieses Framework verhindert, dass sich parallele Arbeit gegenseitig überschreibt — auf **drei klar getrennten Ebenen**. Sie werden oft verwechselt, sind aber komplett unterschiedliche Mechanismen. EN: [`kollisionsschutz-drei-ebenen.en.md`](kollisionsschutz-drei-ebenen.en.md).

„Parallel arbeiten" heißt je nach Kontext etwas anderes — und jeder Kontext hat seinen **eigenen** Schutzmechanismus. Wer sie vermischt, sucht den Fehler auf der falschen Ebene.

## Die drei Ebenen auf einen Blick

| Ebene | Wer arbeitet parallel? | Geteilt wird… | Schutz | Status |
|---|---|---|---|---|
| **1 — Multi-USER** | mehrere Menschen an einem Projekt | nur das GitHub-Repo (Remote) | eigener Klon pro User, Sync über Git | dokumentiert (Anhang P §3 + U), Runbook |
| **2 — Multi-SESSION** | eine Person, mehrere Sessions | derselbe lokale Klon | eigener `git worktree` / Session-Hinweis | Hinweis (siehe unten) |
| **3 — Multi-AGENT** | mehrere KI-Agenten in einer Story | derselbe Working Tree einer Session | `EXECUTION_ISOLATION` (write-scope / git-worktree) | im Framework verankert (BOO-52) |

**Faustregel:** Je tiefer die Ebene, desto enger der geteilte Raum — und desto strenger der Mechanismus. Ebene 1 trennt über **Git**, Ebene 2 über **Worktrees**, Ebene 3 über **Write-Scopes/Worktrees + Gate**.

## Ebene 1 — Multi-USER (mehrere Menschen, ein Projekt)

**Situation:** 10 Entwickler arbeiten an Projekt X auf einer VPS.

**Schutz:** Jeder hat einen **eigenen System-User** und **klont das Repo in sein eigenes Home** (`/home/<user>/projects/projektX`). **Keine geteilten Working Trees.** Synchronisiert wird ausschließlich über GitHub (`push`/`pull`/PR/Merge) — das ist „optimistic concurrency": alle arbeiten frei, Konflikte werden beim Merge gelöst. Es gibt kein lokales „Original"; alle Klone sind gleichwertig, GitHub ist der Bezugspunkt.

**Konsequenz für die Projektstruktur:** Der geteilte Teil (PMO-Hub, `decisions/`, `meetings/`, Specs) liegt im Repo und wird via Git geteilt. Das persönliche Tageslogbuch `journal/daily/` gehört bei Multi-User in die `.gitignore` — so hat jeder sein eigenes lokales Journal ohne Kollision.

→ Setup-Schritte: **Runbook [`runbooks/multi-user-vps.md`](runbooks/multi-user-vps.md)** · HANDBUCH **Anhang P §3** (Multi-User-VPS) + **Anhang U** (Pro-Projekt-Checkliste).

## Ebene 2 — Multi-SESSION (eine Person, mehrere Sessions, ein Klon)

**Situation:** Du hast zwei Claude-Code-Sessions offen, die **denselben** lokalen Klon beschreiben (zwei Fenster, zwei Geräte auf dasselbe Verzeichnis).

**Problem:** Die Sessions wechseln Branches und überschreiben sich gegenseitig den Working-Tree-Zustand — der Branch wandert unter einem weg.

**Schutz:** **Nicht** zwei Sessions auf denselben Klon. Stattdessen pro paralleler Spur ein eigener **`git worktree`** (`git worktree add ../projektX-spur2 <branch>`) — eigenes Arbeitsverzeichnis, eigener Branch, geteilte `.git`-Datenbank. Optional warnt ein **Session-Hinweis** beim Start, wenn eine andere Session denselben Tree aktiv nutzt.

→ Das ist die leichteste Ebene: meist reicht **Disziplin + Worktree**. Ein Lock-Hinweis ist Sicherheitsnetz, kein Muss.

## Ebene 3 — Multi-AGENT (eine Session, mehrere Sub-Agenten an einer Story)

**Situation:** Eine Story wird mit mehreren KI-Agenten **parallel** umgesetzt (`sub-agents` / `agentic`).

**Schutz (im Framework verankert, BOO-52):** `CONVENTIONS.md` legt `EXECUTION_ISOLATION` fest:
- `none` — keine parallelen Edits (`linear`).
- `write-scope` — parallele Helfer nur mit **disjunkter Datei-Ownership** (`write_scopes` in der Spec).
- `git-worktree` — jeder Agent bekommt einen **eigenen Worktree/Branch** (Pflicht für `agentic`).

Der `implement`-Skill erzwingt das in **Schritt 0c „Execution-Isolation-Pre-Flight"** als hartes Gate: `sub-agents` braucht befüllte `write_scopes`, `agentic` braucht `git-worktree`. So überschreiben sich Agenten nie.

→ Diese Ebene ist **bereits vollständig gebaut** — kein Setup nötig, sie greift pro Story.

## Merksatz

> **Ebene 1 = eigener Klon. Ebene 2 = eigener Worktree. Ebene 3 = Write-Scopes/Worktree + Gate.**
> Drei Räume, drei Schlösser — nie das eine Problem mit dem Werkzeug der anderen Ebene lösen.
