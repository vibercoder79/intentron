# Release Notes — Wave F Security Documentation Model

> 🌐 **Language:** English (this file) · [🇩🇪 Deutsch](wave-f-security-doc-model.md)

Status: 2026-05-19

## Purpose

Wave F closes BOO-62. The framework now explains security not only through individual gates, but as a coherent documentation model: `ARCHITECTURE_DESIGN.md` leads, `SECURITY.md` operationalizes, and sub-artifacts provide evidence and technical enforcement.

## Affected Story

- BOO-62

## Implemented Focus Areas

### Architecture references Security

`bootstrap/references/architecture-design-template.md` and `.en.md` now contain:

- `SECURITY.md` in the references table,
- a security reference model,
- the explanation that `ARCHITECTURE_DESIGN.md` leads security as a quality dimension and boundary, while `SECURITY.md` is the operational security contract.

### Security references sub-artifacts

`bootstrap/references/security-template.md` and `.en.md` now contain:

- security sub-artifacts with purpose and update trigger,
- `API_INVENTORY.md`,
- `.semgrep.yml`,
- `.codex/hooks.json` / `.claude/settings.json`,
- `.claude/sensitive-paths.json` / `.codex/sensitive-paths.json`,
- Threat Models,
- privacy/compliance documents,
- security-by-design flow.

### Handbook reading guidance

`HANDBUCH.md` now contains a coherent chapter on the security documentation model in DE and EN:

`ARCHITECTURE_DESIGN.md -> SECURITY.md -> security sub-artifacts`

The roles of `/ideation`, `/implement`, `/security-architect`, `/architecture-review` and `/sprint-review` are explained within it.

## Changed Artifacts

- `HANDBUCH.md`
- `bootstrap/references/architecture-design-template.md`
- `bootstrap/references/architecture-design-template.en.md`
- `bootstrap/references/security-template.md`
- `bootstrap/references/security-template.en.md`

## Open Follow-Up Work

- Optional: later add a dedicated security flow sketch in the Olli corporate design, if the handbook chapter should be guided even more strongly visually.
