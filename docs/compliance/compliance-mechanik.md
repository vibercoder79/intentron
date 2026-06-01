# Compliance-Mechanik — End-to-End

![Compliance-Mechanik — Lebenszyklus (/ideation → /implement → /sprint-review) × Gates/Kataloge × Privacy/EU AI Act](../assets/compliance-mechanik.png)

*Gates (per Commit, harter Stopp) vs. Kataloge (periodischer Audit); automatisch vs. REVIEW-NEEDED (menschliche Entscheidung). ([Excalidraw-Quelle](../assets/compliance-mechanik.excalidraw))*

> **Zweck.** Dieses Dokument zeigt einem CISO/CIO/Operator in **einem** Blick, *wie* Compliance im
> Framework greift — über den gesamten Lebenszyklus einer Änderung, von der Idee bis zum periodischen
> Audit. Es erfindet nichts dazu: Es bündelt die bereits vorhandenen Mechanismen (Gates, Hooks,
> Kontrollkataloge) zu einer prüfbaren Gesamtsicht.
>
> Vertiefung: Wo die Belege landen → [docs/runbooks/audit-perspective.md](../runbooks/audit-perspective.md) ·
> Privacy-Hintergrund → HANDBUCH **Anhang O** (Privacy by Design, BOO-69) ·
> Skill-Details → [dpo/SKILL.md](../../dpo/SKILL.md).

---

## 1. Zwei Mechanismen — und wofür sie da sind

Compliance greift im Framework über **zwei verschiedene Mechanismen**. Sie ergänzen sich, ersetzen
sich aber **nicht** gegenseitig.

### Gates — der harte Stopp pro Code-Änderung

Ein **Gate** wirkt **pro Code-Änderung** und ist ein **HARTER STOPP** im `/implement`-Lauf. Trifft
eine geänderte Datei ein definiertes Muster, hält das Gate den Commit an, bis ein **Mensch**
bestätigt. Es gibt keine Ausnahme, keinen Auto-Bypass.

| Gate | `/implement`-Schritt | Bedingung | Bestätigung | Beleg |
|------|----------------------|-----------|-------------|-------|
| **Sensitive-Paths-Gate** (BOO-18) | Schritt **5.5** | `.claude/sensitive-paths.json` vorhanden **und** geänderte Datei trifft ein Pattern | `review-ok: {Name} - {Kommentar}` | `## Human Review` im Spec-File |
| **Personal-Data-Paths-Gate** (BOO-69) | Schritt **5.5b** | Story-Frontmatter `personal_data: true` **und** `.claude/personal-data-paths.json` vorhanden **und** Pattern-Treffer | `privacy-ok: {Name} - {Kommentar}` **oder** DPO-REVIEW-Report | `## Privacy Review` im Spec-File |

Flankierend, ebenfalls als deterministischer Schutz **vor** dem Schreiben:

- **Layer-0-Edit-Bodyguard** (BOO-86) — deterministischer Backstop, der riskante Muster
  (hardcoded Secrets, abgeschaltete TLS-Verifikation, `eval`/`exec` auf Fremd-Input) abfängt,
  *bevor* sie geschrieben werden. Siehe HANDBUCH Anhang V.
- **raw-pii-guard** (BOO-93, optional, Privacy-Add-on) — AST-Hook gegen Roh-/Klartext-PII in
  Log-Senken.

> **Merksatz:** Gates = per-Code, harter Stopp, ein Mensch muss bestätigen.

### Kataloge — der periodische Doku-/Prozess-Audit

Ein **Katalog** ist kein Code-Stopp, sondern ein **periodischer Audit** im `/sprint-review`
(Schritt **7c**). Ein deterministischer Runner, `dpo-audit.py`, arbeitet versionierte
YAML-Kontrollkataloge ab und meldet pro Control einen Status: **PASS**, **GAP** oder
**REVIEW-NEEDED**.

