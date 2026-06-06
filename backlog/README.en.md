<a name="english"></a>

# Backlog — Dependency-Aware Sprint Planning

> Loads the whole backlog, maps dependencies, honors DB schema chains, and proposes a concrete priority order. No more "which story next?" by gut feeling.

**Version:** 1.5.0 · **Command:** `/backlog`

> 🔗 Sprint automation: **`/sprint-run`** runs a whole sprint and orchestrates the chain `backlog → implement → sprint-review`. See [`sprint-run/`](../sprint-run/README.en.md) · HANDBUCH Appendix AD.

> **Claude Code mode:** `/backlog` only reads and prioritizes (writes nothing) → **`plan`** (plan mode). It rides along read-only inside the `/sprint-run` daemon. Details: HANDBUCH §6 "Claude Code mode".

---

## What It Does

Most backlogs are flat lists sorted by priority. Real backlogs have hidden structure: dependencies, schema version chains, and stories that Linear still shows as "Todo" even though they shipped last week.

This skill loads the whole picture — system context from `CLAUDE.md` + `ARCHITECTURE_DESIGN.md`, completed issues from the last 30 days, all open issues — then builds a dependency graph. It catches things a human would miss:

- Stories that look blocked but aren't (blocker is already Done)
- Two stories both targeting `schemaVersion 18` (conflict — one must rewrite)
- Circular dependencies
- Orphaned references (`CLAW-14` mentioned in Issue X but doesn't exist)

---

## How It Works

```
Load environment  (.claude/environment.json — paths + tools_available, fall back to defaults)
        │
        ▼
Load system context  (CLAUDE.md + ARCHITECTURE_DESIGN.md + SYSTEM_ARCHITECTURE.md)
        │
        ▼
Load completed issues (last 30 days)
        │
        ▼
Load open backlog (all statuses)
        │
        ▼
Dependency graph · Schema chain check · Cycle detection
        │
        ▼
Sort:  In Progress > Blockers > Intent label > Priority > Dep-Depth > Age
        │
        ▼
Output:  Ordered list · Conflicts · Backlog hygiene suggestions
```

The `.claude/environment.json` provides paths (`paths.specs`, `paths.architecture_design`, `paths.reports_local`, ...) and a `tools_available` gate: if a tool is not active, the skill skips the call and notes it in the output. If the file is missing, the skill falls back to default paths and records that.

---

## The Schema-Chain Check (Mandatory)

Runs on every backlog pass. Stops schema conflicts before two engineers start the same migration:

1. Scan open issues for `## DB Schema Impact` sections
2. Build chain: `currentSchemaVersion → targetSchemaVersion` per story
3. Rule: **Stories with lower `targetSchemaVersion` always first**
4. Conflict flag: Two stories with the same target version → reported as **critical blocker**

Example output:
```
Schema Chain: STORY-A (v17 → v18) must ship before STORY-B (v18 → v19).
Conflict:     STORY-C and STORY-D both target v18 — one must be rewritten.
```

---

## Intent-Label Prioritization

When sorting, the skill honors the intent label from the `## Intent-Check` section in the story body (set by `/ideation`):

- `on-intent` comes **before** `neutral` at the same status and same priority
- `off-intent` stories drop to the end — with a warning: "Story X is off-intent — belongs in the backlog, not the sprint"
- If the label is missing, the story is treated as `neutral`

The output explains the reason: "Story X prioritized over Y because on-intent at equal points."

---

## Trigger Phrases

- `/backlog`
- "what's next?"
- "sprint planning"
- "priorities"
- "what should I pick up?"

---

## Interfaces with Other Skills

| Upstream | What's provided | Downstream | What we deliver |
|----------|-----------------|------------|------------------|
| `ideation` | New stories + dependencies + schema-impact | `implement` | The top-ranked story + reason why it comes first |
| Linear | Open / completed issues | `architecture-review` | Stories that need an architecture pre-check |
| `architecture-review` (System mode) | Recommended issues | `sprint-review` | Current backlog snapshot for quarterly audit |

---

## Artifacts / Outputs

- **Prioritized story list** with explicit reasoning per story
- **Dependency conflicts** — orphans, cycles, broken references
- **Schema chain report** — who goes before whom and why
- **Hygiene suggestions** — issues to close, re-priority, or split

---

## Installation

```bash
cp -r backlog ~/.claude/skills/backlog
```

---

## File Structure

```
backlog/
└── SKILL.md     ← Skill definition (read by Claude Code)
```

No reference files — the workflow is self-contained in `SKILL.md`.

---

---

