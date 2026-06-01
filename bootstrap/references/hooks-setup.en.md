# Hook Templates — Governance Enforcement

These hooks enforce the core governance rules at the machine level.
Both hooks live under `.claude/hooks/` and are activated via Claude Code `settings.json`.

Important: in INTENTRON, "hook" first means a **coding/runtime hook** of the active AI tool, not necessarily a native Git hook in `.git/hooks/`.

| Layer | Purpose | Examples |
|-------|---------|----------|
| AI runtime hook | Blocks risky tool calls while work is happening | Claude Code `PreToolUse` → `pre-edit-bodyguard.sh` (`Edit|Write`), Codex `.codex/hooks.json` |
| Local Git hook | Optional protection directly before commit/push | `.git/hooks/pre-commit`, `.git/hooks/commit-msg` |
| CI gate | Independent proof on GitHub/GitLab/Azure | ESLint/Ruff, Semgrep, tests, coverage, Sonar |

Bootstrap may optionally mirror rules into Git hooks, but the framework obligation lives in the project contract: `CONVENTIONS.md` describes active gates, runtime hooks enforce early, CI proves independently.

---

## spec-gate.sh

Blocks `git commit` with an issue reference (e.g. `ISSUE-42`) when:
1. no spec file `specs/ISSUE-42.md` exists
2. the spec file has no filled `## Agent-Pattern` field
3. pattern = `Agent-Team` but no team composition is given

