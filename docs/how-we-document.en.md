# How this framework documents (How We Document)

> Consolidated entry point (BOO-130): **which** doc artifacts exist, **where** they live, **how documentation stays continuous**, and **how an existing repo** is brought up to date. The details are spread out (HANDBUCH §7, Block C, hooks) — this page is the map. DE: [`how-we-document.md`](how-we-document.md).

## Principle: Docs-as-Code, enforced continuously

Documentation is **versioned Markdown in the same repo as the code** — not a separate wiki that rots. It travels **in the same PR as the change** and is **enforced by git hooks**, not hoped for via discipline. Guiding rule: *docs-in-sync* — every finished story carries its affected doc artifacts along.

## 1) The artifacts — what's created, where

Always scaffolded at bootstrap (BOO-61 baseline), then maintained continuously:

| Artifact | Purpose |
|---|---|
| `CLAUDE.md` / `AGENTS.md` | runtime entry for the AI (incl. session-start routine, BOO-129) |
| `CONVENTIONS.md` | tool/adapter contract (runtime, backlog, gates) |
| `ARCHITECTURE_DESIGN.md` | **hub** — §9 auto-links all doc layers |
| `GOVERNANCE.md` / `SECURITY.md` | governance rules · threat model (fill SECURITY.md via `security-architect`) |
| `specs/<PREFIX>XXX.md` | story spec — required before any code change (spec gate) |
| `INDEX.md` | project file index |
| `journal/` | reports, sprint/learning entries |
| `docs/project/{README, decisions/, meetings/, research/}` | project doc SSoT on `repo-docs` (PMO hub + ADRs + minutes) |
| `DEVELOPER_ONBOARDING.md` | onboarding for new people/tools |

Full table + owners: **HANDBUCH §7 "The artifacts — what's created, where, and why"**.

## 2) The three doc layers (Block C)

1. **Story specs** (repo) — one spec per story, ground truth for implement.
2. **Project docs** — Obsidian vault **or** `docs/project/` (repo-docs) **or** external DMS (with a repo pointer).
3. **Component/architecture docs** — per component, under the hub.

**Hub & auto-linking:** `ARCHITECTURE_DESIGN.md §9` registers every new `*.md` automatically. SSoT variant choice: `references/project-documentation-ssot.en.md`.

## 3) How "continuous" is enforced (gates)

| Mechanism | Effect |
|---|---|
| `spec-gate.sh` | no commit with a story reference without `specs/<PREFIX>XXX.md` |
| `doc-version-sync.sh` | **HARD GATE** — no `git push` on version drift between DOC_FILES |
| `orphan-check.sh` (opt-in) | no doc without a hub entry (§9) |
| **session-start routine** (BOO-129) | on `repo-docs`: Claude reads the PMO hub + latest `meetings/`/`decisions/`, writes back at the end → the markdown folders become a living "brain" |
| **docs-in-sync principle** | per story-done: carry along HANDBUCH/specs/release notes/backlog |

Against **drift / "wiki rot"** (the dominant failure mode of wikis), the Docs-as-Code coupling + these gates are the structural counter.

## 4) Bringing an existing / foreign repo up to date

"Read the repo, do an architecture review, bring the docs up to date" is a defined path:

1. **`/architecture-review`** reads the code + checks the 8 AI-architecture checks.
2. **Existing-project onboarding** (HANDBUCH **Appendix U**) + **`references/framework-upgrade.en.md`** (`inspect` → `apply-safe` → `apply-with-confirmation`) pull artifacts in idempotently (`migrate-to-v2.sh --issue BOO-XX`).
3. Result report to `journal/reports/framework-upgrade/YYYY-MM-DD.md`; deliberate deviations are **documented, not overwritten**.

## References

HANDBUCH §7 (artifacts) · Block C / §6 · `references/project-documentation-ssot.en.md` · Appendix T (verification) · Appendix U (existing-project onboarding) · BOO-129 (session-start loop). Terms unclear? → glossary (Appendix C / `docs/glossar.en.md`).
