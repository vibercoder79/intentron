<a name="english"></a>

# Sprint-Run — sprint orchestrator for fully automatic sprint execution

> Runs an entire sprint without manual story-by-story control: selects stories from the
> prioritized backlog, implements each one via `/implement` in daemon mode (own `git worktree`
> + branch), maintains the Linear status, waits for green remote CI, merges, cleans up and
> triggers `/sprint-review` at the 80% token boundary. Pure orchestrator — the orchestrated
> skills remain unchanged.

**Version:** 1.0.0 · **Command:** `/sprint-run`

---

## What the skill does

Without an orchestrator a sprint is run manually: call `/implement`, select story,
wait, next story, maintain Linear, manage worktrees by hand. `/sprint-run`
automates exactly this mechanic.

The skill chains the already existing building blocks — `/implement` daemon mode,
execution isolation (worktree), token pre-flight, remote CI loop (BOO-148) — into one
continuous sprint run. It writes **no** product code and does not change `/implement`,
`/backlog`, `/sprint-review`.

---

## How it works

| # | Step | Purpose |
|---|---------|-------|
| 0 | Load environment + sprint context | detect thresholds, adapter, daemon mode |
| 1 | **Sprint pre-flight** ⛔ | Backlog prioritized? Specs complete? Gates green? Tooling ready? |
| 2 | Plan sprint token budget | 80% budget, order by dependency + priority |
| 3 | Sprint plan + operator approval | daemon mode skips the approval |
| 4 | **Daemon loop per story** | worktree → `/implement` → CI wait → merge → Linear → cleanup |
| 5 | Error handling | story back, `daemon_fail_policy` (stop/continue) |
| 6 | Sprint boundary → `/sprint-review` | at 80% token / backlog empty / stop-on-fail |
| 7 | Sprint report | table: stories, token, CI, worktrees |

---

## Gate-block safety (critical)

If `/implement` triggers a **sensitive-paths** or **personal-data gate**, the
daemon **pauses** and notifies the operator (story ID + reason). Resume only after explicit
`review-ok` / `privacy-ok`. **No** automatic bypass, **no** timeout resume — even in
`--auto` mode.

---

## Distinction from `/implement`

| | `/implement` | `/sprint-run` |
|---|---|---|
| Scope | **one** story | **N** stories (entire sprint) |
| Worktrees | — (runs in the current tree) | own worktree + branch per story |
| Sprint end | — | 80% token boundary → `/sprint-review` |
| Invocation | direct | orchestrates `/implement` per story |

---

## Trigger phrases

- `/sprint-run`
- "run the sprint"
- "drive the sprint"
- "automation-cycle"

---

## Interfaces to other skills

| Upstream | What is delivered | Downstream | What we deliver |
|----------|--------------------|------------|------------------|
| `backlog` | Prioritized sprint list | `implement` (per story) | story ID, worktree, daemon trigger |
| `ideation` | Stories + specs + ADD | `sprint-review` (sprint end) | aggregated story metrics |

Chain: `intent → ideation → backlog → sprint-run → ( implement )* → sprint-review`.

---

## Installation

```bash
cp -r sprint-run ~/.claude/skills/sprint-run
```

Prerequisite: `git worktree` available, `gh` authenticated (remote CI wait), and the
sibling skills `backlog`, `implement`, `sprint-review` installed.

---

## File structure

```
sprint-run/
├── SKILL.md                                  ← Skill definition
├── SKILL.en.md                               ← English mirror
├── README.md / README.en.md                  ← this file (+ DE)
├── overview.excalidraw / .png (+ .en)        ← Skill overview sketch
└── references/
    ├── orchestration-checklist.md   (+ .en.md)  ← Sprint pre-flight + loop checks
    ├── gate-block-handling.md       (+ .en.md)  ← Pause/resume protocol
    ├── worktree-flow.md             (+ .en.md)  ← Worktree per story
    └── token-boundary.md            (+ .en.md)  ← 80% boundary logic
```

---

## Sketches

All diagrams in the Owlist Design System (see HANDBUCH Appendix AD):

- `overview.png` — Skill overview (this skill at a glance)
- `docs/sprint-run-flow.png` — Sprint-Run flow (daemon loop start → sprint end)
- `docs/story-breakdown.png` — Story breakdown (worktree → implement → CI → merge → cleanup)
- `docs/agent-interaction.png` — Agent interaction (backlog ↔ sprint-run ↔ implement ↔ sprint-review)
- `docs/github-integration.png` — GitHub integration (story → branch → PR → CI run)
- `docs/gate-block-handling.png` — Gate-block state machine (running → gate → paused → resumed)
