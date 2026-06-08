# Release Notes - Wave L Multi-Operator-Koordination

> 🌐 **Sprache:** Deutsch (diese Datei) · [🇬🇧 English](wave-l-multi-operator-coordination.en.md)

Stand: 2026-05-27

## Zweck

Wave L schliesst BOO-72. Das Framework bekommt einen HANDBUCH-Anhang R, der die ehrliche Antwort auf eine bisher unbeantwortete Operator-Frage liefert: "Wenn 20 Entwickler gleichzeitig im selben GitHub-Repo arbeiten und sich Doku aus Obsidian (oder Jira/Confluence/Notion) holen — funktioniert das Framework dann noch?". Anhang R trennt die Frage in drei Layer (Code / Koordination / Doku), zeigt pro Layer "was skaliert nativ, was nicht, welche Optionen hat der Operator", und gibt eine konkrete 10-Schritte-Anleitung fuer INTENTRON in einem 20-koepfigen Team. **Reine Doku-Story** — kein neuer Skill, keine neue Bootstrap-Frage, keine Framework-Konvention. Inklusive 1 hochwertigem Excalidraw-Sketch (`docs/assets/boo-72-multi-operator-3-layer.png`).

**Erwarteter Effekt:** Anhang R schliesst das letzte grosse Vertriebs-Argument bei Team-Mandaten — "skaliert das auf 20 Personen?" hat jetzt eine klare HANDBUCH-Antwort. Anhang P (Wave K) deckt 2-5 Operatoren, Anhang R erweitert auf 5-20+.

## Betroffene Stories

- BOO-72 — HANDBUCH Anhang R Multi-Operator-Koordination + Excalidraw-Sketch

## Wichtige Klarstellung: keine Vier-Augen-Enforcement

Anhang R dokumentiert die Vier-Augen-Konvention fuer `review-ok` (Sensitive-Paths-Gate) und `privacy-ok` (Personal-Data-Paths-Gate) als **Operator-Disziplin**, nicht als Framework-Gate. Theoretisch waere ein Author-Vergleich im Gate prueffbar (Author des Gate-Commits != Author der Aenderung), aber das wuerde Framework-Komplexitaet erhoehen ohne klar messbaren Mehrwert. Audit-Trail laeuft ueber `git blame` — die Konvention ist beobachtbar, nicht erzwungen. BOO-72 schliesst Enforcement explizit aus.

## Was Nutzer mit dem neuen Setup bekommen

- **HANDBUCH Anhang R "Multi-Operator-Koordination" (DE+EN)** mit:
  - 3-Layer-Modell (Code-Layer / Koordinations-Layer / Doku-Layer) — pro Layer eine Tabelle "was skaliert, was nicht, Optionen".
  - **Branch-Strategie-Vergleich:** Trunk-Based / Feature-Branches / GitFlow mit Empfehlung pro Team-Groesse.
  - **CODEOWNERS-Beispiel:** konkrete `.github/CODEOWNERS`-Pattern fuer kritische Pfade (`SECURITY.md`, `PRIVACY.md`, `ARCHITECTURE_DESIGN.md`) + Domain-Bereiche.
  - **Team-Topologien:** Pool / Squad / Hybrid mit Tradeoffs und konkretem 15-Personen-Beispiel.
  - **Doku-SSoT-Wahl-Matrix** ueber 7 Optionen × 4 Team-Groessen (Solo / Klein / Mittel / Gross) mit Skalierungs-Indikatoren.
  - **Vier-Augen-Konvention** fuer `review-ok` / `privacy-ok` mit Audit-Spur-Beispiel.
  - **Skill-Pool-Governance** mit Wartungs-Owner-Rolle, Drift-Audits, Skill-Quarantaene fuer externe Skills.
  - **Konflikt-Eskalation** mit 3 Stufen (CODEOWNERS → Squad-Lead → Lead-Architekt-Veto).
  - **10-Schritte-Setup-Anleitung** "Wie setzt man INTENTRON in einem 20-koepfigen Team auf?" — erweitert Anhang P Szenario 3 (Multi-User-VPS-Coding-Factory).
  - "Was Anhang R nicht macht"-Sektion mit harten Abgrenzungen.
- **Excalidraw-Sketch `docs/assets/boo-72-multi-operator-3-layer.png`** mit OWLIST-Farben — visualisiert das 3-Layer-Modell mit Fan-in (Code), Kanban-Strip (Koordination) und Side-by-Side-Trio (Doku-SSoT-Wahl). Bootstrap-Callout zeigt die Verknuepfung zu Frage B.3 (Doku-SSoT) und A.7 (Deployment).

