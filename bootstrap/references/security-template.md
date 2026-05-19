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

## 6. Incident-Notiz

Wenn ein Security-Finding erst nach Merge/Release sichtbar wird:

- Finding kurz beschreiben,
- betroffene Version/Story nennen,
- Mitigation dokumentieren,
- Follow-up als Backlog-Record anlegen.
