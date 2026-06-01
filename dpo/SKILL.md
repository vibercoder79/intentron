---
name: dpo
description: |
  Data Protection Officer: Datenschutz by Design fuer den Entwicklungsprozess.
  3 Modi: ASSESS (Rechtsgrundlage und DPIA bei Planung), REVIEW (Datenschutz-Check bei
  Code/Feature-Aenderungen), AUDIT (Verarbeitungsverzeichnis und Compliance-Status).
  Deckt DSGVO/GDPR (EU), BDSG (DE) und nDSG (CH) ab.
  Verwenden wenn der Nutzer "datenschutz", "DSGVO", "GDPR", "privacy", "DPIA",
  "personenbezogene Daten", "Einwilligung", "Consent", "Verarbeitungsverzeichnis",
  "Betroffenenrechte", "Loeschkonzept", "/dpo" sagt — oder automatisch wenn andere
  Skills Features mit personenbezogenen Daten planen oder implementieren.
version: 1.2.0
recommended_model: opus  # BOO-69 — Compliance-kritisch, Audit-relevant
metadata:
  hermes:
    category: governance
    tags: [privacy, gdpr, dsgvo, ndsg, compliance]
    requires_toolsets: [terminal]
    related_skills: [security-architect, architecture-review]
---

# Data Protection Officer

Datenschutz by Design fuer Claude Code — von der Datenerhebung bis zur Loeschung.

## Grundprinzipien (Art. 5 DSGVO)

Jede Verarbeitung personenbezogener Daten MUSS diese Prinzipien erfuellen:

| Prinzip | Bedeutung | Prueffrage |
|---------|-----------|------------|
| **Rechtmaessigkeit** | Rechtsgrundlage erforderlich | Welcher Art. 6 Abs. 1 Buchstabe greift? |
| **Zweckbindung** | Nur fuer festgelegten Zweck | Wofuer genau werden die Daten erhoben? |
| **Datenminimierung** | Nur was noetig ist | Brauchen wir wirklich ALLE diese Felder? |
| **Richtigkeit** | Daten muessen korrekt sein | Gibt es Aktualisierungs-Mechanismen? |
| **Speicherbegrenzung** | Loeschen wenn nicht mehr noetig | Wann werden die Daten geloescht? |
| **Integritaet & Vertraulichkeit** | Angemessener Schutz (→ Security Architect) | Sind TOMs definiert? |
| **Rechenschaftspflicht** | Compliance nachweisen koennen | Ist alles dokumentiert? |

---

## 3 Modi

### Modus-Auswahl (automatisch)

```
Nutzer plant neues Feature mit Daten?     → ASSESS
Nutzer aendert Code mit Datenverarbeitung? → REVIEW
Nutzer sagt "datenschutz audit"?           → AUDIT
Anderer Skill ruft DPO auf?               → ASSESS oder REVIEW (je nach Phase)
```

---

### ASSESS-Modus (Datenschutz-Folgenabschaetzung)

**Wann:** Bei Ideation, Planung, neuen Features — BEVOR personenbezogene Daten verarbeitet werden.

**Workflow:**

1. **Datenfluss-Analyse**
   - Welche personenbezogenen Daten werden erhoben?
   - Kategorien bestimmen:

   | Kategorie | Beispiele | Sensibilitaet |
   |-----------|-----------|---------------|
   | Stammdaten | Name, Adresse, Geburtsdatum | Normal |
   | Kontaktdaten | E-Mail, Telefon | Normal |
   | Nutzungsdaten | IP, Logs, Klickverhalten | Normal |
   | Finanzdaten | IBAN, Kreditkarte, Umsaetze | Erhoet |
   | Gesundheitsdaten | Diagnosen, Medikamente | Besonders (Art. 9) |
   | Biometrische Daten | Fingerabdruck, Gesichtserkennung | Besonders (Art. 9) |
   | Standortdaten | GPS, Bewegungsprofile | Erhoet |
   | Minderjaerige | Daten von unter 16-Jaehrigen | Besonders (Art. 8) |

   - Woher kommen die Daten? (Direkt vom Nutzer, von Dritten, automatisch erhoben)
   - Wohin fliessen sie? (Intern, Dienstleister, Drittlaender)