```bash
#!/bin/bash
# ─────────────────────────────────────────────────────────────────────────────
#  SPEC-GATE — Governance hook
#  Blocks git commit when spec file is missing or Agent-Pattern is not filled
#
#  Claude Code PreToolUse hook (Bash)
#  Input: JSON via stdin: {"tool_input": {"command": "..."}}
#  Exit 1 → tool call blocked | Exit 0 → allowed
# ─────────────────────────────────────────────────────────────────────────────

set -euo pipefail

PROJECT_ROOT=$(git rev-parse --show-toplevel 2>/dev/null || echo ".")

# Parse JSON → extract command
INPUT=$(cat)
CMD=$(echo "$INPUT" | python3 -c "
import sys, json
try:
    d = json.load(sys.stdin)
    print(d.get('tool_input', {}).get('command', ''))
except:
    print('')
" 2>/dev/null || echo "")

# Only check git commit commands
if ! echo "$CMD" | grep -qE 'git commit'; then
  exit 0
fi

# Extract ISSUE-XXX from commit message (e.g. PROJ-42, ISSUE-123)
ISSUE=$(echo "$CMD" | grep -oP '[A-Z]+-\d+' | head -1 || echo "")
if [ -z "$ISSUE" ]; then
  exit 0  # No issue referenced → no gate
fi

# ── Check 1: spec file present? ────────────────────────────────────────────
SPEC_FILE="${PROJECT_ROOT}/specs/${ISSUE}.md"
if [ ! -f "$SPEC_FILE" ]; then
  echo ""
  echo "╔══════════════════════════════════════════════════════════════╗"
  echo "║  🚫  GOVERNANCE BLOCK: specs/${ISSUE}.md missing!           "
  echo "╚══════════════════════════════════════════════════════════════╝"
  echo ""
  echo "  Commit with ${ISSUE} is BLOCKED."
  echo "  Rule: NEVER change code without a spec file"
  echo ""
  echo "  Next steps:"
  echo "  1. Read specs/TEMPLATE.md"
  echo "  2. Create + fill specs/${ISSUE}.md"
  echo "  3. git add specs/${ISSUE}.md && git commit -m 'docs: specs/${ISSUE}.md'"
  echo ""
  exit 1
fi

# ── Check 2: Agent-Pattern section present? ────────────────────────────────
if ! grep -q "## Agent-Pattern" "$SPEC_FILE"; then
  echo ""
  echo "╔══════════════════════════════════════════════════════════════╗"
  echo "║  🚫  GOVERNANCE BLOCK: Agent-Pattern missing in spec!       "
  echo "╚══════════════════════════════════════════════════════════════╝"
  echo ""
  echo "  Commit with ${ISSUE} is BLOCKED."
  echo "  Rule: every spec needs a ## Agent-Pattern section"
  echo ""
  echo "  Next steps:"
  echo "  1. Open specs/${ISSUE}.md"
  echo "  2. Insert the ## Agent-Pattern section from specs/TEMPLATE.md"
  echo "  3. Fill chosen pattern + rationale"
  echo ""
  exit 1
fi

# ── Check 3: chosen pattern not empty/TBD/placeholder? ─────────────────────
PATTERN=$(grep "^\*\*Chosen pattern:\*\*\|^\*\*Gewähltes Pattern:\*\*" "$SPEC_FILE" | sed 's/\*\*[A-Za-zäö ]*:\*\* //' | tr -d '[:space:]' || echo "")
if [ -z "$PATTERN" ] || [ "$PATTERN" = "TBD" ] || echo "$PATTERN" | grep -q "\["; then
  echo ""
  echo "╔══════════════════════════════════════════════════════════════╗"
  echo "║  🚫  GOVERNANCE BLOCK: Agent-Pattern not filled!            "
  echo "╚══════════════════════════════════════════════════════════════╝"
  echo ""
  echo "  'Chosen pattern:' is empty, TBD, or still a placeholder."
  echo "  Allowed values: Solo | Subagent | Agent-Team | Parallel-Subagents"
  echo ""
  exit 1
fi

# ── Check 4: Agent-Team → team composition present? ────────────────────────
if echo "$PATTERN" | grep -qi "Agent-Team"; then
  TEAM=$(grep "^\*\*Team composition:\*\*\|^\*\*Team-Komposition:\*\*" "$SPEC_FILE" | sed 's/\*\*[A-Za-zäö ]*:\*\* //' | tr -d '[:space:]' || echo "")
  if [ -z "$TEAM" ] || [ "$TEAM" = "n/a" ] || echo "$TEAM" | grep -q "\["; then
    echo ""
    echo "╔══════════════════════════════════════════════════════════════╗"
    echo "║  🚫  GOVERNANCE BLOCK: team composition missing!            "
    echo "╚══════════════════════════════════════════════════════════════╝"
    echo ""
    echo "  Pattern 'Agent-Team' chosen but team composition is empty."
    echo "  Example: Lead (Sonnet) + Explore (Haiku) + Plan (Sonnet)"
    echo "  Fill in: **Team composition:** in specs/${ISSUE}.md"
    echo ""
    exit 1
  fi
fi

exit 0
```

**Activation in `.claude/settings.json`:**
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

> **Adapt for new project:** `PROJECT_ROOT` is set automatically via `git rev-parse`.
> Only the `PROJECT_PATH` placeholder in `settings.json` must be replaced with the absolute project path.

---

## pre-edit-bodyguard.sh — Layer 0 (BOO-86)

Layer-0 gate: a Claude Code **PreToolUse hook** with matcher `Edit|Write|MultiEdit` that catches unsafe patterns (secrets, `eval`, disabled TLS verification, SQL concatenation) **before** the AI writes them to disk. Sibling hook to `spec-gate.sh` — while spec-gate.sh fires on `Bash`/`git commit` (i.e. only at commit time), the bodyguard sits one stage earlier: directly at the write operation.

**Pattern layering:**
- Framework base under `.claude/hooks/bodyguard/patterns/*.yml` — `_universal.yml` (secrets, language-agnostic) + language-specific sets (`python.yml`, `javascript.yml`, `java.yml`, `c-cpp.yml`, selected by file extension).
- Optional project overlay `.claude/bodyguard.local.yml` — loaded last, overrides/extends the base by `name`. Project-owned, survives framework updates.

