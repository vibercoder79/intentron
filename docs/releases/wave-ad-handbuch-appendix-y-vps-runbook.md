# Wave AD — HANDBUCH-Anhang Y: VPS/Cloud-Team-Runbook (BOO-94)

> 🌐 **Sprache:** Deutsch (diese Datei) · [🇬🇧 English](wave-ad-handbuch-appendix-y-vps-runbook.en.md)

**Linear:** [BOO-94](https://linear.app/owlist/issue/BOO-94/) · Folge aus dem VPS-Team-Runbook PR #16

## Problem

Das VPS-Team-Setup-Wissen lag als standalone Runbook (`docs/runbooks/vps-team-setup.md`, DE, aus
PR #16) — wertvoll, aber **nicht Teil des kanonischen HANDBUCHs**: nicht aus dem
Inhaltsverzeichnis verlinkt, nicht zweisprachig, ohne Diagramm. Die uebrigen Deployment-/
Betriebs-Themen (Anhaenge P Deployment-Szenarien, Q Souveraenitaet, R Multi-Operator,
S Skill-Installation, T Verifikation, U Multi-Projekt, V Bodyguard) sind dagegen nummerierte,
DE+EN-paritaetische Anhaenge mit Querverweisen. Der VPS-Team-Lebenszyklus
(einmal-pro-VPS → pro-Projekt → Team) ist genau das Bindeglied zwischen §8d, P und U und gehoert
als Anhang Y in dieselbe Reihe. Zwei parallele Quellen waeren ein Drift-Risiko.

## Was sich aendert

- **Anhang Y „VPS/Cloud-Team-Runbook"** in `HANDBUCH.md` (DE) **und** `HANDBUCH.en.md` (EN), strikt
  paritaetisch, im Inhaltsverzeichnis (Anhang-Uebersicht) verlinkt. Unterabschnitte Y.1–Y.8:
  Szenario/Voraussetzungen, einmal-pro-VPS, pro-Projekt (Git-Hooks pro Repo!), Onboarding Projekt
  2..N + Brownfield (`migrate-to-v2.sh`), Team (CODEOWNERS/Branch-Protection), Entscheidungen
  (Docker vs. Direkt-Install, Git-lokal vs. GitHub, Souveraenitaet), Vier-Layer auf headless VPS,
  Schnellreferenz. Inhaltlich aus dem Runbook synthetisiert (Anhang-Form, keine 1:1-Copy).
- **Excalidraw-Uebersichtsdiagramm** `docs/assets/vps-team-runbook.excalidraw` (+ `.en.excalidraw`
  + beide `.png`, 6960×3680, Style aus `quality-gate-four-layers`): Lebenszyklus VPS-Setup →
  Projekt-Wiring → Multi-Projekt/Team, mit der einmal-pro-VPS-vs-pro-Projekt-Trennung
  („Git-Hooks pro Repo") als visuellem Kern. In beide Anhaenge eingebettet, visuell validiert
  (3 Render-Runden).
- **Anhang-Index A–X → A–Y** (DE+EN paritaetisch): HANDBUCH-Anhang-Uebersicht
  („24 Anhaenge (A–X)" → „25 … (A–Y)", Themenliste um Y ergaenzt), README („Anhaenge A–X" → „A–Y"
  inkl. Aufzaehlungs-Eintrag Y), CONVENTIONS („Anhang A-X" → „A-Y").
- **Standalone-Runbook → Pointer:** `docs/runbooks/vps-team-setup.md` auf einen Kurz-Verweis auf
  Anhang Y reduziert (kein duplizierter Volltext → kein Drift; Datei behalten, um
  PR-#16-Historie/Links nicht zu brechen — Decision 1).
- **Querverweise** §8d / Anhang P / Anhang U → Anhang Y ergaenzt (DE+EN).

## Designentscheid

- **Anhang Y wird kanonisch**, das standalone Runbook wird zum Pointer — kein Doppel-Inhalt,
  konsistent mit der Single-Source-Linie BOO-89.
- **Keine inhaltliche Neuerfindung** — nur Promotion des bereits in PR #16 belegten
  Runbook-Inhalts; alle Aussagen bleiben gegen die Anhaenge P/Q/R/S/T/U/V + §8d belegt.
- **Zweisprachig + Diagramm DE+EN** (zwei Varianten + PNGs, analog `quality-gate-four-layers`) —
  bringt den Anhang auf das Niveau von P/Q/R/S/T/U/V.
- **Index ueberall mitziehen** (HANDBUCH-Uebersicht, README, CONVENTIONS) — sonst entsteht
  derselbe Selbstwiderspruch wie vor der Vier-Layer-Doku-Sync (A–U vs. A–X).
- **Leichtgewicht:** reine Doku/Diagramm, kein Verhaltens-Change, keine neue Dependency.

## Verifiziert

- Anhang Y existiert in HANDBUCH.md UND HANDBUCH.en.md, gleiche H2/H3-Struktur, im
  Inhaltsverzeichnis verlinkt.
- `grep -rniE "A–X|A-X"` ueber README/CONVENTIONS/HANDBUCH* liefert keine veralteten Treffer mehr;
  „25 Anhaenge / 25 appendices (A–Y)" konsistent.
- Beide Diagramm-PNGs neu gerendert, visuell auf Ueberlappung/Layout geprueft.
- `docs/runbooks/vps-team-setup.md` enthaelt keinen duplizierten Volltext mehr, sondern den
  Pointer.
- Querverweise §8d/P/U → Y vorhanden (DE+EN).
- `git diff --check` clean; DE/EN-Paritaet geprueft.

## Rollout

Additiv, reine Doku/Diagramm. Kein Verhaltens-Change, keine Migration noetig. Nach Merge ist Anhang
Y die kanonische Quelle; das standalone Runbook bleibt als Pointer bestehen. Bestands-Projekte sind
nicht betroffen.

## Effekt

Das Betriebswissen fuer Team-VPS ist jetzt erstklassiger, auffindbarer, zweisprachiger
HANDBUCH-Bestandteil mit Diagramm — kein loses standalone Doc mehr.

## Verweise

- Spec: `specs/BOO-94.md`
- Release-Ueberblick: `docs/releases/v0.6.0-overview.md` (Wave AD)
- Anhang Y: `HANDBUCH.md` + `HANDBUCH.en.md`
- Diagramm: `docs/assets/vps-team-runbook.excalidraw` (+ `.en.excalidraw` + beide `.png`)
- Standalone-Pointer: `docs/runbooks/vps-team-setup.md`
- Baut auf PR #16; Index-Konsistenz knuepft an PR #14 (A–U → A–X) an
- Linear: BOO-94
