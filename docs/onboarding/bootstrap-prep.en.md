# Bootstrap preparation — the questions the `/bootstrap` interview will ask

> **Purpose.** Framework setup runs as a guided `/bootstrap` interview (~10 min, 4 blocks A–D). This sheet lists the questions **up front** — hand it to the customer's IT with: *"Next week, during the bootstrapping process, I'll ask you these questions. Please make sure your team can answer them."* The session then runs fast, with no back-and-forth.
>
> Mirrors the real interview questions 1:1 (`bootstrap/SKILL.md` blocks A–D). The deeper customer-specific integration/CI part is covered by the separate sheet `docs/onboarding/integration-discovery.md`. Technical prerequisites at the end.

## Block A — Project core (10 questions, ~4 min)

1. **Stack.** Backend / frontend / full-stack? Which language(s) and framework(s)? — *who knows: lead/architect.*
2. **Frontend performance (frontend/full-stack only).** Set a Lighthouse-CI performance budget? — *frontend lead.*
3. **Target runtime / AI tool.** Which AI coding tool is the runtime: Claude Code, Codex, Cursor, cross-tool? — *engineering lead.*
4. **Project identity.** Project name? One-sentence description (what does the system do)? Start version (default 0.1.0)?
5. **Backlog basics.** Issue prefix (e.g. `MA-`)? Primary documentation language (de/en)?
6. **Backlog adapter.** Where do tickets live: Linear / GitHub Issues / Jira / Azure DevOps Boards / Microsoft Planner / none (markdown-only)? — *PM/PO.*
7. **Add-ons.** Which extra dimensions apply: Privacy/GDPR · Cost Efficiency · Signal Quality · Compliance (regulated industry) · **EU AI Act** (AI component with customer data)? — *data-protection/compliance owner.*
8. **Governance intensity.** lite / standard / heavy? (heavy = more gates, mandatory review, branch protection — for regulated/critical systems.) — *CTO/lead.*
9. **Execution isolation.** Should parallel AI agents run in isolated Git worktrees? — *engineering lead.*
10. **Deployment scenario.** Solo-Mac / Solo-VPS / Multi-user-VPS / team-with-coding-server? (Where the team develops *with the framework*.) — *IT/infra.*

## Block B — Existing infrastructure (6 questions, ~4 min)

1. **Project directory.** Exists (absolute path) or create new (where)?
2. **GitHub repo.** Present (URL)? Create later? No GitHub wanted?
3. **Project documentation SSoT.** Where the project docs live: Obsidian vault (path) · repo `docs/project/` · external DMS (Notion/Confluence/SharePoint + URL) · undecided (repo fallback) · repo-docs + personal vault harvest (team with Obsidian)? — *central team decision.*
4. **Backlog system.** Concrete tool + access: Linear (team slug) / GitHub Issues (repo) / Jira (project key) / Azure DevOps (project) / Planner (plan) / none.
5. **API keys.** Project keys already in a `.env`, or is `.env.example` enough (keys later)? — *DevOps.*
6. **Developer handover.** Create + maintain a `Developer Onboarding` artifact, or just link to existing docs?

**Extra (provider postflight):** Is there already a **monitoring/logging platform** (use central / prepare new / open)? Should the **research skill** be wired up (provider: Perplexity/OpenRouter/none)? **Visualization** via Miro (MCP present?) or fallback Excalidraw/Mermaid?

> **Merge-mode note:** If the directory/repo already contains files, bootstrap asks before overwriting (backup / add only missing governance files / abort).

## Block C — Documentation architecture (proposal + review)

Based on stack (A.1) and existing infra (block B), bootstrap **proposes** a 3-layer documentation architecture. Prepare: *who on the customer side decides about doc structure/storage (any mandates, an existing wiki/DMS, naming/storage conventions)?*

## Block D — Optional components (yes/no at the end)

Targeted yes/no decisions: **self-healing**, **DocSync**, **daemon/automation**, **learning loop**. Prepare: *do you want these optional automations — and any operational objections (e.g. automation that writes into your environment)?*

## Technical prerequisites (ready before the session)

- **Node.js v18+**, **Git**, an AI coding tool (Claude Code as the reference implementation)
- Accounts/access: AI tool (e.g. Anthropic), GitHub (if used), backlog tool (if used)
- Absolute path for the project directory; repo URL if applicable; vault/DMS path if applicable
- Details: HANDBUCH Appendix A (checklist) + §4 (step-by-step installation)

> **Deeper integration part:** If the built solution must integrate into your live/existing environment (hosting, your CI/CD, interfaces, network, secrets, compliance, go-live), additionally use `docs/onboarding/integration-discovery.md`.
