# Wave BQ — Model/mode routing in the sprint-run daemon + implement on Opus (BOO-170)

**What's there now:** The model/mode recommendation is now **enforced in the `/sprint-run --auto` daemon** (previously pure docs). Per story, a new tested helper script resolves the recommended model and starts `/implement` as a subprocess with `--model` + `--permission-mode dontAsk`. Plus a policy fix: **product code now runs on Opus** (best model for the code core). Interactively it stays a recommendation by design.

## Stories
- **BOO-170** — daemon model routing + spike + implement-Opus policy.

## Changes
- **New: `sprint-run/scripts/resolve-model.py`** (dependency-free, tested) — resolves `<skill>/SKILL.md recommended_model` (tier) → `model-tiers.json current_version` (version). Fallback `sonnet`.
- **sprint-run step 4.3 (DE+EN):** `/implement` as a subprocess with resolved `--model` + `--permission-mode dontAsk` + section "Model/mode routing (BOO-170)" (override hierarchy, multi-tier limit, daemon-vs-interactive).
- **Policy implement → opus (DE+EN):** `recommended_model: sonnet → opus`; `model-tiers.json` opus extended. Code core (step 5) + security findings (6e) opus, mechanical iteration loops (6a) stay haiku.
- **HANDBUCH (DE+EN):** enforcement paragraph in the model-routing appendix + opus routing row extended.
- **Version bumps:** implement 2.13.0 → 2.14.0, sprint-run 1.1.0 → 1.2.0.

## Spike (verified)
`claude --help`: `--model` + `--permission-mode` (choices acceptEdits/auto/bypassPermissions/default/dontAsk/plan) exist; no `--effort`. sprint-run is prompt-driven (no daemon program) → variant A (helper + subprocess spec) rather than a fully executable daemon.

## Effect
In an unattended sprint, every story automatically runs on the recommended model and in unattended mode — with the operator override hierarchy preserved. Product code on Opus = best quality for the value core; loops on Haiku = no wasted spend.

## Scope
Variant A (lightweight). **Open (follow-up story):** implement-internal subagent model routing (haiku loops / opus security within one run) + fully executable VPS daemon. Effort remains non-enforceable (no CLI flag). Wave letter **bq** (bp = Claude mode all skills BOO-169).

## References
Spec: `specs/BOO-170.md`. Branch: `feat/boo-170-daemon-model-routing`. Related: BOO-169 (mode docs), BOO-168 (mode foundation), BOO-84 (tier routing), BOO-157 (sprint-run). Operator source: Tobias, 2026-06-06.
