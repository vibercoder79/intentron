# Release Notes - Wave K Deployment Scenarios + Sovereignty Stack

> 🌐 **Language:** English (this file) · [🇩🇪 Deutsch](wave-k-deployment-and-sovereignty.md)

As of: 2026-05-27

## Purpose

Wave K closes BOO-70 and BOO-71. For the first time, the framework gives operators structured guidance on two setup questions that until now were consulting topics:

1. **BOO-70 — Deployment scenarios:** On which device topology does INTENTRON run? Appendix P describes four lived patterns (Solo-Mac, Solo-VPS, Multi-User-VPS coding factory, Team-with-coding-server) with a decision matrix, setup steps, skill installation, secrets separation, backup strategy and tradeoffs.
2. **BOO-71 — Sovereignty stack guide + LLM proxy hook:** Which EU-compliant alternatives exist to the default stack composition (GitHub, Anthropic USA, iCloud)? Appendix Q delivers the inspiration layer — five stack components with a table mapping and a short migration guide — and adds the optional config field `llm_proxy_url` as a hook point for operator-run anonymization/sovereignty proxies.

**Expected effect:** Both topics are moved from the "let's-ask-consulting" mode into the "read-the-appendix" mode. Bootstrap stays frictionless (default Solo-Mac, no new interview step for sovereignty) — but operators with regulated requirements find an initial orientation in the HANDBUCH.

## Affected Stories

- BOO-70 — HANDBUCH appendix P Deployment scenarios + bootstrap question A.7
- BOO-71 — HANDBUCH appendix Q Sovereignty stack guide + `llm_proxy_url` hook in `environment.json`

## Important Clarifications

### BOO-70: Bootstrap asks **one** question, not four scenarios

Pragmatic separation: the operator decision comes from the HANDBUCH appendix, bootstrap still performs the default setup (Solo-Mac). On choosing `b) different`, bootstrap only outputs a hint block, no interview fork, no scenario-specific setup code. This keeps the bootstrap skill lean and the beaten path unchanged for ~80% of operators.

### BOO-71: NO anonymization engine in the framework

Appendix Q documents EU alternatives per stack component and describes the `llm_proxy_url` hook conceptually. The framework implements **no** proxy routing whatsoever — the value is read, logged in `meta.json.llm_routing`, and with that the framework task is fulfilled. Anonymization (e.g. Microsoft Presidio) is an operator task and runtime infrastructure, not governance. The hook point is the minimal contract that enables audit trails without forcing a proxy implementation onto the operator.

### Privacy ≠ Sovereignty

Data sovereignty (Appendix Q) and Privacy-by-Design (Appendix O, BOO-69, Wave J) are orthogonal. An EU stack does not replace a GDPR obligation, and a GDPR-compliant processing on US cloud does not exempt from the CLOUD-Act risk. Operators with both requirements activate the Privacy add-on **and** choose their stack components according to Appendix Q.

## What Users Get with the New Setup

- **HANDBUCH appendix P "Deployment scenarios" (DE+EN)** with a decision matrix (6 operator profiles) and four complete scenario sections — operator profile, setup steps, skill installation, secrets separation, user isolation (where relevant), backup strategy, tradeoffs. Backup recommendations per scenario explicit (Time Machine / Hetzner Storage Box / Backblaze B2 / VPS snapshot), not vague.
- **Bootstrap question A.7 (`DEPLOYMENT_SCENARIO`)** with default Solo-Mac and a reference block for "different". The bootstrap briefing box now shows "Block A — Project core (10 questions)" instead of 9. Existing Solo-Mac operators experience zero change.
- **HANDBUCH appendix Q "Sovereignty stack guide + LLM proxy hook" (DE+EN)** with:
  - Decision matrix "When is the sovereignty switch worth it?" (7 triggers).
  - Table of EU-compliant alternatives for 5 stack components (code hosting, vault sync, LLM, issue tracker, CI) with tradeoff hints.
  - Per component a short migration guide (3-5 steps) plus a reference to the external docs of the respective tool.
  - LLM proxy hook section with a JSON schema snippet, a Microsoft Presidio concept example and a hard design-decision clarification.
- **`.claude/environment.json` schema extension:** optional field `llm_proxy_url: <url|null>` with default `null`. Documentation in `file-templates.md` updated (DE+EN).
- **`/implement` step 0 extended (point 7):** read-only explanation of the `llm_proxy_url` field, logging as an audit trace in `meta.json.llm_routing`. No routing code in the framework.

## Concrete Changes