**Behavior:**
- Default: **warning** (low false positive, no alarm fatigue) — `warn` patterns report to stderr but do not block.
- `BODYGUARD_STRICT=1`: **hard block** — all `warn` patterns are escalated to `block`, exit 1 prevents the write.
- `block` patterns (e.g. AWS key, private-key block) always block.

Deliberately lightweight: a small, curated pattern set per edit — NOT a full Semgrep run (depth stays at layers 2/3). Pattern schema (flat YAML subset, read by a mini parser in the hook — no PyYAML): `name` · `pattern` (Python regex) · `language` · `source` (CWE/OWASP/gitleaks/Semgrep — mandatory, audit evidence) · `action` (`block|warn`).

> **Script body + all pattern files:** see `bootstrap/references/file-templates.md` §`hooks/pre-edit-bodyguard.sh (BOO-86 — Layer-0 Edit-Bodyguard)` (canonical source).

---

## doc-version-sync.sh

Blocks `git commit` when `lib/config.js` is staged with an increased VERSION but documentation files (listed in DOC_FILES inside config.js) are still on the old version.

```bash
#!/bin/bash
# .claude/hooks/doc-version-sync.sh
# Blocks git commit when config.js VERSION is raised but docs are outdated
# Activation: in .claude/settings.json as a PreToolUse hook on Bash calls

PROJECT_ROOT=$(git rev-parse --show-toplevel 2>/dev/null || echo ".")
CONFIG_FILE="${PROJECT_ROOT}/lib/config.js"

# Check whether config.js is staged
if ! git diff --cached --name-only | grep -q "lib/config.js"; then
  exit 0  # config.js not staged → no check needed
fi

# Extract current VERSION from config.js
CURRENT_VERSION=$(grep -oP "VERSION\s*=\s*'\K[^']+" "$CONFIG_FILE" 2>/dev/null)
if [ -z "$CURRENT_VERSION" ]; then
  exit 0  # No VERSION pattern → skip
fi

# Previous committed VERSION
PREV_VERSION=$(git show HEAD:lib/config.js 2>/dev/null | grep -oP "VERSION\s*=\s*'\K[^']+" | head -1)

if [ "$CURRENT_VERSION" = "$PREV_VERSION" ]; then
  exit 0  # No version change → no check needed
fi

echo "📋 Version bump detected: ${PREV_VERSION} → ${CURRENT_VERSION}"
echo "   Checking documentation files..."

# Extract DOC_FILES from config.js (simple pattern match)
MISMATCH=0
while IFS= read -r doc_path; do
  if [ -f "${PROJECT_ROOT}/${doc_path}" ]; then
    DOC_VERSION=$(grep -oP '\*\*Version:\*\*\s*\K[\d.]+' "${PROJECT_ROOT}/${doc_path}" 2>/dev/null | head -1)
    if [ -n "$DOC_VERSION" ] && [ "$DOC_VERSION" != "$CURRENT_VERSION" ]; then
      echo "   ⚠️  ${doc_path}: v${DOC_VERSION} (expected: v${CURRENT_VERSION})"
      MISMATCH=1
    fi
  fi
done < <(grep -oP "path:\s*'\K[^']+" "$CONFIG_FILE" 2>/dev/null)

if [ $MISMATCH -eq 1 ]; then
  echo ""
  echo "⛔ DOC-VERSION-SYNC: update documentation files to the new version!"
  echo "   Bypass: git commit --no-verify (only for deliberate bypass, with justification in commit)"
  exit 1
fi

echo "✓ All docs on version ${CURRENT_VERSION}"
exit 0
```

---

## Portability

All hooks have **no external dependencies** — only Bash, grep, git, python3. The bodyguard is dependency-free too: bash + python3 stdlib, **no PyYAML** — the pattern files are read by a mini parser inside the hook.

Adapt for a new project:
- Issue prefix is auto-extracted from the commit message in spec-gate.sh (pattern `[A-Z]+-\d+`) — no manual adjustment required
- `versionPattern` → adapt to the doc format (standard: `**Version:** X.Y.Z`)

