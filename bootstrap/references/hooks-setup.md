# Hook Templates — Governance Enforcement

Diese Hooks sichern maschinell die Kern-Governance-Regeln ab.
Beide Hooks liegen unter `.claude/hooks/` und werden via Claude Code `settings.json` aktiviert.

Wichtig: In INTENTRON meint "Hook" zuerst einen **Coding-/Runtime-Hook** des jeweiligen KI-Werkzeugs, nicht zwingend einen nativen Git-Hook in `.git/hooks/`.

| Layer | Zweck | Beispiele |
|-------|-------|-----------|
| KI-Runtime-Hook | Blockiert riskante Tool-Aufrufe waehrend der Arbeit | Claude Code `PreToolUse` → `pre-edit-bodyguard.sh` (`Edit|Write`), Codex `.codex/hooks.json` |
| Lokaler Git-Hook | Optionaler Schutz direkt vor Commit/Push | `.git/hooks/pre-commit`, `.git/hooks/commit-msg` |
| CI-Gate | Unabhaengiger Beweis auf GitHub/GitLab/Azure | ESLint/Ruff, Semgrep, Tests, Coverage, Sonar |

Bootstrap darf Git-Hooks optional spiegeln, aber die Framework-Pflicht liegt im Projektvertrag: `CONVENTIONS.md` beschreibt aktive Gates, Runtime-Hooks setzen sie frueh durch, CI beweist sie unabhaengig.

---

## spec-gate.sh

Blockiert `git commit` mit Issue-Referenz (z.B. `ISSUE-42`) wenn:
1. kein Spec-File `specs/ISSUE-42.md` existiert
2. das Spec-File kein ausgefülltes `## Agent-Pattern` Feld enthält
3. Pattern = `Agent-Team` aber keine Team-Komposition angegeben