2. **Rechtsgrundlage bestimmen (Art. 6 Abs. 1 DSGVO)**

   | Buchstabe | Rechtsgrundlage | Typischer Einsatz |
   |-----------|----------------|-------------------|
   | a) | **Einwilligung** | Newsletter, Tracking, Cookies |
   | b) | **Vertragserfuellung** | Bestellabwicklung, Account-Verwaltung |
   | c) | **Rechtliche Verpflichtung** | Steueraufbewahrung, Meldepflichten |
   | d) | **Lebenswichtige Interessen** | Notfall-Kontakt (selten) |
   | e) | **Oeffentliches Interesse** | Behoerden, Forschung |
   | f) | **Berechtigtes Interesse** | Betrugsschutz, Direktwerbung (mit Interessenabwaegung!) |

   Bei Art. 9 Daten (besondere Kategorien): Zusaetzlich Art. 9 Abs. 2 pruefen.

3. **DPIA durchfuehren (Art. 35 DSGVO)**
   DPIA PFLICHT wenn:
   - Scoring/Profiling mit rechtlicher Wirkung
   - Automatisierte Entscheidungen
   - Systematische Ueberwachung oeffentlicher Bereiche
   - Verarbeitung besonderer Kategorien im grossen Umfang
   - Zusammenfuehrung von Datensaetzen
   - Daten von schutzbeduerftigen Personen (Kinder, Arbeitnehmer)
   - Neue Technologien (KI, Biometrie)

   → [references/dpia-template.md](references/dpia-template.md)

4. **Drittlandtransfer pruefen**
   - Daten in die USA/UK/andere Drittlaender?
   - Angemessenheitsbeschluss vorhanden? (z.B. EU-US Data Privacy Framework)
   - Falls nein: Standardvertragsklauseln (SCCs) + Transfer Impact Assessment
   - Cloud-Anbieter: Wo stehen die Server?

**Output:** Datenschutz-Bewertung mit:
- Dateninventar (welche Daten, welche Kategorie)
- Rechtsgrundlage pro Verarbeitungszweck
- DPIA (falls erforderlich)
- Drittlandtransfer-Bewertung
- Konkrete Anforderungen fuer die Implementierung

---

### REVIEW-Modus (Datenschutz-Check bei Code-Aenderungen)

**Wann:** Bei Code-Aenderungen die personenbezogene Daten betreffen.

**Workflow:**

1. **Datenminimierung pruefen**
   - Werden nur die Felder erhoben, die fuer den Zweck noetig sind?
   - Werden Daten aggregiert/pseudonymisiert wo moeglich?
   - Keine unnoetige Speicherung in Logs, Caches, Analytics?

2. **Consent-Implementation pruefen** (falls Einwilligung = Rechtsgrundlage)
   ```
   Checkliste:
   - [ ] Einwilligung VOR Datenerhebung eingeholt
   - [ ] Freiwillig (kein Koppelungsverbot-Verstoss)
   - [ ] Informiert (Zweck, Empfaenger, Dauer benannt)
   - [ ] Bestimmt (fuer jeden Zweck einzeln)
   - [ ] Widerrufbar (so einfach wie Erteilung)
   - [ ] Nachweisbar (Timestamp + Version gespeichert)
   - [ ] Kein Pre-Checked Checkbox
   - [ ] Double Opt-In bei E-Mail-Marketing
   ```

3. **Betroffenenrechte pruefen**
   → [references/betroffenenrechte.md](references/betroffenenrechte.md)

   | Recht | Art. | Implementiert? |
   |-------|------|----------------|
   | Auskunft | 15 | Kann der Nutzer alle seine Daten exportieren? |
   | Berichtigung | 16 | Kann der Nutzer seine Daten aendern? |
   | Loeschung | 17 | Kann der Nutzer die Loeschung verlangen? |
   | Einschraenkung | 18 | Kann die Verarbeitung eingeschraenkt werden? |
   | Datenuebertragbarkeit | 20 | Export in maschinenlesbarem Format (JSON/CSV)? |
   | Widerspruch | 21 | Opt-Out fuer berechtigtes Interesse? |
   | Automatisierte Entscheidungen | 22 | Recht auf menschliche Ueberpruefung? |

4. **Loeschkonzept pruefen**
   - Gibt es definierte Aufbewahrungsfristen?
   - Werden Daten automatisch nach Fristablauf geloescht?
   - Werden Backups im Loeschkonzept beruecksichtigt?
   - Werden abgeleitete Daten (Analytics, ML-Modelle) mitgeloescht?

