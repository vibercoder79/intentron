# Release Notes — Wave E Provider and Upgrade

> 🌐 **Language:** English (this file) · [🇩🇪 Deutsch](wave-e-provider-upgrade.md)

Status: 2026-05-19

## Purpose

Wave E operationalizes BOO-58 and BOO-60. Bootstrap now distinguishes skill installation from provider readiness and describes a safe upgrade path for existing projects.

## Affected Stories

- BOO-58
- BOO-60

## Implemented Focus Areas

### Provider postflight

New is `bootstrap/references/provider-postflight.md` including an English variant. The completion report must list GitHub, backlog adapter, research, Visualize/Miro, monitoring, and Obsidian separately:

- `OK`: chosen and verified or deliberately actively confirmed,
- `WARN`: artifact present, external verification missing,
- `SKIP`: deliberately not used,
- `FAIL`: should be active, but is blocked or failed.

Secrets are never displayed or written to repo files, chat, logs, `.env.example`, or completion reports.

### Monitoring, research, and visualize

Bootstrap now operationally asks about:

- central or project-local monitoring/logging platform,
- logging contract with mandatory fields and forbidden content,
- research source: framework, companion, installed globally, or not used,
- research provider: Perplexity MCP, Perplexity API, OpenRouter, or no provider,
- Visualize/Miro with Miro MCP check and fallback Excalidraw/Mermaid.

### Upgrade path

New is `bootstrap/references/framework-upgrade.md` including an English variant. Existing projects are not re-bootstrapped and not blindly overwritten. The three modes are:

- `inspect`: only read and show diff/risk/TODOs,
- `apply-safe`: only add new files or missing sections additively,
- `apply-with-confirmation`: confirm each potentially overwriting change individually.

The upgrade report can be stored under `journal/reports/framework-upgrade/YYYY-MM-DD.md` and uses `docs/releases/` as migration input.

## Changed Artifacts

- `bootstrap/SKILL.md`
- `bootstrap/SKILL.en.md`
- `bootstrap/README.md`
- `bootstrap/README.en.md`
- `bootstrap/references/provider-postflight.md`
- `bootstrap/references/provider-postflight.en.md`
- `bootstrap/references/framework-upgrade.md`
- `bootstrap/references/framework-upgrade.en.md`
- `bootstrap/references/optional-components.md`
- `bootstrap/references/optional-components.en.md`
- `HANDBUCH.md`

## Open Follow-up Work

- Optional: later decouple provider postflight as a machine-readable template or script.
- Optional: later implement the upgrade mode as a dedicated script instead of a purely operational skill instruction.
