# Release Notes - Wave N Vault-Harvest + Skill-Installations-Strategie

> 🌐 **Sprache:** Deutsch (diese Datei) · [🇬🇧 English](wave-n-vault-harvest-and-skill-location.en.md)

Stand: 2026-05-28

## Zweck

Wave N schliesst zwei wiederkehrende Operator-Fragen rund um **Vault-Struktur und Skill-Verortung** — beide reine Doku-Wellen, kein Feature-Code, aber hohe Orientierungs-Wirkung fuer Teams:

1. **BOO-75 — Vault-Harvest-Pattern:** Wie kombiniere ich Repo-Docs (Team-SSoT) mit einem persoenlichen Obsidian-Vault? Antwort: zwei getrennte Fluesse + scharfer Grundsatz "Obsidian ist ein Solo-Werkzeug, kein Enterprise-Werkzeug".
2. **BOO-76 — Skill-Installations-Strategie:** Wo gehoeren die Skills hin — global, pro Projekt oder System-Pool? Antwort: drei Install-Ebenen + Decision-Matrix pro Deployment-Szenario + Cross-Tool-Sicht.

**Erwarteter Effekt:** Zwei Fragen, die bisher in Beratungsgespraechen oder verstreut im HANDBUCH beantwortet wurden, haben jetzt je einen klaren, bebilderten Anhang.

## Betroffene Stories

- BOO-75 — HANDBUCH Anhang R Layer 3 erweitert (Vault-Harvest) + Bootstrap Block B.3 5. Option + Config-Scaffold
- BOO-76 — HANDBUCH Anhang S NEU (Skill-Installations-Strategie)

## BOO-75 — Vault-Harvest-Pattern (Repo-Docs + persoenlicher Vault)

**Problem:** In Multi-Person-Projekten kann der Obsidian-Vault nicht die geteilte Doku-SSoT sein — ein Vault ist persoenlich. Die lebende Doku gehoert ins GitHub-Repo unter `docs/`. Aber wer ueber mehrere Projekte arbeitet, will Cross-Project-Insights weiterhin im eigenen Vault.

**Was jetzt da ist:**

- **HANDBUCH Anhang R Layer 3** (DE+EN): scharfer Grundsatz "Obsidian = Solo, nicht Enterprise" + **2-Fluss-Modell**:
  - Fluss 1 — normales Git (alle, bidirektional): `docs/` ↔ GitHub-Repo. Team-SSoT.
  - Fluss 2 — Vault-Harvest (pro Person, einseitig): `git post-merge`-Hook kopiert ausgewaehlte `docs/` in den persoenlichen Vault, nie zurueck. Kein Cron/Webhook.
  - Teaching-Sketch `docs/assets/vault-harvest-solo-vs-team.png` (durchgezogen-bidirektional vs. gestrichelt-einseitig).
- **Bootstrap Block B.3** (DE+EN): 5. Doku-SSoT-Option `[e] Repo-Docs + persoenlicher Vault-Harvest` als dokumentierte Wahl + Inline-Hinweis (doppelte Absicherung beim Installieren: Solo→Obsidian, Team→Repo, Team-mit-Obsidian→Harvest) + `[e]`-Handling (DocSync=nein, Onboarding-Schritt). Version 3.29.0 → 3.30.0.
- **Config-Scaffold** `bootstrap/references/vault-sync-pattern.md` (+ `.en.md`): Team-Vertrag `tracked-paths.json` + `local.json`-Schema + Mechanik + Kernregeln.

**Wichtig:** Die Sync-Engine selbst (Stefans `vault-sync.py` etc.) wird **nicht** vendored — die Referenz-Implementierung liegt in `StefanWeimarPRODOC/project-template`. Engine-Vendoring ist Phase 2 (blockiert, separate Story).

## BOO-76 — Skill-Installations-Strategie (Anhang S)

**Problem (wiederkehrende Frage):** "Wo installiere ich die Skills?" Frueher pauschal "auf Projektebene" — aber das erzeugt Update-Last (jedes Projekt einzeln). Speziell unklar: 20-Personen-Team auf einer VPS, mehrere User, Claude zentral.

**Was jetzt da ist — HANDBUCH Anhang S** (DE+EN) mit Sketch `docs/assets/skill-install-locations.png`:

- **Drei Install-Ebenen:** global pro User (`~/.claude/skills/`), pro Projekt (`<projekt>/.claude/skills/` committed), globaler System-Pool (`/opt/claude/skills/`).
- **Tradeoff:** global = ein Update, kein Pinning; pro-Projekt = N Updates, aber reproduzierbar + audit-fest.
- **Decision-Matrix pro Deployment-Szenario** (Bezug Anhang P): Solo-Mac/Solo-VPS → global pro User; Multi-User-VPS → System-Pool (Wartungs-Owner); Team-Server → System-Pool oder pro-Projekt.
- **20-Personen-VPS-Antwort konkret:** ein globaler System-Pool `/opt/claude/skills/`, read-only, ein Wartungs-Owner, ein `git pull` fuer die ganze Maschine — NICHT pro Projekt.
- **Cross-Tool:** Claude Code (`~/.claude/skills/` + `.claude/skills/`), Codex (`.codex/skills/`), andere via Anhang K. Multi-Tool-Teams → pro-Projekt committed ist portabler.

## Konkrete Aenderungen

| Bereich | Aenderung | Datei |
|---|---|---|
| HANDBUCH Anhang R Layer 3 | Obsidian=Solo geschaerft + 2-Fluss-Modell + Sketch + DocSync-Abgrenzung (DE+EN) | `HANDBUCH.md` + `.en.md` |
| HANDBUCH Anhang S NEU | Skill-Installations-Strategie (DE+EN) + Sketch | `HANDBUCH.md` + `.en.md` |
| Bootstrap Block B.3 | 5. Doku-SSoT-Option + Inline-Hinweis + `[e]`-Handling; v3.30.0 | `bootstrap/SKILL.md` + `.en.md` |
| Config-Scaffold NEU | Vault-Sync Team-Vertrag + local.json-Schema | `bootstrap/references/vault-sync-pattern.md` + `.en.md` |
| Sketches NEU | Vault-Harvest + Skill-Install-Ebenen | `docs/assets/vault-harvest-solo-vs-team.png`, `docs/assets/skill-install-locations.png` |
| Migration | `migrate_boo_75` + `migrate_boo_76` (Doku-only Hinweis-Bloecke) | `bootstrap/scripts/migrate-to-v2.sh` |
| Migration-Checklist | §BOO-75 + §BOO-76 (DE+EN) | `bootstrap/references/migration-checklist-v1-to-v2.md` + `.en.md` |
| Specs | `specs/BOO-75.md`, `specs/BOO-76.md` | specs/ |

## Skill-Versions-Bumps

- `bootstrap` 3.29.0 → 3.30.0 (BOO-75: 5. Doku-SSoT-Option + Inline-Hinweis)

## Migration fuer Bestands-Projekte

Beide reine Doku — idempotente Hinweis-Bloecke:

```bash
bash bootstrap/scripts/migrate-to-v2.sh --issue BOO-75   # Vault-Harvest (Doku-only)
bash bootstrap/scripts/migrate-to-v2.sh --issue BOO-76   # Skill-Installations-Strategie (Doku-only)
```

## Offene Folgepunkte

- **BOO-75 Phase 2** (blockiert): Vault-Sync-Engine ins Framework vendoren — sobald `StefanWeimarPRODOC/project-template` zugaenglich ODER eine framework-native Minimal-Engine gebaut wird (Operator-Entscheidung offen).
- **Framework-native Vault-Sync-Engine:** Alternative zu Stefans Code — eine schlanke, framework-eigene Sync-Mechanik, die Bootstrap bei Option `[e]` direkt generiert. Eigene Story bei Bedarf.

## Verweise

- Specs: `specs/BOO-75.md`, `specs/BOO-76.md`
- HANDBUCH: Anhang R Layer 3 (Vault-Harvest), Anhang S (Skill-Installation)
- Config-Scaffold: `bootstrap/references/vault-sync-pattern.md`
- Diskussion Vault-Sync: SecondBrain `02 Projekte/Code-Crash Framework/Decisions/2026-05-28 Vault-Sync fuer Multi-Person-Projekte (Stefan).md`
- Feedback-Quelle: Operator Stefan (Vault-Sync) + Tobias (Skill-Location), 2026-05-27/28
- Linear: BOO-75, BOO-76
- Konsolidierter Ueberblick: `docs/releases/v0.2.0-overview.md`
