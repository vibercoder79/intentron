# Release Notes - Wave T Vault-Sync-Verbesserungen

> 🌐 **Sprache:** Deutsch (diese Datei) · [🇬🇧 English](wave-t-vault-sync-improvements.en.md)

Stand: 2026-05-28

## Zweck

Wave T schliesst BOO-82 und macht die framework-native Vault-Harvest-Engine (BOO-77) **team-tauglicher und schneller**. Zwei Verbesserungen, beide aus dem Review von Stefans `project-template` (jetzt zugaenglich) — **framework-nativ nachgebaut, kein Code uebernommen**:

1. **`default_vault_subdir` im Team-Vertrag** — das Default-Vault-Layout steht jetzt zentral in der versionierten `tracked-paths.json`, nicht mehr pro Mitarbeiter in der `local.json`.
2. **Inkrementeller `--since <sha>`-Sync** — spiegelt nur seit `<sha>` geaenderte Dateien, fuer grosse Repos.

**Erwarteter Effekt:** Onboarding eines neuen Team-Mitglieds wird trivial — `bash scripts/install-vault-sync.sh`, `path_mappings` leer lassen, fertig. Das Vault-Layout ist Team-Konvention statt copy-paste-Pflicht. Wer abweichen will, ueberschreibt weiterhin pro Person.

## Betroffene Stories

- BOO-82 — `default_vault_subdir` im Team-Vertrag + inkrementeller `--since`-Sync

## Hintergrund: Stefans Template als Modell-Consumer

Stefans `StefanWeimarPRODOC/project-template` ist eine Consumer-Fork, die unsere Anhaenge validiert. Beim Review (Tobias, 2026-05-28) fielen zwei genuine Verbesserungen auf, die wir uebernehmen — der Rest (GitHub-Issues-Workflow, quality-gate.yml, fork-spezifische Regeln) bleibt absichtlich draussen. **Stefans Code wird nicht vendored** — beide Ideen sind framework-nativ implementiert, konsistent mit der BOO-77-Entscheidung.

## Was Nutzer mit den Verbesserungen bekommen

### 1. Default-Vault-Layout im Team-Vertrag

`tracked-paths.json` traegt jetzt pro Eintrag ein `default_vault_subdir` mit `{project_slug}`-Platzhalter:

```json
{ "glob": "docs/components/*.md", "type": "component", "default_vault_subdir": "02 Projekte/{project_slug}/Components/" }
```

Die Engine loest das Vault-Ziel in dieser Reihenfolge auf:

1. **`path_mappings` aus `local.json`** — falls ein Praefix passt (laengstes gewinnt), Override pro Mitarbeiter.
2. **`default_vault_subdir` aus dem Team-Vertrag** — sonst der Team-Default.
3. **kein Treffer** → Datei wird uebersprungen (`SKIP`).

`local.json` startet damit mit `path_mappings: {}` — leer = Vertrags-Default greift. Beide Platzhalter `{project_slug}` und `{slug}` werden ersetzt (rueckwaerts-kompatibel mit alten `{slug}`-Mappings).

### 2. Inkrementeller Sync

```bash
python3 scripts/vault-sync.py --since <sha>
```

Synct nur Dateien aus `git diff --name-only <sha>..HEAD`. Ist git nicht verfuegbar oder der SHA ungueltig → WARN + Voll-Sync-Fallback (kein stiller Datenverlust). Der post-merge-Hook nutzt weiterhin den Voll-Sync; `--since` ist fuer manuelle/optimierte Laeufe.

## Rueckwaerts-Kompatibilitaet

- Alte `local.json` mit gefuelltem `path_mappings` (auch `{slug}`) laeuft unveraendert — Override bleibt erste Prioritaet.
- Alte `tracked-paths.json` ohne `default_vault_subdir`: Eintraege ohne Default fallen auf `path_mappings` zurueck; ohne beides → `SKIP` (wie bisher).
- Pfad-Containment-Check (`realpath` gegen `vault_path`) bleibt unveraendert aktiv.

## Validation (Smoke-Test, 8 Faelle gruen)

1. `default_vault_subdir` ohne `path_mappings` → 3 Dateien an Default-Pfade. ✓
2. `path_mappings`-Override gewinnt; Rest via Default. ✓
3. `--since <sha>` → nur die eine geaenderte Datei. ✓
4. Containment: `../ausbruch`-Mapping → BLOCK, 0 Dateien ausserhalb. ✓
5. Frontmatter: `type:` nur injiziert wenn fehlend, `title:` bleibt, `vault_sync_*` ergaenzt. ✓
6. Ungueltiger `--since`-SHA → WARN + Voll-Sync. ✓
7. Keine `local.json` → still `exit 0`. ✓
8. `py_compile` OK. ✓

## Konkrete Aenderungen

| Bereich | Aenderung | Datei |
|---|---|---|
| Engine | `_map_target` Default-Fallback + `{project_slug}`/`{slug}`, `_changed_since` + `--since`, `_process_file` ausgelagert | `bootstrap/references/vault-sync/vault-sync.py` |
| Team-Vertrag | `version: 1`, `_comment`, `default_vault_subdir` pro 4 Eintraegen | `bootstrap/references/vault-sync/tracked-paths.json` |
| Installer | `local.json`-Vorlage `path_mappings: {}` + erklaerendes `_comment` | `bootstrap/references/vault-sync/install-vault-sync.sh` |
| Config-Scaffold | Baustein 1/2 + Ziel-Aufloesung + `--since` + Phase 3 (DE+EN) | `bootstrap/references/vault-sync-pattern.md` + `.en.md` |
| HANDBUCH Anhang R | Team-Vertrag-/local.json-Bullets + Aktivierungs-Satz erweitert (DE+EN) | `HANDBUCH.md` + `.en.md` |
| Spec | `specs/BOO-82.md` | specs/ |

## Skill-Versions-Bumps

- Keiner. Reine Engine-Template- + Doku-Aenderung; Bootstrap kopiert die aktualisierten Files unveraendert ueber Option `[e]`.

## Migration fuer Bestands-Projekte

Projekte, die das Vault-Harvest bereits aktiviert haben, holen sich die neue Engine + den erweiterten Team-Vertrag durch erneutes Kopieren der Files aus `bootstrap/references/vault-sync/` (bzw. `bash bootstrap/scripts/migrate-to-v2.sh --issue BOO-77` re-kopiert die Engine). Anschliessend `default_vault_subdir` in der bestehenden `tracked-paths.json` ergaenzen (Team-Entscheidung). Bestehende `local.json` mit `path_mappings` laeuft ohne Aenderung weiter.

## Verweise

- Spec: `specs/BOO-82.md`
- Engine: `bootstrap/references/vault-sync/`
- HANDBUCH: Anhang R Layer 3 (Vault-Harvest), `bootstrap/references/vault-sync-pattern.md`
- Vorherige Vault-Welle: `docs/releases/wave-o-vault-sync-engine.md`
- Konsolidierter Ueberblick: `docs/releases/v0.2.0-overview.md`
- Operator-Entscheidung: Tobias, 2026-05-28 (zwei Ideen aus Stefans Template, Code nicht)
- Linear: BOO-82
