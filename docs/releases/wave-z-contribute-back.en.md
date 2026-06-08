# Wave Z — Contribute-Back Loop: contribute-fix.sh (BOO-90)

> 🌐 **Language:** English (this file) · [🇩🇪 Deutsch](wave-z-contribute-back.md)

**Linear:** [BOO-90](https://linear.app/owlist/issue/BOO-90/) · Follow-up story from BOO-88

## Problem

When a deployed factory user finds a bug in a copied governance artifact and
fixes it locally (like the coverage-check bug from privacy-proxy / PP-001 → BOO-88), there was **no
way back** to the factory source. The backflow ran manually (user → Tobias → fix).
That does not scale and is not audit-capable.

## What Changes

- **New helper `bootstrap/scripts/contribute-fix.sh`** (field→source): detects framework artifacts
  changed locally in the project (initially the scaffolded hooks under
  `.claude/hooks/` that live canonically in `bootstrap/references/hooks/` — see BOO-89) and
  produces per deviation:
  - a clean **patch** (`contribute-back/<name>.patch`),
  - an **issue proposal** (`contribute-back/<name>.proposal.md`) with title + body + patch.
- **No auto-push, no auto-PR.** The operator reviews and submits themselves — no
  unrequested outflow of code from a customer project.
- **Coupling to BOO-89:** the more hooks become single-source (`references/hooks/`), the more
  artifacts `contribute-fix` covers automatically.

## Usage

```bash
bash <framework>/bootstrap/scripts/contribute-fix.sh --project .
# → contribute-back/coverage-check.sh.{patch,proposal.md} (if deviation)
```

## Verified

- Local deviation → patch + proposal produced, patch contains the operator change.
- Identical to source → "nothing to contribute", no `contribute-back/` created.
- `bash -n` clean.

## Design Decision

Operator choice "/contribute-fix helper (backflow)". Deliberately the **field→source** path (the
actual gap); the source→field path (version marker + replacing migration) is already
established with BOO-88 for coverage-check and can be generalized later.

## Follow-up

- Generalization to further artifact types (not only hooks) and an optional
  `/contribute-fix` skill wrapper remain later expansion stages.
