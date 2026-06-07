# Wave BO — Runbooks & doc interlinking: audit runbook, linked evidence, INDEX + elevator pitch (BOO-167)

> 🌐 **Language:** English (this file) · [🇩🇪 Deutsch](wave-bo-runbooks-vernetzung.md)

**What's there now:** The role runbooks (Wave BJ) move from a loose set to an interlinked whole. The auditor runbook is now first-class (with an audit prompt, persistence zones and a sketch), every evidence column in the runbooks is clickable, a new role-based signpost sits at the very top of the README, a new alphabetical INDEX file gives the full overview of all documents, the HANDBUCH names the runbooks explicitly, and a plain-language 60-second elevator pitch explains the framework at a whiteboard. Docs only. DE+EN.

## Stories
- **BOO-167** — doc-interlinking story (7 work packages A–G).

## Changes (DE+EN)
- **`docs/runbooks/audit-perspective.md` / `.en.md`** — expanded from 156 to ~311 lines: audience auditor (cyber-security AND code-quality) addressed directly, "In one sentence"/"Big picture"(+sketch)/"Further reading", the three **persistence zones** (committed/durable · CI artifact/30 days · local-gitignored), a dual-audience table, and an **audit prompt** as a bilingual copy-paste block (8-step scan, read-only, two modes).
- **`docs/runbooks/ceo-business-case` · `ciso-security` · `cto-code-quality` · `dpo-privacy` (each `.md`/`.en.md`)** — `> **Who this is for.**` → `> **Audience:**` (reader role only) + a separate time/key-question sentence; evidence/artifact columns switched from plain text to Markdown links (only real repo targets; project-local artifacts stay code spans); header/intro drift harmonised. DPO was the linking template.
- **New `docs/INDEX.md` / `.en.md`** — alphabetical table of all 32 documents (Document | Description | Audience | Languages) plus a separate "Skill documentation" block (15 skill READMEs). Linked from the README.
- **New `docs/pitch/elevator-pitch.md` / `.en.md`** — 60-second pitch (~205/210 words), jargon-free, with a whiteboard script + embedded sketch; complements the existing 30-minute presentation.
- **New sketches (DE+EN, `.excalidraw` + `.png`):** `docs/audit-perspective-runbook.*` (question→evidence→location with 3 persistence zones), `docs/pitch/elevator-pitch.*` (whiteboard script). **Updated:** `docs/role-runbooks-map.*` — from "Four lenses" to **"Five lenses"** (auditor as a downstream cross-cutting lens).
- **`README.md`** — new lean role signpost "Who are you? / Wer bist du?" at the very top (DE+EN) linking the CEO/CISO/CTO/DPO/auditor runbooks + pointers to the INDEX and the elevator pitch. The existing long table stays.
- **`HANDBUCH.md` / `.en.md`** — chapter 13 names the 5 role runbooks + `framework-update`/`sonarcloud-setup`; TOC "appendices A through AB" → "A through AD"; appendix signpost extended with AC/AD.
- **`docs/glossar.md` / `.en.md`** — new entries "Auditor", "Audit trail", "Audit artifact" with an everyday analogy.

## Impact
For "I'm new — where do I start?" there is now a role-based entry point within the first screen, a full index and a 60-second pitch. The auditor has a self-contained, actionable runbook including a copy-paste prompt. Evidence is click-through instead of merely named.

## Scope
Docs only, no code, no new mechanics. Wave letter `bo` (`bn` was the last used). Project-local artifacts (`specs/`, `.claude/*`, `journal/*`, `ARCHITECTURE_DESIGN.md`) stay code spans (no dead links). No CIO/CDO runbook (does not exist). `docs-drift` green, all new relative links/embeds verified against the filesystem.

## References
Linear: BOO-167. Branch: `tobiaschschmidt/boo-167-docs-runbooks-doku-vernetzung-auditor-runbook-ausbauen`. Builds on Wave BJ (BOO-158–163, role runbooks). Operator source: Tobias, 2026-06-06.
