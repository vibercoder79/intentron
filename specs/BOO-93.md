# BOO-93 — Raw-PII-in-Logs-Guard (optionales AST-PII-Sink-Gate)

## Summary

Ein **optionaler** statischer AST-Check (`raw-pii-guard.py`), der meldet, wenn Quellcode ein PII-tragendes Feld in eine Log-/Audit-Senke (`log.*()`, `logger.*()`, `audit.*()`, `logging.*()`) gibt — als verbotenes Keyword-Argument, Attribut-Lesezugriff oder Variablen-Name (`original_value`, `plaintext`, `raw_value` …). Realisiert die in `v0.5.0-overview` vorgemerkte Ausbaustufe „Layer-0-Bodyguard-Warnung in PII-Pfaden". **AST statt Regex** (ignoriert Kommentare/Strings, kaum Fehlalarme), **dependency-frei** (python3-Stdlib), **Default = Warnung** (Hard-Block nur via `--strict`/`STRICT=1`, konsistent mit BOO-86). Quelle: Upstream-Beitrag privacy-proxy / PP-004 (Martin), 2026-05-31 — Pattern nachgebaut, **kein PolyForm-Code übernommen**.

## Why

Klartext-PII in Logs ist ein faktisches Datenleck: Logs werden gespeichert, an Monitoring geschickt, breit gelesen und selten gelöscht (DSGVO Art. 5 Datenminimierung / Art. 32 Sicherheit der Verarbeitung). Für die regulierte Zielgruppe (CH-Banken/Versicherer) ist das auditrelevant. Heute fällt PII-in-Logs durch **alle** Schichten: der Layer-0-Bodyguard (BOO-86) fängt Secrets/eval/TLS/SQL, **nicht** Log-Senken; der dpo-Skill (BOO-87) behandelt PII-Logging nur als Review-/Doku-Guidance, nicht als Enforcement. Es gibt also keinen automatischen Wächter, der den klassischen „versehentlich den Rohwert geloggt"-Fehler abfängt. Die Richtung war bereits geplant (`docs/releases/v0.5.0-overview.md`) — diese Story macht aus der Notiz eine Umsetzung.

## What

- **Kanonischer Guard** `bootstrap/references/hooks/raw-pii-guard.py` (Single-Source):
  - AST-Parsing (python3-Stdlib `ast`). Erkennt Aufrufe, deren Funktions-Root-Name eine Senke ist (`log`, `logger`, `logging`, `audit`, `audit_log`, … — auch `self.logger.info`), und prüft die Argumente auf (1) verbotene Keyword-Argumente, (2) verbotene Attribut-Lesezugriffe (`user.original_value`), (3) verbotene Variablen-Namen.
  - **Default-Verbotsliste** bewusst spezifische Roh-/Klartext-Marker (`original_value`, `plaintext`, `raw_value`, `cleartext`, `decrypted`, `unmasked`, …) — **keine** generischen Feldnamen wie `email` (Fehlalarm-Vermeidung).
  - **Projekt-Overlay** `.claude/raw-pii-guard.local` (eine Zeile pro Eintrag, `#`-Kommentare, Präfix `sink:` für zusätzliche Senken) — Basis-+-Overlay-Muster analog BOO-86/BOO-87/BOO-91.
  - CLI: `[--strict] [--config PATH] [FILE …]`; ohne FILE werden die gestageten `*.py` geprüft. `--self-test` für internen Selbsttest.
  - Default = Warnung (Exit 0); `--strict` bzw. `STRICT=1`/`RAW_PII_STRICT=1` → Exit 1.
  - Unparsebare Dateien (SyntaxError) werden übersprungen (kein harter Abbruch).
- **Scaffolding/Doku** `hooks-setup.md` (DE) + `hooks-setup.en.md` (EN): neue Sektion „Optional: raw-pii-guard.py" — was es tut, Aktivierung (Migration), lokale Pre-Commit-Nutzung, Overlay-Config, **optionaler CI-Workflow** `raw-pii-guard.yml` (opt-in), Querverweis dpo.
- **`migrate_boo_93()`** in `migrate-to-v2.sh`: opt-in Scaffold — kopiert die kanonische `raw-pii-guard.py` byte-identisch nach `.claude/hooks/` (idempotent, Skip bei Byte-Gleichheit), `log_manual`-Hinweis zur Verdrahtung. `ALL_ISSUES`-Registrierung.
- **dpo-Querverweis** in `dpo/references/privacy-patterns.md`: der Guard ist die optionale automatische Enforcement-Schicht zur bestehenden PII-in-Logs-Review-Guidance.
- **Release Notes** v0.6.0.

## Constraints

- **Opt-in & leichtgewichtig:** für Projekte ohne PII inaktiv; kein Pflicht-Gate. Default = Warnung gegen Alarm-Müdigkeit (BOO-86-Linie), Hard-Block nur opt-in.
- **Dependency-frei:** nur python3-Stdlib (`ast`) — kein Semgrep, kein externer Scanner, keine Library.
- **Single-Source by construction:** der Guard existiert genau **einmal** (kanonisch unter `bootstrap/references/hooks/`) und wird von der Migration verbatim kopiert — keine eingebettete Zweitkopie, daher kein Drift-Risiko (anders als coverage-check vor BOO-89). Kein loses `ci/`-Paket (wie im Feld-Vorschlag), sondern eingehängt in die bestehende Hook-/Migrations-Konvention.
- **AST statt Regex:** präziser bei Log-Senken (ignoriert Kommentare/Strings) — bewusste Einführung des ersten AST-Werkzeugs im Repo (alle bisherigen Checks sind regex/grep-basiert). Operator-Entscheid 2026-06-01.
- **Kein PolyForm-Code übernommen** — nur das Pattern nachgebaut (Hard-Constraint).
- **DE + EN konsistent** (Scaffolding-Doku).

