# Wave CA — Make observability visible: docs + logging/monitoring runbook (BOO-179)

> 🌐 **Language:** English (this file) · [🇩🇪 Deutsch](wave-ca-observability-sichtbar.md)

**What is now in place:** Observability is visible and backed by an onboarding track. The **substance** already existed (architecture dimension #5 / BOO-14: `observability.md` skeleton at bootstrap, `ARCHITECTURE_DESIGN.md §5/§6`, grafana skill) — but you **couldn't see where** logging/monitoring requirements belong. This story closes the visibility gap. Deliberately **no** ideation interview (would bloat it) — logging/monitoring is a downstream track after bootstrap.

## Changes

- **Runbook `docs/runbooks/logging-monitoring.md` (+ `.en`):** onboarding questions (corporate/compliance requirements · log targets · log file vs. Prometheus/Grafana · metrics/endpoint · alert channels · retention) + **2 copy-paste examples of how to write `observability.md`** (`payment-api` + `notification-worker`, with the three real mandatory alerts), plus validation (`promtool check rules`) and feeding into `ARCHITECTURE_DESIGN.md §5/§6` via `/architecture-review`.
- **HANDBOOK chapter `8d-ter. Logging & monitoring` (+ `.en`):** concept (downstream track, enforced via architecture review / corporate-IT sign-off rather than ideation) + the three mandatory sections → points to the runbook.
- **`observability.md` explained in three places:** HANDBOOK §7 Group G (callout "this is where logging/monitoring requirements belong"), `docs/onboarding/artefakt-landkarte.md` (+ `.en`, previously not listed at all), `docs/runbooks/audit-perspective.md` (+ `.en`, as audit evidence).
- **Bootstrap final checklist** (`bootstrap/SKILL.md` §7.6 + `.en`): hint "logging/monitoring required? → enter requirements in `observability.md`" (pure reference, **no** version bump).

## The three mandatory sections of `observability.md`

Logging schema · metrics endpoint · alert rules (`{service}_down` / `_error_rate_high` >5% / `_p95_slow` p95 >1s, routing via `observability/.env.observability`).

## Scope

- No change to the observability architecture dimension itself (exists, BOO-14) — only visibility + guidance. **No** ideation touchpoint. The grafana skill stays standalone.
- Wave letter **ca** (bz = stack linter BOO-178).

## References

Spec: `specs/BOO-179.md`. Branch: `tobiaschschmidt/boo-179-docs-observability-sichtbar`. Related: BOO-14 (observability dimension/skeleton), BOO-180 (doc DoD), BOO-178 (stack linter, same shape). Operator source: Tobias, 2026-06-07.
