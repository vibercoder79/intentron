# Wave AF — Onboarding-Fix: Install + Quickstart + Self-Install/Self-Update (BOO-96)

> 🌐 **Sprache:** Deutsch (diese Datei) · [🇬🇧 English](wave-af-onboarding-fix.en.md)

**Linear:** [BOO-96](https://linear.app/owlist/issue/BOO-96/) · Quelle: Onboarding-Frage Operator, 2026-06-01

## Problem

Der dokumentierte Installations-Befehl war nach dem Rebrand (code-crash-framework → `intentron`)
kaputt: HANDBUCH §4 Schritt 3 (DE+EN) klonte `vibercoder79/claudecodeskills` und nutzte den Pfad
`intentron/bootstrap` — den es dort nicht gibt (verifiziert per GitHub-API: kein `intentron/`-Ordner,
nur `code-crash-framework/`, 404). Der Bootstrap-Skill liegt im public Repo
**`vibercoder79/intentron` direkt im Root** (`bootstrap/SKILL.md`). Ein neuer Nutzer bekam
„No such file or directory". Zusaetzlich verlinkte die README-Sektion „Wo anfangen?" nur
`/bootstrap` — einen Slash-Command, der erst existiert, wenn der Skill installiert ist — ohne den
vorgelagerten Install-Schritt. Der Einstieg lief ins Leere.

## Stories

| Story | Inhalt | Status |
|-------|--------|--------|
| **BOO-96** | Install-Befehl korrigieren + sichtbarer README-Quickstart + AI-Self-Install- und AI-Self-Update-Prompts | ✅ done |

## Was sich aendert

- **Install-Befehl korrigiert** (HANDBUCH.md + HANDBUCH.en.md, je Schritt 3 + Update-Anhang;
  bootstrap/README „neuer Server"-Block): Clone auf
  `https://github.com/vibercoder79/intentron.git` (public, kein SSH noetig),
  `git sparse-checkout set bootstrap`, `cp -r bootstrap ~/.claude/skills/`.
- **README-Quickstart** (DE „Schnellstart" + EN „Quickstart"), prominent vor dem
  „Warum"-Abschnitt, mit drei Einstiegswegen:
  - **A) Manuell + `/bootstrap`** — der eine Shell-Befehl, danach Slash-Command (+ Hinweis
    Session-Restart fuer Command-Registrierung).
  - **B) AI-Self-Install-Prompt** — copy-paste in eine Claude-Code-Session: KI klont das public
    Repo, kopiert `bootstrap/` nach `~/.claude/skills/bootstrap/`, **liest dann SKILL.md und
    folgt ihr** (umgeht die Slash-Registrierungs-Verzoegerung).
  - **C) AI-Self-Update-Prompt** — fuer alte/Brownfield-Installationen: Ist-Zustand analysieren
    (`.claude/`, Bootstrap-Version, Skills, Hooks), Gap gegen aktuelles `intentron` melden, dann
    updaten via Re-Clone + `bootstrap/scripts/migrate-to-v2.sh` (idempotent) +
    `bootstrap/references/verify-setup.sh`. Sicherer gestufter Flow nach
    `bootstrap/references/framework-upgrade.md` (inspect → apply-safe → apply-with-confirmation;
    ueberschreibt lokale Entscheidungen/Secrets nie blind).
- **Note-Callout** (DE+EN): gleiches Ergebnis, A explizit/auditierbar, B schnellster Kaltstart,
  C Upgrade; Migrationen + verify-setup.sh idempotent.

## Designentscheid

- **Kanonische Skill-Quelle = `intentron`-Repo, `bootstrap/` im Root** (nicht
  claudecodeskills/intentron — existiert nicht). Single `git clone` ist self-contained
  (vendored Bundle-Skills, BOO-74).
- **https statt SSH** im Quickstart/Prompt — public Repo, kein Key-Setup, niedrigste Huerde.
- **Drei dokumentierte Wege statt einem** — bewusst, weil die Zielgruppen unterschiedlich sind
  (Hand-Install/Auditierbarkeit vs. schneller KI-Start vs. Brownfield-Upgrade).
- **B liest SKILL.md direkt** statt blind `/bootstrap` aufzurufen — vermeidet die
  Registrierungs-Race.

## Verifiziert

- Kein `sparse-checkout set intentron/bootstrap` / `cp -r intentron/bootstrap` mehr in
  HANDBUCH/README/bootstrap-README (grep = 0).
- Install-Befehl zeigt ueberall auf `intentron.git` + sparse `bootstrap` (DE+EN, beide
  HANDBUCH-Stellen + bootstrap/README): 7 korrekte Clone-Befehle.
- README hat `## Quickstart` (EN) + `## Schnellstart` (DE) mit Wegen A/B/C.
- Prompts copy-paste-faehig; Self-Install liest SKILL.md; Self-Update referenziert
  migrate-to-v2.sh + verify-setup.sh. DE/EN paritaetisch.

## Effekt

Der Einstieg funktioniert wieder fuer frische Nutzer, ist sichtbar, und es gibt jetzt drei Wege —
Hand-Install, KI-Selbst-Install und KI-Selbst-Update einer Altinstallation. Reine Doku, kein
Verhaltens-Change.

## Verweise / Release

- Branch `feat/boo-96-onboarding-prompts`. Release: **v0.6.1 (Wave AF)** — siehe
  `docs/releases/v0.6.1-overview.md`, Detail-Spec `specs/BOO-96.md`.
