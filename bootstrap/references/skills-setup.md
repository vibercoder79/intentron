# Skills Setup — Neue Projekt-Installation

Skills werden aus dem offiziellen GitHub-Repo via `git clone` in einen Temp-Ordner geholt und in `{PROJECT_PATH}/.claude/skills/` kopiert. Kein Symlink auf VPS-Pfade, kein globales `/root/.claude/skills/`.

## Repo-Struktur (BOO-74/121)

**Source-Garantie:** Alle **Bundle-Skills** (inkl. `intent`) kommen **immer aus dem `intentron`-Repo** — **nie** aus `claudecodeskills`. Sie liegen flach als Top-Level-Ordner (keine `intentron/`-Verschachtelung mehr — das war die alte Pre-BOO-74-Struktur):

- **`$SKILL_SRC/<skill>/`** (intentron-Clone) — alle Bundle-Skills: `architecture-review`, `backlog`, `bootstrap`, `cloud-system-engineer`, `dpo`, `grafana`, `ideation`, `implement`, `intent`, `pitch`, `security-architect`, `sprint-review`, `visualize`.
- **`claudecodeskills` (separater, optionaler Clone)** — **nur** die Allzweck-Skills `research`, `design-md-generator`, `setup-checklist`, `skill-creator`. **Kein** Bundle-Skill.

> **Master vs. Mirror:** `dpo` und `security-architect` werden in `claudecodeskills` gepflegt (Master), liegen aber als **Mirror** im intentron-Bundle — Bootstrap installiert sie aus intentron. **Regression-Schutz:** `bootstrap/scripts/check-skill-sources.sh` (CI: `skill-sources.yml`) verifiziert Mirror-Vollstaendigkeit + dass kein Bundle-Skill gegen `claudecodeskills` gesourced wird. **Operator-Hinweis:** den lokalen `bootstrap`-Skill aktuell halten (`git pull` im intentron-Klon), sonst greifen veraltete Source-Pfade (Pre-BOO-74).

## Installation (Standard-Flow)

```bash
# Temp-Ordner anlegen
SKILL_SRC=$(mktemp -d)

# Aktuelles Skills-Repo klonen (shallow)
git clone --depth 1 https://github.com/vibercoder79/claudecodeskills "$SKILL_SRC"

# Skills-Verzeichnis im Projekt anlegen
cd {PROJECT_PATH}
mkdir -p .claude/skills

# Sub-Skills unter intentron/ im Repo
BOOTSTRAPPING_SUBSKILLS="architecture-review backlog cloud-system-engineer grafana ideation implement sprint-review visualize"

# Gewaehlte Skills kopieren (Pfad-Mapping beachten)
for skill in ideation implement backlog; do
  if echo "$BOOTSTRAPPING_SUBSKILLS" | grep -qw "$skill"; then
    SRC_PATH="$SKILL_SRC/intentron/$skill"
  else
    SRC_PATH="$SKILL_SRC/$skill"
  fi
  cp -R "$SRC_PATH" ".claude/skills/$skill"
done

# Temp-Ordner aufraeumen
rm -rf "$SKILL_SRC"
```

## Verfuegbare Skills

| Skill | Beschreibung | Tier |
|-------|-------------|------|
| `ideation` | Deep Research + User Story Erstellung | Minimum |
| `implement` | Implementierungs-Workflow mit Governance-Gates | Minimum |
| `backlog` | Sprint Planning + Backlog-Uebersicht | Minimum |
| `intent` | Pipeline-Einstieg: Intent-Erfassung (Perceive der 4P) | Minimum |
| `architecture-review` | Architektur-Review (Standard-Dimensionen + aktivierte Add-ons) | Standard |
| `sprint-review` | Periodisches Audit + **Learning-Loop-Eintrag** (siehe `learning-loop.md`) | Standard |
| `research` | Deep Research via WebSearch + Perplexity | Standard |
| `security-architect` | Security-Review (STRIDE/OWASP) | Standard |
| `skill-creator` | Neue Skills erstellen + paketieren | Standard |
| `grafana` | Grafana Dashboard-Entwicklung | Optional |
| `cloud-system-engineer` | VPS-Infrastruktur | Optional |
| `visualize` | Architektur-Diagramme in Miro | Optional |
| `design-md-generator` | DESIGN.md aus Website/PDF extrahieren | Optional |

## Skill-Tier-Auswahl im Bootstrap

```
Welche Skills installieren?
  a) Minimum   (ideation, implement, backlog, intent)
  b) Standard  (+ architecture-review, sprint-review, research, security-architect, skill-creator)
  c) Voll      (alle verfuegbaren)
  d) Manuell   (Operator waehlt einzeln)
```

## Anpassung der installierten Skills

**Generisch (Default):** Skills werden unveraendert aus dem Master-Repo kopiert. Die referenzen sind generisch gehalten (keine Projekt-Annahmen) und funktionieren direkt.

**Projekt-spezifisch (nur bei Bedarf):** Wenn das Projekt domain-spezifische Anpassungen braucht (z.B. Component-Docs-Mapping fuer `implement/references/change-checklist.md`), ist der Weg:

1. Die entsprechende Datei im installierten Skill lokal editieren
2. Die Anpassung als projekt-spezifisch dokumentieren (z.B. in `specs/JAR-XXX.md` die erste Story dazu)
3. Optional: Die Anpassung als Skill-Variante via `/skill-creator` paketieren

