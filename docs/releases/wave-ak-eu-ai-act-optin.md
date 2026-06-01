# Wave AK — EU AI Act echtes konditionales Opt-in (BOO-105)

**Problem vorher (aus BOO-101):** „Strikt opt-in" stimmte am Runner-Ende nicht. `dpo-audit.py` laedt per `glob` alle `dpo/controls/*.yml` — der EU-AI-Act-Katalog lief also bei jedem dpo-Audit mit, auch in Privacy-Projekten ohne KI-Anteil (`AI_SYSTEM.md fehlt`-GAP = Rauschen). Ausserdem gab es nur eine A.4-Notiz, keine ausfuehrbare Bootstrap-Phase.

**Was jetzt da ist:**

- **Katalog raus aus dem Auto-Load:** `dpo/controls/eu-ai-act.yml` → `dpo/controls/optional/eu-ai-act.yml`. Der nicht-rekursive Framework-Glob laedt Unterordner nicht; der rekursive Overlay-Glob laedt ihn, sobald er ins Projekt kopiert ist.
- **Ausfuehrbare Bootstrap-Phase 4.4n-bis** (nur bei `[x] EU AI Act`, setzt Privacy voraus): kopiert den Katalog ins Projekt-Overlay `.claude/dpo/controls/`, rendert `AI_SYSTEM.md`, ergaenzt den `ARCHITECTURE_DESIGN.md`-Verweis, optional Backlog-Label `ai-act`. DE+EN.
- **Doku angeglichen:** A.4-Notiz, dpo/SKILL.md(.en) Katalog-Tabelle + Runner-Liste, README-Pfad, Katalog-Header.

**Effekt:** EU-AI-Act-Pruefung laeuft garantiert **nur** in Projekten, die das Add-on gewaehlt haben — kein Rauschen in Nicht-KI-Projekten. Der Pfad ist end-to-end deterministisch (Frage → Phase → Katalog im Overlay → dpo-AUDIT → REVIEW-NEEDED).

Spec: `specs/BOO-105.md`. Release: v0.7.2.