## Harness override — settings.json may be auto-regenerated

**Important:** The Claude Code harness can auto-regenerate `.claude/settings.json` when permissions are granted, and may strip hook sections. This is a known behavior.

**Robust fallback:** Also register hooks in `.claude/settings.local.json` (gitignored, stays stable):

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

Settings load order: user → project → local. `settings.local.json` takes precedence and survives harness regeneration.

The bootstrap skill creates **both** — `settings.json` as primary registration (team-wide, committed) and `settings.local.json` as fallback (local, gitignored).

`.gitignore` is extended to include `.claude/settings.local.json`.

## Optional: orphan-check.sh

If Block C (doc architecture) activated hub auto-linking, the bootstrap skill installs a third hook `orphan-check.sh` that checks pre-commit whether every new `*.md` is registered in `ARCHITECTURE_DESIGN.md §9 References`.

```bash
#!/bin/bash
# orphan-check.sh — blocks commit if new *.md is not registered in hub §9

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
  exit 0
fi

# New .md files in staging.
# Work-item docs have their own indexes (backlog README / links.spec in the record) and need
# no hub entry — otherwise the hook forces an artificial §9 entry for every story/record.
# Default exempts specs/<PREFIX>-<NUM>.md and docs/project/backlog/record-*.md;
# override via ORPHAN_EXCLUDE (env) for project-specific conventions.
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
  echo "⛔ ORPHAN-CHECK: New MD files not in hub §9 references:"
  echo -e "$ORPHANS"
  echo ""
  echo "  Rule: ARCHITECTURE_DESIGN.md is the hub — all new docs must be linked there."
  echo "  Add them to §9 References, then re-commit."
  exit 1
fi

exit 0
```

## Optional: raw-pii-guard.py (PII-in-logs guard, BOO-93)

An **optional** static AST check that flags source code passing a PII-bearing field into a
log/audit sink (`log.*()`, `logger.*()`, `audit.*()`, `logging.*()`) — as a forbidden keyword
argument, attribute read, or variable name (`original_value`, `plaintext`, `raw_value` …).
Cleartext PII in logs is a real data leak (GDPR Art. 5/32); the Layer-0 bodyguard (BOO-86)
covers secrets/eval/TLS/SQL, **not** log sinks.

Properties: **AST not regex** (ignores comments/strings, few false positives),
**dependency-free** (python3 stdlib only), **default = warning** (hard block only via `--strict`
or `STRICT=1` — consistent with BOO-86 against alarm fatigue). For projects without PII, just
leave it inactive.

**Enable** (opt-in): The canonical source lives at
`bootstrap/references/hooks/raw-pii-guard.py` (single source). Scaffold via migration:

```bash
bash bootstrap/scripts/migrate-to-v2.sh --issue BOO-93   # copies to .claude/hooks/raw-pii-guard.py
```

**Local (pre-commit):** run on staged `*.py` (with no arguments the guard detects staged files
itself):

```bash
python3 .claude/hooks/raw-pii-guard.py --strict   # a hit blocks the commit
```

**Project overlay** (optional) `.claude/raw-pii-guard.local` — one entry per line, `#` comments;
prefix `sink:` for additional sinks, otherwise an additional forbidden field:

```
# project-specific forbidden fields
iban_plain
card_pan
sink:audit_trail
```

**CI (optional)** — `.github/workflows/raw-pii-guard.yml` (opt-in, blocks the PR on a hit):

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
      - name: PII-in-logs guard
        run: |
          files=$(git ls-files '*.py')
          [ -z "$files" ] && exit 0
          python3 .claude/hooks/raw-pii-guard.py --strict $files
```

Self-test: `python3 .claude/hooks/raw-pii-guard.py --self-test`. Cross-reference: the dpo skill
(`dpo/references/privacy-patterns.md`) holds the PII-in-logs review guidance — this guard is the
optional automatic enforcement layer for it.
