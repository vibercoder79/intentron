# Collision protection: the three levels of parallelism

> How this framework prevents parallel work from overwriting itself — at **three clearly separated levels**. They are often confused, but they are completely different mechanisms. DE: [`kollisionsschutz-drei-ebenen.md`](kollisionsschutz-drei-ebenen.md).

"Working in parallel" means different things in different contexts — and each context has its **own** protection mechanism. Mixing them up means looking for the bug on the wrong level.

## The three levels at a glance

| Level | Who works in parallel? | What is shared… | Protection | Status |
|---|---|---|---|---|
| **1 — Multi-USER** | several people on one project | only the GitHub repo (remote) | own clone per user, sync via Git | documented (Appendix P §3 + U), runbook |
| **2 — Multi-SESSION** | one person, several sessions | the same local clone | own `git worktree` / session hint | hint (see below) |
| **3 — Multi-AGENT** | several AI agents in one story | the same working tree of a session | `EXECUTION_ISOLATION` (write-scope / git-worktree) | built into the framework (BOO-52) |

**Rule of thumb:** the deeper the level, the tighter the shared space — and the stricter the mechanism. Level 1 separates via **Git**, level 2 via **worktrees**, level 3 via **write-scopes/worktrees + gate**.

## Level 1 — Multi-USER (several people, one project)

**Situation:** 10 developers work on project X on a VPS.

**Protection:** each has an **own system user** and **clones the repo into their own home** (`/home/<user>/projects/projektX`). **No shared working trees.** Synchronization happens exclusively via GitHub (`push`/`pull`/PR/merge) — this is "optimistic concurrency": everyone works freely, conflicts are resolved at merge time. There is no local "original"; all clones are equal, GitHub is the reference point.

**Consequence for the project structure:** the shared part (PMO hub, `decisions/`, `meetings/`, specs) lives in the repo and is shared via Git. The personal daily log `journal/daily/` goes into `.gitignore` for multi-user — so everyone has their own local journal without collisions.

→ Setup steps: **runbook [`runbooks/multi-user-vps.en.md`](runbooks/multi-user-vps.en.md)** · HANDBUCH **Appendix P §3** (multi-user VPS) + **Appendix U** (per-project checklist).

## Level 2 — Multi-SESSION (one person, several sessions, one clone)

**Situation:** you have two Claude Code sessions open that write to the **same** local clone (two windows, two devices on the same directory).

**Problem:** the sessions switch branches and overwrite each other's working-tree state — the branch moves out from under one of them.

**Protection:** do **not** run two sessions on the same clone. Instead, one **`git worktree`** per parallel track (`git worktree add ../projektX-track2 <branch>`) — own working directory, own branch, shared `.git` database. Optionally a **session hint** warns at start if another session is actively using the same tree.

→ This is the lightest level: usually **discipline + worktree** is enough. A lock hint is a safety net, not a must.

## Level 3 — Multi-AGENT (one session, several sub-agents on one story)

**Situation:** a story is implemented **in parallel** by several AI agents (`sub-agents` / `agentic`).

**Protection (built into the framework, BOO-52):** `CONVENTIONS.md` defines `EXECUTION_ISOLATION`:
- `none` — no parallel edits (`linear`).
- `write-scope` — parallel helpers only with **disjoint file ownership** (`write_scopes` in the spec).
- `git-worktree` — each agent gets its **own worktree/branch** (mandatory for `agentic`).

The `implement` skill enforces this in **step 0c "execution-isolation pre-flight"** as a hard gate: `sub-agents` needs populated `write_scopes`, `agentic` needs `git-worktree`. This way agents never overwrite each other.

→ This level is **already fully built** — no setup needed, it applies per story.

## In one sentence

> **Level 1 = own clone. Level 2 = own worktree. Level 3 = write-scopes/worktree + gate.**
> Three rooms, three locks — never solve one level's problem with another level's tool.
