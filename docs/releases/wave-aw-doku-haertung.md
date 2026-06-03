# Wave AW — Doku-Härtung & Onboarding-Klarheit (BOO-130–136)

**Was jetzt da ist:** ein konsolidierter „So dokumentieren wir"-Einstieg, ein Klartext-Glossar für Nicht-Entwickler, GitHub Issues als sichtbar empfohlener Backlog-Standard, ein Linear-MCP-auf-VPS-Runbook, ein kanonischer Onboarding-Dateiname, der GitHub-Pro-Hinweis für Branch-Protection und ein SECURITY.md-Next-Step. Ergebnis der Doku-Review vom 2026-06-03. EN: [`wave-aw-doku-haertung.en.md`](wave-aw-doku-haertung.en.md).

## Stories
- **BOO-130** — `docs/how-we-document.md` (+ `.en`, + Sketch): Doku-Modell auf einer Seite (Artefakte · 3 Schichten · Gates · Bestands-Repo-Pfad); aus HANDBUCH §7 verlinkt.
- **BOO-131** — `docs/glossar.md` (+ `.en`): Klartext-Glossar (Runner, MCP, Hook, Gate, PR, Spec, ADR …) für Nicht-Entwickler; aus Anhang C verlinkt.
- **BOO-132** — A.3b markiert **GitHub Issues als empfohlenen Standard** (Mechanik unverändert).
- **BOO-133** — HANDBUCH **Anhang AB**: Linear-MCP-auf-headless-VPS-Runbook (SSH-Port-Forward-OAuth + Token-Setup ohne Leak); §3-Token-Ort korrigiert (Settings → Security and Access); §8g-Deeplink.
- **BOO-134** — Onboarding-Dateiname kanonisch **`DEVELOPER_ONBOARDING.md`** (behebt verify-setup-WARN-Mismatch in repo-docs); Regel „kein HANDBUCH.md im Projekt".
- **BOO-135** — §3 + Anhang A: **GitHub Pro/Team** nötig für Branch-Protection bei privaten Repos (public gratis).
- **BOO-136** — Phase 7.6: Next-Step „**SECURITY.md via security-architect (DESIGN) befüllen**" + Basis-Klarstellung.

## Neu / geändert (DE+EN)
- **Neu:** `docs/how-we-document.md`, `docs/glossar.md` (je + `.en`), Sketch `docs/assets/boo-130-how-we-document.{excalidraw,png}` (+ `.en`), HANDBUCH **Anhang AB**.
- **HANDBUCH:** §3 (GitHub-Pro + Linear-Token-Ort), §7 (Verweis), Anhang A (Branch-Protection-Plan), Anhang C (Glossar-Verweis), §8g (AB-Deeplink), TOC + §13-Wegweiser (28 Anhänge).
- **`bootstrap/SKILL.md`:** A.3b (GitHub-Default), Phase 7.6 (SECURITY-Next-Step).
- **`references/`:** `project-documentation-ssot.md` (kanonischer Onboarding-Name), `verify-setup.sh` (WARN präzisiert).

## Verweise
Specs: `specs/BOO-130.md` … `BOO-136.md`. Branch: `feat/boo-doku-haertung`. Design-Input RAG/Schicht-2 → SecondBrain Factory-Research (nicht im Bootstrap).
