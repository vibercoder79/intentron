# Wave AW — Documentation hardening & onboarding clarity (BOO-130–136)

**What's now there:** a consolidated "how we document" entry point, a plain-language glossary for non-developers, GitHub Issues as the visibly recommended backlog standard, a Linear-MCP-on-VPS runbook, a canonical onboarding filename, the GitHub-Pro note for branch protection, and a SECURITY.md next step. Result of the 2026-06-03 documentation review. DE: [`wave-aw-doku-haertung.md`](wave-aw-doku-haertung.md).

## Stories
- **BOO-130** — `docs/how-we-document.en.md` (+ DE, + sketch): the doc model on one page (artifacts · 3 layers · gates · existing-repo path); linked from HANDBUCH §7.
- **BOO-131** — `docs/glossar.en.md` (+ DE): plain-language glossary (runner, MCP, hook, gate, PR, spec, ADR …) for non-developers; linked from Appendix C.
- **BOO-132** — A.3b marks **GitHub Issues as the recommended standard** (mechanism unchanged).
- **BOO-133** — HANDBUCH **Appendix AB**: Linear-MCP-on-headless-VPS runbook (SSH port-forward OAuth + token setup without a leak); §3 token location corrected (Settings → Security and Access); §8g deeplink.
- **BOO-134** — onboarding filename canonical **`DEVELOPER_ONBOARDING.md`** (fixes the verify-setup WARN mismatch on repo-docs); rule "no HANDBUCH.md in the project".
- **BOO-135** — §3 + Appendix A: **GitHub Pro/Team** required for branch protection on private repos (public free).
- **BOO-136** — phase 7.6: next step "**fill SECURITY.md via security-architect (DESIGN)**" + basis clarification.

## New / changed (DE+EN)
- **New:** `docs/how-we-document.md`, `docs/glossar.md` (each + `.en`), sketch `docs/assets/boo-130-how-we-document.{excalidraw,png}` (+ `.en`), HANDBUCH **Appendix AB**.
- **HANDBUCH:** §3 (GitHub Pro + Linear token location), §7 (pointer), Appendix A (branch-protection plan), Appendix C (glossary pointer), §8g (AB deeplink), TOC + §13 signpost (28 appendices).
- **`bootstrap/SKILL.md`:** A.3b (GitHub default), phase 7.6 (SECURITY next step).
- **`references/`:** `project-documentation-ssot.md` (canonical onboarding name), `verify-setup.sh` (WARN clarified).

## References
Specs: `specs/BOO-130.md` … `BOO-136.md`. Branch: `feat/boo-doku-haertung`. RAG/layer-2 design input → SecondBrain Factory research (not in the bootstrap).
