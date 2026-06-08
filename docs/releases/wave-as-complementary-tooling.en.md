# Wave AS — Complementary tooling: setup-checklist (BOO-113)

> 🌐 **Language:** English (this file) · [🇩🇪 Deutsch](wave-as-complementary-tooling.md)

**What is there now:** the best-practice setup checklist for Claude Code is available as its own public repo, and intentron references it with a clear ordering rule.

## Stories
- **BOO-113** — setup-checklist as its own public repo + reference from intentron.

## Changes
- **New public repo:** https://github.com/vibercoder79/claude-code-setup-checklist (MIT, skill at root, DE+EN).
- **intentron README (DE+EN):** section "Complementary tooling — machine setup" with link + ordering `global → /bootstrap → audit/additive` + rule of thumb.
- **HANDBUCH Appendix Z.4 (DE+EN):** the same reference + rule.
- **Sync (outside intentron):** `publish_skill.py` extended with fan-out — one publish writes to `claudecodeskills` (private) AND to the public repo; the skill README carries the complementarity note as the source.

## Ordering rule
1. `setup-checklist global` — machine best practice.
2. `/bootstrap` — project governance (owns project CLAUDE.md + hooks).
3. optional `setup-checklist audit`/`projekt` additive (`.claudeignore`, `.gitignore`, `CLAUDE.local.md`).

Rule of thumb: machine + hygiene = checklist · project governance = bootstrap. No file twice.

## References
Spec: `specs/BOO-113.md`. Release: v0.7.9.
