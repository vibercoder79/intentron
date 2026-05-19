# Framework-Upgrade fuer bestehende Projekte

Ziel: Bestehende Projekte koennen eine neue Code-Crash-Framework-Version uebernehmen, ohne lokale Entscheidungen, Skills, Hooks, CI oder Sicherheitsdateien blind zu ueberschreiben.

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
4. Projektlokale Skills vergleichen.
5. Neue Skill-Versionen nur nach Modus-Regel uebernehmen.
6. Projektvertrag und Runtime-Mapping migrieren.
7. Neue Pflichtartefakte als Skelett anlegen, ohne lokale Inhalte zu ueberschreiben.
8. Provider-Postflight im Upgrade-Modus ausfuehren.
9. Diff pruefen.
10. Commit und Push erst nach Operator-Bestaetigung.

## Dateikategorien

| Kategorie | Upgrade-Verhalten |
|---|---|
| Projektlokale Skill-Kopien | Aktualisieren nur nach Diff/Backup oder Versionshinweis. |
| `CONVENTIONS.md` | Nicht ersetzen; neue Sektionen mergen oder als TODO markieren. |
| `AGENTS.md` / `CLAUDE.md` | Nicht ersetzen; Precedence und Runtime-Bruecke nachziehen. |
| Architektur-/Security-Dateien | Nie pauschal ueberschreiben; neue Pflichtsektionen einfuegen oder als TODO markieren. |
| `.codex/hooks.json` / `.claude/settings.json` | Neue Hooks registrieren, bestehende Eintraege erhalten. |
| `.env`, Secrets, lokale Reports | Nie anfassen, nie committen, nie in Reports kopieren. |

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

## Aktualisierte Skills

| Skill | Alt | Neu | Entscheidung |
|---|---|---|---|

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
