# Security Template

> Rendered by `/bootstrap` as `SECURITY.md` in the target project.
> Never write real secrets, tokens, cookies, or passwords into this document.

# {{PROJECT_NAME}} — Security

**Version:** {{VERSION_START}} | **Updated:** {{TODAY}}

## 1. Security Principle

Security is a living project contract, not a final checklist. Every story states its `Security Impact`; every relevant change documents its `Security Validation`.

## 2. Secrets Policy

- Never commit secrets to Git.
- `.env` and `.env.*` remain gitignored.
- `.env.example` contains names, formats, and placeholders only, never real values.
- Logs must not contain tokens, cookies, personal data, or internal credential fragments.

## 3. Change-Type Matrix

| Change-Type | Required validation |
|-------------|---------------------|
| `none` | Explain why no new attack surface is introduced |
| `api` | Auth, rate limits, timeouts, input validation, error sanitizing |
| `auth` | Authentication, authorization, session/token handling, sensitive paths |
| `data` | Data classification, access, retention, logging, privacy |
| `dependency` | Existence, age, CVE, lockfile, supply-chain risk |
| `ci` | Secret exposure, permissions, artifact scope, branch/PR protection |
| `governance` | Gate effect, bypass rules, audit trail |
| `external-provider` | Provider status, credentials, cost, data flow, fallback |

## 4. Security Validation Evidence

Every relevant story documents before `Done`:

- checks that were run,
- findings and fixes,
- accepted residual risks,
- sensitive paths touched,
- required updates to `SECURITY.md`, `API_INVENTORY.md`, `.semgrep.yml`, `.claude/sensitive-paths.json`, `.codex/hooks.json`, `ARCHITECTURE_DESIGN.md`, or `CONVENTIONS.md`.

## 5. Sensitive Paths

Bootstrap can create `.claude/sensitive-paths.json` and/or `.codex/sensitive-paths.json`. These patterns force human review for critical areas.

Example:

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

## 6. Incident Note

If a security finding appears after merge/release:

- describe the finding briefly,
- name the affected version/story,
- document the mitigation,
- create a follow-up Backlog Record.
