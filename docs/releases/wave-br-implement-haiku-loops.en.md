# Wave BR — implement: lint loops on a Haiku subagent (BOO-171)

**What's there now:** `/implement` delegates its mechanical iteration loops (6a ESLint/Ruff, 6a-bis Semgrep) to a new **`lint-fixer` subagent with `model: haiku`** — the expensive reasoning part (code core step 5, security findings 6e) stays on **Opus**. Closes the internal tier gap that BOO-170 (one top-level model per subprocess) left open. Lightweight variant: exactly the one real cost lever.

## Stories
- **BOO-171** — lint loops on a Haiku subagent (BOO-170 follow-up).

## Changes
- **New `implement/references/lint-fixer.agent.md`** — named subagent definition (`model: haiku`, tools Read/Edit/Write/Bash), a purely mechanical "fix until green" worker with hard limits.
- **implement step 6a (DE+EN):** delegation block — 6a/6a-bis to `lint-fixer` (haiku), code core (5) + security (6e) stay Opus, graceful degradation (subagent unavailable → parent keeps iterating).
- **Version:** implement 2.14.0 → 2.15.0. `model-tiers.json` unchanged (`implement-iterations: haiku` already existed).

## Spike (verified)
Subagents carry `model:` in frontmatter; an opus parent can spawn a haiku child (reliable via named `.claude/agents/*.md`). **Caveat:** per-subagent cost attribution is not guaranteed by CC. Finding: implement already had the `meta.json` tier schema, but the loop ran inline — this story makes the delegation real.

## Effect
The blunt lint/test-fix loops run on the cheapest model (~19× cheaper output than Opus) with no quality loss at the code core. Consistent with the `meta.json` tier tracking.

## Scope
Lightweight variant. **Open (follow-up):** automatic bootstrap scaffolding of `.claude/agents/lint-fixer.md`; fully executable VPS daemon (variant B from BOO-170); reliable subagent cost attribution. A separate opus security subagent was deliberately omitted (the parent is opus anyway). Wave letter **br** (bq = daemon model routing BOO-170).

## References
Spec: `specs/BOO-171.md`. Branch: `feat/boo-171-implement-subagent-routing`. Related: BOO-170 (daemon top-level routing), BOO-84 (tier routing), BOO-157 (sprint-run). Operator source: Tobias, 2026-06-06.
