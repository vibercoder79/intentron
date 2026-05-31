# BOO-88 — Bugfix Diff-Coverage-Nenner zaehlt nicht-ausfuehrbare Zeilen

## Summary

`hooks/coverage-check.sh` (BOO-15, Diff-Coverage-Gate) zaehlt im Nenner (`TOTAL_ADDED`, Zeile ~1585) JEDE hinzugefuegte Source-Zeile — inklusive Kommentare und Leerzeilen. Diese sind nie ausfuehrbar, koennen also nie im Zaehler (`COVERED_ADDED`) landen. Folge: Die Quote wird kuenstlich gedrueckt, das Gate blockiert faelschlich vollstaendig getestete Stories. Gemeldet aus einer Feld-Installation (privacy-proxy, Story PP-001).

## Why

Das Gate berechnet `PCT = COVERED_ADDED * 100 / TOTAL_ADDED`. Da Kommentare und Leerzeilen in keinem Coverage-Tool als ausfuehrbare Statements auftauchen, landen sie nie im Zaehler — wohl aber im Nenner. Konkretes Beispiel:

- 8 ausfuehrbare Zeilen (alle getestet) + 4 Kommentar-Zeilen + 2 Leerzeilen = 14 Added-Lines
- Zaehler: 8 (alle ausfuehrbaren Zeilen getestet)
- Quote: `8 / 14 = 57 %` → unter der 60-%-Warn-Schwelle → **BLOCK**
- Obwohl 100 % des tatsaechlich ausfuehrbaren Codes getestet sind

Das Gate bestraft also sauber kommentierten Code.

Konsequenzen ohne diese Story:

- Gut dokumentierter, kommentierter Code wird systematisch schlechter bewertet als dichter Code ohne Kommentare — ein Fehlanreiz.
- Das Gate blockiert faelschlich vollstaendig getestete Stories, Operatoren verlieren Vertrauen in die Zahl oder schalten das Gate ab.
- Ein Governance-Gate, das an regulierte Kunden verkauft wird, liefert nachweislich falsche Zahlen — das untergraebt die Glaubwuerdigkeit des gesamten Quality-Gate-Versprechens.

## What

Der Nenner wird ausschliesslich aus **ausfuehrbaren Statement-Zeilen** gebildet — und zwar aus den Daten, die das Coverage-Tool ohnehin liefert, NICHT per Regex-Kommentar-Erkennung (das waere fragil und sprachabhaengig).

- **c8:** Die `statementMap` listet ALLE ausfuehrbaren Zeilen (unabhaengig vom Ausfuehrungs-Count). Neue Hilfsfunktion `parse_statement_lines_c8` gibt alle `statementMap`-Zeilen aus.
- **pytest-cov:** `executed_lines ∪ missing_lines` = alle ausfuehrbaren Zeilen. Neue Hilfsfunktion `parse_statement_lines_pytest`.
- **Hauptlauf:** Pro File werden zusaetzlich die Statement-Zeilen gecacht. Eine Added-Zeile wird nur dann in `TOTAL_ADDED` gezaehlt, wenn sie eine Statement-Zeile ist (sonst `continue`). Die Zaehler-Logik (`COVERED_ADDED`) bleibt unveraendert.

Konkreter Fix-Code:

```bash
# --- NEU: Statement-Zeilen (alle ausfuehrbaren Zeilen, unabhaengig vom Count) ---
parse_statement_lines_c8() {
    local file="$1"
    python3 - "$COVERAGE_FILE" "$file" <<'PYEOF'
import json, sys
cov_file, target = sys.argv[1], sys.argv[2]
try:
    data = json.load(open(cov_file))
except Exception:
    sys.exit(0)
target_abs = target.lstrip("./")
for k, v in data.items():
    if k.endswith(target_abs) or k.endswith(target):
        stmts = v.get("statementMap", {})
        for stmt_id, loc in stmts.items():
            line = loc.get("start", {}).get("line")
            if line:
                print(line)
        break
PYEOF
}

parse_statement_lines_pytest() {
    local file="$1"
    python3 - "$COVERAGE_FILE" "$file" <<'PYEOF'
import json, sys
cov_file, target = sys.argv[1], sys.argv[2]
try:
    data = json.load(open(cov_file))
except Exception:
    sys.exit(0)
files = data.get("files", {})
target_norm = target.lstrip("./")
for k, v in files.items():
    if k.endswith(target_norm) or k.endswith(target):
        for line in v.get("executed_lines", []):
            print(line)
        for line in v.get("missing_lines", []):
            print(line)
        break
PYEOF
}
```

Geaenderte Zaehlschleife im Hauptlauf (mit `continue`-Guard fuer Nicht-Statement-Zeilen):

