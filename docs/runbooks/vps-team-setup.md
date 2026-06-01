# Runbook: INTENTRON auf einer Developer-VPS für Teams

> **Zweck:** Schritt-für-Schritt-Anleitung, um INTENTRON auf einer geteilten Entwickler-VPS aufzusetzen,
> mehrere Operatoren und mehrere Projekte zu betreiben und ein neues Projekt in Minuten governance-ready
> zu machen. Stand: 2026-06-01 (bootstrap 3.35, dpo 1.2, Vier-Layer-Quality-Gate, BOO-86–93).
>
> **Leitidee:** Vieles ist **einmal pro VPS** zu tun (Tools, Claude Code, Skill-Pool), der Rest ist
> **pro Projekt-Repo** (vor allem die Git-Hooks — `.git/` wird nicht geklont). Diese Trennung ist der rote
> Faden des Runbooks.
>
> **Vertiefung im HANDBUCH:** §8d (Coding-Umgebungen), Anhang P (Deployment-Szenarien), Q (Souveränität),
> R (Multi-Operator), S (Skill-Installation), T (Post-Install-Verifikation), U (Multi-Projekt-Betrieb),
> V (Layer-0-Bodyguard). Dieses Runbook bündelt diese Anhänge zu einem durchgehenden Ablauf.

---

## 0. Zielbild & Voraussetzungen

### 0.1 Welches Deployment-Szenario? (HANDBUCH Anhang P)

| Szenario | Wer | Skill-Pool | Wann |
|---|---|---|---|
| **2 — Solo-VPS** | 1 Operator, 24/7-Background/Mobile | `~/.claude/skills/` | Einzelperson, mehrere Projekte |
| **3 — Multi-User-Factory** | 5+ Operatoren, je eigener System-User | `/opt/claude/skills/` (read-only) | Größeres Dev-Team auf einer VPS |
| **4 — Team-mit-Coding-Server** | 2–5 Operatoren, Mac-Frontend + VPS-Backend | System-Pool oder pro-Projekt | Team, das per VS Code Remote-SSH arbeitet |

Dieses Runbook deckt **Szenario 3/4** (Team-VPS) ab und nennt Solo-VPS-Abweichungen, wo relevant.

### 0.2 VPS-Sizing

- **Daumenwert (Anhang P, Szenario 3):** ≥ **8 GB RAM + 4 vCPU** für ~5 parallele Operatoren. Linear hochskalieren.
- Distribution: **Debian/Ubuntu** (apt-basiert; das Container-Profil basiert auf `debian`). EU-Standort wählen, falls Souveränität ein Thema ist (Anhang Q).

### 0.3 Software-Voraussetzungen (Pflicht + faktisch gebraucht)

| Pflicht (HANDBUCH §3) | Faktisch zusätzlich gebraucht |
|---|---|
| Node.js **v18+** + npm | `gh` (GitHub CLI, für Branch-Protection/CI) |
| Git | `jq` (environment.json/Healthchecks — optional, Skills lesen notfalls per grep/sed) |
| Claude Code CLI | `bash 4+` (Linux-VPS erfüllen das; nur macOS-Standard 3.2 nicht — auf dem VPS kein Thema) |
| | `python3` (Stdlib genügt — dpo-Audit, vault-sync, raw-pii-guard sind dependency-frei) |

> **Hinweis:** `gh`, `git`, `jq` stehen nicht in der §3-Pflichtliste des HANDBUCHs, werden aber für
> Branch-Protection, Self-Hosted-Runner-Healthchecks und environment.json-Queries real gebraucht. Dieses
> Runbook führt sie als Prereq.

---

## 1. EINMAL pro VPS (Maschinen-Setup)

Diese Schritte macht der **VPS-Owner einmal**. Sie gelten für alle Operatoren und alle Projekte.

### 1.1 VPS härten

```bash
# SSH-Key-Login einrichten, dann Passwort-Login deaktivieren
sudo sed -i 's/^#\?PasswordAuthentication.*/PasswordAuthentication no/' /etc/ssh/sshd_config
sudo systemctl reload ssh
# Bei Multi-User: restriktive umask global
echo 'umask 077' | sudo tee -a /etc/profile
```

