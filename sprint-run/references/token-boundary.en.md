# Token-Boundary — 80% logic + sprint budget

Reference for `/sprint-run` step 2 (budget planning) and step 6 (sprint boundary).
Basis: HANDBUCH Appendix G (sprint-sizing mechanic, BOO-38/39/40).

## Principle: token box instead of time box

A sprint is **80% of the context window** of the model used — model-independent.
No burndown, no velocity, no story-points-per-sprint statistic. Outcome is measured via
intent fulfillment, not via token consumption.

| Threshold | Source (`environment.json`) | Effect |
|---|---|---|
| `token_warn_threshold` | default `70` | Soft warning: sprint is nearing its end |
| `token_hard_threshold` | default `80` | **Hard stop**: sprint boundary → `/sprint-review` |

## Budget planning (step 2)

1. Determine the context window of the model (e.g. 200k).
2. Sprint budget = 80% of it (e.g. 160k).
3. Sum the `token_estimate` of all candidate stories (from the spec `Execution Isolation` block).
4. Move stories that blow the budget to the next sprint — **hint, no
   abort**. No story is secretly trimmed.
5. Order: `blockedBy` first, then priority.

## Boundary check (step 4.8 / 6)

After each story (and roughly during ongoing implementation) project the cumulative consumption against
`token_hard_threshold`:

- **< 80%:** next story.
- **≥ 80%:** leave loop → step 6: trigger `/sprint-review`, operator hint
  **"Sprint boundary reached"**. Remaining stories stay in the backlog for the next sprint.

> The boundary is **conservative**: better to stop one story earlier than to run into the
> context limit in the middle of a story. A started, not fully tested story is more expensive than a
> postponed one.

## Relation to story points

| SP | Budget share (@200k) | Execution mode |
|---|---|---|
| 1 | ~5% | linear |
| 2 | ~10–15% | linear / sub-agents |
| 3 | ~20–30% | sub-agents |
| 5 | ~40–60% | agentic |
| 8 | >60% | **split** |

`/sprint-run` uses this estimate only for **ordering and boundary** — the actual
mode choice per story is made by `/implement` (step 0c) based on the spec block.

Sketch: `docs/sprint-run-flow.png` (HANDBUCH Appendix AD).
