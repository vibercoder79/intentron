# Runbook: Code Quality & Tech Debt — how a CTO secures quality with INTENTRON

> **Audience:** CTO or Head of Engineering evaluating whether to adopt this framework.
> Answered in under ten minutes: when my team writes code with AI — how is code quality ensured? How
> do I keep a silent pile of technical debt from growing? Which quality gates apply, how does a story
> move from idea to merge, and where do I, as a leader, take control?
>
> **What this runbook is — and is not.** This is the entry-point lens for the engineering view. It
> introduces **no new mechanism** — it bundles what already lives in the repo: the gates, the story
> lifecycle, the artefacts. If you then want to check *which question* is answered by *which proof*
> at *which place*, read the [audit perspective](audit-perspective.en.md).

## In one sentence

INTENTRON forces every AI-written change through a chain of quality gates — from the spec before
the first commit to the required status check in CI — so that no code reaches your `main` without a
documented intent, without a linter run, and without docs in sync.

## The big picture

![INTENTRON's four quality-gate layers](../quality-gate-four-layers.en.png)

The gates apply in four layers, getting stricter from left to right. Layer 0 catches unsafe patterns
**before** the AI writes them to disk. Layer 1 gives real-time feedback in the IDE. Layer 2 blocks
locally at commit. Layer 3 is the final, non-bypassable instance in CI. The further right, the more
binding — and the harder to bypass.

## Your three core concerns

Three risks weigh on every engineering leader the moment AI enters the picture. The framework
addresses each with a concrete mechanism.

### 1. "Code appears without a documented intent."

AI quickly delivers something that runs — but in six months nobody remembers *why* it was built that
way. That is the origin of tech debt: undocumented decisions nobody questions anymore.

The framework flips this: before any commit, a spec must exist (`specs/{ISSUE-ID}.md`, **Spec-Gate**,
BOO-23). The spec carries mandatory frontmatter — `story_id`, `change_type`, `estimate`,
`token_estimate`, `execution_mode`, `estimation_basis` — and a **Definition of Done** as a mandatory
section. No spec file, no commit. The intent is fixed before the first line is written.

### 2. "Nobody guarantees the linter, security scan, and tests actually ran."

With manual work you relied on discipline. At AI speed that is not enough. The framework wires the
checks across four layers so that a bypass becomes visible.

Layer 2 (CLI / pre-commit) blocks locally and hard: ESLint, Semgrep (SAST), dependency check,
coverage gate. Whoever bypasses this locally with `git commit --no-verify` runs into Layer 3 (CI /
GitHub Actions): required status checks cannot be defeated with `--no-verify`. The hard instance sits
server-side, not on the developer's laptop.

### 3. "The docs drift away from reality."

Stale documentation is tech debt in text form. It costs every new developer hours and leads to wrong
decisions.

**doc-version-sync** is a hard gate against version drift: if `CLAUDE.md`, `ARCHITECTURE_DESIGN.md`,
and `GOVERNANCE.md` diverge, the gate blocks. The CI workflow `docs-drift.yml` additionally checks
DE/EN parity and the consistency between skill definition and README. Docs that are out of sync do
not pass.

## The quality gates — how it interlocks

A story moves through a fixed lifecycle:
`/intent` → `/ideation` → `/backlog` → `/implement` → `/architecture-review` → `/sprint-review` →
`/pitch`. Each quality-relevant step has a gate or mechanism attached that leaves a verifiable
artefact behind.

| Lifecycle step | Mechanism / gate | Artefact / proof |
|---|---|---|
| `/ideation` (shape the story) | Reads the **Learning Loop** and warns about known anti-patterns from earlier sprints | `journal/learnings.md` (L1) → woven into the story |
| Before every commit | **Spec-Gate** (BOO-23): blocks commit without `specs/{ISSUE-ID}.md`; mandatory frontmatter + Definition of Done | `specs/{ISSUE-ID}.md` |
| While writing (AI edit) | **Layer 0 — Edit-Bodyguard** (BOO-86): pre-write check for secrets and unsafe patterns | intercepted edit (warning, before write) |
| While typing (IDE) | **Layer 1 — IDE**: real-time feedback | inline markers in the editor |
| `git commit` (local) | **Layer 2 — CLI / pre-commit**: ESLint, Semgrep (SAST), dependency check, coverage gate — **hard block** | SARIF / JUnit / coverage in `journal/reports/` |
| `/implement` (per run) | Writes the **audit-trail** block (BOO-19): `## Session-Referenz` with commit SHA + session ID + log path into the spec | `## Session-Referenz` in `specs/{ID}.md`; `meta.json` per run |
| Push / merge | **Layer 3 — CI / GitHub Actions**: required status checks against `git commit --no-verify` | green CI run; reports in `journal/reports/` |
| Push (docs) | **doc-version-sync** (hard gate): blocks on version drift across `CLAUDE.md` / `ARCHITECTURE_DESIGN.md` / `GOVERNANCE.md`; `docs-drift.yml` checks DE/EN + skill↔README | green `docs-drift.yml` run |
| `/architecture-review` | Checks the active quality dimensions (`ARCHITECTURE_DESIGN.md` §5) and tech-debt risks | review notes against the active dimensions |
| `/sprint-review` | Governance-drift check (does the project live its `governance_mode`?), anti-pattern self-diagnosis, lessons L1/L2/L3 | sprint report; learning entry |

### How the audit trail closes the gap

The most important building block against "undocumented AI code" is the audit trail (BOO-19). Every
`/implement` run writes a `## Session-Referenz` block into the spec — commit SHA, session ID, log
path. With it, any commit can later be traced back: from commit to spec to intent to AI session. The
script [`audit-trace.sh`](../../bootstrap/scripts/audit-trace.sh) reconstructs this chain. You see not
only *what* changed, but *from which intent*.

### How the Learning Loop prevents tech-debt repetition

An anti-pattern that once caused pain should not arise twice. The Learning Loop captures it and feeds
it back:

| Level | Storage | When |
|---|---|---|
| **L1** | `journal/learnings.md` (default) | appended after each sprint review |
| **L2** | `journal/learnings/` (quarterly) | more structured consolidation |
| **L3** | SQLite | from many sprints onward, for cross-sprint trends |

`/ideation` reads the learnings while shaping a new story and warns when a known anti-pattern looms.
That way, what was learned yesterday flows into today's story definition.

### `governance_mode` — gate strictness scales with risk

Not every project needs full severity. `governance_mode` in
[`CONVENTIONS.md`](../../CONVENTIONS.md) scales the gates along the risk (the three modes are
described in detail in the [HANDBUCH](../../HANDBUCH.md#governance-modi-lite-standard-heavy)).

| Mode | Adds over the previous one |
|---|---|
| `lite` | lightest mode |
| `standard` | security gates, CI lint/SAST, sensitive paths, Learning Loop L1 |
| `heavy` | coverage/performance gates, SonarQube, branch protection, audit trail, mandatory review, Learning Loop L2/L3 |

A throwaway script runs `lite`. A regulated production service runs `heavy`. You choose the severity
per project — the mechanism stays the same.

## Artefacts & skills

Every gate leaves a verifiable proof. These are the artefacts that document code quality:

| Artefact | What it proves |
|---|---|
| `specs/{ID}.md` | Documented intent per story + Definition of Done + audit-trail block |
| `ARCHITECTURE_DESIGN.md` | Central hub: active quality dimensions (§5), architecture decisions |
| [`CONVENTIONS.md`](../../CONVENTIONS.md) | Gate architecture, `governance_mode`, `execution_isolation`, active gates |
| `GOVERNANCE.md` | The project's governance ruleset |
| `journal/reports/` | SARIF (linter/SAST), JUnit (tests), coverage per run |
| `meta.json` | Run metadata per `/implement` run |
| `DEVELOPER_ONBOARDING.md` | Handover knowledge for autonomous teams and tool switches |

> The code-formatted artefacts (`specs/`, `ARCHITECTURE_DESIGN.md`, `GOVERNANCE.md`, `DEVELOPER_ONBOARDING.md` …) are generated **in your project** at bootstrap — they do not live in the framework repo. Their templates are under `bootstrap/references/`.

The quality-relevant lifecycle steps are implemented as skills: `/ideation`, `/implement`,
`/architecture-review`, `/sprint-review`. The gate architecture (4 layers, Spec-Gate,
`governance_mode`) is anchored in [`CONVENTIONS.md`](../../CONVENTIONS.md).

## Where you take control

The framework is not rigid. You set these levers as CTO — per project, matched to the risk:

| Lever | What it controls |
|---|---|
| **`governance_mode`** (`lite` / `standard` / `heavy`) | the baseline strictness of all gates in one move |
| **Coverage thresholds** | how strictly the coverage gate blocks |
| **Active quality dimensions** (`ARCHITECTURE_DESIGN.md` §5) | which quality attributes `/architecture-review` and `/sprint-review` check |
| **Learning Loop level** (L1 / L2 / L3) | how deeply the framework learns from past sprints |
| **`execution_isolation`** | how AI workers are isolated from each other during parallel work |

Rule of thumb: the higher the project's risk, the higher `governance_mode`, the stricter the
coverage threshold, the more active quality dimensions.

## Limits — what the framework does NOT do

An honest expectation protects against disappointment. Three things the framework deliberately does
not do.

- **Gates enforce the *existence* of proof, not its *substantive quality*.** The Spec-Gate checks
  that a spec is there — not that it is well written. The coverage gate checks that the linter ran —
  not that the tests are meaningful. doc-version-sync checks that the docs are in sync — not that
  they are understandable. The substantive bar is still set by people.
- **No speed or velocity metrics.** This is by design, not a gap. The Code-Crash stance per
  Schrader: velocity as a steering metric is obsolete. The framework measures proof and quality, not
  story points per sprint.
- **Four-eyes is a convention, not enforced** (BOO-72). The framework documents the four-eyes
  principle as operator discipline but does not enforce it automatically today. If you need it
  binding, check manually or via branch protection in `heavy` mode.

## Further reading

- [`CONVENTIONS.md`](../../CONVENTIONS.md) — the gate architecture (4 layers, Spec-Gate),
  `governance_mode`, `execution_isolation`, active gates in detail.
- [`HANDBUCH.md`](../../HANDBUCH.md) — the complete setup and operations handbook; the gates are in
  [chapter 8 — Die Guardrails](../../HANDBUCH.md#8-die-guardrails--dein-sicherheitsnetz), the
  artefacts in [chapter 7](../../HANDBUCH.md#7-die-artefakte--was-entsteht-wo-und-warum).
- [`ARCHITECTURE_DESIGN` template](../../bootstrap/references/architecture-design-template.en.md) — the
  template base of the architecture hub (your project turns it into `ARCHITECTURE_DESIGN.md` with the
  active quality dimensions §5).
- [`GOVERNANCE` template](../../bootstrap/references/governance-template.en.md) and
  [`DEVELOPER_ONBOARDING` template](../../bootstrap/references/developer-onboarding-template.en.md) — the
  template bases from which `GOVERNANCE.md` and `DEVELOPER_ONBOARDING.md` are generated in your project.
- [`audit-perspective.en.md`](audit-perspective.en.md) — how an auditor checks the proof
  (question → proof → place).
- [`../quality-gate-four-layers.excalidraw`](../quality-gate-four-layers.excalidraw) — the source of
  the big-picture diagram.
- [`../how-we-document.md`](../how-we-document.md) — how the documentation layers connect.
- [`../glossar.md`](../glossar.md) — the terms (spec, quality gate, `governance_mode` …).
