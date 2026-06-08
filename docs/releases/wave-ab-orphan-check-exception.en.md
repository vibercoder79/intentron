# Wave AB — orphan-check work-item exception (BOO-92)

> 🌐 **Language:** English (this file) · [🇩🇪 Deutsch](wave-ab-orphan-check-exception.md)

**Linear:** [BOO-92](https://linear.app/owlist/issue/BOO-92/) · Source: upstream feedback field installation privacy-proxy / 2XT (Martin), 2026-05-31

## Problem

The optional `orphan-check.sh` hook enforces: every new `*.md` must be registered in the doc hub
`ARCHITECTURE_DESIGN.md` **§9 Referenzen**. This also forced **even** story specs
(`specs/<PREFIX>-<NUM>.md`) and backlog records (`docs/project/backlog/record-*.md`) into the hub —
although they already have their own indexes (`specs/` = ~25 `BOO-NN.md` files, backlog `README.md`,
`links.spec` in the record). An additional §9 entry per story is redundant mandatory effort.
Consequence: either friction on every story, or the operator turns off the hook entirely — then
the hub protection (preventing orphaned documents) is completely lost.

## What changes

- **`ORPHAN_EXCLUDE` variable** in the orphan-check snippet (`bootstrap/references/hooks-setup.md` DE +
  `hooks-setup.en.md` EN), overridable via env. The default excludes `specs/<PREFIX>-<NUM>.md` and
  `docs/project/backlog/record-*.md` from the hub check; all other `.md` continue to be checked
  against the hub:
  ```bash
  ORPHAN_EXCLUDE="${ORPHAN_EXCLUDE:-^(docs/project/backlog/record-.*\.md|specs/[A-Z]+-[0-9]+\.md)$}"
  NEW_MDS=$(git diff --cached --name-only --diff-filter=A \
    | grep -E '\.md$' \
    | grep -vE "$ORPHAN_EXCLUDE" || true)
  ```
- **Configurable instead of hardwired** (field note taken up) — projects can
  override `ORPHAN_EXCLUDE` to extend/replace their own path conventions.
- **§9 clarification:** the field proposal named "§6 References"; the real mandatory section is
  **§9 Referenzen** (`doc-architecture-proposal.md`). The story targets §9.
- **`migrate_boo_92()`** in `migrate-to-v2.sh`: idempotently patches an already-installed
  `.claude/hooks/orphan-check.sh` to the `ORPHAN_EXCLUDE` variant (backup `.bak`) — only
  if `ORPHAN_EXCLUDE` is not yet present. Without an installed hook (the normal case, optional
  hub hook): skip. Registration of `BOO-92` in `ALL_ISSUES`.

## Design decision

- **Fix in the doc snippet** (`hooks-setup.md`), since orphan-check only exists as a doc snippet and
  no real canonical `.sh` is scaffolded.
- **Exceptions via an overridable variable** (`ORPHAN_EXCLUDE`), not hardwired — the
  cleaner upstream form that the field itself suggested.
- **Default exceptions = specs + backlog records** — matching the INTENTRON path conventions.
- **Target §9** (repo reality), not §6 (field-proposal typo).

## Verified

- `specs/BOO-92.md` and `docs/project/backlog/record-*.md` are excluded by the filter.
- A new `.md` at any other location (e.g., `docs/foo.md`, `README.md`) **continues** to be checked
  against the hub.
- `ORPHAN_EXCLUDE` is overridable via env.
- `migrate_boo_92` patches an existing `orphan-check.sh` byte-cleanly (backup `.bak`), is
  idempotent (second run = skip), the patched hook is valid bash (`bash -n`).
- DE/EN snippet equivalent; `git diff --check` clean.

## Rollout

Additive and backward-compatible — one variable + one `grep -vE`, no new dependency.
Default behavior for all other `.md` stays identical; only work-item docs are excluded.
Existing projects with an installed `orphan-check.sh` are idempotently patched via `migrate_boo_92()`;
projects without the optional hook are not affected.

## Effect

Stories no longer create an artificial hub entry; the hub protection for real doc artifacts
is preserved.

## References

- Spec: `specs/BOO-92.md`
- Release overview: `docs/releases/v0.6.0-overview.md` (Wave AB)
- Migration: `migrate_boo_92()` in `bootstrap/scripts/migrate-to-v2.sh`
- Linear: BOO-92