```bash
#!/bin/bash
# ─────────────────────────────────────────────────────────────────────────────
#  SPEC-GATE — Governance Hook
#  Blockiert git commit wenn Spec-File fehlt oder Agent-Pattern nicht ausgefüllt
#
#  Claude Code PreToolUse Hook (Bash)
#  Input: JSON via stdin: {"tool_input": {"command": "..."}}
#  Exit 1 → Tool-Call blockiert | Exit 0 → erlaubt
# ─────────────────────────────────────────────────────────────────────────────

set -euo pipefail

PROJECT_ROOT=$(git rev-parse --show-toplevel 2>/dev/null || echo ".")

# JSON parsen → Command extrahieren
INPUT=$(cat)
CMD=$(echo "$INPUT" | python3 -c "
import sys, json
try:
    d = json.load(sys.stdin)
    print(d.get('tool_input', {}).get('command', ''))
except:
    print('')
" 2>/dev/null || echo "")

# Nur git commit Befehle prüfen
if ! echo "$CMD" | grep -qE 'git commit'; then
  exit 0
fi

# ISSUE-XXX aus Commit-Message extrahieren (z.B. PROJ-42, ISSUE-123)
ISSUE=$(echo "$CMD" | grep -oP '[A-Z]+-\d+' | head -1 || echo "")
if [ -z "$ISSUE" ]; then
  exit 0  # Kein Issue referenziert → kein Gate
fi

# ── Check 1: Spec-File vorhanden? ────────────────────────────────────────────
SPEC_FILE="${PROJECT_ROOT}/specs/${ISSUE}.md"
if [ ! -f "$SPEC_FILE" ]; then
  echo ""
  echo "╔══════════════════════════════════════════════════════════════╗"
  echo "║  🚫  GOVERNANCE-SPERRE: specs/${ISSUE}.md fehlt!            "
  echo "╚══════════════════════════════════════════════════════════════╝"
  echo ""
  echo "  Commit mit ${ISSUE} ist BLOCKIERT."
  echo "  Regel: NIEMALS Code ändern ohne Spec-File"
  echo ""
  echo "  Nächste Schritte:"
  echo "  1. specs/TEMPLATE.md lesen"
  echo "  2. specs/${ISSUE}.md erstellen + befüllen"
  echo "  3. git add specs/${ISSUE}.md && git commit -m 'docs: specs/${ISSUE}.md'"
  echo ""
  exit 1
fi

# ── Check 2: Agent-Pattern Sektion vorhanden? ────────────────────────────────
if ! grep -q "## Agent-Pattern" "$SPEC_FILE"; then
  echo ""
  echo "╔══════════════════════════════════════════════════════════════╗"
  echo "║  🚫  GOVERNANCE-SPERRE: Agent-Pattern fehlt in Spec!        "
  echo "╚══════════════════════════════════════════════════════════════╝"
  echo ""
  echo "  Commit mit ${ISSUE} ist BLOCKIERT."
  echo "  Regel: Jede Spec braucht ## Agent-Pattern Sektion"
  echo ""
  echo "  Nächste Schritte:"
  echo "  1. specs/${ISSUE}.md öffnen"
  echo "  2. ## Agent-Pattern Sektion aus specs/TEMPLATE.md einfügen"
  echo "  3. Gewähltes Pattern + Begründung ausfüllen"
  echo ""
  exit 1
fi

# ── Check 3: Gewähltes Pattern nicht leer/TBD/Platzhalter? ───────────────────
PATTERN=$(grep "^\*\*Gewähltes Pattern:\*\*" "$SPEC_FILE" | sed 's/\*\*Gewähltes Pattern:\*\* //' | tr -d '[:space:]' || echo "")
if [ -z "$PATTERN" ] || [ "$PATTERN" = "TBD" ] || echo "$PATTERN" | grep -q "\["; then
  echo ""
  echo "╔══════════════════════════════════════════════════════════════╗"
  echo "║  🚫  GOVERNANCE-SPERRE: Agent-Pattern nicht ausgefüllt!     "
  echo "╚══════════════════════════════════════════════════════════════╝"
  echo ""
  echo "  'Gewähltes Pattern:' ist leer, TBD oder noch Platzhalter."
  echo "  Erlaubte Werte: Solo | Subagent | Agent-Team | Parallel-Subagents"
  echo ""
  exit 1
fi

# ── Check 4: Agent-Team → Team-Komposition vorhanden? ────────────────────────
if echo "$PATTERN" | grep -qi "Agent-Team"; then
  TEAM=$(grep "^\*\*Team-Komposition:\*\*" "$SPEC_FILE" | sed 's/\*\*Team-Komposition:\*\* //' | tr -d '[:space:]' || echo "")
  if [ -z "$TEAM" ] || [ "$TEAM" = "n/a" ] || echo "$TEAM" | grep -q "\["; then
    echo ""
    echo "╔══════════════════════════════════════════════════════════════╗"
    echo "║  🚫  GOVERNANCE-SPERRE: Team-Komposition fehlt!             "
    echo "╚══════════════════════════════════════════════════════════════╝"
    echo ""
    echo "  Pattern 'Agent-Team' gewählt aber Team-Komposition ist leer."
    echo "  Beispiel: Lead (Sonnet) + Explore (Haiku) + Plan (Sonnet)"
    echo "  Eintragen: **Team-Komposition:** in specs/${ISSUE}.md"
    echo ""
    exit 1
  fi
fi

exit 0
```

**Aktivierung in `.claude/settings.json`:**
```json
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Bash",
        "hooks": [
          {
            "type": "command",
            "command": "bash {{PROJECT_PATH}}/.claude/hooks/spec-gate.sh"
          }
        ]
      }
    ]
  }
}
```

> **Anpassen für neues Projekt:** `PROJECT_ROOT` wird per `git rev-parse` automatisch gesetzt.
> Nur der `PROJECT_PATH` Platzhalter in `settings.json` muss mit dem absoluten Projektpfad ersetzt werden.

---

## pre-edit-bodyguard.sh — Layer 0 (BOO-86)

Layer-0-Gate: Ein Claude-Code-**PreToolUse-Hook** mit Matcher `Edit|Write|MultiEdit`, der unsichere Muster (Secrets, `eval`, abgeschaltete TLS-Pruefung, SQL-Konkatenation) abfaengt, **bevor** die KI sie auf die Platte schreibt. Geschwister-Hook zu `spec-gate.sh` — waehrend spec-gate.sh auf `Bash`/`git commit` feuert (also erst beim Commit greift), sitzt der Bodyguard eine Stufe frueher: direkt am Schreibvorgang.

**Muster-Schichtung:**
- Framework-Basis unter `.claude/hooks/bodyguard/patterns/*.yml` — `_universal.yml` (Secrets, sprachunabhaengig) + `gate-configs.yml` (Quality-Gate-Aufweichung, sprachunabhaengig, **immer geladen** — BOO-176) + sprachspezifische Sets (`python.yml`, `javascript.yml`, `java.yml`, `c-cpp.yml`, anhand der Datei-Endung gewaehlt).
- Optionales Projekt-Overlay `.claude/bodyguard.local.yml` — wird zuletzt geladen und uebersteuert/ergaenzt die Basis per `name`. Kundeneigen, ueberlebt Framework-Updates.

