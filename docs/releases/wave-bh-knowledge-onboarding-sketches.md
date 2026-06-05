# Wave BH — Knowledge-Onboarding: Erklär-Sketches (v1.1.0)

**Was jetzt da ist:** der Bundle-Skill `knowledge-onboarding` (eingeführt in Wave AX / BOO-137) bekommt **5 erklärende Excalidraw-Sketches** im OWLIST-Design, je **DE + EN**, die einzelne Kern-Konzepte grafisch erklären — zusätzlich zum bestehenden Gesamt-Overview. Eingebettet in README und SKILL (DE+EN) an den passenden Stellen. Skill-Version `1.0.0 → 1.1.0`. EN: [`wave-bh-knowledge-onboarding-sketches.en.md`](wave-bh-knowledge-onboarding-sketches.en.md).

## Änderungen

- **5 Sketches** in `knowledge-onboarding/references/sketches/`, je `.excalidraw` + `.png` (DE) und `.en`-Variante (EN) — 20 Dateien, OWLIST-Farben, Render-Loop-validiert:
  1. `01-problem-loesung` — Problem → Lösung: deterministisch statt LLM-Whim (Side-by-Side-Vergleich).
  2. `02-adapter-funnel` — 3 Adapter → eine normalisierte `files[]`-Liste (Convergence/Funnel).
  3. `03-tier-wasserfall` — Klassifikations-Kaskade Tier 0/1/2/3 (Decision-Wasserfall, Hero-Sketch).
  4. `04-manifest-determinismus` — Re-Scan liest das Manifest zuerst: re-read statt re-infer.
  5. `05-anti-fabrikation` — vorschlagen statt blind übernehmen + Coverage-Check (Operator-Gate).
- **Eingebettet:** `README.md`/`README.en.md` (neue Sektion „Sketches — visuell erklärt") und `SKILL.md`/`SKILL.en.md` (je Sketch am passenden Workflow-Schritt: Intro · Schritt 1 · Schritt 4 · Re-Scan · Anti-Fabrikation).
- **Version:** `knowledge-onboarding/SKILL.md`+`.en.md` auf `version: 1.1.0`; README `**Version:** 1.1.0`-Zeile ergänzt (Geschwister-Konsistenz + docs-drift-Versionsgleichstand).
- **HANDBUCH (DE+EN):** Anhang AC um Sketch-Hinweis ergänzt.
- **SecondBrain:** Skill-Doku `03 Bereiche/Skills/knowledge-onboarding.md`+`.en.md` neu angelegt.

## Migration

Keine. Reine Doku-/Asset-Ergänzung — keine Verhaltensänderung am Skill-Workflow, keine neuen Abhängigkeiten.

## Verweise

Skill: `knowledge-onboarding/`. Ursprungs-Wave: [`wave-ax-knowledge-onboarding.md`](wave-ax-knowledge-onboarding.md) (BOO-137). Sketch-Quelle: `knowledge-onboarding/references/sketches/`. Render-Pipeline: `~/.claude/skills/excalidraw-diagram/references/render_excalidraw.py`.
