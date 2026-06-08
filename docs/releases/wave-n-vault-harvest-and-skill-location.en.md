# Release Notes - Wave N Vault Harvest + Skill Installation Strategy

> 🌐 **Language:** English (this file) · [🇩🇪 Deutsch](wave-n-vault-harvest-and-skill-location.md)

Status: 2026-05-28

## Purpose

Wave N closes two recurring operator questions around **vault structure and skill location** — both pure documentation waves, no feature code, but with high orientation value for teams:

1. **BOO-75 — Vault harvest pattern:** How do I combine repo docs (team SSoT) with a personal Obsidian vault? Answer: two separate flows + the sharp principle "Obsidian is a solo tool, not an enterprise tool".
2. **BOO-76 — Skill installation strategy:** Where do the skills belong — global, per project, or system pool? Answer: three install levels + decision matrix per deployment scenario + cross-tool view.

**Expected effect:** Two questions that until now were answered in consulting conversations or scattered across the HANDBUCH now each have one clear, illustrated appendix.

## Affected Stories

- BOO-75 — HANDBUCH Appendix R Layer 3 extended (vault harvest) + Bootstrap Block B.3 5th option + config scaffold
- BOO-76 — HANDBUCH Appendix S NEW (skill installation strategy)

## BOO-75 — Vault Harvest Pattern (Repo Docs + Personal Vault)

**Problem:** In multi-person projects the Obsidian vault cannot be the shared doc SSoT — a vault is personal. The living doc belongs in the GitHub repo under `docs/`. But anyone working across multiple projects still wants cross-project insights in their own vault.

**What is there now:**

- **HANDBUCH Appendix R Layer 3** (DE+EN): the sharp principle "Obsidian = solo, not enterprise" + **2-flow model**:
  - Flow 1 — normal Git (everyone, bidirectional): `docs/` ↔ GitHub repo. Team SSoT.
  - Flow 2 — vault harvest (per person, one-way): a `git post-merge` hook copies selected `docs/` into the personal vault, never back. No cron/webhook.
  - Teaching sketch `docs/assets/vault-harvest-solo-vs-team.png` (solid-bidirectional vs. dashed-one-way).
- **Bootstrap Block B.3** (DE+EN): 5th doc-SSoT option `[e] Repo docs + personal vault harvest` as a documented choice + inline hint (double safeguard at install: solo→Obsidian, team→repo, team-with-Obsidian→harvest) + `[e]` handling (DocSync=no, onboarding step). Version 3.29.0 → 3.30.0.
- **Config scaffold** `bootstrap/references/vault-sync-pattern.md` (+ `.en.md`): team contract `tracked-paths.json` + `local.json` schema + mechanics + core rules.

**Important:** The sync engine itself (Stefan's `vault-sync.py` etc.) is **not** vendored — the reference implementation lives in `StefanWeimarPRODOC/project-template`. Engine vendoring is Phase 2 (blocked, separate story).

## BOO-76 — Skill Installation Strategy (Appendix S)

**Problem (recurring question):** "Where do I install the skills?" Previously a blanket "at project level" — but that creates update burden (each project individually). Especially unclear: a 20-person team on one VPS, multiple users, Claude central.

**What is there now — HANDBUCH Appendix S** (DE+EN) with sketch `docs/assets/skill-install-locations.png`:

- **Three install levels:** global per user (`~/.claude/skills/`), per project (`<projekt>/.claude/skills/` committed), global system pool (`/opt/claude/skills/`).
- **Tradeoff:** global = one update, no pinning; per-project = N updates, but reproducible + audit-proof.
- **Decision matrix per deployment scenario** (reference Appendix P): Solo Mac/Solo VPS → global per user; multi-user VPS → system pool (maintenance owner); team server → system pool or per project.
- **20-person VPS answer concretely:** one global system pool `/opt/claude/skills/`, read-only, one maintenance owner, one `git pull` for the whole machine — NOT per project.
- **Cross-tool:** Claude Code (`~/.claude/skills/` + `.claude/skills/`), Codex (`.codex/skills/`), others via Appendix K. Multi-tool teams → per-project committed is more portable.

## Concrete Changes

| Area | Change | File |
|---|---|---|
| HANDBUCH Appendix R Layer 3 | Obsidian=solo sharpened + 2-flow model + sketch + DocSync delineation (DE+EN) | `HANDBUCH.md` + `.en.md` |
| HANDBUCH Appendix S NEW | Skill installation strategy (DE+EN) + sketch | `HANDBUCH.md` + `.en.md` |
| Bootstrap Block B.3 | 5th doc-SSoT option + inline hint + `[e]` handling; v3.30.0 | `bootstrap/SKILL.md` + `.en.md` |
| Config scaffold NEW | Vault-sync team contract + local.json schema | `bootstrap/references/vault-sync-pattern.md` + `.en.md` |
| Sketches NEW | Vault harvest + skill install levels | `docs/assets/vault-harvest-solo-vs-team.png`, `docs/assets/skill-install-locations.png` |
| Migration | `migrate_boo_75` + `migrate_boo_76` (doc-only hint blocks) | `bootstrap/scripts/migrate-to-v2.sh` |
| Migration checklist | §BOO-75 + §BOO-76 (DE+EN) | `bootstrap/references/migration-checklist-v1-to-v2.md` + `.en.md` |
| Specs | `specs/BOO-75.md`, `specs/BOO-76.md` | specs/ |

## Skill Version Bumps

- `bootstrap` 3.29.0 → 3.30.0 (BOO-75: 5th doc-SSoT option + inline hint)

## Migration for Existing Projects

Both pure documentation — idempotent hint blocks:

```bash
bash bootstrap/scripts/migrate-to-v2.sh --issue BOO-75   # Vault harvest (doc-only)
bash bootstrap/scripts/migrate-to-v2.sh --issue BOO-76   # Skill installation strategy (doc-only)
```

## Open Follow-ups

- **BOO-75 Phase 2** (blocked): vendor the vault-sync engine into the framework — as soon as `StefanWeimarPRODOC/project-template` is accessible OR a framework-native minimal engine is built (operator decision open).
- **Framework-native vault-sync engine:** alternative to Stefan's code — a lean, framework-own sync mechanism that bootstrap generates directly on option `[e]`. Own story if needed.

## References

- Specs: `specs/BOO-75.md`, `specs/BOO-76.md`
- HANDBUCH: Appendix R Layer 3 (vault harvest), Appendix S (skill installation)
- Config scaffold: `bootstrap/references/vault-sync-pattern.md`
- Vault-sync discussion: SecondBrain `02 Projekte/Code-Crash Framework/Decisions/2026-05-28 Vault-Sync fuer Multi-Person-Projekte (Stefan).md`
- Feedback source: Operator Stefan (vault sync) + Tobias (skill location), 2026-05-27/28
- Linear: BOO-75, BOO-76
- Consolidated overview: `docs/releases/v0.2.0-overview.md`
