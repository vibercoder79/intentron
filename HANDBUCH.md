> 🇩🇪 **Deutsch** (this file) · 🇬🇧 [English](HANDBUCH.en.md)

---

# Governance für Vibe Coder — Das komplette Handbuch

> **Für wen ist dieses Handbuch?**
> Du bist Vibe Coder — du hast Ideen, du nutzt KI um Code zu bauen, und du willst schnell
> vorankommen. Governance klingt nach Bürokratie. Dieses Handbuch zeigt dir, warum Governance
> dein schnellstes Werkzeug ist — und wie du es in 30 Minuten aufgesetzt hast.

---

## Inhaltsverzeichnis

1. [Das Problem ohne Governance](#1-das-problem-ohne-governance)
2. [Was du bekommst](#2-was-du-bekommst)
3. [Voraussetzungen und Vorbereitung](#3-voraussetzungen-und-vorbereitung)
4. [Installation — Schritt für Schritt](#4-installation--schritt-für-schritt)
5. [Der Bootstrap-Prozess](#5-der-bootstrap-prozess)
6. [Die Skills — wann nutze ich was?](#6-die-skills--wann-nutze-ich-was)
7. [Die Artefakte — was entsteht, wo, und warum](#7-die-artefakte--was-entsteht-wo-und-warum)
8. [Die Guardrails — dein Sicherheitsnetz](#8-die-guardrails--dein-sicherheitsnetz)
9. [VS Code Setup](#9-vs-code-setup)
10. [Governance für dein Projekt anpassen](#10-governance-für-dein-projekt-anpassen)
11. [Tägliche Nutzung — ein typischer Workflow](#11-tägliche-nutzung--ein-typischer-workflow)
12. [Häufige Fragen](#12-häufige-fragen) — inkl. Claude Agent SDK Migration

---

## 1. Das Problem ohne Governance

### Was passiert wenn du einfach drauf los baust

Stell dir vor: Du hast eine großartige Idee. Du öffnest Claude, sagst "Bau mir X" und in 10 Minuten läuft Code. Genial.

Drei Wochen später:

- Du weißt nicht mehr, warum du eine Entscheidung so getroffen hast
- Du fragst Claude nach einem Bug — Claude kennt den Kontext nicht mehr
- Du willst eine neue Funktion hinzufügen und zerstörst dabei was anderes
- Du weißt nicht, welche Version deines Projekts "stabil" ist
- Du hast 50 Dateien, 3 halbfertige Features und keinen Plan mehr

Das ist **nicht** das Problem von KI. Das ist das Problem von **fehlendem System**.

### Die versteckte Wahrheit über Vibe Coding

Vibe Coding ist mächtig — aber nur wenn die KI versteht **was du gebaut hast** und **warum**.
Ohne Dokumentation und Struktur gibt jede neue Session bei null an.

**Mit Governance** passiert folgendes:
- Du sagst in einer neuen Session: `/status` — Claude sieht sofort alles
- Du sagst: `/implement ISSUE-42` — Claude weiß genau was zu tun ist
- Du sagst: `/breakfix` — Claude diagnostiziert strukturiert
- Jede Änderung ist nachvollziehbar, jeder Fehler hat einen Audit-Trail

---

## 2. Was du bekommst

### Das Code-Crash Framework

Ein **vollständiges Betriebssystem für KI-gestützte Softwareentwicklung**:

```
GitHub Repository (vibercoder79/claudecodeskills)
├── bootstrap/        ← Richtet alles automatisch ein
├── ideation/         ← Von der Idee zur Story
├── implement/        ← Von der Story zum Code
├── backlog/          ← Sprint Planning & Prioritäten
├── breakfix/         ← Wenn etwas kaputt ist
├── architecture-review/  ← Ist mein System gesund?
├── research/         ← Deep Research mit KI
├── sprint-review/    ← Regelmäßige Qualitätskontrolle
├── integration-test/ ← Automatische Tests nach jeder Änderung
└── status/           ← System-Überblick auf Knopfdruck
```

### Was das konkret bedeutet

| Ohne Governance | Mit Governance |
|----------------|----------------|
| Claude vergisst zwischen Sessions | Claude kennt das System immer |
| "Bau mir X" → irgendwas entsteht | `/ideation` → strukturierte Story → `/implement` |
| Bugs tauchen aus dem Nichts auf | Self-Healing Agent überwacht 24/7 |
| Keine Ahnung ob Version stabil | Jede Änderung ist versioniert + dokumentiert |
| Rollback? Welches Rollback? | Git + Changelog = jederzeit zurückrollbar |
| 3 Wochen später: komplettes Chaos | Sprint Review hält alles sauber |

---

## 3. Voraussetzungen und Vorbereitung

### Software die du brauchst

**Pflicht:**

| Software | Wozu | Download |
|----------|------|---------|
| **Claude Code CLI** | Das Herzstück — KI im Terminal | `npm install -g @anthropic-ai/claude-code` ¹ |
| **Node.js** (v18+) | Runtime für Claude Code | nodejs.org |
| **Git** | Versionskontrolle | git-scm.com |

**Empfohlen:**

| Software | Wozu |
|----------|------|
| **Visual Studio Code** | Editor mit Claude Code Integration |
| **GitHub Account** | Dein Code-Repository |

### Accounts die du brauchst

**Pflicht:**

1. **Anthropic Account** — für Claude Code
   - Gehe zu: claude.ai
   - Registrieren → Plan wählen (Pro reicht für den Start)
   - API Key unter: console.anthropic.com → API Keys

2. **GitHub Account** — für dein Repository
   - github.com/signup
   - Kostenlos reicht für den Anfang

**Empfohlen:**

3. **Linear Account** — für Issue Tracking (Backlog, Stories)
   - linear.app
   - Kostenlos für kleine Teams
   - Linear API Key: linear.app → Settings → API → Personal API Keys

**Optional aber wertvoll:**

4. **OpenRouter Account** — für günstigere LLM-Calls
   - openrouter.ai
   - Guthaben aufladen (~$10 reichen lange)
   - API Key unter: openrouter.ai/keys

### API Keys — Übersicht

Bevor du mit `/bootstrap` startest, halte diese Keys bereit:

| Key | Pflicht? | Woher | Variable |
|-----|---------|-------|----------|
| Anthropic API Key | JA | console.anthropic.com | `ANTHROPIC_API_KEY` |
| GitHub SSH Key | JA | `ssh-keygen` + GitHub Settings | — |
| Linear API Key | Empfohlen | linear.app → Settings → API | `LINEAR_API_KEY` |
| OpenRouter Key | Optional | openrouter.ai/keys | `OPENROUTER_API_KEY` |
| Telegram Bot Token | Optional | @BotFather auf Telegram | `TELEGRAM_BOT_TOKEN` |

> **Sicherheitsregel:** API Keys kommen NIEMALS in den Code. Sie landen in `.env` (diese Datei ist
> in `.gitignore` — wird nicht auf GitHub hochgeladen).

> ¹ **Hinweis zum Claude-Paket:** Das CLI-Tool heißt weiterhin `@anthropic-ai/claude-code`.
> Das neue `@anthropic-ai/claude-agent-sdk` (npm) / `claude-agent-sdk` (pip) ist für
> programmatische SDK-Nutzung in eigenen Apps — nicht für das CLI. Details: [FAQ → Claude Agent SDK](#was-ist-das-claude-agent-sdk--muss-ich-migrieren)

### SSH für GitHub einrichten

SSH ist die sichere Verbindung zwischen deinem Rechner und GitHub. Einmal einrichten, nie wieder denken.

```bash
# 1. SSH Key erstellen (falls noch nicht vorhanden)
ssh-keygen -t ed25519 -C "deine@email.com"
# → Einfach Enter drücken für alle Fragen

# 2. Public Key anzeigen
cat ~/.ssh/id_ed25519.pub
# → Diesen Text komplett kopieren

# 3. Auf GitHub eintragen
# github.com → Settings → SSH and GPG Keys → New SSH Key → Text einfügen

# 4. Verbindung testen
ssh -T git@github.com
# → "Hi username! You've successfully authenticated." = Erfolg
```

---

## 4. Installation — Schritt für Schritt

### Schritt 1: Claude Code installieren

```bash
# Node.js Version prüfen (muss 18+ sein)
node --version

# Claude Code installieren
npm install -g @anthropic-ai/claude-code

# Prüfen ob es funktioniert
claude --version
```

### Schritt 2: Claude Code einrichten

```bash
# Claude Code starten — beim ersten Start wirst du nach dem API Key gefragt
claude

# Alternativ: API Key als Environment Variable setzen
export ANTHROPIC_API_KEY="dein-api-key-hier"
```

> **Tipp:** Den `export` Befehl in deine `~/.bashrc` oder `~/.zshrc` eintragen, damit er
> bei jedem Terminal-Start aktiv ist.

### Schritt 3: Bootstrap Skill holen

Das ist der **einzige manuelle Schritt** — danach macht Claude alles automatisch.

```bash
# Bootstrap Skill vom GitHub Repository holen (macOS/Linux — User-Home)
mkdir -p ~/.claude/skills
cd /tmp
git clone --filter=blob:none --sparse git@github.com:vibercoder79/claudecodeskills.git ki-skills
cd ki-skills
git sparse-checkout set code-crash-framework/bootstrap
cp -r code-crash-framework/bootstrap ~/.claude/skills/
cd /tmp && rm -rf ki-skills

# Prüfen ob der Skill da ist
ls ~/.claude/skills/bootstrap/
# → Sollte SKILL.md und einen references/ Ordner zeigen
```

> **Warum nur den Bootstrap Skill?** Der Bootstrap Skill installiert in Phase 5 (via `git clone`)
> automatisch alle weiteren Skills die du brauchst — keine Symlinks, lokal und portabel.

> **Bootstrap Skill vs. Code-Crash Framework:** Der Bootstrap Skill ist der Installer und
> Projekt-Initializer. Er legt Governance-Dateien, Skill-Kopien, Hooks und optionale Adapter im
> Zielprojekt an. Das Code-Crash Framework ist der Vergleichsgegenstand und die Methodik: die
> Regeln, Gates, Artefakte und Rollen, gegen die ein Projekt später geprüft wird. Anders gesagt:
> Bootstrap bringt das Framework ins Projekt; das Framework selbst ist nicht "der Bootstrap".

### Schritt 4: Neues Projekt anlegen

```bash
# Verzeichnis für dein neues Projekt erstellen
mkdir ~/mein-projekt
cd ~/mein-projekt

# Claude Code im Projektverzeichnis starten
claude
```

### Schritt 5: Bootstrap ausführen

In der Claude Code Session:

```
/bootstrap
```

Claude führt dich jetzt durch vier kurze Interview-Blöcke (A–D) und baut danach alles automatisch auf. Gesamtzeit: ca. 10 Minuten.

---

## 5. Der Bootstrap-Prozess (v3.0)

![Bootstrap Skill — Interview-Block-Flow (A–D) + Setup-Phasen (0, 4, 5, 7)](bootstrap/docs/bootstrap-big-picture.png)

*Vom leeren Ordner zum governance-ready Projekt — vier Interview-Blöcke (A–D) umrahmen die Entscheidungen, vier Setup-Phasen (0, 4, 5, 7) setzen sie um. Block D aktiviert optionale Komponenten nur wenn du sie willst. ([Excalidraw-Quelle](bootstrap/docs/bootstrap-big-picture.excalidraw))*

### Überblick

| Schritt | Typ | Inhalt |
|---------|-----|--------|
| **Phase 0** — Briefing | Ankündigung | Bootstrap erklärt was kommt, du bestätigst |
| **Block A** — Projekt-Kern | Interview (7 Fragen) | Stack, Name, Beschreibung, Pfad, GitHub-URL, Backlog-Tool + Prefix, Version |
| **Block B** — Bestehende Infrastruktur | Interview (6 Fragen) | GitHub-Repo? Projekt-Dokumentations-SSoT? Backlog-Tool? `.env`? Runtime-Datei? Developer-Uebergabe? — integriert in das was schon da ist |
| **Block C** — Doku-Architektur | Vorschlag + Review | Project Hub, Developer Onboarding, Governance, Zielarchitektur, Backlog-Verweis + 3-Schichten-Vorschlag |
| **Phase 4** — Grundstruktur | Automatisch (~2 min) | Dateien, Git init, Linting, Governance-Hooks, Component-Skelette |
| **Phase 5** — Skills installieren | Automatisch | Skills via `git clone` aus `claudecodeskills` (keine Symlinks) |
| **Block D** — Optional-Komponenten | 4× Ja/Nein am Ende | Self-Healing / DocSync / Automation-Daemon / Learning-Loop (L1/L2/L3) |
| **Phase 7** — Finalisierung | Automatisch | gewaehlte Dokumentations-SSoT, optionale SecondBrain-Integration, globaler Registry-Eintrag, finaler Commit |

> **Warum Blöcke statt 14-Fragen-Batch?** Einzelne Fragen sind einfacher zu beantworten und jeder Block baut auf dem vorherigen auf — der Doku-Architektur-Vorschlag in Block C kennt deinen Stack (A.1) und deine bestehende Infra (B) schon.

### Block A — Projekt-Kern (7 Fragen)

#### A.1: Stack-Frage — als allererstes

```
Was möchtest du entwickeln?

a) Node.js / JavaScript Backend (API, CLI, Daemon)
b) Frontend (React, Vue, Vanilla JS)
c) Full-Stack (Node.js Backend + Frontend)
d) Python (KI/ML, Scripts, FastAPI, Django)
e) Anderes / Noch nicht klar
```

Die Antwort bestimmt Linter und Formatter:

| Deine Wahl | Linter | Formatter | Wird automatisch angelegt |
|-----------|--------|-----------|--------------------------|
| Node.js | ESLint | — | `eslint.config.mjs` |
| Frontend | ESLint + Prettier | Prettier | `eslint.config.mjs` + `.prettierrc` |
| Full-Stack | ESLint + Prettier | Prettier | `eslint.config.mjs` + `.prettierrc` |
| Python | Ruff | Black | `pyproject.toml` |

#### A.2–A.7: Projekt-Identität

| Frage | Beispiel | Warum |
|-------|----------|-------|
| Projektname | `MeinShop` | Wird überall verwendet |
| Kurze Beschreibung | `E-Commerce für handgemachte Produkte` | Claude versteht was du baust |
| Projekt-Pfad | `/home/user/mein-projekt` | Wo der Code landet |
| Backlog-Tool | `linear` / `github-issues` / `none` | Steuert Issue-Prefix und Daemon-Eligibility |
| Issue-Prefix | `SHOP` | Stories werden SHOP-1, SHOP-2, … |
| Start-Version | `1.0.0` | Versionierung ab Tag 1 |

#### A.4: Architektur-Dimensionen + Add-ons

Bootstrap installiert 8 **Standard**-Architektur-Dimensionen (Reliability, Data Integrity, Security, Performance, Observability, Maintainability, Testability, Scalability) und fragt, welche der 4 **optionalen Add-ons** dazugeschaltet werden:

| Add-on | Wann sinnvoll |
|--------|---------------|
| **Privacy / DSGVO** | Du verarbeitest personenbezogene Daten, DSGVO gilt |
| **Cost Efficiency** | Cloud-Rechnung ist relevant, LLM-Calls werden per Token abgerechnet |
| **Signal Quality** | Trading, Monitoring, alles was auf externe Signale reagiert |
| **Compliance** | Regulierte Branche (Finance, Health, öffentlicher Sektor) |

**Standard vs. Add-on:** Standard-Dimensionen gelten fuer **jedes** Projekt — universelle Software-Eigenschaften, die in jedem KI-unterstuetzten Bau abgesichert werden. Add-ons sind kontext-spezifisch und werden nur aktiviert, wenn die Projekt-Domain sie braucht.

Beliebige Kombination möglich — Default ist "keine". Jede aktive Dimension wird eine Sektion in `ARCHITECTURE_DESIGN.md §3 Quality Attributes`, die `/ideation`, `/architecture-review` und `/sprint-review` pruefen.

### Block B — Bestehende Infrastruktur (6 Fragen)

Bootstrap integriert in das was schon da ist, statt zu überschreiben. Die Fragen:

1. **GitHub-Repo existiert schon?** (URL oder "neu anlegen")
2. **Wo liegt die Projekt-Dokumentations-SSoT?** Obsidian Vault, Repo `docs/project/`, externes DMS wie Notion/Confluence/SharePoint oder vorlaeufiger Fallback
3. **Backlog-Tool eingerichtet?** (Linear-Projekt / GitHub-Issues / none)
4. **`.env` schon da?** (Keys behalten oder Template anlegen)
5. **Runtime-Anweisungen schon da?** (`AGENTS.md`, `CLAUDE.md`, mergen oder erzeugen)
6. **Developer Onboarding?** als Standard-Artefakt erzeugen oder vorhandenes Onboarding verlinken

### Block C — Doku-Architektur

Vor dem Schichtenmodell operationalisiert Bootstrap die gewaehlte Dokumentations-SSoT. Obsidian ist der Best-Practice-Pfad fuer vernetztes Projektwissen, aber das Framework ist nicht Obsidian-only:

| Option | Bootstrap erzeugt oder verlinkt |
|---|---|
| Obsidian Vault | Projektordner mit Project/PMO Hub, Developer Onboarding, Governance, Zielarchitektur, Backlog, Decisions, Meetings, Research, Assets, Archive |
| Repo docs | `docs/project/` mit denselben Standard-Artefakten |
| Externes DMS | lokaler Pointer `docs/project/DOCUMENTATION_SSOT.md` auf Notion, Confluence, SharePoint oder ein anderes System |
| Noch unklar | Repo-Fallback unter `docs/project/` plus TODO und Postflight `WARN` |

Developer Onboarding ist das Uebergabe-Artefakt. Ziel ist, dass ein fremdes Team oder eine andere Coding-Runtime das Projekt uebernehmen kann: Claude Code -> Codex, Cursor, GitHub Copilot, Google Antigravity oder ein klassisches Entwicklungsteam.

Basierend auf Stack (A.1) und bestehender Infra (Block B) schlägt Bootstrap dann eine **3-Schichten-Doku-Architektur** vor:

| Schicht | Lebt in | Zweck |
|---------|---------|-------|
| **1. Story-Specs** | `specs/ISSUE-XX.md` | Pro Story, Pflicht für Commit via `spec-gate.sh` |
| **2. Component-Docs** | `docs/components/*.md` oder Obsidian `Components/*.md` | Lebende Doku pro Komponente (voice, memory, frontend …) |
| **3. Architektur-Vorgaben** | `Architektur-Vorgaben.md` | Konsolidierte Stack-Entscheidungen, querschnittliche Regeln |

**Hub:** `ARCHITECTURE_DESIGN.md` verlinkt alle drei Schichten via **§9-Auto-Verlinkung** — jede neue `*.md` unter den Doku-Ordnern wird automatisch im Hub registriert. Optionaler `orphan-check.sh`-Hook blockiert Commits mit Docs ohne Hub-Eintrag.

Du kannst den Vorschlag übernehmen, anpassen oder einzelne Schichten abwählen.

### Phase 4: Grundstruktur (automatisch, ~2 Minuten)

Claude legt Dateien an, initialisiert Git, richtet Linting ein, installiert Governance-Hooks und scaffolded die Component-Doc-Skelette. Siehe [Artefakte-Landkarte](#7-die-artefakte--was-entsteht-wo-und-warum) für eine visuelle Übersicht aller Dateien.

**`ARCHITECTURE_DESIGN.md §2` enthält einen Pflicht-Block KI-Architektur-Prinzipien (BOO-24, Schrader Kap. 4):** 4 Prinzipien (kleine Module, explizite Interfaces, Testbarkeit, Observability) + 4 Anti-Patterns werden proaktiv beim Projekt-Setup verankert — nicht erst reaktiv im ersten Review entdeckt. `/architecture-review` (BOO-7) prüft alle 8 Punkte bei jeder Story. Referenz: `code-crash-framework/references/ki-architektur-prinzipien.md`.

**Wichtigste Datei: `CLAUDE.md`** — der "Personalausweis" deines Projekts für die KI. Bei jeder neuen Claude-Session liest Claude diese Datei und kennt sofort Projekt, Regeln, Dateipfade, letzten Stand.

### Phase 5: Skills installieren (automatisch)

Skills werden via `git clone` aus dem Repository `vibercoder79/claudecodeskills` nach `.claude/skills/` geholt — **keine Symlinks, keine Runtime-Abhängigkeit zum Quell-Repo**. Die Skill-Kopien sind lokal und portabel.

Wichtige Trennung: VS-Code-Plugins sind Workstation-Infrastruktur; Skills sind Projekt-Infrastruktur. ESLint, SonarQube for IDE, Error Lens, Python/Ruff usw. installierst du einmal in VS Code. Bootstrap prueft und dokumentiert pro Projekt nur, ob diese Plugins verfuegbar sind; er installiert sie nicht fuer jedes Projekt neu. Skills sind anders: Jedes gebootstrappte Projekt bekommt eine eigene lokale `.claude/skills/`-Kopie (und bei Codex-Adaptern optional `.codex/skills/`). Diese Kopie ist der gepinnte Runtime-Stand des Projekts. Wenn du ein zweites Projekt bootstrappst, werden die ausgewaehlten Skills auch in dieses zweite Projekt kopiert. Das ist Absicht, keine doppelte globale Installation.

Wenn ein Projekt bereits `.claude/skills/<skill>/` enthaelt, ist Phase 5 eine Update-/Merge-Entscheidung: Projektkopie behalten, gegen den aktuellen Master-Skill vergleichen und nur bewusst aktualisieren. Projektspezifisch angepasste Skills nicht blind ersetzen.

```
Welche Skills installieren?
a) Minimum (ideation, implement, backlog)      ← Für den Start ideal
b) Standard (+ architecture-review, sprint-review, research, breakfix)  ← Empfohlen
c) Voll (alle Skills)                          ← Volles Arsenal
d) Manuell auswählen
```

### Block D — Optional-Komponenten (am Ende)

Nachdem das Basisprojekt steht, stellt Bootstrap gezielte Optional-Komponenten- und Provider-Postflight-Fragen:

| Komponente | Was sie macht | Kosten |
|------------|---------------|--------|
| **Self-Healing-Agent** | Cron-Check alle 15 Min: Versionen synchron, Dateien vorhanden, Daemons laufen | Niedrig |
| **DocSync zu Obsidian** | Auto-Spiegel der Docs in deinen Vault | Keine (wenn Vault existiert) |
| **Automation-Daemon** | Linear-Webhook → automatisches `/implement` bei "In Progress" | Braucht Linear + Webhook-Endpoint |
| **Learning-Loop (L1/L2/L3)** | Framework wird mit jedem Sprint klüger — siehe nächste Sektion | L1 gratis, L3 bringt SQLite |
| **Research** | Framework-, Companion- oder globaler Skill plus Perplexity/OpenRouter/MCP-Providerstatus | Provider-abhaengig |
| **Visualize/Miro** | Diagramm-Skill plus Miro-MCP-Verifikation oder Excalidraw/Mermaid-Fallback | Miro-abhaengig |
| **Monitoring** | zentrale Plattform, projektlokales Setup oder dokumentierte Architekturfrage | Plattform-abhaengig |

### Learning-Loop (L1/L2/L3)

Eine **portable Feedback-Schleife**, die abgeschlossene Sprints in Anti-Pattern-Warnungen für zukünftige Stories verwandelt. Drei Stufen zur Auswahl:

| Level | Speicher | Schreibt | Liest |
|-------|----------|----------|-------|
| **L1 — Einfach** | `journal/learnings.md` (append-only Markdown) | `/sprint-review` hängt nach jedem Review an | `/ideation` liest bei Story-Erstellung (warnt bei passendem Anti-Pattern) |
| **L2 — Sprint-Journal** | `journal/sprint-YYYY-QN.md` (eine Datei pro Sprint) | `/sprint-review` | `/ideation` + `/architecture-review` |
| **L3 — SQLite** | `.learning-loop/loop.db` (strukturiert) | `/sprint-review` | `/ideation` + `/architecture-review` + `/backlog` (Prio-Anpassung) |

**Warum das wichtig ist:** Ohne Loop startet jeder Sprint bei Null. Mit Loop tauchen Entscheidungen, die letzten Sprint Schmerzen verursacht haben (falsche Abhängigkeit, übersehene Acceptance Criterion, Scope Creep), als Warnung auf — *bevor* die nächste Story geschrieben wird.

### Phase 7: Finalisierung

- **Dokumentations-SSoT finalisieren** — Bootstrap erzeugt oder verlinkt Project Hub, Developer Onboarding, Governance, Zielarchitektur, Backlog, Decisions, Meetings, Research, Assets und Archive in der gewaehlten SSoT
- **SecondBrain-Integration** — wenn Block B Obsidian gewaehlt hat, legt Bootstrap einen PMO-Hub unter `02 Projekte/<ProjektName>/` an
- **Globale Registry** — `~/.claude/MEMORY.md` bekommt einen Pointer auf das neue Projekt
- **Finaler Commit** — alles in einem Commit mit Zusammenfassungs-Tabelle

```
✓ Block A: Projekt-Kern + Stack + Add-ons
✓ Block B: Bestehende Infrastruktur + Dokumentations-SSoT integriert
✓ Block C: Project Hub + Developer Onboarding + Doku-Architektur
✓ Phase 4: Grundstruktur (Dateien, Git, Linting, Hooks, Labels)
✓ Phase 5: Skills installiert ({Anzahl})
✓ Block D: Optional-Komponenten ({Status})
✓ Phase 7: SecondBrain + Registry + Final-Commit

Dein Projekt ist bereit. Starte mit: /ideation
```

---

## 6. Die Skills — wann nutze ich was?

### Übersicht: Das Skill-System

Skills sind **wiederholbare Workflows** die Claude durch komplexe Aufgaben führen.
Du rufst sie mit `/skillname` auf und Claude folgt einem definierten Prozess.

```
Idee → /ideation → Story in Linear
Story → /implement → Code, Tests, Git Push
Problem → /breakfix → Diagnose, Fix, Prevention
Woche → /backlog → Was steht an?
Quartal → /sprint-review → System-Gesundheit
Sprint-Ende → /pitch → Evidenz-Briefing fuer Stakeholder
Jederzeit → /status → Was läuft gerade?
```

Die vollstaendige 4P-Delivery-Pipeline (Schrader Code Crash Kap. 5) ist verdrahtet als:

```
/intent → /ideation → /backlog → /implement → /architecture-review → /sprint-review → /pitch
\______/   \_____________________________/                                              \____/
Perceive   Prompt + Produce                                                              Pitch
```

Siehe **Anhang L** fuer das vollstaendige 4P-Pipeline-Mapping und den `/pitch`-Evidenz-Vertrag.

Jeder Skill hat eine eigene README mit visueller Übersicht:

| Skill | README + Sketch |
|-------|-----------------|
| bootstrap | [README](bootstrap/README.md) · [Sketch](bootstrap/docs/bootstrap-big-picture.png) |
| ideation | [README](ideation/README.md) · [Sketch](ideation/overview.png) |
| implement | [README](implement/README.md) · [Sketch](implement/overview.png) |
| backlog | [README](backlog/README.md) · [Sketch](backlog/overview.png) |
| architecture-review | [README](architecture-review/README.md) · [Sketch](architecture-review/overview.png) |
| sprint-review | [README](sprint-review/README.md) · [Sketch](sprint-review/overview.png) |
| pitch | [README](pitch/README.md) · [Sketch](pitch/pitch-overview.png) |
| research | [README](research/README.md) · [Sketch](research/overview.png) |
| security-architect | [README](security-architect/README.md) · [Sketch](security-architect/overview.png) |
| grafana | [README](grafana/README.md) · [Sketch](grafana/overview.png) |
| cloud-system-engineer | [README](cloud-system-engineer/README.md) · [Sketch](cloud-system-engineer/overview.png) |
| visualize | [README](visualize/README.md) · [Sketch](visualize/overview.png) |
| skill-creator | [README](skill-creator/README.md) · [Sketch](skill-creator/overview.png) |
| design-md-generator | [README](design-md-generator/README.md) · [Sketch](design-md-generator/overview.png) |

### `/ideation` — Von der Idee zur Story

![Ideation Skill](ideation/overview.png)

**Wann:** Du hast eine Idee für ein neues Feature.

**Was passiert:**
1. Du beschreibst deine Idee in natürlicher Sprache
2. Claude recherchiert (optional: Deep Research mit Perplexity)
3. Claude prüft ob die Idee zur Architektur passt
4. Claude erstellt eine strukturierte User Story in Linear

**Beispiel:**
```
Du: /ideation

Claude: "Beschreibe deine Idee..."
Du: "Ich möchte dass Kunden ihre Bestellungen verfolgen können"

→ Claude erstellt SHOP-42 in Linear mit:
   - Was genau gebaut wird
   - Warum (Business Value)
   - Wie (technischer Ansatz)
   - Akzeptanzkriterien
   - Aufwandsschätzung
```

#### Pre-Flight Checks in `/ideation`

Bevor die eigentliche Ideation-Arbeit beginnt, laufen zwei weiche Pre-Flight-Checks. **Weich = der Operator wird gefragt, kein Hard-Block.** Sie verhindern den teuersten Failure Mode: Stories gegen ein veraltetes Bild des Systems schreiben.

**Check 1 — Environment geladen (Schritt 0):** Der Skill liest `.claude/environment.json`, um Pfade, Tools und Thresholds zu kennen. Fehlt die Datei, greifen Defaults und der Skill warnt einmalig.

**Check 2 — Architektur-Doku-Aktualität (Schritt 0a, weich):** Der Skill vergleicht den letzten Aenderungs-Zeitstempel der `ARCHITECTURE_DESIGN.md` gegen `thresholds.architecture_doc_freshness_days` aus `.claude/environment.json` (Default `30`). Wenn die Doku aelter ist als der Threshold:

```
Warnung: ARCHITECTURE_DESIGN.md wurde seit 47 Tagen nicht aktualisiert
(Threshold: 30 Tage).

Empfehlung: /architecture-review ausfuehren, bevor neue Stories gegen
eine evtl. veraltete Architektur angelegt werden.

Trotzdem fortfahren? [ja/nein]
```

Bei `nein` stoppt der Skill, der Operator faehrt `/architecture-review`, danach wird `/ideation` erneut gestartet. Bei `ja` wird das Override in der resultierenden Story unter `Current State` dokumentiert.

**Warum weich, kein Hard-Block?** Ein Hard-Gate wuerde jedes Projekt, das laenger nicht angefasst wurde, blockieren — die Doku ist aber oft „alt genug zum Warnen, noch valide". Der Operator entscheidet pro Story. Der Threshold steht in `.claude/environment.json`, jedes Projekt kann ihn tunen: schnell evolvierende Systeme setzen 14, stabile Systeme 90.

**Konfigurations-Beispiel** in `.claude/environment.json`:

```json
{
  "thresholds": {
    "architecture_doc_freshness_days": 14
  }
}
```

### `/implement` — Von der Story zum Code

![Implement Skill](implement/overview.png)

**Wann:** Du willst eine Story umsetzen.

**Was passiert (10-Schritte-Prozess):**
1. Issue aus Linear laden
2. Spec-File erstellen (`specs/SHOP-42.md`)
3. **Operator-OK einholen** ← du bestätigst den Plan
4. Code schreiben
5. Tests
6. Git Commit + Push
7. Deploy Health Check
8. Backlog-Record oder Adapter-Story schließen
9. Changelog aktualisieren
10. Ergebnis präsentieren

**Beispiel:**
```
Du: /implement SHOP-42

Claude: [liest Issue, erstellt Plan, zeigt dir was er tun will]
Claude: "Soll ich loslegen? [Ja/Nein/Ändern]"
Du: "Ja"
Claude: [implementiert, testet, pusht, schließt Issue]
```

> **Wichtig:** `/implement` ändert NIEMALS Code ohne dein OK in Schritt 3.
> Du hast immer die Kontrolle.

### `/backlog` — Sprint Planning

![Backlog Skill](backlog/overview.png)

**Wann:** Du weißt nicht was als nächstes wichtig ist.

**Was passiert:**
1. Claude lädt alle offenen Issues aus Linear
2. Analysiert Abhängigkeiten (was blockiert was?)
3. Schlägt priorisierte Reihenfolge vor
4. Zeigt Aufwand und Risiko pro Issue

**Beispiel:**
```
Du: /backlog

Claude zeigt:
┌─────────────┬──────────────────────────────────┬──────────┬──────────┐
│ Issue       │ Titel                            │ Prio     │ Aufwand  │
├─────────────┼──────────────────────────────────┼──────────┼──────────┤
│ SHOP-38     │ Zahlungsabwicklung reparieren    │ KRITISCH │ S        │
│ SHOP-42     │ Bestellverfolgung                │ HOCH     │ M        │
│ SHOP-51     │ Dashboard Redesign               │ MITTEL   │ L        │
└─────────────┴──────────────────────────────────┴──────────┴──────────┘
→ Empfehlung: SHOP-38 zuerst (blockiert SHOP-42)
```

### `/breakfix` — Wenn etwas kaputt ist

**Wann:** Das System hat ein Problem, einen Bug, oder verhält sich komisch.

**Was passiert (6-Schritte-Prozess):**
1. **Detect:** Was genau ist das Problem?
2. **Diagnose:** Warum passiert es?
3. **Fix:** Lösung implementieren
4. **Verify:** Ist es wirklich behoben?
5. **Document:** Incident in `journal/incidents/` archivieren
6. **Prevent:** Wie verhindern wir das in Zukunft?

**Beispiel:**
```
Du: /breakfix

Claude: "Beschreibe das Problem..."
Du: "Die API gibt seit heute 401 Fehler zurück"

→ Claude analysiert Logs, findet expired Session Token,
   implementiert automatischen Token-Refresh,
   schreibt Incident-Report, legt präventiven Test an
```

### `/architecture-review` — System-Gesundheit

![Architecture Review Skill](architecture-review/overview.png)

**Wann:** Bevor du eine große Entscheidung triffst. Regelmäßig (monatlich).

**Was passiert:**
Claude prüft die aktiven Dimensionen deines Systems — 8 Standard
(Reliability, Data Integrity, Security, Performance, Observability, Maintainability, Testability, Scalability)
plus aktive Add-ons (Privacy / DSGVO, Cost Efficiency, Signal Quality, Compliance):
- Wird SSoT (Single Source of Truth) eingehalten?
- Gibt es zirkuläre Abhängigkeiten?
- Sind alle Sicherheitsregeln aktiv?
- Stimmt die Dokumentation mit dem Code überein?
- Coverage auf neuem Code? Test-Pyramide eingehalten?

**Output:** Risiko-Tabelle mit konkreten Handlungsempfehlungen.

### `/research` — Deep Research

![Research Skill](research/overview.png)

**Wann:** Du willst eine technische Entscheidung treffen und brauchst Fakten.

**Was passiert:**
- Automatisches Routing: Einfache Fragen → WebSearch, komplexe → Perplexity (tiefere KI-Analyse)
- Ergebnisse werden gegengeprüft
- Strukturierter Research-Report

**Beispiel:**
```
Du: /research

"Welche Payment-Provider funktionieren am besten mit Node.js
 und haben die niedrigsten Gebühren für Europa?"

→ Vergleichstabelle mit Stripe, Mollie, PayPal, Klarna
   inkl. Gebühren, Integrationsaufwand, Vor-/Nachteile
```

### `/sprint-review` — Quartals-Audit

![Sprint Review Skill](sprint-review/overview.png)

**Wann:** Alle 4-6 Wochen.

**Was passiert:**
- Tech Debt Analyse: Was muss dringend aufgeräumt werden?
- Backlog-Hygiene: Welche Issues sind veraltet?
- Architektur-Check: Hat sich technische Schulden angesammelt?
- Empfehlungen für die nächsten Wochen

### `/pitch` — Evidenz fuer Stakeholder-Termine

![Pitch Skill](pitch/pitch-overview.png)

**Wann:** Vor einem Stakeholder-Termin, nachdem `/sprint-review` gelaufen ist.

**Was passiert:**
- 8 Quellen werden read-only aggregiert: L3-Lessons-DB, lokale Implement-Reports, CI-Reports, Sprint-Files, ARCHITECTURE_DESIGN.md, INTENT-XX.md, Feature-Flag-Stand, Git-Log
- Architektur-Diff seit dem letzten Pitch wird berechnet
- Demo-Pfad-Heuristik schlaegt eine User-Journey vor, die die Intent-Erfuellung am besten zeigt
- Output: `pitch/PITCH-XX.md` mit Frontmatter (`metrics_snapshot`, `related_intents`, `demo_path`, `status`) + 5 Body-Sektionen — committed, NICHT gitignored

**Anti-Scope:** Skill erzeugt KEINE Slides, KEIN Voice-Over, KEINEN Outcome-Text und KEIN Demo-Video. Mensch baut die Story und macht die Live-Demo. Details in **Anhang L** (4P-Pipeline-Mapping).

### `/status` — Auf einen Blick

**Wann:** Immer wenn du wissen willst was gerade los ist.

**Output:**
```
SYSTEM STATUS — MeinShop v1.3.2
─────────────────────────────────
✓ Alle Daemons laufen
✓ Letzte Änderung: vor 2h (SHOP-42 deployed)
⚠ 3 offene Issues in Backlog
✓ Win-Rate letzte 7 Tage: 87%
✓ Keine offenen Incidents
```

### `/integration-test` — Nach jeder Änderung

**Wann:** Automatisch nach `/implement`, aber auch manuell aufrufbar.

**Was passiert:**
Claude führt vordefinierte Checks durch und zeigt:
- Tier-1 Checks (KRITISCH — müssen grün sein)
- Tier-2 Checks (Warnungen — sollten geprüft werden)

---

## 7. Die Artefakte — was entsteht, wo, und warum

### Was ist ein Artefakt?

Ein **Artefakt** ist eine Datei, die das Governance-Framework erzeugt oder erwartet — Doku,
Checklists, Hooks, Specs, Automation-Scripts, Memory-Eintraege. Jedes Artefakt hat einen
klaren Zweck und wird von bestimmten Skills gelesen oder geschrieben.

Die meisten Teams sammeln Doku ad-hoc. Das Code-Crash Framework definiert ein festes, minimales Set von
Artefakten die zusammen nachvollziehbare, reproduzierbare, KI-freundliche Entwicklung
ermoeglichen.

### Die 5 Artefakt-Gruppen

![Artefakte-Landkarte — alle Artefakte auf einen Blick](bootstrap/docs/artifact-map.png)

*Die komplette Artefakte-Landkarte: jede Governance-Datei, jeder Hook, jede Spec, jede Automation die Bootstrap erzeugt — gruppiert in 5 Kategorien, mit Pfeilen die zeigen welcher Skill welches Artefakt nutzt. ([Excalidraw-Quelle](bootstrap/docs/artifact-map.excalidraw))*

#### Gruppe A — Governance-Doku

Regeln · Architektur · Prozess · Historie.

| Artefakt | Zweck | Geschrieben von | Gelesen von |
|----------|-------|-----------------|-------------|
| `CLAUDE.md` | Claude-Identitaet + Projektregeln | bootstrap + du | jeder Skill (automatisch beim Session-Start) |
| `CONVENTIONS.md` | Projekt-lokaler Vertrag: Governance-Modus, Execution-Isolation, aktive Gates | bootstrap + du | `/ideation`, `/implement`, `/architecture-review`, `/sprint-review`, Tool-Adapter |
| `GOVERNANCE.md` | Prozess-Regeln — wann/warum | bootstrap | jeder Skill |
| `SYSTEM_ARCHITECTURE.md` | Ueberblick Komponenten, Datenfluss | bootstrap + `/implement` | jeder Skill |
| `ARCHITECTURE_DESIGN.md` | Lead-Dokument — alle ADRs, 8 Sektionen | bootstrap + `/ideation` | `/implement`, `/architecture-review`, `/sprint-review` |
| `INDEX.md` | Datei-Index | bootstrap + `/implement` | jeder Skill |
| `COMPONENT_INVENTORY.md` | Komponenten-Inventur | bootstrap + `/implement` | Self-Healing (Check U) |
| `DEVELOPMENT_PROCESS.md` | Prozess-Referenz | bootstrap | Referenz |
| `SECURITY.md` | Security-Policy | bootstrap + `/security-architect` | `/implement`, `/sprint-review` |
| `CHANGELOG.md` | Was hat sich wann geaendert | `/implement` (auto) | jeder Skill |
| `API_INVENTORY.md` | Alle externen APIs | `/implement` | `/security-architect` (AUDIT) |
| `journal/STRATEGY_LOG.md` | Strategische Entscheidungen | du + `/ideation` | `/ideation` (Pflicht vor Story-Erstellung) |
| `journal/LEARNINGS.md` | Outcome-Tracking | `/implement` (nach Issue-Close) | `/sprint-review` |
| `lib/config.js` | Single Source of Truth: VERSION + DOC_FILES | bootstrap | Self-Healing, doc-version-sync |

### Security-Dokumentationsmodell

Security im Code-Crash Framework ist keine einzelne Checkliste, sondern ein verknuepftes Dokumentationsmodell:

*Sketch: Der Security-Workflow zeigt, wie `ARCHITECTURE_DESIGN.md`, `SECURITY.md`, Unterartefakte, Skill-Gates und Learning Loop ineinandergreifen. ([Excalidraw-Quelle](docs/security-workflow.excalidraw))*

| Ebene | Artefakt | Rolle |
|---|---|---|
| Architektur-Leitvertrag | `ARCHITECTURE_DESIGN.md` | Nennt Security als Qualitaetsdimension, dokumentiert Security-/Privacy-Grenzen und verweist auf den Security-Vertrag. |
| Operativer Security-Vertrag | `SECURITY.md` | Definiert Security-Grundsatz, Secrets-Policy, Change-Type-Matrix, Validation Evidence, sensitive Pfade und Incident-Notizen. |
| Security-Unterartefakte | `API_INVENTORY.md`, `.semgrep.yml`, `.codex/hooks.json`, `.claude/sensitive-paths.json`, `.codex/sensitive-paths.json`, Threat Models, Privacy-/Compliance-Dokumente | Enthalten konkrete Evidenz, Provider-/API-Details, technische Gates und Human-Review-Regeln. |

Der Ablauf ist bewusst gesteuert: `/ideation` schreibt `Security Impact` und, falls relevant, `Security Validation` in die Story. `/implement` liest `ARCHITECTURE_DESIGN.md`, `SECURITY.md` und die passenden Unterartefakte, bevor Code geaendert wird. `/security-architect` ergaenzt Threat Models, Policies oder Reviews bei riskanten Aenderungen. `/architecture-review` prueft, ob Security weiter zum Architektur-Zielbild passt. `/sprint-review` sucht nach Security-Schulden, offenen Findings und wiederkehrenden Mustern.

Damit wird Security by Design operativ: Security Impact planen, gegen den Vertrag implementieren, mit Gates validieren, betroffene Artefakte aktualisieren und wiederkehrende Findings in den Learning Loop zurueckspielen.

#### Gruppe B — Checklists + Guardrails

Maschinell erzwungene Regeln und Referenzlisten.

| Artefakt | Zweck | Enforcement |
|----------|-------|-------------|
| `.claude/hooks/spec-gate.sh` | Blockiert `git commit ISSUE-XX` ohne `specs/ISSUE-XX.md` | **HARD GATE** (PreToolUse Hook) |
| `.claude/hooks/doc-version-sync.sh` | Blockiert `git push` bei VERSION-Drift zwischen DOC_FILES | **HARD GATE** (PreToolUse Hook) |
| `.claude/hooks/guard.sh` | Blockiert Zugriff auf `.env` und Schluessel-Dateien | Soft Guard |
| `.claude/hooks/format.sh` | Auto-Format bei Edit/Write (Biome/Black) | Passiv |
| `.claude/settings.json` | Hook-Registration + Permissions | Config |
| `eslint.config.mjs` / `.prettierrc` / `pyproject.toml` | Linting-Config (Stack-abhaengig) | Passiv + `/implement` Schritt 6a |
| `.claude/ISSUE_WRITING_GUIDELINES.md` | Issue-Format-Regeln | Referenz |
| `architecture-review/references/dimensions-detail.md` | Die 8 Standard- + 4 Add-on-Dimensionen | Referenz fuer `/ideation`, `/architecture-review`, `/sprint-review` |
| `implement/references/change-checklist.md` | Pro-Aenderung Validation | Referenz fuer `/implement` Schritt 6 |
| `security-architect/references/owasp-checklist.md` | OWASP Top 10:2025 + ASVS 5.0 | Referenz fuer `/security-architect` |

#### Gruppe C — Specs + Traceability

Der Pfad Idee → Issue → Spec → Commit → Changelog.

| Artefakt | Zweck | Aufbau |
|----------|-------|--------|
| `specs/TEMPLATE.md` | Template fuer neue Specs | Why · What · Constraints · Current State · Tasks (T1, T2…) |
| `specs/ISSUE-XX.md` | Eine Spec pro Story (Pflicht vor Commit) | Aus TEMPLATE gefuellt + `## Zusammenfassung` von `/implement` Schritt 8 |
| Backlog-Records / Adapter-Stories | Externes oder lokales Story-Tracking | Feature-Template oder Fix/Refactor-Template |
| Git Commits | Format: `T1: ISSUE-XX — Beschreibung` | Durch spec-gate.sh gegated |
| Obsidian Vault | Change-Logs + Projekt-Memory | Auto-sync durch `doc-sync.js` |

#### Gruppe D — Self-Healing + Automation

Runtime-Agents — kein Ops-Team noetig.

| Artefakt | Zweck | Frequenz |
|----------|-------|----------|
| `agents/self-healing.js` | Check M (Versionen) · U (Dateien) · P (Prozesse) + Telegram-Alert | Cron, alle 15 Min |
| `lib/doc-sync.js` | Sync in Obsidian-Vault | On demand + Cron |
| `.env` / `.env.example` | Secrets + API-Keys (gitignored) | Manuell |
| `agents/linear-automation-daemon.js` | Webhook-driven Auto-Implement | Optional |

#### Gruppe E — Skill-System

Skills konsumieren Artefakte aus A–D.

| Artefakt | Zweck |
|----------|-------|
| `~/.claude/skills/*` | Globale Skill-Quelle / Operator-Registry |
| `.claude/skills/*` | Projekt-lokale Skill-Kopien, gepinnt und portabel |
| `~/.claude/projects/-root/memory/MEMORY.md` | Globale Memory |
| `~/.claude/projects/-root/memory/project_{slug}_init.md` | Projekt-spezifische Memory |

#### Gruppe F — Environment-Manifest (BOO-34)

| Artefakt | Zweck |
|----------|-------|
| `.claude/environment.json` | Single Source of Truth fuer Umgebung (mac/vps/ci), verfuegbares Tooling und Default-Pfade |
| `.claude/generate-environment-json.sh` | Bash-Generator (BSD- und Linux-kompatibel, ohne Dependencies) |

##### Coding-Umgebungen — Mac vs. VPS vs. CI

Gleiche Governance-Code-Basis, drei sehr unterschiedliche Ausfuehrungs-Kontexte. Skills verhalten sich je nach `environment` leicht unterschiedlich:

- **`mac`** — Operator-Workstation. Interaktive Sessions, IDE-Integrationen verfuegbar (SonarLint-Plugin, ESLint-Extension), `brew` fuer Tool-Installs. `tools_available.sonarqube_ide_plugin` kann `true` sein, falls der Operator das Plugin installiert hat.
- **`vps`** — Server (z.B. Hostinger srv1443320). Keine IDE-Plugins, `apt`/`pip` fuer Installs, laeuft in tmux/screen, Reports landen in `journal/reports/local/`. `sonarqube_ide_plugin` ist immer `false`. Operator steuert via SSH.
- **`ci`** — GitHub Actions / GitLab CI Runner. Erkannt ueber env-var `$CI` egal welcher Wert. Reports landen in `journal/reports/ci/`, Lessons-Learned-Writes werden uebersprungen, damit CI ephemeral bleibt. CI-Check passiert ZUERST in der Detection, weil ein CI-Runner Linux ODER Mac sein kann.

Skills lesen die Datei in einem Schritt-0-Read. Schnelle Reads mit `grep`/`sed` reichen; fuer reichhaltigere Queries ist `jq` bequem (optionale Installation — `brew install jq` auf Mac, `apt install jq` auf VPS):

```bash
# Ohne jq (laeuft immer)
HAS_SEMGREP=$(grep '"semgrep"' .claude/environment.json | grep -oE 'true|false')

# Mit jq (reichhaltigere Queries)
ENV=$(jq -r .environment .claude/environment.json)
TESTS=$(jq -r .tools_available.tests .claude/environment.json)
REPORTS=$(jq -r .paths.reports_local .claude/environment.json)
```

Re-Generierung nach Tooling-Aenderungen: `bash .claude/generate-environment-json.sh --force`. Die Datei wird committed; `metadata.created_at` ist die Audit-Spur.

#### Gruppe G — Observability-Skelett (BOO-14)

| Artefakt | Zweck |
|----------|-------|
| `observability.md` | Zentrales Observability-Skelett (Projekt-Root) — drei Pflicht-Sektionen: Logging-Schema, Metrics-Endpoint, Alert-Rules |
| `observability/alerts/<service>.yml` | Pro Service eine Prometheus-Alert-Rules-Datei — Pflicht-Alerts: `{service}_down`, `{service}_error_rate_high` (>5%), `{service}_p95_slow` (p95 >1s) |
| `observability/.env.observability` | Routing-Konfiguration (Telegram / Slack / Email-Webhooks) — **gitignored**, nur `.env.observability.example` committed |

##### Die drei Saeulen der Observability

Schrader Code Crash Kap. 3 §Production Readiness §Observability + Kap. 4 §Run the System (Saeule 3 Observability): "Wer ohne Observability deployed, fliegt blind." Bootstrap legt das Geruest ab Tag 0 an; der Operator fuellt die Service-spezifischen Inhalte pro Block-C-Komponente.

- **Logging-Schema** — strukturiertes JSON mit Pflicht-Feldern `timestamp`, `level`, `service`, `trace_id`, `message`, `context`. Stack-Defaults: Node.js → `pino`, Python → `structlog`.
- **Metrics-Endpoint** — `/metrics` im Prometheus-Format pro Service, Port-Konvention `9090+N` (auth=9091, api=9092, db=9093, ...). Stack-Defaults: Node.js → `prom-client`, Python → `prometheus_client`.
- **Alert-Rules** — drei Pflicht-Alerts pro Service: `{service}_down` (`up == 0` fuer >2 min, severity critical), `{service}_error_rate_high` (errors/requests >5% fuer 5 min, severity warning), `{service}_p95_slow` (p95(request_duration_seconds) >1s fuer 5 min, severity warning). Lokale Validierung via `promtool check rules observability/alerts/*.yml`.

Bestands-Projekte: `bash <skill-repo>/bootstrap/scripts/migrate-to-v2.sh --issue BOO-14` legt die drei Files idempotent an. Operator-Schritte zur Service-Befuellung: siehe `bootstrap/references/migration-checklist-v1-to-v2.md §BOO-14`.

#### Gruppe H — Reliability-Skelett (BOO-25)

| Artefakt | Zweck |
|----------|-------|
| `lib/idempotency.{js,py}` | Idempotency-Middleware (Redis-basiert) — Pflicht-Header `Idempotency-Key`, Verhalten: gleicher Key + gleicher Body → cached Response, gleicher Key + abweichender Body → HTTP 422 |
| `lib/retry.{js,py}` | Retry-Helper mit Exponential-Backoff + Jitter — Defaults: maxRetries=3, baseDelay=200ms, factor=2; **kein Retry bei 4xx**, kein Retry bei 422-Idempotency-Konflikten |
| `lib/circuit-breaker.{js,py}` | Circuit-Breaker-Wrapper — Defaults: errorThresholdPercentage=50, resetTimeout=30s, volumeThreshold=10; ein Breaker pro externer Abhaengigkeit (DB, Auth, externe API, Message Bus) |
| `docs/SLO.md` | Service-Level-Objectives-Skelett — Availability-Ziel, Error-Budget-Tabelle pro Quartal, mindestens 3 SLIs aus dem BOO-14-Metrics-Endpoint, Review-Cadence im `/sprint-review` |

##### Die fuenf Saeulen der Reliability

Schrader Code Crash Kap. 4 §Run the System (Saeule 6 Reliability): "Wer kein Error-Budget hat, weiss nicht, wann er stoppen muss." Bootstrap legt die vier Skelette ab Tag 0 an; der Operator entscheidet pro Service welche Saeulen aktiv sind und verdrahtet Middleware/Wrapper in die Entry-Points.

- **Idempotenz** — Doppel-Writes mit gleichem `Idempotency-Key` liefern die cached Response; abweichende Bodies bei gleichem Key liefern HTTP 422. Cache-Backend: Redis (`REDIS_URL`).
- **Retry + Backoff** — Exponential-Backoff mit Jitter fuer transiente Downstream-Fehler. Status-Filter: nur 5xx und Netzwerk-Fehler werden retried; 4xx und Idempotency-Konflikte (422) nicht.
- **Circuit Breaker** — Pro-Abhaengigkeit-Breaker, der nach Ueberschreiten der Error-Rate-Schwelle oeffnet, fuer `resetTimeout` Calls blockiert und dann half-open prueft, ob die Abhaengigkeit zurueck ist. Schwellen pro Abhaengigkeit tunen.
- **Graceful Degradation** — Explizite Fallback-Pfade wenn ein Downstream offen oder langsam ist (cached Read, Queue-and-Forget, Feature-Flag aus). Pro Service in der Reliability-Sektion dokumentiert.
- **SLO + Error-Budget** — Availability-Ziel (z.B. 99.9%), Error-Budget pro Quartal, mindestens 3 SLIs (`error_rate`, `p95_latency`, `availability`) gegen den BOO-14-Metrics-Endpoint gemessen. Pflicht-Pruefung in jedem Sprint-Review; Budget-Exhaustion loest Stop-Ship aus.

Bestands-Projekte: `bash <skill-repo>/bootstrap/scripts/migrate-to-v2.sh --issue BOO-25` legt die vier Files idempotent an (Stack-Detection via `package.json` / `pyproject.toml` / `requirements.txt`). Operator-Schritte zur Aktivierung: siehe `bootstrap/references/migration-checklist-v1-to-v2.md §BOO-25`. Cross-Link: `architecture-review/references/dimensions-detail.md` §1.1-§1.5 detailliert jede Saeule.

#### Gruppe I — Implement-Run Local Reports (BOO-36)

`/implement` Schritt 6 persistiert raw Tool-Outputs parallel zur deklarativen Iteration. Das Verzeichnis ist **gitignored** — `/sprint-review` aggregiert die Reports spaeter in `journal/sprint-{date}.md`.

| Artefakt | Zweck | Geschrieben von | Gelesen von |
|----------|-------|-----------------|-------------|
| `journal/reports/local/{YYYY-MM-DD_HHMM}_{STORY-ID}/eslint-iter{N}.sarif` | ESLint-SARIF pro Iteration (Fallback `.json`) | `/implement` Schritt 6a | `/sprint-review` |
| `journal/reports/local/{YYYY-MM-DD_HHMM}_{STORY-ID}/tests-iter{N}.junit.xml` | JUnit-XML pro Test-Iteration | `/implement` Schritt 6a-quart | `/sprint-review` |
| `journal/reports/local/{YYYY-MM-DD_HHMM}_{STORY-ID}/coverage-final.json` | Coverage-Endstand (c8 / pytest-cov) | `/implement` Schritt 6a-quart | `/sprint-review` |
| `journal/reports/local/{YYYY-MM-DD_HHMM}_{STORY-ID}/semgrep-final.sarif` | Semgrep-SARIF-Endstand | `/implement` Schritt 6a-bis | `/sprint-review` |
| `journal/reports/local/{YYYY-MM-DD_HHMM}_{STORY-ID}/meta.json` | Run-Metadaten (Schema unten) | `/implement` Schritt 6f-bis | `/sprint-review` |

##### meta.json Schema

```json
{
  "story_id": "BOO-15",
  "started_at": "2026-04-27T14:30:00Z",
  "completed_at": "2026-04-27T14:34:00Z",
  "iterations": {
    "eslint": 3,
    "tests": 2,
    "semgrep": 1,
    "coverage": 1
  },
  "final_status": "passed",
  "environment": "mac"
}
```

Feld-Konvention:
- `story_id` — Backlog-Record- oder Adapter-Key
- `started_at` / `completed_at` — ISO-8601 UTC
- `iterations.<gate>` — Anzahl Iterationen pro Gate, 0 wenn Gate uebersprungen
- `final_status` — `passed` | `failed` | `stopped_iteration_limit`
- `environment` — `mac` | `vps` | `ci` | `unknown` (gespiegelt aus `.claude/environment.json`)

##### Verantwortlichkeits-Trennung

| Wer | Schreibt | Liest |
|-----|----------|-------|
| `/implement` | `journal/reports/local/` (raw Outputs + meta.json) | nichts |
| `/sprint-review` (erste Phase) | `journal/sprint-{date}.md` (aggregiert) | `journal/reports/local/` + `journal/reports/ci/` |
| `/sprint-review` (zweite Phase) | `journal/learnings.db` (parsed L2) | nichts |

Die Trennung ist hart: Implement persistiert, Sprint-Review aggregiert. `/implement` schreibt **nicht** direkt in die L3-Learnings-DB. Das haelt Implement schnell (kein DB-Lock, kein Schema-Wissen) und macht Sprint-Review zum Single Writer der Learnings-DB.

### Wie liest man ein Artefakt? — Anatomie-Beispiel `specs/ISSUE-XX.md`

Jedes Spec-File folgt derselben Struktur:

```markdown
# SHOP-42 — Bestellverfolgung

## Why
Kunden fragen oft per E-Mail "wo ist meine Bestellung?". Eine Tracking-Seite reduziert
Support-Last und verbessert UX.

## What
- Deliverable: `/orders/:id/track` Seite mit Live-Status
- Done wenn: Kunde sieht Status + Timestamps + Carrier-Link

## Constraints
- MUST: bestehendes Order-DB-Schema wiederverwenden
- MUST NOT: neue externe API ohne Freigabe
- Out of scope: E-Mail-Benachrichtigungen (separate Story)

## Current State
- `src/routes/orders.js` — aktuell List/Detail-Views
- `lib/order-db.js` — Schema v12

## Tasks
- T1: `/orders/:id/track` Route (Dateien: src/routes/orders.js) — Verify via /orders/1/track
- T2: Tracking-Status-Komponente (Dateien: components/OrderTracking.jsx) — Verify via Storybook
- T3: Carrier-API anbinden (Dateien: lib/carrier-api.js, .env.example) — Verify via Mock

## Zusammenfassung
(wird nach Implementation durch /implement Schritt 8 gefuellt — 3 Absaetze, Laien-Sprache)
```

Diese Struktur ist nicht verhandelbar — der spec-gate-Hook erzwingt die Existenz der Datei,
und `/implement` Schritt 3c validiert die Form bevor die Plan-Phase beginnt.

### Welcher Skill schreibt/liest welches Artefakt?

Die [Artefakte-Landkarte](bootstrap/docs/artifact-map.png) oben zeigt die volle Matrix visuell.
Kurzzusammenfassung:

- **`/ideation`** schreibt: Backlog-Record / Adapter-Story, ADD-Sektion, Spec-Platzhalter. Liest: ARCHITECTURE_DESIGN.md, STRATEGY_LOG.md
- **`/implement`** schreibt: Code, specs/ISSUE-XX.md (Zusammenfassung), CHANGELOG.md, LEARNINGS.md. Liest: Spec, ARCHITECTURE_DESIGN.md, Change-Checklist
- **`/architecture-review`** liest: ALLE Gruppe-A-Dokumente + ADD + alle ADRs. Schreibt: Review-Report
- **`/sprint-review`** liest: ALLE Gruppe-A-Dokumente + LEARNINGS.md + Git-Log. Schreibt: Audit-Report
- **`/security-architect`** schreibt: SECURITY.md-Updates, Threat-Models. Liest: OWASP-Checklist, STRIDE-Refs

### Die goldene Regel

> **Jedes Artefakt hat einen Zweck. Jeder Skill konsumiert oder schreibt bestimmte Artefakte.
> Kein Skill schreibt in ein Artefakt das er nicht besitzt. Kein Artefakt wird dupliziert.**

Das ist das ganze Framework in einem Satz.

---

## 8. Die Guardrails — dein Sicherheitsnetz

### Was sind Guardrails?

Guardrails sind **automatische Sicherheitsmechanismen** die verhindern dass du aus Versehen
Dinge tust die du bereust. Nicht als Strafe — als dein Fallschirm.

### Guardrail 1: Spec-Gate (Git Hook)

**Problem:** Du änderst Code ohne zu wissen warum — und in 3 Wochen erinnerst du dich nicht mehr.

**Lösung:** Bevor du Code committen kannst (der zu einem Issue gehört), muss ein Spec-File
(`specs/SHOP-42.md`) existieren das erklärt **was** und **warum**.

```bash
git commit -m "SHOP-42: Add order tracking"
# → Ohne specs/SHOP-42.md: BLOCKIERT
# → Mit specs/SHOP-42.md: erlaubt

# ⛔ spec-gate: specs/SHOP-42.md fehlt!
#    Erstelle zuerst specs/SHOP-42.md aus specs/TEMPLATE.md
#    Bypass: git commit --no-verify (nur wenn du bewusst drüber bist)
```

**Bypass vorhanden?** Ja: `--no-verify`. Aber du weißt dann bewusst dass du die Regel brichst.

### Guardrail 2: Doc-Version-Sync (Git Hook)

**Problem:** Du erhöhst die Version in `config.js` aber vergisst 5 Dokumentationsdateien.

**Lösung:** Wenn `config.js` mit einer neuen Version gestaged ist, prüft der Hook automatisch
ob alle Docs auf der gleichen Version sind.

```bash
git commit -m "v1.4.0 - neue Features"
# → config.js: VERSION = '1.4.0'
# → SYSTEM_ARCHITECTURE.md: Version: 1.3.2 → BLOCKIERT

# ⛔ doc-version-sync: SYSTEM_ARCHITECTURE.md noch auf v1.3.2!
#    Bitte auf v1.4.0 aktualisieren
```

### Guardrail 3: Self-Healing Agent

Ein Agent der alle 15 Minuten im Hintergrund prüft:

| Check | Was wird geprüft |
|-------|-----------------|
| Signal Freshness | Sind alle Daten aktuell? |
| Doc Sync | Stimmen alle Dokumentationsversionen überein? |
| Architecture Guard | Sind Kern-Regeln eingehalten? |
| API Health | Sind alle externen APIs erreichbar? |
| Security Events | Gab es verdächtige Aktivitäten? |

Bei Problemen: Telegram-Alert (wenn eingerichtet) oder Log-Eintrag in `journal/`.

### Guardrail 4: Spec-Driven Development

Die einfachste aber mächtigste Regel:

```
NIEMALS Code ändern ohne Backlog-Record oder Adapter-Story
NIEMALS Code committen ohne Spec-File (specs/ISSUE-ID.md)
NIEMALS Operator (= du) übergehen — immer erst zeigen dann tun
```

Das klingt nach extra Arbeit. In der Praxis dauert ein Spec-File 2 Minuten — und verhindert
Stunden an Debug-Arbeit weil du weißt was du warum gebaut hast.

### Guardrail 5: Operator-in-the-Loop

Bei `/implement`: **Schritt 3 ist immer ein Pause-Punkt.**
Claude zeigt dir den Plan, du sagst OK, dann erst wird Code geschrieben.

Du kannst niemals aus Versehen etwas deployen das du nicht gesehen hast.

---

## 8b. Anti-Patterns auf Programm-Ebene — Schrader Kap. 7

Schrader beschreibt in Kap. 7 "Risiken und Anti-Patterns" 11 Muster, die entstehen wenn KI-gestützte Entwicklung falsch skaliert. Die technischen Anti-Patterns sind in den Skill-Gates operationalisiert (BOO-3 bis BOO-19). Die organisatorischen Anti-Patterns sind nicht automatisch detektierbar — sie erfordern menschliche Reflexion.

Dieser Abschnitt dokumentiert die vier kulturellen/organisatorischen APs, die kein Skill abdecken kann:

### AP6: Erfahrungsschulden

Wenn Features ohne ausreichendes UX-/Design-Review ausgeliefert werden. KI beschleunigt das: funktionierende Software entsteht in Minuten — ohne die natürliche Bremse, die früher Zeit für Design erzwang.

**Woran du es erkennst:** Nutzer fragen regelmäßig "Wie macht man das nochmal?", obwohl sie das Produkt kennen. Support-Volumen steigt für Fragen, die ein intuitives Produkt gar nicht aufwirft. Features existieren, werden aber nicht gefunden.

**Gegenmittel:**
- Erfahrungsschulden sichtbar machen: Widersprüchliche Interaktionsmuster zählen
- Design-Check als Gate am lauffähigen Kandidaten, nicht am Mockup
- 15%-Budget für UX-Vereinheitlichung (analog zur 15%-Regel für technische Schulden)
- Feedback-Schleifen mit echten Nutzern: Messen WIE Features genutzt werden

> "Ein Produkt, das technisch sauber ist und eine schlechte Experience bietet, verliert gegen ein Produkt, das technisch fragwürdig ist, sich aber gut anfühlt. Experience ist kein Add-on — sie ist das Produkt." — Schrader

### AP7: Verantwortungsdiffusion

Niemand fühlt sich für KI-generierten Code verantwortlich. Die KI hat generiert, der Entwickler hat geprüft, der Tester getestet — wenn etwas schiefgeht, ist die implizite Antwort: "Die KI hat es so gemacht."

**Woran du es erkennst:** Bei Problemen wird nach Schuldigen gesucht statt nach Ursachen. Retrospektiven enden ohne klare Verantwortlichkeiten. Product Owner sagen "Das war technisch, nicht meine Verantwortung."

**Klare Accountability-Regeln:**
1. Wer den Intent formuliert, ist dafür verantwortlich
2. Wer Code generieren lässt, ist für den Code verantwortlich — "Die KI hat es so gemacht" ist keine Entschuldigung
3. Wer reviewt, teilt die Verantwortung für Qualität
4. Jedes Teammitglied ist persönlich für das Ergebnis verantwortlich

Diese Regeln müssen **explizit dokumentiert und gelebt** werden — nicht nur angenommen.

### AP9: Individual-First als Isolation

"Jede und jeder arbeitet jetzt eigenständig mit KI!" Das Team löst sich in Einzelpersonen auf. Ergebnis: Silos, Doppelarbeit, widersprüchliche Architektur.

**Woran du es erkennst:** Dieselben Probleme werden von verschiedenen Personen auf verschiedene Arten gelöst. Architekturentscheidungen widersprechen einander. Onboarding neuer Talente dauert länger statt kürzer.

**Gegenmittel:**
1. **Zeitversetzte Architektur-Reviews:** Wöchentliche Team-Reviews der Architekturentscheidungen
2. **Geteilte Code-Verantwortung:** Jedes Modul ist mindestens zwei Personen bekannt
3. **Dokumentation als Kernarbeit:** Nicht optional, nicht "später"
4. **Regelmäßige interne Demos:** Nicht für Kunden — für das Team selbst

> "Individual + KI ist die atomare Einheit. Aber Atome brauchen Moleküle, um Materie zu bilden." — Schrader

### AP11: Die politischen Saboteure

Die schwierigsten Anti-Patterns entstehen nicht aus Inkompetenz, sondern aus Kalkül. Drei Typen:

**Der Neid-Saboteur:** Jemand, dessen Status durch KI-Produktivitätsgewinne bedroht wird. Reaktion: subtile Sabotage — Code-Reviews die zu lange dauern, Standards die plötzlich nicht verhandelbar sind, Skepsis verpackt als konstruktive Kritik.

**Der Power Player:** Eine Abteilung, die durch die Transformation Einfluss verliert. Reaktion: strategische Bedenken in Steuerungskomitees, Pilotprojekte werden in den eigenen Bereich gezogen und ausgehungert.

**Der Angst-Blocker:** Ein technisch brillanter Mitarbeiter, der blockiert aus Selbstschutz. Reaktion: übermäßige Komplexität einführen, jede Vereinfachung wird zum Sicherheitsrisiko erklärt.

**Das Radar:** Das Muster erkennen, nicht einzelne Aktionen isoliert bewerten. Folge dem Budget und dem Einfluss — wer verliert durch die Transformation? Das sind die Risikozonen. Konstruktiv ansprechen bevor es destruktiv wird.

---

**Vollständiger Katalog aller 11 APs** (inkl. technische mit Skill-Abdeckung): `code-crash-framework/references/anti-pattern-katalog.md`

**Automatische Sprint-Diagnose:** `/sprint-review` Schritt 7 stellt pro AP eine Diagnose-Frage und empfiehlt Maßnahmen bei Treffern.

**Referenz:** Schrader "Code Crash" (2026), Kapitel 7 "Risiken und Anti-Patterns", Z. 3626ff.

---

## 8c. Production Readiness nach Schrader

Schrader behandelt in Kap. 3 §Production Readiness und Kap. 4 §Run the System die Anforderungen an KI-gestützt entwickelten Code, der in Produktion gehen soll. Wir haben die Punkte in die bestehenden Skills und Gates eingearbeitet — nicht 1:1, sondern adaptiert an unsere Pipeline.

**Was wir bewusst NICHT 1:1 übernommen haben:**

- **Intent-Propagation** dreistufig statt binär: Schrader beschreibt Intent als einen Übergabepunkt; wir verankern ihn an drei Stellen — Gate in `/ideation` (Story-Aufnahme), Gewichtung in `/backlog` (Priorisierung), Measure-Loop in `/implement` (Verifikation nach dem Bauen).
- **4P-Pipeline (Perceive/Prompt/Produce/Pitch)** nicht als Umbenennung: Wir behalten unsere bestehenden Phasen (Intent → Ideation → Implement → Review) und mappen 4P konzeptionell, ohne die Pipeline neu zu beschriften. Begründung: Stabilität der Skill-Namen über Versionen hinweg.

### Mapping-Tabelle

| Schrader-Thema | Kapitel / Seite | Unsere Governance-Entsprechung | Wo im Skill verankert | Linear-Issue |
| -- | -- | -- | -- | -- |
| Intent before Implementation | Kap. 4 S. 82ff | `/intent`-Skill | `~/.claude/skills/intent/` | BOO-1 |
| Intent-Propagation | Kap. 4 S. 130ff | Gate in `/ideation`, Gewichtung in `/backlog`, Measure-Loop in `/implement` | 3 Skills | BOO-10 |
| KI-taugliche Architektur | Kap. 4 S. 105ff | KI-Tauglichkeit-Checkliste in `/architecture-review` | `architecture-review/SKILL.md` | BOO-7 |
| Run the System — Security | Kap. 4 S. 98 | Zweistufiges SAST (Semgrep + SonarQube) | `/bootstrap`, `/implement` Schritt 6a | BOO-3/4/5/6 |
| Run the System — Testability | Kap. 4 S. 100 | Testability als eigene Dimension + Coverage-Gate | `architecture-dimensions/testability.md`, `/implement` 6a | BOO-8, BOO-15 |
| Run the System — Observability | Kap. 4 S. 102 | Observability als eigene Dimension + Pflicht-Skelett | `architecture-dimensions/observability.md`, `/bootstrap` Phase 4 | BOO-8, BOO-14 |
| Run the System — Scalability | Kap. 3 S. 66 | Scalability als eigene Dimension (4 Invarianten) | `architecture-dimensions/scalability.md`, `/architecture-review` | BOO-13 |
| Run the System — Performance | Kap. 3 S. 66 | Performance-Baseline-Gate | `/implement`, CI-Workflow `perf.yml` | BOO-16 |
| Production-Readiness-Gates | Kap. 3 S. 66 | ESLint + Semgrep + SonarQube + Coverage + Performance + Human Review | `/implement` Schritt 6 | BOO-3/4/5/6, 15, 16, 18 |
| Halluzinations-Check | Kap. 3 S. 66 | Dependency + Existenz-Check | `/implement` Schritt 6a | BOO-12 |
| Feature Flags für AI-Code | Kap. 3 S. 68ff | Rollout-Konvention im Spec-Template | `spec-gate.sh`, Spec-Template | BOO-17 |
| Mandatory Human Review | Kap. 3 S. 68ff | `sensitive-paths.json` + Review-Gate | `/implement` Schritt 5.5 | BOO-18 |
| Audit Trails | Kap. 3 S. 68ff | Session-Log-Linkage im Spec + `audit-trace.sh` | `/implement`, `scripts/audit-trace.sh` | BOO-19 |
| 4P-Pipeline (Perceive/Prompt/Produce/Pitch) | Kap. 5 S. 135ff | NICHT 1:1 übernommen, in bestehende Pipeline gemappt | — | Meeting-Minute 2026-04-22 §EP4 |

> Die Dimensions-Pfade in Spalte 4 (`architecture-dimensions/testability.md` etc.) referenzieren die logische Verankerung in der Skill-Architektur. Die ausgeschriebenen Dimensions-Details liegen real konsolidiert in `code-crash-framework/architecture-review/references/dimensions-detail.md`.

---

## 8d. Coding-Umgebungen Mac / VPS / CI

Die Toolchain läuft in vier Umgebungen unterschiedlich. **Kernpunkt:** Keine Qualitäts-Einbuße beim VPS-Coding — die Gates sind dieselben (ESLint, Semgrep, Coverage, Performance). Was anders ist: die Tooling-Liste. IDE-spezifische Plugins (Error Lens, SonarQube for IDE) gibt es nur auf dem Mac in VS Code; auf dem VPS arbeitest du mit den CLI-Varianten. SonarQube Cloud läuft serverseitig und unabhängig von der Coding-Umgebung — der Server analysiert nach jedem CI-Lauf.

| Tool | Mac (VS Code) | Mac (Terminal) | VPS via SSH | GitHub Actions |
| -- | -- | -- | -- | -- |
| Error Lens | ✓ Plugin | ✗ | ✗ | ✗ |
| ESLint VS-Code-Plugin | ✓ Plugin | ✗ | ✗ | ✗ |
| ESLint CLI (`npx eslint`) | ✓ via npm | ✓ | ✓ (npm) | ✓ (Action) |
| SonarQube for IDE | ✓ Plugin | ✗ | ✗ | ✗ |
| SonarQube Cloud | n/a | n/a | n/a | ✓ (server-side) |
| Semgrep CLI | ✓ | ✓ | ✓ | ✓ (Action) |
| Tests (Vitest/pytest) | ✓ via npm | ✓ | ✓ | ✓ |

Praxisregel: Wenn du auf dem VPS via SSH arbeitest, erwartest du keine Inline-Hints im Editor — du läufst die CLIs explizit (`npx eslint .`, `semgrep --config auto .`, `npm test`). Die Gates schlagen in CI ohnehin zu, wenn du etwas durchrutschen lässt.

![Drei-Layer-Quality-Gate — IDE / CLI / CI entlang der Coding-Zeitachse](docs/quality-gate-three-layers.png)

*Defense in Depth über drei Ebenen: IDE-Plugins für Echtzeit-Feedback beim Tippen, CLI-Tools als harte Pre-Commit-Sperre, GitHub Actions als Merge-Gate nach dem Push. Je früher ein Defekt erkannt wird, desto billiger der Fix. ([Excalidraw-Quelle](docs/quality-gate-three-layers.excalidraw))*

> **Hinweis zur Skizzen-Beschriftung:** Die Excalidraw zeigt BOO-28 noch als "geplant". Seit v3.17.0 (2026-05-12) ist BOO-28 done — `migrate_boo_28()` legt `.github/workflows/eslint.yml` (Node-Stacks) bzw. `.github/workflows/ruff.yml` (Python-Stacks) mit Pflicht-SARIF-Output nach `.ci-reports/` an (Vorbereitung BOO-32 Hermes-Konsumtion). Das Neu-Rendern der PNG ist nicht Scope dieser Aufgabe.

**CI-Layer (Layer 3) — GitHub Actions:** Bootstrap legt Stack-abhängig die folgenden Workflow-Files in `.github/workflows/` an — alle drei schreiben SARIF nach `.ci-reports/` und uploaden via `github/codeql-action/upload-sarif@v3` in den GitHub-Security-Tab.

| Workflow | Trigger | Tool | Stack | Quelle (BOO) |
|----------|---------|------|-------|--------------|
| `eslint.yml` | push + pull_request | ESLint (Lint) | Node / JS / TS | BOO-28 |
| `ruff.yml` | push + pull_request | Ruff (Lint) | Python | BOO-28 |
| `semgrep.yml` | push + pull_request auf main | Semgrep (SAST) | alle | BOO-4 |
| `perf.yml` | pull_request auf main | autocannon / pytest-benchmark | alle | BOO-16 |
| `sonar.yml` | push auf main | SonarQube Cloud | alle | BOO-5 |

Required Status Checks `ESLint`, `Ruff`, `Semgrep`, `SonarCloud` werden über `gh api ... branches/main/protection` (BOO-29) aktiviert — ohne grünen Lauf kein Merge.

### Branch-Protection-Setup (BOO-29)

Seit v3.18.0 (2026-05-12) legt `/bootstrap` die `main`-Branch-Protection automatisch in **Phase 4.4k** an — direkt nach dem ersten `git push -u origin main` (Phase 4.9). Die Logik sitzt in `code-crash-framework/bootstrap/scripts/setup-branch-protection.sh`. Drei Punkte sind dabei wichtig:

1. **Dynamische Required Status Checks.** Das Skript liest alle Workflow-Dateien unter `.github/workflows/*.yml` und extrahiert pro Datei das erste `name:`-Feld — das ist der GitHub-Actions-Context-Name. Aus dieser Liste wird `required_status_checks[contexts][]` gebaut. Workflows, die in einem Stack fehlen (z.B. `ruff.yml` in einem reinen Node-Projekt), werden ausgelassen — kein hartes Failen.

2. **Voraussetzungen werden geprüft.** Vor dem `gh api`-Aufruf prüft das Skript: `gh --version` (CLI installiert?), `gh auth status` (eingeloggt mit `repo`-Scope?), `git remote get-url origin` (Remote vorhanden?), und `gh api repos/<owner>/<repo>/branches/main` (main-Branch existiert remote?). Bei Fehler bricht das Skript mit klarer Operator-Meldung ab — keine stille Akzeptanz.

3. **Idempotenz.** Der `gh api -X PUT`-Call ist ein Replace, kein Append — mehrfaches Ausführen überschreibt die Protection identisch. Auch in Bestands-Projekten (`migrate_boo_29()` in `migrate-to-v2.sh`) wird derselbe Code-Pfad benutzt — eine einzige Source of Truth.

Der gesetzte Protection-Block (1:1 aus BOO-29):

```bash
gh api -X PUT "repos/${OWNER}/${REPO}/branches/main/protection" \
  -F required_status_checks[strict]=true \
  -F required_status_checks[contexts][]=<dynamisch> \
  -F enforce_admins=false \
  -F required_pull_request_reviews[dismiss_stale_reviews]=true \
  -F required_pull_request_reviews[required_approving_review_count]=1 \
  -F restrictions=null \
  -F allow_force_pushes=false
```

`enforce_admins=false` ist bewusst — der Operator (typischerweise Admin) darf in Notfällen direkt auf `main` pushen. `allow_force_pushes=false` schützt die Git-Historie vor versehentlichem Überschreiben. `dismiss_stale_reviews=true` zwingt jeden Push nach einem Review zu einer neuen Approval-Runde — Code-Review-Trail bleibt aktuell.

---

## 8g. Linear-Setup pro Projekt (BOO-30)

Das Linear-Team hinter einem Projekt (`B.4 == Linear`) braucht zwei Konfigurations-Stücke zusätzlich zum Default, damit der Issue-Lebenszyklus sich selbst trägt: einen **sechsteiligen Workflow** und die **GitHub-Integration**. Beides sind einmalige Operator-Aufgaben pro Projekt — die Linear-API könnte das automatisieren, aber das Aufwand-/Nutzen-Verhältnis ist schlecht (einmaliger Setup, gut geführte UI). Bewusste Entscheidung, hier dokumentiert damit der Operator genau weiß was manuell und was automatisch ist.

**Klare Trennung manuell vs. automatisiert:**
- **Manuell pro Projekt (Operator):** die sechs Workflow-States anlegen + GitHub-Integration verbinden. Schritte unten.
- **Automatisiert via Bootstrap:** die Issue-Template-Erweiterung lebt in `bootstrap/references/issue-writing-guidelines-template.de.md` (v3.1). `/bootstrap` rendert `.claude/ISSUE_WRITING_GUIDELINES.md` mit der Pflicht-Sektion `## Definition of Done (Pflicht)`. `migrate_boo_27()` verankert den passenden DoD-Block in `.github/ISSUE_TEMPLATE/story.yml`. Bestands-Projekte können die Erweiterung über `migrate_boo_30()` (idempotent) nachziehen.

### Workflow-States (1:1 aus BOO-30)

Die sechs States sind die tragende Struktur. Ihre Namen sind nicht verhandelbar — die GitHub-Integration matcht auf sie, und die DoD-Checkliste referenziert den State `Done` direkt. Anlegen in **Linear → Settings → <Team> → Workflow** in genau dieser Reihenfolge:

| State | Bedeutung | Auto-Transition |
|---|---|---|
| Backlog | Triage | initial |
| In Progress | Skill arbeitet, lokale Gates iterativ | manuell |
| In Review | PR offen, CI läuft | auto bei PR-Open |
| QA Failed | CI rot, Story re-opened | manuell oder Webhook |
| Done | PR gemerged, alle Checks grün | auto bei PR-Merge |
| Cancelled | verworfen | manuell |

Die drei Paare sind bewusst: `Backlog` ↔ `Cancelled` klammert den Lebenszyklus (Start vs. verworfen), `In Progress` ↔ `In Review` klammert die Arbeitsphase (lokale Iteration vs. Remote-Validierung), `QA Failed` ↔ `Done` klammert das CI-Urteil (rot vs. grün). Wer `QA Failed` weglässt, kollabiert ein rotes CI in ein Re-Open von `In Progress` und verliert das Fehler-Häufigkeits-Signal, das `/sprint-review` ausliest.

### GitHub-Integration (manueller Operator-Setup)

**Linear → Settings → Integrations → GitHub → Connect Repository** öffnen und das Projekt-Repo auswählen. Nach dem OAuth-Handshake greift Linears Auto-Recognition sofort auf vier Flächen — ohne weitere Konfiguration:

- **Branch-Namen** mit `{ISSUE_PREFIX}-XX` (z.B. `BOO-30-feature-foo` oder `feature/BOO-30-foo`) verknüpfen den Branch automatisch mit dem Issue.
- **PR-Titel** mit `{ISSUE_PREFIX}-XX` verknüpfen den PR mit dem Issue und transitionen den State bei PR-Open auf `In Review`.
- **Commit-Messages** mit `{ISSUE_PREFIX}-XX` tauchen im Issue-Activity-Feed auf.
- **PR-Body** mit `Closes {ISSUE_PREFIX}-XX` schließt das Issue (Transition auf `Done`) wenn der PR gemerged wird.

Die Auto-Transitions decken die zwei CI-getriebenen Kanten ab (`In Progress` → `In Review` bei PR-Open, `In Review` → `Done` bei PR-Merge). Die zwei manuellen Kanten (`Backlog` → `In Progress`, irgendwas → `QA Failed`) bleiben manuell — das ist der Punkt: ein rotes CI muss eine Operator-Entscheidung auslösen, kein stilles Auto-Revert.

### Operator-Checkliste

- [ ] Sechs Workflow-States im Linear-Team angelegt (Namen exakt: `Backlog`, `In Progress`, `In Review`, `QA Failed`, `Done`, `Cancelled`)
- [ ] GitHub-Integration mit Projekt-Repo verbunden
- [ ] Test-Story mit Branch `{ISSUE_PREFIX}-XX-test` erstellt — PR-Open transitioniert das Issue auf `In Review`
- [ ] Issue-Writing-Guidelines (`.claude/ISSUE_WRITING_GUIDELINES.md`) auf die v3.1-DoD-Sektion geprüft — automatisch bei frischen Projekten, für Bestands-Projekte `migrate-to-v2.sh --issue BOO-30` ausführen

### Definition of Done (1:1 aus BOO-30)

Jedes Issue trägt diese Checkliste (seit v3.1 automatisch ins Template gerendert). Eine Story darf erst auf Linear-State `Done`, wenn:

```markdown
## Definition of Done (Pflicht)

Story darf erst auf Linear-Status "Done" wenn:
* [ ] Alle lokalen Gates gruen (ESLint, Semgrep, Tests, Coverage)
* [ ] PR ist gemerged auf main
* [ ] Alle Required Status Checks gruen (siehe BOO-29)
* [ ] Kein offener "QA Failed"-Status
* [ ] Spec-File `specs/BOO-XX.md` aktualisiert mit Result-Summary (Implement-Skill Schritt 8)
```

Die Punkte werden nicht pro Story angepasst. Wenn ein Gate wirklich nicht zutrifft (z.B. reine Doku-Story ohne Tests), markiert der Operator es mit `* [N/A] Tests — reine Doku-Story`, statt die Zeile zu löschen — der Audit-Trail bleibt erhalten.

> **Issue-Referenz:** BOO-30. Quellen: `bootstrap/references/issue-writing-guidelines-template.de.md` v3.1, `bootstrap/SKILL.md` Phase 4.4l, `bootstrap/scripts/migrate-to-v2.sh` §`migrate_boo_30`. Migration für Bestands-Projekte: `bootstrap/references/migration-checklist-v1-to-v2.md` §BOO-30.

---

## 8e. Skill-Architektur — /ideation vs /architecture-review

`/ideation` und `/architecture-review` sind die zwei strategischen Skills im Bundle. Sie wirken auf unterschiedlichen Zeitachsen und Scopes — die Unterscheidung muss klar sein, sonst doppelt sich die Arbeit oder fällt aus.

Abgrenzung: Das Framework ist zuerst eine sequenzielle Engineering-Pipeline mit Quality-Gates, nicht selbst ein vollautonomer Developer-Agent. Subagents sind in diesem Bild spezialisierte Ausfuehrungshelfer innerhalb einer kontrollierten Story. Eine Claude-, Codex- oder Hermes-Schicht kann das Framework agentisch nutzen, aber das Framework selbst bleibt die Struktur, die Autonomie durch Intent, Specs, Gates, Reports und menschliche Review-Punkte begrenzt.

| Dimension | `/ideation` | `/architecture-review` |
| -- | -- | -- |
| Trigger | bei jeder neuen Story (häufig) | periodisch / vor Phase-Wechseln (selten) |
| Scope | EINE Story | GESAMTES System |
| Zeithorizont | nächste 1-2 Tage Coding | nächste Wochen / Monate |
| L3-Query | "ähnliche Stories der letzten X Sprints" | "Trends über 12+ Sprints" |
| Output | bessere AC + Anti-Pattern-Warnung | Refactoring-Issues + ADRs + Dimension-Status |
| Charakter | proaktiv (vor dem Bauen) | reaktiv-strukturell (auf Gebautes schauen) |

### Datenfluss

```
ARCHITECTURE_DESIGN.md = Soll-Zustand
Code-Basis             = Ist-Zustand
L3-DB                  = Erfahrungs-Speicher

/ideation        → liest Soll + Erfahrung → schreibt neue Stories
/implement       → liest Detail-Soll → produziert Ist
/architecture-review → vergleicht Soll vs Ist + L3-Trends → aktualisiert Soll
/sprint-review   → schreibt L3 (Erfahrung)

Kreislauf:
  /architecture-review pflegt ARCHITECTURE_DESIGN.md aktuell
                           ↓
                       /ideation liest sie
                           ↓
                       schreibt bessere Stories
                           ↓
                       /implement baut sie
                           ↓
                       /sprint-review aggregiert
                           ↓
                       L3-DB
                           ↓
  /architecture-review ←  liest L3 + Code-Basis für nächsten Audit
```

![Skill-Datenfluss-Kreislauf — 4 Skills, 3 Datenquellen, ein geschlossener Loop](docs/skill-dataflow-cycle.png)

*Die vier Skills arbeiten auf drei Datenquellen (`ARCHITECTURE_DESIGN.md` Soll-Zustand, Code-Basis Ist-Zustand, L3-DB Erfahrungs-Speicher). Jeder Sprint schließt den Kreis: `/architecture-review` hält das Soll aktuell, `/ideation` schreibt Stories dagegen, `/implement` produziert das Ist, `/sprint-review` aggregiert nach L3. ([Excalidraw-Quelle](docs/skill-dataflow-cycle.excalidraw))*

![L3-DB Reader und Writer — wer schreibt wann, wer liest wann](docs/l3-db-readers-writers.png)

*Learning-Loop-Storage in drei Stufen (L1 Markdown, L2 Markdown mit Frontmatter, L3 SQLite). `/sprint-review` ist einziger Writer (Schritt 7, Pflicht). `/ideation` liest die letzten 3 Einträge beim Story-Start (Schritt 0.5), `/architecture-review` liest L3-Trends als ADR-Kontext. Der `.learning-loop` File-Marker bestimmt den aktiven Level. ([Excalidraw-Quelle](docs/l3-db-readers-writers.excalidraw))*

---

## 8f. Performance-Baseline — Pre-Production-Gate vs Production-Alarm

Performance-Regressionen werden an zwei Stellen abgefangen — vor dem Merge (CI-Gate, BOO-16) und nach dem Deploy (Production-Alarm, BOO-14). Die zwei Mechanismen sind komplementär:

- **BOO-14 Production-Alarm** (`{service}_p95_slow`): Loest aus, wenn p95 in Produktion länger als 5 Minuten >1s ist. Severity warning. Quelle: Metrics-Endpoint pro Service.
- **BOO-16 Pre-Production-Gate** (`.github/workflows/perf.yml`): Vergleicht den CI-Bench-Lauf gegen die Living-Baseline in `journal/perf-baseline.json`. Schwellen: ≤5% Differenz = PASS, 5-20% = WARN (PR-Kommentar), >20% = FAIL (Merge blockiert). Override per PR-Label `perf-override` oder Commit-Trailer `Perf-Override: <Grund>`, append-only in `journal/reports/perf/overrides.log`.

Ohne Pre-Production-Gate wird die Regression erst nach dem Deploy sichtbar — der Production-Alarm allein ist also ein zu spätes Warnsignal. Ohne Living-Baseline würde jede Regression automatisch die neue Baseline werden (Anti-Pattern), deswegen wird die Baseline manuell vom Operator nach dem ersten grünen CI-Lauf gefüllt.

### Artefakte

| Artefakt | Zweck | Quelle |
|---|---|---|
| `journal/perf-baseline.json` | Living Baseline pro Service | Operator nach erstem grünen CI-Lauf |
| `bench/<service>.bench.js` oder `bench/<service>_bench.py` | Service-Benchmark | `migrate_boo_16()` aus Template |
| `.github/workflows/perf.yml` | CI-Gate (≤5% PASS, 5–20% WARN, >20% FAIL) | `migrate_boo_16()` |

**Referenz:** Schrader Code Crash Kap. 3 §Production Readiness (Gate 3: Performance Baseline). Pendant zum Production-Alarm `{service}_p95_slow` aus BOO-14.

---

## 9. VS Code Setup

### Claude Code Extension

Die offizielle Claude Code Extension für VS Code integriert alles direkt in deinen Editor:

- Terminal mit Claude Code direkt in VS Code
- Datei-Kontext wird automatisch an Claude übergeben
- Inline Code-Vorschläge
- Direkt aus dem Editor `/implement` aufrufen

**Installation:**
```
VS Code → Extensions → "Claude Code" suchen → Install
```

### Die Basis-Plugins (immer, für jeden Stack)

Diese 3 Plugins installierst du **einmal** — sie funktionieren für alle Projekte:

**1. ESLint** — Coding-Regeln in Echtzeit
→ https://marketplace.visualstudio.com/items?itemName=dbaeumer.vscode-eslint
- Prüft deinen Code automatisch gegen die Regeln in `eslint.config.mjs`
- Zeigt Fehler und Warnungen direkt im Editor (rote/gelbe Unterkringelung)
- **Verbindung zur Governance:** Der `/implement` Skill ruft ESLint nach jeder Änderung
  automatisch auf — Fehler blockieren den Commit (deklarative Iteration bis grün, max 5 Loops)
- **Industriestandard-Regelsatz seit BOO-2 (2026-05-01):** `eslint.config.mjs` enthält
  ESLint Recommended + Airbnb Base + `eslint-plugin-security` + `eslint-plugin-sonarjs`
  (alles MIT-Lizenz, keine Cloud-Services). Python-Pendant: Ruff `select` mit `S`
  (flake8-bandit) + `B` (bugbear) + `C4` (comprehensions). Templates siehe
  `bootstrap/references/file-templates.md`.

**2. SonarQube for IDE (SonarLint)** — Tiefenanalyse
→ https://marketplace.visualstudio.com/items?itemName=SonarSource.sonarlint-vscode
- Analysiert tiefergehende Muster: Code Smells, potenzielle Bugs, Security Vulnerabilities
- Arbeitet passiv im Hintergrund — kein manuelles Starten
- Findet was ESLint nicht findet — SQL Injection, hardcoded Credentials, unsichere Crypto-Nutzung
- **Connected Mode (nach BOO-5 SonarQube Cloud Setup):** VS Code → SonarLint → Connected Mode → SonarCloud → Organisation + Projekt-Key eintragen → Cloud-Findings erscheinen direkt im Editor. `tools_available.sonarqube_ide_plugin: true` in `.claude/environment.json` setzen sobald eingerichtet.

**3. Error Lens** — Kein Verstecken mehr
→ https://marketplace.visualstudio.com/items?itemName=usernamehw.errorlens
- Zeigt ESLint- und SonarLint-Findings **direkt in der Zeile** — nicht erst beim Hover
- Rote Zeile = Fehler. Gelbe Zeile = Warnung. Sofort sichtbar, nicht ignorierbar.

### Global vs. pro Projekt

Diese Regel gilt beim Bootstrap eines neuen Projekts:

| Ebene | Wie oft einrichten? | Beispiele | Warum |
|---|---:|---|---|
| **VS Code / Workstation** | Einmal pro Rechner | Claude-Code-/Codex-Extension, ESLint-Plugin, SonarQube for IDE, Error Lens, Python/Ruff-Extensions | Editor-Faehigkeiten gelten fuer alle Projekte. Bootstrap prueft nur, ob sie verfuegbar sind, und dokumentiert das im Projekt. |
| **Globale Skill-Quelle** | Einmal pro Operator, dann bewusst aktualisieren | `~/.claude/skills/bootstrap/`, optional `~/.codex/skills/` | Quelle oder Registry fuer neue Projekte und Updates, aber nicht die einzige Runtime-Kopie. |
| **Projekt-Governance** | Einmal pro Projekt | `CLAUDE.md`, `AGENTS.md`, `.claude/environment.json`, `GOVERNANCE.md`, `ARCHITECTURE_DESIGN.md`, `specs/`, `intents/`, `journal/`, `pitch/` | Das ist Projektgedaechtnis und Audit-Trail. Es muss mit dem Repository reisen. |
| **Projekt-lokale Skill-Kopien** | Einmal pro Projekt, danach bewusst pinnen/aktualisieren | `.claude/skills/<skill>/`, optional `.codex/skills/<skill>/` | Jedes Projekt behaelt exakt den Skill-Stand, mit dem es gebootstrapped wurde. Alte Projekte aendern sich nicht still, nur weil die globale Skill-Quelle neuer ist. |

Der Sketch zeigt die Trennung: Die Workstation stellt gemeinsame Faehigkeiten bereit, `/bootstrap` uebersetzt die Auswahl in einen Projektvertrag, und das Repository traegt den reproduzierbaren Zustand.

![Bootstrap-Tree — globales Setup vs Projektvertrag](docs/bootstrap-project-tree.png)

*Globales Setup bleibt global; Projektvertrag und lokale Skill-Kopien reisen mit dem Repository. ([Excalidraw-Quelle](docs/bootstrap-project-tree.excalidraw))*

```mermaid
flowchart LR
  subgraph W["Workstation / VS Code (einmal installieren)"]
    V["VS Code Plugins\nESLint · SonarQube for IDE · Error Lens"]
    G["Globale Skill-Quelle\n~/.claude/skills/bootstrap"]
  end

  subgraph P1["Projekt A"]
    A1["Governance-Dateien\nCLAUDE.md · GOVERNANCE.md · specs/"]
    A2["Projekt-lokale Skills\n.claude/skills/*"]
  end

  subgraph P2["Projekt B"]
    B1["Governance-Dateien\nCLAUDE.md · GOVERNANCE.md · specs/"]
    B2["Projekt-lokale Skills\n.claude/skills/*"]
  end

  V -. "fuer alle Projekte verfuegbar" .-> P1
  V -. "fuer alle Projekte verfuegbar" .-> P2
  G -->|"Bootstrap kopiert gewaehlte Skills"| A2
  G -->|"Bootstrap kopiert gewaehlte Skills"| B2
  A2 --> A1
  B2 --> B1
```

Also: Bei einem zweiten Projekt musst du die VS-Code-Plugins nicht nochmal installieren. Die ausgewaehlten Skills werden aber erneut in `.claude/skills/` dieses Projekts kopiert. Das ist Absicht, damit das Projekt reproduzierbar bleibt und nicht unbemerkt von globalen Skill-Updates abhaengt.

### Stack-spezifische Plugins

Abhängig davon was du entwickelst, kommen diese dazu:

**Node.js / JavaScript Backend:**

→ REST Client (API-Endpunkte direkt aus VS Code testen)
  https://marketplace.visualstudio.com/items?itemName=humao.rest-client

**Frontend (React, Vue, Vanilla JS):**

→ Prettier — automatisches Formatieren beim Speichern
  https://marketplace.visualstudio.com/items?itemName=esbenp.prettier-vscode

→ Auto Rename Tag — HTML-Tags automatisch umbenennen
  https://marketplace.visualstudio.com/items?itemName=formulahendry.auto-rename-tag

→ CSS Peek — CSS-Klassen direkt aus HTML anspringen
  https://marketplace.visualstudio.com/items?itemName=pranaygp.vscode-css-peek

**Full-Stack:**

→ Prettier — automatisches Formatieren beim Speichern
  https://marketplace.visualstudio.com/items?itemName=esbenp.prettier-vscode

**Python:**

→ Python (Pflicht — Grundlage für alles)
  https://marketplace.visualstudio.com/items?itemName=ms-python.python

→ Black Formatter — automatisches Formatieren
  https://marketplace.visualstudio.com/items?itemName=ms-python.black-formatter

→ Ruff — Linter (moderner Ersatz für Flake8)
  https://marketplace.visualstudio.com/items?itemName=charliermarsh.ruff

→ Error Lens
  https://marketplace.visualstudio.com/items?itemName=usernamehw.errorlens

→ SonarLint
  https://marketplace.visualstudio.com/items?itemName=SonarSource.sonarlint-vscode

→ Pylance — bessere Autovervollständigung (optional)
  https://marketplace.visualstudio.com/items?itemName=ms-python.vscode-pylance

→ Jupyter — für Data Science / ML Notebooks (optional)
  https://marketplace.visualstudio.com/items?itemName=ms-toolsai.jupyter

> **Tipp:** Bootstrap gibt dir am Ende des Setups automatisch die passenden Links
> für deinen Stack aus — einfach klicken und installieren. Kein Suchen nötig.

**Das Zusammenspiel:**
```
Du tippst Code
  → Error Lens zeigt ESLint + SonarLint Findings inline (sofort)
  → Du fixst während du schreibst

/implement wird ausgeführt
  → ESLint CLI läuft automatisch: npx eslint --max-warnings=0
  → 0 Errors = Gate bestanden → weiter
  → Errors vorhanden = Gate blockiert → erst fixen
```

**Die Regeldatei: `eslint.config.mjs`**

Der Bootstrap legt diese Datei **automatisch im Projekt-Root an** — du musst nichts manuell tun.
Das VS Code ESLint Plugin erkennt sie beim Öffnen des Projekts sofort und aktiviert alle Regeln.

Sie enthält:
- Fehler-Prävention: `no-undef`, `no-unreachable`, `use-isnan`
- Security-Regeln: `no-eval`, `no-implied-eval`, `no-new-func`
- Qualitäts-Regeln: `eqeqeq`, `no-unused-vars`, `prefer-const`
- Async-Regeln: `no-async-promise-executor`, `no-await-in-loop`
- Lesbarkeit: `max-len` (120 Zeichen), `max-depth` (5 Ebenen)

Anpassen: Öffne `eslint.config.mjs` im Projekt-Root und füge/entferne Regeln nach Bedarf.

### ESLint bei einem neuen Projekt

**Szenario:** Du startest ein neues Projekt in Claude Code — die `eslint.config.mjs` fehlt noch.

**Mit Bootstrap (empfohlen):**
```
/bootstrap
```
Bootstrap erstellt die `eslint.config.mjs` automatisch in Phase 1 — du musst nichts weiter tun.
Danach erkennt das VS Code ESLint Plugin sie sofort.

**Ohne Bootstrap (manuell):**
1. Kopiere die `eslint.config.mjs` aus einem bestehenden Projekt in den Root des neuen Projekts
2. Alle Regeln sind generisch — keine Anpassung nötig für Node.js Projekte
3. VS Code ESLint Plugin aktiviert sich automatisch beim nächsten Öffnen der Datei

**Wo liegt die Datei?**
```
mein-projekt/           ← Projekt-Root (wo du claude startest)
├── eslint.config.mjs   ← HIER — direkt im Root, nicht in einem Unterordner
├── lib/
├── agents/
└── ...
```

> **Wichtig:** ESLint v9+ verwendet das neue Format (`eslint.config.mjs`). Das alte Format
> (`.eslintrc.js`) ist veraltet. Bootstrap erstellt immer das neue Format.

### Empfohlene VS Code Settings für Governance

Erstelle `.vscode/settings.json` in deinem Projekt:

```json
{
  // Auto-Formatierung beim Speichern
  "editor.formatOnSave": true,

  // Git-Blame in Statuszeile anzeigen (GitLens)
  "gitlens.statusBar.enabled": true,
  "gitlens.currentLine.enabled": true,

  // Trailing Whitespace entfernen
  "files.trimTrailingWhitespace": true,

  // Finale Newline hinzufügen
  "files.insertFinalNewline": true,

  // Terminal: Projektverzeichnis als Standard
  "terminal.integrated.cwd": "${workspaceFolder}",

  // Dateien die ignoriert werden sollen
  "files.exclude": {
    "**/.git": true,
    "**/node_modules": true,
    "**/.env": true
  },

  // .env Dateien NIEMALS in Source Control
  "git.ignoredRepositories": [],
  "dotenv.enableAutocloaking": true
}
```

### Empfohlene VS Code Coding Rules (`.editorconfig`)

Erstelle `.editorconfig` im Projektroot:

```ini
# EditorConfig hilft Entwicklern konsistenten Code zu schreiben
# https://editorconfig.org
root = true

[*]
indent_style = space
indent_size = 2
end_of_line = lf
charset = utf-8
trim_trailing_whitespace = true
insert_final_newline = true

[*.md]
trim_trailing_whitespace = false

[Makefile]
indent_style = tab
```

Diese Datei wird **automatisch von VS Code respektiert** (kein Plugin nötig) und stellt sicher
dass Code-Formatierung konsistent ist — egal wer am Projekt arbeitet.

---

## 10. Governance für dein Projekt anpassen

### Der Projekt-Vertrag: `CONVENTIONS.md`

`CONVENTIONS.md` ist der projektlokale Vertrag zwischen Operator, KI-Tool und Repository. Die Datei wird von `/bootstrap` einmal pro Projekt angelegt und danach von den nachgelagerten Skills gelesen. Sie installiert die Skills **nicht** jedes Mal neu; sie sagt den bereits projektlokal kopierten Skills, wie streng dieses Projekt arbeiten soll.

Die `code-crash-framework/CONVENTIONS.md` im Framework ist die Spezifikation. Die `CONVENTIONS.md` im Projekt ist die Anpassung fuer ein konkretes Repository: gewaehlter Modus, gewaehlte Isolation und aktive Gates.

Codex-ready gelesen ist das Framework keine Blackbox und kein vollautonomer Developer-Agent,
sondern eine sequenzielle Engineering-Pipeline mit Quality-Gates. Jede Story laeuft durch eine
kontrollierte Kette aus Intent, Backlog-Record, Spec, Implementierung, lokalen Checks,
Remote-Checks, Review und Ergebnis-Dokumentation. Subagents sind darin spezialisierte
Ausfuehrungshelfer mit begrenztem Auftrag und Write-Scope; sie ersetzen nicht den Story-Vertrag
und duerfen Quality-Gates nicht umgehen. Codex, Claude, Cursor oder lokale LLMs sind Adapter auf
diesen Vertrag, nicht die Governance selbst.

| Frage | Antwort in `CONVENTIONS.md` |
|---|---|
| Wie viel Governance braucht dieses Projekt? | `governance_mode` |
| Duerfen Subagents parallel arbeiten? | `execution_isolation` |
| Brauchen wir Git Worktrees? | `git-worktree` in der Isolation-Strategie |
| Welche Gates sind aktiv? | Gate-Tabelle |
| Ist das Framework selbst autonom? | nein: es ist eine sequenzielle Engineering-Pipeline mit Quality-Gates |

### Backlog-Record und Tool-Adapter

Das Framework spricht absichtlich von einem **Backlog-Record**, nicht zwingend von einem
Linear-Issue. Ein Backlog-Record ist der neutrale Story-Vertrag: ID/Prefix, Intent, Kontext,
Akzeptanzkriterien, Definition of Done, `execution_mode`, `execution_isolation`, `write_scopes`,
Risiken und Referenzen auf Specs oder ADRs. Linear ist der empfohlene Adapter, weil Workflow,
Labels, GitHub-Integration und API gut passen. GitHub Issues, Microsoft Planner oder ein
Markdown-Backlog koennen denselben Record aber ebenfalls tragen, solange die Pflichtfelder und
Gates erhalten bleiben.

Die Adapter-Regel lautet: Das Tool darf anders aussehen, der Record nicht. Wenn ein Adapter ein
Feld nicht nativ kennt, wird es im Body, Frontmatter oder einer verlinkten Spec abgelegt. Skills
lesen zuerst den neutralen Record und uebersetzen erst danach in Linear-, GitHub- oder
Markdown-spezifische Aktionen. Deshalb ist "kein Linear" kein Framework-Bruch; "kein
Backlog-Record" ist einer.

### Governance-Modi: lite, standard, heavy

`/bootstrap` fragt diesen Modus im Setup in Block A.5 ab. Wenn im Gespraech von "Light-Modus" die Rede ist, ist technisch der Wert `lite` gemeint.

Begriffe: Der technische Konfigurationswert heisst `lite`; gemeint ist im Alltag "Light Governance". `none` ist kein Governance-Modus. `none` gehoert zur Execution-Isolation und bedeutet: keine besondere Isolation fuer parallele Agentenarbeit.

| Modus | Geeignet fuer | Typische Pruefungen |
|---|---|---|
| `lite` | Lernprojekte, Wegwerf-Skripte, fruehe Experimente | `CLAUDE.md`/`AGENTS.md`, `CONVENTIONS.md`, Specs, Basis-Lint/Test |
| `standard` | normale Produktentwicklung | Spec-Gate, Issue-Quality-Gate, Architektur-/Security-Basischeck, Lint/Test, Sprint Review |
| `heavy` | Produktion, regulierte oder sicherheitskritische Arbeit | alle Standard-Gates plus erweiterte Security, Compliance, Architektur-Nachweise, strengere Reports |

Der Modus ist kein Reifegrad-Abzeichen, sondern eine Kostenentscheidung. Zu wenig Governance macht KI-Coding bruechig; zu viel Governance bremst ein kleines Experiment. `/bootstrap` schlaegt `standard` als Default vor, weil das die sinnvolle Mitte ist: genug Sicherheit fuer echte Projekte, noch keine Enterprise-Zeremonie.

### Was wird weggelassen?

| Bereich | `lite` | `standard` | `heavy` |
|---|---|---|---|
| Kernkontext | enthalten: `CLAUDE.md`/`AGENTS.md`, `CONVENTIONS.md`, `GOVERNANCE.md`, `specs/`, einfache `README`/Index-Dateien | enthalten | enthalten |
| Skills | minimal: `/bootstrap`, `/ideation`, `/implement`; Reviews koennen installiert sein, sind aber keine schweren Gates | normales Set: `/ideation`, `/implement`, `/architecture-review`, `/sprint-review`, `/pitch` | normales Set plus strengere Nutzung von `/security-architect`, tieferen Reviews und Audit-Routinen |
| Issue-/Spec-Disziplin | Spec erforderlich, kleines Template reicht | volles Issue-Quality-Gate + Spec-Gate | volles Issue-Quality-Gate + staerkere Evidenz und Review-Notizen |
| Security | Basis-Hygiene fuer Secrets und Dependencies | SAST/Lint/Security-Basis, Sensitive Paths | Mandatory Security Review fuer sensible Bereiche, staerkerer Audit-Trail |
| Tests/Linting | nur Basis-Lint/Test; Coverage kann Hinweis sein | Lint/Test verpflichtend; Coverage empfohlen oder aktiv wenn konfiguriert | Coverage-Gate aktiv, Regressionspruefungen erwartet |
| Architektur-Doku | leichte Architektur-Notiz reicht | `ARCHITECTURE_DESIGN.md`, ADRs und Review-Kadenz | Architektur-Evidenz, ADR-Vollstaendigkeit und Review-Nachweise erwartet |
| CI/CD | optional; lokale Gates reichen fuer kleine Wochenendprojekte | CI-Lint/SAST empfohlen/default wenn GitHub existiert | Branch Protection, Required Status Checks, CI-Reports |
| Performance/Observability | normalerweise weggelassen, ausser das Projekt braucht es | Basis-Observability und Performance-Doku wenn relevant | Performance-Budgets, SLOs, Observability und Reports erwartet |
| Learning Loop | optional oder L1-Notizen | L1 default, L2 optional | L2/L3 fuer langlebige Systeme erwartet |
| Worktrees | nicht erforderlich; Default-Isolation `none` | Write-Scopes fuer Subagents | `git-worktree` Pflicht fuer agentische/parallele Spuren |

Anders gesagt: `lite` ist der Modus fuer "ich will am Wochenende schnell etwas bauen". Er behaelt die Wirbelsaeule des Frameworks: Kontext, Konvention, Spec, Basis-Gates. Er laesst bewusst die teuren Teile weg: schwere CI, SonarQube, Branch Protection, Performance-Baselines, Audit-Trails und verpflichtende Deep Reviews. Alles davon kann spaeter nachgezogen werden, ohne das Framework zu wechseln.

Was `lite` **nicht** weglassen darf: einen lesbaren Projektvertrag, einen Backlog-Record oder
eine Spec pro nicht-trivialer Aenderung, Secrets-Hygiene, lokale Checks passend zum Stack und eine
kurze Ergebnis-Dokumentation. `standard` laesst keine Kern-Gates weg, sondern macht sie
produktfaehig: Issue-Qualitaet, Architektur-/Security-Baseline, CI und Sprint-Review werden zum
Normalfall. `heavy` laesst ebenfalls nichts weg; es fuegt Nachweislast hinzu: Audit-Trail,
Pflicht-Reviews, Coverage-/Performance-Gates, Branch Protection und Compliance-Evidenz.

Kurzform:

| Modus | Wird bewusst weggelassen | Wird nicht weggelassen |
|---|---|---|
| `lite` | schwere CI, SonarQube, Branch Protection, Performance-Baselines, Audit-Trails, verpflichtende Deep Reviews | Projektvertrag, Backlog-Record, Spec, Secrets-Hygiene, lokale Basis-Gates, Ergebnisnotiz |
| `standard` | regulatorische Nachweislast, verpflichtende Worktrees, volle Audit-Routinen, L2/L3-Learning als Pflicht | Issue-/Spec-Gates, Security-Basis, Lint/Test, CI wo vorhanden, Sprint-Review |
| `heavy` | nichts aus `standard`; nur bewusst irrelevante Add-ons werden nicht aktiviert | alle Standard-Gates plus Review-, Audit-, Security-, Compliance- und Produktionsnachweise |

![Governance-Modi — Lite Standard Heavy](docs/governance-modes.png)

*Gleiches Framework, anderes Reibungsbudget. Lite behaelt die Wirbelsaeule, Standard ergaenzt produktfaehige Gates, Heavy ergaenzt Produktions- und Audit-Nachweise. ([Excalidraw-Quelle](docs/governance-modes.excalidraw))*

### Execution-Isolation und Worktrees

`execution_isolation` entscheidet, wie parallele KI-Arbeit das Repository bearbeiten darf.

| Strategie | Bedeutung | Erlaubte Ausfuehrungsmodi |
|---|---|---|
| `none` | ein Operator oder eine KI-Spur arbeitet im aktuellen Worktree | `linear` |
| `write-scope` | Subagents duerfen arbeiten, aber jeder bekommt explizit erlaubte Pfade | `linear`, `sub-agents` |
| `git-worktree` | jede parallele Spur bekommt eigenen Git-Worktree und Branch | `linear`, `sub-agents`, `agentic` |

Hier werden Worktrees im Framework verankert. Sie sind nicht fuer jede Story noetig. Sie werden Pflicht, wenn das Framework agentisch genutzt wird: ein Developer-Agent bekommt Backlog/Kontext und laesst mehrere Spuren parallel arbeiten. Fuer normale sequenzielle Arbeit reichen Spec-Gate und Write-Scopes. Fuer echte agentische Ausfuehrung verhindern Worktrees, dass parallele Agenten sich gegenseitig ueberschreiben, und geben dem Integration Owner einen sauberen Merge-Punkt.

Codex-Hinweis: Codex darf die Story trotzdem intern in Plan, Taskliste und Sandbox-Schritte
zerlegen. Das ist kein Governance-Verstoss. Die Grenze liegt beim Schreibverhalten: `linear`
bedeutet eine sequenzielle Schreibspur, `sub-agents` bedeutet begrenzte Helfer-Spuren, und
`agentic` bedeutet isolierte Worktree-Spuren. Subagents sind keine Freifahrtscheine fuer
vollautonome Entwicklung; sie bekommen Rolle, Kontext, konkrete Aufgabe, erlaubte Dateien und
Rueckgabeformat. Das optionale Story-Feld `codex_execution_hint` kann `single-agent`,
`parallel-workers` oder `worktree-required` empfehlen, ueberschreibt aber niemals
`execution_mode`, `execution_isolation`, `write_scopes` oder die Gates.

![Execution-Isolation — none write-scope git-worktree](docs/execution-isolation-worktrees.png)

*Execution-Isolation uebersetzt Story-Autonomie in technische Trennung: eine Spur, begrenzte Subagents oder getrennte Worktrees. ([Excalidraw-Quelle](docs/execution-isolation-worktrees.excalidraw))*

### Welcher Skill nutzt welche Konvention?

| Skill | Rolle |
|---|---|
| `/bootstrap` | erstellt die projektlokale `CONVENTIONS.md` und schreibt Default-Modus/-Isolation in `.claude/environment.json` |
| `/ideation` | leitet `execution_mode`, `worktree_strategy` und `write_scopes` fuer die Story ab |
| `/implement` | stoppt hart, wenn `execution_mode` und Isolation-Strategie nicht zusammenpassen |
| `/architecture-review` | prueft, ob parallele Ausfuehrung architektonisch sicher ist |
| `/sprint-review` | erkennt Governance-Drift: Projekt sagt das eine, Team praktiziert etwas anderes |
| Tool-Adapter (Codex, Cursor, Aider, lokale LLMs) | lesen denselben Vertrag und uebersetzen ihn in ihr eigenes Ausfuehrungsmodell |

### Sketch-Status

Die neuen Konventionen haben jetzt dedizierte OWLIST-Sketches fuer Governance-Modi, Execution-Isolation, Projektstruktur, Runtime-Adapter, Validierungsschleifen, Provider-Checks und Upgrade-Pfade:

| Sketch | Status | Dateien |
|---|---|---|
| Governance-Modi | erledigt | `docs/governance-modes.png` / `docs/governance-modes.excalidraw` |
| Execution-Isolation | erledigt | `docs/execution-isolation-worktrees.png` / `docs/execution-isolation-worktrees.excalidraw` |
| Bootstrap-Tree | erledigt | `docs/bootstrap-project-tree.png` / `docs/bootstrap-project-tree.excalidraw` |
| Codex-Artefakte-Landkarte | erledigt | `docs/artifact-map-codex.excalidraw` |
| Cross-Tool-Artefakte-Landkarte | erledigt | `docs/artifact-map-cross-tool.excalidraw` |
| Runtime-Entscheidungsbaum | erledigt | `docs/runtime-decision-tree.excalidraw` |
| Backlog-Record/Adapter-Modell | erledigt | `docs/backlog-record-adapter-model.excalidraw` |
| Validate-Fix-Learn-Schleife | erledigt | `docs/validate-fix-learn.excalidraw` |
| Provider-Postflight-Matrix | erledigt | `docs/provider-postflight-matrix.excalidraw` |
| Upgrade-Pfad bestehender Projekte | erledigt | `docs/upgrade-path-existing-projects.excalidraw` |
| Project-Documentation-SSoT | erledigt | `docs/project-documentation-ssot.excalidraw` |
| Foreign-Developer-Onboarding-Flow | erledigt | `docs/foreign-developer-onboarding-flow.excalidraw` |
| Quality-Gate-Layer aktualisieren | offen | Governance-Intensitaet ergaenzen |

### Provider-Postflight und Upgrade

Bootstrap behandelt Provider-Bereitschaft als eigene Postflight-Dimension. Eine lokale Skill-Kopie reicht nicht fuer `OK`: GitHub, Backlog-Adapter, Research, Visualize/Miro, Monitoring und Obsidian bekommen jeweils `OK`, `WARN`, `SKIP` oder `FAIL` mit naechster Aktion. Der operative Vertrag steht in `bootstrap/references/provider-postflight.md`.

Bestehende Projekte nutzen den Upgrade-Pfad in `bootstrap/references/framework-upgrade.md`: `inspect`, `apply-safe`, `apply-with-confirmation`. Der Upgrade-Report kann unter `journal/reports/framework-upgrade/YYYY-MM-DD.md` abgelegt werden und nutzt die Release Notes aus `docs/releases/` als Migrationsinput.

### Die zentrale Konfigurations-Datei: `lib/config.js`

Alles läuft über eine einzige Datei — das ist der **Single Source of Truth (SSoT)** Prinzip.

```javascript
// lib/config.js — Beispiel-Struktur nach Bootstrap

module.exports = {
  // Projekt-Identität
  PROJECT_NAME: 'MeinShop',
  VERSION: '1.0.0',           // ← Diese Zahl steuert ALLE Versions-Nummern

  // Linear Integration
  LINEAR_TEAM: 'MeinShop',
  LINEAR_PREFIX: 'SHOP',

  // Dokumentationsdateien (werden automatisch auf VERSION geprüft)
  DOC_FILES: [
    { path: 'SYSTEM_ARCHITECTURE.md', versionPattern: /\*\*Version:\*\*\s*([\d.]+)/ },
    { path: 'CHANGELOG.md', versionPattern: /## v([\d.]+)/ },
    // weitere Docs...
  ],

  // Deine eigenen Konfigurationen
  APP: {
    port: 3000,
    environment: 'development',
  }
};
```

**Wichtigste Regel:** Wenn du `VERSION` erhöhst, müssen alle `DOC_FILES` auf die neue Version
aktualisiert werden. Der Doc-Version-Sync Hook erzwingt das automatisch.

### CLAUDE.md anpassen — Claude kennenlernen

Die `CLAUDE.md` ist der Kern. Hier sagst du Claude wer er/sie ist:

```markdown
# Mein Projekt — Context File

## Wer bist du?

Du bist der Lead-Entwickler für MeinShop — einen E-Commerce für handgemachte Produkte.
[Beschreibe dein Projekt in 3-5 Sätzen]

## Deine Aufgabe

1. [Hauptaufgabe 1]
2. [Hauptaufgabe 2]
3. Dokumentation immer aktuell halten

## Das System

[Beschreibe die Architektur in groben Zügen]

## Regeln

- NIEMALS Code ändern ohne Backlog-Record oder Adapter-Story
- NIEMALS Spec-File vergessen
- [Deine eigenen Regeln]
```

**Je besser du das befüllst, desto besser kennt Claude dein Projekt.**

### Issue-Prefix anpassen

Der Bootstrap erstellt alles mit deinem gewählten Prefix. Beispiele:

- E-Commerce Shop: `SHOP-`
- Mobile App: `APP-`
- API Service: `API-`
- Marketing Tool: `MKT-`

### Eigene Skills erstellen

Mit dem `/skill-creator` Skill kannst du eigene, projektspezifische Workflows erstellen:

```
/skill-creator

"Ich möchte einen Skill der täglich automatisch
 unsere Produktpreise mit der Konkurrenz vergleicht
 und einen Report erstellt."

→ Claude erstellt /price-monitor Skill mit passendem Workflow
```

---

## 11. Tägliche Nutzung — ein typischer Workflow

![Ein typischer Arbeitstag](docs/daily-workflow.png)

*Morgens · Feature · Bugfix · Wochenabschluss — Skills in Aktion. ([Excalidraw-Quelle](docs/daily-workflow.excalidraw))*

### Morgens: Was steht an?

```bash
# Terminal öffnen, ins Projektverzeichnis
cd ~/mein-projekt
claude

# Überblick verschaffen
/status
/backlog
```

Claude zeigt dir: offene Issues, System-Gesundheit, was zuletzt passiert ist.

### Feature entwickeln

```
Schritt 1 — Idee formalisieren:
/ideation
→ "Ich möchte X bauen weil..."
→ Claude erstellt SHOP-XX in Linear

Schritt 2 — Implementieren:
/implement SHOP-XX
→ Claude zeigt Plan → Du bestätigst → Code wird geschrieben
→ Automatisch: Tests, Git Push, Backlog-Record/Adapter-Story geschlossen

Schritt 3 — Prüfen:
/integration-test
→ Alle Checks grün? Gut. Rotes Kreuz? Claude erklärt was zu tun ist.
```

### Bug aufgetaucht?

```
/breakfix
→ Problem beschreiben
→ Claude diagnostiziert
→ Fix implementieren
→ Incident dokumentiert
→ Präventivmaßnahme installiert
```

### Ende der Woche

```
/sprint-review
→ Was haben wir diese Woche gemacht?
→ Was ist Tech Debt?
→ Prioritäten für nächste Woche
```

### Beispiel: Ein vollständiger Tag

```
09:00  /status          → Alles grün, 3 offene Issues
09:05  /backlog         → SHOP-38 hat höchste Prio (Zahlungsfehler)
09:10  /implement SHOP-38
09:12  → Claude zeigt Plan: "Session Token Refresh implementieren"
09:13  → Du: "Ja, los"
09:25  → Code implementiert, getestet, gepusht, Issue geschlossen
09:30  /integration-test → Alle 12 Checks grün
10:00  /ideation        → Neue Idee: Newsletter-System
10:15  → SHOP-55 erstellt in Linear
11:00  /implement SHOP-55
...
17:00  /sprint-review   → Wochenrückblick
```

---

## 12. Häufige Fragen

Für konkrete Praxisfragen, die kurz bleiben und laufend erweitert werden sollen, gibt es zusätzlich das lebende Q&A-Dokument: [`docs/qa.md`](docs/qa.md).

### "Ich bin kein Entwickler. Funktioniert das trotzdem für mich?"

Ja. Die Skills sind bewusst so designed dass du kein tiefes technisches Wissen brauchst.
Du beschreibst was du willst in normaler Sprache — Claude übernimmt die technische Umsetzung.
Die Governance sorgt dafür dass dabei trotzdem strukturiert und sicher vorgegangen wird.

### "Was wenn ich einen Fehler mache und etwas kaputt geht?"

Dafür gibt es `/breakfix`. Und weil jede Änderung in Git ist, kann jeder Schritt rückgängig
gemacht werden:

```bash
# Letzte Änderung rückgängig machen
git revert HEAD

# Zu einem bestimmten Zeitpunkt zurückgehen
git log --oneline    # → zeigt alle Commits
git checkout <hash>  # → zu diesem Zustand zurück
```

### "Muss ich wirklich für jedes kleine Feature ein Issue anlegen?"

Für winzige Tippfehler: Nein. Für alles was mehr als 10 Minuten Arbeit ist: Ja.

Der Aufwand für ein Issue ist 2 Minuten mit `/ideation`. Der Aufwand für ein undokumentiertes
Feature das in 3 Monaten für Probleme sorgt: Stunden.

### "Kann ich mehrere Projekte haben?"

Ja. Der Bootstrap-Prozess richtet für jedes Projekt eine eigenständige Umgebung ein.
Claude Code merkt anhand des Arbeitsverzeichnisses welches Projekt gerade aktiv ist.

### "Was kostet das?"

| Service | Kosten |
|---------|--------|
| Claude Code CLI | Im Claude Pro Abo enthalten |
| GitHub | Kostenlos |
| Linear | Kostenlos (Hobby Plan) |
| OpenRouter | Pay-as-you-go (~$0.001 pro Anfrage) |
| Telegram Bot | Kostenlos |

Für ein kleines Projekt: **0 bis ~$5/Monat**.

### "Was wenn ich die Governance-Regeln lästig finde?"

Alle Guardrails haben einen `--no-verify` Bypass. Du kannst sie umgehen — aber bewusst.

Das Ziel ist nicht Kontrolle sondern **bewusstes Handeln**. Wenn du weißt "ich umgehe
gerade die Regel weil X" ist das gut. Wenn du aus Versehen Regeln brichst ohne es zu
merken — das ist das Problem das Governance verhindert.

### "Was ist das Claude Agent SDK — muss ich migrieren?"

Das **Claude Agent SDK** (`@anthropic-ai/claude-agent-sdk`) ist das umbenannte Nachfolger-Paket
von `@anthropic-ai/claude-code` (npm) bzw. `claude-code-sdk` (pip). Es ist ein Rebranding mit
einigen Breaking Changes in v0.1.0.

**Wichtig: Für wen ist die Migration relevant?**

| Anwendungsfall | Migration nötig? |
|----------------|-----------------|
| Claude Code als **CLI-Tool** nutzen (`claude` im Terminal, Skills, Hooks) | **Nein** — nichts zu tun |
| Claude Code als **Bibliothek** in eigenem Code importieren (`import { query } from "@anthropic-ai/claude-code"`) | **Ja** — Paket und Imports umbenennen |

**Das Code-Crash Framework und dieses Handbuch nutzen Claude Code ausschließlich als CLI-Tool.**
Wenn du `/bootstrap`, `/implement` oder andere Skills verwendest, bist du **nicht betroffen**.

Nur wenn du eigene Apps baust, die `@anthropic-ai/claude-code` oder `claude-code-sdk`
programmatisch importieren, musst du migrieren:

```bash
# npm
npm uninstall @anthropic-ai/claude-code
npm install @anthropic-ai/claude-agent-sdk

# pip
pip uninstall claude-code-sdk
pip install claude-agent-sdk
```

```typescript
// Vorher
import { query } from "@anthropic-ai/claude-code";
// Nachher
import { query } from "@anthropic-ai/claude-agent-sdk";
```

Drei Breaking Changes in v0.1.0:
- **System-Prompt** wird nicht mehr automatisch mitgeladen (explizit setzen wenn gewünscht)
- **Settings-Quellen** (`~/.claude/settings.json`, `CLAUDE.md`) werden nicht mehr automatisch gelesen
- **Python:** `ClaudeCodeOptions` heißt jetzt `ClaudeAgentOptions`

Migrations-Guide: https://platform.claude.com/docs/en/agent-sdk/migration-guide

---

### "Wie aktualisiere ich die Skills wenn neue Versionen kommen?"

```bash
# Nur Bootstrap aktualisieren (wie beim ersten Mal)
cd /tmp
git clone --filter=blob:none --sparse git@github.com:vibercoder79/claudecodeskills.git ki-skills
cd ki-skills
git sparse-checkout set code-crash-framework/bootstrap
cp -r code-crash-framework/bootstrap /root/.claude/skills/
cd /tmp && rm -rf ki-skills

# In Claude Code: Bootstrap kann dann bestehende Skills updaten
/bootstrap --update
```

### Upgrade-Pfad fuer bestehende Projekte

Bestehende Projekte werden nicht blind ueberschrieben. Ein Framework-Upgrade folgt drei Stufen:

1. **inspect:** aktuellen Projektvertrag lesen (`CONVENTIONS.md`, `CLAUDE.md`/`AGENTS.md`,
   `.claude/environment.json`, Specs, Hooks, Workflows, Backlog-Adapter) und Abweichungen zum
   neuen Framework-Stand als Diff oder Checkliste ausgeben.
2. **apply-safe:** nur additive, idempotente Aenderungen automatisch anwenden, zum Beispiel neue
   optionale Templates, fehlende Dokumentationsabschnitte, neue ignorierte Report-Ordner oder
   Backlog-Felder ohne bestehende Inhalte zu veraendern.
3. **apply-with-confirmation:** alles, was bestehende Regeln, Hooks, CI, Issue-Templates,
   Branch-Protection, Governance-Modus, Adapter-Konfiguration oder Skill-Versionen veraendert,
   braucht explizite Operator-Bestaetigung.

Der Grundsatz ist: Framework-Versionen duerfen ein Projekt haerter oder klarer machen, aber nicht
heimlich umdeuten. Wenn ein bestehendes Projekt bewusst von der neuen Empfehlung abweicht, wird die
Abweichung dokumentiert statt ueberschrieben.

Der operative Ablauf ist in `bootstrap/references/framework-upgrade.md` beschrieben. Vor dem Upgrade
werden die Release Notes in `docs/releases/` gelesen; der Report dokumentiert alte/neue Version,
aktualisierte Skills, neu angelegte Dateien, bewusst nicht ueberschriebene Dateien, manuelle TODOs
und Provider-Postflight.

---

## Anhang A: Checkliste vor dem ersten Bootstrap

```
Vor /bootstrap:

SOFTWARE:
☐ Node.js v18+ installiert (node --version)
☐ Git installiert (git --version)
☐ Claude Code installiert (claude --version)

ACCOUNTS:
☐ Anthropic Account + API Key
☐ GitHub Account + SSH Key eingerichtet (ssh -T git@github.com)
☐ Linear Account + API Key (optional aber empfohlen)

INFORMATIONEN BEREIT:
☐ Projektname (z.B. "MeinShop")
☐ Kurze Projekt-Beschreibung (1-2 Sätze)
☐ Gewünschter Projektpfad
☐ GitHub Repository URL (neues leeres Repo angelegt)
☐ Linear Team Name (falls genutzt)
☐ Gewünschter Issue-Prefix (z.B. "SHOP")

BOOTSTRAP SKILL:
☐ /root/.claude/skills/bootstrap/ vorhanden
☐ SKILL.md in diesem Ordner sichtbar
```

## Anhang B: Wichtige Dateien Spickzettel

| Datei | Zweck | Wann anfassen |
|-------|-------|---------------|
| `CLAUDE.md` | KI-Persönlichkeit & Regeln | Beim Setup, bei großen Änderungen |
| `lib/config.js` | Alle Konfigurationen | Bei Versionsänderungen, neuen Einstellungen |
| `specs/TEMPLATE.md` | Story-Vorlage | Als Vorlage für neue Specs |
| `specs/ISSUE-XX.md` | Spec für eine Story | Vor jeder Implementierung |
| `CHANGELOG.md` | Was hat sich wann geändert | Automatisch durch /implement |
| `API_INVENTORY.md` | Alle externen APIs | Bei jeder neuen API-Integration |
| `.env` | API Keys & Secrets | Initial + bei neuen Keys |
| `journal/` | Alle Logs & Incidents | Nur lesen / durch Tools schreiben |

## Anhang C: Glossar

| Begriff | Bedeutung |
|---------|-----------|
| **SSoT** | Single Source of Truth — eine einzige Quelle für eine Information |
| **Governance** | Regeln und Prozesse die sicherstellen dass ein System gesund bleibt |
| **Spec** | Spec-File — kurzes Dokument das beschreibt was und warum gebaut wird |
| **Backlog-Record** | Tool-neutraler Story-Vertrag mit Intent, ACs, DoD, Modus, Isolation, Write-Scopes und Referenzen |
| **Issue** | Adapter-spezifische Darstellung eines Backlog-Records, oft in Linear oder GitHub Issues |
| **Linear-Adapter** | Empfohlener Backlog-Adapter; speichert und synchronisiert den neutralen Backlog-Record in Linear |
| **Git Hook** | Automatischer Check der bei Git-Befehlen ausgeführt wird |
| **Self-Healing** | System das Probleme selbst erkennt und (wenn möglich) behebt |
| **Daemon** | Ein Prozess der dauerhaft im Hintergrund läuft |
| **Vibe Coding** | KI-gestütztes Entwickeln wo die KI großteils den Code schreibt |
| **Artefakt** | Datei mit definiertem Zweck im Governance-Framework (Doku, Hooks, Specs, Scripts) |

---

## Anhang D: Hermes-Bridge — `metadata.hermes`-Block (BOO-31)

Das Code-Crash Framework ist so gebaut, dass es mit [Hermes](https://hermes-agent.nousresearch.com/) andocken kann — einem Compound-Engineering-Layer der CI-Outputs ueber Projekte hinweg liest, wiederkehrende Patterns erkennt und Patches als PRs vorschlaegt. Hermes ist **optional**: Wenn du Hermes nicht installierst, funktionieren alle Skills wie gewohnt. Wenn du Hermes installierst, sind die Skills schon vorbereitet, sodass Hermes ohne Inferenz zwischen ihnen routen kann.

Jeder Bundle-Skill traegt einen `metadata.hermes`-Block im YAML-Frontmatter. Hermes liest diesen Block beim Scan des Skill-Katalogs und nutzt ihn fuer Routing, Cross-Skill-Memory und Toolset-Dependency-Checks.

### Schema

```yaml
metadata:
  hermes:
    category: <governance | coding | doku | research | trading | personal-assistant>
    tags: [<tag1>, <tag2>, ...]
    requires_toolsets: [<toolset1>, <toolset2>, ...]
    related_skills: [<other-skill>, ...]
```

- **category** — Grobe Einordnung. Hermes nutzt das fuer Top-Level-Routing.
- **tags** — Feingranulare Capability-Tags. Frei waehlbar; Hermes nutzt sie fuer Volltext-Suche.
- **requires_toolsets** — Externe Tools oder MCP-Server die der Skill zur Laufzeit braucht (z.B. `terminal`, `git`, `github`, `linear`, `sonarqube`, `obsidian`, `eslint`, `semgrep`, `grafana-mcp`, `ssh`, `mermaid`).
- **related_skills** — Andere Skills in derselben Workflow-Kette. Hermes nutzt das um Skill-Aufrufe zu verketten oder relevanten Kontext einzublenden.

### Bundle-Skill-Mapping

| Skill | category | tags | requires_toolsets | related_skills |
|---|---|---|---|---|
| `bootstrap` | governance | setup, project-init, governance-config | terminal, git, github, obsidian | (keine — Setup-Skill) |
| `intent` | governance | intent-definition, perceive, anti-pattern-check | terminal, obsidian | ideation, backlog |
| `ideation` | coding | story-writing, spec-writing, intent-gate | terminal, git, linear, obsidian | intent, backlog, implement |
| `backlog` | coding | linear, m365, intent-label, prioritization | linear, github, terminal | ideation, intent |
| `implement` | coding | code-generation, deklarativer-modus, quality-gates | terminal, git, eslint, semgrep | ideation, sprint-review |
| `architecture-review` | governance | review, dimensions, ki-tauglichkeit | terminal, git, sonarqube | sprint-review, ideation |
| `sprint-review` | governance | retro, lessons-loop, anti-pattern-check | terminal, git, sonarqube, linear | implement, architecture-review |
| `cloud-system-engineer` | coding | infra, vps, hostinger | terminal, ssh | bootstrap |
| `grafana` | coding | observability, dashboards | terminal, grafana-mcp | architecture-review, sprint-review |
| `visualize` | doku | diagrams, system-architecture | terminal, mermaid | architecture-review |

### Backward Compatibility

Der `metadata.hermes`-Block ist additiv — claude-skills ohne Hermes ignorieren ihn schlicht (YAML-Parser akzeptiert unbekannte Frontmatter-Keys). Kein Breaking-Change fuer Nicht-Hermes-User.

---

## Anhang E: Reports-Konvention — `journal/reports/` (BOO-32)

Damit Hermes (oder jeder externe Analyser) Tool-Outputs ueber Projekte hinweg lesen kann, folgt jedes Projekt demselben `journal/reports/`-Layout. Zwei Sub-Trees: `local/` fuer `/implement`-Runs (BOO-36), `ci/` fuer GitHub-Actions-Runs (diese Sektion).

### Verzeichnis-Layout

```
journal/
├── learnings.md                    ← L1
├── sprint-{date}.md                ← L2
├── learnings.db                    ← L3
└── reports/
    ├── local/
    │   └── {YYYY-MM-DD_HHMM}_{STORY-ID}/   ← BOO-36
    │       ├── eslint-iter{N}.sarif
    │       ├── tests-final.junit.xml
    │       ├── coverage-final.json
    │       ├── semgrep-final.sarif
    │       └── meta.json
    └── ci/
        └── run-{github-action-id}/          ← BOO-32
            ├── eslint.sarif
            ├── tests.junit.xml
            ├── coverage.lcov
            ├── coverage.json
            ├── semgrep.sarif
            └── sonarqube.json
```

`journal/reports/` ist gitignored — Reports sind kurzlebiges Signal, keine Source-of-Truth. CI-Runs uploaden das ganze `run-{id}/`-Verzeichnis als GitHub-Actions-Artifact (Retention 30 Tage), Local-Runs bleiben auf der Operator-Maschine bis `/sprint-review` sie aggregiert.

### Tool-Mapping

| Tool | Format | Dateiname | Producing-Step |
|---|---|---|---|
| ESLint | SARIF | `eslint.sarif` | `npx eslint . --format @microsoft/eslint-formatter-sarif --output-file ...` |
| Ruff | SARIF | `eslint.sarif` (oder `ruff.sarif`) | `ruff check --output-format sarif --output-file ...` |
| Tests (Vitest / Jest) | JUnit XML | `tests.junit.xml` | Vitest `--reporter=junit`, Jest mit `jest-junit` |
| Tests (pytest) | JUnit XML | `tests.junit.xml` | `pytest --junit-xml=...` |
| Coverage (Vitest / Jest) | LCOV + JSON | `coverage.lcov` + `coverage.json` | eingebauter Coverage-Reporter |
| Semgrep | SARIF | `semgrep.sarif` | `semgrep --sarif --output ...` |
| SonarQube | JSON (Web-API) | `sonarqube.json` | Post-Run-Fetch von der SonarCloud-API |
| Performance-Bench | JSON | `perf.json` (pro Service) | autocannon / pytest-benchmark, siehe BOO-16 |

### Aggregator-Step in jedem CI-Workflow

Jeder Workflow der ein Tool ausfuehrt, endet mit zwei Schritten: Collect-into-`run-{id}/` und Upload-Artifact. Template:

```yaml
- name: Collect reports
  if: always()
  run: |
    mkdir -p journal/reports/ci/run-${{ github.run_id }}
    # tool-spezifischen Output in das Run-Verzeichnis verschieben:
    cp -f .ci-reports/eslint.sarif journal/reports/ci/run-${{ github.run_id }}/ 2>/dev/null || true
    # pro Tool wiederholen, das dieser Workflow erzeugt

- name: Upload reports as artifact
  if: always()
  uses: actions/upload-artifact@v4
  with:
    name: ci-reports-${{ github.run_id }}
    path: journal/reports/ci/run-${{ github.run_id }}/
    retention-days: 30
```

`if: always()` stellt sicher dass Reports auch dann hochgeladen werden, wenn das Gate scheitert — das Failure-Signal ist fuer Pattern-Detection wertvoller als das Success-Signal.

### Hermes-Konsumtion

Die Hermes-Installation enthaelt ein Fetch-Skript (out-of-scope fuer dieses Bundle — siehe Hermes-Doku), das Artifacts ueber die GitHub-API zieht, in `~/.hermes/cache/{project}/run-{id}/` entpackt und an den Pattern-Detector weitergibt. Weil jedes Projekt das gleiche Layout nutzt, braucht Hermes nur einen Parser pro Tool, nicht pro Projekt.

### Migration fuer Bestands-Projekte

Siehe `bootstrap/references/migration-checklist-v1-to-v2.md` §BOO-32 — primaer: Aggregator + upload-artifact-Steps in bestehende Workflows ergaenzen, `journal/reports/ci/` zu `.gitignore` hinzufuegen.

---

## Anhang F: Hermes Compound-Layer Setup (BOO-33)

Hermes ist der optionale Compound-Engineering-Layer der CI-Outputs ueber Projekte hinweg liest (Anhang E), wiederkehrende Patterns ueber viele Sprints erkennt und Patches als PRs vorschlaegt. Hermes ist **nicht Teil des Bundles** — er laeuft auf einer separaten Maschine (VPS oder Workstation), liest den Skill-Katalog via `metadata.hermes` (Anhang D), und das Reports-Layout unter `journal/reports/`.

### 1. VPS-Auswahl

| Option | Vorteile | Nachteile |
|---|---|---|
| **Beifahrer auf bestehendem VPS** (z.B. mit anderem Service geteilt) | guenstig, schneller Start | RAM-Konkurrenz, keine Failure-Isolation |
| **Eigener Hermes-VPS** (Hostinger KVM 4–8 GB, ca. 5–10 EUR/Monat) | saubere Failure-Domain, einfaches Skalieren | eine Rechnung mehr, separate Ops |

Empfehlung: Beifahrer fuer die Pilot-Phase, eigener VPS sobald Hermes mehr als ein Produktiv-Projekt bedient.

### 2. Installation

```bash
# Auf dem VPS (Linux):
curl -fsSL https://raw.githubusercontent.com/NousResearch/hermes-agent/main/scripts/install.sh | bash

# Verifizieren:
hermes --version
```

### 3. Claude Max-Abo Auth (kein Doppelzahlen)

```bash
# Lokal auf dem Mac (Browser noetig):
claude setup-token
# → liefert einen 1-Jahres-OAuth-Token

# Auf dem VPS:
echo "CLAUDE_CODE_OAUTH_TOKEN=<token>" >> ~/.hermes/.env

# WICHTIG: ANTHROPIC_API_KEY NICHT setzen — sonst Pay-per-Token-Billing
```

### 4. Memory-DB-Init

```bash
hermes setup
# Provider: anthropic via OAuth-Token (Max-Abo)
# Memory-Backend: SQLite + FTS5 (Default)
# Honcho User-Modeling: ja
```

### 5. Approval-Gate (PFLICHT)

```bash
hermes config set skill_manage.require_approval true
hermes config set skill_manage.pr_target main
```

Begruendung: ohne Approval-Gate driftet Hermes (Misevolution-Paper). Hard Requirement — nie deaktivieren.

### 6. Cron-Schedule

```bash
# /etc/crontab oder crontab -e auf dem Hermes-VPS:
0 3 * * * cd /home/hermes && hermes run-loop --mode=compound 2>&1 | logger -t hermes
```

3 Uhr nachts: pullt Repos, analysiert Sprint-Outputs, generiert Patches als PRs.

### 7. Health-Check

`scripts/hermes-healthcheck.sh` (Template — auf dem Hermes-VPS implementieren):

```bash
#!/usr/bin/env bash
set -euo pipefail
hermes status               # Daemon laeuft?
[[ -r ~/.hermes/memory.db ]] || { echo "memory DB nicht lesbar"; exit 1; }
hermes auth verify          # OAuth-Token noch gueltig?
cd ~/skills && git pull --ff-only  # Skill-Katalog erreichbar?
echo "OK"
```

Per Cron alle 6 h ausfuehren; bei Non-Zero-Exit alarmieren.

### 8. Troubleshooting

| Symptom | Wahrscheinliche Ursache | Fix |
|---|---|---|
| `rate limit` | Max-Abo-5h-Fenster ausgeschoepft | warten oder in kleinere Runs splitten |
| `skill not found` | `metadata.hermes`-Frontmatter fehlt | `git pull` im Skills-Repo (siehe BOO-31) |
| `no patterns` | CI-Reports-Pfad falsch | `journal/reports/ci/`-Layout pruefen (siehe BOO-32 + Anhang E) |
| `OAuth expired` | 1-Jahres-Token abgelaufen | `claude setup-token` auf dem Mac erneut, frischen Token nach `~/.hermes/.env` kopieren |
| `PR not opened` | Approval-Gate blockiert | `hermes config get skill_manage.require_approval` pruefen — sollte `true` sein |

### Verwandte Sektionen

- Anhang D — `metadata.hermes`-Block-Schema (BOO-31)
- Anhang E — `journal/reports/`-Konvention (BOO-32)
- Hermes-Docs: https://hermes-agent.nousresearch.com/docs/

---

## Anhang G: Sprint-Sizing-Mechanik — Token-Window-Basis (BOO-38)

### Warum klassisches Sprint-Sizing tot ist

Klassisches Sprint-Sizing in Stunden oder Tagen funktioniert bei KI-gestuetztem Coding schlecht. Eine Stunde KI-Coding kann null oder 200 Zeilen produzieren — Komplexitaet ist nicht die richtige Achse. Velocity-Tracking macht Story Points zu Fetischen, das Mass frisst seinen Zweck (Schrader, Code Crash Kap. 2 §Velocity-Obsession). Wir brauchen eine modellunabhaengige Sprint-Box, die eine einzige Frage operationalisiert: "Passt das in eine Claude-Session ohne Compaction?"

### Sprint = 80% des Context-Windows

Ein Sprint ist die Arbeit, die in **80% des aktuellen Modell-Context-Windows** ohne Compaction passt. Modellunabhaengig: 80% sind die Regel, egal ob 200k oder 1M Tokens. Bei 80%+ wird der Sprint geschlossen — neuer Chat oder `/clear` + `/compact`.

### Story Points — duale Funktion

| SP | Sprint-Budget-Anteil | Token @ 200k | Typischer Inhalt | Ausfuehrungsmodus |
|---|---|---|---|---|
| 1 | ~5% | ~8k | 1–2 Files, < 50 Zeilen | linear |
| 2 | ~10–15% | ~16–24k | Single-File-Refactor, ~200 Zeilen | linear / sub-agents |
| 3 | ~20–30% | ~32–48k | Feature in 1 Session, mehrere Files + Tests | sub-agents |
| 5 | ~40–60% | ~64–96k | Voll-Window-Story, Browse + Implement + Test + Doku | agentic |
| 8 | mehr als 60% Budget | — | **muss aufgeteilt werden** | — |

Story Points werden dual genutzt:
1. **Token-Schaetzung** — passt die Story ins Sprint-Budget?
2. **Ausfuehrungsmodus-Selektor** — linear (klein, direkt), sub-agents (mittel, fokussierte Delegationen), agentic (gross, parallele Sub-Agents)

### Kein Velocity-Tracking

Keine Velocity-KPI, keine SP-pro-Sprint-Statistik, keine Burndown-Charts. Aus Schraders eigener Argumentation:

> "Story Points und Velocity haben ausgedient. Sie messen, wie viel Arbeit erledigt wird. Wir muessen messen, ob die Arbeit Wirkung hat." (Code Crash Kap. 8 §Intent Metrics Dashboard)

Stattdessen: Outcome-Tracking ueber Intent-Erfuellung (BOO-1 + BOO-10) und Quality-Gate-Compliance (BOO-15/16/17).

### Sub-Agent als Token-Multiplikator

Stories im `agentic`-Modus verbrauchen im Hauptkontext nur Briefing + Reports (~15–20k), nicht die vollen 64–96k. Die Orchestrator-Regel aus CLAUDE.md ist damit nicht nur Methodik, sondern **Token-Mathematik**: ohne Sub-Agent-Delegation sprengen drei grosse Stories das 80%-Budget.

### Schwellen-Konfiguration

In `.claude/environment.json`:

```json
{
  "thresholds": {
    "token_warn_threshold": 70,
    "token_hard_threshold": 80
  }
}
```

Zwei-Stufen-Warnung:
- **70% warn:** Weicher Hinweis — "eine kleine Story passt vielleicht noch rein"
- **80% hard:** Sprint-Ende-Empfehlung; User kann mit bewusster Entscheidung weiter

Pre-Flight-Check in `/implement` Schritt 0b setzt das um (siehe BOO-40).

### Schaetzungs-Quelle: `/ideation`

`/ideation` Schritt 5b laeuft eine Token-Heuristik gegen die Story-Beschreibung und schreibt die Schaetzung ins Spec-Frontmatter:

```yaml
---
story_id: BOO-XX
estimate: 3
token_estimate: 38000
execution_mode: sub-agents
estimation_basis: |
  4 Files (~8k), ~250 Zeilen Diff (~5k), Test-Erweiterung (+30%),
  HANDBUCH-Update (+20%), 2 aehnliche Stories in L3 (Faktor 0.9)
---
```

`estimation_basis` ist Prosa, damit der Operator die Schaetzung pruefen + korrigieren kann. Heuristik-Signale siehe BOO-39.

### L3-Kalibrierung

Nach 5–10 Sprints enthaelt die L3-Learnings-DB tatsaechlichen Token-Verbrauch pro Story. `/ideation` liest das und kalibriert die Heuristik: aehnliche vergangene Stories verschieben den Multiplikator. Selbst-korrigierende Schaetzung ueber die Zeit.

---

## Anhang H: Lighthouse-CI-Integration fuer Frontend-Performance (BOO-45)

Pendant zu BOO-16 Performance-Gate fuer Backend-Services. Fuer Browser-Apps (Frontend oder Full-Stack mit Frontend-Anteil) misst Lighthouse CI echte User-Metriken (LCP, CLS, TBT, Bundle-Size) und erzwingt Budgets — gleiche Idee wie BOO-16s p95-Baseline, andere Signal-Quelle.

### Wann scaffolded das Bundle Lighthouse?

`/bootstrap` Block A.1b stellt die Frage nur, wenn `STACK_CHOICE` = `b` (Frontend) oder `c` (Full-Stack). Fuer reine Backend-Stacks erscheint die Frage nicht — Lighthouse braucht eine Browser-renderbare URL.

### Gescaffoldete Files

1. **`lighthouserc.json`** — Performance-Budgets (LCP <2.5s, CLS <0.1, TBT <300ms, Accessibility ≥0.9, Performance ≥0.9). Template in `bootstrap/references/file-templates.md` §`lighthouserc.json (BOO-45)`.
2. **`.github/workflows/lighthouse.yml`** — laeuft auf jeden Push + PR via `treosh/lighthouse-ci-action@v12`. Baut Frontend, startet Preview-Server, fuehrt Lighthouse aus, schreibt Reports nach `journal/reports/ci/run-{id}/` (BOO-32-Konvention).

### Manuelle Operator-Tasks beim Setup

1. **URL pro Environment** — `ci.collect.url` in `lighthouserc.json`. Default `http://localhost:3000/` ist nur fuer den ersten Smoke-Test. Eigene Preview-Deploy / Staging / Prod-URL eintragen.
2. **Performance-Budgets** — Defaults sind branchenueblich. Bei viel Drittanbieter-Code (Analytics, Ads) verschieben sich Metriken — Operator justiert.
3. **Mobile-Throttling-Profil** — `desktop` (kein Throttling) fuer SaaS/B2B, `mobile` (Default 3G-slow + 4x CPU-Throttle) fuer Consumer-Apps.
4. **Build- und Preview-Server-Command** — in `lighthouse.yml`, `npm run build` und `npx serve -s dist -l 3000` an Stack anpassen (Next.js: `npm run start`; Astro: `npm run preview`; Vite: `npm run preview`).
5. **`LHCI_GITHUB_APP_TOKEN`** (optional) — fuer Lighthouse-CI-Server-Status-Checks. Filesystem-Reports funktionieren ohne.

### Hermes-Konsumtion

Reports landen in `journal/reports/ci/run-{id}/lighthouse.json` (aggregierte Score-Summary) und `journal/reports/ci/lighthouse-out/*.json` (Roh-Reports pro URL). Hermes konsumiert beide via BOO-32-Reports-Konvention.

### Migration fuer Bestands-Frontend-Projekte

Siehe `bootstrap/references/migration-checklist-v1-to-v2.md` §BOO-45. `migrate_boo_45()` prueft `package.json` auf Frontend-Frameworks (React/Vue/Svelte/Astro/Next/Nuxt/Vite/Webpack) und scaffolded die beiden Files wenn anwendbar. Override per `FRONTEND_OVERRIDE=true` fuer Nicht-Standard-Frontend-Setups.

---

## Anhang I: Self-Hosted-Runner-Setup (BOO-46)

Folgeschnitt zu BOO-16. GitHub-Hosted-Runner sind Shared-Hardware mit ±30% Varianz zwischen identischen Bench-Laeufen. Daher BOO-16-Default-Fail-Threshold von 20% — generoes genug um den Noise zu absorbieren. Operatoren die ein schaerferes Signal brauchen, koennen einen Self-Hosted-Runner mit reservierten Ressourcen einsetzen — Varianz faellt auf ~5%, Threshold kann auf 10% geschaerft werden.

### Wann lohnt sich ein Self-Hosted-Runner

- BOO-16-Performance-Gate flackert zwischen PASS und FAIL ohne echte Code-Aenderung (Varianz > 20%)
- Performance-Regressionen sind kritisch fuers Produkt (Latency-sensitive API, Echtzeit-Service)
- Mehrere Projekte teilen sich denselben Runner (Cost-Amortisation)

### Operator-seitiges Setup (manuell)

Das Bundle provisioniert den Runner NICHT — VPS- oder Hardware-Wahl ist Operator-Hoheit. Das Bundle patcht `perf.yml` nur dann, wenn der Runner online ist (via `migrate_boo_46()`).

#### 1. Hardware- / VPS-Wahl

| Option | Vorteile | Nachteile |
|---|---|---|
| **Hostinger VPS-Beifahrer** (z.B. mit anderem Service geteilt) | guenstig, schnell | RAM-Konkurrenz bei anderen heavy Prozessen |
| **Dedizierter VPS** (Hostinger KVM 4–8 GB, ~5–10 EUR/Monat) | saubere Failure-Domain, skalierbar | eine Rechnung mehr |
| **Mac-Mini im Buero** | Hardware-Kontrolle, idle ausserhalb Bueroszeiten | benoetigt Heim-Netzwerk, kein Remote-Provisioning |

Empfehlung: Hostinger-Beifahrer fuer die Pilot-Phase; dedizierter VPS sobald Perf-Gate fuer mehr als ein Produktiv-Projekt laeuft.

#### 2. GitHub-Actions-Runner installieren

```bash
# Settings -> Actions -> Runners -> New self-hosted runner
# Befehle aus dem GitHub-UI kopieren, dann auf dem VPS:
mkdir actions-runner && cd actions-runner
curl -o actions-runner-linux-x64-2.319.1.tar.gz -L \
  https://github.com/actions/runner/releases/download/v2.319.1/actions-runner-linux-x64-2.319.1.tar.gz
tar xzf ./actions-runner-linux-x64-2.319.1.tar.gz

./config.sh --url https://github.com/{owner}/{repo} --token {RUNNER_TOKEN}
# Defaults akzeptieren: Runner-Name + Work-Folder + Labels (Default: 'self-hosted,Linux,X64')
```

#### 3. systemd-Service fuer Auto-Start

```bash
sudo ./svc.sh install
sudo ./svc.sh start
sudo ./svc.sh status
# Auf Boot aktivieren:
sudo systemctl enable actions.runner.{owner}-{repo}.{runner-name}.service
```

#### 4. `perf.yml` patchen

`bash migrate-to-v2.sh --issue BOO-46` im Projekt ausfuehren. Das:
- Ersetzt `runs-on: ubuntu-latest` mit `runs-on: self-hosted` (mit `.boo46-backup`-Backup)
- Ersetzt Threshold `1.20` (20%) mit `1.10` (10%) — schaerferes Signal
- Aktualisiert Kommentare entsprechend

#### 5. Health-Check

`scripts/runner-healthcheck.sh` (operator-side, auf dem Runner-VPS, alle 6h via Cron):

```bash
#!/usr/bin/env bash
set -euo pipefail
gh api "repos/{owner}/{repo}/actions/runners" \
  | jq -e '.runners[] | select(.name == "{runner-name}") | select(.status == "online")' \
  > /dev/null
```

Alert bei Non-Zero-Exit (z.B. Telegram-Bot, E-Mail).

### Wann verzichten

Wenn dein Performance-Gate selten ausloest und der 20%-Threshold reicht — verzichte auf BOO-46. Der Runner ist Operations-Overhead, nicht gratis. Nur diesen Aufwand zahlen wenn das schaerfere Signal es wert ist.

---

## Anhang K: Tool-Adapter — dieses Framework mit anderen KI-Tools nutzen (BOO-49)

Das Code-Crash Framework wurde Claude-Code-first entwickelt, aber die **Methodik ist tool-agnostisch**. Etwa 70% von dem was das Framework definiert sind reine Konventionen (Datei-Layouts, Frontmatter, bash-Hooks, GitHub Actions). Die restlichen 30% — Slash-Commands, Skill-Aufruf, MCP-Integrationen — haengen vom KI-Tool ab. Dieser Anhang zeigt, wie du das Framework mit den gaengigsten Alternativen betreibst.

**Tool-neutrale Spezifikation:** `CONVENTIONS.md` auf Bundle-Top-Level. Lies das immer zuerst, wenn du das Framework mit einem anderen Tool aufnimmst.

### Claude Code (primary, aktueller Standard)

- Skills liegen unter `~/.claude/skills/<name>/SKILL.md`
- Aufruf via Slash-Commands: `/bootstrap`, `/implement`, `/sprint-review`, etc.
- Volle MCP-Integration: Linear, Obsidian, Hostinger, GitHub
- Sub-Agent-Delegation fuer parallele Arbeit (Wave-Logik)
- Eingebauter `/context`-Befehl fuer Token-Window-Messung (BOO-40 Pre-Flight)

Das ist was jede Sektion dieses Handbuchs standardmaessig beschreibt.

### Codex (sekundaer, kompatibel)

OpenAI Codex nutzt dasselbe **SKILL.md-Format** wie Claude Code. Die Methodologie ist uebertragbar; nur der Aufruf unterscheidet sich.

Wichtig: Codex macht aus dem Framework keinen vollautonomen Developer-Agent. Codex ist ein
Adapter, der den neutralen Story-Vertrag liest und in seine eigene Arbeitsweise uebersetzt. Die
Framework-Logik bleibt sequenziell und gate-basiert: Backlog-Record → Spec → kontrollierte
Umsetzung → Checks → Review → Ergebnisnotiz. Subagents oder parallele Worker sind nur
spezialisierte Ausfuehrungshelfer innerhalb dieser Story.

**Setup:**
- Symlink oder Kopie der Skills: `ln -s ~/.claude/skills ~/.codex/skills` (oder einzelne Skills kopieren)
- Codex liest das Frontmatter `name` + `description` automatisch
- `metadata.hermes`-Block funktioniert as-is

**Aufruf:**
- Keine Slash-Commands — nutze `@Codex` im Linear-Issue-Body ODER `codex run-task <prompt>` via CLI
- Async by Default — jeder Task laeuft in einer isolierten Cloud-Sandbox, Ergebnisse kommen als PR zurueck
- Fuer recurring Tasks: `.codex/automations/<name>.toml` (Cron + memory.md, aehnlich wie Self-Healing-Agent)

**Execution-Mapping:**
- Codex darf aus der Linear-Story einen eigenen Plan und Task-Breakdown erstellen; das ist normales Codex-Verhalten.
- Der Story-Vertrag steuert trotzdem das Schreibverhalten: `linear` = eine sequenzielle Spur, `sub-agents` = begrenzte Helfer-Spuren, `agentic` = Worktree-isolierte Spuren.
- Optionaler Hinweis: `codex_execution_hint: single-agent | parallel-workers | worktree-required`.
- Der Hinweis ist nur beratend; harte Gates bleiben `execution_mode`, `execution_isolation`, `worktree_strategy`, `write_scopes`, Tests, Lint, Security und Review-Gates.

**Kontext-Bruecke** (Codex hat kein MCP):
- `CLAUDE.md` (das Framework pflegt es schon) wird von Codex beim Session-Start gelesen — gleiches File, beide Tools
- `specs/{ISSUE-ID}.md` liefert per-Story-Kontext; Codex liest es explizit
- Optional: n8n-Workflow der Obsidian-Daily-Note + Linear-Issue-Body als Codex `system_prompt` exportiert

**Siehe BOO-50** fuer das optionale Codex-Integration-Setup (Phase A: Daily Bug-Scanner).

### Cursor (tertiaer)

Cursor nutzt `.cursorrules` statt Skills. Mapping:

- SKILL.md-Frontmatter `description` → `.cursorrules` "When to use"-Regel
- Skill-Body → `.cursorrules` "Steps"-Anweisung
- Ein `bootstrap/scripts/convert-skill-to-cursorrules.sh`-Script kann bei Bedarf als Folge-Issue ergaenzt werden
- Konventionen (specs/, journal/, hooks/) bleiben unveraendert — Cursor laeuft auf demselben Filesystem

### Aider, OpenCode, lokale LLMs (Ollama mit Qwen2.5-Coder etc.)

- Konventionen sind tool-agnostisch; jedes KI-Tool kann SKILL.md als Doku lesen und die Schritte ausfuehren
- Aider `.aider.conf` kann `CONVENTIONS.md` als System-Prompt referenzieren
- Lokale LLMs via OpenAI-kompatible Endpoints funktionieren identisch
- Das 1M-Token-Context-Window von Claude Code Opus 4.7 ist einzigartig — lokale LLMs haben typischerweise 8-128k, also muessen groessere Skills (`/architecture-review`, `/sprint-review`) ggf. gesplittet werden

### Tool-agnostische Komponenten (laufen unveraendert mit jedem Tool)

Diese haengen nie vom KI-Tool ab:

| Komponente | Pfad | Funktion |
|---|---|---|
| bash-Hooks | `hooks/*.sh` | spec-gate, doc-version-sync, audit-trace, branch-protection, dep-check |
| GitHub Actions | `.github/workflows/*.yml` | ESLint/Ruff, Semgrep, Coverage, Perf, Sonar, Lighthouse |
| `journal/`-Baum | `journal/reports/{ci,local}/`, `journal/learnings.*` | Reports + Learning-Loop |
| Markdown-Artefakte | `CLAUDE.md`, `ARCHITECTURE_DESIGN.md`, `GOVERNANCE.md`, `SECURITY.md`, `specs/TEMPLATE.md` | Projekt-Kontext |
| Konfigurations-Files | `.claude/environment.json`, `.claude/sensitive-paths.json`, `sonar-project.properties`, `lighthouserc.json` | Thresholds + Tool-Registry |
| `metadata.hermes`-Block | Skill-Frontmatter | Hermes-Bridge (Anhang D) |

### Tool-Wechsel ohne Re-Bootstrap

Die Portability-Checkliste in `CONVENTIONS.md` §6 erlaubt dir, das Tool zu wechseln ohne das Framework zu verlieren. Typische Szenarien:

- **Claude-Rate-Limit erreicht → temporaer Codex:** Codex aktivieren (BOO-50), weiterarbeiten auf gleichen `specs/`, `journal/`, Hooks
- **Privacy-getriebener Wechsel → lokales LLM:** alle Konventionen + Hooks unveraendert; nur das Tool das sie aufruft aendert sich
- **Team-Wechsel → Cursor:** `.cursorrules` aus Skills generieren, Konventionen bleiben
- **Langfristig:** das Framework IST die Methodologie, das Tool ist der Ausfuehrer

### Wo du trotzdem von Claude Code profitierst

Trotz Tool-Portabilitaet sind manche Claude-Code-Features schwer zu replizieren:

- 1M-Token-Context-Window (Opus 4.7) — grosse Architektur-Reviews profitieren
- MCP-Server — direkte Linear/Obsidian/Hostinger-Integration
- Eingebaute Sub-Agents (Wave-Logik fuer parallele Arbeit)
- `/context`-Token-Messung (BOO-40 Pre-Flight hat saubere Claude-Integration)

Fuer die strategischen Skills (`/bootstrap`, `/intent`, `/ideation`, `/architecture-review`, `/sprint-review`) bleibt Claude Code das empfohlene Tool. Codex / andere sind sinnvoll fuer Execution-heavy / async Tasks.

### Verwandte Sektionen

- Anhang D — `metadata.hermes`-Block-Schema (BOO-31)
- Anhang E — `journal/reports/`-Konvention (BOO-32)
- Anhang J (geplant) — Codex-Integration-Setup (BOO-50)
- `CONVENTIONS.md` auf Bundle-Top-Level — vollstaendige tool-neutrale Spezifikation

---

## Anhang L: 4P-Pipeline-Mapping — Pitch als geschlossene Phase (BOO-37)

Schraders Code Crash Kap. 5 definiert eine vier-phasige Delivery-Pipeline: **Perceive → Prompt → Produce → Pitch**. Bis BOO-37 deckte das Bundle nur die ersten drei ab; die Pitch-Phase hatte keinen Skill. `/pitch` schliesst den Loop.

### Die 4P → Skill-Zuordnung

| Phase | Was sie ist | Skill(s) |
|---|---|---|
| **Perceive** | Ein Problem wahrnehmen, das es wert ist geloest zu werden, und als Intent festhalten | `/intent` (BOO-1) |
| **Prompt** | Den Intent in eine konkrete Story mit Erfolgskriterien und Scope uebersetzen | `/ideation` + `/backlog` |
| **Produce** | Bauen — mit Quality-Gates, Tests, Observability und Learning-Loop | `/implement` + `/architecture-review` + `/sprint-review` |
| **Pitch** | Zeigen, was gebaut wurde — Evidenz zuerst, Demo danach, Slides nie | `/pitch` (BOO-37) |

### Warum `/pitch` Hybrid ist, nicht Vollautomat

Drei Optionen wurden am 2026-04-28 abgewogen (siehe BOO-37):

1. **Kein Skill** — jeder Operator baut das Briefing per Hand. Skaliert nicht, sobald BOO-15/16/17 viele Datenquellen produzieren.
2. **Voller Skill mit Slide-Generierung** — der Skill schreibt das Pitch-Deck. Verraet Schraders Prinzip ("der Pitch ist Evidenz, nicht Theater"), hohes KI-Slop-Risiko.
3. **Hybrid (gewaehlt)** — Skill sammelt Evidenz, Mensch baut die Story und macht die Live-Demo.

`/pitch` erzeugt AUSSCHLIESSLICH ein Markdown-Briefing (`pitch/PITCH-XX.md`). Er erzeugt KEINE Slides, KEIN Voice-Over, KEINEN Outcome-Text und KEIN Demo-Video. Die Buehne bleibt menschlich.

### `PITCH-XX.md` Frontmatter-Schema

```yaml
---
pitch_id: PITCH-12
sprint: 12
created_at: 2026-04-28T14:00:00Z
related_intents: [INTENT-3, INTENT-5]
related_stories: [BOO-15, BOO-16, BOO-17]
metrics_snapshot:
  loc_delta: "+2,341 / -890"
  coverage_trend: "82% → 84% (+2pp)"
  p95_change: "180ms → 145ms (-19%)"
  iterations_avg: 2.3
  feature_flags_active: 3
  intent_fulfillment_score: 0.85
demo_path: "User-Onboarding → Search → Checkout"
status: prepared | delivered | post-mortem
---
```

Feld-Referenz in `pitch/references/pitch-template.md`.

### Die 8 read-only Datenquellen

| Quelle | Pfad | Was wird gelesen |
|---|---|---|
| L3 Lessons-DB | `journal/learnings.db` | Cross-Sprint-Trends, Iterations-Avg |
| Local Reports | `journal/reports/local/{date}_{story}/` | Iterations-Counts, Final-Status (`meta.json`) |
| CI Reports | `journal/reports/ci/run-{id}/` | Coverage, Performance-Baselines (BOO-32) |
| Sprint-Files (L2) | `journal/sprint-{date}.md` | Aggregat-Metriken pro Sprint |
| Architektur-Doku | `ARCHITECTURE_DESIGN.md` | Snapshot fuer Diff vs. letztem Pitch |
| Intents | `intents/INTENT-XX.md` | Erfolgskriterien fuer Intent-Erfuellung |
| Feature-Flags | `.claude/feature-flags.json` (BOO-17) | aktive Flags + Rollout-Phase |
| Git-Log | `git log --shortstat --since=...` | LOC-Delta, Commit-Counts |

Der Skill ist **strikt read-only**. Er schreibt NICHT in die L3-DB — das schuetzt die saubere Trennung zu `/sprint-review`.

### Anti-Scope

Was der Skill EXPLIZIT NICHT tut:

- **Keine Slide-Generierung** — kein PowerPoint, kein Reveal.js, kein Marp
- **Kein Outcome-Text** — User-Reaktionen entstehen nur in der Live-Demo, freitext im Schritt 6
- **Kein Voice-Over / kein Demo-Video**
- **Kein Schreiben in L3** — read-only Position
- **Keine Stakeholder-Mail** — Kommunikation bleibt menschliche Arbeit

Wenn jemand diese Features will: separates Issue, nicht im BOO-37-Scope.

### `paths.pitches` in `.claude/environment.json`

Bootstrap v3.23.0 fuegt `paths.pitches: "pitch/"` (und `paths.intents: "intents/"`) zum Environment-Manifest hinzu. Bestehende Projekte ziehen es via `bash .claude/generate-environment-json.sh --force` nach einem `git pull` des Bundles.

### Verortung in der Skill-Pipeline

```
/intent → /ideation → /backlog → /implement → /architecture-review → /sprint-review → /pitch
                                                                                        ↑
                                                                            Evidenz-Briefing
                                                                            fuer den naechsten Demo
```

`/pitch` laeuft NACH `/sprint-review` (Sprint-Metriken muessen aggregiert sein) und VOR dem Stakeholder-Termin (Operator nimmt das Markdown-Briefing als Spickzettel mit in den Raum).

### Verwandte Sektionen

- Anhang D — `metadata.hermes`-Block-Schema (BOO-31)
- Anhang E — `journal/reports/`-Konvention (BOO-32)
- Anhang G — Sprint-Sizing-Mechanik (BOO-38)
- `pitch/SKILL.md` — vollstaendiger Skill-Workflow (6 Schritte)
- `pitch/references/pitch-template.md` — Body-Schema fuer `PITCH-XX.md`
- `pitch/references/demo-path-heuristic.md` — Heuristik fuer den Demo-Pfad-Vorschlag

---

## Anhang M: Schrader-Decoder — Wir haben das Operating System fuer Code Crash gebaut

Dieser Anhang ist die Karte vom Buch ins Bundle. Schraders "Code Crash" (2026) liefert die Theorie der KI-Software-Aera, dieses Bundle liefert die ausfuehrbare Praxis dazu. Wenn du das Buch nicht gelesen hast, ist das kein Problem — der Decoder ist kein Re-Reading, sondern eine Uebersetzung: pro Schrader-Kapitel ein Konzept, ein Hero-Sketch, eine Hand voll Detail-Sketches mit den zentralen Buch-Argumenten, und eine konkrete Stelle im Bundle, wo das Konzept als Skill, BOO oder Governance-Regel lebt.

![Operating System Overview](docs/schrader-sketches/operating-system-overview.png)

*Das ganze Bundle auf einen Blick — Skills, 4P-Pipeline, Governance-Schicht.*

Das Bundle ist mein Operating System fuer Code-Crash-Engineering. Schrader beschreibt, was sich aendert, wenn KI das Code-Schreiben uebernimmt. Das Bundle ist die operative Antwort darauf — 11 Skills, die 4P-Pipeline und eine Governance-Schicht, die die Theorie in taegliche Praxis verwandelt.

### Kapitel 1 — Effekte zweiter Ordnung

![Kapitel 1 — ChatGPT-Moment](docs/schrader-sketches/chapter-01-hero.png)

*Der ChatGPT-Moment im November 2022 — der Riss in der Realitaet, mit dem das Buch beginnt.*

**Schrader sagt:** Der Flaschenhals Code-Schreiben ist weg. Der neue Flaschenhals heisst Intent — und die Effekte zweiter Ordnung (Jevons-Paradox) sind groesser als die offensichtlichen Effizienzgewinne. Schrader stellt die Triade Soul-System-Speed vor und skizziert erstmals die 4P-Pipeline aus Perceive, Prompt, Produce und Pitch.

**Vertiefung im Buch:**

![Silent Revolution — Wer gewinnt, wer verliert](docs/schrader-sketches/chapter-02-hero.png)

*Die stille Revolution: agentische KI-Tools machen LLMs zu Produktivitaets-Monstern; die Coordination Class verliert, kleine autonome Teams gewinnen.*

![Das neue Paradox](docs/schrader-sketches/chapter-02-detail-1.png)

*Software-Entwicklung wird gleichzeitig leichter und auf neue Weise schwerer — wenn alle bauen koennen, entscheidet der Spark statt der Syntax.*

![Two Paradigm Shifts](docs/schrader-sketches/chapter-02-detail-2.png)

*Zwei parallele Brueche: Agile in der Krise + Intent wird produktiv. Wenn Output nichts mehr kostet, wird Input zur knappen Ressource.*

**Wir loesen das so:** Das gesamte Bundle ist die Antwort auf Jevons — wenn Code billiger wird, wird Intent teurer, also bekommt Intent einen eigenen Skill am Anfang der Pipeline. Die 4P-Struktur ist nicht Deko, sondern in der Skill-Architektur verankert: jeder Skill gehoert eindeutig zu einem P. Details siehe Anhang L (4P-Pipeline-Mapping).

### Kapitel 2 — Die agile Illusion

![Kapitel 2 — Cargo Cult Agile](docs/schrader-sketches/chapter-03-hero.png)

*Cargo Cult: Rituale ohne Kern. Standups ohne Hindernis-Talk, Story Points als Performance-Mass, Sprints mit Top-Down-Scope — Mini-Wasserfall in agiler Tarnung.*

**Schrader sagt:** Cargo-Cult-Agile wiederholt Rituale ohne den Kern zu treffen. Output hat Outcome verdraengt, SAFe loest das falsche Problem, und die kleinste sinnvolle Einheit ist nicht mehr das Team, sondern Individuum plus KI. Teams werden nur noch dann gebaut, wenn sie nachweislich beschleunigen.

**Vertiefung im Buch:**

![SAFe — Anatomie des Versagens](docs/schrader-sketches/chapter-03-detail-1.png)

*Agile Release Trains mit 50-125 Personen, Rollen-Inflation, Artefakt-Explosion, Zeremonien-Flut — SAFe skaliert nicht Agilitaet, sondern die Illusion von Agilitaet.*

![Wer profitiert von SAFe](docs/schrader-sketches/chapter-03-detail-2.png)

*Das Geschaeftsmodell hinter dem Festhalten: Zertifizierungs-Industrie, Consulting-Komplexitaet, Middle-Management-Kontrolle, organisierte Unverantwortlichkeit.*

**Wir loesen das so:** Velocity ist tot — kein Burndown, keine Story-Points-pro-Sprint-Statistik. Ein Sprint im Bundle ist 80 Prozent des Context-Windows des verwendeten Modells, also eine Token-Box statt einer Zeit-Box. Outcome wird ueber Intent-Erfuellung gemessen, nicht ueber Storypoint-Verbrauch. Details: HANDBUCH Anhang G (Sprint-Sizing-Mechanik), BOO-38, BOO-39, BOO-40.

### Kapitel 3 — Die KI-Revolution in der Softwareentwicklung

![Kapitel 3 — Vier Generationen KI-Coding](docs/schrader-sketches/chapter-04-hero.png)

*Von Autocomplete ueber Chat und Terminal-first bis zu Agentic IDEs — mit Opus 4.5 wird KI vom Assistenten zum Produktionspartner.*

**Schrader sagt:** Vier Generationen KI-Coding — Autocomplete, Chat, Terminal-first, Agentic IDEs — und mit Opus 4.5 wird KI vom Assistenten zum Produktionspartner. Vibe Coding allein reicht nicht mehr, daraus muss Agentic Engineering werden. Die neue Latte heisst Produktionsreife.

**Vertiefung im Buch:**

![Vibe Coding vs Agentic Engineering](docs/schrader-sketches/chapter-04-detail-1.png)

*Der Unterschied liegt in der Haltung: Vibe-Coder hoffen, dass es funktioniert. Agentic Engineers stellen sicher, dass es funktioniert — strukturiert, mit Tests, mit Security-Grenzen.*

![Senior vs Junior + Skill Atrophy](docs/schrader-sketches/chapter-04-detail-2.png)

*Fastly-Studie (Juli 2025): Senior-Entwickler nutzen KI-Code 2,5-mal so oft wie Juniors und profitieren staerker. Anfaenger brauchen Reibung, um Urteilsvermoegen zu entwickeln — sonst entsteht die naechste Generation, die KI dirigiert, ohne ihre Werke zu verstehen.*

**Wir loesen das so:** Drei-Layer-Quality-Gate-Architektur macht aus Vibe Coding produktionsreifes Agentic Engineering — Layer 1 in der IDE, Layer 2 als Pre-Commit-Hook, Layer 3 in der CI. ESLint, Semgrep, Coverage-Gate, Performance-Baseline und SonarQube greifen ineinander, damit nichts an den Gates vorbei in main wandert. Details: HANDBUCH §6 + §8d, BOO-2 (ESLint), BOO-4 (Semgrep), BOO-15 (Coverage), BOO-16 (Performance), BOO-5 (SonarQube), BOO-24 (KI-Architektur-Prinzipien).

### Kapitel 4 — Intent is the new Code (Kernkapitel)

![Kapitel 4 — Intent als knappste Ressource](docs/schrader-sketches/chapter-05-hero.png)

*Intent als Startpunkt der Wertschoepfung: Soul-System-Speed-Triade ersetzt die alte Wirkungskette Vision → Objective → Outcome → Tech Requirement.*

**Schrader sagt:** Intent ist die neue knappe Ressource. Die Soul-System-Speed-Triade verwandelt Intent in Realitaet, und Agency — Judgment, Cultural Fluency, Meaning-Setting — ist die menschliche Faehigkeit, die KI nicht ersetzen kann. Das Kapitel listet die Top 5 Intent-Fehler und liefert das Template: "[Nutzergruppe] soll [messbares Ergebnis] erreichen, ohne [Reibung]. Erfolg = [Metrik]."

**Vertiefung im Buch:**

![Feed the Soul — Agency](docs/schrader-sketches/chapter-05-detail-1.png)

*Soul hat zwei Dimensionen — die menschliche (Agency: Entscheidungsfaehigkeit, Verantwortung, innere Verankerung) und die produktbezogene (das, was differenziert).*

![Intent vor Prompt — die richtige Reihenfolge](docs/schrader-sketches/chapter-05-detail-2.png)

*Zuerst Intent (technologie-agnostisch), dann Optionen generieren lassen, dann gegen den Intent bewerten, erst zum Schluss Prompts schreiben. Wer mit Prompts startet, baut das Falsche schnell.*

![Intent Session — der 6-Schritte-Workshop](docs/schrader-sketches/chapter-05-detail-3.png)

*Ein guter Intent entsteht im Team aus Product, Design, Engineering plus Domaenen-Wildcard: Stories hoeren, Status quantifizieren, Brainstormen, Schaerfen, Validieren, Verschriftlichen.*

**Wir loesen das so:** Der /intent-Skill ist die direkte Antwort auf das Kernkapitel — vorgeschaltet vor /ideation, mit Anti-Pattern-Self-Check, der die drei Soulkiller und die fuenf Intent-Fehler aus Schrader explizit durchgeht. Der formulierte Intent propagiert anschliessend durch alle nachgelagerten Skills: er ist Gate in der Ideation, Gewicht im Backlog, Messpunkt im Implement-Measure-Loop. Details: BOO-1 (Intent-Skill), BOO-10 (Intent-Propagation), `intent/SKILL.md`, `intent/references/intent-anti-patterns.md`.

### Kapitel 5 — Die Intent-to-Production Pipeline

![Kapitel 5 — 4P-Pipeline](docs/schrader-sketches/chapter-06-hero.png)

*Vier Boxen, ein Prozess: Perceive → Prompt → Produce → Pitch. Der klassische Genehmigungs-Stage-Gate-Prozess wird ersetzt durch eine Pipeline, die in Wochen liefert statt in Quartalen.*

**Schrader sagt:** Die 4P-Pipeline aus Perceive, Prompt, Produce und Pitch ersetzt den klassischen Genehmigungsprozess. Prototypen sind tot — die neue Pitch-Form ist die Live-Demo mit Vorher-Nachher-Metriken. Dazu die Two-Document Rule: ein Intent Document fuer das Was, ein Execution Plan fuer das Wie.

**Vertiefung im Buch:**

![Vier Phasen fliessen ineinander](docs/schrader-sketches/chapter-06-detail-3.png)

*Perceive → Prompt → Produce → Pitch im Detail: jede Phase Stunden bis Tage statt Wochen. Gesamter Zyklus 1-4 Wochen fuer klar definierte Features, 8-12 Wochen fuer regulierte Umgebungen.*

![Quality Gates statt Menschen-Kontrolle](docs/schrader-sketches/chapter-06-detail-2.png)

*Old vs New Model: Statt Tech Lead, Architect und Security Officer als Genehmiger gibt es automatisierte Gates auf jedem Commit. Das Autonomy-Paradox: autonome Teams brauchen haertere, automatisierte Guardrails, weil keine Zeit fuer menschliche Intervention bleibt.*

![Multi-Agent Orchestration](docs/schrader-sketches/chapter-06-detail-5.png)

*Writer Agent, Editor Agent, Code Agent — jeder mit eigener SOUL.md fuer Persoenlichkeit und Entscheidungsprinzipien. Der Product Engineer wird Orchestrator: Mission definieren, Spezialisten koordinieren, statt selbst zu implementieren.*

![Pitch als Moment der Wahrheit](docs/schrader-sketches/chapter-06-detail-4.png)

*Schlechte Ideen werden gebaut und scheitern sichtbar. Gute Ideen beweisen sich. Niemand kann sich mehr hinter Konzepten verstecken — der Pitch entscheidet, ob weitere Mittel fliessen.*

![Feature Flag Strategy](docs/schrader-sketches/chapter-06-detail-1.png)

*Statt Big-Bang-Releases: schrittweiser Rollout per Feature Flag. Die 4P-Pipeline liefert kontinuierlich, das Risiko wird durch graduellen Roll-out gemanagt statt durch laenger werdendes Testen.*

**Wir loesen das so:** Die komplette Skill-Pipeline ist 4P — /intent ist Perceive, /ideation und /backlog sind Prompt, /implement plus /architecture-review plus /sprint-review sind Produce, und /pitch ist Pitch. Pitch laeuft seit BOO-37 als Hybrid: der Skill sammelt Evidenz und baut die Argumentations-Struktur, die eigentliche Live-Demo macht der Mensch. Details: HANDBUCH Anhang L (4P-Pipeline-Mapping), BOO-37 (Pitch-Skill).

### Kapitel 6 — Product Teams (Kernkapitel)

![Kapitel 6 — Klassisches Team vs Product Team](docs/schrader-sketches/chapter-07-hero.png)

*Vier Koepfe, ein Outcome ("Checkout-Abbruch von 12% auf 8%"), eigene Architektur, mehrfacher Deploy pro Tag — keine Genehmigungen mehr. So sieht ein echtes Product Team aus.*

**Schrader sagt:** Individuum plus KI ist die neue kleinste Einheit. Product Teams folgen der 3-5-Koepfe-Regel, der Product Engineer hat fuenf Kernfaehigkeiten — Intent-Klarheit, technisches Urteilsvermoegen, Systemdenken, User Empathy, Ownership. Dazu das Alliance Model, Communities of Profession und Outcome Governance ueber drei Saeulen.

**Vertiefung im Buch — Team-Aufbau:**

![No-Team-Test](docs/schrader-sketches/chapter-07-detail-4.png)

*Vor jeder Team-Bildung der ehrliche Check: Brauchst du wirklich ein Team, oder ist Individuum + KI schneller? Vier Fragen — alle "Nein" heisst: kein Team noetig.*

![3-5-Koepfe-Regel](docs/schrader-sketches/chapter-07-detail-2.png)

*Product Engineer + Design + Software Engineer als Kern, plus Wildcard und Junior. Mehr als 5 Koepfe ist Warnsignal: splitten statt aufblaehen — Kommunikationswege wachsen quadratisch.*

![Ownership Architecture](docs/schrader-sketches/chapter-07-detail-1.png)

*Wer besitzt was: Soul (Vision, Meaning) gehoert Product Engineer und Design, System (Architektur, Security) den Engineers, Speed (Pipeline, Go/No-Go) dem gesamten Team.*

![Shared Speed Ownership](docs/schrader-sketches/chapter-07-detail-3.png)

*Geteilte Verantwortung fuer Speed ist kein Kompromiss, sondern Kern: jedes Mitglied traegt persoenlich Verantwortung fuer Velocity — keine unverbindliche Gruppenaufgabe.*

**Vertiefung im Buch — neue Rollen:**

![Kapitel 6 — Product Engineer](docs/schrader-sketches/chapter-08-hero.png)

*Die alten Trennungen zwischen PM, Developer und Designer loesen sich auf. Was entsteht, ist neu: der Product Engineer arbeitet mit KI durchgaengig von Intent zu Outcome — ohne Handoffs.*

![Software Engineer — Skill Atrophy](docs/schrader-sketches/chapter-08-detail-1.png)

*Der Software Developer wird wieder Software Engineer: weniger Implementierung, mehr technischer Intent, mehr Kontrolle. Gegenmittel gegen das Verkuemmern der Coding-Muskeln: manuelle Coding-Uebungen behalten.*

![Designer — Select Rather Than Create](docs/schrader-sketches/chapter-08-detail-2.png)

*KI liefert Best Practice, nicht Markenidentitaet. Der Designer waehlt aus zehn KI-Varianten die richtige, nicht die schoenste. Auswaehlen verlangt Urteilsvermoegen, nicht Handwerk.*

**Vertiefung im Buch — Skalierung & Fuehrung:**

![Kapitel 6 — Alignment Model](docs/schrader-sketches/chapter-09-hero.png)

*Die 2x2-Matrix: hohe Autonomie kombiniert mit hohem Alignment ergibt Empowered Teams. Chaos, Buerokratie und Command-and-Control sind die anderen Quadranten.*

![Human in the Lead vs Human in the Loop](docs/schrader-sketches/chapter-09-detail-3.png)

*Loop ist gefaehrlich unzureichend: KI arbeitet, Mensch greift gelegentlich ein. Lead ist die noetige Haltung: Mensch fuehrt, KI unterstuetzt — proaktiv, mit klarer Verantwortung.*

![Alliance Model — Guardrails](docs/schrader-sketches/chapter-09-detail-1.png)

*Statt SAFe-Trains kommen Alliances: 4-10 Teams (15-40 Personen), getragen von Mission und transparenter Info, nicht von Hierarchie. Guardrails reduzieren Autonomie — also sparsam setzen.*

![Wer entscheidet was](docs/schrader-sketches/chapter-09-detail-4.png)

*Entscheidungs-Architektur: 90 Prozent lokal im Team, bilateral zwischen zwei Teams, alliance-weit nur was wirklich alle betrifft. Eskalations-Stufen: bilateral → Mediation → Alliance-Decision.*

![Alliance vs SAFe-Train](docs/schrader-sketches/chapter-09-detail-2.png)

*Der fundamentale Unterschied: SAFe koordiniert Abhaengigkeiten, Alliances eliminieren sie. Vertikale Schnitte ("Team Checkout"), API-Contracts, sparsame Shared Services, manchmal bewusst Duplizieren.*

![J-Curve der Team-Transformation](docs/schrader-sketches/chapter-09-detail-5.png)

*Drei bis sechs Monate Produktivitaets-Tal in der Lernphase — die J-Curve ist Teil der Investitionsrechnung, nicht ein Bug. Direkte Kosten + indirekte Kosten + Risiken muessen vor dem Start klar sein.*

**Wir loesen das so:** Issue-Writing-Guidelines mit dreistufigem Ausfuehrungsmodus — agentic fuer komplexe Aufgaben mit parallelen Sub-Agents, sub-agent fuer mittlere fokussierte Aufgaben, linear fuer kleine direkte Aufgaben. Story Points haben dabei eine duale Rolle: Token-Schaetzung UND Modus-Selektor. Sub-Agents bekommen beim Spawn ein Mini-Briefing mit Rolle, Kontext und konkreter Aufgabe, statt sich aus dem Chat-Verlauf etwas zusammenzureimen. Details: BOO-11 (Issue-Guidelines v3.0), BOO-38 (SP dual), HANDBUCH §8g (Linear-Setup), `.claude/ISSUE_WRITING_GUIDELINES.md`.

### Kapitel 7 — Risiken und Anti-Patterns

![Kapitel 7 — Drei Kategorien Pathologien](docs/schrader-sketches/chapter-10-hero.png)

*Jede neue Arbeitsweise erzeugt eigene Pathologien. Drei Kategorien — Prozess, Qualitaet, Kultur — plus Frueh-Warnsystem und Kill-Kriterien. Wer Risiken kennt, antizipiert sie.*

**Schrader sagt:** Elf Anti-Patterns in drei Kategorien — drei Prozess-, drei Qualitaets- und fuenf Kultur-Pathologien — plus ein Frueh-Warnsystem und harte Kill-Kriterien fuer Projekte und Skills. Der zentrale Begriff ist Slopware: KI-Mittelmaessigkeit, die die Qualitaetsschwelle nach unten zieht, bis niemand mehr merkt, dass etwas fehlt.

**Vertiefung im Buch:**

![Slopware statt Software](docs/schrader-sketches/chapter-10-detail-1.png)

*KI macht Produktion billig — also wird mehr produziert. Mehr Code, mehr Features, mehr Mittelmass. Ohne strikte Quality Gates ertrinkt die Codebase in derselben Flut, die ab 2026 GitHub, Substack und ArXiv ueberschwemmt.*

![Early Warning System](docs/schrader-sketches/chapter-10-detail-2.png)

*Zwei Ebenen — Organisation und Team — mit konkreten Signalen: alte Meetings kehren zurueck, Reporting-Overhead steigt, Autonomie wird beschnitten, Security-Luecken haeufen sich, niemand nutzt KI-Tools. Pro Signal ein Bedeutung-und-Action-Eintrag.*

**Wir loesen das so:** /sprint-review hat einen eigenen Schritt 7 fuer Anti-Pattern-Selbstdiagnose, der den Katalog aus `sprint-review/references/anti-pattern-katalog.md` Punkt fuer Punkt durchgeht. Ergaenzend pruefen /architecture-review und /implement KI-spezifische Architektur-Anti-Patterns, bevor Code in den Hauptzweig wandert. Details: BOO-26 (Anti-Pattern-Katalog), BOO-24 und BOO-7 (KI-Architektur), HANDBUCH §8b (Kulturelle Anti-Patterns).

### Kapitel 8 — Still Day One (Epilog)

![Kapitel 8 — Still Day One](docs/schrader-sketches/chapter-11-hero.png)

*Februar 2026, Schrader-Manuskript: Die Motivation bleibt gleich, das HOW aendert sich radikal. Was uebrig bleibt, wenn alles sich aendert: Menschen-Probleme. Teams scheitern an Kommunikation, nicht an Technologie.*

**Schrader sagt:** Europa hat eine Chance ueber Branchenwissen plus Leapfrogging — der Rueckstand wird zum Vorteil, wenn man Generationen ueberspringt. "Human in the Lead" ist der neue Fuehrungs-Modus, keine passive Loop-Wache, sondern aktive Steuerung. Trusted AI plus Regulatory Fast Lanes sind der eigentliche Wettbewerbsvorteil.

**Vertiefung im Buch:**

![Fuenf Jahre, drei Handlungsfelder](docs/schrader-sketches/chapter-11-detail-1.png)

*Unternehmen bauen Product Engineering Teams (Beispiel Maschinenbauer 2028: drei Teams, neuer Konfigurator, Predictive Maintenance, Embedded-AI — bis 2030 Plattform-Unternehmen). Gesellschaft profitiert von 10x billiger Software in Schule, Verwaltung, Gesundheit. Startups bekommen das groesste Fenster der Tech-Geschichte.*

**Wir loesen das so:** Das Bundle ist tool-agnostisch — primary ist Claude Code, aber es laeuft genauso mit Codex, Cursor, Aider und lokalen LLMs. Der Operator bleibt im Fahrersitz, die Skills sind Werkzeug, nicht Pilot. Hermes ist ein optionaler Compound-Layer, der Muster ueber mehrere Projekte hinweg erkennt, aber das Bundle funktioniert auch ohne. Details: HANDBUCH Anhang K (Tool-Adapter, BOO-49), Anhang D-F (Hermes), `CONVENTIONS.md` (tool-neutrale Spec).

### Was als naechstes — vom Decoder zum Buch

![Buch-Uebersicht](docs/schrader-sketches/chapter-overview.png)

*Vom Theorie-Buch zum operativen Folge-Buch: Schrader sagt, was sich aendert; das Bundle zeigt, wie es konkret aussieht.*

Schrader liefert die Theorie, das Bundle liefert die Praxis — Skill-Code, Konventionen, Hooks, CI-Gates. Jedes zentrale Konzept des Buchs hat eine ausfuehrbare Entsprechung in einem Skill, einer BOO oder einer HANDBUCH-Sektion. Dieser Decoder ist gleichzeitig das Skelett fuer ein geplantes Folge-Buch, das die Uebersetzung von Schraders Theorie in operative Praxis vertieft: nicht "was sollte sich aendern", sondern "so machst du es konkret". Bis dahin ist dieser Anhang die kuerzeste Brueckenversion — eine Seite Theorie, mehrere Sketches mit den zentralen Buch-Argumenten, eine Seite Bundle, pro Kapitel.

## Anhang N: Token-Effizienz-Policy (BOO-84) — Modell-Routing + Prompt-Caching

Code-Crash-Operatoren bezahlen unnoetig viele Anthropic-Tokens, wenn jeder Skill auf dem Operator-Default-Modell laeuft (meist Opus). Diese Sektion erklaert beide Hebel, die das Framework standardmaessig nutzt — **Modell-Routing pro Skill** und **Prompt-Caching fuer wiederverwendete Bloecke**. Beide folgen dem Designentscheid Leichtgewicht: Empfehlung statt Hard-Lock, Operator-Override jederzeit moeglich, Audit-Trail fuer Compliance.

### N.1 Modell-Routing-Policy

Jeder Skill traegt im Frontmatter `recommended_model: haiku | sonnet | opus` — ein **Tier**, keine Versionsnummer. Die Zuordnung Tier-zu-Version (z.B. Haiku 4.5, Sonnet 4.6, Opus 4.7) lebt zentral in `bootstrap/references/model-tiers.json` und wird einmalig pro Anthropic-Release zentral aktualisiert. So muss kein Operator 11 Skill-Files anfassen, wenn ein neues Modell erscheint.

**Routing-Tabelle**

| Tier | Modell-Klasse | Wofuer | Default-Skills |
|------|---------------|--------|----------------|
| `haiku` | Claude Haiku | Iterations-Loops, Lints, Frage-Generierung, kleine Smoke-Tests | `/implement` Schritte 6a/6a-bis/6a-tris/6a-quart, Lint-Loops |
| `sonnet` | Claude Sonnet | Sicherer Default fuer die meisten Skill-Aufgaben | `bootstrap`, `backlog`, `visualize`, `sprint-review`, `pitch`, `ideation`, `intent`, `grafana` |
| `opus` | Claude Opus | Architektur-Reviews, Security-Findings, Threat Modeling | `architecture-review`, `cloud-system-engineer`, `/implement` Schritt 6e (Security-Findings) |

**Operator-Override (zweistufig)**

1. **CLI-Flag** fuer einmalige Ausnahmen: `/implement --model opus`
2. **CLAUDE.md `model_overrides:` Sektion** fuer projekt-weite Default-Aenderung:

```yaml
model_overrides:
  implement-iterations: sonnet   # statt haiku, weil unsere Iterationen komplexer sind
```

**Praezedenz:** CLI-Flag > CLAUDE.md-Override > Skill-Default-Tier.

Jeder Override wird in `meta.json` unter `override_audit` festgehalten mit Skill, empfohlenem Tier, genutztem Modell, Operator und Zeitstempel.

**Pflicht-Bleibt-Opus (Audit-Argument)**

Security-relevante Skills duerfen pro Story-Lauf **nicht** automatisch auf ein schwaecheres Tier downgrade-en. Operator-Override moeglich, aber im Audit-Trail festgehalten. Das ist das harte Argument fuer regulierte Branchen (FINMA, BaFin, MaRisk): wir koennen pro Story nachweisen, welches Modell fuer welche Aufgabe genutzt wurde — wer auf ein schwaecheres Modell gewechselt hat und warum.

**FinOps-Argument**

Bei einem typischen Kunden-Engagement (6 Monate, ~80 Stories, alle Lints + Tests + Coverage iteriert): naive Opus-Nutzung kostet ca. $400-500 nur fuer Iterations-Loops. Mit Haiku-Routing fuer diese Loops: ~$30-40. **Faktor 12x guenstiger, Marge-Hebel 15-25%.** Dieses Argument geht in jedes Discovery-Gespraech: "Code-Crash optimiert deine LLM-Kosten by design."

### N.2 Prompt-Caching technisch erklaert

Anthropic gibt einen **90% Rabatt auf gecachte Input-Tokens** (Ephemeral Cache mit 5-Min-TTL). Code-Crash nutzt das systematisch fuer Bloecke, die innerhalb einer Story-Iteration mehrfach gelesen werden — ohne dass der Operator manuell Cache-Marker setzen muss.

**Was wird gecacht**

- **SKILL.md-Files** aller geladenen Skills (jeweils 5-15k Tokens) — werden in jeder Iteration des Skills gelesen.
- **Project-Constitution** (`CONVENTIONS.md`, 20-50k Tokens) — wird in jedem Skill-Aufruf gelesen.
- **`SECURITY.md`, `ARCHITECTURE_DESIGN.md`** — gelesen in Architektur-Reviews und Security-Findings.
- **Repository-Map** (`/implement` Schritt 3) — gelesen in jeder Iteration der Implementierungs-Phase.

**Constraints**

| Constraint | Wert | Warum |
|------------|------|-------|
| Mindest-Block-Groesse | 1024 Tokens | Anthropic-Minimum; kleinere Bloecke werden nicht gecacht. |
| Cache TTL | 5 Minuten | Nach 5 Min ohne Read laeuft der Cache ab, naechste Iteration zahlt wieder voll. |
| Cache-Write-Aufschlag | ca. +25% | Erster Write ins Cache ist teurer als ein normaler Read. Lohnt sich ab 2 Reads. |
| Secrets im Cache | verboten | Kein API-Key, Token oder Credential darf in einen Cache-Block. |

**Wie wir das messen**

Cache-Hit-Rate (`cache_read_tokens / (input_tokens + cache_read_tokens)`) wird in jeder Story-`meta.json` als eigener Wert gespeichert. `/sprint-review` aggregiert das pro Sprint. Ziel-Wert: ueber 60% Cache-Hit-Rate bei mehr-iterativen Stories. Wenn die Rate dauerhaft unter 30% liegt: vermutlich passen Cache-Bloecke nicht zur Skill-Struktur — Folge-Story zur Tuning-Iteration.

**Was das fuer Iterations-Schmerzen heisst**

Bei einer Story mit 5 Lint-Iterationen liest jeder Iterations-Aufruf die `SKILL.md` (10k Tokens) und die Constitution (30k Tokens) neu. Ohne Caching: 5x40k = 200k Tokens voll bezahlt. Mit Caching: 1x40k voll, dann 4x4k (90% Rabatt) = 56k effektive Kosten. **Ersparnis: ~70% nur durch Caching.** Kombiniert mit Haiku-Routing fuer diese Iterationen: ~95% guenstiger als naive Opus + kein Cache.

**Designentscheid-Hinweis**

Cache ist optional aktivierbar via Claude-Code-Hook. Wenn der Hook nicht eingerichtet ist: alles funktioniert weiter, nur ohne Caching-Vorteil und ohne Cost-Aggregat im Sprint-Review (`meta.json.token_tracking` bleibt leer). Kein Hard-Block — Operator kann Caching jederzeit nachruesten.

## Anhang O: Privacy by Design (BOO-69) — DPO als Framework-Bundle-Skill

### Wann brauche ich den Privacy-Modus?

Aktiviere das Privacy-Add-on im `/bootstrap` (Phase A.4), wenn einer dieser Trigger zutrifft:

- Das Projekt verarbeitet personenbezogene Daten von EU-Buergerinnen oder Personen mit Schweiz-Bezug — die DSGVO bzw. das nDSG greifen.
- Das Projekt hat eine Auftragsverarbeiter-Konstellation (Verarbeitung im Auftrag eines Dritten).
- Branche mit erhoehter Pflicht: Gesundheit (Patientendaten), Finanz (Bonitaet, KYC), HR (Beschaeftigtendaten), Bildung (Lernerdaten), oeffentliche Verwaltung.

Kein Privacy-Modus noetig: Solo-Tool ohne Datenerhebung, ausschliesslich anonyme Daten, kein EU/CH-Bezug, kein Auftragsverarbeitungs-Kontext.

### Was macht der DPO-Skill (3-Modi-Mapping)

Der DPO-Skill ist seit **BOO-74 (Wave M)** ein **Framework-Bundle-Skill**: er liegt direkt im `code-crash-framework`-Repo (analog `bootstrap/`, `implement/`, `security-architect/`) und wird von Bootstrap Phase 5 aus dem Framework-Repo nach `~/.claude/skills/dpo/` installiert. Master des Skills bleibt das `claudecodeskills`-Repo (gepflegt via `publish_skill.py`); das Framework-Repo haelt eine gespiegelte Vendored-Kopie. Solo-Operatoren ohne Framework koennen DPO weiterhin direkt aus `claudecodeskills` beziehen. Drei Modi mit klarem Trigger-Punkt in der Pipeline:

| Modus | Trigger | Pipeline-Stelle | Output |
|-------|---------|------------------|--------|
| ASSESS | Story plant neue Verarbeitung personenbezogener Daten | `/ideation` Schritt 0e (`personal_data: true` im Story-Frontmatter) | `dpia/DPIA-<feature>.md` aus DPIA-Template, Rechtsgrundlage gewaehlt |
| REVIEW | Code-Aenderung trifft personal-data-paths | `/implement` Schritt 5.5b (Personal-Data-Paths-Gate) | Privacy-Findings inline + `journal/reports/local/<date>_<story>/privacy.md` |
| AUDIT | Alle N Sprints (Default 4, konfigurierbar via `environment.json.privacy_audit_cadence`) | `/sprint-review` Schritt 7c | Verarbeitungsverzeichnis-Diff im Sprint-Report, offene Compliance-Punkte |

DPO deckt DSGVO/GDPR (EU), BDSG (DE) und nDSG (CH) ab. Schweizer Spezialitaeten (kein 72h-Limit, Bussen gegen natuerliche Personen, EDOEB statt EU-Behoerde) sind in den Skill-References dokumentiert.

### Zusammenspiel DPO ↔ security-architect

Klare Trennung der beiden Disziplinen:

| Disziplin | Frage | Skill | Hauptartefakt |
|-----------|-------|-------|----------------|
| Privacy | "Darf ich diese Daten verarbeiten?" | `dpo` | `PRIVACY.md` (Rechtsgrundlagen, Verarbeitungsverzeichnis, Loeschkonzept) |
| Security | "Kann ich diese Daten sicher verarbeiten?" | `security-architect` | `SECURITY.md` (TOMs, Encryption, Access Control) |

Bei aktivem Privacy-Add-on laufen beide Skills parallel. Im Datenschutz-Vorfall (Art. 33 DSGVO) braucht es beide Inputs — DPO bewertet rechtlich (Meldepflicht-Schwellen, Betroffenenrechte), security-architect technisch (Forensik, Mitigation).

### Privacy-Add-on in Bootstrap aktivieren

Phase A.4 Add-on-Block bietet Multi-Select. Bei `[x] Privacy / DSGVO`:

1. Bootstrap installiert den DPO-Skill aus dem Framework-Bundle (`$SKILL_SRC/dpo/`, sofern nicht schon vorhanden) — BOO-74.
2. Bootstrap installiert auch `security-architect` aus dem Framework-Bundle (Voraussetzung fuer das DPO ↔ security-architect-Zusammenspiel).
3. Bootstrap rendert `PRIVACY.md` aus `bootstrap/references/privacy-template.md` (DE oder EN je nach Projekt-Sprache).
4. Bootstrap erzeugt `personal-data-paths.json` Template (`.claude/` oder `.codex/`).
5. Bootstrap setzt Backlog-Label `privacy`.
6. Bootstrap-Phase 4.4n "Privacy-Setup" lauft (analog 4.4i Sensitive-Paths-Setup).

### Migrations-Hinweise fuer Bestands-Projekte

Bestands-Projekt hat das Privacy-Add-on noch nicht aktiv?

```bash
bash bootstrap/scripts/migrate-to-v2.sh migrate_boo_69
```

`migrate_boo_69()` ist idempotent und additiv. Ergebnis:

- `PRIVACY.md` aus Template erzeugt (falls noch nicht vorhanden)
- `personal-data-paths.json` Template angelegt
- DPO-Skill-Kopie aus dem Framework-Bundle nachgezogen (BOO-74; `migrate_boo_74` ergaenzt DPO + security-architect explizit)
- `SECURITY.md` bleibt unveraendert
- Backlog-Label `privacy` ergaenzt

Operator pflegt `PRIVACY.md` nach der Erstausgabe manuell — fuellt Rechtsgrundlagen, Datenkategorien und Loeschfristen mit Projekt-Realdaten. DPO ASSESS-Modus kann beim Erstausfuellen unterstuetzen.

### Verwandte Anhaenge

- **Anhang N (Token-Effizienz):** DPO laeuft auf `recommended_model: opus` (Compliance-kritisch, Audit-relevant). Bei aktivem Modell-Routing wird das im Sprint-Review-Cost-Aggregat fair als Opus-Tier ausgewiesen.
- **Anhang Q (Souveraenitaets-Stack, BOO-71, geplant):** Datensouveraenitaet (US-vs-EU-Cloud-Anbieter) ist ein **separates Thema** und kein Privacy-Ersatz — auch ein souveraener Stack braucht Privacy-by-Design. Anhang Q gibt die Inspirations-Schicht fuer EU-konforme Alternativen.
- **Anhang F (Hermes Compound-Layer):** DPO ist im `metadata.hermes`-Mapping mit `category: governance` und Tags `[privacy, gdpr, dsgvo, ndsg, compliance]` registriert.

---

## Anhang P: Deployment-Szenarien — Solo-Mac / Solo-VPS / Multi-User-VPS / Team-Server (BOO-70)

Dieser Anhang beschreibt vier gelebte Setup-Patterns fuer das Code-Crash-Framework, vom Solo-Operator am Mac bis zur Multi-User-VPS-Coding-Factory. Er existiert, weil das Bootstrap-Skript bewusst nur **eine** zusaetzliche Frage stellt (Default Solo-Mac) und Details hier landen, statt den Bootstrap aufzublaehen. Operatoren waehlen ihr Szenario via Decision-Matrix, lesen die zugehoerige Szenario-Sektion und arbeiten die Setup-Schritte einmalig ab. Das Framework selbst funktioniert in allen vier Szenarien gleich — nur die Umgebung drumherum unterscheidet sich.

![Deployment-Szenarien — die vier Setup-Topologien von Solo-Mac bis Coding-Factory](docs/assets/boo-70-deployment-scenarios.png)

### Decision-Matrix

| Operator-Profil | Empfohlenes Szenario | Hauptgrund |
|-----------------|----------------------|------------|
| Solo-Operator stationaer (Buero, ein Mac) | Szenario 1 — Solo-Mac | Frictionless Default, Skill-Pool zentral, keine Server-Wartung. |
| Solo-Operator mobil (mehrere Geraete, ortsunabhaengig) | Szenario 2 — Solo-VPS | 24/7-Erreichbarkeit, Geraete-unabhaengiger Zugriff via SSH. |
| 2-5 Operatoren mit gemeinsamem Code-Hub | Szenario 4 — Team-mit-Coding-Server | Hybrid Mac-Frontend + VPS-Backend, geteilter Backlog. |
| Coding-Factory mit 5+ Operatoren und geteilter Skill-Sammlung | Szenario 3 — Multi-User-VPS | Saubere User-Isolation, zentral wartbarer Skill-Pool. |
| Behoerde / Branche mit DSGVO-Pflicht | Szenario 2 oder 3 (EU-VPS) | Datenstandort-Kontrolle; Verweis auf Anhang O Privacy by Design + Anhang Q Souveraenitaets-Stack. |
| Hobby / Experiment ohne Produktiv-Anspruch | Szenario 1 — Solo-Mac | Minimaler Setup-Aufwand, Operator kann jederzeit auf VPS migrieren. |

### Szenario 1 — Solo-Mac (Default, ~80% der Operatoren)

**Operator-Profil**

- Ein Operator, ein Mac (stationaer oder Laptop).
- Kein 24/7-Background-Bedarf, keine Mobile-Zugriffe ueber Geraete-Grenzen hinweg.
- Will frictionless starten und ohne Server-Wartung arbeiten.

**Setup-Schritte**

1. Claude Code CLI via `npm` installieren (Anthropic-Standardpfad).
2. Skill-Pool zentral in `~/.claude/skills/` halten — alle Projekte greifen darauf zu.
3. Projekt-Verzeichnis unter `~/Documents/GitHub/<projekt>/` anlegen.
4. Im Projekt `claude` starten und `/bootstrap` ausfuehren (Bootstrap-Frage A.7 = a) Solo-Mac).
5. Secrets in `~/.claude/.env` ablegen (User-Ebene, nicht im Projekt).
6. `.gitignore` im Projekt pruefen — `.env`, `.claude/local/`, `journal/reports/local/` muessen drin sein.
7. Linear oder GitHub Issues als Backlog-Tool im Bootstrap-Interview waehlen.
8. Time Machine fuer den Mac aktivieren (System-Einstellungen → Time Machine).

**Skill-Installation**

- Zentraler Pool unter `~/.claude/skills/`. Kein pro-Projekt-Sync noetig.
- Skill-Updates via `git pull` im Skill-Repo, gilt sofort fuer alle Projekte.
- `security-architect` und `dpo` (Framework-Bundle-Skills seit BOO-74) ebenfalls zentral im Pool (siehe Anhang O).

**Secrets-Trennung**

- Eine `.env` auf User-Ebene unter `~/.claude/.env`.
- Projekt-Verzeichnisse enthalten **keine** Secrets — nur Verweise auf Env-Variablen.
- `.gitignore`-Pruefung ist Pflicht-Schritt im Bootstrap.

**Backup-Strategie**

- Time Machine auf externe Festplatte (primaer).
- Optional: Mac-Backup nach iCloud (Dokumente-Ordner) oder Backblaze B2 fuer Cloud-Kopie.
- Skill-Pool und Projekte sind ueber Git versioniert — Backup ist Schutz gegen Hardware-Defekt, nicht gegen Code-Verlust.

**Tradeoffs**

- Kein 24/7-Background-Run moeglich (Mac muss laufen).
- Nicht mobil ueber Geraete-Grenzen hinweg — Operator-Geraet ist der Single Point of Use.
- Keine Geraete-Redundanz: Mac-Ausfall = Arbeitsstillstand bis Backup-Restore.

### Szenario 2 — Solo-VPS (BOO-9-Pattern, fuer Mobile-Worker und 24/7-Background-Tasks)

**Operator-Profil**

- Ein Operator, mehrere Zugriffsgeraete (Laptop, Tablet, fremder Rechner).
- Braucht 24/7-Erreichbarkeit fuer Cron-Tasks, lang laufende Background-Agenten, geplante Builds.
- Akzeptiert Server-Wartung als Tradeoff fuer Mobilitaet.

**Setup-Schritte**

1. VPS beim Provider deiner Wahl bereitstellen (z.B. Hostinger VPS, Hetzner — Operator waehlt aus).
2. SSH-Key-basierten Login einrichten, Passwort-Login deaktivieren.
3. Auf dem VPS Node.js + `npm` installieren und Claude Code CLI via `npm` installieren.
4. Skill-Pool unter `~/.claude/skills/` per `git clone` aus dem persoenlichen Skill-Repo holen.
5. Skill-Sync via `git pull` manuell — heterogene Skill-Versionen zwischen Mac und VPS sind erlaubt (siehe Memory-Hinweis: kein Auto-Sync).
6. Optional: Cron-Job fuer regelmaessiges `git pull` einrichten, wenn der Operator Update-Disziplin formalisieren will.
7. Eigene `.env` auf dem VPS unter `~/.claude/.env` ablegen — strikt getrennt vom Mac-`.env`.
8. Backup-Ziel konfigurieren (Hetzner Storage Box oder Backblaze B2 — Operator waehlt aus).
9. Projekt-Verzeichnis unter `~/projects/<projekt>/` anlegen und `/bootstrap` ausfuehren.

**Skill-Installation**

- Zentraler Pool unter `~/.claude/skills/` auf dem VPS, identische Struktur wie am Mac.
- Skill-Sync ist **manuell** (`git pull`) oder via Cron — kein Auto-Push vom Mac.
- Heterogene Versionen erlaubt: VPS kann auf einer aelteren Skill-Version stehen, wenn der Operator das so will.

**Secrets-Trennung**

- VPS-`.env` strikt getrennt vom Mac-`.env`.
- Keine `.env` aus dem Mac-Backup auf den VPS uebertragen — pro Geraet eigene Werte.
- SSH-Keys sind keine Secrets im Sinne der `.env`, gehoeren aber in `~/.ssh/` mit Mode 600.

**Backup-Strategie**

- Hetzner Storage Box oder Backblaze B2 als Backup-Ziel (Operator waehlt aus).
- Backup-Frequenz: mindestens taeglich fuer `journal/`, `backlog/`, `.claude/local/`.
- Git-versionierte Inhalte (Code, Skills) sind durch das Remote-Repo abgedeckt — Backup deckt Operator-State und Secrets.

**Tradeoffs**

- Setup-Aufwand 1-2 Stunden initial (SSH-Hardening, Skill-Sync, Backup-Konfiguration).
- Single Point of Failure: VPS down = kein Zugriff.
- Etwas hoehere LLM-Latenz wegen EU-Routing und zusaetzlichem Netzwerk-Hop.

### Szenario 3 — Multi-User-VPS-Coding-Factory (BOO-83-Pattern, fuer Teams + geteilte Skill-Sammlung)

**Operator-Profil**

- 5+ Operatoren auf gemeinsamem VPS, jeweils mit eigenem System-User.
- Geteilte Skill-Sammlung, eigene Repositories pro User.
- Wartungs-Owner ist definiert (sonst Anti-Pattern).

**Setup-Schritte**

1. VPS-Sizing dimensionieren: mindestens 8 GB RAM und 4 vCPU als Daumenwert fuer 5 parallele Operatoren (Operator waehlt aus).
2. Pro Operator System-User anlegen: `sudo useradd -m -s /bin/bash <name>`.
3. SSH-Keys pro User in `/home/<name>/.ssh/authorized_keys` hinterlegen, Passwort-Login global aus.
4. `UMASK 077` global setzen, damit User-Verzeichnisse nicht weltlesbar werden.
5. `sudo`-Regeln pro User definieren — wer darf was, was bleibt root-only.
6. Skill-Pool-Strategie entscheiden: entweder global unter `/opt/claude/skills/` (read-only fuer User) **oder** pro User in `~/.claude/skills/` (eigene Kopie pro Operator). Beide Patterns sind dokumentiert und unterstuetzt.
7. Repository-Worktrees pro User: jeder User cloned seine Projekte in sein eigenes Home — keine geteilten Working Trees.
8. Secrets STRIKT pro User in `~/.claude/.env`. Keine geteilten `.env`-Dateien.
9. Backup-Strategie zentral (VPS-Snapshot beim Provider) plus pro Home-Verzeichnis (Hetzner Storage Box oder Backblaze B2 — Operator waehlt aus).
10. Konfigurations-Drift regelmaessig pruefen (`jq` auf `~/.claude/settings.json` pro User vergleichen).

**Skill-Installation**

- **Variante A (global):** `/opt/claude/skills/` read-only, gepflegt von Wartungs-Owner. Updates via `git pull` als root. User koennen nicht selbst patchen.
- **Variante B (pro User):** jeder User pflegt sein eigenes `~/.claude/skills/`. Mehr Freiheit, mehr Drift-Risiko.
- Entscheidung dokumentieren — Wechsel mittendrin ist teuer.

**Secrets-Trennung**

- Strikt pro User in `~/.claude/.env`, Mode 600.
- Keine Shared-Secrets ueber `/etc/` oder `/opt/`.
- Bei Operator-Wechsel: User-Account loeschen, `.env` ist mit weg.

**Backup-Strategie**

- VPS-weiter Snapshot beim Provider (taeglich, Operator waehlt aus).
- Plus pro Home-Verzeichnis-Backup nach Hetzner Storage Box oder Backblaze B2.
- Git-Remotes pro User decken Code ab — Backup deckt Operator-State, Journal, Secrets.

**Tradeoffs**

- Wartungsaufwand spuerbar: User-Onboarding, Skill-Updates, Drift-Erkennung, Snapshot-Pruefung.
- User-Isolation ist kritisch — ein kompromittierter User darf nicht andere User sehen.
- Konfigurations-Drift zwischen Usern muss aktiv ueberwacht werden (sonst "wieso laeuft Skill X bei Alice und nicht bei Bob").

### Szenario 4 — Team-mit-Coding-Server (Hybrid Mac-Frontend + VPS-Backend, 2-5 Operatoren)

**Operator-Profil**

- 2-5 Operatoren mit eigenem Mac, aber gemeinsamem Code-Hub auf VPS.
- Editor laeuft lokal (VS Code Remote-SSH), Code lebt auf dem Server.
- Verteiltes Team mit Zeitzonen-Versatz oder unterschiedlichen Standorten.

**Setup-Schritte**

1. VPS bereitstellen (siehe Szenario 2 Schritte 1-3).
2. VS Code Remote-SSH-Extension auf jedem Operator-Mac installieren.
3. Pro Operator System-User auf dem VPS (analog Szenario 3 Schritte 2-3).
4. Claude Code CLI auf dem VPS installieren — Operatoren starten `claude` ueber die Remote-SSH-Session.
5. Geteilten Backlog in Linear oder GitHub Issues anlegen — alle Operatoren arbeiten gegen dasselbe Backlog.
6. Secrets pro Operator in `~/.claude/.env` auf dem VPS, **nicht** in geteilten Verzeichnissen.
7. Optional: Syncthing fuer Datei-Sync zwischen Macs und VPS einsetzen, wenn Operator-Daten lokal vorgehalten werden muessen (Operator waehlt aus).
8. Backup wie Szenario 3 (VPS-Snapshot plus pro Home).

**Skill-Installation**

- Wie Szenario 3 — entweder global unter `/opt/claude/skills/` oder pro User.
- Bei kleinen Teams (2-3 Operatoren) reicht oft Variante B (pro User), weil Drift-Risiko kleiner ist.

**Secrets-Trennung**

- Pro Operator in `~/.claude/.env` auf dem VPS.
- Keine Mac-`.env` in den VPS-Workflow uebertragen.
- Optional: Secrets-Vault des Operators (z.B. <Secret-Vault-Tool deiner Wahl>) — Framework setzt nichts voraus.

**Backup-Strategie**

- VPS-Snapshot beim Provider (taeglich).
- Plus Hetzner Storage Box oder Backblaze B2 fuer Home-Verzeichnisse.
- Mac-seitig: Time Machine deckt lokalen State ab, falls Operatoren lokal arbeiten.

**Tradeoffs**

- Komplex im Setup: SSH-Hardening, Remote-Extension, geteilter Backlog, Secrets-Disziplin.
- Brauchbar nur bei verteiltem Team mit gemeinsamem Code-Hub — fuer Solo-Setups Overkill.
- LLM-Latenz haengt vom VPS-Standort ab, nicht vom Operator-Standort.

### Bootstrap-Frage A.7 (BOO-70)

Im `/bootstrap` Phase A wird genau eine Frage zum Deployment-Szenario gestellt:

```
A.7 Deployment-Szenario:
  a) Solo-Mac (Default)
  b) anders → siehe HANDBUCH Anhang P
```

Bei `a)` laeuft der bestehende Bootstrap-Pfad unveraendert weiter. Bei `b)` gibt der Bootstrap nur einen Hinweis-Block aus, der auf diesen Anhang verweist — **kein** Interview-Fork, **kein** szenarienspezifischer Setup-Code im Bootstrap-Skill. Operator setzt sein Szenario manuell anhand der Schritte in der jeweiligen Sektion auf.

### Verwandte Anhaenge

- **Anhang I (Self-Hosted Runner):** Wer Szenario 2-4 nutzt, kann auf demselben VPS auch einen Self-Hosted CI-Runner betreiben — Sizing-Hinweise in Anhang I.
- **Anhang F (Hermes Compound-Layer):** Hermes-Routing funktioniert in allen Szenarien identisch, weil es auf Skill-Ebene wirkt, nicht auf Deployment-Ebene.
- **Anhang O (Privacy by Design):** Bei DSGVO-pflichtigen Projekten in Szenario 2-4 EU-Standort fuer den VPS waehlen — Anhang O liefert die Rechtsgrundlagen-Sicht.
- **Anhang Q (Souveraenitaets-Stack-Guide):** Inspirations-Schicht fuer EU-konforme Provider-Alternativen, falls Datensouveraenitaet ein expliziter Treiber ist.

Basiert auf BOO-9 (VPS-Rollout) und BOO-83 (VPS-Multi-User-Pattern).
## Anhang Q: Souveraenitaets-Stack-Guide + LLM-Proxy-Hook (BOO-71)

Code-Crash-Operatoren arbeiten zunehmend in regulierten Branchen — FINMA, BaFin, MaRisk, NIS-2-Pflichtsektoren, Behoerden-Auftraege. In diesen Kontexten ist die Default-Stack-Zusammensetzung (GitHub, Anthropic USA, iCloud) nicht souveraenitaetskonform, und ein Auditor fragt frueher oder spaeter nach EU-Alternativen. Dieser Anhang ist die **Inspirations-Schicht** des Frameworks: eine kuratierte Tabelle EU-konformer Komponenten plus ein einziger Hook-Punkt (`llm_proxy_url`) fuer Operator-seitige Anonymisierungs- oder Routing-Proxys. **Keine Anonymisierungs-Engine im Framework selbst** — das ist Runtime-Infrastruktur und gehoert in die Hand des Operators.

![Souveraenitaets-Stack — US-Default vs. EU-Alternative pro Komponente, plus optionaler LLM-Proxy-Hook](docs/assets/boo-71-sovereignty-stack.png)

### Wann lohnt der Souveraenitaets-Switch?

Nicht jedes Projekt braucht einen souveraenen Stack. Diese Decision-Matrix gibt eine ehrliche Orientierung — bei Unsicherheit auf das strengste zutreffende Kriterium ausrichten.

| Trigger | Souveraenitaets-Switch noetig? | Begruendung |
|---------|--------------------------------|-------------|
| Regulierte Branche (FINMA / BaFin / MaRisk) | Ja | Aufsichtsrechtliche Anforderung an Datenstandort und Auslagerungs-Kette; US-Cloud meist nur mit Sonderpruefung. |
| Behoerden-Auftrag (Bund / Land / Kanton) | Ja | Vergaberecht und IT-Grundschutz fordern in der Regel EU-Standort und EU-Vertragspartner. |
| NIS-2-Pflichtsektor (Energie, Transport, Gesundheit, Wasser, Digital) | Ja | NIS-2 verlangt Kontrolle ueber kritische Lieferkette inkl. LLM- und Code-Hosting-Anbieter. |
| Personenbezogene Daten Tier 3 (Gesundheit, Finanz, Strafregister) | Ja | Hoechste DSGVO-Risikoklasse; CLOUD-Act-Exposure ist Audit-Befund. |
| Schweizer Kundenmandat mit nDSG-Pflicht | Ja | nDSG verlangt nachweisbare Datenstandort-Kontrolle und EU/CH-Vertragspartner. |
| Solo-Tool ohne EU-Bezug | Nein | Default-Stack ist okay; Souveraenitaet wuerde Friction ohne Gegenwert hinzufuegen. |
| Code-Crash-Lite-Setup fuer Hobby-Projekte | Nein | Lernkurve und Operator-Aufwand stehen in keinem Verhaeltnis; Default bleibt. |

### EU-konforme Alternativen pro Stack-Komponente

Die folgende Tabelle ist die Kurz-Uebersicht. Pro Komponente folgt unten je eine eigene Sektion mit kurzer Migrations-Anleitung und Hinweis auf die jeweilige offizielle Doku — keine Voll-Setup-Guides, sondern Sprungbrett-Material.

| Komponente | US-Default | EU-Alternative | Tradeoff / Hinweis |
|-----------|------------|----------------|--------------------|
| Code-Hosting | GitHub | Codeberg (Forgejo) oder GitLab Self-hosted | Codeberg ist genossenschaftlich, gemeinnuetzig; GitLab Self-hosted braucht eigene Wartung. |
| Vault-Sync | iCloud oder Obsidian Sync | Syncthing oder Hetzner Storage Box mit Git-Sync | Syncthing ist Peer-to-Peer und braucht laufende Geraete; Storage Box plus Git-Sync ist robuster, aber manueller. |
| LLM-Endpoint | Anthropic API (USA) oder OpenAI (USA) | Mistral La Plateforme (EU), AWS Bedrock Frankfurt (mit CLOUD-Act-Restrisiko), Ollama lokal | Mistral ist EU-Vertragspartner; Bedrock Frankfurt bleibt US-Konzern mit CLOUD-Act-Exposure; Ollama lokal verschiebt Kosten auf Hardware. |
| Issue-Tracker | Linear | Plane (self-hosted) oder GitLab Issues | Plane ist Linear-aehnliche UX, Self-Hosting noetig; GitLab Issues sind weniger schlank, aber mit GitLab-Hosting integriert. |
| CI / Build | GitHub Actions | Forgejo Actions oder Drone CI auf Hetzner | Forgejo Actions sind GitHub-Actions-kompatibel; Drone CI ist leichter und vom Forge entkoppelt. |

### Code-Hosting: GitHub → Codeberg / GitLab Self-hosted

**Migrations-Anleitung**

1. Codeberg- oder GitLab-Account anlegen (bei Self-hosted: GitLab-Server auf EU-VPS installieren, siehe Anhang P).
2. Repo via `git push --mirror` auf den neuen Remote spiegeln.
3. CI-Workflows pruefen — GitHub Actions laufen nicht 1:1 auf Codeberg/Forgejo (siehe Sektion CI weiter unten).
4. Teamberechtigungen und Secrets im neuen Forge erneut einrichten — keine `.env`-Inhalte uebernehmen.
5. Im Bootstrap-Interview `git_provider`-Frage entsprechend setzen; Linear-Github-Bridge gegebenenfalls deaktivieren.

**Externe Doku**

- Offizielle Codeberg-Doku konsultieren (Operator beschafft selbst).
- Offizielle GitLab-Self-Hosted-Doku konsultieren (Operator beschafft selbst).

### Vault-Sync: iCloud / Obsidian Sync → Syncthing / Hetzner Storage Box + Git-Sync

**Migrations-Anleitung**

1. Vault als Git-Repo initialisieren, falls noch nicht geschehen.
2. Syncthing auf allen Geraeten installieren oder Storage-Box-Mount via SSHFS einrichten.
3. iCloud-Sync fuer den Vault-Ordner explizit deaktivieren (sonst Race-Conditions).
4. Bei Storage-Box-Variante: Cron-Job fuer regelmaessigen Git-Commit und -Push einrichten.
5. Backup-Strategie wie in Anhang P — Storage Box deckt Operator-State, Git-Remote deckt Code-Stand.

**Externe Doku**

- Offizielle Syncthing-Doku konsultieren (Operator beschafft selbst).
- Hetzner-Storage-Box-Doku konsultieren (Operator beschafft selbst).

### LLM-Endpoint: Anthropic / OpenAI USA → Mistral La Plateforme / AWS Bedrock Frankfurt / Ollama

**Migrations-Anleitung**

1. EU-Endpoint-Vertragspartner waehlen — Mistral La Plateforme (EU-Vertragspartner) oder AWS Bedrock Frankfurt (CLOUD-Act-Restrisiko explizit dokumentieren).
2. Alternativ Ollama lokal aufsetzen, wenn keine Cloud akzeptabel ist; Hardware-Anforderungen pruefen.
3. Modell-Tier-Mapping in `bootstrap/references/model-tiers.json` anpassen — andere Provider haben andere Tier-Namen und Preise.
4. Cost-Tracking in `meta.json.token_tracking` validieren — Provider-Wechsel veraendert Token-Preise; Operator prueft die aktuelle Preisliste des neuen Providers.
5. Bei sensiblen Daten zusaetzlich `llm_proxy_url` setzen, um Anonymisierung vor dem Provider zu schalten (siehe naechste Sektion).

**Externe Doku**

- Offizielle Mistral-La-Plateforme-Doku konsultieren (Operator beschafft selbst).
- AWS-Bedrock-Doku fuer Frankfurt-Region konsultieren (Operator beschafft selbst).
- Offizielle Ollama-Doku konsultieren (Operator beschafft selbst).

### Issue-Tracker: Linear → Plane / GitLab Issues

**Migrations-Anleitung**

1. Plane (self-hosted) auf EU-VPS deployen oder GitLab Issues im bereits migrierten GitLab nutzen.
2. Bestehende Linear-Issues exportieren (CSV oder API) und in den neuen Tracker importieren.
3. Backlog-Tool im `/bootstrap` umstellen — Skill `backlog` unterstuetzt verschiedene Tools per Konfiguration.
4. Webhook- und Bot-Integrationen neu einrichten (Linear-spezifische Automatisierungen sind nicht portabel).
5. Action-Items aus Meeting-Skills pruefen — Trigger-Logik bleibt, Endpunkt aendert sich.

**Externe Doku**

- Offizielle Plane-Doku konsultieren (Operator beschafft selbst).
- Offizielle GitLab-Issues-Doku konsultieren (Operator beschafft selbst).

### CI / Build: GitHub Actions → Forgejo Actions / Drone CI

**Migrations-Anleitung**

1. CI-Provider waehlen — Forgejo Actions wenn auf Codeberg/Forgejo gewechselt wurde, Drone CI fuer entkoppelten Runner.
2. Workflow-Definitionen pruefen — Forgejo Actions ist groesstenteils GitHub-Actions-kompatibel, aber nicht alle Marketplace-Actions sind portiert.
3. Self-Hosted Runner aufsetzen (siehe Anhang I) — Sizing wie dort beschrieben.
4. Secrets im neuen CI hinterlegen, nicht aus GitHub-Actions-Secrets uebernehmen.
5. Coverage- und Lint-Gates aus `CONVENTIONS.md` gegen den neuen Runner verifizieren.

**Externe Doku**

- Offizielle Forgejo-Actions-Doku konsultieren (Operator beschafft selbst).
- Offizielle Drone-CI-Doku konsultieren (Operator beschafft selbst).

### LLM-Proxy-Hook (`llm_proxy_url`)

Das Framework bietet **einen** konfigurierbaren Hook-Punkt fuer Operator-seitige Proxy-Loesungen: das optionale Feld `llm_proxy_url` in `.claude/environment.json`. Default ist `null` — das bedeutet direkter LLM-Call wie bisher. Setzt der Operator einen Wert, dann ist dieser Wert ein HTTP-Endpunkt eines selbst betriebenen Proxy-Servers, der Anonymisierung, Logging oder Souveraenitaets-Routing macht. **Das Framework setzt das Routing NICHT um** — es liest das Feld, protokolliert es in `meta.json.llm_routing` als Audit-Spur und ueberlaesst dem Operator die Proxy-Implementierung.

**Schema-Snippet `environment.json`**

```json
{
  "llm_proxy_url": "http://localhost:8000"
}
```

Default-Wert: `null`. Erlaubt sind beliebige HTTP- oder HTTPS-Endpunkte, die der Operator erreichbar haelt.

**Beispiel-Use-Case: Anonymisierungs-Proxy mit Microsoft Presidio**

Ein typisches Setup: der Proxy nimmt den ausgehenden Prompt entgegen, identifiziert per Microsoft Presidio personenbezogene Entitaeten (Namen, E-Mails, IBANs), ersetzt sie durch deterministische Tokens und leitet den anonymisierten Prompt an den eigentlichen LLM-Endpoint weiter. Die Response wird beim Rueckweg vom selben Proxy demaskiert. So sieht der LLM-Provider nie Klartext-PII, das Skill-Verhalten bleibt unveraendert. Alternativen sind genauso valide — Operator kann statt Microsoft Presidio auch spaCy, eine eigene Lambda-Funktion oder einen anderen Proxy nutzen. Das Framework macht hier keine Vorgabe.

> **Designentscheid:** Anonymisierung ist Runtime-Infrastruktur, nicht Framework-Aufgabe. Code-Crash bietet den Hook-Punkt und den Audit-Trail — nicht mehr.

### Bootstrap-Verhalten

Bootstrap aendert sich durch BOO-71 **nicht** — kein neuer Interview-Schritt, keine neue Pflicht-Frage. `llm_proxy_url` ist ein Power-User-Feld, der Operator setzt es manuell in `.claude/environment.json` nach dem Bootstrap-Lauf. Fuer Bestands-Projekte fuegt das Migrations-Skript `migrate_boo_71()` das Feld idempotent mit Default `null` in die `environment.json` ein. Wer den Stack souveraen haben will, aber den Proxy noch nicht braucht, kann das Feld leer lassen und spaeter einschalten.

### Privacy ≠ Souveraenitaet

Datensouveraenitaet (US-vs-EU-Cloud-Anbieter) und Privacy-by-Design sind **orthogonale** Themen und ersetzen sich nicht gegenseitig. Ein souveraener Stack mit EU-Hosting befreit nicht von DSGVO-Pflichten — Rechtsgrundlagen, Verarbeitungsverzeichnis, Loeschkonzept und Betroffenenrechte gelten unabhaengig vom Hosting-Standort. Umgekehrt schuetzt ein DSGVO-konformer Default-Stack auf US-Cloud nicht vor CLOUD-Act-Zugriffen oder Behoerden-Vergaberecht. Operatoren mit beiden Anforderungen aktivieren das Privacy-Add-on (siehe Anhang O) **und** waehlen ihre Stack-Komponenten gemaess diesem Anhang Q.

### Verwandte Anhaenge

- **Anhang N (Token-Effizienz, BOO-84):** `llm_proxy_url` und `model_overrides:` koennen konzeptionell in derselben CLAUDE.md-Sektion stehen — beide adressieren Operator-Wahl auf LLM-Ebene.
- **Anhang O (Privacy by Design, BOO-69):** DSGVO/nDSG-Pflicht greift unabhaengig vom Hosting-Standort; Privacy-Add-on und Souveraenitaets-Stack sind orthogonal kombinierbar.
- **Anhang P (Deployment-Szenarien, BOO-70):** EU-VPS-Standort ist Voraussetzung fuer einen souveraenen Stack — Szenarien 2-4 in Anhang P sind die natuerliche Heimat fuer Anhang Q.
- **Anhang F (Hermes Compound-Layer):** Hermes-Routing aendert sich nicht durch einen Proxy — der Compound-Layer wirkt vor dem LLM-Call und ist unabhaengig vom Endpunkt.

Spec: BOO-71. Operator-Feedback Martin 2026-05-27.

## Anhang R: Multi-Operator-Koordination — 5 bis 20+ Operatoren (BOO-72)

Anhang P (BOO-70) beschreibt vier Deployment-Szenarien, davon Szenario 4 fuer **2-5 Operatoren** mit gemeinsamem Coding-Server. Aber was passiert, wenn ein Beratungsmandat mit zehn Personen Code-Crash adoptiert? Wenn ein Inhouse-Team mit zwanzig Entwicklern parallel im selben Repo arbeitet? Dieser Anhang ist die **Inspirations-Schicht** fuer Operator-Teams jenseits der Solo- und Kleinteam-Setups. Er fuegt **keinen** neuen Skill hinzu, **keine** neue Bootstrap-Frage und **keine** Framework-Konvention — er zeigt nur, wie die bestehenden Gates aus Wave A-K im groesseren Team gelebt werden.

![Multi-Operator-Koordination — 3-Layer-Modell](docs/assets/boo-72-multi-operator-3-layer.png)

### Die Operator-Frage hinter Anhang R

> Wenn 20 Entwickler gleichzeitig im selben GitHub-Repo arbeiten und sich Doku aus Obsidian (oder Jira/Confluence/Notion) holen — funktioniert das Framework dann noch? Stellt das Framework sicher, dass mehrere Leute parallel arbeiten koennen, oder muss der Operator das selbst loesen?

Die ehrliche Antwort: **teilweise gedeckt, teilweise Operator-Disziplin.** Anhang R trennt die Frage in drei Layer und beantwortet pro Layer "was skaliert nativ", "was nicht", "welche Optionen hat der Operator".

### Das 3-Layer-Modell

#### Layer 1 — Code-Layer (Git/GitHub)

**Was skaliert nativ:** Git ist fuer Multi-User-Concurrency gebaut. Branches, PRs, Merge-Konflikt-Resolution, Branch-Protection (BOO-29) und Spec-Gate (BOO-4 + BOO-27) sind team-tauglich ohne Framework-Ergaenzung. Der Code-Layer macht zwischen Solo-Operator und 20-Personen-Team konzeptionell **keinen** Unterschied — nur die Frequenz der Konflikte aendert sich.

**Was nicht:** wenn Operatoren direkt auf `main` pushen, Spec-Gate umgehen oder PRs ohne Review mergen, kollabiert die Governance. Das sind aber keine Framework-Luecken, sondern Team-Disziplin-Themen.

**Pattern-Optionen (Branch-Strategie):**

| Strategie | Wann sinnvoll | Tradeoff |
|---|---|---|
| **Trunk-Based Development** | kleine Stories (max 1-2 Tage pro Branch), hohe Release-Frequenz, Feature-Flags fuer "noch nicht fertig"-Code | Disziplin-Pflicht: Branches duerfen NICHT lange leben, sonst Merge-Hoelle |
| **Feature-Branches mit PR-Review** | Standard heute, robust fuer 5-15 Operatoren, jede Story ein Branch | Branches koennen lange leben → Merge-Konflikte mit `main` steigen |
| **GitFlow** | Releases-getriebene Branchen (`develop`, `release/*`, `hotfix/*` neben `main`), audit-pflichtige Regulatorik | Komplex, mehr Branches zu verwalten, langsamer Release-Zyklus |

**Empfehlung pro Team-Groesse:**

- 5-10 Operatoren: Feature-Branches reichen.
- 10-20: Trunk-Based wenn schnelle Release-Frequenz, sonst Feature-Branches mit verbindlichem PR-Reviewer-Pool.
- 20+: GitFlow wenn Audit-Pflicht, sonst Trunk-Based mit CODEOWNERS-Disziplin.

**CODEOWNERS-Pattern (Beispiel):** Pflicht ab 10 Operatoren, sehr empfohlen ab 5. Datei `.github/CODEOWNERS` mit Datei-Pattern → Sub-Team-Mapping. GitHub erzwingt dann, dass jeder PR mindestens 1 Reviewer aus dem zustaendigen Sub-Team hat (in Kombination mit Branch-Protection):

```text
# Kritische Governance-Dokumente brauchen Architekt-Approval
/SECURITY.md            @owlist/sec-leads
/PRIVACY.md             @owlist/legal-leads
/ARCHITECTURE_DESIGN.md @owlist/arch-leads
/CONVENTIONS.md         @owlist/arch-leads

# Domain-spezifische Code-Bereiche
/src/api/**             @owlist/backend
/src/ui/**              @owlist/frontend
/src/auth/**            @owlist/sec-leads @owlist/backend
/infra/**               @owlist/devops

# Doku im Repo
/docs/api/**            @owlist/backend
/docs/ui/**             @owlist/frontend
```

Wichtig: CODEOWNERS ersetzt nicht das Spec-Gate — beide wirken parallel.

#### Layer 2 — Koordinations-Layer (Wer macht was?)

**Was skaliert nativ:** Linear / Jira / GitHub Issues / Azure DevOps / MS Planner haben Workflow-States (`Backlog → In Progress → In Review → Done`). Bootstrap-Frage B.4 deckt die Backlog-Adapter-Wahl ab (BOO-54). "In Progress" pro Issue signalisiert "diese Story ist belegt" — genau die Mechanik, die Sub-Agents in BOO-52 (Execution-Isolation) auf Maschinen-Ebene macht, hier auf Operator-Ebene.

**Was nicht:** das Issue-Tracker-Tool selbst loest nicht "wer entscheidet bei Konflikten an `SECURITY.md`?". Auch "welcher Operator arbeitet an welchem Modul?" ist Team-Organisation, nicht Tool-Sache.

**Pattern-Optionen (Team-Topologien):**

| Topologie | Wann sinnvoll | Tradeoff |
|---|---|---|
| **Pool-Modell** | jeder Operator zieht naechstes Issue aus gemeinsamem Backlog, kein fester Modul-Owner | Hohe Flexibilitaet, niedrige Spezialisierung — bei 15+ Personen wird "wer kennt sich hier aus?" zum Engpass |
| **Squad-Modell** | 3-5 Operatoren pro Modul/Domaene, Squad-Lead entscheidet Cross-Story-Themen | Klar verteilte Verantwortung, Risiko der Squad-Silos — Cross-Squad-Themen brauchen Koordination |
| **Hybrid** | Pool fuer kleine Stories (Bug-Fixes, Refactorings), Squad fuer kritische Pfade (SECURITY/PRIVACY/ARCHITECTURE_DESIGN) | Beste Anpassung an reale Operator-Faehigkeiten, Setup-Aufwand hoeher |

**Empfehlung pro Team-Groesse:**

- 5-10: Pool reicht. Cross-Story-Themen klaert man im Daily-Standup.
- 10-20: Hybrid mit Squad-Owner pro kritischem Pfad (SECURITY, PRIVACY, ARCHITECTURE_DESIGN, ggf. Performance + Observability).
- 20+: Squad-Modell mit Lead-Architekt-Rolle. Lead-Architekt arbeitet Cross-Squad-Themen mit den Squad-Leads aus, hat Veto-Recht bei Architektur-Aenderungen.

**Konkretes Beispiel — 15-Personen-Team mit Hybrid-Topologie:**

- 1 Lead-Architekt (Cross-Squad)
- 3 Squads à 4-5 Operatoren: Backend / Frontend / DevOps
- 1 Sec-Lead (Cross-Squad, owned `SECURITY.md` + `sensitive-paths.json`)
- 1 Legal-Lead (Cross-Squad, owned `PRIVACY.md` + `personal-data-paths.json` + DPO-Skill-Audits)
- Daily-Standup pro Squad (15 Min), Weekly Cross-Squad-Sync (30 Min)
- Backlog in Linear, alle Stories haben `team` als Custom-Field gefuellt

#### Layer 3 — Doku-Layer (Single Source of Truth)

Dieser Layer ist der eigentliche Drift-Punkt im Team. Code-Konflikte loest Git, Issue-Konflikte loest der Workflow-State — aber Doku-Konflikte sind semantisch und brauchen menschliche Entscheidung. Genau dafuer fragt Bootstrap-Frage B.3 die Doku-SSoT ab — die Wahl ist team-kritisch.

**Doku-SSoT-Wahl-Matrix pro Team-Groesse:**

| SSoT | Solo (1) | Klein (2-5) | Mittel (5-10) | Gross (10-20+) | Hauptgrund |
|---|---|---|---|---|---|
| **Obsidian Vault (lokal)** | ✅ | ⚠ | ❌ | ❌ | Solo-Tool, kein semantischer Multi-User-Lock |
| **Obsidian + Git-Sync auf den Vault** | ✅ | ⚠ | ❌ | ❌ | Sync-Konflikte werden manuell — bei 5+ Personen zu teuer; Obsidian-Sync-Tool fuer Binaer-Dateien nicht fuer semantischen Merge geeignet |
| **Obsidian Sync (kostenpflichtig, official)** | ✅ | ✅ | ⚠ | ❌ | Loest technische Sync-Konflikte, nicht semantische ("zwei Personen aendern dieselbe Notiz gleichzeitig") |
| **`docs/project/` im Repo (Markdown)** | ✅ | ✅ | ✅ | ✅ | Selbe Git-Mechanik wie Code: PR-Review fuer Doku, Branch-Protection, CODEOWNERS-Pattern |
| **Confluence** | ⚠ | ✅ | ✅ | ✅ | Externes Tool mit eigenen Multi-User-Permissions, kein Git-Bezug, gut fuer Enterprise mit existierender Confluence-Lizenz |
| **Notion** | ⚠ | ✅ | ✅ | ✅ | Externes Tool, eigene Multi-User-Logik, Versions-Historie pro Page |
| **SharePoint** | ⚠ | ⚠ | ✅ | ✅ | Externes Tool, gut fuer regulierte Enterprises mit Office-365-Footprint, Permission-Granularitaet hoch |

**Empfehlung:**

- 1 Operator: Obsidian (persoenliches Vault + Index)
- 2-5: Obsidian Sync oder Repo-Docs — abhaengig vom Operator-Profil. Wenn alle Operatoren technisch sind: Repo-Docs. Wenn gemischt: Obsidian Sync.
- 5+: Repo-Docs (`docs/project/`) **oder** externes DMS (Confluence/Notion/SharePoint). Obsidian wird zum **persoenlichen** Brainstorming-Tool, nicht zur Team-SSoT.

**Wichtig:** Bootstrap-Frage B.3 setzt `DOCUMENTATION_SSOT.path` einmalig pro Projekt. Eine Migration der SSoT mid-flight ist teuer (Verlinkungs-Drift, History-Verlust) — die Wahl sollte vor dem ersten echten Inhalt getroffen werden.

### Vier-Augen-Konvention fuer Sensitive-Paths und Personal-Data-Paths

Im Solo-Setup setzt der Operator `review-ok` (Sensitive-Paths-Gate, BOO-18) oder `privacy-ok` (Personal-Data-Paths-Gate, BOO-69) selbst — Self-Approval ist akzeptabel, weil es niemanden anderen gibt. **Im Team ist Self-Approval ein Audit-Risiko.** Anhang R empfiehlt die **Vier-Augen-Konvention:**

- Der Operator, der die Aenderung an einem sensitiven oder personal-data-Pfad macht, darf **nicht** der gleiche sein, der `review-ok` oder `privacy-ok` setzt.
- Im PR-Review setzt ein **anderer** Operator (Sec-Lead, Legal-Lead, oder explizit benannter Reviewer) das Gate-Token.
- Der Audit-Trail laeuft ueber `git log` und `git blame` — wer das Gate gesetzt hat, ist im Commit-Author sichtbar.

Beispiel-Audit-Spur:

```bash
$ git log --oneline -5 -- src/auth/jwt.go
a3f1d22 review-ok: jwt rotation reviewed by @sec-lead (closes BOO-XYZ)
e8b227a feat: rotate jwt signing key every 24h (BOO-XYZ)
$ git log --format='%H %an' a3f1d22 e8b227a
a3f1d22 Sec Lead          # review-ok von anderer Person
e8b227a Backend Operator  # eigentliche Aenderung
```

**Wichtig:** Das Framework **erzwingt** die Vier-Augen-Konvention heute nicht — es waere theoretisch im Sensitive-Paths-Gate prueffbar (Author des Gate-Commits != Author der Aenderung), wuerde aber Framework-Komplexitaet erhoehen und Audit-Werkzeuge wie `git blame` parallel bedienen. Anhang R dokumentiert die Konvention als Operator-Disziplin, BOO-72 schliesst Enforcement explizit aus.

### Skill-Pool-Governance im Team

Anhang P Szenario 3 (Multi-User-VPS) hatte schon zwei Skill-Pool-Optionen: global unter `/opt/claude/skills/` (read-only fuer User) oder pro User in `~/.claude/skills/` (eigene Kopie). Bei 10-20 Operatoren reicht das nicht — es braucht eine **Wartungs-Owner-Rolle**:

- **Wartungs-Owner** (1 Person, ggf. Lead-Architekt oder DevOps): pflegt den globalen Skill-Pool. Updates via `git pull` als root oder via dediziertem Service-Account. Pro Skill-Version-Bump: Changelog-Eintrag, kurze Operator-Mail/Slack.
- **User-Sicht:** Operatoren rufen Skills via `~/.claude/skills/`-Symlinks auf `/opt/claude/skills/` auf. Bei Drift (lokaler Operator hat eigenen Skill-Stand): Wartungs-Owner setzt regelmaessig Audit per `jq` auf `~/.claude/settings.json` der User.
- **Skill-Quarantaene:** neue Skills aus externen Quellen werden vom Wartungs-Owner via `security-architect --mode SKILL-SCAN` geprueft, bevor sie in `/opt/claude/skills/` landen.

Bei Hybrid-Pool (mancher Skill global, mancher pro User): die Entscheidung muss in `CONVENTIONS.md` dokumentiert sein, sonst weiss niemand mehr, welche Variante gilt.

### Konflikt-Eskalation bei kritischen Governance-Pfaden

Was passiert, wenn zwei Operatoren widerspruechliche Aenderungen an `SECURITY.md`, `PRIVACY.md` oder `ARCHITECTURE_DESIGN.md` mergen wollen? Anhang R empfiehlt **drei Eskalations-Stufen:**

1. **CODEOWNERS-Owner entscheidet** — wer in der CODEOWNERS-Datei fuer den Pfad eingetragen ist, hat das letzte Wort. In den meisten Faellen reicht das.
2. **Squad-Lead-Vermittlung** — wenn zwei CODEOWNERS-Personen uneinig sind (z.B. Sec-Lead vs. Backend-Lead bei `src/auth/`), vermittelt der Squad-Lead des betroffenen Moduls.
3. **Lead-Architekt-Veto** — Cross-Squad-Themen oder Architektur-Aenderungen mit System-Impact eskaliert der Squad-Lead an den Lead-Architekten. Lead-Architekt hat Veto, dokumentiert die Entscheidung in `Decisions/ADR-XX.md`.

Wichtig: Eskalation ist eine Konvention, kein Framework-Mechanismus. Sie funktioniert nur, wenn das Team sie aktiv lebt. Anhang R ist Inspiration — wie das Team die Rollen besetzt, ist Team-Sache.

### Wie setzt man Code-Crash in einem 20-koepfigen Team auf?

Konkrete 10-Schritte-Anleitung, die Anhang P Szenario 3 (Multi-User-VPS-Coding-Factory) erweitert:

1. **VPS-Setup** (Anhang P Szenario 3): VPS mit 1 System-User pro Operator, Skill-Pool global unter `/opt/claude/skills/` (read-only), Repository-Worktrees pro User in `~/projects/<projekt>/`, Wartungs-Owner-Rolle benannt.
2. **Bootstrap einmalig durch Lead-Architekt:** Frage B.3 = `docs/project/` im Repo **oder** Confluence/Notion. Frage B.4 = Linear oder Jira. Frage A.5 = `heavy` Governance. Frage A.7 = `b) anders` mit Verweis auf dieses Szenario.
3. **CODEOWNERS-Datei pflegen** (Beispiel siehe oben). Beim ersten Setup mit Lead-Architekt + Squad-Leads gemeinsam erarbeiten.
4. **Branch-Protection erweitert:** Required-Reviewer-Pool aus CODEOWNERS, Required-Status-Checks (Spec-Gate, Lint-Gate, Coverage-Gate, ggf. Security-Scan, ggf. DPO-Audit-Hook), `Dismiss stale reviews when new commits are pushed`, `Require linear history`.
5. **Vier-Augen-Konvention fuer Gates:** `privacy-ok` / `review-ok` darf NICHT der gleiche Operator setzen, der die Aenderung gemacht hat. Operator-Disziplin, im Audit-Log via `git blame` nachvollziehbar.
6. **Squad-Modell mit 3-5 Operatoren pro Modul** + 1 Lead-Architekt + 1 Sec-Lead + 1 Legal-Lead. Squad-Leads owned ihr Modul in CODEOWNERS, Sec/Legal-Leads owned die Governance-Pfade.
7. **Konflikt-Eskalation explizit dokumentieren** — in `CONVENTIONS.md` einen Abschnitt "Eskalations-Pfad" mit den drei Stufen oben. Ohne Schrift-Form vergisst das Team es bei Konflikten.
8. **Daily-Standup pro Squad (15 Min)** + Weekly Cross-Squad-Sync (30 Min). Backlog-Pflege wird mit jeder zweiten Standup-Welle gemacht, nicht ad-hoc.
9. **Wartungs-Owner-Rolle aktiv leben:** Skill-Pool-Updates aufschreiben, Drift-Audits regelmaessig (z.B. monatlich), Skill-Quarantaene bei externen Skills.
10. **Onboarding-Dokumentation** unter `DEVELOPER_ONBOARDING.md` pflegen — Anhang R explizit referenzieren, damit neue Operatoren das 3-Layer-Modell verstehen, bevor sie ihren ersten PR machen.

### Was Anhang R nicht macht

Klare Abgrenzung zur Code-Crash-Philosophie "leichtgewichtig + pragmatisch":

- **Kein neuer Skill.** Anhang R ist reine Doku.
- **Keine neue Bootstrap-Frage.** Bootstrap fragt Doku-SSoT (B.3) und Backlog-Adapter (B.4) schon ab — das reicht.
- **Keine Framework-Konvention "wer ist Lead-Architekt"** — das ist Team-Organisation.
- **Kein Vier-Augen-Enforcement im Sensitive-Paths-Gate.** Theoretisch moeglich (Author-Vergleich), bewusst NICHT umgesetzt — Operator-Disziplin bleibt Operator-Disziplin.
- **Keine "Best Practice"-Festlegung.** Pattern-Optionen sind Tradeoff-Tabellen, nicht Empfehlungs-Urteile.
- **Keine Provider-Empfehlung bei Confluence/Notion/SharePoint** — Operator waehlt aus.

### Verwandte Anhaenge

- **Anhang P (Deployment-Szenarien, BOO-70):** Szenario 3 (Multi-User-VPS-Coding-Factory) und Szenario 4 (Team-mit-Coding-Server) sind die infrastrukturelle Basis fuer Anhang R. Wer 20 Operatoren bedient, braucht VPS-Setup aus Szenario 3.
- **Anhang Q (Souveraenitaets-Stack, BOO-71):** orthogonal — ein 20-Personen-Team kann mit Default-Stack laufen oder mit EU-Stack. Souveraenitaets-Entscheidung ist Branchen-Frage, nicht Team-Groesse-Frage.
- **Anhang O (Privacy by Design, BOO-69):** im Team-Setup besonders wichtig — DPO-Skill-Audits via `/sprint-review` Schritt 7c werden mit zunehmender Operator-Anzahl wertvoller, weil mehr Code-Aenderungen pro Sprint durchlaufen.
- **Anhang N (Token-Effizienz, BOO-84):** bei 20 Operatoren mit je mehreren Stories pro Tag werden Token-Kosten zum FinOps-Thema. Model-Routing + Prompt-Caching sind dann nicht mehr Nice-to-have, sondern Cost-Hebel.
- **HANDBUCH §8d (Coding-Umgebungen):** technische Mac/VPS/CI-Unterscheidung, Voraussetzung fuer Anhang P Szenarien 2-4.

Spec: BOO-72. Operator-Frage Tobias 2026-05-27 nach Wave-K-Release. Sketch: [docs/assets/boo-72-multi-operator-3-layer.png](docs/assets/boo-72-multi-operator-3-layer.png).

---

*Dieses Handbuch ist Teil des Code-Crash Frameworks.*
*GitHub: github.com/vibercoder79/code-crash-framework*
*Letzte Aktualisierung: 2026-05-27 (Anhang O umgestellt auf DPO als Framework-Bundle-Skill — BOO-74, Wave M; Anhang R Multi-Operator-Koordination — BOO-72, Wave L)*
