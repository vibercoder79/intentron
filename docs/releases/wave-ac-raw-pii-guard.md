# Wave AC — Raw-PII-in-Logs-Guard (BOO-93)

> 🌐 **Sprache:** Deutsch (diese Datei) · [🇬🇧 English](wave-ac-raw-pii-guard.en.md)

**Linear:** [BOO-93](https://linear.app/owlist/issue/BOO-93/) · Quelle: Upstream-Beitrag privacy-proxy / PP-004 (Martin), 2026-05-31 — Pattern nachgebaut, **kein PolyForm-Code uebernommen**

## Problem

Klartext-PII, die versehentlich in Logs landet (`logger.info("…", original_value=user.email)`),
ist ein faktisches Datenleck (DSGVO Art. 5 Datenminimierung / Art. 32 Sicherheit der Verarbeitung):
Logs werden gespeichert, an Monitoring geschickt, breit gelesen und selten geloescht. Fuer die
regulierte Zielgruppe (CH-Banken/Versicherer) ist das auditrelevant. Bisher fiel PII-in-Logs durch
**alle** Schichten: der Layer-0-Bodyguard (BOO-86) deckt Secrets/eval/TLS/SQL ab, **nicht**
Log-Senken; der dpo-Skill (BOO-87) liefert nur Review-/Doku-Guidance, kein Enforcement. Die
Ausbaustufe „Bodyguard-Warnung in PII-Pfaden" war in `v0.5.0-overview` nur als Idee vermerkt.

## Was sich aendert

- **Kanonischer Guard `bootstrap/references/hooks/raw-pii-guard.py`** (Single-Source) — ein
  statischer **AST**-Check (python3-Stdlib `ast`, kein Regex, kein Semgrep):
  - Erkennt Log-/Audit-Senken (`log.*`, `logger.*`, `audit.*`, `logging.*`, auch
    `self.audit_log.*`) ueber den Funktions-Root-Namen inkl. Attribut-Ketten.
  - Meldet verbotene **Keyword-Argumente, Attribut-Lesezugriffe und Variablen-Namen**
    (`original_value`, `plaintext`, `raw_value`, `cleartext`, `decrypted`, `unmasked` …).
  - **Default-Verbotsliste** bewusst spezifische Roh-/Klartext-Marker — **keine** generischen
    Feldnamen wie `email` (Fehlalarm-Vermeidung). AST ignoriert Kommentare/Strings → kaum
    Fehlalarme.
  - CLI: `[--strict] [--config PATH] [FILE …]`; ohne FILE werden die gestageten `*.py` geprueft.
    Eingebauter `--self-test`. Unparsebare Dateien (SyntaxError) werden uebersprungen.
- **Default = Warnung** (Exit 0), Hard-Block via `--strict` / `STRICT=1` / `RAW_PII_STRICT=1`
  (Exit 1) — konsistent mit BOO-86 gegen Alarm-Muedigkeit.
- **Projekt-Overlay** `.claude/raw-pii-guard.local` (eine Zeile pro Eintrag, `#`-Kommentare,
  Praefix `sink:` fuer zusaetzliche Senken) — Basis-+-Overlay-Muster analog BOO-86/BOO-87/BOO-91.
- **Opt-in Scaffolding:** `migrate_boo_93()` kopiert die kanonische Quelle byte-identisch nach
  `.claude/hooks/` (idempotent, Skip bei Byte-Gleichheit), mit `log_manual`-Hinweis zur
  Verdrahtung; `ALL_ISSUES`-Registrierung.
- **Doku** in `hooks-setup.md` (DE) + `hooks-setup.en.md` (EN): neue Sektion
  „Optional: raw-pii-guard.py" — was es tut, Aktivierung, lokale Pre-Commit-Nutzung,
  Overlay-Config, **optionaler CI-Workflow** `raw-pii-guard.yml` (opt-in), Querverweis dpo.
- **dpo-Querverweis** in `dpo/references/privacy-patterns.md`: der Guard ist die optionale
  automatische Enforcement-Schicht zur bestehenden PII-in-Logs-Review-Guidance.

## Designentscheid

- **Pattern aus PP-004 nachgebaut, kein Code uebernommen** (Hard-Constraint).
- **Engine = AST** statt Regex: praeziser bei Log-Senken (ignoriert Kommentare/Strings); bewusste
  Einfuehrung des ersten AST-Werkzeugs im Repo (Operator-Entscheid 2026-06-01).
- **Opt-in / Warn-Default** statt Pflicht-Hard-Fail — damit nichts Richtung Schwergewicht kippt.
- **Single-Source by construction:** der Guard existiert genau **einmal** (kanonisch unter
  `bootstrap/references/hooks/`) und wird von der Migration verbatim kopiert — kein Drift-Risiko.
  Eingehaengt in die bestehende Hook-/Migrations-Konvention, **nicht** als loses `ci/`-Paket.
- **Dependency-frei:** nur python3-Stdlib (`ast`).

## Verifiziert

- `--self-test`: Bad-Snippet liefert genau 3 Treffer (kwarg + attr + name), Good-Snippet 0
  (Kommentar/String/Nicht-Senke ignoriert).
- Externe Tests: `logger.info("x", original_value=user.email)` und
  `self.audit_log.write(record.plaintext)` werden erkannt; Kommentar `# original_value` und String
  `"raw_value"` nicht; sicherer Aufruf `logger.info(..., user_id=user.id)` nicht.
- `--strict` → Exit 1 bei Treffer; Default → Exit 0 (Warnung).
- Overlay `.claude/raw-pii-guard.local` (zusaetzliches Feld + `sink:`) greift.
- `migrate_boo_93` kopiert byte-identisch (`cmp -s`), ist idempotent (zweiter Lauf = Skip),
  gescaffoldeter Guard ist ausfuehrbar.
- DE/EN-Scaffolding aequivalent; `bash -n` fuer Migration; `git diff --check` clean.

## Rollout

Additiv und **opt-in**. Bestands- und Neu-Projekte aktivieren den Guard bewusst via
`migrate-to-v2.sh --issue BOO-93` (kopiert die kanonische Quelle) und verdrahten ihn in Pre-Commit
und/oder CI. Default = Warnung; `--strict` fuer Hard-Block. Projekte ohne PII lassen ihn inaktiv —
kein Effekt auf bestehende Pipelines.

## Effekt

Der klassische „Rohwert versehentlich geloggt"-Fehler hat erstmals einen automatischen, optionalen
Waechter — fuer regulierte Projekte auditrelevant, fuer PII-freie Projekte einfach inaktiv.

## Verweise

- Spec: `specs/BOO-93.md`
- Release-Ueberblick: `docs/releases/v0.6.0-overview.md` (Wave AC)
- Kanonischer Guard: `bootstrap/references/hooks/raw-pii-guard.py`
- Migration: `migrate_boo_93()` in `bootstrap/scripts/migrate-to-v2.sh`
- dpo-Querverweis: `dpo/references/privacy-patterns.md`
- Linear: BOO-93
