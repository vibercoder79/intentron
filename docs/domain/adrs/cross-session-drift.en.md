# ADR: Cross-session number / wave drift — accepted + documented

> Status: **Accepted** (2026-06-04, BOO-153). Operator decision: **Option B**. DE: [`cross-session-drift.md`](cross-session-drift.md).

## Context

On 2026-06-03/04 several parallel Claude sessions independently assigned **BOO numbers** *and* **release wave letters** without checking Linear or `docs/releases/`. Result: repo spec numbers and Linear numbers are offset by **+1**, and three wave letters are doubly assigned. Related: memory "Parallel git sessions: verify against remote".

## Decision

**Option B** — **accept + document** the offset as a convention, do **not** rename merged "Done" code. Option A (full repo==Linear renumber) was **rejected**: it touches merged, completed specs/`migrate_boo_*` functions (audit trail, possibly already-retrofitted VPS) — risk without functional benefit. A **process guard** stops future drift.

## Mapping: repo spec no. ↔ Linear no.

| Topic | Repo spec | Linear |
|---|---|---|
| SARIF permissions | `BOO-146` | **BOO-147** |
| Remote CI loop | `BOO-147` | **BOO-148** |
| Project-type marker | `BOO-148` | **BOO-149** |
| Branch-protection review count | `BOO-149` | **BOO-150** |
| eslint DE/EN base block | `BOO-150` | **BOO-146** |
| Multi-user VPS | `BOO-151` | `BOO-151` ✅ aligned |
| Clone portability | `BOO-152` | `BOO-152` ✅ aligned |
| This drift cleanup | `BOO-153` | `BOO-153` ✅ aligned |

→ The +1 offset affects **only** the CI-hardening gap fixes (repo 146–149 = Linear 147–150) plus the eslint story (repo 150 = Linear 146). From BOO-151 onward everything is aligned (Linear-first checked).

## Doubly assigned wave letters (accepted, allowlisted in the guard)

| Wave | Topic 1 | Topic 2 |
|---|---|---|
| `BA` | `maschinen-kontext` (Linear BOO-145) | `nextjs-ci-hardening` (repo BOO-140–143) |
| `BB` | `ci-hardening-gaps` (repo BOO-146–149) | `multi-user-vps` (Linear BOO-151) |
| `BC` | `eslint-de-en-align` (Linear BOO-146) | `klon-portabilitaet` (Linear BOO-152) |

## Process guard (prevents recurrence)

1. **Automated:** `.github/scripts/docs_drift_check.py` check 5 — **new** doubly assigned wave letters in `docs/releases/` → FAIL. The three old duplicates above are allowlisted (`ba`, `bb`, `bc`).
2. **Convention (manual):** before assigning **(a)** a BOO number → check Linear (`list_issues`, team "Bootstrapping Evolution"); **(b)** a wave letter → check `docs/releases/` (highest two-letter wave +1).

## Consequences

- Repo spec nos. 146–150 stay permanently +1 offset to Linear — **documented here**, no hidden risk.
- No broken links / no audit-trail confusion from renaming.
- The PR-#48 mis-attachment on Linear BOO-146 was removed (title auto-link).
- Future number/wave drift is caught by the guard.
