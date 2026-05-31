# BOO-91 — CONTEXT.md Ubiquitous Language (kanonisches + verbotenes Vokabular)

## Summary

Ein `CONTEXT.md`-Artefakt, das die **Ubiquitous Language** aus Domain-Driven Design im Projekt verankert: eine Tabelle aus **kanonischem Vokabular** plus **Verbotsliste** von Synonymen, jeder Eintrag mit **Quelle**. Aufbau zweischichtig — analog Bodyguard (BOO-86) und dpo-Overlay (BOO-87): eine **vorgefuellte Framework-Basis** (`bootstrap/references/context-base.md`, DE+EN) plus ein **Projekt-Overlay** (`CONTEXT.md` im Projekt-Root, vom Operator gefuellt). Die KI liest `CONTEXT.md` beim Schreiben und haelt sich an das kanonische Vokabular. Das Pattern ist inspiriert von Matt Pococks `skills`-Repo — **nachgebaut, kein Code uebernommen** (Eigenbau passt zur INTENTRON-Architektur).

## Why

Ohne festes Vokabular erfindet die KI Synonyme: mal `User`, mal `Customer`, mal `Betroffener` fuer dieselbe Entitaet. Das fuehrt zu fragmentiertem Code, schlechter `grep`-Barkeit, Misalignment zwischen Doku und Implementierung und Token-Verschwendung (die KI muss bei jedem Lauf neu raten, welcher Begriff gemeint ist). Bei regulierter Zielgruppe ist Vokabular zusaetzlich **rechtlich geladen**: `Betroffener` ist ein definierter Begriff (DSGVO Art. 4), das Schweizer nDSG sagt `Bearbeitung` statt `Verarbeitung`. Konsequente Begriffe binden Code und Doku an die Rechtsgrundlage — das ist Auditor-relevant. Ein konsistentes Vokabular ist ein billiger Hebel mit hoher Wirkung.

Konsequenzen ohne diese Story:

- Begriffs-Drift: dieselbe Entitaet heisst in fuenf Dateien fuenf verschiedene Namen → schlechtes `grep`, schwerer Refactor
- Schwaechere Compliance-Spur: Vokabular ist nicht an die Rechtsgrundlage gebunden, im Audit-Gespraech schwer belegbar (z.B. nDSG-`Bearbeitung` vs. DSGVO-`Verarbeitung`)
- Token-Verschwendung: die KI raet bei jedem Lauf das gemeinte Synonym statt einen festen Begriff zu nutzen
- Ein billiger, hochwirksamer Hebel (Ubiquitous Language) bleibt ungenutzt — Asymmetrie zu BOO-21 Domain-Context, der das Domaenen-Wissen schon ablegt, aber das Vokabular nicht normiert

## What

- **Framework-Basis (VORGEFUELLT)** `bootstrap/references/context-base.md` (DE+EN) — eine Tabelle mit den Spalten `kanonisch | verboten | quelle`. Die Basis wird mit folgendem Seed-Vokabular ausgeliefert (mindestens diese Eintraege, jeder mit Quelle):

  **Compliance-Vokabular:**

  | kanonisch | verboten | quelle |
  | --- | --- | --- |
  | `Betroffener` | `User` / `Customer` / `Client` im PII-Kontext | DSGVO Art. 4 (betroffene Person) |
  | `Bearbeitung` | `Verarbeitung` | nDSG (Schweiz nutzt „Bearbeitung" statt „Verarbeitung") |
  | `Auftragsverarbeiter` | `Vendor` / `Dienstleister` | DSGVO Art. 28 |
  | `Einwilligung` | `Zustimmung` / `OK` | DSGVO Art. 6 / Art. 7 |
  | `personenbezogene Daten` | `PII` als Code-Begriff ohne Definition | DSGVO Art. 4 |

  **Governance-Vokabular:**

  | kanonisch | verboten | quelle |
  | --- | --- | --- |
  | `Story` | `Ticket` | INTENTRON-Governance |
  | `Spec` | `Anforderung` (lose) | INTENTRON-Governance |
  | `Intent` | `Ziel` (vage) | INTENTRON-Governance |
  | `Gate` | `Check` (generisch) | INTENTRON-Governance |
  | `Layer 0` / `Layer 2` / `Layer 3` | gemischte/uneinheitliche Layer-Benennung | INTENTRON Quality-Gate-Architektur |
  | `BOO-<n>` | freie Issue-Bezeichnung | Linear-Issue-Prefix |

