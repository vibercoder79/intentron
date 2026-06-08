# Wave AF — Onboarding-Fix: Install + Quickstart + Self-Install/Self-Update (BOO-96)

> 🌐 **Language:** English (this file) · [🇩🇪 Deutsch](wave-af-onboarding-fix.md)

**Linear:** [BOO-96](https://linear.app/owlist/issue/BOO-96/) · Source: onboarding question Operator, 2026-06-01

## Problem

The documented installation command was broken after the rebrand (code-crash-framework → `intentron`):
HANDBUCH §4 step 3 (DE+EN) cloned `vibercoder79/claudecodeskills` and used the path
`intentron/bootstrap` — which does not exist there (verified via GitHub API: no `intentron/` folder,
only `code-crash-framework/`, 404). The bootstrap skill lives in the public repo
**`vibercoder79/intentron` directly in the root** (`bootstrap/SKILL.md`). A new user got
„No such file or directory". In addition, the README section „Where to start?" linked only to
`/bootstrap` — a slash command that only exists once the skill is installed — without the
upstream install step. The entry point ran into nothing.

## Stories

| Story | Content | Status |
|-------|--------|--------|
| **BOO-96** | Correct install command + visible README quickstart + AI self-install and AI self-update prompts | ✅ done |

## What changes

- **Install command corrected** (HANDBUCH.md + HANDBUCH.en.md, each step 3 + update appendix;
  bootstrap/README „new server" block): clone to
  `https://github.com/vibercoder79/intentron.git` (public, no SSH needed),
  `git sparse-checkout set bootstrap`, `cp -r bootstrap ~/.claude/skills/`.
- **README quickstart** (DE „Schnellstart" + EN „Quickstart"), prominently before the
  „Why" section, with three entry paths:
  - **A) Manual + `/bootstrap`** — the single shell command, then the slash command (+ note about
    session restart for command registration).
  - **B) AI self-install prompt** — copy-paste into a Claude Code session: the AI clones the public
    repo, copies `bootstrap/` to `~/.claude/skills/bootstrap/`, **then reads SKILL.md and
    follows it** (bypasses the slash-registration delay).
  - **C) AI self-update prompt** — for old/brownfield installations: analyze the current state
    (`.claude/`, bootstrap version, skills, hooks), report the gap against the current `intentron`, then
    update via re-clone + `bootstrap/scripts/migrate-to-v2.sh` (idempotent) +
    `bootstrap/references/verify-setup.sh`. Safer staged flow per
    `bootstrap/references/framework-upgrade.md` (inspect → apply-safe → apply-with-confirmation;
    never blindly overwrites local decisions/secrets).
- **Note callout** (DE+EN): same result, A explicit/auditable, B fastest cold start,
  C upgrade; migrations + verify-setup.sh idempotent.

## Design decision

- **Canonical skill source = `intentron` repo, `bootstrap/` in the root** (not
  claudecodeskills/intentron — does not exist). A single `git clone` is self-contained
  (vendored bundle skills, BOO-74).
- **https instead of SSH** in the quickstart/prompt — public repo, no key setup, lowest barrier.
- **Three documented paths instead of one** — deliberate, because the target groups differ
  (hand-install/auditability vs. fast AI start vs. brownfield upgrade).
- **B reads SKILL.md directly** instead of blindly calling `/bootstrap` — avoids the
  registration race.

## Verified

- No more `sparse-checkout set intentron/bootstrap` / `cp -r intentron/bootstrap` in
  HANDBUCH/README/bootstrap-README (grep = 0).
- Install command points everywhere to `intentron.git` + sparse `bootstrap` (DE+EN, both
  HANDBUCH locations + bootstrap/README): 7 correct clone commands.
- README has `## Quickstart` (EN) + `## Schnellstart` (DE) with paths A/B/C.
- Prompts copy-paste-ready; self-install reads SKILL.md; self-update references
  migrate-to-v2.sh + verify-setup.sh. DE/EN at parity.

## Effect

The entry point works again for fresh users, is visible, and there are now three paths —
hand-install, AI self-install, and AI self-update of an old installation. Pure documentation, no
behavioral change.

## References / Release

- Branch `feat/boo-96-onboarding-prompts`. Release: **v0.6.1 (Wave AF)** — see
  `docs/releases/v0.6.1-overview.md`, detail spec `specs/BOO-96.md`.
