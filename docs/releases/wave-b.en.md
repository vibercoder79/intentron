# Release Notes — Wave B

> 🌐 **Language:** English (this file) · [🇩🇪 Deutsch](wave-b.md)

Status: 2026-05-19

## Purpose

Wave B hardens tooling, architecture, and security-by-design. The changes turn the previous guidance into binding story and implementation rules: Security Impact must be visible in stories, Security Validation must be evidenced before `Done`, and post-implement validation is described as a Validate-Fix-Learn loop.

## Affected Stories

- BOO-55
- BOO-56
- BOO-57

## Implemented Focus Areas

### Hook layer instead of git-hook shorthand

`bootstrap/references/hooks-setup.md` and the English variant now explain three layers:

- AI runtime hook,
- local git hook,
- CI gate.

This makes it clear: governance hooks are coding/runtime hooks of the respective tool. Git hooks and CI can mirror the same rule, but they do not replace the project contract in `CONVENTIONS.md`.

### Architecture context validation

`ARCHITECTURE_DESIGN.md` gets a context validation in the template. Blueprint rules are therefore no longer merely generic but must fit the concrete project situation: critical dimensions, lightweight dimensions, external providers, security/privacy boundaries, and assumptions for the first real implementation run.

### Security-by-design in stories

Feature and fix templates now contain:

- `Security Impact`,
- `Security Validation`.

Every story must declare its change type. For code, security, tooling, dependency, CI, or governance changes, concrete validation evidence must be documented before `Done`.

### Implement as Validate-Fix-Learn

`implement/SKILL.md` and `implement/SKILL.en.md` now describe post-implement validation explicitly as a loop:

```text
Validate -> Interpret -> Decide -> Fix -> Re-Validate -> PASS/FAIL -> Learn
```

Important: a failed gate is first interpreted, then fixed in a targeted way, then validated again. Repeatable patterns are written into the active learning loop.

## Reference Matrix

| Reference | Wave B relation |
|---|---|
| F007 | Architecture template extended with context validation |
| F008 | Hook term clarified as runtime/coding hook |
| F012 | Architecture template remains the place for AI architecture principles and anti-patterns |
| F014 | Tooling/gate layers more clearly separated |
| F015 | Standard dimensions remain a contract, context validation makes them project-specific |
| F016 | Three-layer gate logic sharpened |
| F023 | `implement` reads/checks `SECURITY.md` and the security reference stack more bindingly |
| F024 | Security Impact / Security Validation anchored in story templates |
| F025 | Architecture/security blueprints must be validated against the project context |

## Changed Artifacts

- `bootstrap/references/architecture-design-template.md`
- `bootstrap/references/architecture-design-template.en.md`
- `bootstrap/references/hooks-setup.md`
- `bootstrap/references/hooks-setup.en.md`
- `bootstrap/references/security-template.md`
- `bootstrap/references/security-template.en.md`
- `ideation/references/story-template-feature.md`
- `ideation/references/story-template-feature.en.md`
- `ideation/references/story-template-fix.md`
- `ideation/references/story-template-fix.en.md`
- `implement/SKILL.md`
- `implement/SKILL.en.md`

## Migration Note

Existing projects do not need to be blindly overwritten. At the next upgrade, they should extend their story templates with `Security Impact` and `Security Validation` and check whether `SECURITY.md` as well as sensitive-paths files are present.
