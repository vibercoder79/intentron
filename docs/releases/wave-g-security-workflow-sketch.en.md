# Release Notes — Wave G Security Workflow Sketch

> 🌐 **Language:** English (this file) · [🇩🇪 Deutsch](wave-g-security-workflow-sketch.md)

Status: 2026-05-19

## Purpose

Wave G complements BOO-63. The security documentation model from Wave F is now also available visually as an Excalidraw sketch.

## Affected Story

- BOO-63

## New Artifacts

- `docs/security-workflow.excalidraw`
- `docs/security-workflow.en.excalidraw`

## Content of the Sketch

The sketch shows:

- `ARCHITECTURE_DESIGN.md` as the lead contract,
- `SECURITY.md` as the operational security contract,
- security sub-artifacts such as `API_INVENTORY.md`, `.semgrep.yml`, runtime hooks, sensitive paths, Threat Models and privacy/compliance documents,
- the skill pipeline `/ideation` -> `/implement` -> `/security-architect` -> `/architecture-review` -> `/sprint-review`,
- the feedback of recurring findings into the learning loop,
- the hard rule that secrets, tokens, cookies and private session data are never written.

## Handbook

`HANDBUCH.md` references the DE/EN Excalidraw sources in the security documentation model section.

## Open Follow-Up Work

- Optional: generate PNG exports if the sketch is to be embedded directly in the GitHub README or in presentations.
