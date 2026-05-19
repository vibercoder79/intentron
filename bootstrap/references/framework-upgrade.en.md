# Framework Upgrade for Existing Projects

Goal: Existing projects can adopt a new Code-Crash Framework version without blindly overwriting local decisions, skills, hooks, CI, or security files.

## Base rule

Project-local skills are a reproducible project state. An upgrade is a conscious project decision and is versioned.

## Upgrade modes

| Mode | Behavior |
|---|---|
| `inspect` | Reads current state, framework version, and target version. Shows diff, risks, and manual TODOs. Writes no project files. |
| `apply-safe` | Adds only new files or missing sections. Existing content is not replaced. |
| `apply-with-confirmation` | Asks for every potentially overwriting change individually. |

## User flow

1. Check Git worktree: clean or save changes.
2. Determine current framework version and source.
3. Pull the new framework version into a temporary folder.
4. Compare project-local skills.
5. Adopt new skill versions only according to the selected mode.
6. Migrate project contract and runtime mapping.
7. Add new required artifacts as skeletons without overwriting local content.
8. Run provider postflight in upgrade mode.
9. Review the diff.
10. Commit and push only after operator confirmation.

## File categories

| Category | Upgrade behavior |
|---|---|
| Project-local skill copies | Update only after diff/backup or version note. |
| `CONVENTIONS.md` | Do not replace; merge new sections or mark as TODO. |
| `AGENTS.md` / `CLAUDE.md` | Do not replace; add precedence and runtime bridge. |
| Architecture/security files | Never overwrite wholesale; insert new required sections or mark as TODO. |
| `.codex/hooks.json` / `.claude/settings.json` | Register new hooks while preserving existing entries. |
| `.env`, secrets, local reports | Never touch, never commit, never copy into reports. |

## Upgrade report

Recommended path:

```text
journal/reports/framework-upgrade/YYYY-MM-DD.md
```

Report skeleton:

```markdown
# Framework Upgrade Report

Date: YYYY-MM-DD
Mode: inspect | apply-safe | apply-with-confirmation

## Versions

- Old version / source:
- New version / commit:

## Updated skills

| Skill | Old | New | Decision |
|---|---|---|---|

## Newly created files

- ...

## Changed project contract sections

- `CONVENTIONS.md`: ...
- `AGENTS.md`: ...
- `CLAUDE.md`: ...

## Intentionally not overwritten

- ...

## Manual TODOs

- ...

## Provider postflight

| Provider | Status | Next action |
|---|---|---|

## Operator approval

- Diff reviewed:
- Commit allowed:
```

## Release notes rule

Before every upgrade, read `docs/releases/`. Each release note states:

- migration needs,
- new required artifacts,
- optional follow-up work,
- provider/secret notes,
- breaking changes or deliberate non-changes.

The upgrade path uses those release notes as input for the report.
