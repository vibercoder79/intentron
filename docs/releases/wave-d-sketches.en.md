# Release Notes — Wave D Sketches

> 🌐 **Language:** English (this file) · [🇩🇪 Deutsch](wave-d-sketches.md)

Status: 2026-05-19

## Purpose

Wave D closes BOO-59 visually. The previously text-described Codex, cross-tool, Validate-Fix-Learn, provider, and upgrade views are now available as Excalidraw sources in the Olli corporate design.

## Affected Story

- BOO-59

## Implemented Focus Areas

### Runtime-specific artifact maps

The Codex Artifact Map clearly separates between:

- `AGENTS.md`, `CONVENTIONS.md`, and `ARCHITECTURE_DESIGN.md` as the project contract,
- `.codex/skills`, `.codex/hooks.json`, and `.codex/config.toml` as the Codex runtime,
- `CLAUDE.md` and `.claude/*` as the compatibility bridge,
- `specs/`, `intents/`, `journal/`, and `docs/releases/` as the evidence trail.

The cross-tool map shows the same contract as the shared center for Claude Code, Codex, and further tool adapters.

### Validate-Fix-Learn as a visible loop

The implement workflow is now documented not only textually but also visually as a loop:

`Validate -> Interpret -> Decide -> Fix -> Re-Validate -> PASS/FAIL -> Learn`

This makes it visible that `/implement` does not end after the first tool run. Completion only happens at PASS or with documented operator approval.

### Follow-up views for BOO-58 and BOO-60 prepared

BOO-59 also provides the visual foundations for the next operational steps:

- Provider postflight matrix for BOO-58,
- Upgrade path for existing projects for BOO-60,
- Runtime decision tree for tool-neutral bootstrap decisions,
- Backlog-record/adapter model for Linear, GitHub Issues, and local backlogs.

## New Artifacts

German:

- `docs/artifact-map-codex.excalidraw`
- `docs/artifact-map-cross-tool.excalidraw`
- `docs/runtime-decision-tree.excalidraw`
- `docs/backlog-record-adapter-model.excalidraw`
- `docs/validate-fix-learn.excalidraw`
- `docs/provider-postflight-matrix.excalidraw`
- `docs/upgrade-path-existing-projects.excalidraw`

English:

- `docs/artifact-map-codex.en.excalidraw`
- `docs/artifact-map-cross-tool.en.excalidraw`
- `docs/runtime-decision-tree.en.excalidraw`
- `docs/backlog-record-adapter-model.en.excalidraw`
- `docs/validate-fix-learn.en.excalidraw`
- `docs/provider-postflight-matrix.en.excalidraw`
- `docs/upgrade-path-existing-projects.en.excalidraw`

## Open Follow-up Work

- Generate PNG exports if the sketches are to be embedded directly in README, GitHub preview, or presentations.
- Operationalize provider postflight from BOO-58 as a machine-readable checklist.
- Operationalize the upgrade path from BOO-60 as a concrete `inspect/apply-safe/apply-with-confirmation` flow.
