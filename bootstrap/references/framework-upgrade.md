# Framework-Upgrade fuer bestehende Projekte

Ziel: Bestehende Projekte koennen eine neue INTENTRON-Version uebernehmen, ohne lokale Entscheidungen, Skills, Hooks, CI oder Sicherheitsdateien blind zu ueberschreiben.

## Grundregel

Projektlokale Skills sind reproduzierbarer Projektstand. Ein Upgrade ist eine bewusste Projektentscheidung und wird versioniert.

## Upgrade-Modi

| Modus | Verhalten |
|---|---|
| `inspect` | Liest Bestand, Framework-Version und Zielversion. Zeigt Diff, Risiken und manuelle TODOs. Schreibt keine Projektdateien. |
| `apply-safe` | Fuegt nur neue Dateien oder fehlende Sektionen hinzu. Bestehende Inhalte werden nicht ersetzt. |
| `apply-with-confirmation` | Fragt fuer jede potenziell ueberschreibende Aenderung einzeln nach. |

## Nutzerfluss

1. Git-Arbeitsbaum pruefen: clean oder Aenderungen sichern.
2. Aktuelle Framework-Version und Quelle feststellen.
3. Neue Framework-Version in einen Temp-Ordner ziehen.
4. Projektlokale Skills vergleichen — Versionen bestehender Skills pruefen.
4a. Neue Skills inventarisieren — Skills im Framework die im Projekt fehlen auflisten (siehe unten).
5. Neue Skill-Versionen und neue Skills nach Modus-Regel uebernehmen.
6. Projektvertrag und Runtime-Mapping migrieren.
7. Neue Pflichtartefakte als Skelett anlegen, ohne lokale Inhalte zu ueberschreiben.
8. Provider-Postflight im Upgrade-Modus ausfuehren (`bootstrap/references/provider-postflight.md`).
9. Diff pruefen.
10. Commit und Push erst nach Operator-Bestaetigung.

> Einzelne Baseline-Artefakte (fehlende Pflichtdateien, geschaerfte Gates) werden idempotent
> ueber `bash bootstrap/scripts/migrate-to-v2.sh --issue BOO-NN` nachgezogen — eine Funktion pro
> Issue, mehrfaches Ausfuehren ist sicher. Welche Migration ein Upgrade braucht, nennen die
> Release Notes in `docs/releases/`.

## Dateikategorien

| Kategorie | Upgrade-Verhalten |
|---|---|
| Projektlokale Skill-Kopien | Aktualisieren nur nach Diff/Backup oder Versionshinweis. |
| Neue Skills (im Framework, nicht im Projekt) | In Schritt 4a inventarisieren und nach Operator-Wahl additiv installieren. |
| `CONVENTIONS.md` | Nicht ersetzen; neue Sektionen mergen oder als TODO markieren. |
| `AGENTS.md` / `CLAUDE.md` | Nicht ersetzen; Precedence und Runtime-Bruecke nachziehen. |
| Architektur-/Security-Dateien | Nie pauschal ueberschreiben; neue Pflichtsektionen einfuegen oder als TODO markieren. |
| `.codex/hooks.json` / `.claude/settings.json` | Neue Hooks registrieren, bestehende Eintraege erhalten. |
| `CONTEXT.md`, `solution-artefakte.md`, `DEVELOPER_ONBOARDING.md` | Nur seeden wenn fehlend (idempotent); vorhandene Operator-Inhalte nie ueberschreiben. |
| `.claude/environment.json` (+ `generate-environment-json.sh`) | Fehlende Felder additiv ergaenzen, danach `bash .claude/generate-environment-json.sh --force`; bestehende Werte erhalten. |
| `docs/kollisionsschutz-drei-ebenen.md` | Nur anlegen wenn fehlend (Multi-User-/Multi-Session-Hinweis). |
| `.env`, Secrets, lokale Reports | Nie anfassen, nie committen, nie in Reports kopieren. |

## Schritt 4a: Neue Skills inventarisieren