- **Projekt-Overlay** `CONTEXT.md` im Projekt-Root: Bootstrap seedet die Basis hinein und ergaenzt eine **leere Sektion** `## Projekt-Domaene (vom Operator fuellen)`. Hier traegt der Operator domaenenspezifische Begriffe ein (z.B. `Police` statt `Vertrag` im Versicherungs-Kontext). Knuepft an BOO-21 Domain-Context an. Das Overlay **ueberlebt Framework-Updates** (Migration ueberschreibt es nie).
- **Referenzierung:** `CLAUDE.md`/`CONVENTIONS.md` verweisen auf `CONTEXT.md`, damit die KI es beim Schreiben liest. Default = **Guidance** (kein Hard-Gate) — die KI wird gefuehrt, nicht blockiert.
- **Ausbaustufen (optional, spaeter, NICHT in dieser Story):**
  - dpo-Control „Vokabular folgt CONTEXT.md": `grep`-absent der verbotenen Begriffe → `PASS`/`GAP` im AUDIT-Report (koppelt an BOO-87-Katalog).
  - Layer-0-Bodyguard `warn` auf verbotene Begriffe in PII-Pfaden (koppelt an BOO-86).
  Beide explizit als **out-of-scope** dieser Story benannt — diese Story liefert die Guidance-Schicht, nicht die Enforcement-Schicht.
- **HANDBUCH-Anhang X „CONTEXT.md Ubiquitous Language"** (DE+EN): was Ubiquitous Language ist, warum kanonisch + verboten + Quelle, wie Basis und Overlay zusammenspielen, dass Enforcement eine spaetere Ausbaustufe ist.
- **`migrate_boo_91()`** in `migrate-to-v2.sh`: idempotent, seedet `CONTEXT.md` **nur wenn es fehlt** — ein vorhandenes Overlay wird **nie ueberschrieben**.
- **migration-checklist** Eintrag §BOO-91 (DE+EN).
- **Release Notes** (DE+EN).

## Constraints

- **Designprinzip 2026-05-25 — leichtgewichtig:** Default ist **Guidance, kein Hard-Gate**. Ein erzwingender Block auf Vokabular-Ebene wuerde nur Reibung erzeugen (z.B. legitime Zitate, externe API-Felder) und Operatoren zum Abschalten treiben. Enforcement ist bewusst eine spaetere, opt-in Ausbaustufe.
- **Dependency-frei:** kein neues Tool, keine Library, keine Engine — nur ein Markdown-Artefakt plus Referenz-Verweis.
- **Pragma-Check:** die vorgefuellte Basis spart dem Operator Arbeit — er startet nicht bei null, sondern erweitert nur die Domaenen-Sektion.
- **Security-/Compliance-Check:** das Vokabular ist an die Rechtsgrundlage gekoppelt (jeder Compliance-Begriff traegt seine Quelle, z.B. DSGVO-Artikel / nDSG) und ist damit ueber den dpo-Katalog (BOO-87) spaeter pruefbar.
- **Mittelweg-Begruendung:** Basis fix (wiederverwendbares Compliance-/Governance-Vokabular), Domaene flexibel (Operator-Overlay). Kein starres Komplett-Vokabular, aber auch kein leeres Blatt.
- **DE + EN konsistent** (Basis-Datei, HANDBUCH-Anhang, migration-checklist, Release Notes).
- **Kein Code aus Pococks `skills`-Repo** — nur das Pattern nachgebaut. Hard-Constraint fuer jeden Sub-Agent.

## Decisions

1. **Zweischichtig Basis + Overlay** (analog BOO-86 Bodyguard, BOO-87 dpo-Overlay): Framework-Basis vorgefuellt, Projekt-Overlay vom Operator, Overlay ueberlebt Updates. Konsistentes Architektur-Bild ueber alle drei Artefakte.
2. **Basis vorgefuellt mit Compliance- + Governance-Vokabular** (nicht leer ausgeliefert): das Vokabular ist projektuebergreifend wiederverwendbar und spart Operator-Arbeit.
3. **Default Guidance statt Hard-Gate:** die KI wird gefuehrt (CONTEXT.md beim Schreiben gelesen), nicht blockiert. Verhindert Reibung und Abschalten.
4. **Enforcement (dpo-Control / Bodyguard-warn) bewusst als spaetere Ausbaustufe ausgegliedert:** diese Story liefert die Guidance-Schicht; die Enforcement-Kopplung an BOO-86/BOO-87 ist out-of-scope und separat zu spezifizieren.
5. **Jeder Begriff traegt seine Quelle** (`quelle`-Spalte Pflicht): Audit-Nachweis, jeder kanonische Begriff ist herkunftsbelegt (DSGVO-Artikel / nDSG / INTENTRON-Governance), kein „magisches" Vokabular.

## Agent-Pattern

**Gewaehltes Pattern:** sub-agents (sequentiell).

