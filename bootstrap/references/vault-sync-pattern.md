# Vault-Harvest-Pattern — Config-Scaffold + framework-native Engine (BOO-75/77/82)

Repo-Docs + persoenlicher Vault-Harvest fuer Multi-Person-Teams mit Obsidian-Nutzern. Dieses Dokument beschreibt den Daten-Vertrag und die Mechanik. Die **Sync-Engine ist seit BOO-77 framework-nativ** — sie liegt unter `bootstrap/references/vault-sync/` (`vault-sync.py`, `install-vault-sync.sh`, `post-merge.sh`, `tracked-paths.json`) und wird von Bootstrap-Option `[e]` direkt ins Projekt kopiert. Kein externer Code, keine Dependencies (Python-Stdlib + Bash). Stefans `project-template` war der Pattern-Impuls, ist aber **nicht** die Quelle der Engine.

> **Schwesterdatei (Englisch):** [`vault-sync-pattern.en.md`](./vault-sync-pattern.en.md)
> **HANDBUCH-Hintergrund:** Anhang R Layer 3 (Vault-Harvest-Pattern, 2-Fluss-Modell).

## Wann dieses Pattern?

Ein Team arbeitet am selben GitHub-Repo (Doku lebt in `docs/`), **und** einzelne Operatoren wollen projektuebergreifende Insights weiterhin im persoenlichen Obsidian-Vault sehen. Obsidian ist ein Solo-Werkzeug — es gibt keinen geteilten Team-Vault. Das Pattern loest das ueber zwei getrennte Fluesse:

- **Fluss 1 (normales Git, alle, bidirektional):** `docs/` ↔ GitHub-Repo via `git push`/`git pull`. Team-SSoT.
- **Fluss 2 (Harvest, pro Person, einseitig):** `git post-merge`-Hook kopiert ausgewaehlte `docs/`-Dateien in den persoenlichen Vault — nie zurueck.

## Baustein 1 — Team-Vertrag `.vault-sync/tracked-paths.json` (versioniert)

Definiert, welche Repo-Pfade harvest-bar sind, welches `type:`-Frontmatter beim Mirror ergaenzt wird **und wohin die Datei im Vault standardmaessig wandert** (`default_vault_subdir`, BOO-82). Vier Defaults (aus der Referenz-Implementierung):

```json
{
  "version": 1,
  "tracked_paths": [
    { "glob": "docs/components/*.md",            "type": "component",    "default_vault_subdir": "02 Projekte/{project_slug}/Components/" },
    { "glob": "docs/decisions/*.md",             "type": "decision",     "default_vault_subdir": "02 Projekte/{project_slug}/Decisions/" },
    { "glob": "docs/architecture-guidelines.md", "type": "architecture", "default_vault_subdir": "02 Projekte/{project_slug}/" },
    { "glob": "journal/sprint-*.md",             "type": "sprint-retro", "default_vault_subdir": "04 Ressourcen/{project_slug}/sprints/" }
  ]
}
```

- `type:` wird nur gesetzt, wenn die Quelldatei noch keinen hat (Sprint-Retros bringen ihren eigenen `type:` mit).
- `default_vault_subdir` (BOO-82) traegt das **Default-Vault-Layout im Team-Vertrag** — so muss nicht jeder Mitarbeiter dieselben Pfade in seiner `local.json` wiederholen. Platzhalter `{project_slug}` und `{slug}` werden beide durch den Slug aus `local.json` ersetzt. Nur der Dateiname landet im Default-Unterordner.

Diese Datei ist **versioniert** (committed) — sie ist der Team-Vertrag, worauf sich alle einigen.

## Baustein 2 — Persoenliche Konfig `.vault-sync/local.json` (gitignored)

Pro Mitarbeiter, **niemals committen** (gehoert in `.gitignore`). Schema:

```json
{
  "vault_path": "/Users/<operator>/Obsidian/<vault>",
  "project_slug": "<projekt-slug>",
  "path_mappings": {},
  "last_sync_commit": "<sha>",
  "enabled": true,
  "mode": "auto"
}
```

- `path_mappings` ist seit BOO-82 eine **optionale Ueberschreibung**, kein Pflicht-Feld mehr. Leer (`{}`) lassen = Vault-Ziel kommt aus dem `default_vault_subdir` des Team-Vertrags. Nur wer fuer sich abweichen will, traegt hier ein Praefix-Mapping ein, z.B. `{ "docs/components": "Eigener Ordner/{slug}/Komponenten" }`. Bei mehreren Treffern gewinnt das laengste Praefix; ein passendes `path_mappings` schlaegt immer den Vertrags-Default.
- `mode`: `auto` (still mirroren) | `dry-run` (nur anzeigen) | `ask` (pro Datei fragen).
- `enabled: false` deaktiviert den Harvest fuer diesen Operator ohne Deinstallation.

