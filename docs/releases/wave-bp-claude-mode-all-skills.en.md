# Wave BP — Claude Code mode recommendation across all skills + grafana/security-architect gaps (BOO-169)

> 🌐 **Language:** English (this file) · [🇩🇪 Deutsch](wave-bp-claude-mode-all-skills.md)

**What's there now:** BOO-168 established the Claude Code mode recommendation for `/implement` and `/sprint-run`. This wave rolls the **same pattern** out to the **13 remaining skills** — every README now carries a `> **Claude Code mode:**` line (DE+EN) at the top, referencing HANDBUCH §6. The §6 table classifies all skills and gains a fourth phase. Two gaps found during review are closed alongside. Pure docs — no version bump except the security-architect frontmatter fix.

## Stories
- **BOO-169** — mode recommendation across all skills + grafana/security-architect gaps.

## Changes (DE+EN)
- **README mode line (DE+EN)** for 13 skills: ideation, intent, pitch, knowledge-onboarding, sprint-review, backlog, architecture-review, security-architect, dpo, visualize, cloud-system-engineer, grafana, bootstrap.
- **HANDBUCH §6 (DE+EN)**: examples column extended to all skills + new fourth row "External/irreversible writes → `default` (ask before edits)" (for `/grafana` + `/cloud-system-engineer` mode C) + note that the table is the central source.
- **security-architect (DE+EN)**: added `recommended_model: opus` + `version: 1.1.0` to the frontmatter (which was incomplete); also added security-architect to `bootstrap/references/model-tiers.json` opus.default_for_skills.
- **grafana SKILL (DE+EN)**: operator confirmation blockquote before `update_dashboard(overwrite=true)` (remote overwrite with no local rollback).

## Mode mapping (short form)
- **Thinking skills → `plan`**: ideation, intent, backlog, architecture-review, security-architect, dpo.
- **Execute supervised → `acceptEdits`**: pitch, knowledge-onboarding, sprint-review, visualize, bootstrap (+ implement, sprint-run from BOO-168).
- **Unattended → `dontAsk` + allowlist**: sprint-review + dpo AUDIT (triggered by the daemon).
- **External irreversible writes → `default`**: grafana, cloud-system-engineer mode C (never unattended).

## Effect
Every skill tells the operator, on invocation, which Claude Code mode to run it in — interactive and (where applicable) unattended. Two frontmatter/gate gaps closed.

## Scope
Pure docs, no code. Version bump only security-architect frontmatter (recommended_model + version, README stays 1.1.0 → docs-drift green). Mode vocabulary consistent with BOO-168 (`plan`/`acceptEdits`/`dontAsk`/`bypassPermissions`/`default`). Wave letter **bp** (bo = runbooks networking BOO-167; bn = Claude mode docs BOO-168).

## References
Spec: `specs/BOO-169.md`. Branch: `feat/boo-169-claude-code-modus-alle-skills`. Related: BOO-168 (mode foundation), BOO-84 (model-tier routing). Operator source: Tobias, 2026-06-06.
