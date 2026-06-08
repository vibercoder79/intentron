# Release Notes — Wave C

> 🌐 **Language:** English (this file) · [🇩🇪 Deutsch](wave-c.md)

Status: 2026-05-19

## Purpose

Wave C documents the open provider, diagram, and upgrade aspects from the dry run in a way that prevents them from blurring again in the next implementation. The first cut held the visual artifacts as follow-up work; BOO-59 now adds the Excalidraw sources in the Olli corporate design.

## Affected Stories

- BOO-58
- BOO-59
- BOO-60

## Implemented Focus Areas

### Providers are not automatically ready for use

Bootstrap must not confuse local skill files with external provider connections. GitHub, Linear, Jira, Azure DevOps, Planner, SonarQube, Grafana, Miro, Telegram, Obsidian sync, research providers, and hosting platforms need their own status values:

- `OK`
- `WARN`
- `SKIP bewusst`
- `FAIL`

Secrets are never displayed or written to files in the process.

### Upgrade path for existing projects

Existing projects are not overwritten. The safe path is:

1. `inspect` — read the existing state, show diff and risks.
2. `apply-safe` — apply only additive, idempotent changes.
3. `apply-with-confirmation` — change existing rules, hooks, CI, templates, adapters, and skill versions only after confirmation.

### Diagram follow-up work

BOO-59 brings the visual views in as Excalidraw sources:

- Codex Artifact Map: `docs/artifact-map-codex.excalidraw`
- Cross-Tool Artifact Map: `docs/artifact-map-cross-tool.excalidraw`
- Runtime decision tree: `docs/runtime-decision-tree.excalidraw`
- Backlog-record/adapter model: `docs/backlog-record-adapter-model.excalidraw`
- Validate-Fix-Learn loop: `docs/validate-fix-learn.excalidraw`
- Provider postflight matrix: `docs/provider-postflight-matrix.excalidraw`
- Upgrade path for existing projects: `docs/upgrade-path-existing-projects.excalidraw`

All seven sketches are also available as English `.en.excalidraw` variants. PNG exports remain an optional publishing step when the images need to be rendered for README, GitHub, or presentations.

## Reference Matrix

| Reference | Wave C relation |
|---|---|
| F003 | Monitoring/logging needs platform and provider context |
| F011 | Artifact maps must distinguish Claude, Codex, and cross-tool views |
| F020 | Research must be described as a framework component or companion with provider status |
| F021 | Visualize/Miro needs an MCP query and completion verification |
| F022 | Validate-Fix-Learn needs its own operational and visual representation |
| BOO-60 | Upgrade path for existing projects documented |

## Changed Artifacts in This Cut

- `HANDBUCH.md`
- `bootstrap/SKILL.md`
- `bootstrap/SKILL.en.md`
- `docs/*.excalidraw` for BOO-59
- `docs/releases/wave-c.md`

## Open Follow-up Work

- Pull provider postflight out of `bootstrap/SKILL.md` as its own machine-readable template if needed.
- Create an upgrade report as a template in `bootstrap/references/` as soon as the upgrade function is not only documented but scriptable.
