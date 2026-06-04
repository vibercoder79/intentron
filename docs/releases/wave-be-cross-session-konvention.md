# Wave BE — Konvention gegen Cross-Session-Drift in ideation/implement (BOO-154)

**Was jetzt da ist:** Die Lektion aus dem intentron-internen Drift (BOO-153) ist jetzt als **Konvention im ausgelieferten Framework** verankert — `ideation` und `implement` weisen explizit darauf hin, wie man Nummern-/ID-Kollisionen bei parallelen Sessions/Entwicklern vermeidet. DE+EN.

## Stories
- **BOO-154** — ideation Schritt 6 (Backlog-first-ID-Konvention) + implement Schritt 0c (Cross-Session-/Isolations-Hinweis) + Verweis auf das Drei-Ebenen-Kollisionsschutz-Modell.

## Änderungen (DE+EN)
- **`ideation/SKILL.md`** (2.7.0 → **2.8.0**, README mitgezogen): Schritt 6 — Story-Nummer **vom Backlog-Tool** holen, dann `specs/<PREFIX>XXX.md` mit genau dieser Nummer benennen; nie manuell/parallel vergeben.
- **`implement/SKILL.md`** (2.12.0 → **2.13.0**, README mitgezogen): Schritt 0c — Pre-Flight isoliert Agenten EINER Story (Ebene 3); mehrere Menschen/Sessions → eigener Klon / `git worktree` (Ebene 1/2).
- Beide verweisen auf `docs/kollisionsschutz-drei-ebenen.md`.

## Wirkung
Das, was intentron-intern den Drift auslöste (manuelle Parallel-Vergabe von IDs), wird in Kundenprojekten jetzt **explizit adressiert** — die zentrale Backlog-Vergabe + Isolation steht als Konvention direkt in den Skills, nicht nur implizit im Tooling.

## Abgrenzung
Reine Skill-Doku/Konvention — kein Runtime-Code, kein Guard-Mechanismus im Kundenprojekt (der Wave-Guard bleibt intentron-intern, BOO-153).

## Verweise
Spec: `specs/BOO-154.md`. Branch: `feat/boo-154-cross-session-konvention`. Anknüpfung: BOO-151 (Drei-Ebenen-Kollisionsschutz), BOO-153 (ADR cross-session-drift). Operator-Quelle: Tobias, 2026-06-04.
