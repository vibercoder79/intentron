# Wave AK — EU AI Act real conditional opt-in (BOO-105)

> 🌐 **Language:** English (this file) · [🇩🇪 Deutsch](wave-ak-eu-ai-act-optin.md)

**Problem before (from BOO-101):** „Strictly opt-in" was not true at the runner end. `dpo-audit.py` loads all `dpo/controls/*.yml` via `glob` — so the EU AI Act catalog ran along on every dpo audit, even in Privacy projects without an AI part (`AI_SYSTEM.md fehlt` GAP = noise). In addition, there was only an A.4 note, no executable bootstrap phase.

**What is there now:**

- **Catalog out of the auto-load:** `dpo/controls/eu-ai-act.yml` → `dpo/controls/optional/eu-ai-act.yml`. The non-recursive framework glob does not load subfolders; the recursive overlay glob loads it as soon as it is copied into the project.
- **Executable bootstrap phase 4.4n-bis** (only with `[x] EU AI Act`, requires Privacy): copies the catalog into the project overlay `.claude/dpo/controls/`, renders `AI_SYSTEM.md`, adds the `ARCHITECTURE_DESIGN.md` reference, optionally a backlog label `ai-act`. DE+EN.
- **Documentation aligned:** A.4 note, dpo/SKILL.md(.en) catalog table + runner list, README path, catalog header.

**Effect:** The EU AI Act check runs guaranteed **only** in projects that chose the add-on — no noise in non-AI projects. The path is end-to-end deterministic (question → phase → catalog in the overlay → dpo-AUDIT → REVIEW-NEEDED).

Spec: `specs/BOO-105.md`. Release: v0.7.2.