**Niemals** Master-Skills direkt aus dem Projekt commiten — der Master-Stand bleibt generisch.

## Update-Strategie

Wenn der Master-Skill ein Update bekommt, kann der Operator im Projekt:

```bash
# Neuen Stand holen
SKILL_SRC=$(mktemp -d)
git clone --depth 1 https://github.com/vibercoder79/claudecodeskills "$SKILL_SRC"

# Pfad im Repo ermitteln (intentron/ vs. Top-Level) — siehe "Repo-Struktur" oben
BOOTSTRAPPING_SUBSKILLS="architecture-review backlog cloud-system-engineer grafana ideation implement sprint-review visualize"
if echo "$BOOTSTRAPPING_SUBSKILLS" | grep -qw "<skill>"; then
  SRC_PATH="$SKILL_SRC/intentron/<skill>"
else
  SRC_PATH="$SKILL_SRC/<skill>"
fi

# Diff anzeigen vor Overwrite
diff -r "$SRC_PATH" ".claude/skills/<skill>"

# Gezielt Updates uebernehmen (nicht stumpf ueberschreiben)
# Operator entscheidet pro File
```

Alternativ: Projekt-spezifische Anpassungen erneut anwenden nach Copy.

## Reihenfolge der Skill-Installation

1. `research` — keine Abhaengigkeiten
2. `ideation` — braucht story-templates (im Skill enthalten)
3. `backlog` — braucht Linear/M365/GitHub-Connector
4. `implement` — braucht `change-checklist.md` + Git
5. `architecture-review` — braucht Dimensionen-Referenz
6. `security-architect` — standalone
7. `sprint-review` — braucht `learning-loop.md` falls Learning-Loop aktiv
8. Optional (Voll-Tier): `grafana`, `cloud-system-engineer`, `visualize`, `design-md-generator`
9. `skill-creator` — standalone

## ISSUE_WRITING_GUIDELINES.md

Wird NICHT aus einem externen Pfad kopiert, sondern aus `references/issue-writing-guidelines-template.md` gerendert (Prefix eingesetzt). Siehe SKILL.md Phase 4.3.

## implement-Skill: Governance-Integration

Der aktuelle `implement`-Skill enthaelt diese Pflichtschritte (werden automatisch aktiv wenn der Skill installiert ist):

| Schritt | Was | Governance-Impact |
|---------|-----|-------------------|
| 3 | Kontext — `ARCHITECTURE_DESIGN.md` Hub + Component-Doc lesen | Hub-first-Navigation |
| 3b | Governance-Validation (8 Dimensionen + Security) | Pflicht vor Plan |
| 3c | Spec-File Gate (spec-gate.sh erzwingt es) | Spec pflichtig |
| 5 | Implementation inkl. T_last Doku-Update | Component-Doc + Hub §9 + `lib/config.js` VERSION bump |
| 6a | Linting-Gate (ESLint/Ruff — 0 Errors Pflicht) | Qualitaets-Gate |

## Learning-Loop-Integration (wenn aktiviert)

Wenn Block D = L1/L2/L3, wird:

- `sprint-review`-Skill um Schritt 7 (Learning-Loop-Eintrag) erweitert — siehe `learning-loop.md`
- `ideation`-Skill um Schritt 0.5 (Learnings-Kontext lesen vor Story-Erstellung) erweitert

Aktivierung: `.learning-loop`-File im Projekt-Root mit Inhalt `L1`, `L2` oder `L3`.

## Sync-Konvention: Vendored-Skills (BOO-74)

Seit BOO-74 (Wave M) liegen `dpo` und `security-architect` als **vendored Bundle-Skills** im `intentron`-Repo. Damit installiert Bootstrap sie aus demselben Repo wie alle anderen Bundle-Skills (Phase 5). Aber: der **Master** dieser zwei Skills bleibt das `claudecodeskills`-Repo.

### Master vs. Mirror

| Rolle | Repo | Pflege |
|-------|------|--------|
| Master | `claudecodeskills` | `publish_skill.py <skill>` — Quelle der Wahrheit, auch fuer Solo-Operatoren ohne Framework |
| Mirror | `intentron` | Vendored 1:1-Kopie (`dpo/`, `security-architect/`), aus der Bootstrap installiert |

### Pflicht bei jedem DPO- oder security-architect-Update

1. Skill lokal in `~/.claude/skills/<skill>/` aendern.
2. `python3 ~/.claude/skills/skill-creator/scripts/publish_skill.py <skill> -m "..."` — aktualisiert den Master in `claudecodeskills` + SecondBrain-Doku.
3. **Mirror nachziehen:** `cp -R ~/.claude/skills/<skill>/ ~/Documents/GitHub/intentron/<skill>/` und im Framework-Repo committen.
4. Verifikation: `diff -rq ~/.claude/skills/<skill>/ ~/Documents/GitHub/intentron/<skill>/` → keine Diff.

### Drift-Risiko

Wird Schritt 3 vergessen, laeuft der Framework-Mirror auf einem aelteren Skill-Stand als der Master. Neue Bootstrap-Laeufe installieren dann die veraltete Version. **Folge-Story (geplant):** `sync_framework_mirror.sh` automatisiert Schritt 3+4 — bis dahin ist es Operator-Pflicht.
