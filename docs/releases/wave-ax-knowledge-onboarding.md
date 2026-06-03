# Wave AX — Knowledge-Onboarding: Bestands-Doku in Governance-Artefakte routen (BOO-137)

**Was jetzt da ist:** ein neuer Framework-Bundle-Skill `knowledge-onboarding`, der vorhandenes Projekt-Wissen (GAP-Analysen, Legal-Recherche, README, PLAN, `docs/`-Context, Design-Files, Demo-Storyboards, Handover, Prompt-Library) **deterministisch + wiederholbar** in die Framework-Governance-Artefakte routet. Determinismus durch **Routing-Rubrik (SSoT, 4 Tiers)** + persistiertes **Manifest** (`journal/knowledge-onboarding-map.yml`) + **Pinning** fuer Operator-Korrekturen. Quellen-agnostisch (GitHub-Repo / lokaler Ordner / Chat). Laeuft **post-bootstrap**. EN: [`wave-ax-knowledge-onboarding.en.md`](wave-ax-knowledge-onboarding.en.md).

## Stories
- **BOO-137** — neuer Bundle-Skill `knowledge-onboarding/` (Top-Level, Source-Garantie BOO-121): `SKILL.md`+`.en.md`, `README.md`+`.en.md`, `references/routing-rubric.md`+`.en.md`, Excalidraw-Overview-Sketch DE+EN (Render-Loop, OWLIST-Farben).

## Was der Skill macht (Kurz)

1. **Adapter-Wahl** — 3 Quellen-Adapter (GitHub-Repo / lokaler Ordner / Chat) → einheitliche Datei-Liste.
2. **Pre-Flight** — Framework-Artefakte erkennen (`CLAUDE.md`/`AGENTS.md`/`CONVENTIONS.md`/`ARCHITECTURE_DESIGN.md`/…) → **Tier-0-Ausschluss**.
3. **Manifest lesen** (Determinismus-Anker) — bekannte Files behalten ihr Routing, geaenderte werden re-klassifiziert, `pinned: true` schuetzt.
4. **Klassifikation Tier 0/1/2/3** — Tier 1 Filename, Tier 2 Inhalts-Signale, Tier 3 mehrdeutig → **Operator fragt**, nie raten.
5. **Vorschlag-Tabelle** — kein Auto-Apply; Operator entscheidet.
6. **Routing-Apply** — Default `referenzieren` (Verweis-Block mit Quell-Link/Signal/Tier/Stand), Option `extrahieren` mit Diff-Approval.
7. **Manifest schreiben** (committed, Audit-Trail).
8. **Coverage-Check** — Warnung bei Skip > 50 % oder Tier-3 > 30 %.

## Routing-Rubrik (10 Kategorien + Tier 0)

| Tier | Kategorie | Ziel |
|---|---|---|
| 0 | Framework-Artefakt / Code | skip |
| 1 | Intent · GAP · Scope | `intents/` + `ARCHITECTURE_DESIGN.md §1` |
| 1 | Legal · Compliance | `SECURITY.md`/`GOVERNANCE.md` + DPO + ADR |
| 1 | Design · UI · Visual | `ARCHITECTURE_DESIGN.md §5` + `DESIGN.md` + ADR |
| 2 | Getroffene Entscheidung | ADR `docs/domain/adrs/` |
| 1 | Architektur · Plan | `ARCHITECTURE_DESIGN.md` + Backlog |
| 1 | Vokabular · Kontext | `CONTEXT.md` + Component-Docs |
| 1 | Recherche | `docs/project/research/` |
| 1 | Demo · Storyboard · Pitch | `docs/project/demo/` |
| 1 | Onboarding · Handover | `DEVELOPER_ONBOARDING.md` |
| 1 | Prompt-Library | `docs/project/prompts/` |
| 3 | mehrdeutig | Operator fragt (pinned) |

Vollstaendig (mit Stichwort-Listen + Beispielen): `knowledge-onboarding/references/routing-rubric.md`.

## Anti-Fabrikations-Regeln

- Kein Routing ohne Match-Signal — niemals raten.
- Kein Volltext-Copy ohne Operator-Approval — Default ist `referenzieren`.
- Quell-Verweis Pflicht in jedem eingefuegten Block (`<!-- knowledge-onboarding · BOO-137 · source:<path> · stand:<date> -->`).
- Coverage-Check Pflicht.
- Manifest als Audit-Trail; Operator-Korrekturen mit `pinned: true` sind immutable im Re-Scan.

## Neu / geaendert (DE+EN)

- **Neu:** Skill-Verzeichnis `knowledge-onboarding/` mit 8 Files (SKILL/README/References je DE+EN, Excalidraw + PNG je DE+EN), `specs/BOO-137.md`.
- **Verdrahtung Bootstrap:** `bootstrap/SKILL.md` (DE+EN) Phase 5 Skill-Auswahl (Standard-Tier) + Repo-Struktur-Hinweis + Phase 7.6 Punkt 7 (Hinweis bei Bestands-Doku).
- **`bootstrap/scripts/check-skill-sources.sh`** — `knowledge-onboarding` in `BUNDLE_SKILLS`-Array.
- **`bootstrap/references/skills-setup.md` (DE+EN)** — Skill-Tabelle erweitert (Standard-Tier).
- **`bootstrap/references/existing-infra-check.md`** — `EXISTING_INFRA`-Output um Flag `bestands_doku_erkannt: true|false` ergaenzt.
- **`docs/how-we-document.md` (DE+EN)** §4 — `/knowledge-onboarding` als Schritt 0 vorangestellt (menschliche Doku zuerst, dann `/architecture-review`, dann `framework-upgrade`).
- **HANDBUCH (DE+EN)** — neuer Anhang AC „Knowledge-Onboarding".

## Verweise

Spec: `specs/BOO-137.md`. Branch: `feat/boo-137-knowledge-onboarding`. ADR: SecondBrain `02 Projekte/Code-Crash Framework/Decisions/2026-06-03 Knowledge-Onboarding-Skill — Routing-Rubrik + Manifest-Determinismus.md`. Anlassfall + Rubrik-Validierung: `vibercoder79/bko-widerspruch-assistent`.
