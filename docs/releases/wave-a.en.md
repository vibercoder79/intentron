# Release Notes — Wave A

> 🌐 **Language:** English (this file) · [🇩🇪 Deutsch](wave-a.md)

Status: 2026-05-19

## Purpose

Wave A hardens the Codex and dry-run readability of INTENTRON. The focus
is on the bootstrap and contract foundation: runtime selection, artifact baseline,
backlog adapter, postflight, handbook clarification, and upgrade path.

## Affected Stories

- BOO-52
- BOO-53
- BOO-54
- BOO-60
- BOO-61

## Key Clarifications

### Codex-ready framework explanation

The framework is described as a sequential engineering pipeline with quality gates, not as a
fully autonomous developer agent. Codex, Claude, Cursor, or local LLMs are adapters on the same
story contract. Subagents are specialized execution helpers within a controlled
story and remain bound to role, context, write scope, return format, and gates.

### Bootstrap Skill vs. INTENTRON

The Bootstrap Skill installs and initializes a project: governance files, local
skill copies, hooks, optional adapters, and base artifacts. INTENTRON is the
methodology and the object of comparison: conventions, gates, artifacts, roles, and review points.
Bootstrap brings the framework into the project; Bootstrap is not the framework itself.

### Lite / Standard / Heavy

The governance modes are not maturity badges, but friction budgets:

- `lite` omits expensive parts such as heavy CI, SonarQube, branch protection, performance baselines,
  audit trails, and mandatory deep reviews.
- `lite` does not omit: project contract, backlog record, spec, secrets hygiene, local
  base gates, and result note.
- `standard` makes the core gates production-capable: issue/spec gates, security baseline, lint/test,
  CI where available, and sprint review.
- `heavy` adds burden of proof: review, audit, security, compliance, and
  production evidence.

### Backlog tool abstraction

The framework uses the neutral term backlog record. Linear is the recommended adapter,
but not the only valid form. GitHub Issues, Microsoft Planner, or a Markdown backlog
can carry the same record, as long as mandatory fields and gates are preserved.

### Upgrade path for existing projects

Existing projects are not blindly overwritten. The documented upgrade path has three
stages:

1. `inspect`: read the project state and make deviations visible.
2. `apply-safe`: apply only additive, idempotent changes.
3. `apply-with-confirmation`: have every change to existing rules, hooks, CI, templates,
   branch protection, governance mode, adapter configuration, or skill versions
   confirmed.

## Reference Matrix

| Reference | Wave A relation |
|---|---|
| F001 | Confirm `intent` as core set / pipeline entry point |
| F002 | Neutralize backlog record; treat Linear only as adapter |
| F004 | Extend Claude-first target structure with Codex/cross-tool mapping |
| F005 | Governance modes must not break the skill/artifact baseline |
| F006 | Explain `AGENTS.md`, `CLAUDE.md`, and `CONVENTIONS.md` in a role-clean way |
| F009 | Anchor runtime query and transformation logic for Claude Code/Codex/cross-tool |
| F010 | Make the learning-loop level visible as a project-wide contract in postflight |
| F013 | Clarify project identity card per runtime |
| F017 | Pull the repository publish decision into the bootstrap conclusion |
| F018 | Keep artifacts current after bootstrap and mirror them in release notes |
| F019 | Verify external services and providers separately from the local setup |
| Upgrade path | Protect existing projects with `inspect`, `apply-safe`, `apply-with-confirmation` |

## Changed Artifacts

- `HANDBUCH.md`
- `CONVENTIONS.md`
- `bootstrap/SKILL.md`
- `bootstrap/SKILL.en.md`
- `bootstrap/README.md`
- `bootstrap/README.en.md`
- `docs/releases/wave-a.md`

## Not Changed

- No Excalidraw or PNG files.
- No runtime scripts, hook scripts, or CI workflows.