### 1.2 Toolchain installieren

> Es gibt **kein** zentrales Install-Script im Framework — die folgende Sequenz ist aus dem
> Container-Profil-Dockerfile (`bootstrap/references/devcontainer/Dockerfile`) für einen frischen
> Debian/Ubuntu-VPS abgeleitet. Alternativ → **Container-Weg** (Abschnitt 5.1).

```bash
# Basis
sudo apt-get update && sudo apt-get install -y git jq curl ca-certificates python3 python3-pip python3-venv pipx tmux

# Node.js LTS (z.B. via nodesource oder nvm) — Beispiel nvm:
curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.40.1/install.sh | bash
. ~/.nvm/nvm.sh && nvm install --lts

# System-Linter/SAST einmal global (isoliert via pipx / npm -g)
pipx install semgrep
pipx install ruff
npm install -g eslint
npm install -g @anthropic-ai/claude-code     # Claude Code CLI
# Optional: gh (GitHub CLI), SonarScanner — projekt-/teamabhängig
```

Welche Tools das Framework nutzt: **Semgrep, Ruff, ESLint** (System-Ebene), **SonarScanner** (optional, server-side
SonarQube Cloud), **pytest/Vitest + Coverage (c8/pytest-cov)** und **autocannon/pytest-benchmark** (Perf) als
Projekt-Dev-Deps. Verifiziert hart geprüft werden später nur `eslint` + `semgrep` (`verify-setup.sh`).

### 1.3 Operatoren anlegen (nur Szenario 3, Multi-User)

```bash
sudo useradd -m -s /bin/bash alice
sudo mkdir -p /home/alice/.ssh && echo "<alice-pubkey>" | sudo tee /home/alice/.ssh/authorized_keys
sudo chmod 700 /home/alice/.ssh && sudo chmod 600 /home/alice/.ssh/authorized_keys && sudo chown -R alice:alice /home/alice/.ssh
```

Secrets liegen **pro Operator** in `~/.claude/.env` (Mode 600), strikt getrennt. Niemals geteilte Keys.

### 1.4 Skill-Pool einrichten (HANDBUCH Anhang S)

| Szenario | Skill-Pool | Begründung |
|---|---|---|
| Solo-VPS | `~/.claude/skills/` | ein User |
| **Multi-User (5+)** | **`/opt/claude/skills/` (read-only, ein Wartungs-Owner)** | „20 User × N Projekte = Update-Hölle" — **nicht** pro Projekt installieren |

```bash
# Multi-User-Pool (als Wartungs-Owner)
sudo mkdir -p /opt/claude/skills
sudo git clone --depth 1 https://github.com/vibercoder79/intentron /opt/claude/skills/_intentron-bundle
# Skills aus dem Bundle in den Pool legen (bootstrap + ideation + implement + backlog + security-architect + dpo …)
# Update später zentral: ein `git pull` im Pool → alle Operatoren aktuell.
```

Der `/bootstrap`-Skill selbst muss im Skill-Verzeichnis liegen:

```bash
cp -r /opt/claude/skills/_intentron-bundle/bootstrap ~/.claude/skills/bootstrap   # bzw. in den System-Pool
```

> **Bundle vs. Companion:** Im Repo `vibercoder79/intentron` liegen die Framework-Skills + die vendored
> Bundle-Skills `dpo` und `security-architect` (ein `git clone` ist self-contained). Companion-Skills
> (`research`, `skill-creator`, …) liegen separat in `claudecodeskills` und werden nur bei Bedarf ergänzt.

### 1.5 Globale Claude-Code-Config

- `~/.claude/CLAUDE.md` — globale Registry/Projekt-Tabelle (Bootstrap Phase 7.3 trägt pro Projekt eine Zeile ein).
- `~/.claude/settings.json` — Session-Logging u.a. (per Default aktiv).
- `~/.claude/.env` — Secrets **pro Operator** (Mode 600).

### 1.6 (Optional) `core.hooksPath` global

Statt Git-Hooks pro Repo zu setzen, kann der Owner **einmal** einen geteilten Hooks-Ordner verdrahten:

