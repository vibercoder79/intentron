# Wave BR — implement: Lint-Loops auf Haiku-Subagent (BOO-171)

**Was jetzt da ist:** `/implement` delegiert seine mechanischen Iterations-Loops (6a ESLint/Ruff, 6a-bis Semgrep) an einen neuen **`lint-fixer`-Subagenten mit `model: haiku`** — der teure Reasoning-Teil (Code-Kern Schritt 5, Security-Findings 6e) bleibt auf **Opus**. Schließt die interne Tier-Lücke, die BOO-170 (ein Top-Level-Modell pro Subprozess) offenließ. Schlanke Variante: genau der eine reale Kostenhebel.

## Stories
- **BOO-171** — Lint-Loops auf Haiku-Subagent (BOO-170-Folge).

## Änderungen
- **Neu `implement/references/lint-fixer.agent.md`** — benannte Subagent-Definition (`model: haiku`, tools Read/Edit/Write/Bash), rein mechanischer „fix bis grün"-Worker mit harten Grenzen.
- **implement Schritt 6a (DE+EN):** Delegations-Block — 6a/6a-bis an `lint-fixer` (haiku), Code-Kern (5) + Security (6e) bleiben Opus, graceful degradation (Subagent aus → Parent iteriert selbst).
- **Version:** implement 2.14.0 → 2.15.0. `model-tiers.json` unverändert (`implement-iterations: haiku` existierte bereits).

## Spike (verifiziert)
Subagenten tragen `model:` im Frontmatter; opus-Parent kann haiku-Child spawnen (zuverlässig via benanntem `.claude/agents/*.md`). **Caveat:** Kosten-Attribution pro Subagent ist CC-seitig nicht garantiert. Befund: implement hatte das `meta.json`-Tier-Schema schon, der Loop lief aber inline — diese Story macht die Delegation real.

## Wirkung
Die stumpfen Lint-/Test-Fix-Schleifen laufen auf dem günstigsten Modell (~19× billiger im Output als Opus), ohne Qualitätsverlust am Code-Kern. Konsistent mit dem `meta.json`-Tier-Tracking.

## Abgrenzung
Schlanke Variante. **Offen (Folge):** automatisches bootstrap-Scaffolding von `.claude/agents/lint-fixer.md`; vollausführbarer VPS-Daemon (Variante B); verlässliche Subagent-Kosten-Attribution. Ein separater opus-Security-Subagent wurde bewusst weggelassen (Parent ist eh Opus). Wave-Buchstabe **br** (bq = Daemon-Model-Routing BOO-170).

## Verweise
Spec: `specs/BOO-171.md`. Branch: `feat/boo-171-implement-subagent-routing`. Verwandt: BOO-170 (Daemon-Top-Level-Routing), BOO-84 (Tier-Routing), BOO-157 (sprint-run). Operator-Quelle: Tobias, 2026-06-06.