- **Framework-Kataloge:** `dpo/controls/` (`gdpr.yml`, `ndsg.yml`, optional `nist-ai-600.yml`).
- **Projekt-Overlay (BYO):** `.claude/dpo/controls/` (`.yml` + `.json`, gleiches Schema) — der Runner
  mergt sie automatisch zu den Framework-Katalogen.
- **Determinismus:** gleicher Projektstand = gleiches Ergebnis (reproduzierbar, Git-belegbar; bewusst
  **keine Datenbank**).
- **Cadence:** aus `environment.json.privacy_audit_cadence`, **Default: alle 4 Sprints**.
- **Report-Paar:** `dpo/reports/<date>_audit.md` (menschenlesbar) + `dpo/reports/<date>_audit.json`
  (maschinenlesbar).

Der Runner unterscheidet ehrlich zwei Check-Klassen — er täuscht keine Voll-Automatik vor:

| Check-Klasse | `check_typ` | Ergebnis | Wer entscheidet |
|--------------|-------------|----------|-----------------|
| **Mechanisch** | `file-exists`, `file-contains`, `grep-absent` | **PASS / GAP** (reproduzierbar) | Maschine |
| **Urteil** | `review` | **REVIEW-NEEDED** | Operator/Legal — manuell danach |

> **Merksatz:** Kataloge = periodisch, Doku-/Prozess-Audit, Report statt Stopp (`dpo-audit.py` setzt
> Exit-Code 0 — der Audit ist ein Bericht, kein Gate).

---

## 2. Touchpoint-Tabelle — wo Compliance je Phase greift

| Phase | Privacy / DSGVO | EU AI Act | Automatisch vs. menschliche Entscheidung |
|-------|-----------------|-----------|-------------------------------------------|
| **`/ideation`** | Schritt **0e**: Frontmatter `personal_data: true/false`; bei `true` DPO-ASSESS/DPIA **empfohlen** | Schritt **0e-bis**: `ai_act_relevant`-Pre-Flight (**weich**) | Automatisch: Frontmatter-Setzung + Hinweis. Mensch: ob DPO-ASSESS/DPIA durchgeführt wird |
| **`/implement`** | Schritt **5.5b**: Personal-Data-Gate — **harter Stopp**, `privacy-ok` | Schritt **5.5c**: **weicher Hinweis**, `AI_SYSTEM.md` aktuell halten — **kein** harter Stopp | Privacy: Maschine stoppt, **Mensch** bestätigt. AI Act: Maschine erinnert, kein Stopp |
| **`/sprint-review`** | Schritt **7c**: Kataloge `gdpr.yml` / `ndsg.yml`, periodisch | Schritt **7c**: Katalog `eu-ai-act.yml` prüft `AI_SYSTEM.md`-Vollständigkeit (nur wenn Add-on aktiv) | Mechanische Checks: Maschine (PASS/GAP). Urteils-Checks: **REVIEW-NEEDED** → Operator/Legal |

Flankierend über alle `/implement`-Läufe: Schritt **5.5** Sensitive-Paths-Gate (harter Stopp,
`review-ok`) + Layer-0-Edit-Bodyguard (vor dem Schreiben).

---

## 3. Lebenszyklus Privacy / DSGVO

```
/ideation 0e            /implement 5.5b              /sprint-review 7c
Pre-Flight (weich)  →   Personal-Data-Gate      →    Kataloge (periodisch)
personal_data:          HARTER STOPP                 gdpr.yml / ndsg.yml
true / false            privacy-ok: ...              PASS / GAP / REVIEW-NEEDED
DPO-ASSESS/DPIA         (oder DPO-REVIEW-Report)     Cadence: alle 4 Sprints
empfohlen
```