**Quality-Gate-Schutz (BOO-176):** `gate-configs.yml` flaggt verdaechtige Regel-Deaktivierung / Schwellen-Edits (breites `eslint-disable`, `@ts-nocheck`, nacktes `# noqa` / `# type: ignore`, Suite-weites Test-Skip, PHPStan-`level:`, Coverage-Schwellen) schon beim Schreiben — als `warn`, damit der Agent die Messlatte nicht klammheimlich absenkt. Den harten Human-Review-Block bei Aenderung an Gate-Config-**Dateien** (eslint/ruff/pyproject/semgrep/phpstan/coverage/jest/vitest/sonar) liefert zusaetzlich `.claude/sensitive-paths.json` (Gruppe „Gate-Config / Quality-Threshold"). Der echte Alt→Neu-Schwellen-Vergleich ist Sache der Post-Story-Gate-Assertion, nicht dieses Hooks.

**Verhalten:**
- Default: **Warnung** (low-false-positive, keine Alarm-Muedigkeit) — `warn`-Muster melden auf stderr, blockieren aber nicht.
- `BODYGUARD_STRICT=1`: **Hard-Block** — alle `warn`-Muster werden zu `block` hochgestuft, Exit 1 verhindert den Schreibvorgang.
- `block`-Muster (z.B. AWS-Key, Private-Key-Block) blockieren immer.

Bewusst leichtgewichtig: eine kleine, kuratierte Muster-Menge pro Edit — KEIN voller Semgrep-Lauf (Tiefe bleibt bei Layer 2/3). Muster-Schema (flacher YAML-Subset, vom Mini-Parser im Hook gelesen — kein PyYAML): `name` · `pattern` (Python-Regex) · `sprache` · `quelle` (CWE/OWASP/gitleaks/Semgrep — Pflicht, Audit-Beleg) · `action` (`block|warn`).

> **Skript-Inhalt + alle Muster-Dateien:** siehe `bootstrap/references/file-templates.md` §`hooks/pre-edit-bodyguard.sh (BOO-86 — Layer-0 Edit-Bodyguard)` (kanonische Quelle).

---

## doc-version-sync.sh

Blockiert `git commit` wenn `lib/config.js` mit erhöhter VERSION gestaged ist, aber Dokumentationsdateien (lt. DOC_FILES in config.js) noch auf alter Version stehen.

```bash
#!/bin/bash
# .claude/hooks/doc-version-sync.sh
# Blockiert git commit wenn config.js VERSION erhoeht aber Doku veraltet
# Aktivierung: in .claude/settings.json als PreToolUse-Hook auf Bash-Calls

PROJECT_ROOT=$(git rev-parse --show-toplevel 2>/dev/null || echo ".")
CONFIG_FILE="${PROJECT_ROOT}/lib/config.js"

# Pruefen ob config.js gestaged ist
if ! git diff --cached --name-only | grep -q "lib/config.js"; then
  exit 0  # config.js nicht gestaged → kein Check noetig
fi

# Aktuelle VERSION aus config.js extrahieren
CURRENT_VERSION=$(grep -oP "VERSION\s*=\s*'\K[^']+" "$CONFIG_FILE" 2>/dev/null)
if [ -z "$CURRENT_VERSION" ]; then
  exit 0  # Kein VERSION-Pattern → skip
fi

# Letzte committete VERSION ermitteln
PREV_VERSION=$(git show HEAD:lib/config.js 2>/dev/null | grep -oP "VERSION\s*=\s*'\K[^']+" | head -1)

if [ "$CURRENT_VERSION" = "$PREV_VERSION" ]; then
  exit 0  # Keine Versionsänderung → kein Check noetig
fi

echo "📋 Versions-Bump erkannt: ${PREV_VERSION} → ${CURRENT_VERSION}"
echo "   Pruefe Dokumentationsdateien..."

# DOC_FILES aus config.js extrahieren (einfacher Pattern-Match)
MISMATCH=0
while IFS= read -r doc_path; do
  if [ -f "${PROJECT_ROOT}/${doc_path}" ]; then
    DOC_VERSION=$(grep -oP '\*\*Version:\*\*\s*\K[\d.]+' "${PROJECT_ROOT}/${doc_path}" 2>/dev/null | head -1)
    if [ -n "$DOC_VERSION" ] && [ "$DOC_VERSION" != "$CURRENT_VERSION" ]; then
      echo "   ⚠️  ${doc_path}: v${DOC_VERSION} (erwartet: v${CURRENT_VERSION})"
      MISMATCH=1
    fi
  fi
done < <(grep -oP "path:\s*'\K[^']+" "$CONFIG_FILE" 2>/dev/null)

if [ $MISMATCH -eq 1 ]; then
  echo ""
  echo "⛔ DOC-VERSION-SYNC: Dokumentationsdateien auf alte Version aktualisieren!"
  echo "   Bypass: git commit --no-verify (nur bei bewusstem Bypass, mit Begruendung im Commit)"
  exit 1
fi

echo "✓ Alle Docs auf Version ${CURRENT_VERSION}"
exit 0
```

---

## coverage-check.sh — Diff-Coverage-Gate (BOO-15, v2 BOO-88)

Misst die Test-Coverage **nur auf neu hinzugefuegten Zeilen** (`git diff --added`) gegen `coverage-final.json` (c8) bzw. `coverage.json` (pytest-cov) — Gesamt-Coverage auf Legacy-Repos waere unfair (Schrader Kap. 3). v2 (BOO-88) zaehlt im Nenner **nur ausfuehrbare Statement-Zeilen** (keine Kommentare/Leerzeilen), damit die Quote nicht faelschlich zu niedrig wird.

- **Nicht als Pre-Commit-Hook verdrahtet** (Tests dauern zu lange) — der Guard laeuft im `/implement`-Coverage-Gate (Schritt 6a) und optional in CI.
- Schwelle env-ueberschreibbar (`COVERAGE_MIN`, Default siehe Skript-Kopf).
- Kanonische Quelle: `bootstrap/references/hooks/coverage-check.sh`; Single-Source + Drift-Guard via `check-hook-sources.sh` (BOO-89).

## Portabilitaet

Alle Hooks haben **keine externen Dependencies** — nur Bash, grep, git, python3. Auch der Bodyguard ist dependency-frei: bash + python3-Stdlib, **kein PyYAML** — die Muster-Dateien werden von einem Mini-Parser im Hook gelesen.

Anpassen fuer neues Projekt:
- Issue-Prefix wird in spec-gate.sh automatisch aus der Commit-Message extrahiert (Pattern `[A-Z]+-\d+`) — keine manuelle Anpassung noetig
- `versionPattern` → je nach Doku-Format anpassen (Standard: `**Version:** X.Y.Z`)

## Harness-Override — settings.json wird ggf. auto-regeneriert

**Wichtig:** Der Claude-Code-Harness kann `.claude/settings.json` bei Permission-Grants auto-regenerieren und Hook-Sektionen dabei stripppen. Das ist ein bekanntes Verhalten.

**Robuster Fallback:** Hooks zusaetzlich in `.claude/settings.local.json` registrieren (gitignored, bleibt stabil):

```json
// {PROJECT_PATH}/.claude/settings.local.json
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Bash",
        "hooks": [
          { "type": "command", "command": "bash {PROJECT_PATH}/.claude/hooks/spec-gate.sh" },
          { "type": "command", "command": "bash {PROJECT_PATH}/.claude/hooks/doc-version-sync.sh" }
        ]
      },
      {
        "matcher": "Edit|Write|MultiEdit",
        "hooks": [
          { "type": "command", "command": "bash {PROJECT_PATH}/.claude/hooks/pre-edit-bodyguard.sh" }
        ]
      }
    ]
  }
}
```

Settings laden in der Reihenfolge: user → project → local. `settings.local.json` hat also Prioritaet und ueberlebt Harness-Regeneration.

Der Bootstrap-Skill legt **beide** an — `settings.json` als primaere Registrierung (fuer Team-Nutzung, gitted) und `settings.local.json` als Fallback (lokal, gitignored).

`.gitignore` wird um `.claude/settings.local.json` erweitert.

## Optional: orphan-check.sh

Wenn in Block C (Doku-Architektur) die Hub-Auto-Verlinkung aktiviert wurde, installiert der Bootstrap-Skill einen dritten Hook `orphan-check.sh`, der pre-commit prueft ob jede neue `*.md` im `ARCHITECTURE_DESIGN.md §9 Referenzen`-Block eingetragen ist.

```bash
#!/bin/bash
# orphan-check.sh — blockiert commit wenn neue *.md nicht im Hub §9 registriert

set -euo pipefail

PROJECT_ROOT=$(git rev-parse --show-toplevel 2>/dev/null || echo ".")
HUB="${PROJECT_ROOT}/ARCHITECTURE_DESIGN.md"

INPUT=$(cat)
CMD=$(echo "$INPUT" | python3 -c "
import sys, json
try:
    d = json.load(sys.stdin)
    print(d.get('tool_input', {}).get('command', ''))
except:
    print('')
" 2>/dev/null || echo "")

if ! echo "$CMD" | grep -qE 'git commit'; then
  exit 0
fi

if [ ! -f "$HUB" ]; then
  exit 0  # Kein Hub → kein Check
fi

# Neue .md-Files im Staging.
# Work-Item-Docs haben eigene Indizes (Backlog-README / links.spec im Record) und brauchen
# keinen Hub-Eintrag — sonst erzwingt der Hook fuer jede Story/jeden Record einen kuenstlichen
# §9-Eintrag. Default nimmt specs/<PREFIX>-<NUM>.md und docs/project/backlog/record-*.md aus;
# ueber ORPHAN_EXCLUDE (Env) ueberschreibbar fuer projekt-eigene Konventionen.
ORPHAN_EXCLUDE="${ORPHAN_EXCLUDE:-^(docs/project/backlog/record-.*\.md|specs/[A-Z]+-[0-9]+\.md)$}"
NEW_MDS=$(git diff --cached --name-only --diff-filter=A \
  | grep -E '\.md$' \
  | grep -vE "$ORPHAN_EXCLUDE" || true)

if [ -z "$NEW_MDS" ]; then
  exit 0
fi

ORPHANS=""
while IFS= read -r md; do
  base=$(basename "$md")
  if ! grep -q "$base" "$HUB"; then
    ORPHANS="${ORPHANS}\n  - $md"
  fi
done <<< "$NEW_MDS"

if [ -n "$ORPHANS" ]; then
  echo ""
  echo "⛔ ORPHAN-CHECK: Neue MD-Files nicht im Hub §9 Referenzen:"
  echo -e "$ORPHANS"
  echo ""
  echo "  Regel: ARCHITECTURE_DESIGN.md ist Hub — alle neuen Docs muessen dort verlinkt sein."
  echo "  Bitte §9 Referenzen ergaenzen, dann erneut committen."
  exit 1
fi

exit 0
```

## Optional: raw-pii-guard.py (PII-in-Logs-Guard, BOO-93)

Ein **optionaler** statischer AST-Check, der meldet, wenn Quellcode ein PII-tragendes Feld
in eine Log-/Audit-Senke (`log.*()`, `logger.*()`, `audit.*()`, `logging.*()`) gibt — als
verbotenes Keyword-Argument, Attribut-Lesezugriff oder Variablen-Name (`original_value`,
`plaintext`, `raw_value` …). Klartext-PII in Logs ist ein faktisches Datenleck (DSGVO Art. 5/32);
der Layer-0-Bodyguard (BOO-86) deckt Secrets/eval/TLS/SQL ab, **nicht** Log-Senken.

Eigenschaften: **AST statt Regex** (ignoriert Kommentare/Strings, kaum Fehlalarme),
**dependency-frei** (nur python3-Stdlib), **Default = Warnung** (Hard-Block nur via `--strict`
bzw. `STRICT=1` — konsistent mit BOO-86 gegen Alarm-Muedigkeit). Fuer Projekte ohne PII einfach
inaktiv lassen.

**Aktivieren** (opt-in): Die kanonische Quelle liegt unter
`bootstrap/references/hooks/raw-pii-guard.py` (Single-Source). Per Migration scaffolden:

```bash
bash bootstrap/scripts/migrate-to-v2.sh --issue BOO-93   # kopiert nach .claude/hooks/raw-pii-guard.py
```

**Lokal (Pre-Commit):** auf die gestageten `*.py` anwenden (ohne Argumente erkennt der Guard
die gestageten Dateien selbst):

```bash
python3 .claude/hooks/raw-pii-guard.py --strict   # Treffer blockt den Commit
```

**Projekt-Overlay** (optional) `.claude/raw-pii-guard.local` — ein Eintrag pro Zeile,
`#`-Kommentare; Praefix `sink:` fuer zusaetzliche Senken, sonst zusaetzliches verbotenes Feld:

```
# projekt-spezifische verbotene Felder
iban_plain
card_pan
sink:audit_trail
```

**CI (optional)** — `.github/workflows/raw-pii-guard.yml` (opt-in, blockt den PR bei Treffer):

```yaml
name: raw-pii-guard
on:
  pull_request:
    paths: ['**/*.py']
  push:
    branches: [main]
    paths: ['**/*.py']
jobs:
  raw-pii-guard:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with: { python-version: '3.x' }
      - name: PII-in-Logs-Guard
        run: |
          files=$(git ls-files '*.py')
          [ -z "$files" ] && exit 0
          python3 .claude/hooks/raw-pii-guard.py --strict $files
```

Selbsttest: `python3 .claude/hooks/raw-pii-guard.py --self-test`. Querverweis: dpo-Skill
(`dpo/references/privacy-patterns.md`) beschreibt die Review-Guidance zu PII-in-Logs — dieser
Guard ist die optionale automatische Enforcement-Schicht dazu.

**Ruff-Kompatibilitaet (BOO-95):** Die kanonische `raw-pii-guard.py` ist gegen ein striktes
Ruff-Profil (`line-length 100`, `select = E,F,S`) sauber — eine `per-file-ignore`-Ausnahme im
Downstream-Projekt ist **nicht** noetig. Das Framework lintet die Quelle selbst via CI
(`.github/workflows/ruff-hooks.yml`, Profil `bootstrap/references/hooks/ruff.toml`).

## anti-placeholder-check.py — Anti-Platzhalter-Check fuer Test-Dateien (BOO-177)

Ein gezielter, **deterministischer** Check **nur auf Test-Dateien** (KEIN Linter), der Tests
flaggt, die die Coverage-Zahl heben, ohne etwas zu testen: triviale/leere Assertions
(`expect(true).toBe(true)`, `assert True`, `assert 1 == 1`, leerer Testkoerper) und
unbegruendete Skips (`it.skip`/`xit`/`@pytest.mark.skip` ohne `reason=`/Begruendungskommentar).
Gleiches Grundproblem wie BOO-176 ("Agent gamed das Gate"), hier auf der Test-Ebene.

Eigenschaften: **Python-AST** (wie `raw-pii-guard.py`, ignoriert Kommentare/Strings) +
zeilen-basierte **JS/TS-Heuristik**, **dependency-frei** (nur python3-Stdlib), **Default = Warnung**
(Hard-Block via `--strict` bzw. `STRICT=1`). Erkennt Test-Dateien an `*.test.{js,ts,jsx,tsx}`,
`*.spec.{js,ts}`, `test_*.py`, `*_test.py`, `tests/**` (Jest/Vitest- und pytest-Konventionen).

**Aktivieren:** Die kanonische Quelle liegt unter
`bootstrap/references/hooks/anti-placeholder-check.py` (Single-Source). Per Migration scaffolden:

```bash
bash bootstrap/scripts/migrate-to-v2.sh --issue BOO-177   # kopiert nach .claude/hooks/anti-placeholder-check.py
```

**Test-Gate (Standard-Verdrahtung):** Wird vom `/implement`-Skill in Schritt **6a-quint**
(nach dem Coverage-Lauf) aufgerufen — die geaenderten Test-Dateien aus `git diff --cached`
werden im Strict-Modus geprueft; jeder Treffer ist ein Gate-Fail:

```bash
python3 .claude/hooks/anti-placeholder-check.py --strict   # ohne Argumente: gestagete Test-Dateien
```

**Projekt-Allowlist** (optional) `.claude/anti-placeholder-check.local` — ein Glob pro Zeile,
`#`-Kommentare; Praefix `path:` deklariert zusaetzliche Test-Pfade, sonst wird der Glob von der
Pruefung ausgenommen:

```
# generierte Test-Fixtures ausnehmen
**/__generated__/*.test.ts
# zusaetzliches Test-Verzeichnis als Test-Pfad behandeln
path:spec/
```

Selbsttest: `python3 .claude/hooks/anti-placeholder-check.py --self-test`. Querverweis:
Coverage-Gate (`coverage-check.sh`, BOO-15) misst die *Menge* getesteten Codes — dieser Check
sichert die *Qualitaet* der Tests; beide laufen im selben Test-Gate (Schritt 6a).

**Ruff-Kompatibilitaet (BOO-95):** Die kanonische `anti-placeholder-check.py` ist gegen dasselbe
strikte Ruff-Profil (`line-length 100`, `select = E,F,S`) sauber — das Framework lintet die Quelle
selbst via CI (`.github/workflows/ruff-hooks.yml`, Profil `bootstrap/references/hooks/ruff.toml`).
