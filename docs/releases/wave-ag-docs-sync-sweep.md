# Wave AG — Doku-Sync-Sweep (BOO-97)

**Linear:** [BOO-97](https://linear.app/owlist/issue/BOO-97/)

## Problem

Ein Repo-weiter Doku-Gap-Audit (6 parallele Subagenten, gegen-verifiziert) zeigte: die
Skill-READMEs und die Repo-README hingen dem tatsaechlichen Feature-Stand hinterher
(Versions-Drift), plus zwei tote Reference-Verweise und Paritaets-Luecken.

## Stories

| Story | Inhalt | Status |
|-------|--------|--------|
| **BOO-97** | Repo-weiter Doku-Gap-Audit (6 Subagenten) + Behebung der High/Medium-Luecken | ✅ done |

## Was sich aendert

- **README:** `/intent`-Zeile in beiden Skills-Tabellen ergaenzt (fehlte — 12 von 13 Skills);
  „Was ist neu"-Block auf v0.6.0/v0.6.1 erweitert (DE+EN).
- **Tote Verweise entfernt:** `implement/references/governance-validation.md` (SKILL.md/.en +
  README-Tree) und `ideation/references/perplexity-api.md` (gehoert zum research-Skill → durch
  echte `token-heuristik.md` ersetzt).
- **architecture-review README** v1.3.0 → **v1.12.0**: KI-Tauglichkeits-Checkliste (BOO-7),
  SonarQube-Cloud-Lese-Block (BOO-6), Feature-Flag-Hygiene (BOO-17) nachgezogen (DE+EN).
- **sprint-review README** v1.2.0 → **v2.6.0**: dpo-Audit-Trigger (Schritt 7c),
  Anti-Pattern-Selbstdiagnose, Reports-/Cost-Aggregation nachgezogen (DE+EN).
- **EN-Paritaet:** `security-architect/SKILL.en.md` neu (einziger Bundle-Skill ohne EN) +
  `dpo/README.en.md` neu.
- **security-architect SKILL.md:** Ueberschrift „3 Modi" → „4 Modi" (SKILL-SCAN war schon
  gelistet).
- **HANDBUCH:** DE-Inhaltsverzeichnis „A bis X" → „A bis Y"; Footer-Datum + Changelog (DE+EN)
  auf aktuellen Stand.

## Bewusst als Folge-Backlog vermerkt (nicht in diesem Sweep)

Granulare `wave-ab…ag.md` (Regel-1-Backfill), HANDBUCH §13 „v0.2.0-Themen"-Framing,
claudecodeskills-Restverweise in §3/§5/§7, intent EN-Templates, coverage-check in hooks-setup,
3 Low-Version-Bumps (visualize/grafana/cloud-system-engineer).

## Effekt

Die Doku spiegelt wieder den realen Feature-Stand; keine toten Verweise mehr; alle Bundle-Skills
DE+EN. Reine Doku, kein Verhaltens-Change.

## Verweise / Release

- Branch `feat/boo-97-doku-sync`. Release: **v0.6.2 (Wave AG)** — siehe
  `docs/releases/v0.6.2-overview.md`. (Detail-Spec `specs/BOO-97.md` liegt nicht im Repo vor;
  Quelle dieser Notiz ist der v0.6.2-Overview.)