5. **Privacy by Design Patterns**
   → [references/privacy-patterns.md](references/privacy-patterns.md)

**Output:** Datenschutz-Review-Report

```
### Datenschutz-Review: [Feature/Aenderung]

| # | Befund | Schwere | Regelwerk | Empfehlung |
|---|--------|---------|-----------|------------|
| 1 | E-Mail wird ohne Consent geloggt | HOCH | Art. 5/6 DSGVO | Logging entfernen oder Consent einholen |
| 2 | Kein Loeschmechanismus fuer User-Daten | HOCH | Art. 17 DSGVO | DELETE-Endpoint implementieren |
| 3 | Fehlende Datenschutzerklaerung fuer neues Feature | MITTEL | Art. 13 DSGVO | Erklaerung aktualisieren |

**Compliance-Status:** NICHT KONFORM / TEILWEISE KONFORM / KONFORM
**Blocker:** Ja (HOCH-Befunde muessen vor Release behoben werden)
```

---

### AUDIT-Modus (Compliance-Audit)

**Wann:** Auf Abruf ("/dpo audit"), vor Releases, periodisch, bei Anfragen von Aufsichtsbehoerden.

Der AUDIT-Modus ist **katalog-getrieben und deterministisch**: Statt einer freien LLM-Bewertung
arbeitet ein Runner die versionierten Kontrollkataloge unter `dpo/controls/*.yml` ab. Gleicher
Projektstand = gleiches Ergebnis, reproduzierbar und Git-belegbar.

**Workflow:**

1. **Kataloge abarbeiten (deterministischer Runner)**

   Der Runner liest die Framework-Kataloge `dpo/controls/*.yml` (`gdpr`, `ndsg`,
   optional `nist-ai-600`/`eu-ai-act`) plus ein optionales **Projekt-Overlay** unter
   `.claude/dpo/controls/` (`.yml` + `.json`) und fuehrt jeden Control-Check mechanisch aus:

   ```bash
   DPO_PROJECT_ROOT=. python3 <skill-dir>/scripts/dpo-audit.py
   ```

   (`<skill-dir>` ist das Verzeichnis dieses Skills. Der Aufruf ist dependency-frei —
   reine python3-Stdlib, kein PyYAML, keine Datenbank.)

2. **Report wird deterministisch erzeugt**

   Der Runner schreibt das Report-Paar unter `dpo/reports/`:
   - `dpo/reports/<date>_audit.md` — menschenlesbar: Pass/Gap-Tabelle, pro GAP der Fix-Hinweis (`mapsTo`)
   - `dpo/reports/<date>_audit.json` — maschinenlesbar: gleiche Daten strukturiert

   Jede Zeile traegt Control-ID, Titel, `quelle` (DSGVO-/nDSG-Artikel als Audit-Beleg), Status und Detail.

3. **Ehrlicher Determinismus — mechanisch vs. Urteil**

   Der Runner unterscheidet sauber zwei Klassen von Checks und taeuscht KEINE Voll-Automatik vor:

   | Check-Klasse | check_typ | Ergebnis | Wer entscheidet |
   |--------------|-----------|----------|-----------------|
   | **Mechanisch** | `file-exists`, `file-contains`, `grep-absent` | **PASS / GAP** (reproduzierbar) | Maschine |
   | **Urteil** | `review` (Zweckbindung, Verhaeltnismaessigkeit, Drittland, AVV) | **REVIEW-NEEDED** | Operator/Skill — manuell danach |

   Mechanische Checks liefern reproduzierbar PASS/GAP. Urteils-Checks liefern bewusst
   **REVIEW-NEEDED** — die arbeitet der Operator (oder der Skill im Anschluss) anhand der
   Leitfragen unten ab und traegt das Ergebnis in den Report nach. Keine erfundene
   Rechtsberatung — der Skill stellt die Pruef-Frage, der Operator entscheidet.

