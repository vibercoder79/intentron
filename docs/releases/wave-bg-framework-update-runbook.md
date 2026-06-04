# Wave BG — Runbook „Framework-Update" für Bestandsprojekte (BOO-156)

**Was jetzt da ist:** Ein dedizierter Copy-Paste-Runbook bündelt das Framework-Update eines Bestandsprojekts in einem Stück — Bootstrap-Skill aktualisieren + `/bootstrap`-Upgrade (inspect → apply-safe → apply-with-confirmation). Aus dem README in EN + DE verlinkt. Reine Doku. DE+EN.

## Stories
- **BOO-156** — `docs/runbooks/framework-update.md` (+EN) neu + README-Verlinkung.

## Änderungen (DE+EN)
- **Neu `docs/runbooks/framework-update.md` / `.en.md`**: Schritt 1 (Bootstrap-Skill via sparse-checkout aktualisieren) + Schritt 2 (`/bootstrap` erkennt die bestehende Installation, Modus-Abfrage) inkl. Ein-Klick-Prompt, Sicherheit/Idempotenz, Verweisen. Struktur analog `secondbrain-nachziehen.md`.
- **`README.md`**: Runbook im EN-Abschnitt „C) AI self-update for an old / brownfield install" und im DE-Pendant verlinkt.

## Wirkung
Auf die Frage „ist der Framework-Update-Weg dokumentiert?" gibt es jetzt eine einzelne, vollständige Anleitung statt zwei zusammenzusetzender Hälften.

## Abgrenzung
Reine Doku, kein Code, kein Skill, kein Sketch. Wave-Buchstabe `bg` (bf = BOO-155). Baut auf BOO-144 (Runbook-Muster) + BOO-155 (korrigierte Upgrade-Doku).

## Verweise
Spec: `specs/BOO-156.md`. Branch: `tobiaschschmidt/boo-156-docs-runbook-framework-updatemd-bestandsprojekt-auf`. Verwandt: `docs/runbooks/secondbrain-nachziehen.md` (BOO-144). Operator-Quelle: Tobias, 2026-06-04.
