# BOO-84 — Token-Effizienz-Policy (Modell-Routing + Prompt-Caching)

## Summary

Verankert eine systematische Token-Effizienz-Policy im Framework: pro Skill empfohlenes Modell-Tier (Haiku/Sonnet/Opus), zentrales Tier-Mapping mit Pricing, Prompt-Caching fuer SKILL.md + Constitution + Repo-Map, drei-Ebenen-Cost-Tracking in `meta.json` und Cost-Aggregation im Sprint-Review. Erwarteter Effekt: **50-70% Token-Reduktion pro Story**, ~15-25% Marge-Hebel bei Kunden-Engagements.

## Why

Heute laeuft jeder Skill auf dem Modell, das der Operator in Claude Code eingestellt hat — meist Opus 4.7. Bei einfachen Aufgaben (Lint-Iterationen, Frage-Generierung, Smoke-Tests) ist das **massiver Overkill**: 5 Lint-Iterationen auf Opus = ~$0.50; auf Haiku 4.5 = ~$0.04 (Faktor 12x). Daneben fehlt eine systematische Prompt-Caching-Strategie (Anthropic gibt 90% Rabatt auf gecachte Tokens), und es gibt keine Konvention in `CLAUDE.md`, welcher Skill auf welchem Modell laufen soll.

Konsequenzen ohne diese Story:

- Marge bei Kunden-Engagements 15-25% niedriger als noetig.
- Kein USP "Code-Crash ist Token-optimiert" gegenueber Spec Kit, Aider, Cline.
- Bei FINMA-Audit keine Antwort auf "wie stellt ihr Cost-Effizienz beim KI-Einsatz sicher?".

## What

- **Frontmatter-Erweiterung** aller Bundle-Skills: `recommended_model: haiku | sonnet | opus` (tier-basiert, kein Versions-Suffix).
- **Neues File `bootstrap/references/model-tiers.json`**: Tier-zu-Version-Mapping + USD-Pricing pro Tier (`price_per_million_input`, `cached_input_price`, `output_price`).
- **Bootstrap-Erweiterung**: ergaenzt eine **Model-Routing-Sektion in `CLAUDE.md`** beim Init, inklusive `model_overrides:`-Sektion fuer projekt-weite Default-Aenderung.
- **Operator-Override zweistufig**: CLI-Flag `/implement --model opus` (einmalig) + CLAUDE.md `model_overrides:` (persistent). Praezedenz: CLI > CLAUDE.md > Skill-Default.
- **Prompt-Caching-Markers** systematisch aktiviert fuer SKILL.md-Files, CONVENTIONS.md, SECURITY.md, ARCHITECTURE_DESIGN.md, Repo-Map.
- **`meta.json`-Schema-Erweiterung**: Token-Tracking auf drei Ebenen (pro Iteration / pro Skill-Aufruf / pro Story) + Cache-Hit-Rate + Override-Audit-Trail.
- **`/sprint-review` aggregiert** Cost-Daten pro Sprint mit Breakdown nach Modell-Tier.
- **HANDBUCH-Erweiterung**: zwei neue Sektionen "Prompt-Caching technisch erklaert" und "Modell-Routing-Policy" (DE+EN).
- **Migration**: `migrate_boo_84()` in `migrate-to-v2.sh` + `migration-checklist-v1-to-v2.md` §BOO-84 (DE+EN).
- **CHANGELOG**: Eintrag mit Cost-Reduktions-Zahlen.

## Constraints

- Keine **Hard-Blocks** beim Modell-Wahl — Operator-Override muss moeglich bleiben.
- Kein Force-Cache fuer Aufrufe <1024 Tokens (unter Anthropic-Minimum).
- Security-relevante Skills (`architecture-review`, `analyze` falls existent, `implement` Schritt 6e) bleiben **nachweisbar auf Opus** — Audit-Argument fuer regulierte Branchen.
- Keine Secrets in Cache-Bloecken.
- DE + EN konsistent.

## Decisions

Entschieden in Q&A-Session 2026-05-25 (siehe SecondBrain `02 Projekte/Code-Crash Framework/Q&A.md` §BOO-84):

1. **Tier-basiert** (haiku/sonnet/opus) statt hartkodiert. Tier-zu-Version-Mapping zentral in `model-tiers.json`, einmalig pro Anthropic-Release zu aktualisieren.
2. **Drei-Ebenen-Cost-Tracking** (Iteration / Skill / Story) + Cache-Hit-Rate.
3. **USD-Pricing hartkodiert** in `model-tiers.json` mit Release-Pflicht zur Aktualitaets-Pruefung.
4. **Override zweistufig**: CLI-Flag + CLAUDE.md `model_overrides:`, mit Audit-Trail in `meta.json`.
5. **Test-Lauf via BOO-74**: BOO-74 wird als Test-Story durchlaufen, Vor/Nach-Vergleich im PR.

Begleitender ADR: SecondBrain `Decisions/2026-05-25 Designprinzip Leichtgewichtigkeit ohne Security-Kompromisse.md` — BOO-84 erfuellt den Designentscheid durch Empfehlung-statt-Hard-Lock-Pattern.

## Agent-Pattern

**Gewaehltes Pattern:** Linear-Lead mit gezielten Sub-Agents fuer HANDBUCH-Sektionen.

**Begruendung:** Skill-Frontmatter-Updates sind 11x dasselbe Pattern (idempotent, klein) — schneller direkt im Lead-Modus als ueber Sub-Agent-Briefing. HANDBUCH-Sektionen sind substantielle Schreibarbeit mit klar abgegrenztem Scope — gut delegierbar mit "nicht erfinden"-Constraint, EN-Pass durch Lead (Memory-Feedback zu Heredoc-Timeouts).

## Validation

- Manueller Test: `/implement` Schritt 6e (Security-Findings) bleibt auf Opus — kein Auto-Downgrade.
- Manueller Test: `/architecture-review` bleibt auf Opus.
- Cache-Marker enthalten keine Secrets.
- BOO-74 Test-Lauf mit Routing+Caching dokumentiert (PR-Belege).
- `git diff --check` clean.
- `rg "haiku-4.5\|sonnet-4.6\|opus-4.7"` zeigt keine hartkodierten Versionen mehr in Skill-Frontmattern (nur in `model-tiers.json`).

## Acceptance Criteria

- Alle Bundle-Skills haben `recommended_model:` im Frontmatter (tier-basiert).
- `bootstrap/references/model-tiers.json` mit Tier-zu-Version-Mapping + Pricing existiert.
- Bootstrap-Skill schreibt Model-Routing-Sektion in CLAUDE.md beim Init.
- `meta.json`-Schema dokumentiert 3-Ebenen-Tracking + Cache-Hit-Rate + Override-Audit.
- `/sprint-review` Report enthaelt Cost-Aggregation mit Modell-Tier-Breakdown.
- HANDBUCH (DE+EN) hat beide neuen Sektionen.
- `migrate_boo_84()` implementiert, migration-checklist §BOO-84 ergaenzt.
- CHANGELOG-Eintrag mit Cost-Reduktions-Erwartung.
- BOO-74 Test-Lauf-Resultat im PR dokumentiert (Vor/Nach-Tabelle).
