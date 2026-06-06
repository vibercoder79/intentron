# Wave BN — Claude-Code-Modus-Empfehlung + /sprint-run „Zwei Modi" (BOO-168)

**Was jetzt da ist:** Klarstellung, dass **`/sprint-run` selbst ausführt** (mit einer einmaligen Plan-Freigabe) und **`--auto` nur diese Freigabe weglässt** — beide führen den Sprint real aus, es gibt keinen „Nur-Prüfen"-Modus. Plus ein neuer **HANDBUCH-§6-Abschnitt**, welcher **Claude-Code-Berechtigungsmodus** zu welchem Skill passt, und die Abgrenzung **Skill-Plan ≠ Claude-Code-Planungsmodus** (read-only, blockiert die Umsetzung). Reine Doku — `sprint-run` bleibt v1.1.0. DE+EN.

## Stories
- **BOO-168** — Modus-Empfehlung + Zwei-Modi-Klarstellung.

## Änderungen (DE+EN)
- **HANDBUCH §6 (DE+EN)**: neuer Abschnitt „Claude-Code-Modus: welcher Berechtigungs-Modus zu welchem Skill?" — Denk-Skills → `plan`; Umsetzung beaufsichtigt → `acceptEdits`; unbeaufsichtigt (`--auto`) → `dontAsk` + Allowlist (`bypassPermissions` nur isoliert); nie Plan Mode für die Umsetzung; Abgrenzung + Sicherheitsnetz.
- **`sprint-run/README` (DE+EN)**: „Zwei Modi"-Block (Default vs `--auto`, beide führen aus) + Plan-Mode-Abgrenzung + Claude-Code-Modus-Empfehlung.
- **`sprint-run/SKILL` (DE+EN)**: Daemon-Modus-Abschnitt entschärft (Default-Loop läuft nach der Freigabe ebenso durch) + Modus-Blockquote.
- **`docs/runbooks/sprint-run` (DE+EN)**: Klarstellung „beide führen aus" + Modus-Tipp.
- **`implement/README` (DE+EN)**: Claude-Code-Modus-Zeile (gleiche `--auto`-Logik).

## Wirkung
Keine Verwechslung mehr von „`/sprint-run` prüft nur / `--auto` führt aus" und von Skill-Plan vs. Claude-Code-Planungsmodus. Nutzer wissen, welchen Claude-Code-Modus sie pro Skill-Phase wählen.

## Abgrenzung
Reine Doku, kein Code, **kein Versions-Bump**. Modus-Fakten gegen die offizielle Claude-Code-Doku verifiziert (6 Modi; Plan Mode read-only). Wave-Buchstabe **bn** (bm = sprint-run-readme BOO-166).

## Verweise
Spec: `specs/BOO-168.md`. Branch: `feat/boo-168-claude-mode-docs`. Verwandt: BOO-157 (`/sprint-run`), BOO-165 (Gate-Assertion), BOO-166 (README-Overhaul). Operator-Quelle: Tobias, 2026-06-06.