**Begruendung:** Mehrere klar abgegrenzte Brocken (Basis-Datei `context-base.md` mit Seed-Vokabular, Bootstrap-Seeding von `CONTEXT.md` + Domaenen-Sektion, CLAUDE.md/CONVENTIONS-Referenzierung, HANDBUCH-Anhang, Migration). Pro Brocken ein fokussierter Sub-Agent. **Hard-Constraint pro Sub-Agent: „kein Code aus Pococks `skills`-Repo — nur Pattern nachbauen"** und **„kein Vokabular erfinden, das nicht belegbar ist — jeder Eintrag braucht eine Quelle"** (Memory feedback_subagent_spec_fabrication). EN-Pass nicht im selben Sub-Agent wie der DE-Inhalt (Memory feedback_subagent_long_heredoc_timeout) — separater Pass pro Datei.

## Validation

- `context-base.md` (DE+EN) existiert, syntaktisch valide Markdown-Tabelle, vorgefuellt mit dem genannten Compliance- + Governance-Seed-Vokabular
- Jeder Eintrag in `context-base.md` hat eine ausgefuellte `quelle`-Spalte
- Bootstrap-Lauf seedet `CONTEXT.md` im Projekt-Root mit der Basis plus leerer `## Projekt-Domaene (vom Operator fuellen)`-Sektion
- `CLAUDE.md` und `CONVENTIONS.md` referenzieren `CONTEXT.md` (Verweis vorhanden)
- `migrate_boo_91()` seedet `CONTEXT.md` nur wenn es fehlt; ein vorhandenes Overlay wird nicht ueberschrieben (zweiter Lauf erzeugt keine Diffs, manuell ergaenztes Overlay bleibt unveraendert)
- HANDBUCH-Anhang X DE+EN, im Inhaltsverzeichnis verlinkt
- Enforcement-Ausbaustufen (dpo-Control, Bodyguard-warn) explizit als out-of-scope dokumentiert, nicht implementiert
- `git diff --check` clean

## Acceptance Criteria

- [ ] `bootstrap/references/context-base.md` (DE+EN) existiert und ist vorgefuellt mit dem Compliance-Vokabular (`Betroffener`, `Bearbeitung`, `Auftragsverarbeiter`, `Einwilligung`, `personenbezogene Daten`) und dem Governance-Vokabular (`Story`, `Spec`, `Intent`, `Gate`, `Layer 0/2/3`, `BOO-<n>`)
- [ ] Jeder Eintrag traegt eine Quelle (DSGVO-Artikel / nDSG / INTENTRON-Governance)
- [ ] Bootstrap seedet `CONTEXT.md` im Projekt-Root mit Basis + leerer `## Projekt-Domaene (vom Operator fuellen)`-Sektion
- [ ] `CLAUDE.md`/`CONVENTIONS.md` referenzieren `CONTEXT.md` (Default Guidance, kein Hard-Gate)
- [ ] `migrate_boo_91()` implementiert, idempotent, seedet `CONTEXT.md` nur wenn fehlend — Overlay wird nie ueberschrieben
- [ ] HANDBUCH-Anhang X „CONTEXT.md Ubiquitous Language" (DE+EN)
- [ ] migration-checklist Eintrag §BOO-91 (DE+EN)
- [ ] Release Notes (DE+EN)
- [ ] bootstrap-Versions-Bump
- [ ] Enforcement-Ausbaustufen (dpo-Control „Vokabular folgt CONTEXT.md", Layer-0-Bodyguard-warn) explizit als out-of-scope benannt, nicht implementiert
- [ ] `git diff --check` clean
- [ ] Manueller Smoke-Test: Bootstrap im Demo-Projekt erzeugt `CONTEXT.md` mit Basis + Domaenen-Sektion; zweiter Migrations-Lauf laesst ein manuell ergaenztes Overlay unveraendert

## Dependencies

- **Knuepft an BOO-21** (Domain-Context) — `CONTEXT.md` normiert das Vokabular, das BOO-21 als Domaenen-Wissen ablegt; die Domaenen-Sektion ist die Bruecke
- **Overlay-Muster aus BOO-86** (Layer-0 Bodyguard, Basis + `.local`-Overlay) als Architektur-Vorbild
- **dpo-Kopplung aus BOO-87** (Kontrollkatalog) als spaetere Enforcement-Ausbaustufe — `grep`-absent verbotener Begriffe als dpo-Control, out-of-scope dieser Story
- **Muster (kein Code):** Matt Pococks `skills`-Repo als Inspiration, nachgebaut — kein uebernommener Code

## Session-Referenz

Spec geschrieben in Session 2026-05-31 (Wettbewerbsanalyse Pocock / BMAD). Linear: <https://linear.app/owlist/issue/BOO-91/>.

## Rollout

Additiv und optional. Bestands-Projekte werden via `migrate_boo_91()` upgegradet (idempotent, additiv — seedet `CONTEXT.md` nur wenn fehlend, Overlay bleibt unangetastet). Default ist **Guidance** (kein Hard-Gate); die Enforcement-Kopplung an dpo/Bodyguard ist eine bewusst spaeter spezifizierte, opt-in Ausbaustufe.
