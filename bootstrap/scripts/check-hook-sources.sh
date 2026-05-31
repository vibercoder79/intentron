#!/usr/bin/env bash
# check-hook-sources.sh — Drift-Guard fuer gescaffoldete Hooks (BOO-89)
#
# Sichert die Single-Source-Konvention ab: ein Hook, der kanonisch unter
# bootstrap/references/hooks/<name>.sh liegt, darf NICHT zusaetzlich als eingebetteter
# Heredoc in migrate-to-v2.sh oder als Inline-Body im file-templates.md gepflegt werden
# (sonst driften die Kopien — siehe BOO-88). Zusaetzlich: ein frisch migrierter Hook muss
# byte-identisch zur kanonischen Quelle sein.
#
# Exit 0 = konsistent · Exit 1 = Drift/Verstoss gefunden.
# Lokal + in CI lauffaehig (nur bash + git + coreutils, dependency-frei).
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"          # bootstrap/
HOOKS_DIR="$ROOT/references/hooks"
TEMPLATES="$ROOT/references/file-templates.md"
TEMPLATES_EN="$ROOT/references/file-templates.en.md"
MIGRATE="$ROOT/scripts/migrate-to-v2.sh"

fail=0
note() { printf '  %s\n' "$1"; }
err()  { printf '  ✗ %s\n' "$1"; fail=1; }
ok()   { printf '  ✓ %s\n' "$1"; }

echo "== Drift-Guard: gescaffoldete Hooks (BOO-89) =="

# --- 1) Kanonische Hooks pruefen ---
if [[ ! -d "$HOOKS_DIR" ]]; then
    note "kein references/hooks/ — keine Single-Source-Hooks (ok)"
else
    for f in "$HOOKS_DIR"/*.sh; do
        [[ -e "$f" ]] || continue
        name="$(basename "$f")"
        if bash -n "$f" 2>/dev/null; then ok "kanonisch valide: $name"; else err "Syntaxfehler in kanonischer $name"; fi
        # Darf nicht zusaetzlich als Heredoc in migrate-to-v2.sh eingebettet sein.
        marker="$(echo "${name%.sh}" | tr '[:lower:]-' '[:upper:]_')_EOF"  # z.B. COVERAGE_CHECK_EOF
        if grep -q "<<'${marker}'" "$MIGRATE" 2>/dev/null; then
            err "$name ist kanonisch UND als Heredoc ($marker) in migrate-to-v2.sh — Single-Source verletzt"
        fi
        # Spezifisch coverage-check: alter COVCHECK_EOF darf nicht zurueckkehren.
        if [[ "$name" == "coverage-check.sh" ]]; then
            grep -q "COVCHECK_EOF" "$MIGRATE" 2>/dev/null && err "COVCHECK_EOF wieder eingebettet — migrate muss aus references/hooks/ kopieren" || ok "migrate kopiert coverage-check aus references/hooks/ (kein Heredoc)"
            for t in "$TEMPLATES" "$TEMPLATES_EN"; do
                if grep -q 'STMT_SEEN' "$t" 2>/dev/null; then err "$(basename "$t") enthaelt wieder den coverage-check-Inline-Body (STMT_SEEN) — sollte Pointer sein"; fi
            done
        fi
    done
fi

# --- 2) Frisch migrierter coverage-check == kanonisch? ---
CANON="$HOOKS_DIR/coverage-check.sh"
if [[ -f "$CANON" && -f "$MIGRATE" ]]; then
    tmp="$(mktemp -d)"; trap 'rm -rf "$tmp"' EXIT
    ( cd "$tmp" && git init -q && bash "$MIGRATE" --issue BOO-15 >/dev/null 2>&1 ) || true
    if [[ -f "$tmp/.claude/hooks/coverage-check.sh" ]] && cmp -s "$tmp/.claude/hooks/coverage-check.sh" "$CANON"; then
        ok "migriert == kanonisch (byte-identisch)"
    else
        err "migrierte coverage-check.sh weicht von der kanonischen Quelle ab"
    fi
fi

# --- 3) Noch eingebettete Hooks listen (Single-Source-Kandidaten, informativ) ---
echo "  -- noch eingebettet (BOO-89-Folge-Kandidaten, kein Fehler): --"
grep -oE "<<'[A-Z_]+_EOF'" "$MIGRATE" 2>/dev/null | sort -u | sed "s/^/    /" || true

echo
if [[ "$fail" -eq 0 ]]; then echo "Drift-Guard: OK"; else echo "Drift-Guard: DRIFT gefunden"; fi
exit "$fail"
