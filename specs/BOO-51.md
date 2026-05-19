# BOO-51 — Dry-Run GAP Hardening

## Summary

Parent-Spec fuer den lokalen Commit, der die ersten Dry-Run-GAP-Hardening-Wellen aus BOO-52 bis BOO-61 im Code-Crash Framework verankert.

## Why

Der Codex-Dry-Run im Projekt `OWLIST KI Newsletter Cybersecurity` zeigte mehrere Luecken im Framework: Runtime-Mapping fuer Codex, Backlog-Tool-Abstraktion, Baseline-Artefakte, Postflight, Security-by-Design, Validate-Fix-Learn und Upgrade-Pfad fuer bestehende Projekte.

## What

- Bootstrap- und Vertragsdokumente um Runtime-, Backlog-Adapter- und Postflight-Regeln ergaenzen.
- Handbuch und Release Notes aktualisieren.
- Story-Templates um `Security Impact` und `Security Validation` erweitern.
- Implement-Skill um Security-Referenzstack und Validate-Fix-Learn-Semantik nachschaerfen.
- Architektur- und Hook-Templates mit Kontextvalidierung und Runtime-Hook-Layer ergaenzen.

## Constraints

- Keine Secrets schreiben.
- Keine bestehenden Projektanpassungen blind ueberschreiben.
- Deutsch und Englisch konsistent halten.
- Keine Excalidraw-/PNG-Dateien in diesem Commit neu erzeugen.

## Agent-Pattern

**Gewähltes Pattern:** Parallel-Subagents

**Begründung:** Bootstrap-/CONVENTIONS- und Handbuch-/Release-Notes-Aenderungen konnten getrennt bearbeitet werden. Die Integration und Verifikation erfolgte im Hauptarbeitsbaum.

**Team-Komposition:** Worker A fuer Bootstrap/CONVENTIONS; Worker B fuer Handbuch/Release Notes; Hauptagent fuer Integration, Security-/Implement-Ergaenzungen, Obsidian-Spiegel, Commit/Push.

## Validation

- `git diff --check`
- `git diff --cached --check`
- `rg`-Checks auf verbleibende harte Linear-only Pflichtformulierungen
- Obsidian-Spiegel der geaenderten Framework-Dokumentation aktualisiert
