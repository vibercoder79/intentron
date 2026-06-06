# Wave BL — Governance framing sharpened: INTENTRON ≠ autonomous agentic AI (BOO-164)

**What's now in place:** The canonical boundary — "INTENTRON is a sequential engineering pipeline with quality gates, **not** a fully autonomous developer agent" — now also appears at the **three most-read entry points** (README intro, HANDBUCH introduction, bootstrap entry) instead of only in the deep chapters. Pure docs, no runtime code. DE+EN.

## Stories
- **BOO-164** — clarification paragraphs at the entry points + de-escalation of agentic-sounding signals.

## Changes (DE+EN)
- **`README.md`**: "What INTENTRON is not / Was INTENTRON nicht ist" clarification paragraph in the EN and DE intro; comparison table "Multi-agent orchestration" with a footnote (delegated sub-skills inside one controlled story, not autonomous agents); "autonomous (human) team" disambiguated.
- **`HANDBUCH.md` (+EN)**: introduction table row "Self-healing agent monitors 24/7" → "automated self-healing check (optional, cron — Block D)"; "What INTENTRON is NOT" boundary paragraph pulled forward into §1 (cross-ref to §8e).
- **`CONVENTIONS.md`**: §0 clarification "Not an autonomous agent / Kein autonomer Agent" (DE and EN block) — for Codex/Cursor migrants who expect agentic behaviour.
- **`bootstrap/SKILL.md` (+EN)**: entry scope note "sequential, controlled flow, not an autonomously running agent system" (no version bump — lightweight).

## Effect
A skimming reader (CISO, decision-maker, tool migrant) sees on the first screen: the framework is **human-steered governance for a sequential development flow** with gates and review points — the AI tools (Claude, Codex, Cursor) are adapters onto the contract, not the governance itself. The misreading "this is agentic AI that runs off on its own" is defused at the source.

## Scope
No runtime code, no gate/hook changed. Canonical sentence reused verbatim, no new terminology. No rename of `execution_mode: agentic` or the execution-isolation mechanics. Schrader's term "Agentic Engineering" (production-readiness, not autonomy) stays. Deep chapters (HANDBUCH §8e, CONVENTIONS execution-isolation l. 372/819) are the source, not the target. Wave letter **bl** (bk = gate-assertion BOO-165, bj = role-runbooks BOO-158).

## References
Spec: `specs/BOO-164.md`. Branch: `tobiaschschmidt/boo-164-governance-vs-agentic-framing`. Touches: `README.md`, `HANDBUCH.md` (+EN), `CONVENTIONS.md`, `bootstrap/SKILL.md` (+EN). Related: HANDBUCH §8e, CONVENTIONS §0. Operator source: Tobias, 2026-06-06.