1. **`/ideation` Schritt 0e — Privacy-Pre-Flight (weich, BOO-69).**
   Das Story-Frontmatter wird um `personal_data: true|false` erweitert. Bei `true` wird ein
   Hinweis-Block in den Story-Body gesetzt: **DPO ASSESS-Modus empfohlen** vor Spec-Finalisierung
   (`/dpo --mode assess` → `dpia/DPIA-<feature>.md` mit Rechtsgrundlage und Risikobewertung). Das ist
   **kein** Hard-Gate — der harte Stopp folgt erst im Code.

2. **`/implement` Schritt 5.5b — Personal-Data-Paths-Gate (harter Stopp, BOO-69).**
   Läuft nur, wenn `personal_data: true` **und** `.claude/personal-data-paths.json` existiert. Trifft
   eine geänderte Datei ein Pattern, **stoppt** der Lauf mit vollständigem Diff zur Review. Der Commit
   wird erst durchgeführt, wenn `privacy-ok: {Name} - {Kommentar}` bestätigt wird **oder** der
   DPO-Skill einen REVIEW-Report ablegt. Das Ergebnis wird unter `## Privacy Review` ins Spec-File
   geschrieben. **Ohne `privacy-ok` keine Fortsetzung** — keine Ausnahme.

3. **`/sprint-review` Schritt 7c — DPO-Audit (periodisch, BOO-69/BOO-87).**
   Läuft nur, wenn `PRIVACY.md` im Projekt-Root existiert **und** der Sprint-Counter die
   `privacy_audit_cadence`-Schwelle erreicht hat (Default 4). `dpo-audit.py` arbeitet `gdpr.yml` /
   `ndsg.yml` ab und schreibt das Report-Paar mit PASS/GAP/REVIEW-NEEDED je Control. Urteils-Punkte
   (Verarbeitungsverzeichnis Art. 30, Auftragsverarbeitung Art. 28, Drittland-Transfer, Zweckbindung)
   sind `review`-Typ → REVIEW-NEEDED → Operator entscheidet.

---

## 4. Lebenszyklus EU AI Act

```
/ideation 0e-bis        /implement 5.5c              /sprint-review 7c
Pre-Flight (weich)  →   weicher Hinweis         →    Katalog eu-ai-act.yml
ai_act_relevant         AI_SYSTEM.md aktuell         prüft AI_SYSTEM.md-
                        halten — KEIN Stopp          Vollständigkeit
                                                     (nur wenn Add-on kopiert hat)
```

1. **`/ideation` Schritt 0e-bis — `ai_act_relevant`-Pre-Flight (weich).**
   Frühe, weiche Einstufung, ob die Story EU-AI-Act-relevant ist. Kein Hard-Gate.

2. **`/implement` Schritt 5.5c — weicher Hinweis (kein harter Stopp).**
   Erinnert daran, `AI_SYSTEM.md` aktuell zu halten (Zweck, Risikoklasse, Maßnahmen). Bewusst **kein**
   harter Stopp — der EU AI Act ist Governance, kein zeilenweiser Code-Check.

3. **`/sprint-review` Schritt 7c — Katalog `eu-ai-act.yml` (periodisch).**
   Der Katalog liegt bewusst unter `dpo/controls/optional/` und wird vom Runner **nicht** automatisch
   geladen. Er greift **nur**, wenn das **EU-AI-Act-Add-on** (Bootstrap-Phase 4.4n-bis, BOO-105) ihn
   ins Projekt-Overlay `.claude/dpo/controls/` kopiert hat — und dann nur für dieses Projekt. Er prüft
   die **Vollständigkeit von `AI_SYSTEM.md`**:

   | Control | Prüft | Typ | Ergebnis |
   |---------|-------|-----|----------|
   | `AIACT-Doc-001` | `AI_SYSTEM.md` vorhanden | `file-exists` | PASS / GAP |
   | `AIACT-Art6-001` | Risikoklasse dokumentiert | `file-contains` | PASS / GAP |
   | `AIACT-Art13-001` | Transparenz-/Kennzeichnungspflicht | `file-contains` | PASS / GAP |
   | `AIACT-Art14-001` | Human Oversight definiert | `file-contains` | PASS / GAP |
   | `AIACT-Art12-001` | Protokollierung / Logging | `file-contains` | PASS / GAP |
   | `AIACT-Art5-001` | Verbotene Praktiken ausgeschlossen | `review` | **REVIEW-NEEDED** |
   | `AIACT-Art6-002` | Hochrisiko-Einstufung + Konformität | `review` | **REVIEW-NEEDED** |
   | `AIACT-GPAI-001` | GPAI-/Basismodell-Betroffenheit | `review` | **REVIEW-NEEDED** |

   Die **Urteils-Punkte** (verbotene Praktiken, Hochrisiko, GPAI) sind immer **REVIEW-NEEDED** —
   Operator/Legal entscheidet. Quelle: KI-Verordnung VO (EU) 2024/1689.