## Baustein 3 — Mechanik (framework-native, BOO-77)

Die Engine liegt im Framework unter `bootstrap/references/vault-sync/` und wird von Bootstrap-Option `[e]` ins Projekt kopiert:

- `scripts/install-vault-sync.sh` — interaktives Init pro Mitarbeiter (`--force` / `--uninstall`), legt `local.json` an, traegt `.gitignore`-Eintrag ein, symlinkt den Hook.
- `scripts/vault-sync.py` — Sync-Engine (Python-Stdlib-only, Frontmatter-Merge mit `vault_sync_*`-Namespace, Pfad-Containment-Check, Modi `auto`/`dry-run`/`ask`, liest Commit-SHA direkt aus `.git/HEAD`).
- `.claude/hooks/post-merge.sh` — Wrapper, via Symlink in `.git/hooks/post-merge`, feuert nach jedem `git pull`. `exit 0` wenn keine `local.json`.
- `.vault-sync/tracked-paths.json` — versionierter Team-Vertrag (siehe Baustein 1).

### Ziel-Aufloesung (BOO-82)

Pro getrackter Datei bestimmt die Engine das Vault-Ziel in dieser Reihenfolge:

1. **`path_mappings` aus `local.json`** — falls ein Praefix passt (laengstes gewinnt), Ueberschreibung pro Mitarbeiter.
2. **`default_vault_subdir` aus dem Team-Vertrag** — sonst der Team-Default; nur der Dateiname landet darin.
3. **kein Treffer** → Datei wird uebersprungen (`SKIP`).

So funktioniert der Harvest out-of-the-box mit leerem `path_mappings`, bleibt aber pro Person uebersteuerbar.

### Inkrementeller Sync `--since <sha>` (BOO-82)

`python3 scripts/vault-sync.py --since <sha>` synct nur Dateien, die seit `<sha>` bis `HEAD` geaendert wurden (`git diff --name-only <sha>..HEAD`). Fuer grosse Repos schneller als der Voll-Sync. Ist git nicht verfuegbar oder der SHA ungueltig, faellt die Engine mit einer Warnung auf den Voll-Sync zurueck (kein stiller Datenverlust). Der post-merge-Hook nutzt weiterhin den Voll-Sync — `--since` ist fuer manuelle/optimierte Laeufe.

## Kernregeln

- **Einseitig Repo → Vault.** Der Vault wird NIE vom Sync zurueckgeschrieben.
- **Vault nie manuell veraendern,** wo der Sync hinschreibt — Annotationen laufen ueber `.notes.md`-Schwesterdateien, die der Sync nicht anfasst.
- **Frontmatter-Namespace `vault_sync_*`** (`vault_sync_project`, `vault_sync_path`, `vault_sync_commit`, `vault_sync_at`) — kollisionsfrei mit Quell-Properties, in Obsidian-Bases filterbar.
- **Null Reibung:** Mitarbeiter ohne `local.json` → Hook `exit 0` stillschweigend.
- **Abgrenzung DocSync (Block D.2):** DocSync ist solo + bidirektional (Vault ↔ Repo). Vault-Harvest ist team + einseitig (Repo → Vault). Im Team-Modus daher **DocSync = nein** setzen.

## Aktivierung im Bootstrap

Bootstrap-Frage B.3, Option `[e] Repo-Docs + persoenlicher Vault-Harvest`. Bootstrap kopiert die Engine-Files ins Projekt (`scripts/vault-sync.py`, `scripts/install-vault-sync.sh`, `.claude/hooks/post-merge.sh`, `.vault-sync/tracked-paths.json`), traegt `.vault-sync/local.json` in `.gitignore` ein, setzt Block D DocSync = nein und ergaenzt den Onboarding-Schritt. Danach aktiviert jeder Mitarbeiter den Harvest optional mit `bash scripts/install-vault-sync.sh` (Default-Modus `dry-run`).

## Vault-Harvest aktivieren — Schritt fuer Schritt

Das macht jeder Mitarbeiter **einmal pro Projekt-Klon**, der seinen persoenlichen Vault befuellen will. Niemand muss mitmachen — ohne `local.json` passiert nichts (`exit 0`).

