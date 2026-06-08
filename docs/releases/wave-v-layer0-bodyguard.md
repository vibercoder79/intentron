# Release Notes - Wave V Layer-0 Edit-Bodyguard

> 🌐 **Sprache:** Deutsch (diese Datei) · [🇬🇧 English](wave-v-layer0-bodyguard.en.md)

Stand: 2026-05-31

## Zweck

Wave V (BOO-86) gibt dem Framework einen neuen **Layer 0**: einen Claude-Code-PreToolUse-Hook auf `Edit|Write|MultiEdit`, der unsichere Muster (Secrets, `eval`, abgeschaltete TLS-Pruefung, SQL-Konkatenation) abfaengt, **bevor** die KI sie auf die Platte schreibt. Geschwister-Hook zu `spec-gate.sh` (der auf `Bash`/`git commit` feuert). Damit ist Security **ab Erzeugung** statt erst ab Commit verankert.

## Warum

Heute pruefen Linter erst **nach** der Implementierung (Layer 2: CLI-Linter vor Commit) bzw. in CI (Layer 3). Die **Erzeugungs-Luecke** — der Moment, in dem unsicherer Code ueberhaupt erst entsteht — blieb offen. Schraders Kern ist aber "sicher ab Erzeugung", nicht "sicher ab Commit". Ein bereits geschriebenes Secret muss erkannt, entfernt und ggf. rotiert werden — teurer Rueckbau gegenueber "gar nicht erst entstehen". Der Bodyguard sitzt vor dem Schreib-Vorgang der KI und blockiert/warnt, bevor das Muster auf der Platte landet. Das ist der USP "Security ab Generierung".

## Designentscheid

- **Default = Warnung, Hard-Block opt-in.** Kuratiert + low-false-positive. Bei zu vielen Fehlalarmen entsteht Alarm-Muedigkeit → Operatoren schalten den Hook ab → Schutz auf null. Hard-Block nur via `BODYGUARD_STRICT=1` fuer Projekte mit hoeherem Compliance-Druck.
- **Reflex statt Tiefenpruefung.** Layer 0 ist ein schneller, deterministischer Reflex auf eine kleine kuratierte Muster-Menge — **kein** voller Semgrep-Lauf pro Edit. Die Tiefe (Datenfluss, vollstaendiger Scan) bleibt bei Layer 2/3.
- **Basis + Overlay.** Framework-Basis-Muster + Projekt-Overlay `.claude/bodyguard.local.yml` (Kunde erweitert/uebersteuert per `name`, ueberlebt Framework-Updates — Kunden-Eigentum, wird nie ueberschrieben).
- **Quelle pro Muster ist Pflicht.** Jedes Muster traegt im `quelle`-Feld seinen Beleg (CWE / OWASP / gitleaks / Semgrep-Registry / Bandit / eslint-plugin-security) — Audit-Nachweis, keine "magischen" Regexe.
- **Dependency-frei.** Nur `bash` + `python3`-Stdlib; ein Mini-YAML-Parser im Hook (kein PyYAML noetig).

## Bezug agentic-security (PolyForm)

Das Pattern wurde aus `agentic-security` ("pre-edit-bodyguard") **nachgebaut** — **kein Code uebernommen**. `agentic-security` steht unter PolyForm-Lizenz; uebernommen wurde ausschliesslich die **Idee** eines Layer-0-Edit-Hooks. Muster, Schema, Hook-Logik und Doku sind eigenstaendig aus oeffentlichen Katalogen (CWE/OWASP/gitleaks/Semgrep) erstellt. Hard-Constraint der Story: kein PolyForm-Code im Repo.

## Was Nutzer bekommen

- **`.claude/hooks/pre-edit-bodyguard.sh`** — der Hook: liest stdin-JSON (`tool_input` mit `file_path` + `content`/`new_string`/`edits`), waehlt die Muster-Datei per Datei-Endung, matcht. Exit 1 = blockiert (Begruendung an Claude), Exit 0 = erlaubt.
- **`.claude/hooks/bodyguard/patterns/_universal.yml`** — Secrets, sprachunabhaengig (AWS-Key, Private-Key-Block, Slack-/GitHub-Token, generische Secret-Zuweisung).
- **`.claude/hooks/bodyguard/patterns/{python,javascript,java,c-cpp}.yml`** — sprachspezifische Unsafe-Code-Muster (z.B. `subprocess shell=True`, `verify=False`, `rejectUnauthorized: false`, `Runtime.exec`, `gets`/`strcpy`).
- **`.claude/hooks/bodyguard/SOURCES.md`** — Herkunft, Quellen-Tabelle und Pflege-Konvention (kuratiert + klein halten, kein Auto-Merge externer Muster).
- **`.claude/bodyguard.local.yml`** — optionales Projekt-Overlay (Kunden-Eigentum, ueberlebt Updates).
- **`migrate_boo_86`** — idempotente, additive Migration fuer Bestands-Projekte (siehe unten).

## Migration

`bash bootstrap/scripts/migrate-to-v2.sh --issue BOO-86`

- Legt Hook, Muster-Kataloge und `SOURCES.md` an (nur falls nicht vorhanden), `chmod +x` auf den Hook.
- Legt das Overlay `.claude/bodyguard.local.yml` **nur** an, wenn es fehlt — vorhandenes Kunden-Overlay wird **nie** ueberschrieben.
- Registriert den `Edit|Write|MultiEdit`-Matcher in `.claude/settings.json` **und** `.claude/settings.local.json` — idempotent, nur ergaenzend; bestehende `Bash`-Matcher (z.B. `spec-gate.sh`) bleiben unangetastet.
- **Idempotent:** zweiter Lauf erzeugt keine Diffs (Dateien + Registrierung werden erkannt, `[SKIP]`).

Verifikation: `bash -n .claude/hooks/pre-edit-bodyguard.sh` (Exit 0); Smoke-Test mit einem Test-Secret in einer `.py`/`.js` → Exit 1 (`[BODYGUARD] BLOCKIERT`); sauberer Code → Exit 0. Rollback: Hook + `bodyguard/`-Verzeichnis loeschen und den `Edit|Write|MultiEdit`-Block aus beiden settings-Dateien entfernen.

## Konkrete Aenderungen

| Bereich | Datei |
|---|---|
| Hook + Muster-Kataloge + SOURCES + Overlay (Templates) | `bootstrap/references/file-templates.md` §hooks/pre-edit-bodyguard.sh |
| Migration | `migrate_boo_86` in `bootstrap/scripts/migrate-to-v2.sh` (+ `ALL_ISSUES`) |
| Migration-Checklist §BOO-86 (DE+EN) | `bootstrap/references/migration-checklist-v1-to-v2.md` + `.en.md` |
| Spec | `specs/BOO-86.md` |

## Skill-Versions-Bumps

- keine (Hook-Templates + Migration + Doku, kein Skill-Code-Change)

## Verweise

- Spec: `specs/BOO-86.md`
- Kanonische Templates: `bootstrap/references/file-templates.md` §hooks/pre-edit-bodyguard.sh
- Muster-Quellen: `.claude/hooks/bodyguard/SOURCES.md` (CWE/OWASP/gitleaks/Semgrep)
- ADR: `02 Projekte/Code-Crash Framework/Decisions/2026-05-31 agentic-security-Adoption Bodyguard + dpo-Katalog.md`
- Bezug: `agentic-security` ("pre-edit-bodyguard") — Pattern nachgebaut, kein Code (PolyForm-Lizenz)
- Linear: BOO-86
