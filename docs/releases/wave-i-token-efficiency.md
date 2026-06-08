# Release Notes - Wave I Token-Effizienz-Policy

> 🌐 **Sprache:** Deutsch (diese Datei) · [🇬🇧 English](wave-i-token-efficiency.en.md)

Stand: 2026-05-25

## Zweck

Wave I schliesst BOO-84. Das Framework verankert eine systematische Token-Effizienz-Policy: pro Skill empfohlenes Modell-Tier (Haiku/Sonnet/Opus), zentrales Tier-Mapping mit USD-Pricing, Prompt-Caching fuer wiederverwendete Bloecke und Cost-Tracking in `meta.json`. Erwarteter Effekt: 50-70% Token-Reduktion pro Story, ~15-25% Marge-Hebel bei Kunden-Engagements.

## Betroffene Stories

- BOO-84

## Was Nutzer mit dem neuen Setup bekommen

- Pro Skill ein **empfohlenes Modell-Tier** (`haiku | sonnet | opus`) im Frontmatter — Operator muss nicht mehr manuell vor jedem Run das Modell wechseln.
- Ein **zentrales Mapping-File** `bootstrap/references/model-tiers.json` mit Tier-zu-Version und USD-Pricing. Bei Anthropic-Releases einmalig zentral aktualisieren statt 11 Skill-Files anfassen.
- **Operator-Override jederzeit moeglich** — zweistufig: CLI-Flag `/implement --model opus` (einmalig) plus `model_overrides:` in CLAUDE.md (projekt-weit). Override-Audit-Trail in `meta.json` fuer Compliance.
- **Prompt-Caching systematisch aktiv** fuer SKILL.md, Constitution, SECURITY.md, ARCHITECTURE_DESIGN.md, Repo-Map — 90% Rabatt auf wiederverwendete Bloecke.
- **Cost-Aggregation im Sprint-Review** — pro Sprint USD-Cost-Aufschluesselung nach Modell-Tier, Cache-Hit-Rate, Override-Count.
- **Audit-Argument fuer regulierte Branchen** — Security-relevante Skills (`architecture-review`, `cloud-system-engineer`, `/implement` Schritt 6e) bleiben nachweisbar auf Opus, kein Auto-Downgrade.

## Konkrete Aenderungen

| Bereich | Aenderung | Datei |
|---|---|---|
| Tier-Mapping NEU | Zentrales JSON mit Versions- und Pricing-Mapping | `bootstrap/references/model-tiers.json` |
| Skill-Frontmatter | `recommended_model:` in allen 11 Bundle-Skills (DE+EN), Tier-basiert | `*/SKILL.md`, `*/SKILL.en.md` |
| Bootstrap-Phase 4.4m | Neue Sub-Phase "Token-Effizienz-Setup" — schreibt Model-Routing-Sektion in CLAUDE.md | `bootstrap/SKILL.md` v3.26.0 |
| CLAUDE.md-Template | Neue Sektionen "Model-Routing-Policy" + "Prompt-Caching" | `bootstrap/references/file-templates.md` |
| implement Schritt 6f-bis | `meta.json` um 3-Ebenen-Token-Tracking + Cache-Hit-Rate + Override-Audit-Trail erweitert | `implement/SKILL.md` v2.10.0 |
| sprint-review Schritt 2b | Cost-Aggregation pro Sprint mit Tier-Breakdown | `sprint-review/SKILL.md` v2.5.0 |
| HANDBUCH Anhang N NEU | Kombinierte Sektion Modell-Routing-Policy + Prompt-Caching technisch erklaert | `HANDBUCH.md` (DE+EN) |

## Skill-Versions-Bumps

- `architecture-review` 1.11.0 -> 1.12.0
- `backlog` 1.4.0 -> 1.5.0
- `bootstrap` 3.25.0 -> 3.26.0
- `cloud-system-engineer` 1.0.0 -> 1.1.0
- `grafana` 1.0.0 -> 1.1.0
- `ideation` 2.5.0 -> 2.6.0
- `implement` 2.9.0 -> 2.10.0
- `intent` 1.2.0 -> 1.3.0
- `pitch` 1.0.0 -> 1.1.0
- `sprint-review` 2.4.0 -> 2.5.0
- `visualize` 2.2.0 -> 2.3.0

## Migration fuer Bestands-Projekte

`migrate_boo_84()` in `bootstrap/scripts/migrate-to-v2.sh`:

1. Schreibt Model-Routing-Sektion in projekt-lokale `CLAUDE.md` (idempotent).
2. Setzt projekt-weite `model_overrides:` Default-Block (leer, Operator fuellt nach Bedarf).
3. Erweitert `meta.json`-Schema-Doku in `journal/reports/local/README.md` (optional).

Operator fuehrt manuell aus:

```bash
bash bootstrap/scripts/migrate-to-v2.sh boo_84
```

Migration ist additive — bestehendes Verhalten bleibt unveraendert, neue Felder werden ergaenzt.

## Designentscheid-Konformitaet

Diese Wave folgt dem INTENTRON-Leitsatz "leichtgewichtig + pragmatisch, ohne Security-Kompromisse":

- **Empfehlung statt Hard-Lock**: Operator kann jederzeit Modell uebersteuern, kein Block bei Tier-Wahl.
- **Audit-Trail fuer Compliance**: jede Override wird protokolliert (FINMA/BaFin-faehig).
- **Security-Bleibt-Opus dokumentiert**: explizite Spec-Anforderung, keine stille Optimierung auf Kosten der Sicherheit.
- **Hook-Aktivierung optional**: ohne Caching-Hook funktioniert alles weiter, nur ohne Cost-Aggregat.

## Erwartete Wirkung

Bei 5 Lint-Iterationen pro Story: ~95% guenstiger als naive Opus + kein Cache (Haiku-Routing 12x guenstiger als Opus, plus Caching 70% Reduktion auf wiederverwendete Bloecke). Bei 6-Monats-Engagement mit ~80 Stories: 15-25% Marge-Hebel. USD-Cost wird pro Sprint im Sprint-Review-Report ausgewiesen — FinOps-Argument fuer Discovery-Gespraeche.

## Folgepunkte

- **PostToolUse-Hook fuer Auto-Token-Capture**: optionaler Folge-Skill, der `.claude/last-run-tokens.json` und `.claude/last-run-overrides.json` waehrend des Runs schreibt. Ohne Hook bleiben `meta.json.token_tracking`-Felder leer — kein Story-Lauf blockiert.
- **BOO-74 Test-Probelauf**: BOO-74 (Constitution-Refactor) wird mit aktivem Routing + Caching durchlaufen, Vor/Nach-Cost-Tabelle wird im BOO-84-PR oder im BOO-74-PR dokumentiert.
- **Release-Pflicht**: `model-tiers.json` Versions- und Pricing-Eintraege pro INTENTRON-Release gegen Anthropic-Pricing-Seite pruefen (Eintrag in der projektinternen Handbuch-Sync-Queue).
