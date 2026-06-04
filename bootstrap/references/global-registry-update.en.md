# Global Registry Update — Register a new project

After setting up a new project, these registry points are updated:

## 1. SecondBrain (Obsidian) — Project hub

**Only if `OBSIDIAN_VAULT` was set in Block B.**

Path: `{OBSIDIAN_VAULT}/02 Projekte/{PROJECT_NAME}/`

Folder structure:
```
{OBSIDIAN_VAULT}/02 Projekte/{PROJECT_NAME}/
├── {PROJECT_NAME} - PMO HUB.md        ← Project hub with phase table, status, references
├── Architektur-Vorgaben.md            ← Skeleton (filled via /ideation)
├── Components/                        ← Living per-component docs (if Block C = yes)
├── Decisions/                         ← ADRs (filled on first ADR)
├── Meetings/                          ← Meeting notes
└── Research/                          ← Deep research outputs (/research)
```

**PMO HUB template:**

```markdown
---
tags: [project, {{PROJECT_NAME_LOWER}}]
status: active
phase: conception
created: {{TODAY}}
updated: {{TODAY}}
language: {{PRIMARY_LANG}}
source: bootstrap
---

# {{PROJECT_NAME}} — PMO Hub

> {{PROJECT_DESC}}

## Project goal

[One-sentence goal — operator to refine]

## Status

**Phase:** Conception → Phase 0

## Stack

See `ARCHITECTURE_DESIGN.md` in the repo ({{GITHUB_REPO}}).

## Repositories & code

| What | Path / URL |
|------|------------|
| GitHub repo | {{GITHUB_REPO}} |
| Local path | `{{PROJECT_PATH}}` |
| Backlog | {{BACKLOG_URL}} |
| Issue prefix | `{{ISSUE_PREFIX}}` |

## Active add-ons

{{ADDONS_LIST}}

## Installed skills

{{SKILLS_LIST}}

## Doc architecture (3 layers + hub)

- **Hub (repo):** `ARCHITECTURE_DESIGN.md` — central entry, §9 references
- **Story specs (repo):** `specs/{{ISSUE_PREFIX}}XXX.md`
- **Component docs (Obsidian):** `Components/*.md`
- **Architecture guidelines (Obsidian):** this page → `Architektur-Vorgaben.md`

## Learning loop

Level: {{LEARNING_LOOP_LEVEL}}
Path: `{{PROJECT_PATH}}/journal/` + `04 Ressourcen/{{PROJECT_NAME}}/learnings.md` (cross-link)

## Open items

- [ ] First story via /ideation
- [ ] Adjust backlog labels as needed
- [ ] Fill Obsidian project folder with research as needed

## Links

- [[Architektur-Vorgaben]]
- [[../../../../../04 Ressourcen/{{PROJECT_NAME}}/learnings]]
```

## 2. Project index (Obsidian)

**Only if `OBSIDIAN_VAULT` is set.**

File: `{OBSIDIAN_VAULT}/00 Kontext/Projekte.md`

If exists: add row in project table. If not: create file with base structure.

```markdown
| {{PROJECT_NAME}} | [[02 Projekte/{{PROJECT_NAME}}/{{PROJECT_NAME}} - PMO HUB\|Hub]] | {{PROJECT_PATH}} | {{VERSION_START}} | active |
```

## 3. Global CLAUDE.md (optional)

**Only if the operator has a global `~/.claude/CLAUDE.md` with a project table.**

The skill presents the new entry:

```markdown
| **{{PROJECT_NAME}}** | `{{PROJECT_PATH}}` | {{GITHUB_REPO}} | {{OBSIDIAN_PROJECT_PATH}} |
```

Operator confirms insertion point. Skill writes the line — or presents it for manual insertion.

### 3a. Standard project path `PROJECTS_ROOT` (BOO-138)

On a machine hosting several projects (developer VPS), the bootstrap defines **once** where projects live by default — and then reads this path as the default on every subsequent bootstrap. This is the machine-level prerequisite for frictionless multi-project operation (HANDBUCH Appendix U path 2).

**Read (every bootstrap, Block B question 1):** the skill checks `~/.claude/CLAUDE.md` for a `PROJECTS_ROOT` entry. If set, question 1 is pre-filled with `<PROJECTS_ROOT>/<project-name>`; the operator confirms with Enter or overrides with a custom path.

**Write (first project of the machine only):** if no `PROJECTS_ROOT` is recorded, the skill asks once and records it — after operator confirmation — in `~/.claude/CLAUDE.md`. Suggested block:

```markdown
## Project standard path

- `PROJECTS_ROOT`: `~/projects` — new projects are created here by default (`<PROJECTS_ROOT>/<project-name>`).
- Per project the standard structure applies (PMO hub, `specs/`, `journal/daily/`, `docs/project/`) + the session routines from the project `CLAUDE.md` (BOO-129/139).
```

Rules: operator confirmation required (no silent write); **no secret**; override always possible (the operator may deliberately place a project outside `PROJECTS_ROOT`). No cross-project cockpit — the daily state emerges when opening the respective project (PMO hub + latest `journal/daily/` note).

### 3b. Machine context (BOO-145)

At the end of **Block A** (A.8) the bootstrap automatically writes a `## Machine context` section into the global `~/.claude/CLAUDE.md` — **idempotent + with no separate operator step**. It gives every AI session on the machine immediate orientation (OS, framework version, preferred stack, available skills). Together with `PROJECTS_ROOT` (§3a) it forms the **machine-level context** of the global `~/.claude/CLAUDE.md`.

**Read (every bootstrap, A.8):** the skill checks `~/.claude/CLAUDE.md` for a `## Machine context` section. If present, **do nothing** (do not overwrite — the operator may freely adjust it).

**Write (only if the section is missing):** determine the values and append:

- **Type:** `uname -s` → `Darwin` = `macOS`, `Linux` = `Linux` (fallback `$OSTYPE`).
- **Framework version:** `git -C <intentron-repo> describe --tags --abbrev=0` (e.g. `v0.8.1`); fallback `bootstrap` skill version.
- **Stack preference:** from `STACK_CHOICE`/`LANG_VARIANT` (A.1), plain text.
- **Available skills:** `ls ~/.claude/skills/` (comma-separated).

```markdown
## Machine context
- Type: macOS
- Framework: intentron v0.8.1 — skills under ~/.claude/skills/ + per project
- Stack preference: Node.js / Next.js / TypeScript
- Available skills: anti-slop, content-veredler, projekt-init, research, ...
```

Rules: no secret; do not overwrite (idempotent); if the global `~/.claude/CLAUDE.md` is missing, it is created. Acceptance: after `/bootstrap` the machine context is present, **without** a separate user step.

## 4. Local project memory (optional)

**Only if the operator uses `~/.claude/projects/` for memory.**

Memory strategy depends on setup. Skill optionally creates:

Path: `~/.claude/projects/<sanitized-project-path>/memory/project_init.md`

```markdown
---
name: {{PROJECT_NAME}} — Initial Setup
description: Setup status and quick reference
type: project
---

**Project:** {{PROJECT_NAME}}
**Path:** {{PROJECT_PATH}}
**GitHub:** {{GITHUB_REPO}}
**Obsidian:** {{OBSIDIAN_PROJECT_PATH}}
**Backlog:** {{BACKLOG_TOOL}} ({{BACKLOG_URL}})
**Version:** {{VERSION_START}}
**Setup date:** {{TODAY}}

## Installed skills
{{SKILLS_LIST}}

## Active add-ons
{{ADDONS_LIST}}

## Governance hooks
- spec-gate.sh: active
- doc-version-sync.sh: active
{{ORPHAN_CHECK_NOTE}}

## Learning loop
Level: {{LEARNING_LOOP_LEVEL}}

## Outstanding
- [ ] First story via /ideation
{{OUTSTANDING_ITEMS}}
```

## 5. Final check

After registry update, the skill shows a summary:

```
Registry update complete:
  ✅ Obsidian project hub: {{OBSIDIAN_PROJECT_PATH}}
  ✅ Obsidian project index: 00 Kontext/Projekte.md
  [✅ / ⏭]  Global CLAUDE.md line added
  [✅ / ⏭]  Project memory created: ~/.claude/projects/.../project_init.md
```

If the Obsidian vault is not set, the Obsidian parts are skipped — the PMO HUB function is then partially covered in the repo itself (via `ARCHITECTURE_DESIGN.md` hub).
