# Runbook: SonarCloud-Integration für neue GitHub-Repos

**Zweck:** Schritt-für-Schritt-Anleitung zum Einrichten von SonarCloud als Required Status Check in einem neuen GitHub-Repository.

**Zuletzt aktualisiert:** 2026-06-05

> EN: [`sonarcloud-setup.en.md`](sonarcloud-setup.en.md)

---

## Wann macht SonarCloud Sinn?

**Kurzantwort: nur wenn GitHub Actions als CI/CD-Pipeline genutzt wird.**

SonarCloud triggert via GitHub Actions bei jedem Push. Ohne eine CI-Pipeline ist dieses Setup sinnlos.

| Setup | SonarCloud? |
|-------|------------|
| GitHub Actions CI/CD — Push → Actions → Deploy | **Ja — voller Nutzen** |
| Direkt auf VPS — GitHub = nur Code-Storage | **Nein — lokale Hooks ersetzen CI-Gates** |
| Hybrid (manche Branches via CI) | Optional, pro Branch |

**Bei Direct-Deploy-Setups (VPS, kein GitHub Actions):**
Lokale Hooks decken dieselben Quality-Gates ab: `pre-edit-bodyguard` (Layer 0), `spec-gate`, `semgrep pre-commit` (Layer 2). SonarCloud kann nachgerüstet werden, wenn später eine CI-Pipeline eingeführt wird.

> Visueller Überblick der beiden Deployment-Modi:
> [`sonarcloud-setup.excalidraw`](sonarcloud-setup.excalidraw) — in Excalidraw.com öffnen

---

## Voraussetzungen

- GitHub-Repo existiert (public oder private)
- SonarCloud-Account unter sonarcloud.io (kostenlos für Open-Source, lizenzpflichtig für private Repos)
- Admin-Zugriff auf das GitHub-Repo (für Secrets + Branch Protection)

---

## Schritt 1: SonarCloud-Projekt anlegen

1. Auf [sonarcloud.io](https://sonarcloud.io) einloggen
2. **+** → **Analyze new project**
3. GitHub-Organisation auswählen → Repository anklicken → **Set up**
4. Analysemethode: **GitHub Actions** wählen
5. SonarCloud zeigt dann den `SONAR_TOKEN` → **nicht schließen**, wird im nächsten Schritt gebraucht

---

## Schritt 2: Richtigen Token-Typ verwenden

> **Kritisch:** Für GitHub Actions immer **Project Analysis Token** verwenden, nicht den User Token.

Token holen:
- sonarcloud.io → Projekt → **Administration** → **Analysis Method** → **GitHub Actions**
- Dort auf **Generate a token** klicken → Token kopieren

Falscher Token-Typ führt zu `Execute Analysis`-Fehler in GitHub Actions.

---

## Schritt 3: GitHub Secret setzen

1. GitHub-Repo → **Settings** → **Secrets and variables** → **Actions**
2. **New repository secret**
   - Name: `SONAR_TOKEN`
   - Value: Token aus Schritt 2 einfügen
3. **Add secret**

---

## Schritt 4: sonar-project.properties erstellen

Im Root des Repos anlegen:

```properties
sonar.projectKey=<org>_<repo-name>
sonar.organization=<org-slug>
sonar.sources=.
sonar.exclusions=node_modules/**,dist/**,.next/**,coverage/**
sonar.javascript.lcov.reportPaths=coverage/lcov.info
```

`projectKey` und `organization` stehen auf der SonarCloud-Projektseite unter **Information**.

---

## Schritt 5: GitHub Actions Workflow anlegen

Datei: `.github/workflows/sonarcloud.yml`

```yaml
name: SonarCloud Analysis

on:
  push:
    branches: [main]
  pull_request:
    types: [opened, synchronize, reopened]

jobs:
  sonarcloud:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
        with:
          fetch-depth: 0

      - name: SonarCloud Scan
        uses: SonarSource/sonarcloud-github-action@master
        env:
          GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
          SONAR_TOKEN: ${{ secrets.SONAR_TOKEN }}
```

---

## Schritt 6: SonarCloud als Required Status Check eintragen

1. GitHub-Repo → **Settings** → **Branches** → Branch Protection Rule für `main` öffnen (oder neu anlegen)
2. **Require status checks to pass before merging** aktivieren
3. In der Suche: `SonarCloud Code Analysis` eingeben → anhaken
4. **Save changes**

> **Hinweis:** Der Status Check erscheint in der Suche **erst, nachdem der Workflow mindestens einmal erfolgreich gelaufen ist**.
> Nicht gefunden? → Schritt 6a ausführen, dann hier weitermachen.

### Schritt 6a: Ersten Scan manuell anstoßen

**Option A — Leeren Commit pushen (empfohlen):**
```bash
git commit --allow-empty -m "chore: trigger sonarcloud scan" && git push
```

**Option B — Fehlgeschlagenen Run neu starten:**
GitHub-Repo → **Actions** → `SonarCloud Analysis` → letzten Lauf anklicken → **Re-run all jobs**

Danach in GitHub Actions warten bis der Job grün ist, dann Schritt 6 wiederholen.

---

## Troubleshooting

| Fehler | Ursache | Lösung |
|--------|---------|--------|
| `You are not authorized to run analysis` | User Token statt Project Analysis Token | Token aus Schritt 2 neu generieren |
| `SONAR_TOKEN` not found | Secret nicht gesetzt oder Typo | Schritt 3 wiederholen |
| Quality Gate bleibt auf `In Progress` | Erster Scan läuft noch | 2–5 Minuten warten |
| Status Check nicht in Branch Protection sichtbar | Workflow noch nie erfolgreich gelaufen | Schritt 6a ausführen, dann erneut suchen |

---

## Verwandte Artefakte

- `specs/<STORY-ID>.md` — Story: SonarCloud-Integration einrichten
- `.github/workflows/sonarcloud.yml` — Workflow-Datei
- `sonar-project.properties` — Projekt-Konfiguration
- `ARCHITECTURE_DESIGN.md §9` — Referenz-Index
