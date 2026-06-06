<a name="deutsch"></a>

# Pitch — Evidenz fuer Stakeholder-Termine sammeln

> Schliesst Schraders 4P-Pipeline (Perceive / Prompt / Produce / Pitch). Der Skill sammelt Metriken, Architektur-Diff und Intent-Erfuellung als Markdown-Briefing fuer Stakeholder-Termine. Keine Slides, kein Outcome-Text, kein Demo-Video — die Buehne bleibt menschlich.

**Version:** 1.1.0 · **Befehl:** `/pitch`

> **Claude-Code-Modus:** `/pitch` sammelt Evidenz und schreibt ein Briefing-File → beaufsichtigt **`acceptEdits`**. Kein unbeaufsichtigter Betrieb (du reviewst das Briefing vor dem Termin). Details: HANDBUCH §6 „Claude-Code-Modus".

---

## Was der Skill tut

Schraders Pitch-Prinzip aus *Code Crash* Kapitel 5 ist Evidenz statt Live-Coding. Dieser Skill ist die Hybrid-Variante (Option 3 aus drei Varianten, entschieden am 2026-04-28): er sammelt die Daten, der Mensch baut daraus die Story und macht die Live-Demo. Output ist ein einzelnes Markdown-Briefing unter `pitch/PITCH-XX.md` — committed, NICHT gitignored, weil Pitch-Briefings Teil der Projekt-Geschichte sind.

Der Skill ist read-only gegenueber dem Learning-Loop und schreibt NIE in L3 (`journal/learnings.db`) — das ist die saubere Trennung zu `/sprint-review`, das den Lern-Loop besitzt. `/pitch` laeuft nach `/sprint-review` und vor dem Stakeholder-Termin.

---

## Wie er funktioniert

```
Schritt 0: Environment laden
   · .claude/environment.json (BOO-34) lesen
   · paths.pitches, paths.reports_local, paths.reports_ci,
     paths.lessons_l3, paths.intents, paths.feature_flags
   · Fallback auf Defaults bei fehlender Datei

Schritt 1: Pitch-Scope abfragen
   · Welcher Sprint? Welche Intents? Welche Stories?
   · Optional: Stakeholder-Kontext (1 Satz)
   · PITCH-XX-Nummer = hoechste vorhandene + 1

Schritt 2: Daten aus 8 Quellen sammeln (graceful skip)
   · L3 Lessons-DB (read-only) · Local Reports · CI Reports
   · Sprint-Files · Architektur-Doku · Intents
   · Feature-Flags · Git-Log

Schritt 3: Architektur-Diff berechnen
   · git diff vom letzten PITCH-Datum bis HEAD
     auf ARCHITECTURE_DESIGN.md
   · Erst-Pitch: kompletten Stand zusammenfassen

Schritt 4: Demo-Pfad-Heuristik anwenden
   · Score = Aenderungs-Delta + Intent-Relevanz
   · User-Journey-Vorschlag (z.B. Onboarding → Search → Checkout)
   · Intent-Erfuellung pro related_intent: Score 0–1 oder null

Schritt 5: pitch/PITCH-XX.md schreiben
   · Frontmatter + 5 Body-Sektionen
   · status: prepared
   · Operator zum Review aufgefordert

Schritt 6 (post-pitch, optional):
   · status: delivered
   · Freitext-Outcome-Notiz vom Operator
   · Kein Auto-Outcome — User-Reaktion ist menschliche Arbeit
```

---

## Trigger-Phrasen

- `/pitch`
- "Pitch vorbereiten"
- "Sprint X praesentieren"
- "Stakeholder-Termin vorbereiten"
- "/pitch post" (Post-Pitch-Modus fuer Schritt 6)

---

## Schnittstellen zu anderen Skills

