# Wave CB — EN-Nachzug der 43 Alt-Wave-Release-Notes: DE+EN-Parität rückwirkend (BOO-174)

> 🌐 **Sprache:** Deutsch (diese Datei) · [🇬🇧 English](wave-cb-en-parity-altwaves.en.md)

**Was jetzt da ist:** Alle 43 Wave-Release-Notes, die aus der Zeit **vor** der DE+EN-Parität-Regel (Doku-DoD, BOO-180) stammen und nur Deutsch waren, haben jetzt einen originalgetreuen englischen Spiegel. Der Release-Index ist in DE und EN regeneriert — keine *(DE only)*-Markierungen mehr. Reine Doku, keine Code-Änderung.

## Problem vorher

Beim Release-Notes-Audit (BOO-173) gefunden: 43 `wave-*.md` (von `wave-a` bis `wave-as`, inkl. `wave-b`…`wave-z`) hatten keinen `.en.md`-Spiegel. Im Index waren sie als *(DE only)* markiert. Die DE+EN-Parität-Regel galt damit nur für neue Waves — der Bestand blieb halb-deutsch.

## Änderungen

- **43 EN-Spiegel NEU** — pro Alt-Wave ein `wave-*.en.md`: gleiche Struktur, Überschriften, Tabellen, Reihenfolge; Code-Identifier, BOO-Nummern, Pfade, Links, Wave-Buchstaben und Versionen wortgleich übernommen (Anti-Fabrikation).
- **Sprachschalter in allen 43 DE-Quellen nachgerüstet** — `🌐`-Zeile direkt unter der H1, sonst inhaltlich unverändert (je +2 Zeilen, 0 Löschungen).
- **Release-Index regeneriert** — `README.md` (DE): EN-Link pro Eintrag ergänzt. `README.en.md` (EN): englischer Titel aus dem jeweiligen EN-Spiegel-H1 + `· [DE]`-Link, `*(DE only)*` entfernt. Wave-Zähler 81 → 82.

## Vorgehen

Agentic in 8 kleinen, nach Größe balancierten Batches über disjunkte Datei-Cluster (Memory: lange DE+EN-Sub-Agents timeouten → klein batchen). Pro Batch: DE-Quelle lesen → EN-Spiegel schreiben → Schalter nachrüsten. Danach Lead-Cross-Check: BOO-Nummern, URLs, Backtick-Identifier und Link-Ziele DE↔EN abgeglichen.

## Verweise

- Spec: `specs/BOO-174.md`
- Doku-Definition-of-Done: `docs/releases/wave-bw-doku-definition-of-done.md` (BOO-180)
- Release-Index-Konvention: `docs/releases/wave-bt-release-index.md` (BOO-173)
- Vorherige Welle: `docs/releases/wave-ca-observability-sichtbar.md`