```bash
git config --global core.hooksPath /opt/claude/githooks   # dann liegen die Hooks zentral
```

> Das ist die **Ausnahme**, nicht die Default-Konvention. Per Default werden Hooks pro Repo installiert
> (Abschnitt 2.3). Bei `core.hooksPath` muss der Owner den Ordner pflegen.

---

## 2. PRO PROJEKT (jedes Repo)

Diese Schritte macht **jeder Operator pro Projekt-Repo**. Kernpunkt: **`.git/` wird nicht geklont → Git-Hooks
und `environment.json` müssen pro Repo neu gesetzt werden.**

### 2.1 Projekt anlegen / klonen

```bash
mkdir -p ~/projects/<projekt> && cd ~/projects/<projekt>   # oder: git clone <repo-url> && cd <projekt>
```

### 2.2 Bootstrap starten (neues Projekt)

Claude Code im Projektordner starten und `/bootstrap` eingeben. Der Orchestrator führt durch:

- **Block A — Projekt-Kern** (~10 Fragen): Stack, Backlog-Prefix + **Backlog-Adapter** (`linear`/`github`/`jira`/`planner`/`none`), Architektur-Dimensionen + Add-ons (Privacy/Cost/Signal/Compliance), **Governance-Intensität** (`lite`/`standard`/`heavy`), Execution-Isolation, **Deployment-Szenario** (`solo-mac`/`other`).
- **Block B — Bestehende Infrastruktur**: Projekt-Verzeichnis, GitHub-Repo, **Doku-SSoT** (siehe 5.2), Backlog-Adapter, API-Keys, Developer-Übergabe. (Bei vorhandenen Dateien: Merge-Modus.)
- **Block C — Doku-Architektur**: 3-Schichten-Doku mit `ARCHITECTURE_DESIGN.md` als Hub.
- **Block D — Optional-Komponenten**: Self-Healing-Agent, DocSync zum Vault, Learning-Loop u.a.

Setup-Phasen: **0** (Briefing) → **4** (Grundstruktur + Gates) → **5** (Skills) → **7** (Finalisierung inkl. `verify-setup.sh`).

### 2.3 Git-Hooks installieren (PRO REPO — der wichtigste Schritt)

`.git/hooks/` wird **nicht** mit geklont. Jedes frische `git clone` hat noch keine Hooks. Bootstrap legt sie pro
Projekt an; bei einem bestehenden Klon neu setzen. Vier-Layer-Quality-Gate-Hooks:

| Hook | Layer | Pflicht? | Funktion |
|---|---|---|---|
| `spec-gate.sh` | — | **Pflicht** (alle Modi) | Kein Commit `ISSUE-XX` ohne `specs/ISSUE-XX.md` (HARD GATE) |
| `doc-version-sync.sh` | — | **Pflicht** | Kein Push bei VERSION-Drift zwischen DOC_FILES (HARD GATE) |
| `pre-edit-bodyguard.sh` | **Layer 0** | Pflicht, Default = **Warnung** | Secrets/`eval`/TLS-aus/SQL-Konkatenation **vor** dem Schreiben; Hard-Block via `BODYGUARD_STRICT=1` |
| `orphan-check.sh` | — | Optional (Hub-Auto-Verlinkung) | Neue `*.md` müssen im Hub §9 registriert sein (seit BOO-92: specs/ + backlog-records ausgenommen) |
| `coverage-check.sh` | Layer 2 | Optional (`heavy`) | Coverage-Gate ≥80% neuer Code (von `/implement` aufgerufen, nicht im Pre-Commit) |
| `raw-pii-guard.py` | — | Optional (Privacy-Add-on) | AST-Check: PII-Feld in Log-Senke (siehe `hooks-setup.md`) |

Hooks werden über `.claude/settings.json` (PreToolUse) registriert; sie sind dependency-frei (bash/grep/git/python3).

### 2.4 environment.json generieren

```bash
bash .claude/generate-environment-json.sh        # erkennt die einmal-installierten Tools für DIESES Projekt
```

