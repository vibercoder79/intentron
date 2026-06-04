# Runbook: Framework update — lift an existing project to the current version

> For machines/projects where INTENTRON is **already installed** and that want to adopt the **current framework state** — without re-bootstrapping, without blindly overwriting local decisions. DE: [`framework-update.md`](framework-update.md).

## When this runbook?

You have a project running an **older INTENTRON version** and want to lift it to the current state — new gates, new required artifacts, bug fixes from the latest release waves. This is the **upgrade case**.

Distinction from the neighbouring runbooks:
- Only retrofit the lightweight SecondBrain building block (without upgrading) → [`secondbrain-nachziehen.md`](secondbrain-nachziehen.md)
- Several people, one VPS project → [`multi-user-vps.md`](multi-user-vps.md)

Two levels, both non-destructive:

1. **Update the tool** — bring the `bootstrap` skill on the machine up to date.
2. **Lift the project** — `/bootstrap` in the project detects the existing installation and runs the upgrade in three modes.

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

## Step 2 — Run the upgrade in the project (dry-run first)

In a Claude Code session **inside the project folder**, simply type **`/bootstrap`**. The skill detects the existing installation (§7.5a) and asks for the mode — no flag needed:

| Mode | Behavior |
|---|---|
| **`inspect`** | show diff + risks + manual TODOs only, **writes nothing** (dry-run) |
| **`apply-safe`** | additive/idempotent changes only (new templates, missing sections); existing content stays |
| **`apply-with-confirmation`** | anything that changes existing rules, hooks, CI or skill versions is confirmed per change |

**Recommended order: `inspect` → `apply-safe` → `apply-with-confirmation`.**

One-shot prompt — paste into Claude Code opened in the old repo as an alternative to the interactive mode prompt:

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
