# Wave AI — Enterprise-Readiness (BOO-100…103)

> 🌐 **Language:** English (this file) · [🇩🇪 Deutsch](wave-ai-enterprise-readiness.md)

Four connected building blocks from the enterprise preparation 2026-06-01. Pure documentation + one modular opt-in compliance catalog. No intervention in the core pipeline.

## BOO-100 — Value-Prop-Frame
README „Why INTENTRON" + HANDBUCH §1 (DE+EN) extended with the frame „faster AND compliant — violations are caught in the commit, not in the downstream audit". Names the CISO/auditor as the problem figure; backed by gates (sensitive-paths/personal-data, Layer-0-Bodyguard), spec linkage, audit-trace.sh, heavy mode.

## BOO-101 — EU AI Act modular
New dpo control catalog `dpo/controls/eu-ai-act.yml` (same schema, auto-loaded by the AUDIT runner) + `dpo/references/ai-system-template.md` (`AI_SYSTEM.md` template). Bootstrap add-on `[ ] EU AI Act` (strictly opt-in, requires Privacy). Covers AI Regulation documentation obligations (risk class, transparency, human oversight, logging, GPAI) — judgment checks as REVIEW-NEEDED, NO legal advice. No new skill/runner/dependency.

## BOO-102 — Integration-Discovery-Questionnaire
`docs/onboarding/integration-discovery.md` (+ .en): 7 question clusters for the customer-specific integration/CI part (hosting, CI/CD, interfaces, network, secrets, compliance, RACI/go-live) — what the customer IT must clarify in advance so the solution integrates into the live environment.

## BOO-103 — Audit/CISO Runbook
`docs/runbooks/audit-perspective.md` (+ .en): „audit question → evidence → location" table + check steps + caveats. Aggregates existing evidence (spec gate, audit-trace.sh, journal/reports, branch protection, dpo-audit.py, verify-setup, four-eyes). Plus: dead `GOVERNANCE.md` link in `audit-trace.sh` fixed.

Specs: `specs/BOO-100.md`…`BOO-103.md`. Release: v0.7.0.
