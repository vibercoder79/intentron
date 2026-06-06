# Wave BQ — Model-/Modus-Routing im sprint-run-Daemon + implement auf Opus (BOO-170)

**Was jetzt da ist:** Die Modell-/Modus-Empfehlung wird im **`/sprint-run --auto`-Daemon erzwungen** (vorher reine Doku). Pro Story löst ein neues, getestetes Helper-Skript das empfohlene Modell auf und startet `/implement` als Subprozess mit `--model` + `--permission-mode dontAsk`. Dazu eine Policy-Korrektur: **Produktcode läuft jetzt auf Opus** (bestes Modell für den Code-Kern). Interaktiv bleibt es bewusst Empfehlung.

## Stories
- **BOO-170** — Daemon-Model-Routing + Spike + implement-Opus-Policy.

## Änderungen
- **Neu: `sprint-run/scripts/resolve-model.py`** (dependency-frei, getestet) — löst `<skill>/SKILL.md recommended_model` (Tier) → `model-tiers.json current_version` (Version) auf. Fallback `sonnet`.
- **sprint-run Schritt 4.3 (DE+EN):** `/implement` als Subprozess mit aufgelöstem `--model` + `--permission-mode dontAsk` + Abschnitt „Modell-/Modus-Routing (BOO-170)" (Override-Hierarchie, Multi-Tier-Grenze, Daemon-vs-interaktiv).
- **Policy implement → opus (DE+EN):** `recommended_model: sonnet → opus`; `model-tiers.json` opus erweitert. Code-Kern (Schritt 5) + Security-Findings (6e) opus, mechanische Iterations-Loops (6a) bleiben haiku.
- **HANDBUCH (DE+EN):** Enforcement-Absatz im Model-Routing-Anhang + opus-Routing-Zeile erweitert.
- **Versions-Bumps:** implement 2.13.0 → 2.14.0, sprint-run 1.1.0 → 1.2.0.

## Spike (verifiziert)
`claude --help`: `--model` + `--permission-mode` (choices acceptEdits/auto/bypassPermissions/default/dontAsk/plan) existieren; kein `--effort`. sprint-run ist prompt-getrieben (kein Daemon-Programm) → Variante A (Helper + Subprozess-Spec) statt vollausführbarem Daemon.

## Wirkung
Im unbeaufsichtigten Sprint läuft jede Story automatisch auf dem empfohlenen Modell und im unbeaufsichtigten Modus — mit gewahrter Operator-Override-Hierarchie. Produktcode auf Opus = beste Qualität für den Wertschöpfungskern; Loops auf Haiku = kein verschwendetes Geld.

## Abgrenzung
Variante A (leichtgewichtig). **Offen (Folge-Story):** implement-internes Subagent-Modell-Routing (haiku-Loops/opus-Security innerhalb eines Laufs) + vollausführbarer VPS-Daemon. Effort bleibt nicht erzwingbar (kein CLI-Flag). Wave-Buchstabe **bq** (bp = Claude-Mode-all-skills BOO-169).

## Verweise
Spec: `specs/BOO-170.md`. Branch: `feat/boo-170-daemon-model-routing`. Verwandt: BOO-169 (Modus-Doku), BOO-168 (Modus-Fundament), BOO-84 (Tier-Routing), BOO-157 (sprint-run). Operator-Quelle: Tobias, 2026-06-06.
