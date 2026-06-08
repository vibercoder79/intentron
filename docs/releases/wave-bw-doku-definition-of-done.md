# Wave BW — Doku-Definition-of-Done als Konvention (BOO-180)

> 🌐 **Sprache:** Deutsch (diese Datei) · [🇬🇧 English](wave-bw-doku-definition-of-done.en.md)

**Was jetzt da ist:** Die gelebte Doku-Pflicht ist jetzt eine **explizite Konvention** statt nur Gewohnheit. Neue/geänderte Dokumente müssen vernetzt, in den drei Index-Ebenen nachgezogen, DE+EN und mit Release-Note pro Issue geliefert werden. Bisher stand davon nur „bilingual (DE+EN)" in der Definition of Done — Vernetzung, Index-Nachzug und das Touchpoint-Quartett existierten nur als Praxis, nicht dokumentiert. Diese Story rahmt die Doku-Disziplin, die BOO-176/177 schon befolgt haben.

## Änderungen

- **Doku-Definition-of-Done-Checkliste** — neu im kanonischen Guidelines-Template `bootstrap/references/issue-writing-guidelines-template.md` (EN) + `.de.md` (DE), als eigener Block **zusätzlich** zur unveränderten kanonischen 5-Punkt-DoD (BOO-30): Vernetzung · 3 Indizes (`docs/INDEX.md`, `docs/onboarding/artefakt-landkarte.md`, `docs/releases/README.md`, je + `.en`) · DE+EN-Parität · Release-Note pro Issue · Sketch wo hilfreich · `docs-drift` grün.
- **Kurzfassung in `CONVENTIONS.md` §3** (EN- und DE-Block) — neue Subsection „Doku-Definition-of-Done (BOO-180)" mit dem **Touchpoint-Quartett**: HANDBUCH/Doku · Release-Note · Spec · Linear pro „Done" synchron halten. Verlinkt auf das Guidelines-Template.
- **Template-Triplikat** — `migrate_boo_180()` in `migrate-to-v2.sh` (registriert in `migrate_all` + `ALL_ISSUES`): nicht-destruktiver Hinweis, dass Bestandsprojekte die projektlokale `docs/issue-writing-guidelines.md` neu ziehen, um die Doku-DoD zu erben. Neue Projekte erben sie über den Guidelines-Copy beim Bootstrap.

## Abgrenzung

- **Reine Doku/Konvention, kein Code-Verhalten.** Kein neuer Hook, kein Gate — die DoD ist Operator-Disziplin, von `docs-drift` (DE+EN-Parität, tote Links) flankiert.
- Die kanonische 5-Punkt-DoD (BOO-30) bleibt **unverändert** — die Doku-DoD ist ein zusätzlicher Block, der nur greift, wenn die Story Doku berührt.
- **Selbst regelkonform:** diese Story erfüllt die eigene DoD (DE+EN, vernetzt Guidelines ↔ CONVENTIONS, Release-Note im Index, docs-drift grün).
- Wave-Buchstabe **bw** (bv = Unit-Test-Härtung BOO-177).

## Verweise

Spec: `specs/BOO-180.md`. Branch: `tobiaschschmidt/boo-180-docs-doku-definition-of-done`. Verwandt: BOO-30 (kanonische DoD), BOO-173 (Release-Index), BOO-176/177 (folgen der Doku-DoD). Operator-Quelle: Tobias, 2026-06-07.