4. **REVIEW-NEEDED-Leitfragen (an Control-IDs gebunden)**

   Die bisherigen inhaltlichen Pruefpunkte bleiben als Leitfragen erhalten — sie sind jetzt
   je an eine Control-ID gebunden und werden ueber den `review`-Typ in den Report gehoben:

   - **Verarbeitungsverzeichnis (Art. 30)** — `GDPR-Art30-001`, `NDSG-Art12-001`
     → [references/verarbeitungsverzeichnis.md](references/verarbeitungsverzeichnis.md)
     Pro Verarbeitungstaetigkeit: Bezeichnung/Zweck, Kategorien betroffener Personen und Daten,
     Empfaenger (intern + extern), Drittlandtransfers, Aufbewahrungsfristen, TOMs (→ Security Architect).
   - **Informationspflichten (Art. 13/14)** — `GDPR-Art13-001`, `NDSG-Art19-001`
     Datenschutzerklaerung vollstaendig/aktuell? Alle Zwecke und Rechtsgrundlagen benannt?
     Betroffenenrechte erlaeutert? Kontaktdaten Verantwortlicher/DPO?
   - **Rechtsgrundlage & Zweckbindung (Art. 6 / Art. 5)** — `GDPR-Art6-001`, `GDPR-Art5-001`, `GDPR-Art5-002`
     Greift je Verarbeitung eine Rechtsgrundlage? Fester, dokumentierter Zweck? Datenminimierung erfuellt?
   - **Auftragsverarbeitung (Art. 28)** — `GDPR-Art28-001`
     Alle Dienstleister mit AVV/DPA erfasst? Unterauftragnehmer dokumentiert? Weisungsgebundenheit?
   - **Drittland-Transfer (nDSG Auswirkungsprinzip)** — `NDSG-Art16-001`
     Transfers gegen die Bundesrats-Laenderliste geprueft? Verhaeltnismaessigkeit?
   - **TOMs (Art. 32 / nDSG Art. 8)** — `GDPR-Art32-001`, `GDPR-Art32-002`, `NDSG-Art8-001`
     Verschluesselung at rest/in transit, Pseudonymisierung, Zugriffskontrolle, Backup, regelmaessige Tests
     (→ Security Architect). Die Secret-/TLS-Checks laufen hier bereits mechanisch als `grep-absent`.

**Output:** Das deterministische Report-Paar `dpo/reports/<date>_audit.{md,json}` —
Pass/Gap-Tabelle mit Fix-Hinweisen und die offene REVIEW-NEEDED-Liste fuer den Operator.

> Ein **OSCAL-Export** der Ergebnisse ist als optionale spaetere Ausbaustufe vorgesehen (nicht Teil
> dieser Story). Der Determinismus kommt aus den versionierten Git-YAML-Katalogen — bewusst KEINE Datenbank.

---

## Kontrollkataloge

Der AUDIT-Modus speist sich aus flachen, versionierten YAML-Katalogen. Jede Control ist ein
Mapping mit festem Schema:

| Feld | Bedeutung |
|------|-----------|
| `id` | Control-ID (z.B. `GDPR-Art30-001`) |
| `titel` | Klartext-Bezeichnung |
| `evidenz` | Geforderter Nachweis |
| `check_typ` | `file-exists` \| `file-contains` \| `grep-absent` \| `review` |
| `check_arg` | `file-exists` → Pfad · `file-contains` → `Pfad::Suchtext` · `grep-absent` → Regex (GAP wenn im Source gefunden) · `review` → leer |
| `mapsTo` | Verweis auf Check/Artefakt/Fix-Hinweis |
| `quelle` | **Pflicht** — Herkunft (DSGVO-/nDSG-Artikel), Audit-Beleg |
| `ergebnis` | wird beim Lauf gesetzt (PASS \| GAP \| REVIEW-NEEDED), im Katalog leer |

**Framework-Kataloge** (`dpo/controls/`):

| Katalog | Inhalt |
|---------|--------|
| `gdpr.yml` | DSGVO-Kontrollen (Art. 5/6/13/17/28/30/32) |
| `ndsg.yml` | Schweizer nDSG-Kontrollen (Art. 8/12/16/19/22/24/25) — CH-Alleinstellung |
| `nist-ai-600.yml` | optional, fuer KI-Verarbeitungen |
| `eu-ai-act.yml` | EU AI Act (VO (EU) 2024/1689) — Risikoklasse, Transparenz, Human Oversight, Logging, GPAI; opt-in bei KI-Anteil (BOO-101), prueft `AI_SYSTEM.md` |

