# Runbook: Framework update — lift an existing project to the current version

> For machines/projects where INTENTRON is **already installed** and that want to adopt the **current framework state** — without re-bootstrapping, without blindly overwriting local decisions. DE: [`framework-update.md`](framework-update.md).

## When this runbook?

You have a project running an **older INTENTRON version** and want to lift it to the current state — new gates, new required artifacts, bug fixes from the latest release waves. This is the **upgrade case**.

Distinction from the neighbouring runbooks:
- Only retrofit the lightweight SecondBrain building block (without upgrading) → [`secondbrain-nachziehen.md`](secondbrain-nachziehen.md)
- Several people, one VPS project → [`multi-user-vps.md`](multi-user-vps.md)

Two steps, both non-destructive:

1. **Update the tool** — bring the `bootstrap` skill on the machine up to date.
2. **Lift the project** — paste the upgrade prompt into the Claude Code session; the skill detects the existing installation and runs three modes (inspect → apply-safe → apply-with-confirmation).

## Step 1 — Update the bootstrap skill

Pulls only the `bootstrap` skill fresh from the repo (sparse, without the full clone):

```bash
cd /tmp
git clone --filter=blob:none --sparse https://github.com/vibercoder79/intentron.git intentron
cd intentron && git sparse-checkout set bootstrap
cp -r bootstrap ~/.claude/skills/
cd /tmp && rm -rf intentron
```

> On a **multi-user VPS** with a central skill pool, do a single `git pull` in the pool (`/opt/claude/skills/`) instead — see [`multi-user-vps.md`](multi-user-vps.md) or HANDBUCH Appendix R (skill pool governance).

## Step 2 — Paste the upgrade prompt into the Claude Code session

Open Claude Code **inside the project folder** and paste this prompt — the upgrade runs without an interactive interview:

```text
This repo may run an older INTENTRON version. Upgrade it safely following
bootstrap/references/framework-upgrade.md (modes inspect → apply-safe → apply-with-confirmation).
(1) inspect: read the current project contract (CONVENTIONS.md, CLAUDE.md/AGENTS.md,
    .claude/environment.json, hooks, specs), fetch the current framework from
    https://github.com/vibercoder79/intentron, read docs/releases/ for what changed, and show me
    a diff + risks + manual TODOs without writing anything.
(2) apply-safe: apply only additive/idempotent changes and run the relevant
    bootstrap/scripts/migrate-to-v2.sh --issue BOO-NN migrations.
(3) apply-with-confirmation: for anything that changes existing rules, hooks, CI or skill
    versions, ask me per change. Never touch .env/secrets.
Finally run bootstrap/references/verify-setup.sh and write an upgrade report to
journal/reports/framework-upgrade/YYYY-MM-DD.md.
```

The prompt automatically runs three phases: **inspect** (dry-run, nothing is written) → **apply-safe** (additive changes only) → **apply-with-confirmation** (confirm each destructive change individually).

| Mode | Behavior |
|---|---|
| **`inspect`** | show diff + risks + manual TODOs only, **writes nothing** |
| **`apply-safe`** | additive/idempotent changes only; existing content stays |
| **`apply-with-confirmation`** | anything that changes existing rules, hooks, CI or skill versions is confirmed per change |

> **Alternative:** type `/bootstrap` in the session — the skill detects the existing installation (§7.5a) and asks for the mode interactively.

## Safety & idempotency

- **Read before edit, additive only:** existing content (`CONVENTIONS.md`, `CLAUDE.md`, hooks, specs) is never blindly overwritten.
- **`.env`/secrets/local reports:** never touch, never commit, never copy into reports.
- **Idempotent:** `migrate-to-v2.sh --issue BOO-NN` and `verify-setup.sh` are safe to re-run.
- **Before the upgrade:** make the Git worktree clean or save changes; read `docs/releases/` (migration needs, new required artifacts, breaking changes).
- **Commit/push only after operator approval** — after reviewing the diff.

## Afterwards

- Deliberate deviations are **documented instead of overwritten** (principle: framework versions may make a project harder/clearer, not silently reinterpret it).
- Optional: run the full brownfield onboarding (HANDBUCH Appendix U, path 3) if you want to pull in not only the upgrade but also new skills/gates.

## References

`bootstrap/references/framework-upgrade.md` (modes, user flow, file categories) · `bootstrap/SKILL.md` §7.5a (auto-detection) · `bootstrap/scripts/migrate-to-v2.sh` (existing-project migrations) · `bootstrap/references/provider-postflight.md` · `bootstrap/references/verify-setup.sh` · HANDBUCH §"Upgrade path for existing projects" · `docs/upgrade-path-existing-projects.excalidraw` · related: [`secondbrain-nachziehen.md`](secondbrain-nachziehen.md), [`multi-user-vps.md`](multi-user-vps.md). BOO-156.
