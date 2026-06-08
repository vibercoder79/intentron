# Runbook: Integrate a new stack/linter

> **Audience:** Operators with a project stack the framework does **not cover out of the box** (PHP/TYPO3, Java/Kotlin, Go, …) but that should still be wired to the same quality gates as JS/TS and Python. Under 30 minutes, manual, verifiable. DE: [`stack-linter-integrieren.md`](stack-linter-integrieren.md).

## When this runbook?

The bootstrap covers JS/TS and Python with ready-made gates. If onboarding picks the `e) Other` path you get a linter hint table plus guided discovery — **but no automatic gate setup**. Deliberate design decision: not every language is built into the framework (bloat). Instead, this runbook walks you **step by step** through the manual integration — and the **guarantee** comes not from a prompt but from the [verification step](#step-7--verification-the-central-step) (deliberately inject an error → the gate must turn red).

This runbook also doubles as a **prompt template**: you can hand it to an agent ("integrate stack X following this runbook") — but sign-off stays the manual verification test, not trust in the agent.

**Scope:** the protection mechanic of the gate configs (human-review block on change) is the subject of BOO-176 — here only the **entry step** ([step 6](#step-6--register-gate-configs-in-sensitive-pathsjson-mandatory)). Concept and background are in the HANDBUCH chapter "Integrate a new stack/linter".

## The canonical linter table

The columns per stack — linter, formatter, typecheck, coverage, and the **gate-config file(s)** you protect in step 6. Taken from the bootstrap `e)` path, not re-invented:

| Stack | Linter | Formatter | Typecheck | Coverage | Gate-config file(s) |
|---|---|---|---|---|---|
| JS/TS | ESLint (+ `typescript-eslint`) | Prettier | `tsc --noEmit` | c8 + jest/vitest | `eslint.config.mjs` |
| Python | Ruff (+ Black) | Black | — | pytest-cov | `pyproject.toml` / `ruff.toml` |
| PHP | PHPStan / Psalm + PHP-CS-Fixer | PHP-CS-Fixer | (PHPStan) | PHPUnit `--coverage` | `phpstan.neon` |
| Java / Kotlin | Checkstyle / ktlint + SpotBugs | — | (javac) | JaCoCo | `checkstyle.xml` |
| Go | golangci-lint (+ gofmt) | gofmt | (go vet) | `go test -cover` | `.golangci.yml` |

JS/TS and Python are already covered — the remaining rows are your target state. Find your stack in the table and keep an eye on the **gate-config file(s)**: they reappear in steps 1, 6 and 7.

## The 5 places — overview

You integrate a new stack/linter at exactly these five places. The steps below work through them in order, plus the mandatory `sensitive-paths.json` bridge step and the verification step.

1. **`.claude/environment.json` → `tools_available`** — declare linter + test runner so `/implement` knows the gates.
2. **CI workflow** — `.github/workflows/<linter>.yml` analogous to `eslint.yml`/`semgrep.yml` (required status check).
3. **`.semgrep.yml` pack** — Semgrep ruleset for the language (the SAST gate 6a-bis is cross-language).
4. **Coverage tool** — wire the stack's own coverage tool to the 6a-quart coverage gate.
5. **ADR** in `docs/domain/adrs/` — record the stack/linter decision.

---

## Step 1 — Extend `.claude/environment.json` → `tools_available`

`/implement` reads `tools_available` in a step-0 read instead of running detection itself. If you don't register the linter/test runner, **the skill doesn't know the new gates** and silently skips them. Extend the `tools_available` section for the new stack — PHP/TYPO3 example:

```json
{
  "tools_available": {
    "eslint": true,
    "semgrep": true,
    "tests": "phpunit",
    "phpstan": true,
    "sonarqube_ide_plugin": false,
    "sonarqube_cloud": true
  }
}
```

`tests` is the test-runner key (`"phpunit"` instead of `"vitest"`/`"pytest"`). Add the linter key (`"phpstan": true`) analogous to `eslint`/`semgrep` — it is the marker by which `/implement` recognises that the lint gate applies to this stack. Schema and field reference: [`bootstrap/references/file-templates.md`](../../bootstrap/references/file-templates.md) §`.claude/environment.json`.

> Re-generating via `bash .claude/generate-environment-json.sh --force` only auto-detects the covered stacks. Add the new linter key **manually** and commit it — `metadata.created_at` is the audit trail.

## Step 2 — Create the CI workflow

Create `.github/workflows/<linter>.yml` analogous to `eslint.yml`/`semgrep.yml` — layer 3, **required status check** on the protected `main`. Conventions from the existing workflows (e.g. [`.github/workflows/ruff-hooks.yml`](../../.github/workflows/ruff-hooks.yml)): `actions/checkout@v4`, a **pinned** tool version (reproducible findings), `pull_request` trigger. Concrete copy template: [PHP/TYPO3 below](#copy-template-phptypo3).

After creating it, register the workflow as a **required status check** in the branch protection of `main` (GitHub → Settings → Branches), otherwise a red run can be merged.

## Step 3 — Add a `.semgrep.yml` pack for the language

The SAST gate **6a-bis** is cross-language, but Semgrep needs the matching ruleset per language. Add the pack for your stack in `.semgrep.yml` via the `p/` registry packs:

```yaml
rules: []
# Language packs from the Semgrep registry:
# PHP:    p/php
# Go:     p/golang
# Java:   p/java
# Kotlin: p/kotlin
```

Alternatively pass them directly in the CI run: `semgrep --config p/php --config p/r2c-security-audit`. Use real registry pack names (`p/php`, `p/golang`, `p/java`) — no invented pack IDs.

## Step 4 — Wire the coverage tool to the 6a-quart gate

The test gate **6a-quart** checks diff coverage (≥ 80 % pass). It needs a coverage tool per stack that produces machine-readable coverage data. Pick the stack's own tool from the table:

| Stack | Coverage command | Output |
|---|---|---|
| PHP | `phpunit --coverage-clover coverage.xml` | Clover XML |
| Java/Kotlin | JaCoCo (`jacoco.xml`) | JaCoCo XML |
| Go | `go test -coverprofile=coverage.out ./...` | Go coverage profile |

Add the coverage run to the same CI workflow from step 2 so the gate sees the diff coverage of the new code. How the 6a-quart gate correlates added lines with coverage: [`unit-tests.en.md`](unit-tests.en.md).

## Step 5 — Record an ADR in `docs/domain/adrs/`

Record the stack/linter decision as an ADR (bootstrap `e)` convention). This makes it traceable **why** this project runs e.g. PHPStan level 8 instead of Psalm — and is the audit anchor for the gate configs. Format like the existing ADRs under [`docs/domain/adrs/`](../domain/adrs/) (status / context / decision / rationale):

```markdown
# ADR: Stack integration PHP/TYPO3 — PHPStan level 8 + PHP-CS-Fixer

- **Status:** accepted (YYYY-MM-DD)
- **Context source:** stack not covered by bootstrap (path `e) Other`)

## Context
The project is a TYPO3 extension stack (PHP 8.x). Bootstrap covers JS/TS + Python;
PHP runs through the `e)` path.

## Decision
Linter/typecheck: **PHPStan level 8** (`phpstan.neon`). Formatter: **PHP-CS-Fixer**.
Coverage: **PHPUnit** (`--coverage-clover`). Gate config: `phpstan.neon` (protected
in `sensitive-paths.json`).

## Rationale
PHPStan is the standard in the TYPO3 ecosystem; level 8 as a balanced threshold
(strict, but without level-9 generics overhead). Verified via the verification step.
```

---

## Step 6 — Register gate configs in `sensitive-paths.json` (mandatory)

> **Bridge to BOO-176 — do not skip.** The covered stacks (JS/TS, Python) already register their gate-config patterns in `.claude/sensitive-paths.json`. For your **new** stack the "only the operator moves the bar" protection applies **only if you add the new gate-config file here.** Otherwise an agent can e.g. lower the PHPStan level without triggering a human-review block — it then doesn't fix the code, it lowers the bar.

Add your stack's gate-config file (from the [table](#the-canonical-linter-table)) to the `patterns` block of the "Gate-config / quality-threshold" group. `phpstan.neon` is already in the default template; add others for other stacks:

```json
{
  "patterns": [
    "**/eslint.config.*",
    "**/ruff.toml",
    "**/pyproject.toml",
    "**/.semgrep.yml",
    "**/phpstan.neon",
    "**/phpstan.neon.dist",
    "**/.php-cs-fixer.dist.php",
    "**/.golangci.yml",
    "**/checkstyle.xml",
    "**/jacoco.xml"
  ]
}
```

Any change to these files then triggers a human-review block (`review-ok`). Reference: [`bootstrap/references/file-templates.md`](../../bootstrap/references/file-templates.md) §`.claude/sensitive-paths.json` ("Gate-config / quality-threshold" group).

---

## Step 7 — Verification (the central step)

> **This is where the guarantee comes from, not from a prompt.** A wired-in gate is worthless if it doesn't turn red on a real error. This **manual test** proves the wiring holds — it is not a prompt but a deliberately induced red run.

Run the test for each gate you integrated (lint and/or typecheck):

1. **Inject an error.** Deliberately introduce a lint/type error into a real source file, e.g. for PHP/PHPStan a type-mismatched assignment:
   ```php
   <?php
   function add(int $a, int $b): int {
       return $a . $b; // PHPStan: returns string instead of int
   }
   ```
2. **The gate must turn red.** Push to a branch / open the PR → the CI workflow from step 2 **must fail** (required status check red). Cross-checked locally: `vendor/bin/phpstan analyse` reports the error.
3. **Remove the error.** Revert the line (`return $a + $b;`).
4. **The gate must turn green.** Re-run → green.

If the gate does **not** turn red in step 2, the wiring is broken: check `tools_available` (step 1), the CI trigger/path (step 2) and whether the workflow is registered as a required status check. **Only once the red/green cycle runs cleanly is the stack integrated.**

---

## Copy template PHP/TYPO3

Full, copy-paste example for a TYPO3/PHP stack — the four files plus the `sensitive-paths.json` entry.

**1. `phpstan.neon`** (gate config — linter + typecheck):

```neon
parameters:
    level: 8
    paths:
        - src
        - tests
    excludePaths:
        - tests/Fixtures/*
```

**2. `.github/workflows/phpstan.yml`** (CI workflow, required status check):

```yaml
name: phpstan

on:
  push:
    paths:
      - '**.php'
      - 'phpstan.neon'
      - '.github/workflows/phpstan.yml'
  pull_request:

jobs:
  phpstan:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: shivammathur/setup-php@v2
        with:
          php-version: '8.3'
          coverage: none
      # Version pinned for reproducible findings.
      - name: Install dependencies
        run: composer install --no-interaction --no-progress
      - name: Run PHPStan
        run: vendor/bin/phpstan analyse --no-progress
```

**3. PHPUnit coverage** (to the 6a-quart gate, separate job or step):

```yaml
  phpunit:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: shivammathur/setup-php@v2
        with:
          php-version: '8.3'
          coverage: xdebug
      - run: composer install --no-interaction --no-progress
      - name: Tests with coverage
        run: vendor/bin/phpunit --coverage-clover coverage.xml
```

**4. `sensitive-paths.json` entry** (mandatory, step 6):

```json
{
  "patterns": [
    "**/phpstan.neon",
    "**/phpstan.neon.dist",
    "**/.php-cs-fixer.dist.php"
  ]
}
```

## Copy template Go (optional)

**`.golangci.yml`** (gate config):

```yaml
run:
  timeout: 3m
linters:
  enable:
    - govet
    - staticcheck
    - errcheck
    - gofmt
```

**`.github/workflows/golangci-lint.yml`**:

```yaml
name: golangci-lint

on:
  push:
    paths:
      - '**.go'
      - '.golangci.yml'
      - '.github/workflows/golangci-lint.yml'
  pull_request:

jobs:
  golangci:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-go@v5
        with:
          go-version: '1.23'
      - name: golangci-lint
        uses: golangci/golangci-lint-action@v6
        with:
          version: v1.62.2
```

Coverage via `go test -coverprofile=coverage.out ./...`; register `.golangci.yml` in `sensitive-paths.json` as `**/.golangci.yml`.

---

## Routing external stack/version docs

Project- and version-specific knowledge (e.g. the TYPO3 API docs of a particular major version, framework-specific coding conventions) does **not** belong hard-coded in the runbook but routed via the [`knowledge-onboarding`](../../knowledge-onboarding) skill into the governance artifacts. That way the agent gets the stack/version-specific knowledge provided in a controlled way (propose instead of blindly adopt, with a coverage check) — instead of inventing it. Trigger: after the bootstrap, when existing docs / prior material on the stack are available.

---

## Further reading

| Topic | Source |
|---|---|
| Operator short version concept + the 5 places | HANDBUCH chapter "Integrate a new stack/linter" ([`HANDBUCH.en.md`](../../HANDBUCH.en.md)) |
| Protection mechanic of gate configs (human-review block) | [`specs/BOO-178.md`](../../specs/BOO-178.md) (scope vs. BOO-176) |
| Test gate 6a-quart, diff coverage, reports | [`unit-tests.en.md`](unit-tests.en.md) |
| `environment.json` / `sensitive-paths.json` schema | [`bootstrap/references/file-templates.en.md`](../../bootstrap/references/file-templates.en.md) |
| Routing external docs | [`knowledge-onboarding/SKILL.md`](../../knowledge-onboarding/SKILL.md) |
| Look up terms | [`../glossar.en.md`](../glossar.en.md) |

---

> *German version: [`stack-linter-integrieren.md`](stack-linter-integrieren.md).*
