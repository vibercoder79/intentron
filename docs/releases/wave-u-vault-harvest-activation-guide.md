# Release Notes - Wave U Vault-Harvest-Aktivierungs-Anleitung

> 🌐 **Sprache:** Deutsch (diese Datei) · [🇬🇧 English](wave-u-vault-harvest-activation-guide.en.md)

Stand: 2026-05-28 · **v0.2.1-Linie** (erste Doku-Politur nach dem v0.2.0-Release)

## Zweck

Operator-Frage: "Ist genuegend beschrieben, WIE man `install-vault-sync.sh` ausfuehrt?" — **Nein.** Die Doku erklaerte das **Was** und **Warum** des Vault-Harvest gut (Pattern, Sicherheit, Team-Vertrag), aber das **Wie** der Durchfuehrung war nur ein Einzeiler (*"aktiviere mit `bash scripts/install-vault-sync.sh` (Default dry-run)"*). Es fehlte ein durchgehender Operator-Walkthrough.

Diese Welle schliesst die Durchfuehrungs-Luecke — dieselbe Art Luecke wie zuvor bei Codex (Anhang J): Referenz vorhanden, Walkthrough fehlte.

## Was jetzt da ist

**`vault-sync-pattern.md` (DE+EN), neue Sektion "Vault-Harvest aktivieren — Schritt fuer Schritt":**

1. **Voraussetzungen** — Engine-Files im Projekt (Bootstrap `[e]` oder `migrate --issue BOO-77`), Vault existiert lokal.
2. **Init ausfuehren** — `bash scripts/install-vault-sync.sh` mit den **drei interaktiven Prompts** (Vault-Pfad, Projekt-Slug, Modus) explizit benannt.
3. **Trockenlauf pruefen** — `python3 scripts/vault-sync.py --dry-run`, Layout aus `default_vault_subdir` vs. `path_mappings`-Override.
4. **Auf `auto` umstellen** — `"mode": "auto"` in `local.json` (vorher fehlte die dry-run→auto-Erklaerung komplett).
5. **Ausloesen** — `git pull` (Hook) / manuell / `--since <sha>` fuer grosse Repos.
6. **Verifizieren** — gespiegelte Dateien mit `vault_sync_*`-Frontmatter; Notizen nur in `.notes.md`.
7. **Abschalten** — `--uninstall` oder `"enabled": false`.

**HANDBUCH Anhang R (DE+EN):** Verweis-Satz im Aktivierungs-Absatz auf den neuen Walkthrough.

## Konkrete Aenderungen

| Bereich | Aenderung | Datei |
|---|---|---|
| Config-Scaffold | Neue Schritt-fuer-Schritt-Sektion (DE) | `bootstrap/references/vault-sync-pattern.md` |
| Config-Scaffold | Gleiche Sektion (EN) | `bootstrap/references/vault-sync-pattern.en.md` |
| HANDBUCH Anhang R | Verweis-Satz auf den Walkthrough (DE) | `HANDBUCH.md` |
| HANDBUCH Anhang R | dito (EN) | `HANDBUCH.en.md` |

## Keine Code-Aenderung

Reine Doku. Die Engine (`vault-sync.py`, `install-vault-sync.sh`, `post-merge.sh`, `tracked-paths.json`) bleibt unveraendert. Kein Versions-Bump.

## Folgepunkt

Der **reale End-to-End-Test** (echtes Projekt gegen echten Obsidian-Vault, nicht nur `/tmp`-Smoke-Test) bleibt offen — der Walkthrough liefert jetzt aber die Schritt-fuer-Schritt-Vorlage, an der er durchgespielt werden kann.

## Verweise

- Config-Scaffold: `bootstrap/references/vault-sync-pattern.md` §"Vault-Harvest aktivieren — Schritt fuer Schritt"
- HANDBUCH: Anhang R Layer 3 (Vault-Harvest)
- Engine + Pattern: BOO-77, BOO-82
- Operator-Feedback: Tobias, 2026-05-28