| Upstream | Was geliefert wird | Downstream | Was wir liefern |
|----------|--------------------|------------|------------------|
| `/sprint-review` | Sprint-Aggregat-Metriken (Coverage, Iterations, Findings) | Operator (Mensch) | Pitch-Briefing als Spickzettel fuer die Live-Demo |
| `/architecture-review` | `ARCHITECTURE_DESIGN.md` aktueller Stand | — | — |
| `/intent` | `intents/INTENT-XX.md` mit Erfolgskriterien | — | — |
| `/implement` (indirekt) | Local-Reports + Iterations-Counts | — | — |

`/pitch` ist read-only gegenueber allen Upstream-Quellen und schreibt ausschliesslich in `pitch/PITCH-XX.md`. Keine Linear-Schreibaktionen, kein L3-Update.

---

## Artefakte / Outputs

- **`pitch/PITCH-XX.md`** — eine Datei pro Pitch-Event, committed (NICHT gitignored)
  - Frontmatter: `pitch_id`, `sprint`, `created_at` (ISO-8601 UTC), `related_intents`, `related_stories`, `metrics_snapshot.*`, `demo_path`, `status: prepared`
  - Body-Sektionen:
    1. Architektur-Diff seit letztem Pitch
    2. Quality-Gate-Status (Findings, Hotspots, Coverage)
    3. Intent-Erfuellung (pro `related_intent`: Kriterium + Stand + Score 0–1)
    4. Demo-Pfad-Vorschlag (User-Journey)
    5. Open Questions (was Stakeholder fragen koennten)
  - Optional nach dem Termin: `## Outcome (post-pitch)` Freitext-Sektion + `status: delivered`

---

## Hintergrund / Motivation

Schrader argumentiert in *Code Crash* Kapitel 5: Die 4P-Pipeline (Perceive / Prompt / Produce / Pitch) ist nur dann geschlossen, wenn der Stakeholder-Termin ein echter Pitch ist — Evidenz, nicht Live-Coding. Im INTENTRON Framework decken `/intent` (Perceive), `/ideation` + `/backlog` + `/implement` (Prompt + Produce) die ersten drei P ab. Das vierte P fehlte — bis BOO-37.

Am 2026-04-28 wurden drei Varianten diskutiert: (1) Vollautomatischer Slide-Generator, (2) KI-formuliertes Pitch-Skript, (3) Hybrid mit reiner Evidenz-Sammlung. Variante 2 wurde wegen KI-Slop-Risiko verworfen — formulierter Pitch-Text klingt generisch und untergraebt Vertrauen. Variante 3 (diese Implementierung) trennt sauber: Maschine sammelt Fakten, Mensch baut Story.

---

## Quellen

- **Buch:** Matthias Schrader, *Code Crash* (2025), Kapitel 5 §Pitch
- **Linear:** BOO-37 — Pitch-Skill (Bootstrapping Evolution)
- **ADR:** Entscheidung Hybrid-Variante (Option 3) am 2026-04-28

---

## Dateistruktur

```
intentron/pitch/
├── SKILL.md                           ← Skill-Definition (DE — primaer)
├── SKILL.en.md                        ← Skill-Definition (EN)
├── README.md                          ← Diese Datei (DE)
├── README.en.md                       ← Englisches README
├── references/
│   ├── pitch-template.md              ← Body-Schema fuer PITCH-XX.md (DE)
│   ├── pitch-template.en.md           ← Englische Spiegelung
│   ├── demo-path-heuristic.md         ← Scoring-Logik Demo-Pfad (DE)
│   └── demo-path-heuristic.en.md      ← Englische Spiegelung
├── pitch-overview.excalidraw          ← Uebersichts-Diagramm (DE)
├── pitch-overview.png                 ← Gerenderte PNG (DE)
├── pitch-overview.en.excalidraw       ← Uebersichts-Diagramm (EN)
└── pitch-overview.en.png              ← Gerenderte PNG (EN)
```

![Pitch-Skill Overview](pitch-overview.png)
