# Wave AN — Artefakt- & Freigabe-Landkarte (BOO-108)

> 🌐 **Sprache:** Deutsch (diese Datei) · [🇬🇧 English](wave-an-artefakt-landkarte.en.md)

**Was jetzt da ist:** ein drittes Onboarding-Dokument, das die Bruecke zwischen den Discovery-Boegen und den Phasen-Artefakten schliesst — plus Bootstrap-Kopplung, Migration, HANDBUCH-Anhang und Sketch.

## Stories
- **BOO-108** — Artefakt- & Freigabe-Landkarte: RACI-Matrix Artefakt → Abnehmer-Rolle → Regel-Senke.

## Aenderungen
- `docs/onboarding/artefakt-landkarte.md` + `.en.md` — Master-Matrix ueber alle 13 Skills/Phasen in 4 Bloecken (Setup/Governance · Produkt/Architektur · Security/Datenschutz · Lieferung/Betrieb/Compliance). Spalten: Artefakt · Pfad · Phase · Default-Template · Trigger · Abnehmer-Rolle · Regel-Senke · Status.
- **7 Regel-Senken** als Zielspalte: `CLAUDE.md`, `CONVENTIONS.md`, `ARCHITECTURE_DESIGN.md §5`, `SECURITY.md`, `dpo/controls/`, `.claude/environment.json`, `DEVELOPER_ONBOARDING.md`.
- **DESIGN.md-Muster:** Frontend-Design (Farben/Typo/Komponenten) ist Architektur — `§5` verweist immer auf `DESIGN.md` (keine Vorgaben = explizite Aussage); Abnehmer Design/Brand.
- **Bootstrap 4.3c** (`bootstrap/SKILL.md`): Ja/Nein-Frage, seedet gefilterte `solution-artefakte.md` (idempotent), Trigger an Block-A-Antworten.
- **HANDBUCH Anhang Z / Appendix Z** (DE+EN) + Footer; **README**-Abschnitt „Kunden-Onboarding — die drei Checklisten" (DE+EN).
- **Sketch** `docs/assets/onboarding-flow.png` / `.en.png` (+ `.excalidraw`-Quellen), OWLIST-Farben, im Render-Loop erstellt: drei Checklisten → Artefakte×Abnehmer → 7 Regel-Senken → autonomes Team.

## Migration (Bestandsprojekte)
```bash
bash bootstrap/scripts/migrate-to-v2.sh --issue BOO-108
```
`migrate_boo_108()` seedet `solution-artefakte.md` aus der Master-Vorlage (idempotent — vorhandene Operator-Instanz bleibt unberuehrt). Danach manuell auf die Solution filtern.

## Smoke-Test
- `bash -n bootstrap/scripts/migrate-to-v2.sh` → OK; `--list` enthaelt `BOO-108`; `--issue BOO-108 --dry-run` zeigt den Seed-Schritt.
- Beide Sketches gerendert + visuell geprueft (keine Ueberlappung/Clipping).

## Verweise
Spec: `specs/BOO-108.md`. Doku: `docs/onboarding/artefakt-landkarte.md`. Release: v0.7.5.
