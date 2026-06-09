# Runbook: Neuen Stack/Linter integrieren

> **Zielgruppe:** Operator:in mit einem Projekt-Stack, den das Framework **nicht out-of-the-box abdeckt** (PHP/TYPO3, Java/Kotlin, Go, …) und der trotzdem an dieselben Qualitäts-Gates wie JS/TS und Python angeschlossen werden soll. In unter 30 Minuten, manuell, verifizierbar. EN: [`stack-linter-integrieren.en.md`](stack-linter-integrieren.en.md).

## Wann dieses Runbook?

Der Bootstrap deckt JS/TS und Python mit fertigen Gates ab. Wählt das Onboarding den Pfad `e) Anderes`, bekommst du eine Linter-Hinweistabelle und Guided Discovery — **aber kein automatisches Gate-Setup**. Bewusste Design-Entscheidung: Nicht jede Sprache wird ins Framework eingebaut (Aufblähung). Stattdessen führt dich dieses Runbook **Schritt für Schritt** durch die manuelle Integration — und die **Garantie** kommt nicht aus einem Prompt, sondern aus dem [Verifikations-Schritt](#schritt-7--verifikation-der-zentrale-schritt) (absichtlich Fehler einbauen → Gate muss rot werden).

Dieses Runbook ist zugleich **Prompt-Vorlage**: Du kannst es einem Agenten geben („integriere Stack X nach diesem Runbook") — aber die Abnahme bleibt der manuelle Verifikations-Test, kein Vertrauen in den Agenten.

**Abgrenzung:** Die Schutz-Mechanik der Gate-Configs (Human-Review-Block bei Änderung) ist Thema von BOO-176 — hier nur der **Eintrag-Schritt** ([Schritt 6](#schritt-6--gate-configs-in-sensitive-pathsjson-eintragen-pflicht)). Konzept + Hintergrund stehen im HANDBUCH-Kapitel „Stack-Linter integrieren".

→ Das zentrale End-to-End-Bild der bestehenden Linter-Verdrahtung (JS/TS, Python) zeigt HANDBUCH-Kapitel 8d-quart; dieses Runbook erweitert die Kette um neue Stacks.

## Die kanonische Linter-Tabelle

Die Spalten je Stack — Linter, Formatter, Typecheck, Coverage und die **Gate-Config-Datei(en)**, die du in Schritt 6 schützt. Aus dem Bootstrap-`e)`-Pfad übernommen, nicht neu erfunden:

| Stack | Linter | Formatter | Typecheck | Coverage | Gate-Config-Datei(en) |
|---|---|---|---|---|---|
| JS/TS | ESLint (+ `typescript-eslint`) | Prettier | `tsc --noEmit` | c8 + jest/vitest | `eslint.config.mjs` |
| Python | Ruff (+ Black) | Black | — | pytest-cov | `pyproject.toml` / `ruff.toml` |
| PHP | PHPStan / Psalm + PHP-CS-Fixer | PHP-CS-Fixer | (PHPStan) | PHPUnit `--coverage` | `phpstan.neon` |
| Java / Kotlin | Checkstyle / ktlint + SpotBugs | — | (javac) | JaCoCo | `checkstyle.xml` |
| Go | golangci-lint (+ gofmt) | gofmt | (go vet) | `go test -cover` | `.golangci.yml` |

JS/TS und Python sind bereits abgedeckt — die übrigen Zeilen sind dein Zielzustand. Such deinen Stack in der Tabelle und behalte die **Gate-Config-Datei(en)** im Blick: Sie tauchen in Schritt 1, 6 und 7 wieder auf.

## Die 5 Stellen — Überblick

Einen neuen Stack/Linter integrierst du an genau diesen fünf Stellen. Die Schritte unten arbeiten sie der Reihe nach ab, plus den Pflicht-Brücke-Schritt zu `sensitive-paths.json` und den Verifikations-Schritt.

1. **`.claude/environment.json` → `tools_available`** — Linter + Test-Runner deklarieren, damit `/implement` die Gates kennt.
2. **CI-Workflow** — `.github/workflows/<linter>.yml` analog `eslint.yml`/`semgrep.yml` (Required Status Check).
3. **`.semgrep.yml`-Pack** — Semgrep-Regelsatz für die Sprache (SAST-Gate 6a-bis ist sprachübergreifend).
4. **Coverage-Tool** — stack-eigenes Coverage-Werkzeug ans 6a-quart-Coverage-Gate anbinden.
5. **ADR** in `docs/domain/adrs/` — die Stack-/Linter-Entscheidung festhalten.

---

## Schritt 1 — `.claude/environment.json` → `tools_available` ergänzen

`/implement` liest `tools_available` in einem Schritt-0-Read, statt selbst Detection zu fahren. Trägst du den Linter/Test-Runner nicht ein, **kennt der Skill die neuen Gates nicht** und überspringt sie still. Ergänze die `tools_available`-Sektion um den neuen Stack — Beispiel PHP/TYPO3:

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

`tests` ist der Test-Runner-Schlüssel (`"phpunit"` statt `"vitest"`/`"pytest"`). Den Linter-Schlüssel (`"phpstan": true`) ergänzt du analog zu `eslint`/`semgrep` — er ist der Marker, an dem `/implement` erkennt, dass das Lint-Gate für diesen Stack greift. Schema und Feld-Referenz: [`bootstrap/references/file-templates.md`](../../bootstrap/references/file-templates.md) §`.claude/environment.json`.

> Re-Generierung über `bash .claude/generate-environment-json.sh --force` erkennt nur die abgedeckten Stacks automatisch. Den neuen Linter-Schlüssel **manuell eintragen** und committen — `metadata.created_at` ist die Audit-Spur.

## Schritt 2 — CI-Workflow anlegen

Lege `.github/workflows/<linter>.yml` analog zu `eslint.yml`/`semgrep.yml` an — Layer 3, **Required Status Check** an der geschützten `main`. Konventionen aus den Bestands-Workflows (z.B. [`.github/workflows/ruff-hooks.yml`](../../.github/workflows/ruff-hooks.yml)): `actions/checkout@v4`, **gepinnte** Tool-Version (reproduzierbare Befunde), `pull_request`-Trigger. Konkrete Kopiervorlage: [PHP/TYPO3 unten](#kopiervorlage-phptypo3).

Nach dem Anlegen den Workflow als **Required Status Check** in der Branch-Protection der `main` eintragen (GitHub → Settings → Branches), sonst kann ein roter Lauf gemergt werden.

## Schritt 3 — `.semgrep.yml`-Pack für die Sprache ergänzen

Das SAST-Gate **6a-bis** ist sprachübergreifend, aber Semgrep braucht je Sprache den passenden Regelsatz. Ergänze in `.semgrep.yml` das Pack für deinen Stack über die `p/`-Registry-Packs:

```yaml
rules: []
# Sprach-Packs aus der Semgrep-Registry:
# PHP:   p/php
# Go:    p/golang
# Java:  p/java
# Kotlin:p/kotlin
```

Alternativ beim CI-Lauf direkt: `semgrep --config p/php --config p/r2c-security-audit`. Verwende reale Registry-Pack-Namen (`p/php`, `p/golang`, `p/java`) — keine erfundenen Pack-IDs.

## Schritt 4 — Coverage-Tool ans 6a-quart-Gate anbinden

Das Test-Gate **6a-quart** prüft Diff-Coverage (≥ 80 % Pass). Es braucht pro Stack ein Coverage-Werkzeug, das maschinenlesbare Coverage-Daten liefert. Wähle das stack-eigene Werkzeug aus der Tabelle:

| Stack | Coverage-Kommando | Ausgabe |
|---|---|---|
| PHP | `phpunit --coverage-clover coverage.xml` | Clover-XML |
| Java/Kotlin | JaCoCo (`jacoco.xml`) | JaCoCo-XML |
| Go | `go test -coverprofile=coverage.out ./...` | Go-Coverage-Profil |

Den Coverage-Lauf in denselben CI-Workflow aus Schritt 2 aufnehmen, damit das Gate die Diff-Coverage des neuen Codes sieht. Wie das 6a-quart-Gate Added-Lines mit Coverage korreliert: [`unit-tests.md`](unit-tests.md).

## Schritt 5 — ADR in `docs/domain/adrs/` festhalten

Halte die Stack-/Linter-Entscheidung als ADR fest (Bootstrap-`e)`-Konvention). Das macht nachvollziehbar, **warum** dieses Projekt z.B. PHPStan Level 8 statt Psalm fährt — und ist der Audit-Anker für die Gate-Configs. Format wie die Bestands-ADRs unter [`docs/domain/adrs/`](../domain/adrs/) (Status / Kontext / Entscheidung / Begründung):

```markdown
# ADR: Stack-Integration PHP/TYPO3 — PHPStan Level 8 + PHP-CS-Fixer

- **Status:** akzeptiert (YYYY-MM-DD)
- **Kontext-Quelle:** Stack nicht von Bootstrap abgedeckt (Pfad `e) Anderes`)

## Kontext
Das Projekt ist ein TYPO3-Extension-Stack (PHP 8.x). Bootstrap deckt JS/TS + Python
ab; PHP läuft über den `e)`-Pfad.

## Entscheidung
Linter/Typecheck: **PHPStan Level 8** (`phpstan.neon`). Formatter: **PHP-CS-Fixer**.
Coverage: **PHPUnit** (`--coverage-clover`). Gate-Config: `phpstan.neon` (in
`sensitive-paths.json` geschützt).

## Begründung
PHPStan ist im TYPO3-Ökosystem Standard; Level 8 als ausgewogene Schwelle
(strikt, aber ohne Level-9-Generics-Overhead). Verifiziert per Verifikations-Schritt.
```

---

## Schritt 6 — Gate-Configs in `sensitive-paths.json` eintragen (Pflicht)

> **Brücke zu BOO-176 — nicht überspringen.** Die abgedeckten Stacks (JS/TS, Python) tragen ihre Gate-Config-Patterns bereits in `.claude/sensitive-paths.json`. Für deinen **neuen** Stack greift der Schutz „Messlatte nur Operator" **nur, wenn du die neue Gate-Config-Datei hier nachträgst.** Sonst kann ein Agent z.B. das PHPStan-Level absenken, ohne einen Human-Review-Block auszulösen — er fixt dann nicht den Code, sondern senkt die Messlatte.

Ergänze die Gate-Config-Datei deines Stacks (aus der [Tabelle](#die-kanonische-linter-tabelle)) im `patterns`-Block der Gruppe „Gate-Config / Quality-Threshold". `phpstan.neon` ist im Default-Template schon vorhanden; für andere Stacks nachtragen:

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

Jede Änderung an diesen Dateien löst danach einen Human-Review-Block (`review-ok`) aus. Referenz: [`bootstrap/references/file-templates.md`](../../bootstrap/references/file-templates.md) §`.claude/sensitive-paths.json` (Gruppe „Gate-Config / Quality-Threshold").

---

## Schritt 7 — Verifikation (der zentrale Schritt)

> **Hier kommt die Garantie her, nicht aus einem Prompt.** Ein eingebautes Gate hilft nichts, wenn es bei einem echten Fehler nicht rot wird. Dieser **manuelle Test** beweist, dass die Verkabelung greift — er ist kein Prompt, sondern ein bewusst herbeigeführter Rot-Lauf.

Führe den Test je Gate durch, das du integriert hast (Lint und/oder Typecheck):

1. **Fehler einbauen.** Baue absichtlich einen Lint-/Typ-Fehler in eine reale Quelldatei ein, z.B. für PHP/PHPStan eine typwidrige Zuweisung:
   ```php
   <?php
   function add(int $a, int $b): int {
       return $a . $b; // PHPStan: string statt int zurückgegeben
   }
   ```
2. **Gate muss rot werden.** Push auf einen Branch / öffne den PR → der CI-Workflow aus Schritt 2 **muss fehlschlagen** (Required Status Check rot). Lokal gegengeprüft: `vendor/bin/phpstan analyse` meldet den Fehler.
3. **Fehler entfernen.** Korrigiere die Zeile zurück (`return $a + $b;`).
4. **Gate muss grün werden.** Erneuter Lauf → grün.

Wird das Gate in Schritt 2 **nicht rot**, ist die Verkabelung kaputt: Prüfe `tools_available` (Schritt 1), den CI-Trigger/-Pfad (Schritt 2) und ob der Workflow als Required Status Check eingetragen ist. **Erst wenn der Rot-/Grün-Zyklus sauber durchläuft, ist der Stack integriert.**

---

## Kopiervorlage PHP/TYPO3

Vollständiges, kopierbares Beispiel für einen TYPO3/PHP-Stack — die vier Dateien plus der `sensitive-paths.json`-Eintrag.

**1. `phpstan.neon`** (Gate-Config — Linter + Typecheck):

```neon
parameters:
    level: 8
    paths:
        - src
        - tests
    excludePaths:
        - tests/Fixtures/*
```

**2. `.github/workflows/phpstan.yml`** (CI-Workflow, Required Status Check):

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
      # Version gepinnt fuer reproduzierbare Befunde.
      - name: Dependencies installieren
        run: composer install --no-interaction --no-progress
      - name: PHPStan analysieren
        run: vendor/bin/phpstan analyse --no-progress
```

**3. PHPUnit-Coverage** (ans 6a-quart-Gate, eigener Job oder Schritt):

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
      - name: Tests mit Coverage
        run: vendor/bin/phpunit --coverage-clover coverage.xml
```

**4. `sensitive-paths.json`-Eintrag** (Pflicht, Schritt 6):

```json
{
  "patterns": [
    "**/phpstan.neon",
    "**/phpstan.neon.dist",
    "**/.php-cs-fixer.dist.php"
  ]
}
```

## Kopiervorlage Go (optional)

**`.golangci.yml`** (Gate-Config):

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

Coverage über `go test -coverprofile=coverage.out ./...`; `.golangci.yml` in `sensitive-paths.json` als `**/.golangci.yml` eintragen.

---

## Externe Stack-/Versions-Doku einrouten

Projekt- und versionsspezifisches Wissen (z.B. TYPO3-API-Doku einer bestimmten Major-Version, Framework-eigene Coding-Konventionen) gehört **nicht** hartkodiert ins Runbook, sondern via [`knowledge-onboarding`](../../knowledge-onboarding)-Skill in die Governance-Artefakte. So bekommt der Agent das stack-/versionsspezifische Wissen kontrolliert bereitgestellt (vorschlagen statt blind übernehmen, mit Coverage-Check) — statt es zu erfinden. Trigger: nach dem Bootstrap, wenn Bestands-Doku/Vor-Material zum Stack vorliegt.

---

## Weiterlesen

| Thema | Quelle |
|---|---|
| Operator-Kurzfassung Konzept + die 5 Stellen | HANDBUCH-Kapitel „Stack-Linter integrieren" ([`HANDBUCH.md`](../../HANDBUCH.md)) |
| Schutz-Mechanik der Gate-Configs (Human-Review-Block) | [`specs/BOO-178.md`](../../specs/BOO-178.md) (Abgrenzung BOO-176) |
| Test-Gate 6a-quart, Diff-Coverage, Reports | [`unit-tests.md`](unit-tests.md) |
| `environment.json` / `sensitive-paths.json` Schema | [`bootstrap/references/file-templates.md`](../../bootstrap/references/file-templates.md) |
| Externe Doku einrouten | [`knowledge-onboarding/SKILL.md`](../../knowledge-onboarding/SKILL.md) |
| Begriffe nachschlagen | [`../glossar.md`](../glossar.md) |

---

> *Englische Fassung: [`stack-linter-integrieren.en.md`](stack-linter-integrieren.en.md).*