Skills die im Framework-Repo vorhanden sind, aber noch nicht in `.claude/skills/` des Projekts liegen,
werden explizit aufgelistet. Dieser Schritt laeuft in allen drei Modi (`inspect`, `apply-safe`,
`apply-with-confirmation`).

**Delta ermitteln:**

```bash
REPO="OWNER/intentron"  # aus aktuellem Upgrade-Kontext

# Alle Skills im Framework (Verzeichnisse mit SKILL.md im Root)
FRAMEWORK_SKILLS=$(gh api "repos/${REPO}/contents/" \
  --jq '.[].name' | while read d; do
    gh api "repos/${REPO}/contents/${d}/SKILL.md" \
      --jq "\"${d}\"" 2>/dev/null
  done | sort)

# Lokale Skills im Projekt
LOCAL_SKILLS=$(ls .claude/skills/ 2>/dev/null | sort)

# Fehlende Skills
NEW_SKILLS=$(comm -23 <(echo "$FRAMEWORK_SKILLS") <(echo "$LOCAL_SKILLS"))
```

Fuer jeden fehlenden Skill: `name`, `description` und `recommended_model` aus dem
SKILL.md-Frontmatter lesen und dem Operator anzeigen.

**Operator-Auswahl (alle drei Modi):**

```
Neue Skills in v{NEUE_VERSION} (nicht im Projekt):
  1. knowledge-onboarding — Bestands-Doku in Governance-Artefakte routen (sonnet)
  2. pitch             — Demo-Storyboard und Pitch-Materialien verwalten (sonnet)
  3. visualize         — Mermaid-Diagramme aus Architektur-Artefakten generieren (haiku)
  ...

Welche installieren?
  a) Alle
  b) Ausgewaehlte (Komma-getrennte Nummern: 1,3)
  c) Keine — spaeter manuell per `gh api` nachinstallieren
```

**Modus-Verhalten:**

| Modus | Verhalten |
|---|---|
| `inspect` | Listet neue Skills, schreibt nichts. |
| `apply-safe` | Installiert nach Operator-Wahl additiv (kein Ueberschreiben moeglich, da Skills neu sind). |
| `apply-with-confirmation` | Fragt pro Skill einzeln. |

**Nach der Installation:** Manifest-Eintrag in `journal/reports/framework-upgrade/YYYY-MM-DD.md`
unter neuer Sektion `## Neu installierte Skills` (siehe Upgrade-Report-Skelett unten).

## Upgrade-Report

Empfohlener Pfad:

```text
journal/reports/framework-upgrade/YYYY-MM-DD.md
```

Report-Skelett:

```markdown
# Framework Upgrade Report

Datum: YYYY-MM-DD
Modus: inspect | apply-safe | apply-with-confirmation

## Versionen

- Alte Version / Quelle:
- Neue Version / Commit:
- `environment.json` `bootstrap_version` aktualisiert auf:

## Aktualisierte Skills

| Skill | Alt | Neu | Entscheidung |
|---|---|---|---|

## Neu installierte Skills

| Skill | Version | Entscheidung |
|---|---|---|

## Neu angelegte Dateien

- ...

## Geaenderte Projektvertragssektionen

- `CONVENTIONS.md`: ...
- `AGENTS.md`: ...
- `CLAUDE.md`: ...

## Bewusst nicht ueberschrieben

- ...

## Manuelle TODOs

- ...

## Provider-Postflight

| Provider | Status | Naechste Aktion |
|---|---|---|

## Operator-Freigabe

- Diff geprueft:
- Commit erlaubt:
```

## Release-Notes-Regel

Vor jedem Upgrade werden `docs/releases/` gelesen. Jede Release Note nennt:

- Migrationsbedarf,
- neue Pflichtartefakte,
- optionale Nacharbeiten,
- Provider-/Secret-Hinweise,
- Breaking Changes oder bewusste Nicht-Aenderungen.

Der Upgrade-Pfad nutzt diese Release Notes als Input fuer den Report.
