# Runbook: Vercel CI/CD-Integration mit GitHub Actions

**Zweck:** Schritt-für-Schritt-Anleitung zum Einrichten von automatischen Deployments via GitHub Actions → Vercel (kein Vercel Git-Integration, volle Kontrolle über den Deploy-Zeitpunkt).

**Zuletzt aktualisiert:** 2026-06-04

---

## Überblick

Das Setup verwendet **Vercel CLI in GitHub Actions** statt der nativen Vercel-Git-Integration. Vorteil: Deploy läuft erst nach bestandenen CI-Checks (Lint, Tests, SAST).

Drei GitHub Secrets werden benötigt:

| Secret | Woher |
|--------|-------|
| `VERCEL_TOKEN` | Vercel Account Settings → Tokens |
| `VERCEL_ORG_ID` | `.vercel/project.json` nach `vercel link` |
| `VERCEL_PROJECT_ID` | `.vercel/project.json` nach `vercel link` |

---

## Schritt 1: Vercel-Projekt anlegen und verknüpfen

### 1a — Vercel CLI lokal installieren
```bash
npm install --global vercel@latest
```

### 1b — Projekt verknüpfen
Im Root des Repos:
```bash
vercel link
```

Vercel fragt nach Organisation und Projekt. Nach dem Link wird `.vercel/project.json` erstellt:

```json
{
  "orgId": "team_xxxxxxxxxxxx",
  "projectId": "prj_xxxxxxxxxxxx"
}
```

> **Wichtig:** `.vercel/project.json` in `.gitignore` eintragen — enthält keine echten Secrets, aber IDs die nicht ins Repo gehören.

---

## Schritt 2: Vercel API-Token erstellen

1. [vercel.com/account/tokens](https://vercel.com/account/tokens) aufrufen
2. **Create Token**
   - Name: z.B. `github-actions-<projektname>`
   - Scope: **Full Account** oder das spezifische Team
   - Expiration: nach Policy (empfohlen: 1 Jahr, dann rotieren)
3. Token kopieren — wird nur einmal angezeigt

---

## Schritt 3: GitHub Secrets setzen

GitHub-Repo → **Settings** → **Secrets and variables** → **Actions** → **New repository secret**:

| Name | Value |
|------|-------|
| `VERCEL_TOKEN` | Token aus Schritt 2 |
| `VERCEL_ORG_ID` | `orgId` aus `.vercel/project.json` |
| `VERCEL_PROJECT_ID` | `projectId` aus `.vercel/project.json` |

---

## Schritt 4: Vercel Git-Integration deaktivieren

Damit nicht parallel ein Vercel-Deploy und ein GitHub-Actions-Deploy laufen:

1. [vercel.com](https://vercel.com) → Projekt → **Settings** → **Git**
2. **Connected Git Repository** → **Disconnect** (oder Deploy-Hooks deaktivieren)

> Falls die Vercel Git-Integration aktiv bleibt, deployt Vercel bei jedem Push zusätzlich zu GitHub Actions.

---

## Schritt 5: GitHub Actions Workflow

Datei: `.github/workflows/deploy.yml`

```yaml
name: Deploy

on:
  push:
    branches: [main]

jobs:
  deploy:
    name: Deploy to Vercel
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Setup Node.js
        uses: actions/setup-node@v4
        with:
          node-version: '20'
          cache: 'npm'

      - name: Install Vercel CLI
        run: npm install --global vercel@latest

      - name: Pull Vercel environment
        run: vercel pull --yes --environment=production --token="${{ secrets.VERCEL_TOKEN }}"
        env:
          VERCEL_ORG_ID: ${{ secrets.VERCEL_ORG_ID }}
          VERCEL_PROJECT_ID: ${{ secrets.VERCEL_PROJECT_ID }}

      - name: Build
        run: vercel build --prod --token="${{ secrets.VERCEL_TOKEN }}"
        env:
          VERCEL_ORG_ID: ${{ secrets.VERCEL_ORG_ID }}
          VERCEL_PROJECT_ID: ${{ secrets.VERCEL_PROJECT_ID }}

      - name: Deploy to production
        id: deploy
        run: |
          URL=$(vercel deploy --prebuilt --prod --token="${{ secrets.VERCEL_TOKEN }}")
          echo "url=$URL" >> $GITHUB_OUTPUT
          echo "Deployed to: $URL"
        env:
          VERCEL_ORG_ID: ${{ secrets.VERCEL_ORG_ID }}
          VERCEL_PROJECT_ID: ${{ secrets.VERCEL_PROJECT_ID }}
```

---

## Schritt 6: Testen

1. Commit auf `main` pushen
2. GitHub Actions → `Deploy` → Logs verfolgen
3. Am Ende des Jobs steht die Deployment-URL in den Logs (`Deployed to: https://...`)
4. URL aufrufen und App prüfen

---

## Troubleshooting

| Fehler | Ursache | Lösung |
|--------|---------|--------|
| `Error: Vercel token is not defined` | `VERCEL_TOKEN` Secret fehlt oder Typo | Schritt 3 wiederholen |
| `Error: Project not found` | `VERCEL_PROJECT_ID` falsch | Wert aus `.vercel/project.json` prüfen |
| `Error: Team not found` | `VERCEL_ORG_ID` falsch | Wert aus `.vercel/project.json` prüfen |
| Deploy läuft doppelt (Actions + Vercel direkt) | Vercel Git-Integration noch aktiv | Schritt 4 ausführen |
| Build schlägt fehl, lokal läuft es | Env-Variablen fehlen auf Vercel | vercel.com → Projekt → Settings → Environment Variables prüfen |

---

## Verwandte Artefakte

- `specs/<STORY-ID>.md` — Story: CI/CD-Integration
- `.github/workflows/deploy.yml` — Workflow-Datei
- `vercel.json` — Vercel-Konfiguration (maxDuration etc.)
- [`sonarcloud-setup.md`](./sonarcloud-setup.md) — SonarCloud-Runbook (paralleles Setup)
- `ARCHITECTURE_DESIGN.md §9` — Referenz-Index
