# Release Notes - Wave H Documentation SSoT & Onboarding

> 🌐 **Language:** English (this file) · [🇩🇪 Deutsch](wave-h-documentation-ssot-onboarding.md)

Status: 2026-05-20

## Purpose

Wave H closes BOO-64 through BOO-67. The framework now explicitly makes project documentation a contract: Bootstrap queries the documentation SSoT, developer onboarding is generated as a standard artifact, and runtime and story spec preflight prevent blind implementation against false assumptions.

## Affected Stories

- BOO-64
- BOO-65
- BOO-66
- BOO-67

## What Users Get with the New Setup

- a clear documentation anchor per project instead of scattered tool notes,
- a standardized developer onboarding for new developers, external teams and tool changes,
- preflight checks that surface runtime, story spec, relevant SSoTs and maintenance obligations before implementation,
- migration guidance for existing projects so the new artifacts can be added additively.

## Documentation SSoT Options

Bootstrap establishes the decision on the leading documentation location as a project contract:

- `Obsidian` for knowledge-centric project work with hub, governance, ADRs and daily-note connection,
- `Repo docs` for code-adjacent projects where Markdown in the repository is leading,
- `External DMS` for organizations with an existing document management system, provided the framework only links and does not duplicate,
- `undecided` as an explicit interim state that triggers follow-up work instead of silently making assumptions.

## Developer Onboarding as Standard Artifact

The developer onboarding is now a mandatory artifact for projects in which new developers, external teams or other AI coding runtimes are to work productively. It lists:

- Project Hub or leading DMS,
- architecture and governance documents,
- security and secrets rules,
- backlog and story spec conventions,
- first safe steps up to the first story.

Sprint Review and Implementation must maintain the onboarding as soon as runtime, SSoT, security rules, backlog conventions or central artifacts change.

## Runtime/Story Spec Preflight

Before implementation, it is not only asked which story is being implemented, but whether the local context is viable:

- runtime clarified: Claude, Codex, cross-tool or another environment,
- story spec present and suited to the work,
- documentation SSoT known,
- developer onboarding present or deliberately marked as a migration gap,
- security and secrets rules read,
- open maintenance items for Sprint Review or Implementation captured.

## Migration and Action Required for Existing Projects

Existing projects do not need to be re-bootstrapped. The recommended path is additive:

1. Determine the documentation SSoT and record it in the project contract.
2. Derive the developer onboarding from existing hub, architecture, security and backlog documents.
3. Add runtime and story spec preflight to the implementation routine.
4. Document Sprint Review maintenance obligations for onboarding and SSoT.
5. Check external DMS references and mark dead links as blockers.

## New Sketch Artifacts

- `docs/project-documentation-ssot.excalidraw`
- `docs/project-documentation-ssot.en.excalidraw`
- `docs/foreign-developer-onboarding-flow.excalidraw`
- `docs/foreign-developer-onboarding-flow.en.excalidraw`

## Open Follow-Up Work

- External DMS are only linked in the framework as long as no concrete integration has been agreed. This leaves open items for link validation, access rights, owner and update responsibility.
- Optional: later generate PNG exports if the sketches are to be embedded directly in README, handbook or presentations.
- Optional: extend existing project templates with project-specific examples for Obsidian, Repo docs and DMS.
