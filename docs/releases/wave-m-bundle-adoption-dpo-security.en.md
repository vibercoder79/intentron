# Release Notes - Wave M Bundle Adoption DPO + security-architect

> 🌐 **Language:** English (this file) · [🇩🇪 Deutsch](wave-m-bundle-adoption-dpo-security.md)

Status: 2026-05-27

## Purpose

Wave M closes BOO-74 and **corrects a Wave J decision**. In Wave J (BOO-69) the DPO skill was deliberately adopted as a standalone skill — analogous to `security-architect`, which also lived outside the framework repo. Operator feedback from Tobias (2026-05-27 post-Wave-L) revealed the inconsistency: if the framework wants to **guarantee** privacy by design (HANDBUCH Appendix O), the DPO skill must be installable from the framework repo, not from a neighbouring repo. Same logic for `security-architect` (security dimension in bootstrap question A.4).

**Solution:** DPO and security-architect become **vendored bundle skills** in the `intentron` repo. Bootstrap installs them from the same repo as all other bundle skills. The master stays `claudecodeskills`, the framework repo is a mirror.

**Expected effect:** The framework becomes **self-contained**. A `git clone` of the framework repo contains everything bootstrap needs — including the privacy and security skills. Solo operators without the framework continue to obtain DPO/security-architect from `claudecodeskills`.

## Affected Stories

- BOO-74 — DPO + security-architect as vendored bundle skills (corrects the BOO-69 Wave J decision)

## Important Clarifications

### The master stays claudecodeskills

`publish_skill.py` does **not** change. DPO and security-architect continue to be maintained in the `claudecodeskills` repo. The framework repo receives a **mirrored vendored copy**. On every skill update the sync convention applies (see `bootstrap/references/skills-setup.md` §Sync convention): update the master first, then pull the mirror up to date.

### Bootstrap only clones the framework repo now

Before BOO-74, bootstrap Phase 5 cloned the `claudecodeskills` repo and distinguished between `intentron/` subfolder skills and top-level standalone skills. From v3.29.0 onward, bootstrap clones **only** the framework repo — all bundle skills + dpo + security-architect live there flat as top-level folders. Optional general-purpose skills (research, design-md-generator, setup-checklist, skill-creator) are added from claudecodeskills via a yes/no follow-up question.

### Solo use is preserved

Anyone using DPO or security-architect **without** INTENTRON (solo tool, other project) obtains them unchanged from `claudecodeskills`. The vendored copy in the framework repo is only relevant for the bootstrap installation path.

### Unchanged in content

DPO and security-architect are **not** changed in content by BOO-74 — no version bump of these skills. It is pure vendoring (file copy). DPO stays v1.1.0, security-architect stays v1.1.0.

## What Users Get with the New Setup

- **`dpo/` and `security-architect/` as top-level folders** in the `intentron` repo (vendored 1:1 from claudecodeskills, including references DE+EN for DPO).
- **Bootstrap v3.29.0** clones only the framework repo. The "Standard" skill selection now includes dpo + security-architect. Optional general-purpose skills via a follow-up question.
- **Bootstrap Phase 4.4n** installs DPO + security-architect from the framework bundle (`$SKILL_SRC/dpo/`, `$SKILL_SRC/security-architect/`) instead of from an external repo.
- **HANDBUCH Appendix O** reworked: "DPO as a framework bundle skill" instead of "standalone skill". Privacy mechanics (3 modes, trigger points) unchanged.
- **`migrate_boo_74()`** for existing projects: copies DPO + security-architect from the framework repo to `~/.claude/skills/`, idempotent and non-destructive.
- **Sync convention** in `bootstrap/references/skills-setup.md` (DE+EN): master vs. mirror, operator obligation on updates.

## Concrete Changes

| Area | Change | File |
|---|---|---|
| DPO vendored | 1:1 copy from claudecodeskills (SKILL.md + SKILL.en.md + 5 references DE+EN) | `dpo/` (NEW in the framework repo) |
| security-architect vendored | 1:1 copy from claudecodeskills (SKILL.md + 5 references + README + Excalidraw) | `security-architect/` (NEW in the framework repo) |
| Bootstrap Phase 5 | Skill source framework repo instead of claudecodeskills, repo structure doc, new optional follow-up question, copy logic simplified | `bootstrap/SKILL.md` v3.29.0 + `.en.md` |
| Bootstrap Phase 4.4n | "install from framework bundle" instead of "standalone" | `bootstrap/SKILL.md` + `.en.md` |
| Bootstrap A.4 privacy note | Wording "from the framework bundle" | `bootstrap/SKILL.md` + `.en.md` |
| HANDBUCH Appendix O | Title + skill location + activation steps + migration notes reworked to bundle | `HANDBUCH.md` + `HANDBUCH.en.md` |
| Migration | `migrate_boo_74()` + ALL_ISSUES | `bootstrap/scripts/migrate-to-v2.sh` |
| Migration checklist | §BOO-74 (DE+EN) | `bootstrap/references/migration-checklist-v1-to-v2.md` + `.en.md` |
| Sync convention | Master-vs-mirror doc NEW | `bootstrap/references/skills-setup.md` + `.en.md` |

## Skill Version Bumps

- `bootstrap` 3.28.0 → 3.29.0 (minor: skill source reworked, new follow-up question)
- `dpo` unchanged (v1.1.0 — vendored only)
- `security-architect` unchanged (v1.1.0 — vendored only)

## Migration for Existing Projects

`migrate_boo_74()` in `bootstrap/scripts/migrate-to-v2.sh`:

```bash
bash bootstrap/scripts/migrate-to-v2.sh --issue BOO-74
```

Idempotent and non-destructive. Result:

- `dpo/` + `security-architect/` copied from the framework repo to `~/.claude/skills/` (only if not already present).
- Existing installations remain unchanged.

Operator steps: ensure bootstrap version >= 3.29.0, remember sync discipline on future skill updates.

## Design Decision: Vendoring instead of Submodules

Git submodules are operationally heavy (`git submodule init`, `update`, detached-HEAD traps). At this scope (2 skills, ~25 files) vendoring (plain file copy) is lighter and more robust. Tradeoff: sync is an operator obligation until the `sync_framework_mirror.sh` script exists (follow-up story).

## Still Open / Follow-ups

- **`sync_framework_mirror.sh`** (follow-up story): automates the mirror update on `publish_skill.py dpo` / `security-architect`. Until then, operator obligation.
- **More skills into the bundle?** research / design-md-generator / setup-checklist / skill-creator stay in claudecodeskills for now (general-purpose skills, not framework-specific). Own story if needed.
- **security-architect EN variant:** the skill today has only `SKILL.md` (no `SKILL.en.md`), because it was created before the 2026-04-17 bilingualism cutoff. Pull it up to bilingual on a larger security-architect update (CLAUDE.md rule).

## References

- Spec: `specs/BOO-74.md` (planned locally as BOO-73, Linear assigned BOO-74)
- HANDBUCH: Appendix O (reworked to bundle skill)
- Bootstrap: `bootstrap/SKILL.md` Phase 5 + Phase 4.4n
- Sync convention: `bootstrap/references/skills-setup.md` §Sync convention
- Migration: `bootstrap/scripts/migrate-to-v2.sh` (`migrate_boo_74`)
- Feedback source: Operator Tobias, 2026-05-27 (post-Wave-L)
- Linear: <https://linear.app/owlist/issue/BOO-74/>
- Previous wave: `docs/releases/wave-l-multi-operator-coordination.md`