Setzt `environment` auf `mac`/`vps`/`ci`. Auf der VPS = `vps`: keine IDE-Plugins, `sonarqube_ide_plugin=false`,
Reports nach `journal/reports/local/`.

### 2.5 Doku-SSoT festlegen (Block B.3 — siehe 5.2)

### 2.6 Verifizieren

```bash
bash scripts/verify-setup.sh            # Report, Exit 1 bei FAIL
bash scripts/verify-setup.sh --strict   # WARN = FAIL (für CI)
```

Prüft: environment.json, Toolchain (`command -v` pro Tool), **Git-Hooks (pro Repo!)**, Kern-Artefakte
(`CONVENTIONS.md`, `ARCHITECTURE_DESIGN.md`, `specs/`, `journal/`), Privacy-Artefakte (falls aktiv), Backlog-Adapter.
Ziel: **0 FAIL**.

### 2.7 Pro-Projekt-Minimal-Checkliste (HANDBUCH Anhang U)

- [ ] `CLAUDE.md` (Projekt-Vertrag) vorhanden
- [ ] **Git-Hooks installiert** (`.git/hooks/pre-commit` — pro Repo!) — alternativ `core.hooksPath` global
- [ ] `.claude/environment.json` generiert
- [ ] Doku-SSoT festgelegt
- [ ] `bash scripts/verify-setup.sh` zeigt **0 FAIL**

---

## 3. Projekt 2..N & bestehendes Projekt onboarden (HANDBUCH Anhang U)

Die Basis (Tools, Skill-Pool, Claude-Config) steht schon → nur der **Pro-Projekt-Teil** ist nötig.

### Weg 2 — Neues Projekt Nr. 2..N (Schnellpfad)

1. Projekt-Verzeichnis + GitHub-Repo anlegen.
2. `CLAUDE.md` aus Template (Projekt-Kern) — Bootstrap erkennt vorhandene Infra (Block B) und **überspringt** die Skill-Installation.
3. **Git-Hooks installieren** (pro Repo!).
4. `bash .claude/generate-environment-json.sh`.
5. Doku-SSoT wählen (oft dieselbe wie Projekt 1, aber pro Projekt entscheidbar).
6. `bash scripts/verify-setup.sh` → Proof.

→ In Minuten governance-ready, ohne Tools/Skills neu zu installieren.

### Weg 3 — Bestehendes (Brownfield-)Projekt onboarden

1. `/bootstrap` im **Merge-Modus**: Block B erkennt vorhandene Dateien → **„nur fehlende Governance-Dateien ergänzen"** (bestehenden Code nicht anfassen).
2. Governance-Bausteine nachziehen:
   ```bash
   bash bootstrap/scripts/migrate-to-v2.sh --list          # was ist verfügbar
   bash bootstrap/scripts/migrate-to-v2.sh --dry-run --all  # Vorschau
   bash bootstrap/scripts/migrate-to-v2.sh --all            # alle Auto-Schritte (idempotent)
   # oder gezielt, z.B. die neuen Bausteine:
   bash bootstrap/scripts/migrate-to-v2.sh --issue BOO-86   # Layer-0-Bodyguard
   bash bootstrap/scripts/migrate-to-v2.sh --issue BOO-87   # dpo-Kontrollkatalog
   bash bootstrap/scripts/migrate-to-v2.sh --issue BOO-91   # CONTEXT.md
   bash bootstrap/scripts/migrate-to-v2.sh --issue BOO-93   # raw-pii-guard (opt-in)
   ```
3. `bash scripts/verify-setup.sh` → schließt die Lücken-Liste.

> `migrate-to-v2.sh` ist **idempotent** — mehrfaches Ausführen ist sicher. `--dry-run` zeigt nur, was passieren würde.

---

## 4. Team-Aspekte (HANDBUCH Anhang R)

Der **Code-Layer skaliert nativ** — Git/Branches/PRs/Branch-Protection/Spec-Gate sind ohne Framework-Ergänzung
team-tauglich; nur die **Konflikt-Frequenz** steigt. Was ein größeres Team zusätzlich braucht:

