# Wave AU — Stack-Feinschliff, MCP, Sonar-Warn & Branching-Standard (BOO-116/121/122/124/125)

**Was jetzt da ist:** die Stack-Frage führt bei „Anderes" nicht mehr still auf ESLint, der Bootstrap fragt bei Frontend/Full-Stack nach projekt-spezifischen MCPs, warnt vor dem SonarCloud-Merge-Gate, garantiert die Bundle-Skill-Source (intentron) maschinell und benennt einen positionierten Branching-Standard. Zweites Bündel der Probelauf-Folge-Stories (BKO, 2026-06-02).

## Stories
- **BOO-116** — Stack `e) Anderes` → Freitext-Rückfrage „welche Technologie?" + Linter-Hinweis (Go/Rust/Java/PHP/Ruby) statt stillem ESLint.
- **BOO-125** — Block-D-Schritt **D.7**: projekt-spezifische MCP-Abfrage (Vercel/Apify/custom) bei Frontend/Full-Stack + Vercel-Deploy-Klarstellung + Frontend-Combo.
- **BOO-121** — **Source-Garantie**: alle Bundle-Skills (inkl. `intent`) aus intentron; Regression-Check `check-skill-sources.sh` + CI `skill-sources.yml`; skills-setup-Doku korrigiert; Re-Pull-Hinweis.
- **BOO-122** — Warnhinweis bei D.5=ja: SonarCloud wird Required-Check (erster PR blockiert ohne Setup) + Entfernungs-Weg + Optional-Abfrage.
- **BOO-124** — **Branching-Standard** benannt (Trunk-Based + geschützte `main` + PR + Required Checks) + Verkaufs-Einzeiler + DE/EN-Sketch + ADR; Options-Tabelle als „Alternativen" re-gerahmt.

## Änderungen (DE+EN)
- **`bootstrap/SKILL.md`:** A.1 e)-Freitext+Linter-Hinweis (BOO-116); D.7 MCP-Abfrage (BOO-125); D.5 Sonar-Warn-Callout (BOO-122); Phase-5 Re-Pull-Hinweis (BOO-121).
- **`HANDBUCH.md` Anhang R:** benannter Branching-Default + Verkaufs-Einzeiler + Sketch-Embed + ADR-Verweis; Options-Tabelle = „Alternativen" (BOO-124).
- **`references/skills-setup.md`:** §Repo-Struktur auf flache intentron-Struktur + Source-Garantie korrigiert (BOO-121).
- **Neu:** `bootstrap/scripts/check-skill-sources.sh`, `.github/workflows/skill-sources.yml` (BOO-121); `docs/domain/adrs/branching-standard.md` (+ `.en`); `docs/assets/boo-124-branching-standard.{excalidraw,png}` (+ `.en`).

## Leichtgewicht-Prinzip
BOO-116 grenzt sauber zu BOO-127/A.1a ab (Tech-Freitext vs. unsicher→Vorschlag). BOO-124 dupliziert die Options-Tabelle nicht, sondern rahmt sie als Alternativen. BOO-121-Check ist dependency-frei (bash+git).

## Verweise
Specs: `specs/BOO-116.md`, `BOO-121.md`, `BOO-122.md`, `BOO-124.md`, `BOO-125.md`. Branch: `feat/boo-stack-mcp-branching` (auf der Bündel-1-Spitze).
