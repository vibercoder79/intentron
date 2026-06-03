# Info-Gathering — Block A (Project core)

The bootstrap skill collects **only project core information** in Block A. Existing infrastructure is explored in Block B, doc architecture in Block C, optional components in Block D.

**Important:** Ask questions **one at a time or in small groups** (max 3 per prompt), not as a batch.

## Required information

| Variable | Question to operator | Example |
|----------|---------------------|---------|
| `STACK_CHOICE` * | Stack question (a/b/c/d/e) — see SKILL.md Phase 1 A.1 | `d) Python` |
| `PROJECT_NAME` * | What is the project called? | `MyAnalytics` |
| `PROJECT_DESC` * | One sentence: what does the system do? | `Data analysis tool for marketing KPIs` |
| `VERSION_START` * | Start version | `0.1.0` |
| `ISSUE_PREFIX` * | Prefix for issues | default derived from project name (e.g. `MA-`) |
| `PRIMARY_LANG` * | Primary language for docs | `de` or `en` (default `de`) |
| `ADDONS` * | Add-ons (multi-select) | see below |
| `GOVERNANCE_MODE` * | Governance intensity | `lite` / `standard` / `heavy` (default `standard`) |
| `EXECUTION_ISOLATION` * | Parallel-agent isolation | `none` / `write-scope` / `git-worktree` (default by mode) |

> **Optional existing-source import (A.2b, BOO-117):** If a source already exists (intent file, existing repo, existing docs), `PROJECT_DESC` — and optionally `PROJECT_NAME` plus a `stack_hint` (correction for A.1) — can be **suggested** from it instead of asked manually. Variable: `SOURCE_IMPORT = {type: intent|repo|doc|none, ref, derived}`. Cleanly optional: default `none`, no breakage without a source, the operator confirms every suggestion. Details: `SKILL.md` §A.2b.

## Add-ons (architecture dimensions)

Standard dimensions (always active, not deselectable):
- Reliability
- Data Integrity
- Security
- Performance
- Observability
- Maintainability

Optional add-ons — operator selects based on project:

| Add-on | When useful | Adds |
|--------|-------------|------|
| **Privacy / GDPR** | Voice assistants, personal data, tier models | Dimension "Privacy" in `ARCHITECTURE_DESIGN.md`, Privacy section in `SECURITY.md`, tier-concept placeholder |
| **Cost Efficiency** | LLM-heavy projects, SaaS subscriptions, rate limits | Dimension "Cost Efficiency", budget rules in `GOVERNANCE.md` |
| **Signal Quality** | ML / analytics / signal systems | Dimension "Signal Quality", evaluation-metrics slot |
| **Compliance** | Regulated industries (health, finance, legal) | Compliance section in `GOVERNANCE.md` and `SECURITY.md`, audit-trail rules |

## Governance intensity

This question is asked by `/bootstrap` in setup block A.5. "Light mode" is the plain-language label; the technical value is `lite`.

| Mode | When useful | Bootstrap effect |
|------|-------------|------------------|
| `lite` | experiments, learning projects, small private scripts | minimal set: `CLAUDE.md`/`AGENTS.md`, `CONVENTIONS.md`, `specs/`, spec-gate, basic linting |
| `standard` | serious solo projects, small production services, client work | default: security gates, issue guidelines, CI lint/SAST, sensitive-paths, learning loop L1 |
| `heavy` | regulated, revenue-critical, auth/payment/PII-heavy or long-lived systems | full set: coverage, performance, SonarQube, branch protection, audit trail, mandatory review, optional L2/L3 |

## Execution isolation

| Value | When useful | Rule |
|-------|-------------|------|
| `none` | linear work only, no parallel agents | `execution_mode: linear` only |
| `write-scope` | subagents with clearly separated file/module scopes | `sub-agents` allowed if `write_scopes` are present in the spec |
| `git-worktree` | parallel agents or agentic backlog execution | `agentic` allowed, each agent gets its own worktree/branch |

Default coupling:
- `lite` → `none`
- `standard` → `write-scope`
- `heavy` → `git-worktree`

## Block B — Existing infrastructure

See separate doc: `existing-infra-check.en.md`. Short form:

| Variable | Question | Options |
|----------|----------|---------|
| `PROJECT_PATH` * | Project directory | exists + path / create new |
| `GITHUB_REPO` | GitHub repo | URL / later / none |
| `DOCUMENTATION_SSOT` * | Documentation SSoT | Obsidian vault / repo docs / external DMS / undecided |
| `OBSIDIAN_VAULT` | Obsidian vault for docs | path / no (only if SSoT is Obsidian) |
| `EXTERNAL_DMS` | External DMS for docs | system + entry point (only if SSoT is external DMS) |
| `BACKLOG_TOOL` | Backlog system | Linear + slug / M365 / GitHub Issues / none |
| `HAS_ENV` | `.env` exists? | yes / no |

## Block C — Doc architecture

See `project-documentation-ssot.en.md` and `doc-architecture-proposal.en.md`. The skill first fixes the documentation SSoT contract from Block B and then presents a 3-layer proposal:
- Story specs (repo)
- Project docs (Obsidian, `docs/project/`, external DMS with local reference file, or repo fallback)
- Component docs (Obsidian or `docs/components/`)
- Architecture guidelines (Obsidian, `docs/`, or external DMS with repo reference)
- Hub: `ARCHITECTURE_DESIGN.md` in repo with §9-references auto-link

Obsidian is the best practice, but not required. With an external DMS, content is not duplicated; `docs/project/README.md` only documents entry point, link convention, and standard artifacts. With `undecided`, bootstrap creates the repo fallback `docs/project/`, marks a TODO, and sets postflight to `WARN`. Operator confirms or adjusts.

## Block D — Optional components

See `optional-components.en.md`. Short form:

| Variable | Question | Default |
|----------|----------|---------|
| `SELF_HEALING` | Set up cron agent? | no |
| `DOC_SYNC_OBSIDIAN` | DocSync to Obsidian vault? | yes (if vault) / no (else) |
| `AUTOMATION_DAEMON` | Linear webhook daemon? | no |
| `LEARNING_LOOP` | Learning-loop level | L1 / L2 / L3 / no (default L1) |

## Label taxonomy

Project-specific labels for the backlog system. Minimum (always):
- `architecture`, `bug`, `feature`, `refactor`, `docs`, `infra`

Depending on activated add-ons:
- Privacy active → `privacy`
- Compliance active → `compliance`

Domain examples (operator extends per project):
- Web app: `frontend`, `backend`, `api`, `ux`
- AI system: `model`, `prompt`, `evaluation`, `data`
- Voice assistant: `voice`, `brain`, `memory`, `tools`, `interfaces`
- Research project: `research`, `analysis`, `hypothesis`
- Backend service: `service`, `infra`, `api`, `db`

## Hook configuration

Governance hooks are installed automatically in Phase 4. See `hooks-setup.en.md`.

No project-specific customization needed — only `PROJECT_PATH` and `ISSUE_PREFIX` in hook scripts.

## No agent/signal requirement

The skill has no assumptions about autonomous agent systems or signal files. If the project needs autonomous agents, that is clarified per story in the project — not in the bootstrap.
