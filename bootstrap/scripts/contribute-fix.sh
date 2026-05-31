#!/usr/bin/env bash
# contribute-fix.sh — Contribute-Back-Schleife Feld→Quelle (BOO-90)
#
# Erkennt in einem deployten Projekt lokal geaenderte Framework-Artefakte (zunaechst die
# gescaffoldeten Hooks unter .claude/hooks/, die kanonisch in der Factory-Quelle liegen)
# und erzeugt pro Abweichung einen sauberen Patch + einen Issue-Vorschlag. Damit fliessen
# Feld-Fixes (wie der coverage-check-Bug aus privacy-proxy / BOO-88) systematisch zurueck.
#
# Bewusst KEIN Auto-Push und KEIN Auto-PR — der Operator prueft und reicht selbst ein
# (kein ungefragtes Abfliessen von Code aus einem Kundenprojekt).
#
# Usage: contribute-fix.sh [--project <dir>] [--framework <dir>]
#   --project    Projekt-Wurzel (Default: aktuelles Verzeichnis)
#   --framework  Pfad zur Factory-/intentron-Quelle (Default: aus Skript-Lage abgeleitet)
# Exit 0 = Lauf ok (auch wenn Abweichungen gefunden — die stehen im Report).
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
FRAMEWORK="$(cd "$SCRIPT_DIR/../.." && pwd)"   # bootstrap/scripts → Repo-Wurzel
PROJECT="$(pwd)"

while [[ $# -gt 0 ]]; do
    case "$1" in
        --project)   PROJECT="$2"; shift 2 ;;
        --framework) FRAMEWORK="$2"; shift 2 ;;
        -h|--help)   grep '^#' "$0" | sed 's/^# \{0,1\}//'; exit 0 ;;
        *) echo "Unbekanntes Argument: $1" >&2; exit 2 ;;
    esac
done

PROJECT="$(cd "$PROJECT" && pwd)"
HOOKS_CANON="$FRAMEWORK/bootstrap/references/hooks"
OUT="$PROJECT/contribute-back"

if [[ ! -d "$HOOKS_CANON" ]]; then
    echo "[CONTRIBUTE-FIX] Keine kanonischen Hooks unter $HOOKS_CANON — ist --framework korrekt?" >&2
    exit 2
fi

mkdir -p "$OUT"
found=0
proj_name="$(basename "$PROJECT")"

for canon in "$HOOKS_CANON"/*.sh; do
    [[ -e "$canon" ]] || continue
    name="$(basename "$canon")"
    local_file="$PROJECT/.claude/hooks/$name"
    [[ -f "$local_file" ]] || continue
    if cmp -s "$local_file" "$canon"; then
        continue   # identisch → nichts beizutragen
    fi
    found=$((found + 1))
    patch="$OUT/$name.patch"
    # Patch: kanonisch (a) → lokal (b). Operator-Aenderung ist das, was b ggue. a hinzufuegt.
    diff -u "$canon" "$local_file" > "$patch" || true
    {
        echo "# Contribute-Back: \`$name\` weicht von der Factory-Quelle ab"
        echo
        echo "**Projekt:** $proj_name"
        echo "**Lokales Artefakt:** \`.claude/hooks/$name\`"
        echo "**Kanonische Quelle:** \`bootstrap/references/hooks/$name\`"
        echo
        echo "## Vorgeschlagener Issue (an die Factory-Quelle einreichen)"
        echo
        echo "- **Titel:** \`Feld-Fix: $name — <kurz beschreiben>\`"
        echo "- **Body:** Im deployten Projekt \`$proj_name\` wurde \`$name\` lokal angepasst."
        echo "  Der Patch unten zeigt die Abweichung gegenueber der kanonischen Quelle."
        echo "  Bitte pruefen und ggf. in \`bootstrap/references/hooks/$name\` uebernehmen"
        echo "  (kein Auto-Merge — der Drift-Guard BOO-89 zieht die Migration nach)."
        echo
        echo "## Patch"
        echo
        echo '```diff'
        cat "$patch"
        echo '```'
    } > "$OUT/$name.proposal.md"
    echo "[CONTRIBUTE-FIX] Abweichung: .claude/hooks/$name → $OUT/$name.{patch,proposal.md}"
done

echo
if [[ "$found" -eq 0 ]]; then
    echo "[CONTRIBUTE-FIX] Keine Abweichungen gegenueber der Factory-Quelle gefunden — nichts beizutragen."
    rmdir "$OUT" 2>/dev/null || true
else
    echo "[CONTRIBUTE-FIX] $found Artefakt(e) weichen ab. Patches + Vorschlaege liegen in: contribute-back/"
    echo "[CONTRIBUTE-FIX] Naechster Schritt (Operator): pruefen und als Issue/PR an die Factory-Quelle einreichen."
    echo "[CONTRIBUTE-FIX] Es wurde NICHTS automatisch gepusht."
fi
exit 0