| Area | Change | File |
|---|---|---|
| HANDBUCH appendix P NEW | Deployment scenarios reading entry point (DE+EN) | `HANDBUCH.md` + `HANDBUCH.en.md` |
| HANDBUCH appendix Q NEW | Sovereignty stack guide + LLM proxy hook (DE+EN) | `HANDBUCH.md` + `HANDBUCH.en.md` |
| Bootstrap question A.7 NEW | Deployment scenario, default Solo-Mac, reference to appendix P | `bootstrap/SKILL.md` v3.28.0 + `.en.md` |
| Bootstrap phase-0 briefing | "Block A — Project core (10 questions)" (was 9) | `bootstrap/SKILL.md` + `.en.md` |
| environment.json schema | optional field `llm_proxy_url` (default `null`) + field table extended | `bootstrap/references/file-templates.md` + `.en.md` |
| `/implement` step 0 point 7 | Doc block for reading `llm_proxy_url` + `meta.json.llm_routing` audit trace | `implement/SKILL.md` v2.11.1 + `.en.md` |
| Migration | `migrate_boo_70()` (doc-only) + `migrate_boo_71()` (inserts `llm_proxy_url: null` into env.json) | `bootstrap/scripts/migrate-to-v2.sh` |
| Migration checklist | §BOO-70 + §BOO-71 blocks (DE+EN) | `bootstrap/references/migration-checklist-v1-to-v2.md` + `.en.md` |
| ALL_ISSUES array | `BOO-70 BOO-71` added | `bootstrap/scripts/migrate-to-v2.sh` |

## Skill Version Bumps

- `bootstrap` 3.27.0 → 3.28.0 (minor: new question A.7, new optional env.json field)
- `implement` 2.11.0 → 2.11.1 (patch: step 0 doc block, no behavior lock)

## Migration for Existing Projects

`migrate_boo_70()` and `migrate_boo_71()` in `bootstrap/scripts/migrate-to-v2.sh`:

```bash
bash bootstrap/scripts/migrate-to-v2.sh --issue BOO-70
bash bootstrap/scripts/migrate-to-v2.sh --issue BOO-71
```

Both auto-steps idempotent and additive. Result:

- **BOO-70:** only a hint block (doc-only). Operator notes their deployment scenario in `migration-status.md`.
- **BOO-71:** insert `llm_proxy_url: null` into `.claude/environment.json` (if the field is still missing). If the file is missing: hint to `bash .claude/generate-environment-json.sh`.

Operator steps: read HANDBUCH appendix P + Q once, set status in `migration-status.md`, plan a sovereignty switch if applicable. Default Solo-Mac + default stack remain unchanged.

## Design Decision: Inspiration Layer, Not Setup Generator

INTENTRON stays frictionless for ~80% of operators (Solo-Mac, default stack). Wave K adds **no** mandatory step — both appendices are reading material plus 1 bootstrap question (with default path) plus 1 optional config field. Operators with regulated requirements now have a point of contact in the HANDBUCH instead of needing consulting conversations. Anyone who actually carries out the sovereignty switch follows external tool docs (Codeberg, Mistral, etc.) — the framework makes no own setup specifications there.

## Still Open / Follow-ups

- **DPO skill SecondBrain docs** (follow-up task from Wave J): fill `03 Bereiche/Skills/dpo.md` + `dpo.en.md` analogous to the `security-architect.md` docs. Caught up in this wave.
- **Sovereignty stack practice example:** fully switching one concrete Owlist project to an EU stack (e.g. mirroring INTENTRON itself to Codeberg) would be a good "show, don't tell" follow-up step. Own spec due.
- **`meta.json.llm_routing` aggregation in `/sprint-review`:** if operators actively use `llm_proxy_url`, the sprint review could report a `proxy_active` quota. Own spec due.
- **Appendix R (INTENTRON multi-tool adoption):** consulting idea running in parallel — how do operator teams combine INTENTRON with Spec Kit, Cursor and other tools? Own wave.

## References

- Specs: `specs/BOO-70.md`, `specs/BOO-71.md`
- HANDBUCH: Appendix P Deployment scenarios, Appendix Q Sovereignty stack guide
- Bootstrap question: `bootstrap/SKILL.md` §A.7
- environment.json schema: `bootstrap/references/file-templates.md` §`.claude/environment.json`
- implement skill: `implement/SKILL.md` step 0 point 7
- Migration: `bootstrap/scripts/migrate-to-v2.sh` (`migrate_boo_70`, `migrate_boo_71`)
- Migration checklist: §BOO-70, §BOO-71
- Feedback source: Operator Martin, 2026-05-27
- Linear: <https://linear.app/owlist/issue/BOO-70/> + <https://linear.app/owlist/issue/BOO-71/>
- Previous wave: `docs/releases/wave-j-privacy-by-design.md`
