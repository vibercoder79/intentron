# Token-Boundary — 80%-Logik + Sprint-Budget

Referenz zu `/sprint-run` Schritt 2 (Budget-Planung) und Schritt 6 (Sprint-Boundary).
Grundlage: HANDBUCH Anhang G (Sprint-Sizing-Mechanik, BOO-38/39/40).

## Prinzip: Token-Box statt Zeit-Box

Ein Sprint ist **80 % des Context-Windows** des verwendeten Modells — modellunabhaengig.
Kein Burndown, keine Velocity, keine Story-Points-pro-Sprint-Statistik. Outcome wird ueber
Intent-Erfuellung gemessen, nicht ueber Token-Verbrauch.

| Schwelle | Quelle (`environment.json`) | Wirkung |
|---|---|---|
| `token_warn_threshold` | Default `70` | Soft-Warnung: Sprint neigt sich dem Ende |
| `token_hard_threshold` | Default `80` | **Hard Stop**: Sprint-Boundary → `/sprint-review` |

## Budget-Planung (Schritt 2)

1. Context-Window des Modells bestimmen (z.B. 200k).
2. Sprint-Budget = 80 % davon (z.B. 160k).
3. `token_estimate` aller Kandidaten-Stories summieren (aus dem Spec-`Execution Isolation`-Block).
4. Stories, die das Budget sprengen, in den naechsten Sprint verschieben — **Hinweis, kein
   Abbruch**. Keine Story wird heimlich gekuerzt.
5. Reihenfolge: `blockedBy` zuerst, dann Prioritaet.

## Boundary-Check (Schritt 4.8 / 6)

Nach jeder Story (und grob waehrend laufender Implementierung) den kumulierten Verbrauch gegen
`token_hard_threshold` projizieren:

- **< 80 %:** naechste Story.
- **≥ 80 %:** Loop verlassen → Schritt 6: `/sprint-review` triggern, Operator-Hinweis
  **"Sprint-Boundary erreicht"**. Verbleibende Stories bleiben im Backlog fuer den naechsten Sprint.

> Die Boundary ist **konservativ**: lieber eine Story frueher stoppen als mitten in einer Story
> ins Kontext-Limit laufen. Eine angefangene, nicht fertig getestete Story ist teurer als eine
> verschobene.

## Bezug zu Story-Points

| SP | Budget-Anteil (@200k) | Ausfuehrungsmodus |
|---|---|---|
| 1 | ~5 % | linear |
| 2 | ~10–15 % | linear / sub-agents |
| 3 | ~20–30 % | sub-agents |
| 5 | ~40–60 % | agentic |
| 8 | >60 % | **aufteilen** |

`/sprint-run` nutzt diese Schaetzung nur zur **Reihenfolge und Boundary** — die eigentliche
Modus-Wahl pro Story trifft `/implement` (Schritt 0c) anhand des Spec-Blocks.

Sketch: `docs/sprint-run-flow.png` (HANDBUCH Anhang AD).
