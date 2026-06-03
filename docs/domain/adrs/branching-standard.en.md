# ADR: Branching standard — Trunk-Based with a protected `main` (BOO-124)

- **Status:** accepted (2026-06-03)
- **Context source:** post-trial follow-up (BKO, 2026-06-02) — "What standard do you ship with?"

## Context
The branch-strategy **options** (Trunk-Based / feature branches + PR / GitFlow) were documented in the
HANDBUCH (multi-operator Appendix R) as an equal trade-off table — **without a named default**. Sales and
onboarding lacked the clear answer "our standard is X". INTENTRON targets small stories, parallel agent
work, and auditable gates.

## Decision
The framework's **default branching standard** is **Trunk-Based Development with a protected `main`**:
- protected `main` (branch protection BOO-29 + spec gate BOO-4/27),
- **short-lived feature branches** (max 1–2 days),
- **pull requests** with at least 1 review,
- **required status checks** (ESLint/Ruff/Semgrep/Tests/… + optionally SonarCloud/typecheck) must be green.

**Sales one-liner:** "Our standard is Trunk-Based Development with a protected `main` and PR gates — lean,
auditable, agent-friendly. Multi-environment branching (GitFlow & co.) we offer where the release reality
demands it."

## Rationale
- **Lightweight:** few long-lived branches → minimal merge hell.
- **Agent-friendly:** short branches reduce merge drift under parallel agent work (execution isolation).
- **Quality safeguard:** protected `main` + gates enforce review + green checks before every merge.

## Alternatives (not the default)
- **Feature branches with PR review:** robust for 5–15 operators; branches can live long → rising conflicts.
- **GitFlow:** release-driven branches (`develop`, `release/*`, `hotfix/*`); for audit-mandated regulation —
  more complex, slower. Offered where the release reality demands it.

Full trade-off table + scaling recommendation by team size: HANDBUCH Appendix R §Layer 1
"Alternatives (when not our default)". Visualization: `docs/assets/boo-124-branching-standard.en.png`.

## Consequences
- Bootstrap/branch protection (BOO-29) already implement the default (protected `main`, required checks).
- In bootstrapped projects this ADR is linked from `ARCHITECTURE_DESIGN.md §9 References`.
- Deviations (feature-branches-only, GitFlow) are allowed but must be justified in a project-level ADR.
