# Runbook: Audit Perspective — CISO/CIO/CTO verifies rule compliance

> **Purpose.** This runbook describes how an auditor (CISO/CIO/CTO or an external reviewer)
> verifies, from a pure **audit perspective**, that the dev team followed the framework rules: Did
> the linters fire? Did the GitHub Actions run and go green? Are reports and evidence present? Is
> there an unbroken audit trail from the commit back to the intent and the session?
>
> This is **not new machinery** — all evidence already exists in the repo. This runbook is a pure
> **aggregator**: it bundles the existing gates, hooks, workflows, and reports into a checkable
> list. An auditor should be able to look up here *which question* is answered by *which evidence*
> at *which location* — without having to read the whole HANDBUCH first.

## Auditor perspective (lightweight)

An auditor does not want to read the code. They want **evidence**: reproducible artifacts that show
the process ran. The framework is built so that every governance rule leaves a visible artifact — a
spec, a hook block, a CI run, a report. The auditor checks the existence and status of these
artifacts, not the implementation behind them.

Three principles apply to every check:

1. **Evidence before assertion.** "The linter ran" does not count — the SARIF report in the CI
   artifact counts.
2. **CI is the authoritative source.** Local reports under `journal/reports/` are gitignored and
   therefore ephemeral. Anything that must be persistently provable lives in the CI artifact
   (30-day retention) or in committed artifacts (specs, DPO reports).
3. **Convention ≠ enforcement.** Some safeguards (the four-eyes principle) are documented operator
   discipline, not an enforced mechanism. The auditor must know what is *enforced* versus what is
   *agreed* (see caveats).

## Audit question → Evidence → Location

| Audit question | Evidence/Mechanism | Artifact/Location |
|---|---|---|
| Did every change have a documented intent? | `spec-gate.sh` blocks any commit without a spec | `specs/{ISSUE-ID}.md`; `verify-setup` check 3 |
| Is every commit traceable to a prompt/session? | `## Session-Referenz` block + `audit-trace.sh` | `specs/*.md`; `bootstrap/scripts/audit-trace.sh`; CONVENTIONS §Audit-Trail (BOO-19) |
| Did linters/SAST/coverage fire locally? | `/implement` writes SARIF/JUnit/coverage per iteration | `journal/reports/local/{date}_{story}/` + `meta.json` (Appendix E). Caveat: `journal/reports/` is gitignored → CI artifacts are the persistent source |
| Did GitHub Actions run/go green? | CI workflows + aggregator uploads reports as artifact (30-day retention) | `journal/reports/ci/run-{id}/`; workflows `docs-drift.yml` / `hook-sources.yml` / `ruff-hooks.yml` |
| Can a merge bypass green gates? (Bypass) | Branch protection required status checks; CI as Layer 3 against `--no-verify` | `bootstrap/scripts/setup-branch-protection.sh` (BOO-29) |
| Is data-protection/compliance proven? | `dpo-audit.py` → PASS/GAP/REVIEW-NEEDED; sprint-review 7c | `dpo/reports/<date>_audit.{md,json}`; catalogs `dpo/controls/*.yml` |
| Is the setup itself verified (hooks/tools)? | `verify-setup.sh` read-only PASS/WARN/FAIL | `bootstrap/references/verify-setup.sh` (Appendix T) |
| Were findings moved into the backlog? | Sprint-review creates one story per GAP (label `privacy`) | `sprint-review/SKILL.md` step 7/7c |
| Are model overrides traceable? | `override_audit[]` in `meta.json` | `meta.json.override_audit` |
| Four-eyes on sensitive paths? | Convention (NOT enforced) — `git log` / `git blame`, author of gate ≠ author of change | HANDBUCH Appendix R §Four-Eyes |
| Does the project live its `governance_mode`? | Sprint-review step 1 "Governance Drift" | `sprint-review/SKILL.md`; CONVENTIONS governance matrix |

## How to check, concretely

The steps below can be worked top to bottom as an audit pass. All commands are read-only — they
change nothing in the repo.

### 1. Intent completeness: does every issue have a spec?

Every commit with an issue reference needs a spec — enforced by `hooks/spec-gate.sh`. Verify that a
spec file exists for every issue mentioned in the backlog/branch:

```bash
ls specs/                       # all existing specs
git log --oneline | head -30    # commits with issue prefix (e.g. "BOO-42: ...")
```