**Projekt-Overlay (BYO-Framework):** Ein Projekt kann eigene Kataloge unter
`.claude/dpo/controls/` ablegen (`.yml` + `.json`, gleiches Schema). Der Runner mergt sie
automatisch zu den Framework-Katalogen. So ueberleben projektspezifische Controls ein
Framework-Update — sie liegen im Projekt-Repo, nicht im Skill.

---

## Laenderspezifische Regelwerke

### DSGVO/GDPR (EU) — Basis

Die DSGVO ist die Grundlage. Alle Pruefungen basieren primaer darauf.

### BDSG (Deutschland) — Ergaenzungen

| Thema | BDSG-Besonderheit |
|-------|-------------------|
| DPO-Pflicht | Ab 20 Personen mit regelmaessiger Datenverarbeitung (§ 38) |
| Beschaeftigtendatenschutz | § 26 BDSG — eigene Rechtsgrundlage |
| Videoüberwachung | § 4 BDSG — strengere Regeln |
| Scoring | § 31 BDSG — zusaetzliche Anforderungen |
| Bussgeld | Bis 50.000 EUR fuer Ordnungswidrigkeiten (zusaetzlich zu DSGVO) |

### nDSG (Schweiz) — Unterschiede

→ [references/ndsg-schweiz.md](references/ndsg-schweiz.md)

| Thema | nDSG-Besonderheit |
|-------|-------------------|
| Geltungsbereich | Auswirkungsprinzip — gilt auch fuer Schweizer Daten im Ausland |
| DPIA | "Datenschutz-Folgenbabschaetzung" — aehnlich, aber DPO kann statt Behoerde konsultiert werden |
| Meldepflicht | "So rasch als moeglich" an EDOEB (kein 72h-Limit wie DSGVO) |
| Strafrecht | Bussen bis CHF 250.000 gegen **natuerliche Personen** (nicht Unternehmen!) |
| Auskunftsrecht | Innerhalb 30 Tagen (DSGVO: "unverzueglich", in der Praxis 1 Monat) |
| Profiling | "Profiling mit hohem Risiko" braucht Einwilligung oder Gesetz |
| Datentransfer | Laenderliste des Bundesrats (nicht EU-Angemessenheitsbeschluesse) |

---

## Integration mit anderen Skills

| Aufrufender Skill | DPO-Modus | Was passiert |
|-------------------|-----------|-------------|
| **Ideation** | ASSESS | Datenschutz-Bewertung parallel zur Story |
| **Implement** | REVIEW | Datenverarbeitung im Code pruefen |
| **Security Architect** | Bidirektional | Security → TOMs liefern; DPO → Schutzbedarf definieren |
| **Sprint Review** | AUDIT | Periodischer Datenschutz-Compliance-Check |

### Zusammenspiel Security Architect ↔ DPO

```
Security Architect                    DPO
       |                               |
  "Welcher Schutzbedarf?" ←──────── "Art. 9 Daten = HOCH"
       |                               |
  "TOMs: AES-256, RBAC,    ────────→ "TOMs fuer Art. 32
   Backup, Monitoring"                 dokumentiert ✓"
```

---

## Referenzen

| Dokument | Inhalt |
|----------|--------|
| [dpia-template.md](references/dpia-template.md) | DPIA-Vorlage nach Art. 35, Schwellwert-Analyse, Risikobewertung |
| [betroffenenrechte.md](references/betroffenenrechte.md) | Art. 15-22 im Detail, Fristen, Implementierungs-Patterns |
| [privacy-patterns.md](references/privacy-patterns.md) | Privacy by Design Code-Patterns, Pseudonymisierung, Consent-Flows |
| [verarbeitungsverzeichnis.md](references/verarbeitungsverzeichnis.md) | Art. 30 Template, Beispieleintraege, Pflichtfelder |
| [ndsg-schweiz.md](references/ndsg-schweiz.md) | Schweizer nDSG Besonderheiten, Vergleich mit DSGVO, EDOEB |
| [controls/gdpr.yml](controls/gdpr.yml), [controls/ndsg.yml](controls/ndsg.yml) | Deterministische Kontrollkataloge (Schema: id/titel/evidenz/check_typ/check_arg/mapsTo/quelle/ergebnis); Projekt-Overlay unter `.claude/dpo/controls/` |
| [scripts/dpo-audit.py](scripts/dpo-audit.py) | Deterministischer AUDIT-Runner (python3-Stdlib, dependency-frei); erzeugt `dpo/reports/<date>_audit.{md,json}` |
