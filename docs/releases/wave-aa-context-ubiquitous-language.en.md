# Wave AA — CONTEXT.md ubiquitous language: canonical + forbidden vocabulary (BOO-91)

**Linear:** [BOO-91](https://linear.app/owlist/issue/BOO-91/) · ties into BOO-21 (domain context)

As of: 2026-05-31

## Problem

Without a fixed vocabulary the AI invents synonyms: sometimes `User`, sometimes `Customer`,
sometimes `Betroffener` for the same entity. This causes two kinds of damage:

- **Term drift.** The same thing is named five different ways across five files → poor
  `grep`-ability, harder refactors, misalignment between docs and code, token waste (the AI
  re-guesses on every run).
- **Weak compliance trail.** For a regulated audience, vocabulary is legally loaded:
  `Betroffener` is a defined term (GDPR Art. 4), and Switzerland's nDSG uses `Bearbeitung`
  instead of `Verarbeitung`. If the vocabulary isn't bound to the legal basis, it's hard to
  prove in an audit conversation.

Ubiquitous language is a cheap, high-impact lever — until now it went unused.

## Solution

A `CONTEXT.md` artifact anchors the **ubiquitous language** (Domain-Driven Design) in the
project: a `canonical | forbidden | source` table. Two layers — like the edit bodyguard
(BOO-86) and the dpo catalog (BOO-87):

- **Pre-filled framework base** `bootstrap/references/context-base.md` (+ `.en.md`) — ships with
  **compliance vocabulary** (`Betroffener`, `Bearbeitung`, `Auftragsverarbeiter`, `Einwilligung`,
  `personenbezogene Daten`) and **governance vocabulary** (`Story`, `Spec`, `Intent`, `Gate`,
  `Layer 0/2/3`, `BOO-<n>`). Every entry carries its source (GDPR article / nDSG / INTENTRON
  governance) as an audit trail.
- **Project overlay** `CONTEXT.md` in the project root — `migrate_boo_91()` seeds the base into it
  and adds an empty section `## Projekt-Domaene (vom Operator fuellen)` (project domain — to be
  filled by the operator). The operator does not start from zero; they only extend the domain
  section (e.g. `Police` instead of `Vertrag` in an insurance context). The overlay
  **survives framework updates — it is never overwritten**.

The AI reads `CONTEXT.md` while writing (`CLAUDE.md`/`CONVENTIONS.md` point to it).
**Default = guidance, not a hard gate** — the AI is guided, not blocked. An enforcing block at the
vocabulary level would only create friction (legitimate quotes, external API fields) and push
operators to switch it off.

## Migration

`bash bootstrap/scripts/migrate-to-v2.sh --issue BOO-91`

- Seeds `CONTEXT.md` in the project root **only if absent** (base + empty domain section).
- **Idempotent + additive:** a second run detects the existing `CONTEXT.md` (`[SKIP]`), no diff;
  a manually extended overlay stays unchanged; `--dry-run` only logs (`[DRY]`).
- **Rollback:** delete `CONTEXT.md` (back up your domain overlay first — the base lives in
  `bootstrap/references/context-base.md`).

Verification: `test -f CONTEXT.md` (exit 0); `grep -q 'Betroffener' CONTEXT.md` and
`grep -q 'Projekt-Domaene' CONTEXT.md` (exit 0).

## Pocock pattern relation (no code)

The pattern is inspired by Matt Pocock's `skills` repo. Only the **pattern** was taken (canonical
+ forbidden vocabulary as an artifact) — **no code**. The base file, schema, seeding and docs are
written independently; the in-house build fits the INTENTRON architecture. Hard constraint: no
code from Pocock's repo.

## Enforcement as a later expansion stage

This wave ships the **guidance layer**, not the enforcement layer. Deliberately out of scope, for
later (opt-in):

- **dpo control "vocabulary follows CONTEXT.md"** — `grep`-absent of the forbidden terms →
  `PASS`/`GAP` in the AUDIT report (couples to BOO-87).
- **Layer-0 bodyguard `warn`** on forbidden terms in PII paths (couples to BOO-86).

First prove the value of the guidance layer, then specify the enforcement coupling.

## Concrete changes

| Area | File |
|---|---|
| Pre-filled base (DE+EN) | `bootstrap/references/context-base.md` + `.en.md` |
| Project migration | `migrate_boo_91` in `bootstrap/scripts/migrate-to-v2.sh` |
| Migration checklist §BOO-91 (DE+EN) | `bootstrap/references/migration-checklist-v1-to-v2.md` + `.en.md` |
| HANDBUCH Appendix X (DE+EN) | `HANDBUCH.md` + `.en.md` |
| Release notes (DE+EN) | `docs/releases/wave-aa-context-ubiquitous-language.md` + `.en.md` |
| Spec | `specs/BOO-91.md` |

## Version bump

- **bootstrap: 3.34.0 → 3.35.0**

## References

- Spec: `specs/BOO-91.md`
- Base: `bootstrap/references/context-base.md` (+ `.en.md`)
- HANDBUCH: Appendix X "CONTEXT.md — ubiquitous language"
- Migration: `migrate_boo_91` in `bootstrap/scripts/migrate-to-v2.sh`
- Ties into: BOO-21 (domain context, the bridge via the domain section)
- Later expansion stage: dpo control (BOO-87) / Layer-0 bodyguard `warn` (BOO-86) — no hard gate in this wave
- Relation: Matt Pocock's `skills` repo (ubiquitous-language pattern) — rebuilt, no code
- Linear: BOO-91
