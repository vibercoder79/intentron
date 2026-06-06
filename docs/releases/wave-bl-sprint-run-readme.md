# Wave BL — /sprint-run README-Überarbeitung (BOO-166)

**Was jetzt da ist:** Die `sprint-run/README` erklärt den Skill jetzt ausführlich, **bettet die Owlist-Sketches direkt im Text ein** (statt nur aufzulisten), verlinkt **DE↔EN** gegenseitig, hat **Klartext-Voraussetzungen** und eine **realistische Installation** (Bootstrap/Update statt nacktem `cp -r`). README ↔ HANDBUCH Anhang AD ↔ Runbook zeigen gegenseitig aufeinander. Reine Doku — `sprint-run` bleibt **v1.1.0**. DE+EN.

## Stories
- **BOO-166** — README-Overhaul + Sketch-Einbettung + Cross-Linking.

## Änderungen (DE+EN)
- **`sprint-run/README.md` / `.en.md`**: neue Struktur (Was macht /sprint-run · So läuft ein Sprint · Eine Story im Detail · Sicherheit drei Ebenen · Voraussetzungen · Installation · Konfiguration · Verwandtes); `overview` + `sprint-run-flow` + `story-breakdown` + `gate-block-handling` **inline eingebettet**; DE↔EN-Sprachschalter im Kopf; Voraussetzungen in Klartext; realistische Installation (Normalfall `/bootstrap`/Update, Einzel-Skill via sparse-checkout).
- **HANDBUCH Anhang/Appendix AD (DE+EN)**: Rück-Link zur `sprint-run/README`.

## Wirkung
Wer die README öffnet, versteht ohne Vorwissen, was `/sprint-run` tut, sieht die Diagramme direkt im Text und kommt per Klick zur EN-Version, zum HANDBUCH-Tiefenkapitel und zum Runbook. Folgt der Embed-/Cross-Link-Konvention von `knowledge-onboarding`.

## Abgrenzung
Reine Doku, kein Code, keine Funktionsänderung (`sprint-run` bleibt v1.1.0, kein Versions-Bump). Wave-Buchstabe **bl** (bk = gate-assertion BOO-165). Repo-Slot BOO-166 = Linear BOO-166.

## Verweise
Spec: `specs/BOO-166.md`. Branch: `feat/boo-166-readme-overhaul`. Vorbild: `knowledge-onboarding` (Embed-Konvention). Verwandt: BOO-157 (HANDBUCH §6 + Anhang AD), BOO-165 (Gate-Assertion). Operator-Quelle: Tobias, 2026-06-06.
