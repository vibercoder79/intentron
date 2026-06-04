# Wave BE — Convention against cross-session drift in ideation/implement (BOO-154)

**What's now in place:** the lesson from the intentron-internal drift (BOO-153) is now anchored as a **convention in the shipped framework** — `ideation` and `implement` explicitly point out how to avoid number/ID collisions with parallel sessions/developers. DE+EN.

## Stories
- **BOO-154** — ideation step 6 (backlog-first ID convention) + implement step 0c (cross-session / isolation note) + reference to the three-level collision-protection model.

## Changes (DE+EN)
- **`ideation/SKILL.md`** (2.7.0 → **2.8.0**, README updated): step 6 — get the story number **from the backlog tool**, then name `specs/<PREFIX>XXX.md` with exactly that number; never assign manually/in parallel.
- **`implement/SKILL.md`** (2.12.0 → **2.13.0**, README updated): step 0c — pre-flight isolates agents within ONE story (level 3); several people/sessions → own clone / `git worktree` (levels 1/2).
- Both reference `docs/kollisionsschutz-drei-ebenen.md`.

## Effect
What triggered the drift internally (manual parallel ID assignment) is now **explicitly addressed** in customer projects — central backlog assignment + isolation is stated as a convention directly in the skills, not just implicit in the tooling.

## Scope boundary
Pure skill docs/convention — no runtime code, no guard mechanism in the customer project (the wave guard stays intentron-internal, BOO-153).

## References
Spec: `specs/BOO-154.md`. Branch: `feat/boo-154-cross-session-konvention`. Builds on: BOO-151 (three-level collision protection), BOO-153 (ADR cross-session-drift). Operator source: Tobias, 2026-06-04.
