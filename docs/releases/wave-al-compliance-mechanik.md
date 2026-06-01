# Wave AL — EU-AI-Act-Lebenszyklus + Compliance-Mechanik-Doku (BOO-106)

**Problem vorher:** EU AI Act war nur in Bootstrap (Phase 4.4n-bis) + periodischem Audit (sprint-review 7c) verdrahtet — **nicht** in `/ideation`/`/implement` wie Privacy. Und es fehlte ein Dokument, das die Compliance-Mechanik als Ganzes erklaert (Gates vs. Kataloge, automatisch vs. REVIEW-NEEDED), sodass ein CISO/Operator sie nachvollziehen kann.

**Was jetzt da ist:**

- **`docs/compliance/compliance-mechanik.md` (+ `.en.md`)** — end-to-end: zwei Mechanismen (Gates = per-Code-Hartstopp im /implement; Kataloge = periodischer Doku-Audit im /sprint-review), Touchpoint-Tabelle, beide Lebenszyklen (Privacy + EU AI Act), Klarstellungen.
- **`/ideation` Schritt 0e-bis** (DE+EN): EU-AI-Act-Pre-Flight (`ai_act_relevant`), weich, add-on-gated.
- **`/implement` Schritt 5.5c** (DE+EN): weicher Hinweis, AI_SYSTEM.md aktuell halten — KEIN harter Stopp (der AI Act ist Governance/Doku, kein Linter-Thema).

**Effekt:** EU AI Act ist jetzt wie Privacy ueber den ganzen Lebenszyklus sichtbar (Planung → Code → periodischer Audit), und die Mechanik ist in einem CISO-tauglichen Dokument erklaert. Verbindliche Pruefung bleibt der Katalog-Audit (7c) + REVIEW-NEEDED.

Spec: `specs/BOO-106.md`. Release: v0.7.3.