## Konkrete Aenderungen

| Bereich | Aenderung | Datei |
|---|---|---|
| HANDBUCH Anhang R NEU | Multi-Operator-Koordination (DE) | `HANDBUCH.md` ab Zeile 3491 |
| HANDBUCH Appendix R NEU | Multi-operator coordination (EN) | `HANDBUCH.en.md` ab Zeile 2974 |
| Sketch NEU | Excalidraw + PNG-Export | `docs/assets/boo-72-multi-operator-3-layer.excalidraw` + `.png` |
| Spec NEU (in Wave K committed `213bd46`) | Spec BOO-72 mit Operator-Frage + 3-Layer-Modell + Decision-Matrix | `specs/BOO-72.md` |
| Migration | `migrate_boo_72()` (Doku-only Hinweis-Block, idempotent) | `bootstrap/scripts/migrate-to-v2.sh` |
| Migration-Checklist | §BOO-72 (DE+EN) | `bootstrap/references/migration-checklist-v1-to-v2.md` + `.en.md` |
| ALL_ISSUES-Array | `BOO-72` ergaenzt | `bootstrap/scripts/migrate-to-v2.sh` |

## Skill-Versions-Bumps

Keine. Wave L ist reine Doku-Story.

## Migration fuer Bestands-Projekte

`migrate_boo_72()` in `bootstrap/scripts/migrate-to-v2.sh`:

```bash
bash bootstrap/scripts/migrate-to-v2.sh --issue BOO-72
```

Doku-only, keine File-Operation. Auto-Schritt gibt Operator-Hinweise aus:

- HANDBUCH Anhang R / Appendix R lesen
- Team-Groesse + Pattern-Wahl in `migration-status.md` unter §BOO-72 vermerken
- Ab 5 Operatoren: `.github/CODEOWNERS` anlegen
- Ab 10 Operatoren: Vier-Augen-Konvention + Konflikt-Eskalations-Pfad in `CONVENTIONS.md` dokumentieren

Operator-Aktion: HANDBUCH Anhang R einmal lesen, je nach Team-Groesse die Konventionen anwenden. Bei Solo oder Team unter 5: Eintrag mit Status `✗ — Team-Groesse unterhalb Anhang-R-Schwelle`.

## Designentscheid: Inspirations-Schicht, kein Framework-Enforcement

Anhang R schliesst eine echte Doku-Luecke (Vertriebs-Hindernis bei Team-Mandaten), **ohne** das Framework zu erweitern. Das ist INTENTRON-Philosophie "leichtgewichtig + pragmatisch":

- Kein neuer Skill, keine neue Bootstrap-Frage — das Framework macht schon genug.
- Pattern-Optionen sind Tradeoff-Tabellen, nicht Empfehlungs-Urteile.
- Vier-Augen-Enforcement bewusst NICHT umgesetzt — Operator-Disziplin bleibt Operator-Disziplin.
- Keine "Best Practice"-Festlegung bei Confluence vs. Notion vs. SharePoint — Operator waehlt aus.

## Noch offen / Folgepunkte

- **Wave M (BOO-73):** DPO + security-architect ins Framework-Bundle aufnehmen (Vendored-Kopien). Korrektur der Wave-J-Decision "DPO bleibt Standalone" — wenn das Framework Privacy-by-Design garantieren will, muss der DPO-Skill aus dem Framework-Repo installierbar sein. Spec wird direkt im Anschluss an Wave L angelegt.
- **Beispiel-Audit:** ein realer 15+ Operator-Aufbau (Beratungs-Mandat? Inhouse?) waere ein guter "show, don't tell"-Folgeschritt zur Verifikation von Anhang R. Eigene Spec faellig.

## Verweise

- Spec: `specs/BOO-72.md` (committed in Wave K `213bd46`)
- HANDBUCH: Anhang R Multi-Operator-Koordination (DE+EN)
- Sketch: `docs/assets/boo-72-multi-operator-3-layer.png`
- Migration: `bootstrap/scripts/migrate-to-v2.sh` (`migrate_boo_72`)
- Migration-Checklist: §BOO-72 (DE+EN)
- Feedback-Quelle: Operator Tobias, 2026-05-27 (post-Wave-K-Session)
- Linear: <https://linear.app/owlist/issue/BOO-72/>
- Vorherige Welle: `docs/releases/wave-k-deployment-and-sovereignty.md`