```bash
declare -A FILES_SEEN
declare -A STMT_SEEN
while IFS= read -r entry; do
    [[ -z "$entry" ]] && continue
    file="${entry%:*}"
    line="${entry##*:}"

    # Nur Source-Files (unveraendert)
    if ! echo "$file" | grep -qE '\.(js|mjs|ts|tsx|jsx|py)$'; then
        continue
    fi
    if echo "$file" | grep -qE '(^test|/test|_test\.|\.test\.|\.spec\.|tests/|__tests__|conftest\.py)'; then
        continue
    fi

    # Per-File einmal Coverage-Daten holen (gedeckte Zeilen + Statement-Zeilen)
    if [[ -z "${FILES_SEEN[$file]:-}" ]]; then
        if [[ "$COVERAGE_TOOL" == "c8" ]]; then
            FILES_SEEN[$file]="$(parse_covered_lines_c8 "$file" | tr '\n' ' ')"
            STMT_SEEN[$file]="$(parse_statement_lines_c8 "$file" | tr '\n' ' ')"
        else
            FILES_SEEN[$file]="$(parse_covered_lines_pytest "$file" | tr '\n' ' ')"
            STMT_SEEN[$file]="$(parse_statement_lines_pytest "$file" | tr '\n' ' ')"
        fi
    fi

    # NEU: Nenner-Guard — nur ausfuehrbare Statement-Zeilen zaehlen.
    # Kommentare/Leerzeilen sind nie Statements → raus aus dem Nenner.
    if ! echo " ${STMT_SEEN[$file]} " | grep -qw "$line"; then
        continue
    fi

    TOTAL_ADDED=$(( TOTAL_ADDED + 1 ))
    if echo " ${FILES_SEEN[$file]} " | grep -qw "$line"; then
        COVERED_ADDED=$(( COVERED_ADDED + 1 ))
    fi
done <<< "$ADDED"
```

Drei Quellstellen (Single-Source-Drift — alle drei identisch fixen):

- `bootstrap/references/file-templates.md` §coverage-check.sh (DE)
- `bootstrap/references/file-templates.en.md` (EN-Spiegel)
- `bootstrap/scripts/migrate-to-v2.sh` (eingebetteter Heredoc in `migrate_boo_15`)

Versions-Marker und ersetzende Migration:

- Versions-Marker im Skript-Kopf (z.B. `# coverage-check v2`).
- Migration erkennt die alte Version (v1 bzw. fehlender Marker) und ERSETZT das Skript, mit Backup (`.bak`). Begruendung: `migrate_boo_15` ist heute idempotent und ueberschreibt vorhandene Dateien NICHT → bestehende Installs bekaemen den Fix sonst nie.

Test-Faelle:

- Wegwerf-Diff mit 8 Code- + 4 Kommentar- + 2 Leerzeilen + passender `coverage-final.json` → Skript meldet 100 % (nicht 57 %).
- Zweiter Fall: 6 von 8 Code-Zeilen getestet → 75 %.

Begleitend:

- migration-checklist-Eintrag §BOO-88 (DE+EN).
- Release Notes `docs/releases/wave-*-coverage-denominator-fix.md`.
- Skript-Versions-Bump (v1 → v2 im Marker).

## Constraints

- **Dependency-Freiheit bleibt (Designprinzip 2026-05-25, Pflicht):** KEIN `diff-cover`, KEIN `@connectis/diff-test-coverage`. Der bestehende Anti-Patterns-Block bleibt gueltig. Der Fix nutzt ausschliesslich die bereits vorhandenen JSON-Daten (`statementMap` bzw. `executed_lines`/`missing_lines`).
- **Pragma-Check:** Kein neuer Overhead, kein neues Tool — nur ein zweiter Python-Parse-Aufruf pro File auf derselben JSON-Datei.
- **Security/Korrektheit-Check:** Das Gate wird wieder vertrauenswuerdig — direkter Bezug zur regulierten Zielgruppe, die korrekte Coverage-Zahlen braucht.
- **Mittelweg-Begruendung:** Minimal-invasiver Fix an der bestehenden Mechanik (ein Guard + zwei Parser) statt Neubau des Gates.
- Reiner Bugfix: Schwellwerte (`COVERAGE_PASS`/`COVERAGE_WARN`), Workflow und der Aufruf in `/implement` Schritt 6a-quart bleiben unveraendert.
- DE + EN konsistent.

## Decisions