- **CODEOWNERS** (`.github/CODEOWNERS`): **Pflicht ab 10 Operatoren, empfohlen ab 5.** Mappt Datei-Pattern → Sub-Team; GitHub erzwingt ≥1 Reviewer aus dem zuständigen Team. Beispiel:
  ```
  /SECURITY.md            @owlist/sec-leads
  /PRIVACY.md             @owlist/legal-leads
  /ARCHITECTURE_DESIGN.md @owlist/arch-leads
  /CONVENTIONS.md         @owlist/arch-leads
  ```
  **CODEOWNERS ersetzt nicht das Spec-Gate — beide laufen parallel.**
- **Erweiterte Branch-Protection:** Required-Reviewer aus CODEOWNERS, Required-Status-Checks (Spec-Gate, Lint-Gate, Coverage-Gate, ggf. Security-Scan, ggf. DPO-Audit), „Dismiss stale reviews", „Require linear history". Setup: `bootstrap/scripts/setup-branch-protection.sh` (braucht `gh` + `repo`-Scope).
- **Vier-Augen-Konvention:** `review-ok`/`privacy-ok` darf Solo selbst setzen; im Team ist Self-Approval ein Audit-Risiko. Das Framework **erzwingt das nicht** — Operator-Disziplin.
- **Skill-Pool-Governance:** **ein** System-Pool `/opt/claude/skills/`, read-only, ein Wartungs-Owner, `git pull` = alle aktuell. Nicht pro Projekt installieren.
- **Squad-Modell:** 3–5 Operatoren/Modul + Lead-Architekt + Sec-Lead + Legal-Lead.

---

## 5. Entscheidungen (mit Empfehlung)

### 5.1 Docker/devcontainer vs. Direkt-Install

| | Direkt-Install (Abschnitt 1.2) | Container-Profil (BOO-81) |
|---|---|---|
| Wann | Default; Solo-VPS; volle Kontrolle | Team mit **identischen Linter-Versionen**; gewünschte Tool-Isolation; CI-Image-Wiederverwendung |
| Aufwand | manuell, einmal pro VPS | `.devcontainer/` ins Projekt: Bootstrap-Option oder `migrate-to-v2.sh --issue BOO-81` |
| Status | Default | **Optional, nicht Pflicht** |

**Empfehlung:** Für eine Team-VPS, bei der **alle dieselben Tool-Versionen** brauchen, lohnt das Container-Profil
(Versions-Gleichschritt + als CI-Base wiederverwendbar). Für eine kleine VPS oder maximale Kontrolle reicht der
Direkt-Install. Die `Dockerfile` unter `bootstrap/references/devcontainer/` ist die Referenz für beide Wege.

### 5.2 Doku & Backlog: Git-lokal vs. GitHub

- **Lebende Doku gehört bei Teams ins GitHub-Repo (`docs/project/`)** — „Obsidian ist ein Solo-Werkzeug, kein
  Enterprise-Werkzeug" (Anhang R). Repo-Docs ist die einzige SSoT-Option, die über alle Teamgrößen (Solo→20+)
  trägt: gleiche Git-Mechanik wie Code (PR-Review, Branch-Protection, CODEOWNERS für Doku).
  - Solo → Obsidian Vault ok · 2–5 → Obsidian Sync **oder** Repo-Docs · **5+ → Repo-Docs** (oder externes DMS).
  - **Vault-Harvest-Pattern** (optional): Repo = Team-SSoT, zusätzlich einseitiger `git post-merge`-Hook
    Repo → persönlicher Vault (nie zurück).
- **Backlog-Adapter:** Das Framework spricht vom neutralen **Backlog-Record** (ID, Intent, AC, DoD,
  `execution_mode`, …), nicht zwingend Linear. Adapter: **Linear (empfohlen)**, GitHub Issues, Planner, Markdown,
  oder `none`. Regel: *„kein Linear" ist kein Framework-Bruch; „kein Backlog-Record" ist einer.*

**Empfehlung Team-VPS:** Doku-SSoT = **`docs/project/` im GitHub-Repo**; Backlog = Linear oder GitHub Issues
(geteilt). Git-lokal (ohne Remote) nur für reine Experimentier-Repos.

### 5.3 Souveränität (HANDBUCH Anhang Q)

