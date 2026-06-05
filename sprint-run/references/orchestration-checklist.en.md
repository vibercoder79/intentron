# Orchestration Checklist — sprint pre-flight + loop checks

Reference for `/sprint-run` step 1 (sprint pre-flight, HARD GATE) and step 4 (daemon loop).
The sprint may only start once **all** pre-flight points are green.

## Sprint pre-flight (step 1) ⛔

| Check | Pass criterion | On violation |
|---|---|---|
| Backlog prioritized | `/backlog` delivers ordered candidates (`Todo`/`Backlog`, order) | STOP — run `/backlog` first |
| Spec per story | `specs/<ISSUE>.md` exists (spec gate) | remove story from sprint / STOP |
| Schrader-complete | Insight, Constraints, Success Criteria, Desired Outcome each ≥20 characters | remove story from sprint |
| Execution-Isolation block | Spec carries `execution_mode`, `worktree_strategy`, `write_scopes` | remove story from sprint |
| Governance gates | `governance_mode` from CONVENTIONS; sensitive-paths/personal-data configured | clarify pause behavior |
| Tooling | `git worktree` there, `gh` authenticated, `main` clean | STOP |

> The pre-flight is the condition for the loop afterwards to run without follow-up questions.
> In daemon mode (`--auto`) stories that violate a pre-flight point are
> **skipped and logged** — they do not block the whole sprint.

## Loop checks per story (step 4)

Before `/implement` (4.1–4.3):
- [ ] Linear status set to `In Progress`
- [ ] Worktree created: `git worktree add ../wt-<ISSUE> -b feat/boo-<n>-<slug>`
- [ ] Working tree in the worktree clean

After `/implement` (4.5–4.7):
- [ ] Remote CI green (`gh run watch --exit-status`) — otherwise max 3 fix iterations
- [ ] Merge **only** on green CI
- [ ] Worktree removed: `git worktree remove ../wt-<ISSUE>`
- [ ] Linear status `Done` with AC evidence comment

Per iteration:
- [ ] Token consumption checked against the 80% boundary (step 4.8)

## Anti-pattern

- **Taking a story without a spec into the sprint** — the spec gate halts `/implement` anyway, but
  costs half a loop. Catch it in the pre-flight.
- **Multiple stories in the same worktree** — collision risk; one worktree per story (level 2,
  see `docs/kollisionsschutz-drei-ebenen.md`).
- **Merge on red CI** — forbidden (BOO-148). No merge without a green remote run.
