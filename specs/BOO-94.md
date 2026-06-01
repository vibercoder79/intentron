# BOO-94 — VPS-Team-Runbook zu HANDBUCH-Anhang Y promoten (DE+EN + Diagramm)

## Summary

Das standalone Runbook `docs/runbooks/vps-team-setup.md` (DE, aus PR #16) wird zum vollwertigen **HANDBUCH-Anhang Y „VPS/Cloud-Team-Runbook"** promotet: **zweisprachig** (HANDBUCH.md + HANDBUCH.en.md, strikt paritätisch) und mit **Excalidraw-Übersichtsdiagramm** (DE + EN + PNG), konsistent zu den Deployment-Anhängen P/Q/R/S/T/U/V. Anhang Y wird die **kanonische** Quelle; das standalone Runbook wird auf einen Kurz-Pointer reduziert (Single-Source, kein Drift). Der Anhang-Index läuft danach **A–Y** statt A–X.

## Why

Das Runbook ist aktuell ein standalone Doc unter `docs/runbooks/` — wertvoll, aber **nicht Teil des kanonischen HANDBUCHs**, nicht aus dem Inhaltsverzeichnis verlinkt, nicht zweisprachig und ohne Diagramm. Die übrigen Deployment-/Betriebs-Themen (P Deployment-Szenarien, Q Souveränität, R Multi-Operator, S Skill-Installation, T Verifikation, U Multi-Projekt, V Bodyguard) sind dagegen nummerierte, DE+EN-paritätische Anhänge mit Querverweisen. Der VPS-Team-Lebenszyklus (einmal-pro-VPS → pro-Projekt → Team) ist genau das Bindeglied zwischen §8d, P und U und gehört als Anhang Y in dieselbe Reihe. Zwei parallele Quellen (standalone Runbook + Anhang) wären ein Drift-Risiko — deshalb wird Anhang Y kanonisch und das Standalone-Doc ein Pointer.

Konsequenzen ohne diese Story:
- Das Runbook bleibt aus dem HANDBUCH unauffindbar (kein TOC-Eintrag, kein Querverweis aus §8d/P/U).
- Kein EN-Pendant — inkonsistent zur DE/EN-Parität aller anderen Anhänge.
- Kein Diagramm — der VPS→Projekt→Team-Lebenszyklus bleibt rein textuell, anders als die übrigen Deployment-Anhänge.

## What

- **Anhang Y „VPS/Cloud-Team-Runbook"** in `HANDBUCH.md` (DE) **und** `HANDBUCH.en.md` (EN), inhaltlich aus `docs/runbooks/vps-team-setup.md` synthetisiert (Anhang-Form, nicht 1:1-Copy): Szenario-Wahl (P), einmal-pro-VPS vs. pro-Projekt, Git-Hooks-pro-Repo, Onboarding Projekt 2..N + Brownfield (`migrate-to-v2.sh`), Team (CODEOWNERS/Branch-Protection, R), Entscheidungen (Docker vs. Direkt-Install, Git-lokal vs. GitHub, Souveränität Q), Vier-Layer auf headless VPS. Im HANDBUCH-Inhaltsverzeichnis (Anhang-Übersicht) verlinkt.
- **Excalidraw-Diagramm** `docs/assets/vps-team-runbook.excalidraw` (+ `.en.excalidraw` + beide `.png`): Lebenszyklus VPS-Setup → Projekt-Wiring → Multi-Projekt/Team, mit der einmal-pro-VPS-vs-pro-Projekt-Trennung als visuellem Kern. Gerendert über die vorhandene Render-Pipeline (excalidraw-diagram-Skill), visuell validiert.
- **Anhang-Index auf A–Y heben** (DE+EN paritätisch):
  - HANDBUCH-Anhang-Übersicht: „24 Anhänge (A–X)" / „24 appendices (A–X)" → „25 … (A–Y)"; die N–X-Themenliste um Y (VPS/Cloud-Team-Runbook) ergänzen.
  - README: „Anhänge A–X" / „appendices A–X" → „A–Y" inkl. Aufzählungs-Eintrag Y.
  - CONVENTIONS: „Anhang A-X" / „Appendix A-X" → „A-Y".
- **Standalone-Runbook → Pointer:** `docs/runbooks/vps-team-setup.md` wird auf einen kurzen Verweis „Dieses Runbook ist jetzt HANDBUCH-Anhang Y — siehe HANDBUCH.md/.en.md" reduziert (kein duplizierter Inhalt → kein Drift). Alternativ-Entscheid (siehe Decisions): Datei entfernen und Querverweise umbiegen.
- **Querverweise** von §8d, Anhang P und Anhang U auf Anhang Y ergänzen (DE+EN).
- **Release Note** (v0.6.x bzw. nächste passende Version).

## Constraints

- **Strikt DE/EN-paritätisch** — Anhang Y, Index-Stellen, Querverweise.
- **Anhang Y kanonisch, Standalone nur Pointer** — kein Doppel-Inhalt (Drift-Vermeidung; konsistent mit der Single-Source-Linie BOO-89).
- **Keine inhaltliche Neuerfindung** — nur Promotion des bereits in PR #16 belegten Runbook-Inhalts; alle Aussagen bleiben gegen die Anhänge P/Q/R/S/T/U/V + §8d belegt.
- **Diagramm im Stil der bestehenden** (Farb-Palette/Schrift aus den vorhandenen Diagrammen, Render-Pipeline `excalidraw-diagram` → PNG; DE+EN-Variante wie beim Vier-Layer-Quality-Gate-Diagramm).
- **Leichtgewicht:** reine Doku/Diagramm, kein Verhaltens-Change, keine neue Dependency.

## Decisions

1. **Anhang Y wird kanonisch**, das standalone `docs/runbooks/vps-team-setup.md` wird zum Pointer (nicht gelöscht, um bestehende Links/PR-#16-Historie nicht zu brechen). Falls beim Umsetzen ein toter Pointer stört: Datei entfernen + Querverweise umbiegen — beim Implement entscheiden.
2. **Zweisprachig + Diagramm** — bringt den Anhang auf das Niveau von P/Q/R/S/T/U/V (DE+EN, mit Sketch).
3. **Diagramm DE+EN** (zwei Varianten + PNGs), analog `quality-gate-four-layers`.
4. **Index überall mitziehen** (HANDBUCH-Übersicht, README, CONVENTIONS) — sonst entsteht derselbe Selbstwiderspruch wie vor der Vier-Layer-Sync (A–U vs. A–X).

## Agent-Pattern

**Gewähltes Pattern:** `sub-agents` (Story Points 3).

**Begründung:** Klar abgegrenzte Brocken — (a) DE-Anhang in HANDBUCH.md, (b) EN-Anhang in HANDBUCH.en.md (separater Pass, nicht im selben Sub-Agent wie DE), (c) Excalidraw-Diagramm DE+EN + Render, (d) Index-/Querverweis-Updates. Lead (Orchestrator) merged, prüft DE/EN-H2/H3-Parität, verifiziert die gerenderten PNGs selbst und gleicht den Anhang-Index ab. Hard-Constraint pro Sub-Agent: keine inhaltliche Neuerfindung, nur Promotion des Runbook-Inhalts; Diagramm-Farben/Schrift aus bestehenden Diagrammen.

## Validation

- Anhang Y existiert in HANDBUCH.md UND HANDBUCH.en.md, gleiche H2/H3-Struktur, im Inhaltsverzeichnis (Anhang-Übersicht) verlinkt.
- `grep -rniE "A–X|A-X"` über README/CONVENTIONS/HANDBUCH* liefert keine veralteten Treffer mehr (außer bewusst korrekten Stellen); „25 Anhänge / 25 appendices (A–Y)" konsistent.
- Beide Diagramm-PNGs neu gerendert (gleicher Zeitstempel wie die `.excalidraw`), visuell auf Überlappung/Layout geprüft.
- `docs/runbooks/vps-team-setup.md` enthält keinen duplizierten Volltext mehr, sondern den Pointer.
- Querverweise §8d/P/U → Y vorhanden (DE+EN).
- `git diff --check` clean; DE/EN-Parität geprüft.

## Acceptance Criteria

- [ ] Anhang Y „VPS/Cloud-Team-Runbook" in HANDBUCH.md (DE) + HANDBUCH.en.md (EN), paritätisch, im TOC/Anhang-Übersicht verlinkt
- [ ] Excalidraw-Diagramm `docs/assets/vps-team-runbook.excalidraw` (+ `.en` + beide `.png`), gerendert + visuell validiert
- [ ] Anhang-Index A–X → A–Y in HANDBUCH-Übersicht, README, CONVENTIONS (DE+EN)
- [ ] `docs/runbooks/vps-team-setup.md` → Pointer auf Anhang Y (kein duplizierter Inhalt)
- [ ] Querverweise §8d / Anhang P / Anhang U → Y (DE+EN)
- [ ] Release Note
- [ ] `git diff --check` clean; keine veralteten „A–X"-Treffer mehr

## Dependencies

- **Baut auf PR #16** (`docs/runbooks/vps-team-setup.md`) — der Anhang-Inhalt ist dort bereits belegt und synthetisiert.
- **Inhaltlich verknüpft mit** §8d (Coding-Umgebungen) und den Anhängen **P** (Deployment-Szenarien), **Q** (Souveränität), **R** (Multi-Operator), **S** (Skill-Installation), **T** (Verifikation), **U** (Multi-Projekt), **V** (Bodyguard) — Anhang Y bündelt diese zum VPS-Team-Lebenszyklus und verweist auf sie.
- **Index-Konsistenz** knüpft an die Vier-Layer-Doku-Sync (PR #14, A–U → A–X) an — gleiche Stellen, jetzt → A–Y.
- Keine Blocker.

## Session-Referenz

Spec geschrieben in Session 2026-06-01 (Folge aus dem VPS-Team-Runbook PR #16). Linear: <https://linear.app/owlist/issue/BOO-94/>.

## Rollout

Additiv, reine Doku/Diagramm. Kein Verhaltens-Change, keine Migration nötig. Nach Merge ist Anhang Y die kanonische Quelle; das standalone Runbook bleibt als Pointer bestehen (oder wird beim Implement entfernt). Bestands-Projekte sind nicht betroffen.
