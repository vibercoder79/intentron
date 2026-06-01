[🇬🇧 English](#english) · [🇩🇪 Deutsch](#deutsch)

---

<a name="english"></a>

# INTENTRON — AI-Driven Development Governance
### by OWLIST

> **License:** Source-available (PolyForm Perimeter 1.0.0) — usable and adaptable for your own projects, **no reselling**. ([details](#license))

> A **battle-tested, tool-neutral governance framework** for AI-assisted development — reference implementation in Claude Code, runs equally with Codex, Cursor and other AI tools. An interview-driven orchestrator plus a coherent set of sub-skills set up a complete AI-driven development governance framework for any new project, covering the full delivery cycle.

**Core idea:** AI writes your code. Governance makes sure you still understand why in six months.

INTENTRON turns the method described in Matthias Schrader's book "Code Crash" into a working operating system for AI-assisted development.

**The name — INTENT + -TRON:** *Intent* is Schrader's core idea — we extend spec-driven development by the layer *above* the spec: every story is aligned to an **intent** (the *why*), not just a specification (the *what*). The *-tron* suffix names a **machine** (cyclotron, magnetron). Together, INTENTRON is **the engine that turns intent into production** — enforced and traceable.

---

## Why INTENTRON? The edge

Most spec-driven frameworks (Spec Kit & co.) optimize exactly one thing: turning a specification into code. Quality, governance, security, privacy, team-readiness — they leave those out. INTENTRON flips the focus: the generated code is not the product, the *path from intent to production* is — with guardrails a team would otherwise have to build itself.

Four things set us apart concretely:

1. **One contract — tool-neutral and machine-executable.** Your rules (tests, logging, security thresholds, governance) live in *one* place and are shared by three readers: the human, the AI tool (Claude, Codex, Cursor) and the CI that enforces them. Others have rules as prose that nobody enforces — and lock you into *one* tool.
2. **Intent before implementation.** We start one step earlier than the spec — at the *why* (after Schrader). That stops the AI from cleanly building the wrong thing.
3. **Governance that scales with you.** Solo gets three gates, an enterprise gets twelve — same record, only the strictness is dialed up or down.
4. **Privacy & security in the bundle.** DPO and security-architect reviews are built in, not an afterthought. For regulated industries that's the entry ticket.

**Common denominator:** Others optimize "the AI writes code." We optimize "a team — human plus *any* AI — gets intent to production, with guardrails it didn't have to build itself." The guardrails are invisible until they catch something — and when they catch, they explain why.

---

## How INTENTRON differs

A methodical comparison against the two closest framework categories — spec-driven (Spec Kit) and harness optimizers (ECC, Everything Claude Code):

| | INTENTRON | Spec Kit (spec-driven) | ECC (harness optimizer) |
|---|---|---|---|
| Focus | Path from intent → production, with gates | Specification → code | Breadth across Claude Code tools |
| Hard gates (blocking) | ✅ Spec, Sensitive-Paths, Coverage, Slopsquatting | ❌ none | ❌ none |
| Intent before spec | ✅ | ❌ | ❌ |
| Governance scales (Solo→Enterprise) | ✅ | ❌ | ❌ |
| Privacy/Security built in | ✅ (DPO + Security-Architect) | ❌ | ❌ |
| Tool-neutral (1 contract) | ✅ AGENTS.md + CONVENTIONS | partial | ❌ (Claude-Code-bound) |

**A different category, not a competitor:** ECC and similar collections are *harness optimizers / tool pools* — breadth across many tools. INTENTRON is a *method with enforced discipline* — depth. Different axes: breadth does not replace gates.

### The full picture — vs. the orchestration frameworks

A dimension-by-dimension comparison against the agent-orchestration tools (an honest read — what others do better is called out below):

| Dimension | **INTENTRON** | CrewAI | AutoGen / AG2 | BMAD | Cursor Rules |
|-----------|---------------|--------|---------------|------|--------------|
| **Governance enforcement** | ✅ Machine-enforced (Git hooks) | ❌ none | ❌ none | ⚠️ manual | ❌ none |
| **Traceability** | ✅ Idea → issue → spec → commit | ❌ | ❌ | ⚠️ partial | ❌ |
| **Human-in-the-loop** | ✅ Enforced (spec sign-off) | ⚠️ optional | ⚠️ optional | ✅ explicit | ❌ |
| **Self-healing** | ✅ Cron, 15 min, auto-corrects | ❌ | ❌ | ❌ | ❌ |
| **Learning loop** | ✅ Outcome check + LEARNINGS.md | ❌ | ❌ | ❌ | ❌ |
| **Model routing** | ✅ Opus/Sonnet/Haiku per task type | ⚠️ configurable | ✅ good | ❌ | ❌ |
| **Multi-agent orchestration** | ✅ Agent teams + parallel subagents | ✅ strong | ✅ very strong | ⚠️ manual | ❌ |
| **Deploy automation** | ⚠️ partial (Git push + manual) | ❌ | ❌ | ❌ | ❌ |
| **Portability** | ✅ Zero dependencies, 1 folder | ⚠️ pip install | ⚠️ pip install | ⚠️ prompt files | ✅ |
| **Project setup time** | ~30 min (guided) | hours | hours | ~1h | minutes |
| **Target audience** | Solo dev → enterprise team | Enterprise teams | Research / quality | Agile teams | Individual devs |

**Where others are genuinely stronger** — and when to prefer them:

| Framework | Real strength | When to prefer it |
|-----------|---------------|-------------------|
| **CrewAI** | Scalable role-based crews for enterprise — used by 60% of the Fortune 500. Best choice when coordinating >10 agents. | Large team, many parallel workflows, enterprise compliance requirements |
| **AutoGen / AG2** | Debate pattern: two agents argue against each other toward the best solution. Highest output quality for complex analysis tasks. | Research, code review with the highest quality bar, offline batch processes |
| **BMAD** | Structured agile workflow with clear roles (PM, Architect, Developer). Well documented, large community. | Teams already on Scrum/Agile that want an AI-native workflow |
| **Cursor Rules** | Ready to use instantly, zero setup time, right in the editor. | Individual devs who want to start fast without governance overhead |

*(Bootstrap's [README](bootstrap/README.md#framework-vergleich) adds the onboarding view: what makes INTENTRON unique and when to choose it.)*

![INTENTRON positioning — depth & enforcement vs. breadth](docs/intentron-positioning.en.png)

*The full landscape on two axes: spec-driven, harness optimizers and orchestration frameworks all cluster on breadth/low enforcement; INTENTRON alone holds the governance zone — enforced discipline from intent to production, scaling solo → enterprise.*

---

## What Is This?

`intentron/` is a tool-neutral container of skills — implemented for Claude Code as the reference runtime and portable to Codex, Cursor and other AI tools (see [CONVENTIONS.md](CONVENTIONS.md) + HANDBUCH Appendix K) — that form one coherent development workflow:

- **The orchestrator** (`bootstrap/`) interviews you about a new project and scaffolds the full governance framework: runtime instructions, documentation SSoT, Developer Onboarding, backlog adapter, Git hooks, skill selection, optional learning-loop.
- **Sub-skills** (`ideation/`, `implement/`, etc.) cover the downstream delivery workflow — from idea to sprint review.
- **Specialist bundle skills** (`security-architect/`, `dpo/`) live **inside the framework repo** (vendored, since BOO-74) so a single `git clone` is self-contained. Bootstrap installs them from here.
- **Companion skills** (`../research/`, `../skill-creator/`, etc.) are referenced by the governance flow but maintained as stand-alone skills at `claudecodeskills/` top level.

Full setup guide: **[HANDBUCH.md](HANDBUCH.md)** (German, ~230 KB) + **[HANDBUCH.en.md](HANDBUCH.en.md)** (English, ~200 KB) — appendices A–Y cover Hermes, sprint sizing, Codex onboarding (J), tool adapters (K), token efficiency (N), privacy (O), deployment scenarios (P), sovereignty stack (Q), multi-operator coordination (R), skill-installation strategy (S), post-install verification (T), multi-project operation (U), Layer-0 Edit-Bodyguard (V), Contribute-Back loop (W), CONTEXT.md / Ubiquitous Language (X) and the VPS/cloud team runbook (Y).

**What's new (v0.2.0):** see **[docs/releases/v0.2.0-overview.md](docs/releases/v0.2.0-overview.md)** — privacy-by-design, deployment scenarios, sovereignty stack, multi-operator coordination, dpo + security-architect as bundle skills, vault-harvest engine, post-install verification, multi-project operation, optional container profile.

**What's new (v0.3.0–v0.5.0):** see **[docs/releases/v0.3.0-overview.md](docs/releases/v0.3.0-overview.md)**, **[v0.4.0-overview.md](docs/releases/v0.4.0-overview.md)** and **[v0.5.0-overview.md](docs/releases/v0.5.0-overview.md)** — Layer-0 Edit-Bodyguard (BOO-86, pre-edit-bodyguard.sh, four-layer Quality-Gate), dpo control catalogue (BOO-87, GDPR/nDSG controls as Git-tracked YAML, deterministic runner, PASS/GAP/REVIEW-NEEDED report), coverage-check v2 (BOO-88, statement-lines denominator), coverage-check single-source + Drift-Guard (BOO-89), Contribute-Back loop (BOO-90, contribute-fix.sh), CONTEXT.md Ubiquitous Language (BOO-91).

**Tool-neutral specification:** [CONVENTIONS.md](CONVENTIONS.md) — describes the framework conventions without binding to a specific AI tool. Read this first when adopting the framework with Codex, Cursor, or any other tool (see HANDBUCH Appendix K).

**Project handover by design:** every bootstrap now chooses a project documentation SSoT: Obsidian Vault, repo `docs/project/`, external DMS, or an explicit repo fallback. It also creates or links a `Developer Onboarding` artifact so an unfamiliar team or another coding tool can take over the project without relying on old chat history.

---

## Quickstart

Three ways to get INTENTRON into your AI coding tool. The framework repo is **public** and `bootstrap/` sits at the repo root — so the bootstrap skill is a single `git clone` away. The `/bootstrap` skill then sets up your project and pulls every other skill it needs.

### A) Manual install, then `/bootstrap`

```bash
mkdir -p ~/.claude/skills
cd /tmp
git clone --filter=blob:none --sparse https://github.com/vibercoder79/intentron.git intentron
cd intentron && git sparse-checkout set bootstrap
cp -r bootstrap ~/.claude/skills/
cd /tmp && rm -rf intentron
ls ~/.claude/skills/bootstrap/   # should show SKILL.md + references/
```

Then open Claude Code in your project folder and run `/bootstrap`. (Restart the session once so the freshly copied skill is registered as a slash command.) Full step-by-step: **[HANDBUCH §4](HANDBUCH.md)**.

### B) AI self-install (let the tool do it)

Claude Code has shell access, so it can install itself. Paste this into a session opened in an empty project folder:

> Clone the public repo https://github.com/vibercoder79/intentron, copy its `bootstrap/` folder into `~/.claude/skills/bootstrap/` (create the directory if needed), confirm `~/.claude/skills/bootstrap/SKILL.md` exists, then read that SKILL.md and follow it to bootstrap this project.

(Having the AI read `SKILL.md` directly means you don't have to restart the session to register the `/bootstrap` command first.)

### C) AI self-update for an old / brownfield install

For an existing repo that still runs an older INTENTRON version, the safe upgrade follows **[`bootstrap/references/framework-upgrade.md`](bootstrap/references/framework-upgrade.md)** (see also **[HANDBUCH](HANDBUCH.md)** §"Upgrade path for existing projects") — it never overwrites local decisions blindly, in three stages:

1. **`inspect`** — read the current project state, diff it against the new version, show risks and manual TODOs. Writes nothing.
2. **`apply-safe`** — apply only additive/idempotent changes (new templates, missing sections); existing content stays.
3. **`apply-with-confirmation`** — anything that changes existing rules, hooks, CI or skill versions is confirmed per change. `.env`/secrets are never touched.

One-shot prompt — paste into Claude Code opened in the old repo:

> This repo may run an older INTENTRON version. Upgrade it safely following `bootstrap/references/framework-upgrade.md` (modes inspect → apply-safe → apply-with-confirmation). (1) **inspect**: read the current project contract (`CONVENTIONS.md`, `CLAUDE.md`/`AGENTS.md`, `.claude/environment.json`, hooks, specs), fetch the current framework from https://github.com/vibercoder79/intentron, read `docs/releases/` for what changed, and show me a diff + risks + manual TODOs without writing anything. (2) **apply-safe**: apply only additive/idempotent changes and run the relevant `bootstrap/scripts/migrate-to-v2.sh --issue BOO-NN` migrations. (3) **apply-with-confirmation**: for anything that changes existing rules, hooks, CI or skill versions, ask me per change. Never touch `.env`/secrets. Finally run `bootstrap/references/verify-setup.sh` and write an upgrade report to `journal/reports/framework-upgrade/YYYY-MM-DD.md`.

> [!note]
> Same outcome, different entry point: **A** is the explicit/auditable path, **B** is the fastest cold start, **C** lifts an existing install to the current version. The migrations and `verify-setup.sh` are idempotent — safe to re-run.

---

## Why the method comes from "Code Crash" (and how to read this)

The thinking behind INTENTRON comes from **Matthias Schrader's book "Code Crash"**. Schrader's thesis, in one line: AI now writes the code, so the scarce resource is no longer typing speed — it is **intent, governance and the ability to still understand a system months later**. INTENTRON is our attempt to turn that thesis into a working *operating system* for AI-assisted development: skills, gates and artifacts that keep the "why" alive while the AI handles the "how".

- **You do not need to have read the book.** The framework and HANDBUCH are written to stand on their own — every concept is explained where it is used.
- **But we recommend it** for the deeper context. The HANDBUCH references Schrader throughout (anti-patterns, production-readiness, the 4P pipeline), and **Appendix M ("Schrader Decoder")** maps the book's chapters onto the concrete framework pieces.
- If you only read one thing first: this README, then [HANDBUCH.en.md](HANDBUCH.en.md) §1–§8.

## Not a one-size-fits-all framework

INTENTRON gives you a **solid base structure** — but every company, team and setup is different, and we deliberately **do not try to model every case** in the framework itself. The framework stays lightweight; the **HANDBUCH appendices provide guidance for different circumstances** so you can adapt it to your reality:

| Your situation | Where the guidance is |
|----------------|-----------------------|
| Solo vs. VPS vs. team-server | Appendix P (deployment scenarios) |
| Team of 5–20+ developers | Appendix R (multi-operator coordination) |
| Where do skills/tools/hooks live | Appendix S (installation strategy) |
| Several projects on one machine | Appendix U (multi-project operation) |
| EU / regulated industry | Appendix Q (sovereignty stack) + Appendix O (privacy) |
| "Did my setup actually work?" | Appendix T (post-install verification) |
| Running under Codex / another AI tool | Appendix J (Codex onboarding) + Appendix K (tool adapters) |

The framework is the skeleton. **You tailor the muscles** — the appendices tell you how, and a real consumer fork (e.g. a GitHub-Issues + personal-vault setup) shows it works in practice.

---

## System Overview

![Bootstrap Skill — Interview-Block flow (A–D) + setup phases (0, 4, 5, 7)](bootstrap/docs/bootstrap-big-picture.en.png)

*From empty folder to governance-ready project — four interview blocks (A–D) frame the decisions, four setup phases (0, 4, 5, 7) execute them. Block D spins up optional components only on demand.*

---

## The Skills

### Orchestrator + Sub-Skills (this folder)

| Skill | Command | What it does |
|-------|---------|-------------|
| **[bootstrap](bootstrap/)** | `/bootstrap` | **Start here.** Interview-driven project setup — CLAUDE.md, Linear, Git hooks, skill selection. |
| **[ideation](ideation/)** | `/ideation` | Idea → 4-perspective research → Linear issue with acceptance criteria. |
| **[backlog](backlog/)** | `/backlog` | Sprint planning — which story now, which later, and why. Dependency-aware. |
| **[implement](implement/)** | `/implement` | 8-step protocol: Agent pattern → Spec → Code → Governance validation → Commit. |
| **[architecture-review](architecture-review/)** | `/architecture-review` | Reviews architecture dimensions — risks, tech debt, improvement potential. |
| **[sprint-review](sprint-review/)** | `/sprint-review` | Quarterly audit: architecture health, tech debt, backlog hygiene, learning loop. |
| **[pitch](pitch/)** | `/pitch` | Closes the 4P pipeline — gathers evidence (metrics, architecture diff, intent fulfillment) as a Markdown cheat sheet. No slides, human runs the demo. |
| **[grafana](grafana/)** | `/grafana` | Grafana Cloud dashboards via MCP — panels, PromQL, alert rules. |
| **[cloud-system-engineer](cloud-system-engineer/)** | `/cloud-system-engineer` | VPS/Docker infrastructure: health checks, firewall, DNS, resources. |
| **[visualize](visualize/)** | `/visualize` | Generate architecture diagrams in Miro from existing documentation. |

### Specialist bundle skills (this folder, vendored — BOO-74)

| Skill | Command | What it does |
|-------|---------|-------------|
| **[security-architect](security-architect/)** | `/security-architect` | STRIDE threat modeling, OWASP Top 10, ASVS 5.0 — 4 modes (Design/Review/Audit/Skill-Scan). Installed by bootstrap when the security dimension is active. |
| **[dpo](dpo/)** | `/dpo` | Data Protection Officer — privacy by design (GDPR/BDSG/nDSG). 3 modes (Assess/Review/Audit). Versioned control catalogue (GDPR + nDSG controls as Git-tracked YAML, deterministic runner, PASS/GAP/REVIEW-NEEDED report — BOO-87). Installed by the bootstrap Privacy add-on (BOO-69). |

*Master of these two stays in `claudecodeskills/` (via `publish_skill.py`); the framework repo holds a vendored mirror so a single clone is self-contained.*

### Top-level companion skills (parent folder)

| Skill | Command | What it does |
|-------|---------|-------------|
| **[research](../research/)** | `/research` | 2-tier routing: Quick (WebSearch) or Deep (Perplexity + cross-check). |
| **[skill-creator](../skill-creator/)** | `/skill-creator` | Create, package and register new skills into the global registry. |
| **[design-md-generator](../design-md-generator/)** | `/design-md-generator` | Extract a website's visual design system into a machine-readable DESIGN.md. |
| **[setup-checklist](../setup-checklist/)** | `/setup-checklist` | Claude Code best-practice audit — global and project settings. |

---

## How the Skills Work Together

```
💡 Idea
  └─ /ideation ──→ Linear issue + ACs (4 perspectives, research-backed)
       └─ /backlog ──→ Prioritization: which story goes next?
            └─ /implement ──→ Spec file → Code → Governance validation → Commit
                 └─ /architecture-review ──→ Risks? Tech debt?
                      └─ /sprint-review ──→ Quarterly audit: what worked?
                           └─ /pitch ──→ Evidence briefing for the stakeholder demo
```

Governance gates run automatically on `git commit` / `git push` (and `git pull`):
- `spec-gate.sh` — blocks commits without a linked spec file
- `doc-version-sync.sh` — blocks pushes when documentation is out of sync
- `sensitive-paths` gate (BOO-18) — stops at security-sensitive paths until `review-ok`
- `personal-data-paths` gate (BOO-69) — stops at personal-data paths until `privacy-ok`
- `post-merge` vault-harvest hook (BOO-77, opt-in) — mirrors selected docs into a personal vault after `git pull`

No spec, no commit. That's the difference between a prompt and a governance framework.

> **Operating at scale:** running on a VPS, a team, or in a regulated industry? HANDBUCH appendices **P** (deployment scenarios), **R** (multi-operator coordination, 5–20+ operators), **S** (where do skills/tools/hooks belong) and **Q** (EU-sovereignty stack) cover the setup decisions; appendix **O** documents privacy-by-design.

---

## Where to Start

| Situation | Recommendation |
|-----------|---------------|
| New project, empty folder | → [/bootstrap](bootstrap/) — start here |
| Existing project, needs structure | → [HANDBUCH.md §4](HANDBUCH.md) — step-by-step retrofit |
| Just one specific skill | → Clone the skill folder and install it |
| Want to understand everything first | → [HANDBUCH.md](HANDBUCH.md) — full reference |
| Concrete operational question | → [docs/qa.md](docs/qa.md) — living Q&A |

---

## Prerequisites

- **An AI coding tool** — Claude Code (CLI/IDE, reference implementation) or Codex, Cursor & co. (see HANDBUCH Appendix K)
- **Backlog system** — Linear (recommended) / Microsoft 365 Planner / GitHub Issues / none
- **GitHub** repository for your project
- **Project documentation SSoT** — Obsidian Vault, repo `docs/project/`, external DMS, or temporary repo fallback
- Optional extensions: Grafana Cloud, Miro, Hostinger VPS — skills use what's available

---

## License

This project is **source-available** under the [PolyForm Perimeter License 1.0.0](LICENSE.md). Use, modification, and internal deployment — including commercial use — are permitted. You may **not** provide a product that competes with this software (no reselling as a competing product). **INTENTRON** and **OWLIST** are trademarks of OWLIST GmbH; this license grants no trademark rights.

---

<sub>"INTENTRON" is an independent product of OWLIST GmbH and has no business relationship with Matthias Schrader or the publisher of the book "Code Crash". The methodology is based on the principles described in the book "Code Crash"; "Code Crash" is the title of that book. All names mentioned are trademarks of their respective owners.</sub>

---


<a name="deutsch"></a>

# INTENTRON — Governance für KI-gestützte Entwicklung
### by OWLIST

> **Lizenz:** Source-available (PolyForm Perimeter 1.0.0) — nutzbar und anpassbar für eigene Projekte, **kein Weiterverkauf**. ([Details](#lizenz))

> Ein **battle-tested, tool-neutrales Governance-Framework** für KI-gestützte Entwicklung — Referenz-Implementierung in Claude Code, läuft genauso mit Codex, Cursor und anderen KI-Tools. Ein interview-geführter Orchestrator plus kohärente Sub-Skills setzen ein vollständiges KI-getriebenes Governance-Framework für jedes neue Projekt auf und decken den kompletten Delivery-Zyklus ab.

**Kernidee:** KI schreibt deinen Code. Governance stellt sicher, dass du in 6 Monaten noch weißt warum.

INTENTRON setzt die im Buch »Code Crash« von Matthias Schrader beschriebene Methode in ein funktionierendes Betriebssystem für KI-gestützte Entwicklung um.

**Der Name — INTENT + -TRON:** *Intent* ist Schraders Kernbegriff — wir erweitern Spec-Driven Development um die Ebene *über* der Spec: Jede Story ist auf einen **Intent** ausgerichtet (das *Warum*), nicht nur auf eine Spezifikation (das *Was*). Die Endung *-tron* benennt eine **Maschine** (Zyklotron, Magnetron). Zusammen ist INTENTRON **die Engine, die Intent in Produktion überführt** — erzwungen und nachvollziehbar.

---

## Warum INTENTRON? Der Vorteil

Die meisten Spec-Driven-Frameworks (Spec Kit & Co.) optimieren genau eine Sache: aus einer Spezifikation Code generieren. Qualität, Governance, Sicherheit, Datenschutz, Teamfähigkeit blenden sie aus. INTENTRON dreht den Fokus: Nicht der generierte Code ist das Produkt, sondern der *Weg von der Absicht zur Produktion* — mit Leitplanken, die ein Team sonst selbst bauen müsste.

Vier Dinge unterscheiden uns konkret:

1. **Ein Vertrag — tool-neutral und maschinen-ausführbar.** Eure Regeln (Tests, Logging, Security-Schwellen, Governance) leben an *einer* Stelle und werden von drei Lesern geteilt: dem Menschen, dem KI-Tool (Claude, Codex, Cursor) und der CI, die sie erzwingt. Andere haben Regeln als Prosa, die niemand durchsetzt — und binden dich an *ein* Tool.
2. **Intent vor Implementation.** Wir starten eine Stufe früher als die Spec — beim *Warum* (nach Schrader). Das verhindert, dass die KI sauber das Falsche baut.
3. **Governance, die mitwächst.** Solo bekommt drei Gates, ein Konzern zwölf — dieselbe Platte, nur die Strenge wird gedimmt.
4. **Privacy & Security im Bündel.** DPO- und Security-Architect-Prüfungen sind eingebaut, kein Nachgedanke. Für regulierte Branchen ist das die Eintrittskarte.

**Gemeinsamer Nenner:** Andere optimieren „die KI schreibt Code". Wir optimieren „ein Team — Mensch plus *beliebige* KI — bringt Intent nach Produktion, mit Leitplanken, die es nicht selbst bauen musste." Die Leitplanken sind unsichtbar, bis sie etwas fangen — und wenn sie fangen, erklären sie warum.

---

## Wie sich INTENTRON unterscheidet

Ein methodischer Vergleich mit den zwei nächstliegenden Framework-Kategorien — Spec-Driven (Spec Kit) und Harness-Optimierer (ECC, Everything Claude Code):

| | INTENTRON | Spec Kit (Spec-Driven) | ECC (Harness-Optimierer) |
|---|---|---|---|
| Fokus | Weg von Intent → Produktion, mit Gates | Spezifikation → Code | Breite über Claude-Code-Tools |
| Hard Gates (blockierend) | ✅ Spec, Sensitive-Paths, Coverage, Slopsquatting | ❌ keine | ❌ keine |
| Intent vor Spec | ✅ | ❌ | ❌ |
| Governance skaliert (Solo→Konzern) | ✅ | ❌ | ❌ |
| Privacy/Security eingebaut | ✅ (DPO + Security-Architect) | ❌ | ❌ |
| Tool-neutral (1 Vertrag) | ✅ AGENTS.md + CONVENTIONS | teilweise | ❌ (Claude-Code-gebunden) |

**Eine andere Kategorie, kein Wettbewerber:** ECC und ähnliche Sammlungen sind *Harness-Optimierer / Werkzeug-Pools* (Breite über viele Tools). INTENTRON ist eine *Methode mit erzwungener Disziplin* (Tiefe). Verschiedene Achsen — Breite ersetzt keine Gates.

### Das volle Bild — vs. die Orchestrierungs-Frameworks

Ein Dimension-für-Dimension-Vergleich gegen die Agent-Orchestrierungs-Tools (ehrlich gelesen — was andere besser machen, steht direkt darunter):

| Dimension | **INTENTRON** | CrewAI | AutoGen / AG2 | BMAD | Cursor Rules |
|-----------|---------------|--------|---------------|------|--------------|
| **Governance-Enforcement** | ✅ Maschinell erzwungen (Git Hooks) | ❌ Keine | ❌ Keine | ⚠️ Manuell | ❌ Keine |
| **Traceability** | ✅ Idee → Issue → Spec → Commit | ❌ | ❌ | ⚠️ Partiell | ❌ |
| **Human-in-the-Loop** | ✅ Erzwungen (Spec-Freigabe) | ⚠️ Optional | ⚠️ Optional | ✅ Explizit | ❌ |
| **Self-Healing** | ✅ Cron, 15 Min, auto-korrigiert | ❌ | ❌ | ❌ | ❌ |
| **Learning-Loop** | ✅ Outcome-Check + LEARNINGS.md | ❌ | ❌ | ❌ | ❌ |
| **Modell-Routing** | ✅ Opus/Sonnet/Haiku je Task-Typ | ⚠️ Konfigurierbar | ✅ Gut | ❌ | ❌ |
| **Multi-Agent Orchestrierung** | ✅ Agent-Teams + Parallel-Subagents | ✅ Stark | ✅ Sehr stark | ⚠️ Manuell | ❌ |
| **Deploy-Automation** | ⚠️ Teilweise (Git Push + Manual) | ❌ | ❌ | ❌ | ❌ |
| **Portabilität** | ✅ Zero Dependencies, 1 Ordner | ⚠️ pip install | ⚠️ pip install | ⚠️ Prompt-Files | ✅ |
| **Projekt-Setup-Zeit** | ~30 Min (geführt) | Stunden | Stunden | ~1h | Minuten |
| **Zielgruppe** | Solo-Dev → Enterprise-Team | Enterprise-Teams | Forschung / Quality | Agile Teams | Einzelentwickler |

**Was andere Frameworks besser machen** — und wann du sie bevorzugen solltest:

| Framework | Echte Stärke | Wann bevorzugen |
|-----------|--------------|-----------------|
| **CrewAI** | Skalierbare Role-based Crews für Enterprise — 60% der Fortune 500 nutzen es. Beste Wahl wenn >10 Agents koordiniert werden müssen. | Großes Team, viele parallele Workflows, Enterprise-Compliance-Anforderungen |
| **AutoGen / AG2** | Debate-Pattern: 2 Agents argumentieren gegeneinander bis zur besten Lösung. Höchste Ausgabequalität für komplexe Analyse-Aufgaben. | Forschung, Code-Review mit höchsten Qualitätsanforderungen, offline Batch-Prozesse |
| **BMAD** | Strukturierter Agile-Workflow mit klaren Rollen (PM, Architect, Developer). Gut dokumentiert, große Community. | Teams die Scrum/Agile bereits kennen und einen AI-nativen Workflow wollen |
| **Cursor Rules** | Sofort einsatzbereit, keine Setup-Zeit, direkt im Editor. | Einzelentwickler die schnell starten wollen ohne Governance-Overhead |

*(Die bootstrap-[README](bootstrap/README.md#framework-vergleich) ergänzt die Onboarding-Sicht: was INTENTRON einzigartig macht und wann du es wählen solltest.)*

![INTENTRON Positionierung — Tiefe & Erzwingung vs. Breite](docs/intentron-positioning.png)

*Die volle Landschaft auf zwei Achsen: Spec-Driven, Harness-Optimierer und Orchestrierungs-Frameworks clustern alle bei Breite/wenig Erzwingung; nur INTENTRON hält die Governance-Zone — erzwungene Disziplin von Intent bis Produktion, skaliert Solo → Enterprise.*

---

## Was ist das hier?

`intentron/` ist ein tool-neutraler Container von Skills — implementiert für Claude Code als Referenz-Runtime und portierbar auf Codex, Cursor und andere KI-Tools (siehe [CONVENTIONS.md](CONVENTIONS.md) + HANDBUCH Anhang K) — die zusammen einen kohärenten Entwicklungs-Workflow bilden:

- **Der Orchestrator** (`bootstrap/`) führt das Interview zu einem neuen Projekt und legt das komplette Governance-Framework an: Runtime-Anweisungen, Dokumentations-SSoT, Developer Onboarding, Backlog-Adapter, Git-Hooks, Skill-Auswahl, optionaler Learning-Loop.
- **Sub-Skills** (`ideation/`, `implement/`, etc.) decken den nachgelagerten Delivery-Workflow ab — von der Idee bis zum Sprint-Review.
- **Spezialisten-Bundle-Skills** (`security-architect/`, `dpo/`) liegen **im Framework-Repo selbst** (vendored, seit BOO-74) — ein einziges `git clone` ist self-contained. Bootstrap installiert sie von hier.
- **Companion-Skills** (`../research/`, `../skill-creator/`, etc.) werden vom Governance-Flow referenziert, aber als eigenständige Skills auf Top-Level von `claudecodeskills/` gepflegt.

Komplettes Setup-Handbuch: **[HANDBUCH.md](HANDBUCH.md)** (Deutsch, ~230 KB) + **[HANDBUCH.en.md](HANDBUCH.en.md)** (Englisch, ~200 KB) — Anhaenge A–Y decken Hermes, Sprint-Sizing, Codex-Onboarding (J), Tool-Adapter (K), Token-Effizienz (N), Privacy (O), Deployment-Szenarien (P), Souveraenitaets-Stack (Q), Multi-Operator-Koordination (R), Skill-Installations-Strategie (S), Post-Install-Verifikation (T), Multi-Projekt-Betrieb (U), Layer-0-Edit-Bodyguard (V), Contribute-Back-Schleife (W), CONTEXT.md / Ubiquitous Language (X) und das VPS/Cloud-Team-Runbook (Y) ab.

**Was ist neu (v0.2.0):** siehe **[docs/releases/v0.2.0-overview.md](docs/releases/v0.2.0-overview.md)** — Privacy-by-Design, Deployment-Szenarien, Souveraenitaets-Stack, Multi-Operator-Koordination, dpo + security-architect als Bundle-Skills, Vault-Harvest-Engine, Post-Install-Verifikation, Multi-Projekt-Betrieb, optionales Container-Profil.

**Was ist neu (v0.3.0–v0.5.0):** siehe **[docs/releases/v0.3.0-overview.md](docs/releases/v0.3.0-overview.md)**, **[v0.4.0-overview.md](docs/releases/v0.4.0-overview.md)** und **[v0.5.0-overview.md](docs/releases/v0.5.0-overview.md)** — Layer-0-Edit-Bodyguard (BOO-86, pre-edit-bodyguard.sh, vier-schichtige Quality-Gate-Architektur), dpo-Kontrollkatalog (BOO-87, DSGVO/nDSG-Controls als Git-versionierte YAML, deterministischer Runner, Report mit PASS/GAP/REVIEW-NEEDED), coverage-check v2 (BOO-88, Nenner = nur Statement-Zeilen), coverage-check Single-Source + Drift-Guard (BOO-89), Contribute-Back-Schleife (BOO-90, contribute-fix.sh), CONTEXT.md Ubiquitous Language (BOO-91).

**Tool-neutrale Spezifikation:** [CONVENTIONS.md](CONVENTIONS.md) — beschreibt die Framework-Konventionen ohne Bindung an ein bestimmtes KI-Tool. Lies das zuerst, wenn du das Framework mit Codex, Cursor oder einem anderen Tool aufnimmst (siehe HANDBUCH Anhang K).

**Uebergabe standardmaessig mitgedacht:** Jeder Bootstrap waehlt jetzt eine Projekt-Dokumentations-SSoT: Obsidian Vault, Repo `docs/project/`, externes DMS oder expliziter Repo-Fallback. Zusaetzlich wird ein `Developer Onboarding` erzeugt oder verlinkt, damit ein fremdes Team oder ein anderes Coding-Tool das Projekt ohne alte Chat-Historie uebernehmen kann.

---

## Schnellstart

Drei Wege, INTENTRON in dein KI-Coding-Tool zu bekommen. Das Framework-Repo ist **public** und `bootstrap/` liegt im Repo-Root — der Bootstrap-Skill ist also ein einziges `git clone` entfernt. Der `/bootstrap`-Skill richtet danach dein Projekt ein und holt alle weiteren Skills, die er braucht.

### A) Manuell installieren, dann `/bootstrap`

```bash
mkdir -p ~/.claude/skills
cd /tmp
git clone --filter=blob:none --sparse https://github.com/vibercoder79/intentron.git intentron
cd intentron && git sparse-checkout set bootstrap
cp -r bootstrap ~/.claude/skills/
cd /tmp && rm -rf intentron
ls ~/.claude/skills/bootstrap/   # sollte SKILL.md + references/ zeigen
```

Dann Claude Code im Projektordner starten und `/bootstrap` ausführen. (Session einmal neu starten, damit der frisch kopierte Skill als Slash-Command erkannt wird.) Schritt für Schritt: **[HANDBUCH §4](HANDBUCH.md)**.

### B) AI-Self-Install (die KI macht es selbst)

Claude Code hat Shell-Zugriff und kann sich selbst installieren. Diesen Prompt in eine Session in einem leeren Projektordner einfügen:

> Klone das public Repo https://github.com/vibercoder79/intentron, kopiere dessen `bootstrap/`-Ordner nach `~/.claude/skills/bootstrap/` (Verzeichnis ggf. anlegen), prüfe dass `~/.claude/skills/bootstrap/SKILL.md` existiert, lies dann diese SKILL.md und folge ihr, um dieses Projekt zu bootstrappen.

(Wenn die KI `SKILL.md` direkt liest, musst du die Session nicht erst neu starten, damit der `/bootstrap`-Command registriert wird.)

### C) AI-Self-Update für eine alte / Brownfield-Installation

Für ein bestehendes Repo mit älterer INTENTRON-Version folgt das sichere Upgrade **[`bootstrap/references/framework-upgrade.md`](bootstrap/references/framework-upgrade.md)** (siehe auch **[HANDBUCH](HANDBUCH.md)** §„Upgrade-Pfad für bestehende Projekte") — es überschreibt lokale Entscheidungen nie blind, in drei Stufen:

1. **`inspect`** — Ist-Zustand lesen, Diff zur neuen Version, Risiken und manuelle TODOs zeigen. Schreibt nichts.
2. **`apply-safe`** — nur additive/idempotente Änderungen (neue Templates, fehlende Sektionen); Bestehendes bleibt.
3. **`apply-with-confirmation`** — alles, was bestehende Regeln, Hooks, CI oder Skill-Versionen ändert, wird einzeln bestätigt. `.env`/Secrets werden nie angefasst.

Einmal-Prompt — in Claude Code einfügen, geöffnet im alten Repo:

> Dieses Repo fährt evtl. eine ältere INTENTRON-Version. Aktualisiere es sicher nach `bootstrap/references/framework-upgrade.md` (Modi inspect → apply-safe → apply-with-confirmation). (1) **inspect**: lies den Projektvertrag (`CONVENTIONS.md`, `CLAUDE.md`/`AGENTS.md`, `.claude/environment.json`, Hooks, Specs), hole das aktuelle Framework von https://github.com/vibercoder79/intentron, lies `docs/releases/` für die Änderungen, und zeig mir Diff + Risiken + manuelle TODOs, ohne etwas zu schreiben. (2) **apply-safe**: wende nur additive/idempotente Änderungen an und führe die zutreffenden `bootstrap/scripts/migrate-to-v2.sh --issue BOO-NN` Migrationen aus. (3) **apply-with-confirmation**: alles, was bestehende Regeln, Hooks, CI oder Skill-Versionen ändert, einzeln mit mir bestätigen. `.env`/Secrets nie anfassen. Zum Schluss `bootstrap/references/verify-setup.sh` ausführen und einen Upgrade-Report nach `journal/reports/framework-upgrade/YYYY-MM-DD.md` schreiben.

> [!note]
> Gleiches Ergebnis, anderer Einstieg: **A** ist der explizite/auditierbare Weg, **B** der schnellste Kaltstart, **C** hebt eine bestehende Installation auf den aktuellen Stand. Migrationen und `verify-setup.sh` sind idempotent — gefahrlos wiederholbar.

---

## Warum die Methode aus »Code Crash« kommt (und wie man das hier liest)

Der Denkanstoss hinter INTENTRON kommt aus **Matthias Schraders Buch »Code Crash«**. Schraders These in einem Satz: Die KI schreibt jetzt den Code — die knappe Ressource ist nicht mehr Tippgeschwindigkeit, sondern **Intent, Governance und die Faehigkeit, ein System auch in Monaten noch zu verstehen**. INTENTRON ist unser Versuch, diese These in ein funktionierendes *Betriebssystem* fuer KI-gestuetzte Entwicklung zu giessen: Skills, Gates und Artefakte, die das "Warum" am Leben halten, waehrend die KI das "Wie" uebernimmt.

- **Du musst das Buch nicht gelesen haben.** Framework und HANDBUCH stehen fuer sich — jedes Konzept wird dort erklaert, wo es genutzt wird.
- **Wir empfehlen es aber** fuer den tieferen Kontext. Das HANDBUCH nimmt durchgehend Bezug auf Schrader (Anti-Patterns, Production-Readiness, 4P-Pipeline), und **Anhang M ("Schrader-Decoder")** mappt die Buch-Kapitel auf die konkreten Framework-Bausteine.
- Wenn du zuerst nur eines liest: diese README, dann [HANDBUCH.md](HANDBUCH.md) §1–§8.

## Kein One-Size-Fits-All-Framework

INTENTRON gibt dir eine **solide Grundstruktur** — aber jedes Unternehmen, Team und Setup ist anders, und wir versuchen bewusst **nicht, jeden Einzelfall** im Framework selbst abzubilden. Das Framework bleibt leichtgewichtig; die **HANDBUCH-Anhaenge geben Guidance fuer unterschiedliche Gegebenheiten**, damit du es an deine Realitaet anpasst:

| Deine Situation | Wo die Guidance steht |
|-----------------|------------------------|
| Solo vs. VPS vs. Team-Server | Anhang P (Deployment-Szenarien) |
| Team mit 5–20+ Entwicklern | Anhang R (Multi-Operator-Koordination) |
| Wo gehoeren Skills/Tools/Hooks hin | Anhang S (Installations-Strategie) |
| Mehrere Projekte auf einer Maschine | Anhang U (Multi-Projekt-Betrieb) |
| EU / regulierte Branche | Anhang Q (Souveraenitaets-Stack) + Anhang O (Privacy) |
| "Hat mein Setup wirklich funktioniert?" | Anhang T (Post-Install-Verifikation) |
| Betrieb unter Codex / anderem KI-Tool | Anhang J (Codex-Onboarding) + Anhang K (Tool-Adapter) |

Das Framework ist das Skelett. **Die Muskeln schneiderst du** — die Anhaenge zeigen wie, und ein echter Consumer-Fork (z.B. ein GitHub-Issues- + persoenlicher-Vault-Setup) zeigt, dass es in der Praxis traegt.

---

## Das System im Überblick

![Bootstrap Skill — Interview-Block-Flow (A–D) + Setup-Phasen (0, 4, 5, 7)](bootstrap/docs/bootstrap-big-picture.png)

*Vom leeren Ordner zum governance-ready Projekt — vier Interview-Blöcke (A–D) umrahmen die Entscheidungen, vier Setup-Phasen (0, 4, 5, 7) setzen sie um. Block D aktiviert optionale Komponenten nur auf Wunsch.*

---

## Die Skills

### Orchestrator + Sub-Skills (dieser Ordner)

| Skill | Befehl | Was er tut |
|-------|--------|------------|
| **[bootstrap](bootstrap/)** | `/bootstrap` | **Einstieg:** Interview-geführtes Projekt-Setup — CLAUDE.md, Linear, Git-Hooks, Skill-Auswahl. |
| **[ideation](ideation/)** | `/ideation` | Idee → 4-Perspektiven-Research → Linear Issue mit ACs. |
| **[backlog](backlog/)** | `/backlog` | Sprint Planning — welche Story jetzt, welche nach hinten, warum. Abhängigkeiten-aware. |
| **[implement](implement/)** | `/implement` | 8-Schritte-Protokoll: Agent-Pattern → Spec → Code → Governance-Validation → Commit. |
| **[architecture-review](architecture-review/)** | `/architecture-review` | Prüft Architektur-Dimensionen — Risiken, Tech Debt, Verbesserungspotential. |
| **[sprint-review](sprint-review/)** | `/sprint-review` | Quartals-Audit: Architektur-Gesundheit, Tech Debt, Backlog-Hygiene, Learning-Loop. |
| **[pitch](pitch/)** | `/pitch` | Schliesst die 4P-Pipeline — sammelt Evidenz (Metriken, Architektur-Diff, Intent-Erfuellung) als Markdown-Spickzettel. Keine Slides, Mensch macht die Demo. |
| **[grafana](grafana/)** | `/grafana` | Grafana Cloud Dashboards via MCP — Panels, PromQL, Alert Rules. |
| **[cloud-system-engineer](cloud-system-engineer/)** | `/cloud-system-engineer` | VPS/Docker-Infrastruktur: Health-Check, Firewall, DNS, Ressourcen. |
| **[visualize](visualize/)** | `/visualize` | Architektur-Diagramme in Miro aus bestehenden Doku-Dateien generieren. |

### Spezialisten-Bundle-Skills (dieser Ordner, vendored — BOO-74)

| Skill | Befehl | Was er tut |
|-------|--------|------------|
| **[security-architect](security-architect/)** | `/security-architect` | STRIDE Threat Modeling, OWASP Top 10, ASVS 5.0 — 4 Modi (Design/Review/Audit/Skill-Scan). Wird vom Bootstrap installiert, wenn die Security-Dimension aktiv ist. |
| **[dpo](dpo/)** | `/dpo` | Data Protection Officer — Datenschutz by Design (DSGVO/BDSG/nDSG). 3 Modi (Assess/Review/Audit). Versionierter Kontrollkatalog (DSGVO + nDSG Controls als Git-versionierte YAML, deterministischer Runner, Report mit PASS/GAP/REVIEW-NEEDED — BOO-87). Wird vom Privacy-Add-on des Bootstrap installiert (BOO-69). |

*Master dieser zwei bleibt in `claudecodeskills/` (via `publish_skill.py`); das Framework-Repo haelt einen vendored Mirror, damit ein einziges Clone self-contained ist.*

### Top-Level Companion-Skills (Elternordner)

| Skill | Befehl | Was er tut |
|-------|--------|------------|
| **[research](../research/)** | `/research` | 2-Tier-Routing: Quick (WebSearch) oder Deep (Perplexity + Gegencheck). |
| **[skill-creator](../skill-creator/)** | `/skill-creator` | Neue Skills erstellen, paketieren und in die globale Registry einbinden. |
| **[design-md-generator](../design-md-generator/)** | `/design-md-generator` | Visuelles Design-System einer Website als maschinenlesbare DESIGN.md extrahieren. |
| **[setup-checklist](../setup-checklist/)** | `/setup-checklist` | Claude Code Best-Practice-Audit — globale und projekt-Settings. |

---

## Wie die Skills zusammenspielen

```
💡 Idee
  └─ /ideation ──→ Linear Issue + ACs (4 Perspektiven, Research-backed)
       └─ /backlog ──→ Priorisierung: welche Story jetzt?
            └─ /implement ──→ Spec-File → Code → Governance-Validation → Commit
                 └─ /architecture-review ──→ Risiken? Tech Debt?
                      └─ /sprint-review ──→ Quartals-Audit: Was hat funktioniert?
                           └─ /pitch ──→ Evidenz-Briefing fuer den Stakeholder-Demo
```

Governance-Gates laufen automatisch bei `git commit` / `git push` (und `git pull`):
- `spec-gate.sh` — blockiert Commits ohne verknüpftes Spec-File
- `doc-version-sync.sh` — blockiert Pushes wenn Doku veraltet ist
- `sensitive-paths`-Gate (BOO-18) — stoppt bei security-sensitiven Pfaden bis `review-ok`
- `personal-data-paths`-Gate (BOO-69) — stoppt bei personenbezogenen Pfaden bis `privacy-ok`
- `post-merge`-Vault-Harvest-Hook (BOO-77, opt-in) — spiegelt ausgewaehlte Docs nach `git pull` in einen persoenlichen Vault

Kein Spec, kein Commit. Das ist der Unterschied zwischen einem Prompt und einem Governance-Framework.

> **Im Team / auf VPS / reguliert?** HANDBUCH-Anhaenge **P** (Deployment-Szenarien), **R** (Multi-Operator-Koordination, 5–20+ Operatoren), **S** (wo gehoeren Skills/Tools/Hooks hin) und **Q** (EU-Souveraenitaets-Stack) decken die Setup-Entscheidungen ab; Anhang **O** dokumentiert Privacy-by-Design.

---

## Wo anfangen?

| Situation | Empfehlung |
|-----------|------------|
| Neues Projekt, leerer Ordner | → [/bootstrap](bootstrap/) |
| Bestehendes Projekt, Chaos | → [HANDBUCH.md §4](HANDBUCH.md) |
| Nur einzelne Skills | → Gewünschten Skill-Ordner klonen und installieren |
| Alles verstehen bevor ich anfange | → [HANDBUCH.md](HANDBUCH.md) |
| Konkrete Praxisfrage | → [docs/qa.md](docs/qa.md) — lebendes Q&A |

---

## Voraussetzungen

- **Ein KI-Coding-Tool** — Claude Code (CLI/IDE, Referenz-Implementierung) oder Codex, Cursor & Co. (siehe HANDBUCH Anhang K)
- **Backlog-System** — Linear (empfohlen) / Microsoft 365 Planner / GitHub Issues / keines
- **GitHub** Repository für dein Projekt
- **Projekt-Dokumentations-SSoT** — Obsidian Vault, Repo `docs/project/`, externes DMS oder temporaerer Repo-Fallback
- Optional: Grafana Cloud, Miro, Hostinger VPS — Skills nutzen was verfügbar ist

---

## Lizenz

Dieses Projekt ist **source-available** unter der [PolyForm Perimeter License 1.0.0](LICENSE.md). Nutzung, Anpassung und interner Einsatz — auch kommerziell — sind erlaubt. Nicht erlaubt ist die Bereitstellung eines Produkts, das mit dieser Software **konkurriert** (kein Weiterverkauf als Konkurrenzprodukt). **INTENTRON** und **OWLIST** sind Marken der OWLIST GmbH; die Lizenz gewährt keine Markenrechte.

---

<sub>»INTENTRON« ist ein eigenständiges Produkt der OWLIST GmbH und steht in keiner geschäftlichen Verbindung zu Matthias Schrader oder dem Verlag des Buchs »Code Crash«. Die Methodik ist angelehnt an die im Buch »Code Crash« beschriebenen Prinzipien; »Code Crash« ist der Werktitel dieses Buchs. Alle genannten Namen sind Kennzeichen ihrer jeweiligen Inhaber.</sub>
