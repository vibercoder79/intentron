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

## 6. Security Sub-Artifacts

`SECURITY.md` is the operational security contract. It points to sub-artifacts that contain concrete evidence and technical rules:

| Artifact | Purpose | When to update? |
|---|---|---|
| `ARCHITECTURE_DESIGN.md` | Lead document for architecture, quality attributes, and security/privacy boundaries | When a security decision changes architecture or runtime boundaries |
| `API_INVENTORY.md` | External APIs, providers, data flow, auth mechanics | On every new or changed external interface |
| `.semgrep.yml` | SAST rules and security patterns | When new risk classes, frameworks, or languages are added |
| `.codex/hooks.json` / `.claude/settings.json` | Runtime hooks and guardrails | When security gates, sensitive paths, or bypass rules change |
| `.claude/sensitive-paths.json` / `.codex/sensitive-paths.json` | Files/paths requiring human review | When new critical areas appear |
| `docs/security/threat-model-*.md` | Threat models for risky features | For auth, API, external input, data flow, webhooks, agent automation |
| Privacy/compliance documents | Legal basis, DPIA, audit trail | When personal data or regulated processes are involved |

## 7. Security-by-Design Flow

1. `/ideation` writes `Security Impact` and, when relevant, `Security Validation` into the story.
2. `/implement` reads `ARCHITECTURE_DESIGN.md`, `SECURITY.md`, and the matching sub-artifacts.
3. `/implement` runs gates: lint, Semgrep/SAST, tests/smoke, and security checklist. How these gates share the same config-reader logic locally and in CI is shown in HANDBUCH chapter 8d-quart.
4. `/security-architect` adds threat models, policies, or security reviews for risky changes.
5. `/sprint-review` checks whether security debt, open findings, or recurring patterns appeared.

## 8. Incident Note

If a security finding appears after merge/release:

- describe the finding briefly,
- name the affected version/story,
- document the mitigation,
- create a follow-up Backlog Record.