If a referenced issue has no `specs/{ISSUE-ID}.md`, the commit should never have gone through — or
the gate was bypassed (see step 5).

### 2. Reconstruct the audit trail: commit → intent → session

For each spec, `audit-trace.sh` reconstructs the path from the commit back to the conversation log:

```bash
bash bootstrap/scripts/audit-trace.sh BOO-42
```

The script reads the `## Session-Referenz` block from `specs/BOO-42.md` (commit SHA + session ID +
log path), shows the git commit diff, and renders the session turns. Missing fields are explicitly
reported as `unbekannt` (unknown) — which is itself an audit signal.

### 3. Inspect local gate evidence (with a caveat)

`/implement` writes SARIF (linter/SAST), JUnit (tests), and coverage per iteration:

```bash
ls journal/reports/local/        # if present — gitignored, so only on the operator machine
cat journal/reports/local/*/meta.json   # iteration metadata per story
```

Important: `journal/reports/local/` is gitignored and therefore not the authoritative audit
evidence. For persistent proof, go straight to the CI artifacts (step 4).

### 4. Check CI status and CI artifacts

The GitHub Actions are the authoritative, persistent source. Check the run and status:

```bash
gh run list --limit 20
gh run view <run-id>
gh run download <run-id> --name ci-reports-<run-id>   # SARIF/JUnit/coverage as artifact (30-day retention)
```

The workflows `docs-drift.yml`, `hook-sources.yml`, and `ruff-hooks.yml` live under
`.github/workflows/`. Every tool workflow ends with collect-into-`run-{id}/` + upload-artifact.

### 5. Bypass check: could someone merge past the gates?

Local hooks can be bypassed with `git commit --no-verify`. The defense against this is branch
protection with required status checks (CI as Layer 3). Check the active configuration:

```bash
gh api repos/{owner}/{repo}/branches/main/protection
```

Expect `required_status_checks` (the CI checks) and `required_pull_request_reviews`. This is set by
`bootstrap/scripts/setup-branch-protection.sh` (BOO-29). If protection is missing, a local
`--no-verify` bypass is not caught by CI.

### 6. Prove data-protection compliance

The DPO audit runner produces a reproducible, committed report pair:

```bash
ls dpo/reports/                              # <date>_audit.md + <date>_audit.json
cat dpo/reports/<date>_audit.md              # PASS / GAP / REVIEW-NEEDED per control
ls dpo/controls/                             # versioned catalogs: gdpr.yml, ndsg.yml
```

`dpo/scripts/dpo-audit.py` works the catalog deterministically: mechanical checks yield PASS/GAP,
judgment checks yield REVIEW-NEEDED. The auditor reviews the GAP list and whether the REVIEW-NEEDED
items were confirmed by the operator.

### 7. Findings tracking and governance drift

Sprint-review closes the loop: one backlog story per open GAP (label `privacy`,
`sprint-review/SKILL.md` step 7c), and step 1/1b checks whether the project actually lives its
declared `governance_mode` (CONVENTIONS governance matrix) — deviations are documented as
`Governance Drift` in the sprint report.

```bash
verify-setup.sh   # read-only PASS/WARN/FAIL over hooks, toolchain, core artifacts (Appendix T)
git blame -- path/to/sensitive/file   # four-eyes indicator: author of the review-ok gate ≠ author of the change
```

## Caveats

- **`journal/reports/` is gitignored — CI artifacts are authoritative.** Local reports under
  `journal/reports/local/` are short-lived signal and live only on the operator machine. For
  defensible audit proof, the CI artifacts under `journal/reports/ci/run-{id}/` apply
  (GitHub Actions artifact, **30-day retention** — not retrievable after that, download/archive in
  time).
- **Session-log retention.** `audit-trace.sh` reconstructs the conversation log only as long as the
  session log exists. The script recommends keeping session logs for 90 days, then archiving or
  deleting them. Older logs can no longer be rendered; commit SHA and spec remain, the prompt
  history does not.
- **Four-eyes is convention, not enforced.** The framework does **not** currently enforce the
  four-eyes principle for sensitive and personal-data paths (BOO-72 explicitly excludes
  enforcement). It is documented operator discipline (HANDBUCH Appendix R §Four-Eyes). The auditor
  checks it manually via `git log` / `git blame` — the indicator is: author of the
  `review-ok`/`privacy-ok` gate ≠ author of the actual change.
