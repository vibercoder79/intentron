# Bootstrap-Vorbereitung — die Fragen, die im `/bootstrap`-Interview kommen

> **Zweck.** Das Framework-Setup laeuft als gefuehrtes `/bootstrap`-Interview (~10 Min, 4 Bloecke A–D). Dieser Bogen listet die Fragen **vorab** — gib ihn der Kunden-IT mit dem Satz: *„Naechste Woche stelle ich dir im Bootstrapping-Prozess diese Fragen. Bitte sorg dafuer, dass ihr sie beantworten koennt."* So laeuft die Session zuegig und ohne Rueckholschleifen.
>
> Spiegelt 1:1 die echten Interview-Fragen (`bootstrap/SKILL.md` Block A–D). Den tieferen kundenindividuellen Integrations-/CI-Teil deckt der separate Bogen `docs/onboarding/integration-discovery.md` ab. Technische Voraussetzungen am Ende.

## Block A — Projekt-Kern (10 Fragen, ~4 Min)

1. **Stack.** Backend / Frontend / Full-Stack? Welche Sprache(n) und Framework(s)? — *Wer weiss das: Lead/Architekt.*
2. **Frontend-Performance (nur bei Frontend/Full-Stack).** Soll ein Lighthouse-CI-Performance-Budget gesetzt werden? — *Frontend-Lead.*
3. **Ziel-Runtime / KI-Tool.** Welches KI-Coding-Tool ist die Runtime: Claude Code, Codex, Cursor, Cross-Tool? — *Engineering-Lead.*
4. **Projekt-Identitaet.** Projektname? Ein-Satz-Beschreibung (was macht das System)? Start-Version (Default 0.1.0)?
5. **Backlog-Basics.** Issue-Prefix (z.B. `MA-`)? Primaere Doku-Sprache (de/en)?
6. **Backlog-Adapter.** Wo leben die Tickets: Linear / GitHub Issues / Jira / Azure DevOps Boards / Microsoft Planner / keines (Markdown-only)? — *PM/PO.*
7. **Add-ons.** Welche zusaetzlichen Dimensionen sind relevant: Privacy/DSGVO · Cost Efficiency · Signal Quality · Compliance (regulierte Branche) · **EU AI Act** (KI-Anteil mit Kundendaten)? — *DSGVO-/Compliance-Verantwortlicher.*
8. **Governance-Intensitaet.** lite / standard / heavy? (heavy = mehr Gates, Mandatory Review, Branch-Protection — fuer regulierte/kritische Systeme.) — *CTO/Lead.*
9. **Execution-Isolation.** Sollen parallele KI-Agenten in isolierten Git-Worktrees laufen? — *Engineering-Lead.*
10. **Deployment-Szenario.** Solo-Mac / Solo-VPS / Multi-User-VPS / Team-mit-Coding-Server? (Wo entwickelt das Team mit dem Framework.) — *IT/Infra.*

## Block B — Bestehende Infrastruktur (6 Fragen, ~4 Min)

1. **Projekt-Verzeichnis.** Existiert es (absoluter Pfad) oder neu anlegen (wo)?
2. **GitHub-Repo.** Vorhanden (URL)? Spaeter anlegen? Kein GitHub gewuenscht?
3. **Projekt-Dokumentations-SSoT.** Wo lebt die Projekt-Doku: Obsidian-Vault (Pfad) · Repo `docs/project/` · externes DMS (Notion/Confluence/SharePoint + URL) · noch unklar (Repo-Fallback) · Repo-Docs + persoenlicher Vault-Harvest (Team mit Obsidian)? — *zentrale Team-Entscheidung.*
4. **Backlog-System.** Konkretes Tool + Zugang: Linear (Team-Slug) / GitHub Issues (Repo) / Jira (Projekt-Key) / Azure DevOps (Projekt) / Planner (Plan) / keines.
5. **API-Keys.** Liegen Projekt-Keys schon in einer `.env`, oder reicht `.env.example` (Keys spaeter)? — *DevOps.*
6. **Developer-Uebergabe.** `Developer Onboarding`-Artefakt neu erzeugen + pflegen, oder nur auf bestehende Doku verlinken?

**Zusatz (Provider-Postflight):** Gibt es bereits eine **Monitoring-/Logging-Plattform** (zentral nutzen / neu vorbereiten / offen)? Soll der **Research-Skill** angebunden werden (Provider: Perplexity/OpenRouter/keiner)? **Visualisierung** via Miro (MCP vorhanden?) oder Fallback Excalidraw/Mermaid?

> **Hinweis Merge-Modus:** Enthaelt das Verzeichnis/Repo schon Dateien, fragt Bootstrap vor dem Ueberschreiben (Backup / nur fehlende Governance-Dateien ergaenzen / Abbruch).

## Block C — Doku-Architektur (Vorschlag + Review)

Bootstrap **schlaegt** auf Basis von Stack (A.1) und bestehender Infra (Block B) eine 3-Schichten-Doku-Architektur **vor**. Vorbereiten: *Wer auf Kundenseite entscheidet ueber die Doku-Struktur/-Ablage (gibt es Vorgaben, ein bestehendes Wiki/DMS, Namens-/Ablagekonventionen)?*

## Block D — Optional-Komponenten (Ja/Nein am Ende)

Gezielte Ja/Nein-Entscheidungen: **Self-Healing**, **DocSync**, **Daemon/Automation**, **Learning-Loop**. Vorbereiten: *Wuenscht ihr diese optionalen Automatismen — und gibt es betriebliche Einwaende (z.B. Automatisierung, die in eure Umgebung schreibt)?*

## Technische Voraussetzungen (vor der Session bereit)

- **Node.js v18+**, **Git**, ein KI-Coding-Tool (Claude Code als Referenz-Implementierung)
- Accounts/Zugaenge: KI-Tool (z.B. Anthropic), GitHub (falls genutzt), Backlog-Tool (falls genutzt)
- Absoluter Pfad fuers Projektverzeichnis; ggf. Repo-URL; ggf. Vault-/DMS-Pfad
- Details: HANDBUCH Anhang A (Checkliste) + §4 (Installation Schritt fuer Schritt)

> **Tieferer Integrations-Teil:** Wenn die gebaute Solution in eure Live-/Bestandsumgebung integriert werden soll (Hosting, eure CI/CD, Schnittstellen, Netz, Secrets, Compliance, Go-Live), nutzt zusaetzlich `docs/onboarding/integration-discovery.md`.
