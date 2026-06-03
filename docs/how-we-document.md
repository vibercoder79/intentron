# So dokumentiert dieses Framework (How We Document)

> Konsolidierter Einstieg (BOO-130): **welche** Doku-Artefakte es gibt, **wo** sie leben, **wie fortlaufend** dokumentiert wird und **wie ein bestehendes Repo** auf Stand gebracht wird. Die Details liegen verteilt (HANDBUCH §7, Block C, Hooks) — diese Seite ist die Landkarte. EN: [`how-we-document.en.md`](how-we-document.en.md).

## Prinzip: Docs-as-Code, fortlaufend erzwungen

Dokumentation ist **versionierter Markdown im selben Repo wie der Code** — kein separates Wiki, das verrottet. Sie wird **im selben PR wie die Änderung** mitgeführt und durch Git-Hooks **erzwungen**, nicht durch Disziplin gehofft. Leitsatz: *Doku-synchron* — pro fertiger Story werden die betroffenen Doku-Artefakte mitgezogen.

## 1) Die Artefakte — was entsteht, wo

Beim Bootstrap immer angelegt (BOO-61-Baseline), danach fortlaufend gepflegt:

| Artefakt | Zweck |
|---|---|
| `CLAUDE.md` / `AGENTS.md` | Runtime-Einstieg für die KI (inkl. Session-Start-Routine, BOO-129) |
| `CONVENTIONS.md` | Tool-/Adapter-Vertrag (Runtime, Backlog, Gates) |
| `ARCHITECTURE_DESIGN.md` | **Hub** — §9 verlinkt alle Doku-Schichten automatisch |
| `GOVERNANCE.md` / `SECURITY.md` | Governance-Regeln · Threat-Model (SECURITY.md via `security-architect` befüllen) |
| `specs/<PREFIX>XXX.md` | Story-Spec — Pflicht vor jeder Code-Änderung (Spec-Gate) |
| `INDEX.md` | Datei-Index des Projekts |
| `journal/` | Reports, Sprint-/Learning-Einträge |
| `docs/project/{README, decisions/, meetings/, research/}` | Projekt-Doku-SSoT bei `repo-docs` (PMO-Hub + ADRs + Protokolle) |
| `DEVELOPER_ONBOARDING.md` | Einarbeitung neuer Menschen/Tools |

Vollständige Tabelle + Owner: **HANDBUCH §7 „Die Artefakte — was entsteht, wo, und warum"**.

## 2) Die drei Doku-Schichten (Block C)

1. **Story-Specs** (Repo) — eine Spec pro Story, Ground Truth fürs Implement.
2. **Project-Docs** — Obsidian-Vault **oder** `docs/project/` (repo-docs) **oder** externes DMS (mit Repo-Verweis).
3. **Component-/Architektur-Docs** — pro Komponente, unter dem Hub.

**Hub & Auto-Verlinkung:** `ARCHITECTURE_DESIGN.md §9` registriert jede neue `*.md` automatisch. Wahl der SSoT-Variante: `references/project-documentation-ssot.md`.

## 3) Wie „fortlaufend" erzwungen wird (Gates)

| Mechanik | Wirkung |
|---|---|
| `spec-gate.sh` | kein Commit mit Story-Bezug ohne `specs/<PREFIX>XXX.md` |
| `doc-version-sync.sh` | **HARD GATE** — kein `git push` bei Versions-Drift zwischen DOC_FILES |
| `orphan-check.sh` (opt-in) | kein Doc ohne Eintrag im Hub (§9) |
| **Session-Start-Routine** (BOO-129) | bei `repo-docs`: Claude liest PMO-Hub + neueste `meetings/`/`decisions/`, schreibt am Ende zurück → Markdown-Ordner werden zum lebenden „Brain" |
| **Doku-synchron-Prinzip** | pro Story-Done: HANDBUCH/Specs/Release-Notes/Backlog mitziehen |

Gegen **Drift / „Wiki-Rot"** (das Haupt-Scheitern-Muster von Wikis) wirkt strukturell die Docs-as-Code-Kopplung + diese Gates.

## 4) Bestehendes / fremdes Repo auf Stand bringen

„Lies das Repo aus, route die Doku, mach Architektur-Review, bring die Artefakte auf Stand" ist ein definierter Pfad — drei Schritte in dieser Reihenfolge:

0. **`/knowledge-onboarding`** (BOO-137) — **menschliche Doku zuerst**. Routet vorhandenes Vor-Material (GAP-Analysen, Legal-Recherche, README, PLAN, `docs/`-Context, Design-Files, Demo-Storyboards, Handover, Prompts) deterministisch in die Governance-Artefakte. Quellen-agnostisch (GitHub-Repo / lokaler Ordner / Chat), Routing-Rubrik als SSoT, Manifest in `journal/knowledge-onboarding-map.yml` als Determinismus-Anker. Default: referenzieren (kein Volltext-Copy). Tier-3-Faelle frag Operator, nicht raten.
1. **`/architecture-review`** liest den Code + prüft die 8 KI-Architektur-Checks.
2. **Bestands-Onboarding** (HANDBUCH **Anhang U**) + **`references/framework-upgrade.md`** (`inspect` → `apply-safe` → `apply-with-confirmation`) ziehen Artefakt-Skelette idempotent nach (`migrate-to-v2.sh --issue BOO-XX`).
3. Ergebnis-Report nach `journal/reports/framework-upgrade/YYYY-MM-DD.md`; bewusste Abweichungen werden **dokumentiert statt überschrieben**.

## Verweise

HANDBUCH §7 (Artefakte) · Block C / §6 · `references/project-documentation-ssot.md` · Anhang T (Verifikation) · Anhang U (Bestands-Onboarding) · BOO-129 (Session-Start-Loop). Begriffe unklar? → Glossar (Anhang C / `docs/glossar.md`).