## Decisions

1. **Opt-in Add-on, Default = Warnung** (nicht Hard-Build-Fail by default) — konsistent mit BOO-86, gegen Alarm-Müdigkeit.
2. **Engine = AST** (nicht Regex, nicht nur dpo-Control): bei Log-Senken deutlich präziser; bewusste Einführung des ersten AST-Werkzeugs (Operator-Entscheid).
3. **In bestehende Konventionen einhängen** (kanonische Quelle + Migration + optionaler CI-Workflow nach Muster `semgrep.yml`) statt loses `ci/`-Python-Paket.
4. **Verbotsliste spezifisch** (Roh-/Klartext-Marker), **konfigurierbar** über `.claude/raw-pii-guard.local` (Basis-+-Overlay) — niedrige Fehlalarm-Quote, projekt-erweiterbar.
5. **Senken-Erkennung über Root-Namen** (`logger`, `log`, `audit`, …), inkl. Attribut-Ketten (`self.audit_log.write`).

## Agent-Pattern

**Gewähltes Pattern:** `sub-agents` (Story Points 3) — geplant. **Tatsächliche Ausführung:** der Kern (AST-Scanner) wurde vom Orchestrator direkt geschrieben und mit einem eingebauten `--self-test` plus externen Fällen verifiziert (Korrektheit ist das kritische Element); die übrigen Artefakte (Migration, bilinguale Doku, Spec) folgten linear, da der Orchestrator den vollständigen Kontext hielt und Sub-Agent-Overhead den Nutzen überstiegen hätte. Hard-Constraint durchgängig: kein PolyForm-Code, nur Pattern nachgebaut.

## Validation

- `--self-test`: Bad-Snippet liefert genau 3 Treffer (kwarg + attr + name), Good-Snippet 0 (Kommentar/String/Nicht-Senke ignoriert).
- Externe Tests: `logger.info("x", original_value=user.email)` und `self.audit_log.write(record.plaintext)` werden erkannt; Kommentar `# original_value` und String `"raw_value"` nicht; sicherer Aufruf `logger.info(..., user_id=user.id)` nicht.
- `--strict` → Exit 1 bei Treffer; Default → Exit 0 (Warnung).
- Overlay `.claude/raw-pii-guard.local` (zusätzliches Feld + `sink:`) greift.
- `migrate_boo_93` kopiert byte-identisch (`cmp -s`), ist idempotent (zweiter Lauf = Skip), gescaffoldeter Guard ist ausführbar.
- DE/EN-Scaffolding äquivalent; `bash -n` für Migration; `git diff --check` clean.

## Acceptance Criteria

- [ ] `bootstrap/references/hooks/raw-pii-guard.py` (AST, python3-Stdlib) erkennt verbotene Felder in Log-/Audit-Senken (kwarg/attr/name)
- [ ] Default = Warnung; `--strict`/`STRICT=1` → Exit 1; `--self-test` grün
- [ ] Treffer in Kommentaren/Strings/Nicht-Senken werden nicht gemeldet (AST)
- [ ] Verbotsliste über `.claude/raw-pii-guard.local` konfigurierbar (Feld + `sink:`)
- [ ] `hooks-setup.md` (DE) + `.en.md` (EN): Sektion „Optional: raw-pii-guard" inkl. optionalem CI-Workflow
- [ ] `migrate_boo_93()` opt-in, kopiert kanonisch byte-identisch, idempotent, in `ALL_ISSUES`
- [ ] dpo-Querverweis (`privacy-patterns.md`)
- [ ] Release Notes (v0.6.0)
- [ ] `git diff --check` clean

## Dependencies

Realisiert die in `docs/releases/v0.5.0-overview.md` vorgemerkte Enforcement-Ausbaustufe „Bodyguard-Warnung in PII-Pfaden". Verwandt mit **BOO-86** (Layer-0-Bodyguard — gleiche warn-Default-Linie, andere Pattern-Klasse), **BOO-87** (dpo-Kontrollkatalog — Audit-Zeit-Pendant, mögliche spätere `grep-absent`-Control), **BOO-91** (CONTEXT.md-PII-Vokabular als mögliche spätere Quelle der Verbotsliste), **BOO-89** (Single-Source-Prinzip). Keine Blocker.

## Session-Referenz

Spec geschrieben + umgesetzt in Session 2026-06-01 (Abgleich + Umsetzung Upstream-Feedback privacy-proxy / PP-004). Linear: <https://linear.app/owlist/issue/BOO-93/>.

## Rollout

Additiv und **opt-in**. Bestands- und Neu-Projekte aktivieren den Guard bewusst via `migrate-to-v2.sh --issue BOO-93` (kopiert die kanonische Quelle) und verdrahten ihn in Pre-Commit und/oder CI. Default = Warnung; `--strict` für Hard-Block. Projekte ohne PII lassen ihn inaktiv — kein Effekt auf bestehende Pipelines.
