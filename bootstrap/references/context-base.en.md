# CONTEXT.md — Ubiquitous Language (framework base · BOO-91)

Canonical vocabulary plus a forbidden list for this project. The AI reads `CONTEXT.md`
while writing and **consistently uses the canonical terms** — no inventing synonyms
(`User` vs. `Customer` vs. `Betroffener`). Every term carries its **source** (audit trail).

**Default = guidance, not a hard gate.** The AI is guided, not blocked. (The optional
enforcement — checking forbidden terms via the dpo catalog (BOO-87) or the Layer-0
bodyguard (BOO-86) — is a later, opt-in extension.)

This file is the **pre-filled framework base**. On `/bootstrap` it is seeded into the
project's `CONTEXT.md`; the operator adds **project-specific** terms in the "Project domain"
section. The project overlay survives framework updates.

## Compliance vocabulary

| canonical | forbidden | source |
| --- | --- | --- |
| `Betroffener` (data subject) | `User` / `Customer` / `Client` (in PII context) | GDPR Art. 4 (data subject) |
| `Bearbeitung` | `Verarbeitung` | nDSG (Switzerland deliberately uses "Bearbeitung") |
| `Auftragsverarbeiter` (processor) | `Vendor` / `Dienstleister` | GDPR Art. 28 |
| `Einwilligung` (consent) | `Zustimmung` / `OK` | GDPR Art. 6 / Art. 7 |
| `personenbezogene Daten` (personal data) | `PII` as a code term without definition | GDPR Art. 4 |

## Governance vocabulary

| canonical | forbidden | source |
| --- | --- | --- |
| `Story` | `Ticket` | INTENTRON governance |
| `Spec` | `Anforderung` / loose "requirement" | INTENTRON governance |
| `Intent` | vague "goal" | INTENTRON governance |
| `Gate` | generic "check" | INTENTRON quality gate |
| `Layer 0` / `Layer 2` / `Layer 3` | mixed/inconsistent layer naming | INTENTRON quality-gate architecture |
| `BOO-<n>` | free-form issue label | Linear issue prefix |

<!-- SEED END — the section below is copied empty into the project CONTEXT.md on bootstrap -->
