# Wave BP — Claude-Code-Modus-Empfehlung auf alle Skills + grafana/security-architect-Lücken (BOO-169)

> 🌐 **Sprache:** Deutsch (diese Datei) · [🇬🇧 English](wave-bp-claude-mode-all-skills.en.md)

**Was jetzt da ist:** BOO-168 hat die Claude-Code-Modus-Empfehlung für `/implement` und `/sprint-run` etabliert. Diese Wave rollt das **gleiche Muster** auf die **13 übrigen Skills** aus — jede README trägt jetzt am Kopf eine `> **Claude-Code-Modus:**`-Zeile (DE+EN) mit Verweis auf HANDBUCH §6. Die §6-Tabelle ordnet alle Skills ein und bekommt eine vierte Phase. Zwei beim Review gefundene Lücken sind mitgeschlossen. Reine Doku — kein Versions-Bump außer dem security-architect-Frontmatter-Fix.

## Stories
- **BOO-169** — Modus-Empfehlung auf alle Skills + grafana/security-architect-Lücken.

## Änderungen (DE+EN)
- **README-Modus-Zeile (DE+EN)** für 13 Skills: ideation, intent, pitch, knowledge-onboarding, sprint-review, backlog, architecture-review, security-architect, dpo, visualize, cloud-system-engineer, grafana, bootstrap.
- **HANDBUCH §6 (DE+EN)**: Beispiel-Spalte um alle Skills erweitert + neue vierte Zeile „Externe/irreversible Writes → `default` (Ask before edits)" (für `/grafana` + `/cloud-system-engineer` Modus C) + Hinweis, dass die Tabelle die zentrale Quelle ist.
- **security-architect (DE+EN)**: `recommended_model: opus` + `version: 1.1.0` ins Frontmatter ergänzt (Frontmatter war unvollständig); security-architect zusätzlich in `bootstrap/references/model-tiers.json` opus.default_for_skills.
- **grafana SKILL (DE+EN)**: Operator-Confirm-Blockquote vor `update_dashboard(overwrite=true)` (remote-Overwrite ohne lokalen Rollback).

## Modus-Zuordnung (Kurzfassung)
- **Denk-Skills → `plan`**: ideation, intent, backlog, architecture-review, security-architect, dpo.
- **Umsetzen beaufsichtigt → `acceptEdits`**: pitch, knowledge-onboarding, sprint-review, visualize, bootstrap (+ implement, sprint-run aus BOO-168).
- **Unbeaufsichtigt → `dontAsk` + Allowlist**: sprint-review + dpo-AUDIT (vom Daemon getriggert).
- **Externe irreversible Writes → `default`**: grafana, cloud-system-engineer Modus C (nie unbeaufsichtigt).

## Wirkung
Jeder Skill sagt dem Operator beim Aufruf, in welchem Claude-Code-Modus er ihn am besten fährt — interaktiv und (wo zutreffend) unbeaufsichtigt. Zwei Frontmatter-/Gate-Lücken geschlossen.

## Abgrenzung
Reine Doku, kein Code. Versions-Bump nur security-architect-Frontmatter (recommended_model + version, README bleibt 1.1.0 → docs-drift grün). Modus-Vokabular konsistent mit BOO-168 (`plan`/`acceptEdits`/`dontAsk`/`bypassPermissions`/`default`). Wave-Buchstabe **bp** (bo = Runbooks-Vernetzung BOO-167; bn = Claude-Mode-Docs BOO-168).

## Verweise
Spec: `specs/BOO-169.md`. Branch: `feat/boo-169-claude-code-modus-alle-skills`. Verwandt: BOO-168 (Modus-Fundament), BOO-84 (Model-Tier-Routing). Operator-Quelle: Tobias, 2026-06-06.
