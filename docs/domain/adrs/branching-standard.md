# ADR: Branching-Standard — Trunk-Based mit geschützter `main` (BOO-124)

- **Status:** akzeptiert (2026-06-03)
- **Kontext-Quelle:** Probelauf-Folgefrage (BKO, 2026-06-02) — „Mit welchem Standard kommt ihr?"

## Kontext
Die Branch-Strategie-**Optionen** (Trunk-Based / Feature-Branches+PR / GitFlow) waren im HANDBUCH
(Multi-Operator-Anhang R) als gleichwertige Trade-off-Tabelle dokumentiert — **ohne benannten Default**.
Im Verkauf/Onboarding fehlte die klare Antwort „unser Standard ist X". INTENTRON ist auf kurze Stories,
parallele Agentenarbeit und auditierbare Gates ausgelegt.

## Entscheidung
Der **Default-Branching-Standard** des Frameworks ist **Trunk-Based Development mit geschützter `main`**:
- geschützte `main` (Branch-Protection BOO-29 + Spec-Gate BOO-4/27),
- **kurzlebige Feature-Branches** (max 1–2 Tage),
- **Pull Requests** mit mindestens 1 Review,
- **Required Status Checks** (ESLint/Ruff/Semgrep/Tests/… + ggf. SonarCloud/typecheck) müssen grün sein.

**Verkaufs-Einzeiler:** „Unser Standard ist Trunk-Based Development mit geschützter `main` und PR-Gates —
schlank, auditierbar, agenten-tauglich. Multi-Environment-Branching (GitFlow & Co.) bieten wir an, wo die
Release-Realität es verlangt."

## Begründung
- **Leichtgewichtig:** wenige langlebige Branches → minimale Merge-Hölle.
- **Agenten-tauglich:** kurze Branches reduzieren Merge-Drift bei paralleler Agentenarbeit (Execution-Isolation).
- **Qualitätssicherung:** geschützte `main` + Gates erzwingen Review + grüne Checks vor jedem Merge.

## Alternativen (nicht Default)
- **Feature-Branches mit PR-Review:** robust für 5–15 Operatoren; Branches können lange leben → steigende Konflikte.
- **GitFlow:** release-getriebene Branchen (`develop`, `release/*`, `hotfix/*`); für audit-pflichtige Regulatorik —
  komplexer, langsamer. Angeboten, wo die Release-Realität es verlangt.

Vollständige Trade-off-Tabelle + Skalierungs-Empfehlung nach Team-Größe: HANDBUCH Anhang R §Layer-1
„Alternativen (wenn nicht unser Default)". Visualisierung: `docs/assets/boo-124-branching-standard.png`.

## Konsequenzen
- Bootstrap/Branch-Protection (BOO-29) bilden den Default bereits ab (geschützte `main`, Required Checks).
- In gebootstrappten Projekten wird diese ADR aus `ARCHITECTURE_DESIGN.md §9 Referenzen` verlinkt.
- Abweichungen (Feature-Branches-only, GitFlow) sind erlaubt, aber als eigene Projekt-ADR zu begründen.
