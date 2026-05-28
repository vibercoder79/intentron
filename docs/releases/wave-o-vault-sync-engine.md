# Release Notes - Wave O Framework-native Vault-Sync-Engine

Stand: 2026-05-28

## Zweck

Wave O schliesst BOO-77 und macht aus dem dokumentierten Vault-Harvest-Pattern (BOO-75) ein **funktionierendes Setup**. Bei Bootstrap-Option `[e] Repo-Docs + persoenlicher Vault-Harvest` richtet das Framework jetzt das komplette Vault-Harvest ein — mit einer **eigenen, schlanken Sync-Engine**, nicht mehr nur einem Verweis auf ein Nachbar-Repo.

**Erwarteter Effekt:** Wer im Team arbeitet und seinen persoenlichen Obsidian-Vault als Cross-Project-Leseansicht nutzen will, waehlt im Bootstrap `[e]` und hat danach mit einem `bash scripts/install-vault-sync.sh` alles eingerichtet. Kein externer Code, keine Dependencies.

## Betroffene Stories

- BOO-77 — framework-native Vault-Sync-Engine + Bootstrap-`[e]`-Verdrahtung

## Hintergrund: warum framework-native statt vendored

BOO-75 (Wave N) dokumentierte das Vault-Harvest-Pattern und verwies fuer die Engine auf Stefans `StefanWeimarPRODOC/project-template`. Phase 2 (Vendoring seines Codes) war blockiert, weil das Repo nicht zugaenglich ist. Operator-Entscheidung (Tobias, 2026-05-28): **Stefans Code wird nicht gebraucht** — das Framework baut eine eigene, schlanke Implementierung des dokumentierten Patterns. Damit ist der Blocker aufgeloest und das Framework bleibt self-contained.

## Was Nutzer mit dem neuen Setup bekommen

Vier Engine-Files unter `bootstrap/references/vault-sync/`, die Bootstrap-Option `[e]` ins Projekt kopiert:

- **`vault-sync.py`** — einseitige Sync-Engine Repo→Vault (Python-Stdlib). Liest den versionierten Team-Vertrag `.vault-sync/tracked-paths.json` + die gitignored `.vault-sync/local.json` pro Mitarbeiter. Frontmatter-Merge mit `vault_sync_*`-Namespace (idempotent), `type:`-Injektion nur wenn die Quelle keinen hat. Modi `auto` / `dry-run` / `ask`. Ueberspringt `.notes.md`-Sidecars.
- **`install-vault-sync.sh`** — interaktives Init pro Mitarbeiter (`--force` / `--uninstall`), legt `local.json` an, traegt `.gitignore`-Eintrag ein, symlinkt den Hook.
- **`post-merge.sh`** — Hook-Wrapper, feuert nach `git pull`, `exit 0` ohne `local.json` (null Reibung).
- **`tracked-paths.json`** — versionierter Team-Vertrag, 4 Defaults.

## Sicherheit (umgesetzt + getestet)

- **Einseitig:** schreibt NUR in den Vault, NIE ins Repo.
- **Pfad-Containment:** jedes Vault-Ziel wird via `realpath` gegen `vault_path` geprueft — `../`-Ausbruch und Symlink-Traversal werden blockiert.
- **Dry-run-Default**, keine Secrets, keine Netzwerk-Calls, Python-Stdlib-only.
- **security-architect REVIEW** (manuell): einseitiger Datenfluss, kein eval/exec, kein Shell-Injection-Vektor. Keine Findings.
- **Smoke-Test (6 Faelle gruen):** dry-run / real-auto / Containment-Block / enabled=false / keine local.json / Sidecar-Schutz.

## Konkrete Aenderungen

| Bereich | Aenderung | Datei |
|---|---|---|
| Engine-Files NEU | vault-sync.py + install-vault-sync.sh + post-merge.sh + tracked-paths.json | `bootstrap/references/vault-sync/` |
| Bootstrap Block B.3 `[e]` | von "dokumentierte Wahl" auf "Engine-Files generieren + .gitignore + Hook" umgestellt (DE+EN), v3.31.0 | `bootstrap/SKILL.md` + `.en.md` |
| Config-Scaffold | Mechanik-Sektion + Phasen + Sicherheit auf framework-native umgestellt (DE+EN) | `bootstrap/references/vault-sync-pattern.md` + `.en.md` |
| HANDBUCH Anhang R Layer 3 | Aktivierungs-Satz auf framework-native Engine umgestellt (DE+EN) | `HANDBUCH.md` + `.en.md` |
| Migration | `migrate_boo_77` (kopiert Engine-Files in Bestands-Projekt) + ALL_ISSUES | `bootstrap/scripts/migrate-to-v2.sh` |
| Migration-Checklist | §BOO-77 (DE+EN) | `bootstrap/references/migration-checklist-v1-to-v2.md` + `.en.md` |
| Spec | `specs/BOO-77.md` | specs/ |

## Skill-Versions-Bumps

- `bootstrap` 3.30.0 → 3.31.0 (Option `[e]` generiert jetzt Engine-Files)

## Migration fuer Bestands-Projekte

```bash
bash bootstrap/scripts/migrate-to-v2.sh --issue BOO-77
```

Idempotent + nicht-destruktiv: kopiert die Engine-Files nur falls nicht vorhanden, schreibt NICHT in den Vault. Danach pro Mitarbeiter `bash scripts/install-vault-sync.sh`.

## Verweis auf BOO-75

Wave O loest den in BOO-75 dokumentierten "Phase 2 = Vendoring von Stefans Code"-Pfad **anders** als urspruenglich gedacht: framework-native statt vendored. Stefans `project-template` bleibt der Pattern-Impuls, ist aber nicht die Code-Quelle. Kein Master/Mirror-Sync noetig (eigener Code, anders als bei DPO/BOO-74).

## Verweise

- Spec: `specs/BOO-77.md`
- Engine: `bootstrap/references/vault-sync/`
- HANDBUCH: Anhang R Layer 3 (Vault-Harvest), `bootstrap/references/vault-sync-pattern.md`
- Vorherige Welle: `docs/releases/wave-n-vault-harvest-and-skill-location.md`
- Konsolidierter Ueberblick: `docs/releases/v0.2.0-overview.md`
- Operator-Entscheidung: Tobias, 2026-05-28
- Linear: BOO-77