1. **Statement-Quelle = Coverage-Tool-Daten** (`statementMap` bei c8, `executed_lines ∪ missing_lines` bei pytest-cov), NICHT Regex-Kommentar-Erkennung — sprachneutral und nicht fragil.
2. **Fix an allen 3 Quellstellen synchron** (DE-Template, EN-Spiegel, migrate-to-v2.sh-Heredoc) — identische Logik, kein Drift.
3. **Versions-Marker + ersetzende Migration** fuer Bestands-Installs (nicht nur additiv) — sonst bekommen vorhandene Projekte den Fix nie, weil `migrate_boo_15` idempotent ist und nicht ueberschreibt. Migration legt `.bak` an.
4. **Dependency-Freiheit bleibt erhalten** — kein neues Tool, nur vorhandene JSON-Daten.
5. **DRY-Smell (Skript dreifach gepflegt) wird hier NICHT geloest** — separate Folge-Story (Single-Source-Refactor), um diesen Bugfix klein und reviewbar zu halten.

## Agent-Pattern

**Gewaehltes Pattern:** sub-agents (sequentiell).

**Begruendung:** Die Arbeit zerfaellt in abgegrenzte Brocken: (1) Skript-Fix im DE-Template, (2) EN-Spiegel, (3) `migrate-to-v2.sh`-Heredoc plus ersetzende Migration mit Versions-Marker, (4) Test-Fall, (5) Doku/Release-Notes. Sequentiell statt parallel, weil die drei Skript-Varianten byte-identische Logik tragen muessen — der DE-Fix ist die Referenz, die anderen spiegeln ihn. Hard-Constraint pro Sub-Agent: "Nenner-Logik ausschliesslich ueber Coverage-JSON-Statements bilden, KEINE Regex-Kommentarerkennung; Schwellwerte und Workflow nicht anfassen."

## Validation

- `bash -n` auf allen drei Skript-Varianten (DE-Template-Extract, EN-Template-Extract, migrate-to-v2.sh) → Exit 0.
- Test-Fall 8 Code + 4 Kommentar + 2 Leerzeilen → meldet 100 % (nicht 57 %).
- Test-Fall 6 von 8 Code-Zeilen getestet → meldet 75 %.
- Reine Kommentar-/Leerzeilen-Diffs aendern die Quote nicht mehr.
- c8- und pytest-cov-Pfad beide gefixt.
- Versions-Marker im Skript-Kopf vorhanden.
- Migration ersetzt alte Version (v1/fehlender Marker) mit `.bak`-Backup und laesst eine bereits aktualisierte v2-Datei unangetastet (idempotent).
- Alle 3 Quellstellen tragen identische Logik.
- migration-checklist + Release Notes DE+EN vorhanden.
- `git diff --check` clean.

## Acceptance Criteria

- [ ] `parse_statement_lines_c8` und `parse_statement_lines_pytest` in allen 3 Quellstellen vorhanden
- [ ] Zaehlschleife mit `continue`-Guard fuer Nicht-Statement-Zeilen in allen 3 Quellstellen
- [ ] Zaehler-Logik (`COVERED_ADDED`) unveraendert
- [ ] Versions-Marker (`# coverage-check v2`) im Skript-Kopf aller 3 Quellstellen
- [ ] Migration erkennt v1/fehlenden Marker und ersetzt das Skript mit `.bak`-Backup
- [ ] Migration laesst vorhandene v2-Datei unangetastet (idempotent)
- [ ] Test-Fall 8+4+2 → 100 %
- [ ] Test-Fall 6/8 → 75 %
- [ ] `bash -n` Exit 0 auf allen 3 Skript-Varianten
- [ ] c8- und pytest-cov-Pfad beide gefixt
- [ ] Schwellwerte, Workflow und Aufruf in 6a-quart unveraendert
- [ ] Keine neue Dependency (Anti-Patterns-Block bleibt gueltig)
- [ ] migration-checklist Eintrag §BOO-88 (DE+EN)
- [ ] Release Notes `docs/releases/wave-*-coverage-denominator-fix.md`
- [ ] `git diff --check` clean

## Dependencies

- **Bezug:** BOO-15 (Diff-Coverage-Gate, das hier gefixt wird).
- **Bezug:** Drei-Layer-Quality-Gate-ADR (Layer 2 — automatisierte Gates).

## Session-Referenz

Feld-Feedback 2026-05-31 (privacy-proxy / Story PP-001, gemeldet von einem Factory-Nutzer). Linear: <https://linear.app/owlist/issue/BOO-88/>. Folge-Themen (separate Stories): DRY-Single-Source fuer das dreifach gepflegte Skript + Contribute-Back-Schleife fuer Feld-Fixes.

## Rollout

Bugfix — additiv fuer neue Projekte (Bootstrap zieht die v2-Variante) und ersetzend fuer Bestands-Installs via Migration (mit `.bak`-Backup). Kein Feature-Flag noetig. Schwellwerte unveraendert.