Bei FINMA/BaFin/NIS-2/nDSG-Mandat: EU-VPS-Standort wählen, ggf. self-hosted GitLab/Forgejo statt GitHub, EU-LLM-Endpoint
(Mistral/Bedrock-Frankfurt/Ollama) über den optionalen `llm_proxy_url`-Hook in `.claude/environment.json`. Das
Framework **liest** den Hook nur — Anonymisierung/Routing ist Operator-Infrastruktur.

---

## 6. Vier-Layer-Quality-Gate auf der headless VPS

Auf einer SSH-VPS fällt **nur Layer 1 (IDE-Inline-Hints) weg** — alle anderen greifen:

| Layer | Werkzeug | Auf headless VPS? |
|---|---|---|
| **Layer 0 — Edit-Bodyguard** | `pre-edit-bodyguard.sh` (PreToolUse) | **Ja** (KI-Runtime-Hook, IDE-unabhängig) |
| Layer 1 — IDE | Error Lens, ESLint-/Sonar-IDE-Plugin | **Nein** (kein Editor-UI über SSH) |
| **Layer 2 — CLI/Pre-Commit** | `npx eslint .`, `semgrep --config auto .`, `npm test`, coverage-check | **Ja** (CLIs explizit laufen) |
| **Layer 3 — CI** | GitHub Actions (eslint/ruff/semgrep/perf/sonar) | **Ja** (server-side) |

> **Praxisregel:** Auf dem VPS erwartest du kein Inline-Feedback im Editor — du läufst die CLIs explizit. Die Gates
> sind dieselben wie am Mac; nur die Tooling-Liste unterscheidet sich. **Keine Qualitäts-Einbuße beim VPS-Coding.**

---

## 7. Schnellreferenz: einmal pro VPS vs. pro Projekt

| EINMAL pro VPS | PRO PROJEKT (jedes Repo) |
|---|---|
| Tools: Semgrep, Ruff, ESLint, (SonarScanner) via apt/pipx/npm -g | Projekt-Dev-Deps: ESLint/Prettier in `package.json`, pytest, c8/pytest-cov via `npm/pip install` |
| Claude Code CLI installieren | `CLAUDE.md` / `CONVENTIONS.md` / `ARCHITECTURE_DESIGN.md` aus Template |
| Skill-Pool: `~/.claude/skills/` (Solo) bzw. `/opt/claude/skills/` (Multi-User) | **Git-Hooks: `.git/hooks/*` — pro Repo!** (oder `core.hooksPath` global) |
| `~/.claude/CLAUDE.md`, `settings.json`, `.env` (pro Operator) | `.claude/environment.json` via `generate-environment-json.sh` |
| Operatoren-User + SSH-Härtung (Szenario 3) | Doku-SSoT-Wahl, `specs/`, `journal/`, Backlog-Adapter |
| (optional) Container-Profil für Versions-Gleichschritt | `bash scripts/verify-setup.sh` → 0 FAIL |

---

## 8. Bekannte Lücken / zu entscheiden (nicht im Framework abgedeckt)

- **Kein zentrales Install-Script** für die Toolchain — die Sequenz in 1.2 ist aus dem Container-Dockerfile abgeleitet.
- **`generate-environment-json.sh`** wird vom `/bootstrap`-Skill zur Laufzeit erzeugt (kein statisches Template im Repo).
- **`gh`/`git`/`jq`/bash-Version** sind nicht in der §3-Pflichtliste — dieses Runbook führt sie als Prereq.
- **VPS-Sizing** nur als Daumenwert (8 GB/4 vCPU für 5 Operatoren) — nach Last skalieren.
- **`core.hooksPath`** ist eine Operator-Empfehlung, kein Bootstrap-Schritt — bei Nutzung Hooks-Ordner selbst pflegen.

---

*Runbook erstellt 2026-06-01 auf Basis des aktuellen Repo-Stands (bootstrap 3.35, BOO-86–93). Querverweise:
HANDBUCH Anhänge P/Q/R/S/T/U/V, §8d. Bei Framework-Updates dieses Runbook gegen die Anhänge abgleichen.*
