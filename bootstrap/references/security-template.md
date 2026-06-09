# Security Template

> Wird von `/bootstrap` als `SECURITY.md` im Zielprojekt gerendert.
> Keine echten Secrets, Tokens, Cookies oder Passwoerter in dieses Dokument schreiben.

# {{PROJECT_NAME}} — Security

**Version:** {{VERSION_START}} | **Stand:** {{TODAY}}

## 1. Security-Grundsatz

Security ist ein laufender Projektvertrag, kein Abschluss-Check. Jede Story benennt ihren `Security Impact`; jede relevante Aenderung dokumentiert ihre `Security Validation`.

## 2. Secrets-Policy

- Secrets niemals in Git committen.
- `.env` und `.env.*` bleiben gitignored.
- `.env.example` enthaelt nur Namen, Format und Platzhalter, niemals echte Werte.
- Logs duerfen keine Tokens, Cookies, personenbezogenen Daten oder internen Credential-Fragmente enthalten.

## 3. Change-Type Matrix

| Change-Type | Pflichtpruefung |
|-------------|-----------------|
| `none` | Begruendung, warum kein neuer Angriffsvektor entsteht |
| `api` | Auth, Rate-Limits, Timeouts, Input Validation, Error Sanitizing |
| `auth` | Authentication, Authorization, Session-/Token-Handling, sensitive paths |
| `data` | Datenklassifikation, Zugriff, Retention, Logging, Privacy |
| `dependency` | Existenz, Alter, CVE, Lockfile, Supply-Chain-Risiko |
| `ci` | Secret-Exposure, Permissions, Artifact-Scope, Branch-/PR-Schutz |
| `governance` | Gate-Wirkung, Bypass-Regeln, Audit-Spur |
| `external-provider` | Provider-Status, Credentials, Kosten, Datenfluss, Fallback |

## 4. Security Validation Evidence

Jede relevante Story dokumentiert vor `Done`:

- gelaufene Checks,
- Findings und Fixes,
- akzeptierte Restrisiken,
- betroffene sensitive Pfade,
- notwendige Updates an `SECURITY.md`, `API_INVENTORY.md`, `.semgrep.yml`, `.claude/sensitive-paths.json`, `.codex/hooks.json`, `ARCHITECTURE_DESIGN.md` oder `CONVENTIONS.md`.

## 5. Sensitive Paths

Bootstrap kann eine Datei `.claude/sensitive-paths.json` und/oder `.codex/sensitive-paths.json` erzeugen. Diese Patterns erzwingen Human Review bei kritischen Bereichen.

Beispiele:

```json
{
  "patterns": [
    "auth/**",
    "**/*token*",
    "**/*secret*",
    "**/*pii*",
    ".github/workflows/**",
    ".codex/hooks.json",
    ".claude/settings.json"
  ]
}
```

## 6. Security-Unterartefakte

`SECURITY.md` ist der operative Security-Vertrag. Es verweist auf Unterartefakte, die konkrete Evidenz und technische Regeln enthalten:

| Artefakt | Zweck | Wann aktualisieren? |
|---|---|---|
| `ARCHITECTURE_DESIGN.md` | Lead-Dokument fuer Architektur, Quality Attributes und Security-/Privacy-Grenzen | Wenn eine Security-Entscheidung Architektur oder Runtime-Grenzen veraendert |
| `API_INVENTORY.md` | Externe APIs, Provider, Datenfluss, Auth-Mechanik | Bei jeder neuen oder geaenderten externen Schnittstelle |
| `.semgrep.yml` | SAST-Regeln und Security-Patterns | Wenn neue Risiko-Klassen, Frameworks oder Sprachen dazukommen |
| `.codex/hooks.json` / `.claude/settings.json` | Runtime-Hooks und Guardrails | Wenn Security-Gates, sensitive Pfade oder Bypass-Regeln geaendert werden |
| `.claude/sensitive-paths.json` / `.codex/sensitive-paths.json` | Dateien/Pfade mit Human-Review-Pflicht | Wenn neue kritische Bereiche entstehen |
| `docs/security/threat-model-*.md` | Threat Models fuer riskante Features | Bei Auth, API, externem Input, Datenfluss, Webhooks, Agent-Automation |
| Privacy-/Compliance-Dokumente | Rechtsgrundlagen, DPIA, Audit Trail | Wenn personenbezogene Daten oder regulierte Prozesse betroffen sind |

## 7. Security-by-Design-Ablauf

1. `/ideation` schreibt `Security Impact` und, falls relevant, `Security Validation` in die Story.
2. `/implement` liest `ARCHITECTURE_DESIGN.md`, `SECURITY.md` und die passenden Unterartefakte.
3. `/implement` fuehrt Gates aus: Lint, Semgrep/SAST, Tests/Smoke und Security-Checklist. Wie diese Gates lokal und in CI dieselbe Config-Reader-Logik teilen, zeigt HANDBUCH-Kapitel 8d-quart.
4. `/security-architect` ergaenzt Threat Models, Policies oder Security-Reviews bei riskanten Aenderungen.
5. `/sprint-review` prueft, ob Security-Schulden, offene Findings oder wiederkehrende Muster entstanden sind.

## 8. Incident-Notiz

Wenn ein Security-Finding erst nach Merge/Release sichtbar wird:

- Finding kurz beschreiben,
- betroffene Version/Story nennen,
- Mitigation dokumentieren,
- Follow-up als Backlog-Record anlegen.
