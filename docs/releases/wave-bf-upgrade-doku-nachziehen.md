# Wave BF — Upgrade-Doku nachziehen: irreführendes `/bootstrap --update` raus (BOO-155)

**Was jetzt da ist:** Die Einstiegs-Doku zum Framework-Upgrade ist wieder deckungsgleich mit dem realen Mechanismus. Der irreführende Befehl `/bootstrap --update` (ein Flag, das es nie gab) ist raus; `framework-upgrade.md` nennt jetzt die neuen Pflicht-Artefakte und den `migrate-to-v2.sh`-Pfad. Reine Doku, kein Runtime-Code. DE+EN.

## Stories
- **BOO-155** — HANDBUCH-FAQ korrigiert (`/bootstrap` statt `/bootstrap --update`) + `framework-upgrade.md` um Artefakt-/migrate-/provider-Verweise ergänzt.

## Änderungen (DE+EN)
- **`HANDBUCH.md` / `.en.md`** (FAQ „Wie aktualisiere ich die Skills"): `/bootstrap --update` → `/bootstrap`; Kommentar erklärt die Auto-Erkennung der bestehenden Installation + Modus-Abfrage (inspect / apply-safe / apply-with-confirmation), Verweis auf `framework-upgrade.md`.
- **`bootstrap/references/framework-upgrade.md` / `.en.md`**:
  - „Dateikategorien"-Tabelle um `CONTEXT.md`, `solution-artefakte.md`, `DEVELOPER_ONBOARDING.md`, `.claude/environment.json` (+ Generator) und `docs/kollisionsschutz-drei-ebenen.md` ergänzt.
  - Nutzerfluss verankert `bash bootstrap/scripts/migrate-to-v2.sh --issue BOO-NN` als idempotenten Bestands-Migrationspfad.
  - Provider-Postflight-Schritt verlinkt `bootstrap/references/provider-postflight.md`.

## Wirkung
Wer ein bestehendes Projekt auf den aktuellen Framework-Stand zieht, folgt jetzt einer Anleitung, die zum tatsächlichen Skill-Verhalten passt: `/bootstrap` im Projekt → Auto-Erkennung → Modus-Abfrage. Keine toten Befehle, keine fehlenden Artefakte.

## Abgrenzung
Kein echtes `--update`-Flag gebaut (streichen statt bauen — §7.5a deckt es ab). `bootstrap/README.md`-Versions-Header („Version 3.0") bewusst unangetastet (Major-Label, gate-irrelevant). Kein Migrations-Skript-Code geändert.

## Verweise
Spec: `specs/BOO-155.md`. Branch: `tobiaschschmidt/boo-155-docs-upgrade-doku-nachziehen-irrefuhrendes-bootstrap-update`. Anknüpfung: BOO-60 (Upgrade-Modus §7.5a), BOO-91/108/138/139 (die nachgezogenen Artefakte). Operator-Quelle: Tobias, 2026-06-04.
