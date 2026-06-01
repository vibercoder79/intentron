# BOO-96 — Onboarding-Fix: Install-Befehl + Quickstart + Self-Install/Self-Update-Prompts

## Summary

Der dokumentierte Installations-Befehl war nach dem Rebrand (code-crash-framework → `intentron`) kaputt und der Einstieg in der README unsichtbar. Diese Story (1) korrigiert den Install-Befehl in HANDBUCH (DE+EN, je 2 Stellen) + bootstrap/README, (2) ergänzt einen sichtbaren Quickstart in der README (DE+EN) mit drei Einstiegswegen, (3) dokumentiert einen AI-Self-Install-Prompt und (4) einen AI-Self-Update-Prompt für alte/Brownfield-Installationen. Reine Doku, kein Verhaltens-Change. Quelle: Onboarding-Frage Operator, 2026-06-01.

## Why

`/bootstrap` ist ein Slash-Command — er existiert erst, wenn der Skill in `~/.claude/skills/bootstrap/` liegt. Der einzige manuelle Schritt (Skill holen) war aber falsch dokumentiert: HANDBUCH §4 Schritt 3 (DE+EN) klonte `vibercoder79/claudecodeskills` und nutzte den Pfad `intentron/bootstrap`. Verifiziert per GitHub-API: `claudecodeskills` hat **keinen** `intentron/`-Ordner (404, nur `code-crash-framework/`), und der Bootstrap-Skill liegt im Repo **`vibercoder79/intentron` direkt im Root** (`bootstrap/SKILL.md`, public). Ein neuer Nutzer bekam „No such file or directory". Zusätzlich verlinkte die README-Sektion „Wo anfangen?" nur `/bootstrap`, ohne den vorgelagerten Install-Schritt — der Einstieg lief ins Leere.

## What

- **Install-Befehl korrigiert** (HANDBUCH.md + HANDBUCH.en.md, je Schritt 3 + Update-Anhang; bootstrap/README.md „neuer Server"-Block): Clone auf `https://github.com/vibercoder79/intentron.git` (public, kein SSH nötig), `git sparse-checkout set bootstrap`, `cp -r bootstrap ~/.claude/skills/`.
- **README-Quickstart** (DE „Schnellstart" + EN „Quickstart"), prominent vor dem „Warum"-Abschnitt, mit drei Wegen:
  - **A) Manuell + `/bootstrap`** — der eine Shell-Befehl, danach Slash-Command (+ Hinweis Session-Restart für Command-Registrierung).
  - **B) AI-Self-Install-Prompt** — copy-paste in eine Claude-Code-Session: KI klont das public Repo, kopiert `bootstrap/` nach `~/.claude/skills/bootstrap/`, **liest dann SKILL.md und folgt ihr** (umgeht die Slash-Registrierungs-Verzögerung).
  - **C) AI-Self-Update-Prompt** — für alte/Brownfield-Installationen: Ist-Zustand analysieren (`.claude/`, Bootstrap-Version, Skills, Hooks), Gap gegen aktuelles `intentron` melden, dann updaten via Re-Clone + `bootstrap/scripts/migrate-to-v2.sh` (idempotent) + `bootstrap/references/verify-setup.sh`.
- **Note-Callout** (DE+EN): gleiches Ergebnis, A explizit/auditierbar, B schnellster Kaltstart, C Upgrade; Migrationen + verify-setup.sh idempotent.

## Constraints

- **Reine Doku/Onboarding**, kein Code-/Verhaltens-Change am Framework.
- **Public-Repo-Clone via https** (kein SSH-Setup nötig) — niedrigste Einstiegshürde.
- **Self-Install liest SKILL.md direkt** statt auf Session-Restart für die `/bootstrap`-Registrierung zu warten (robuster, kein hängender Schritt).
- **DE + EN paritätisch** (Quickstart, Prompts, Callout).
- **Self-Update nutzt bestehende, idempotente Werkzeuge** (`migrate-to-v2.sh`, `verify-setup.sh`) — keine neue Engine.

## Decisions

1. **Kanonische Skill-Quelle = `intentron`-Repo, `bootstrap/` im Root** (nicht claudecodeskills/intentron — existiert nicht). Single `git clone` ist self-contained (vendored Bundle-Skills, BOO-74).
2. **https statt SSH** im Quickstart/Prompt — public Repo, kein Key-Setup.
3. **Drei dokumentierte Wege statt einem** — bewusst, weil die Zielgruppen unterschiedlich sind (Hand-Install/Auditierbarkeit vs. schneller KI-Start vs. Brownfield-Upgrade).
4. **B liest SKILL.md** statt blind `/bootstrap` aufzurufen — vermeidet die Registrierungs-Race.

## Acceptance Criteria

1. Kein `sparse-checkout set intentron/bootstrap` / `cp -r intentron/bootstrap` mehr in HANDBUCH/README/bootstrap-README (grep = 0).
2. Install-Befehl zeigt überall auf `intentron.git` + sparse `bootstrap` (DE+EN, beide HANDBUCH-Stellen + bootstrap/README).
3. README hat `## Quickstart` (EN) + `## Schnellstart` (DE) mit Wegen A/B/C.
4. Prompts copy-paste-fähig; Self-Install liest SKILL.md; Self-Update referenziert migrate-to-v2.sh + verify-setup.sh.
5. DE/EN paritätisch; Release-Note v0.6.1 bilingual (Konvention Regel 6).

## Result

- Umgesetzt auf Branch `feat/boo-96-onboarding-prompts`. grep-Verifikation: 0 kaputte Pfade, 7 korrekte Clone-Befehle, Quickstart+Schnellstart vorhanden. Release: v0.6.1 (Wave AF).
