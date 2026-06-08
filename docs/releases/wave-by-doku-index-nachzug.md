# Wave BY — Doku-Index-Nachzug: fehlende Runbooks im zentralen Index (BOO-181)

> 🌐 **Sprache:** Deutsch (diese Datei) · [🇬🇧 English](wave-by-doku-index-nachzug.en.md)

**Was jetzt da ist:** Zwei Runbooks, die aus dem HANDBUCH verlinkt waren, aber im zentralen Dokumenten-Index `docs/INDEX.md` fehlten, sind nachgetragen — `unit-tests.md` (BOO-177) und `sprint-unattended-tmux.md` (BOO-172). Beide entstanden vor der 3-Index-Pflicht aus BOO-180 (Doku-DoD) und sind ihr durchgerutscht. Retroaktive Compliance, beim Navigierbarkeits-Check nach dem Sprint „Quality-Gate-Integrität" gefunden.

## Änderungen

- **`docs/INDEX.md` + `.en.md`:** je zwei Zeilen in der Dokumentations-Tabelle (alphabetisch zwischen „Sprint-Run" und „Vercel") — `sprint-unattended-tmux.md` und `unit-tests.md`, beide DE+EN.
- **Artefakt-Landkarte geprüft:** `docs/onboarding/artefakt-landkarte.md` listet Runbooks nicht generell (nur `audit-perspective` als Audit-Artefakt) → kein Nachtrag nötig.

## Abgrenzung

- Reine Doku/Index-Hygiene, kein Code. Folge-Compliance zu BOO-177/BOO-172 unter der Doku-DoD-Konvention (BOO-180) — dogfoodt die neue Regel.
- Wave-Buchstabe **by** (bx = PR-Hygiene BOO-175).

## Verweise

Spec: `specs/BOO-181.md`. Branch: `tobiaschschmidt/boo-181-docs-doku-index-nachzug`. Verwandt: BOO-180 (Doku-DoD), BOO-177 (unit-tests-Runbook), BOO-172 (tmux-Runbook). Operator-Quelle: Tobias, 2026-06-08 (Navigierbarkeits-Frage nach Sprint-Abschluss).
