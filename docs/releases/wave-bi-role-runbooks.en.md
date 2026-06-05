# Wave BI — Role-specific runbooks: CISO · DPO · CTO · managing director (BOO-158–163)

**What's now here:** Four narrative entry-point runbooks explain INTENTRON from one leadership role's point of view — managing director, CISO/IT lead, data protection officer, CTO. Each reads in under 10 minutes, answers "what does the framework mean for me, which gatekeepers apply, where do I take control", and is **not new machinery** but a lens on what already exists (like `audit-perspective.md`). Linked from the README in EN + DE, plus a shared role map as a sketch. Pure docs. DE+EN.

## Stories
- **BOO-158** — Epic (umbrella).
- **BOO-159** — `docs/runbooks/ciso-security.md` (+EN) + sketch.
- **BOO-160** — `docs/runbooks/dpo-privacy.md` (+EN) + sketch.
- **BOO-161** — `docs/runbooks/cto-code-quality.md` (+EN); sketch reused (`quality-gate-four-layers`).
- **BOO-162** — `docs/runbooks/ceo-business-case.md` (+EN) + sketch.
- **BOO-163** — Integration: role map sketch, README (EN+DE), artefakt-landkarte cross-reference, this wave.

## Changes (DE+EN)
- **New `docs/runbooks/ciso-security.md` / `.en.md`** — security view: gatekeepers along the lifecycle, `security-architect` (4 modes), levers, limits.
- **New `docs/runbooks/dpo-privacy.md` / `.en.md`** — privacy view: `dpo` skill (3 modes), personal-data-paths gate, deterministic catalogue audit (`dpo-audit.py`), GDPR/BDSG/nFADP.
- **New `docs/runbooks/cto-code-quality.md` / `.en.md`** — code quality / tech debt: spec-first, 4-layer quality gates, doc-version-sync, audit trail, learning loop, `governance_mode`.
- **New `docs/runbooks/ceo-business-case.md` / `.en.md`** — investment/business view: business risk → mechanism → proof, decision triggers, honest cost.
- **New sketches** `docs/role-runbooks-map.*` (hero), `docs/ciso-security-runbook.*`, `docs/dpo-privacy-runbook.*`, `docs/ceo-business-case-runbook.*` (DE+EN each, `.excalidraw` + `.png`). CTO reuses `docs/quality-gate-four-layers.*`.
- **`README.md`** — new section "Role-specific runbooks" / "Rollenspezifische Runbooks" (EN + DE), after "Where to start".
- **`docs/onboarding/artefakt-landkarte.md` / `.en.md`** — role entry-point note next to the sign-off roles.

## Effect
To the question "is there a role-appropriate introduction to the framework?", there are now four lenses instead of a 230 KB handbook as the only entry point. A CISO, DPO, CTO or managing director understands in under 10 minutes what the framework means for their own role.

## Scope note
Pure docs, no code, no new machinery. Wave letter `bi` (bh = knowledge-onboarding-sketches, bg = BOO-156). Project-local artefacts in the CTO runbook are code spans (no dead links), with a template link under "Further reading". Builds on `artefakt-landkarte` (sign-off roles) + `audit-perspective.md` (style pattern).

## References
Spec: `specs/BOO-158.md`. Branch: `tobiaschschmidt/boo-158-rollenspezifische-runbooks-ciso-dpo-cto-geschaftsfuhrung`. Operator source: Tobias, 2026-06-05.
