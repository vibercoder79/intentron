# Wave BL — Governance-Framing nachgeschärft: INTENTRON ≠ autonome agentische KI (BOO-164)

**Was jetzt da ist:** Die kanonische Abgrenzung „INTENTRON ist eine sequenzielle Engineering-Pipeline mit Quality-Gates, **kein** vollautonomer Developer-Agent" steht jetzt auch an den **drei meistgelesenen Einstiegspunkten** (README-Intro, HANDBUCH-Einleitung, bootstrap-Einstieg) statt nur in den Tiefen-Kapiteln. Reine Doku, kein Runtime-Code. DE+EN.

## Stories
- **BOO-164** — Klarstellungs-Absätze an den Einstiegen + Entschärfung agentisch klingender Signale.

## Änderungen (DE+EN)
- **`README.md`**: Klarstellungs-Absatz „Was INTENTRON nicht ist / What INTENTRON is not" in EN- und DE-Intro; Vergleichstabelle „Multi-Agent-Orchestrierung" mit Fußnote (delegierte Sub-Skills innerhalb einer kontrollierten Story, keine autonomen Agenten); „autonomous (human) team" präzisiert.
- **`HANDBUCH.md` (+EN)**: Einleitungs-Tabellenzeile „Self-Healing Agent überwacht 24/7" → „automatisierte Self-Healing-Prüfung (optional, Cron — Block D)"; Abgrenzungs-Absatz „Was INTENTRON NICHT ist" in §1 vorgezogen (Verweis auf §8e).
- **`CONVENTIONS.md`**: §0-Klarstellung „Kein autonomer Agent / Not an autonomous agent" (DE- und EN-Block) — für Codex-/Cursor-Migranten, die agentisches Verhalten erwarten.
- **`bootstrap/SKILL.md` (+EN)**: Einstiegs-Hinweis „sequenzieller, kontrollierter Flow, kein autonom laufendes Agentensystem" (kein Version-Bump — Leichtgewicht).

## Wirkung
Ein flüchtiger Leser (CISO, Entscheider, Tool-Migrant) erkennt schon im ersten Bildschirm: Das Framework ist **menschlich gesteuerte Governance für einen sequenziellen Entwicklungsflow** mit Gates und Review-Punkten — die KI-Tools (Claude, Codex, Cursor) sind Adapter auf den Vertrag, nicht die Governance selbst. Das Missverständnis „das ist agentische KI, die selbstständig losläuft" wird an der Quelle entschärft.

## Abgrenzung
Kein Runtime-Code, kein Gate/Hook geändert. Kanonischer Satz wörtlich wiederverwendet, keine neue Terminologie. Keine Umbenennung von `execution_mode: agentic` oder der Execution-Isolation-Mechanik. Schrader-Begriff „Agentic Engineering" (Produktionsreife, nicht Autonomie) bleibt. Tiefen-Kapitel (HANDBUCH §8e, CONVENTIONS Execution-Isolation Z. 372/819) sind Quelle, nicht Ziel. Wave-Buchstabe **bl** (bk = gate-assertion BOO-165, bj = role-runbooks BOO-158).

## Verweise
Spec: `specs/BOO-164.md`. Branch: `tobiaschschmidt/boo-164-governance-vs-agentic-framing`. Berührt: `README.md`, `HANDBUCH.md` (+EN), `CONVENTIONS.md`, `bootstrap/SKILL.md` (+EN). Verwandt: HANDBUCH §8e, CONVENTIONS §0. Operator-Quelle: Tobias, 2026-06-06.