**Voraussetzungen:**
- Die Engine-Files liegen im Projekt (Bootstrap-Option `[e]` lief, oder in einem Bestands-Projekt: `bash <skill-repo>/bootstrap/scripts/migrate-to-v2.sh --issue BOO-77`).
- Dein Obsidian-Vault existiert lokal (du kennst den absoluten Pfad).

**1. Init ausfuehren** (im Projekt-Root):

```bash
bash scripts/install-vault-sync.sh
```

Das Skript fragt interaktiv drei Dinge:
- **Absoluter Pfad zu deinem Obsidian-Vault** — z.B. `/Users/du/Obsidian/MeinVault`.
- **Projekt-Slug** — Ordnername im Vault, z.B. `mein-projekt`; ersetzt `{project_slug}` im Team-Vertrag.
- **Modus** — `dry-run` / `auto` / `ask` (Default `dry-run`).

Danach legt es `.vault-sync/local.json` an (gitignored), traegt sie in `.gitignore` ein und verlinkt den `post-merge`-Hook. (`--force` ueberschreibt eine bestehende `local.json`.)

**2. Trockenlauf pruefen** — was wuerde gespiegelt?

```bash
python3 scripts/vault-sync.py --dry-run
```

Zeigt pro Datei das geplante Vault-Ziel. Das Layout kommt aus `default_vault_subdir` des Team-Vertrags; abweichen nur, wenn du in deiner `local.json` ein `path_mappings`-Praefix setzt.

**3. Auf echtes Spiegeln umstellen** — in `.vault-sync/local.json` `"mode": "auto"` setzen (oder beim Init `auto` waehlen). `auto` = still spiegeln, `ask` = pro Datei nachfragen.

**4. Ausloesen** — `git pull` (der `post-merge`-Hook feuert automatisch). Manuell jederzeit: `python3 scripts/vault-sync.py`. Fuer grosse Repos nur Aenderungen seit einem Commit: `python3 scripts/vault-sync.py --since <sha>`.

**5. Verifizieren** — im Vault liegen jetzt die gespiegelten Dateien (z.B. unter `02 Projekte/<slug>/...`) mit `vault_sync_*`-Frontmatter. Eigene Notizen NUR in `.notes.md`-Schwesterdateien ablegen — die fasst der Sync nie an.

**Wieder abschalten:** `bash scripts/install-vault-sync.sh --uninstall` (entfernt Hook + `local.json`; der versionierte Team-Vertrag bleibt). Temporaer pausieren: `"enabled": false` in `local.json`.

## Phasen

- **Phase 1 (BOO-75):** Dokumentation + Config-Scaffold + Bootstrap-Option als dokumentierte Wahl.
- **Phase 2 (BOO-77, done):** **framework-native Engine** unter `bootstrap/references/vault-sync/` — Bootstrap-Option `[e]` richtet das Vault-Harvest vollstaendig ein. Kein externer Code noetig. Smoke-getestet (dry-run / real / Pfad-Containment / disabled / keine local.json).
- **Phase 3 (BOO-82, done):** Komfort + Skalierung. `default_vault_subdir` im Team-Vertrag (Default-Layout zentral statt pro Mitarbeiter wiederholt), `local.json path_mappings` als optionale Ueberschreibung, inkrementeller `--since <sha>`-Sync. Smoke-getestet (Default-Layout / Override-Vorrang / `--since` / Containment / Fallback bei ungueltigem SHA).

## Sicherheit

- Einseitig: schreibt NUR in den Vault, nie ins Repo.
- Pfad-Containment via `realpath`: jedes Ziel muss innerhalb `vault_path` liegen, sonst Abbruch (verhindert `../`-Ausbruch und Symlink-Traversal).
- Keine Netzwerk-Calls, keine Secrets, Python-Stdlib-only.
- `local.json` ist gitignored — der persoenliche Vault-Pfad leakt nie ins Repo.

## Quelle

Pattern-Impuls: Operator-Feedback Stefan, 2026-05-27 (`StefanWeimarPRODOC/project-template`). Framework-native Engine: BOO-77, Operator-Entscheidung Tobias 2026-05-28 (Stefans Code nicht benoetigt). `default_vault_subdir` + inkrementeller `--since`-Sync (BOO-82): zwei uebernommene Ideen aus Stefans Template, framework-nativ nachgebaut (Operator-Entscheidung 2026-05-28).
