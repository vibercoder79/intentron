# Wave AA — CONTEXT.md Ubiquitous Language: kanonisches + verbotenes Vokabular (BOO-91)

**Linear:** [BOO-91](https://linear.app/owlist/issue/BOO-91/) · knüpft an BOO-21 (Domain-Context)

Stand: 2026-05-31

## Problem

Ohne festes Vokabular erfindet die KI Synonyme: mal `User`, mal `Customer`, mal `Betroffener`
für dieselbe Entität. Das erzeugt zwei Schäden:

- **Begriffs-Drift.** Dieselbe Sache heißt in fünf Dateien fünf verschiedene Namen → schlechte
  `grep`-Barkeit, schwerer Refactor, Misalignment zwischen Doku und Code, Token-Verschwendung
  (die KI rät bei jedem Lauf neu).
- **Schwache Compliance-Spur.** Bei regulierter Zielgruppe ist Vokabular rechtlich geladen:
  `Betroffener` ist ein definierter Begriff (DSGVO Art. 4), das Schweizer nDSG sagt
  `Bearbeitung` statt `Verarbeitung`. Ist das Vokabular nicht an die Rechtsgrundlage gebunden,
  ist es im Audit-Gespräch schwer belegbar.

Ubiquitous Language ist ein billiger Hebel mit hoher Wirkung — er blieb bisher ungenutzt.

## Lösung

Ein `CONTEXT.md`-Artefakt verankert die **Ubiquitous Language** (Domain-Driven Design) im
Projekt: eine Tabelle `kanonisch | verboten | quelle`. Zweischichtig — wie Edit-Bodyguard
(BOO-86) und dpo-Katalog (BOO-87):

- **Vorgefüllte Framework-Basis** `bootstrap/references/context-base.md` (+ `.en.md`) — kommt mit
  **Compliance-Vokabular** (`Betroffener`, `Bearbeitung`, `Auftragsverarbeiter`, `Einwilligung`,
  `personenbezogene Daten`) und **Governance-Vokabular** (`Story`, `Spec`, `Intent`, `Gate`,
  `Layer 0/2/3`, `BOO-<n>`). Jeder Eintrag trägt seine Quelle (DSGVO-Artikel / nDSG /
  INTENTRON-Governance) als Audit-Beleg.
- **Projekt-Overlay** `CONTEXT.md` im Projekt-Root — `migrate_boo_91()` seedet die Basis hinein
  und ergänzt eine leere Sektion `## Projekt-Domaene (vom Operator fuellen)`. Der Operator startet
  nicht bei null, sondern erweitert nur die Domänen-Sektion (z.B. `Police` statt `Vertrag` im
  Versicherungs-Kontext). Das Overlay **überlebt Framework-Updates — wird nie überschrieben**.

Die KI liest `CONTEXT.md` beim Schreiben (`CLAUDE.md`/`CONVENTIONS.md` verweisen darauf).
**Default = Guidance, kein Hard-Gate** — die KI wird geführt, nicht blockiert. Ein erzwingender
Block auf Vokabular-Ebene würde nur Reibung erzeugen (legitime Zitate, externe API-Felder) und
Operatoren zum Abschalten treiben.

## Migration

`bash bootstrap/scripts/migrate-to-v2.sh --issue BOO-91`

- Seedet `CONTEXT.md` im Projekt-Root **nur falls nicht vorhanden** (Basis + leere Domänen-Sektion).
- **Idempotent + additiv:** zweiter Lauf erkennt das vorhandene `CONTEXT.md` (`[SKIP]`), kein Diff;
  ein manuell ergänztes Overlay bleibt unverändert; `--dry-run` loggt nur (`[DRY]`).
- **Rollback:** `CONTEXT.md` löschen (Domänen-Overlay vorher sichern — die Basis liegt in
  `bootstrap/references/context-base.md`).

Verifikation: `test -f CONTEXT.md` (Exit 0); `grep -q 'Betroffener' CONTEXT.md` und
`grep -q 'Projekt-Domaene' CONTEXT.md` (Exit 0).

## Bezug Pocock-Pattern (kein Code)

Das Pattern ist inspiriert von Matt Pococks `skills`-Repo. Übernommen wurde ausschließlich das
**Pattern** (kanonisches + verbotenes Vokabular als Artefakt) — **kein Code**. Basis-Datei,
Schema, Seeding und Doku sind eigenständig erstellt; der Eigenbau passt zur INTENTRON-Architektur.
Hard-Constraint: kein Code aus Pococks Repo.

## Enforcement als spätere Ausbaustufe

Diese Wave liefert die **Guidance-Schicht**, nicht die Enforcement-Schicht. Bewusst out-of-scope,
für später (opt-in):

- **dpo-Control „Vokabular folgt CONTEXT.md"** — `grep`-absent der verbotenen Begriffe →
  `PASS`/`GAP` im AUDIT-Report (koppelt an BOO-87).
- **Layer-0-Bodyguard `warn`** auf verbotene Begriffe in PII-Pfaden (koppelt an BOO-86).

Erst Nutzen der Guidance-Schicht beweisen, dann die Enforcement-Kopplung spezifizieren.

## Konkrete Änderungen

| Bereich | Datei |
|---|---|
| Vorgefüllte Basis (DE+EN) | `bootstrap/references/context-base.md` + `.en.md` |
| Projekt-Migration | `migrate_boo_91` in `bootstrap/scripts/migrate-to-v2.sh` |
| Migration-Checklist §BOO-91 (DE+EN) | `bootstrap/references/migration-checklist-v1-to-v2.md` + `.en.md` |
| HANDBUCH Anhang X (DE+EN) | `HANDBUCH.md` + `.en.md` |
| Release Notes (DE+EN) | `docs/releases/wave-aa-context-ubiquitous-language.md` + `.en.md` |
| Spec | `specs/BOO-91.md` |

## Versions-Bump

- **bootstrap: 3.34.0 → 3.35.0**

## Verweise

- Spec: `specs/BOO-91.md`
- Basis: `bootstrap/references/context-base.md` (+ `.en.md`)
- HANDBUCH: Anhang X „CONTEXT.md — Ubiquitous Language"
- Migration: `migrate_boo_91` in `bootstrap/scripts/migrate-to-v2.sh`
- Knüpft an: BOO-21 (Domain-Context, Brücke über die Domänen-Sektion)
- Spätere Ausbaustufe: dpo-Control (BOO-87) / Layer-0-Bodyguard-`warn` (BOO-86) — kein Hard-Gate in dieser Wave
- Bezug: Matt Pococks `skills`-Repo (Ubiquitous-Language-Pattern) — nachgebaut, kein Code
- Linear: BOO-91
