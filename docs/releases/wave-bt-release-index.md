# Wave BT — Release-Notes vernetzt: zentraler Wave-Index + DE↔EN-Sprachschalter (BOO-173)

> 🌐 **Sprache:** Deutsch (diese Datei) · [🇬🇧 English](wave-bt-release-index.en.md)

**Was jetzt da ist:** Die Release-Notes (Wave-Docs) sind jetzt **vernetzt** statt lose nebeneinander zu liegen. Auslöser war ein Operator-Audit: „Sind für alle Merges Release-Notes DE+EN da und vernetzt?" — DE+EN war erfüllt, die Vernetzung fehlte.

## Änderungen
- **Neu `docs/releases/README.md` (+ `.en.md`):** zentraler **Release-Index** — listet **alle Waves** chronologisch (neueste zuerst) mit Titel + Link (DE, EN wo vorhanden). Erklärt die Wave-Konvention und wie man eine neue Wave einträgt. Mit DE↔EN-Sprachschalter.
- **DE↔EN-Sprachschalter** (`🌐`) in die **6 jüngsten** Wave-Paare nachgerüstet (wave-bn…bs, DE+EN) — analog zur README-/Runbook-Konvention.

## Audit-Befund (Stand 2026-06-07)
- Release-Notes pro Merge der letzten Tage (BOO-167…172): **vollständig DE+EN** (wave-bn…bs).
- Sehr frühe Waves (wave-a…as) sind **nur Deutsch** — vor Einführung der DE+EN-Parität; im Index als *(DE only)* markiert, EN-Nachzug bewusst nicht Teil dieser Story.

## Abgrenzung
- Reine Doku, kein Code. Kein EN-Nachzug der Alt-Waves (separate optionale Folge). Index ist statisch — neue Waves werden oben manuell eingetragen (Hinweis steht im Index). Wave-Buchstabe **bt** (bs = tmux-Runbook BOO-172).

## Verweise
Spec: `specs/BOO-173.md`. Branch: `feat/boo-173-release-index`. Verwandt: BOO-167 (Doku-Vernetzung), BOO-172. Operator-Quelle: Tobias, 2026-06-07.
