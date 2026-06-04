# Runbook: Framework-Update — Bestandsprojekt auf den aktuellen Stand heben

> Für Maschinen/Projekte, auf denen INTENTRON **bereits installiert** ist und die den **aktuellen Framework-Stand** übernehmen wollen — ohne neu zu bootstrappen, ohne lokale Entscheidungen blind zu überschreiben. EN: [`framework-update.en.md`](framework-update.en.md).

## Wann dieses Runbook?

Du hast ein Projekt, das eine **ältere INTENTRON-Version** fährt, und willst es auf den jetzigen Stand ziehen — neue Gates, neue Pflicht-Artefakte, Bugfixes aus den letzten Release-Waves. Das ist der **Upgrade-Fall**.

Abgrenzung zu den Nachbar-Runbooks:
- Nur den Leichtgewicht-SecondBrain-Baustein nachrüsten (ohne Upgrade) → [`secondbrain-nachziehen.md`](secondbrain-nachziehen.md)
- Mehrere Menschen, ein VPS-Projekt → [`multi-user-vps.md`](multi-user-vps.md)

Zwei Schritte, beide nicht-destruktiv:

1. **Werkzeug aktualisieren** — den `bootstrap`-Skill auf der Maschine auf den neuesten Stand bringen.
2. **Projekt hochziehen** — diesen Upgrade-Prompt in die Claude-Code-Session einfügen; der Skill erkennt die bestehende Installation und fährt drei Modi (inspect → apply-safe → apply-with-confirmation).

## Schritt 1 — Bootstrap-Skill aktualisieren

Holt nur den `bootstrap`-Skill frisch aus dem Repo (sparse, ohne den ganzen Klon):

```bash
cd /tmp
git clone --filter=blob:none --sparse https://github.com/vibercoder79/intentron.git intentron
cd intentron && git sparse-checkout set bootstrap
cp -r bootstrap ~/.claude/skills/
cd /tmp && rm -rf intentron
```

> Auf einem **Multi-User-VPS** mit zentralem Skill-Pool stattdessen einmal `git pull` im Pool (`/opt/claude/skills/`) — siehe [`multi-user-vps.md`](multi-user-vps.md) bzw. HANDBUCH Anhang R (Skill-Pool-Governance).

## Schritt 2 — Upgrade-Prompt in die Claude-Code-Session einfügen

Öffne Claude Code **im Projektordner** und füge diesen Prompt ein — das Upgrade läuft ohne interaktives Interview:

```text
Dieses Repo fährt evtl. eine ältere INTENTRON-Version. Aktualisiere es sicher nach
bootstrap/references/framework-upgrade.md (Modi inspect → apply-safe → apply-with-confirmation).
(1) inspect: lies den Projektvertrag (CONVENTIONS.md, CLAUDE.md/AGENTS.md, .claude/environment.json,
    Hooks, Specs), hole das aktuelle Framework von https://github.com/vibercoder79/intentron,
    lies docs/releases/ für die Änderungen, und zeig mir Diff + Risiken + manuelle TODOs, ohne
    etwas zu schreiben.
(2) apply-safe: wende nur additive/idempotente Änderungen an und führe die zutreffenden
    bootstrap/scripts/migrate-to-v2.sh --issue BOO-NN Migrationen aus.
(3) apply-with-confirmation: alles, was bestehende Regeln, Hooks, CI oder Skill-Versionen ändert,
    einzeln mit mir bestätigen. .env/Secrets nie anfassen.
Zum Schluss bootstrap/references/verify-setup.sh ausführen und einen Upgrade-Report nach
journal/reports/framework-upgrade/YYYY-MM-DD.md schreiben.
```

Der Prompt fährt automatisch drei Phasen: **inspect** (Dry-run, nichts wird geschrieben) → **apply-safe** (nur additive Änderungen) → **apply-with-confirmation** (alles Destruktive einzeln bestätigen).

| Modus | Verhalten |
|---|---|
| **`inspect`** | Diff + Risiken + manuelle TODOs zeigen, **schreibt nichts** |
| **`apply-safe`** | nur additive/idempotente Änderungen; bestehende Inhalte bleiben |
| **`apply-with-confirmation`** | alles, was bestehende Regeln, Hooks, CI oder Skill-Versionen ändert, einzeln bestätigen |

> **Alternativ:** `/bootstrap` in der Session tippen — der Skill erkennt die bestehende Installation (§7.5a) und fragt den Modus interaktiv ab.

## Sicherheit & Idempotenz

- **Read vor Edit, nur additiv:** Bestehende Inhalte (`CONVENTIONS.md`, `CLAUDE.md`, Hooks, Specs) werden nie blind überschrieben.
- **`.env`/Secrets/lokale Reports:** nie anfassen, nie committen, nie in Reports kopieren.
- **Idempotent:** `migrate-to-v2.sh --issue BOO-NN` und `verify-setup.sh` sind gefahrlos wiederholbar.
- **Vor dem Upgrade:** Git-Arbeitsbaum clean machen oder Änderungen sichern; `docs/releases/` lesen (Migrationsbedarf, neue Pflicht-Artefakte, Breaking Changes).
- **Commit/Push erst nach Operator-Freigabe** — nach Diff-Prüfung.

## Danach

- Bewusste Abweichungen werden **dokumentiert statt überschrieben** (Grundsatz: Framework-Versionen dürfen härter/klarer machen, nicht heimlich umdeuten).
- Optional: das volle Bestands-Onboarding (HANDBUCH Anhang U, Weg 3) fahren, wenn nicht nur das Upgrade, sondern auch neue Skills/Gates nachgezogen werden sollen.

## Verweise

`bootstrap/references/framework-upgrade.md` (Modi, Nutzerfluss, Dateikategorien) · `bootstrap/SKILL.md` §7.5a (Auto-Erkennung) · `bootstrap/scripts/migrate-to-v2.sh` (Bestands-Migrationen) · `bootstrap/references/provider-postflight.md` · `bootstrap/references/verify-setup.sh` · HANDBUCH §„Upgrade-Pfad für bestehende Projekte" · `docs/upgrade-path-existing-projects.excalidraw` · verwandt: [`secondbrain-nachziehen.md`](secondbrain-nachziehen.md), [`multi-user-vps.md`](multi-user-vps.md). BOO-156.
