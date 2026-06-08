# Wave Z — Contribute-Back-Schleife: contribute-fix.sh (BOO-90)

> 🌐 **Sprache:** Deutsch (diese Datei) · [🇬🇧 English](wave-z-contribute-back.en.md)

**Linear:** [BOO-90](https://linear.app/owlist/issue/BOO-90/) · Folge-Story aus BOO-88

## Problem

Wenn ein deployter Factory-Nutzer einen Bug in einem kopierten Governance-Artefakt findet und
lokal fixt (wie der coverage-check-Bug aus privacy-proxy / PP-001 → BOO-88), gab es **keinen
Weg zurueck** in die Factory-Quelle. Der Rueckfluss lief manuell (Nutzer → Tobias → Fix).
Das skaliert nicht und ist nicht audit-tauglich.

## Was sich aendert

- **Neuer Helfer `bootstrap/scripts/contribute-fix.sh`** (Feld→Quelle): erkennt im Projekt
  lokal geaenderte Framework-Artefakte (zunaechst die gescaffoldeten Hooks unter
  `.claude/hooks/`, die kanonisch in `bootstrap/references/hooks/` liegen — siehe BOO-89) und
  erzeugt pro Abweichung:
  - einen sauberen **Patch** (`contribute-back/<name>.patch`),
  - einen **Issue-Vorschlag** (`contribute-back/<name>.proposal.md`) mit Titel + Body + Patch.
- **Kein Auto-Push, kein Auto-PR.** Der Operator prueft und reicht selbst ein — kein
  ungefragtes Abfliessen von Code aus einem Kundenprojekt.
- **Kopplung an BOO-89:** Je mehr Hooks Single-Source werden (`references/hooks/`), desto mehr
  Artefakte deckt `contribute-fix` automatisch ab.

## Nutzung

```bash
bash <framework>/bootstrap/scripts/contribute-fix.sh --project .
# → contribute-back/coverage-check.sh.{patch,proposal.md} (falls Abweichung)
```

## Verifiziert

- Lokale Abweichung → Patch + Vorschlag erzeugt, Patch enthaelt die Operator-Aenderung.
- Identisch zur Quelle → „nichts beizutragen", kein `contribute-back/` angelegt.
- `bash -n` sauber.

## Designentscheid

Operator-Wahl „/contribute-fix-Helfer (Rueckfluss)". Bewusst der **Feld→Quelle**-Pfad (der
eigentliche Gap); der Quelle→Feld-Pfad (Versions-Marker + ersetzende Migration) ist bereits
mit BOO-88 fuer coverage-check etabliert und kann spaeter verallgemeinert werden.

## Folge

- Generalisierung auf weitere Artefakt-Typen (nicht nur Hooks) und ein optionaler
  `/contribute-fix`-Skill-Wrapper bleiben spaetere Ausbaustufen.
