# Wave AY — VPS Standard Project Path & Daily-Note Loop (BOO-138/139)

**What's now in place:** A developer VPS becomes a frictionless multi-project host. The bootstrap asks **once per machine** for a standard project path (`PROJECTS_ROOT`), records it in the global operator `~/.claude/CLAUDE.md`, and then proposes it as the default for every further project — Enter is enough, the override remains. In addition, every project gets a **daily-note loop**: the generated `CLAUDE.md` asks at session end "Shall I write the daily note?" and stores it under `journal/daily/YYYY-MM-DD.md`, which is read back on the next start. This ports the Obsidian-vault principle (fixed project location + daily notes) to the VPS **without Obsidian**. Deliberately **no** cockpit/dashboard — lightweight.

## Stories

- **BOO-138** — **VPS standard project path `PROJECTS_ROOT`**: the first bootstrap on a machine asks for the path + writes it (after operator confirmation) to `~/.claude/CLAUDE.md`; Block B question 1 reads it and proposes `<PROJECTS_ROOT>/<project-name>` as the default (manual override remains).
- **BOO-139** — **journal/daily/ + session-end routine**: the generated project `CLAUDE.md` gets a session-END routine ("write the daily note?") + the convention `journal/daily/YYYY-MM-DD.md`; the session-START routine reads the latest daily note. Reuses the existing `journal/` baseline artifact (BOO-61) — no parallel folder.

## Changes (DE+EN)

- **`bootstrap/SKILL.md`** (version 3.35.0 → **3.36.0**): Block B — `PROJECTS_ROOT` mechanism (read/ask/write) + default proposal on question 1; remember-block extended with `PROJECTS_ROOT` (BOO-138).
- **`bootstrap/references/global-registry-update.md`**: new section "3a. Standard project path `PROJECTS_ROOT`" — read/write rule, operator confirmation, no secret, override (BOO-138).
- **`bootstrap/references/file-templates.md`** (CLAUDE.md template): session-START routine also reads the latest `journal/daily/` note; new **session-END routine** "write the daily note?" + write-back convention (BOO-139).
- **`bootstrap/references/project-documentation-ssot.md`**: lightweight SecondBrain loop extended with `journal/daily/` (BOO-129/139).
- **`HANDBUCH.md` Appendix U**: machine level names `PROJECTS_ROOT`, project level names `journal/daily/`; path 2 step 1 with the default-path proposal (BOO-138/139).

All changes are DE+EN parity (`.en.md` counterparts updated alongside).

## Scope boundary

No cross-project cockpit/dashboard (deliberately dropped — lightweight): "where are we?" emerges when opening the respective project from the PMO hub + latest daily note. `repo-docs` remains a portable Markdown base with relative links (mirrorable to GitHub/Obsidian/DMS); no Dataview/wikilink lock-in.

## References

Specs: `specs/BOO-138.md`, `specs/BOO-139.md`. Branch: `feat/boo-138-139-vps-projektpfad`. Builds on: BOO-129 (session-start loop), BOO-130 (`docs/how-we-document.md`), Appendix U (multi-project operation). Operator source: Tobias, 2026-06-03 (origin: SecondBrain setup → VPS transfer).
