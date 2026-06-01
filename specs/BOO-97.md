# BOO-97 — Doku-Sync-Sweep (Gap-Audit-Fixes)

## Summary

Repo-weiter Doku-Gap-Audit (6 parallele Subagenten, Lead-gegenverifiziert) + Behebung der High/Medium-Lücken. Reine Doku, kein Verhaltens-Change. Quelle: Audit 2026-06-01.

## Why

Die Skill-READMEs und die Repo-README hingen dem tatsächlichen Feature-Stand hinterher (Versions-Drift zwischen SKILL.md und README), plus zwei tote Reference-Verweise und DE/EN-Paritäts-Lücken. Die SKILL.md-Dateien waren aktuell — die abgeleitete Doku nicht. Ein Governance-Framework sollte seine eigene Doku konsistent halten.

## What

**Welle 1 — Quick-Wins:**
- README: `/intent`-Zeile in beide Skills-Tabellen (fehlte — 12 von 13 Skills); „Was ist neu"-Block auf v0.6.0/v0.6.1 erweitert (DE+EN).
- Tote Verweise entfernt: `implement/references/governance-validation.md` (SKILL.md/.en + README-Tree); `ideation/references/perplexity-api.md` (gehört zum research-Skill) → durch echte `token-heuristik.md` ersetzt.
- security-architect SKILL.md: „## 3 Modi" → „## 4 Modi" (SKILL-SCAN war schon gelistet).
- HANDBUCH DE-Inhaltsverzeichnis „A bis X" → „A bis Y"; Footer-Datum + Changelog (DE+EN).

**Welle 2 — größere Nachzüge:**
- architecture-review README v1.3.0 → v1.12.0 (KI-Tauglichkeits-Checkliste BOO-7, SonarQube-Cloud-Lese-Block BOO-6, Feature-Flag-Hygiene BOO-17) — DE+EN.
- sprint-review README v1.2.0 → v2.6.0 (dpo-Audit-Trigger Schritt 7c, Anti-Pattern-Selbstdiagnose, Reports-/Cost-Aggregation) — DE+EN.
- `security-architect/SKILL.en.md` neu (einziger Bundle-Skill ohne EN).
- `dpo/README.en.md` neu.

## Constraints

- Reine Doku/Onboarding, kein Code-/Verhaltens-Change.
- Subagent-Output Lead-gegenverifiziert (Anti-Fabrikation): „BOO-84/Cost"-Block + KI-Tauglichkeit-Begriffe gegen die echten SKILL.md/References belegt.
- DE/EN paritätisch; Release-Note bilingual (Konvention Regel 6).

## Acceptance Criteria

1. README listet alle 13 Skills inkl. `/intent`; „Was ist neu" referenziert v0.6.0/v0.6.1.
2. Keine toten `references/*.md`-Verweise mehr in implement/ideation.
3. architecture-review/sprint-review README = SKILL-Versionsstand; security-architect SKILL.en.md + dpo README.en.md existieren.
4. HANDBUCH-TOC + Footer aktuell (A–Y, 2026-06-01).

## Result

Umgesetzt (PR #22), Release v0.6.2 (Wave AG, bilingual). Geparkter Low-Backlog → BOO-98.