---

## 5. Wichtige Klarstellungen

**(a) Gates ≠ Kataloge.** Gates sind ein **per-Code-Hartstopp** im `/implement` — sie blockieren den
Commit, bis ein Mensch bestätigt. Kataloge sind ein **periodischer Doku-/Prozess-Audit** im
`/sprint-review` — sie melden PASS/GAP/REVIEW-NEEDED in einem Report, ohne etwas zu blockieren. Die
beiden Mechanismen lösen unterschiedliche Probleme und ersetzen sich nicht.

**(b) EU AI Act = Doku-/Governance-Compliance, kein zeilenweiser Code-Check.** Das ist **bewusst** so:
Der AI Act ist ein Governance-Thema (Risikoklasse, Transparenz, Human Oversight, Logging,
GPAI-Pflichten), kein Linter-Thema. Deshalb ist der `/implement`-Touchpoint (5.5c) nur ein **weicher
Hinweis** und der Katalog prüft die Vollständigkeit von `AI_SYSTEM.md` — nicht den Code Zeile für
Zeile.

**(c) Urteils-Punkte sind immer REVIEW-NEEDED.** Wo eine rechtliche Beurteilung nötig ist
(Zweckbindung, Drittland, AVV, verbotene Praktiken, Hochrisiko, GPAI), liefert der Runner bewusst
**REVIEW-NEEDED** statt einer erfundenen Bewertung. Der **Operator/Legal** entscheidet — der Skill
gibt **keine Rechtsberatung**.

**(d) Add-on-gated.** Ohne aktiviertes **Privacy-Add-on** passiert auf der DSGVO-Seite nichts
(Schritte 0e / 5.5b / 7c sind dann inaktiv). Ohne **EU-AI-Act-Add-on** wird `eu-ai-act.yml` nicht ins
Projekt-Overlay kopiert und greift nicht. Compliance ist opt-in pro Projekt.

---

## 6. Belege & Querverweise

| Thema | Quelle |
|-------|--------|
| Wo die Evidenz landet (Audit-Trail, Reports, Gates) | [docs/runbooks/audit-perspective.md](../runbooks/audit-perspective.md) |
| Privacy-Hintergrund (Rechtsgrundlagen, Modi, Kontrollkatalog) | HANDBUCH **Anhang O** (Privacy by Design, BOO-69) |
| Skill-Details (3 Modi, Kataloge, Runner) | [dpo/SKILL.md](../../dpo/SKILL.md) |
| Deterministischer AUDIT-Runner | [dpo/scripts/dpo-audit.py](../../dpo/scripts/dpo-audit.py) |
| Framework-Kataloge | [dpo/controls/gdpr.yml](../../dpo/controls/gdpr.yml), [dpo/controls/ndsg.yml](../../dpo/controls/ndsg.yml) |
| EU-AI-Act-Katalog (opt-in) | [dpo/controls/optional/eu-ai-act.yml](../../dpo/controls/optional/eu-ai-act.yml) |
| Report-Ablage | `dpo/reports/<date>_audit.{md,json}` |
