# Runbook: Unit Tests — flow, gate, evidence

> **Audience:** operators who build with `/implement` and want to understand how unit tests run in the framework — where the reports land, how the test gate decides, and how the anti-placeholder check fires. In under 10 minutes. DE: [`unit-tests.md`](unit-tests.md).

## When this runbook?

You're implementing a story with `/implement` and want to understand the **unit-test part**: why the gate blocks, how to raise diff coverage, what a "placeholder test" is, and where the test evidence lives for the audit. For the operator short version see [HANDBUCH chapter 8c-bis](../../HANDBUCH.en.md).

**Boundary:** this is **only about unit tests** — individual functions/modules in isolation. Integration and E2E tests (multiple components after deployment) are a separate topic **not** covered here. There is deliberately no integration-test skill.

## In one sentence

Unit tests run in the **6a-quart** test gate of `/implement`, which checks **two** things — *enough* tests (diff coverage ≥ 80 %) **and** *real* tests (anti-placeholder check) — and leaves each iteration as JUnit XML, coverage JSON, and a `meta.json` counter under `journal/reports/local/<run>/`.

---

## The 6a-quart test gate at a glance

The step runs **in the skill, not in the pre-commit hook** — a test run can take minutes and would blow the hook's 10-second budget. Per iteration this loop runs:

1. **Increment iteration counters** (`ITER_TESTS`, `ITER_COVERAGE` in sync).
2. **Test run** with coverage output **and** JUnit XML (per-stack commands below).
3. **`coverage-check.sh`** correlates the added lines from `git diff --cached -U0` with the coverage data → diff coverage.
4. **Copy the final coverage** once into the run directory.
5. **Gate decision** (thresholds below). On block: add tests, repeat from step 2.

**At most 5 iterations.** If the gate isn't green by iteration 5: STOP, operator intervention (manual test-reach plan or split the story).

### Gate thresholds (diff coverage)

| Diff coverage | Behaviour |
| -- | -- |
| **≥ 80 %** | **Pass** — proceed to step 6b. |
| **60–80 %** | **Warn** — operator decides, reason in the Linear comment. |
| **< 60 %** | **Block** — add tests, repeat the iteration. |

Thresholds are constants in the script (`COVERAGE_PASS=80`, `COVERAGE_WARN=60`) and overridable via env var: `COVERAGE_PASS=90 bash .claude/hooks/coverage-check.sh`.

### Special cases (gate skipped)

- **No coverage data** (no `coverage-final.json` / `coverage.json`): gate skipped with the hint *"re-run /bootstrap for the test setup"*.
- **Diff only test files / configs / docs**: gate skipped.
- **Diff with 0 added lines**: gate skipped.

---

## Local test run per stack

The commands produce coverage **and** the JUnit XML in one pass. `RUN_DIR` is the run directory under `journal/reports/local/<run>/`, `ITER_TESTS` the incremented iteration counter.

### Node (jest + c8)

```bash
npx c8 --reporter=json --reporter=text-summary \
  npx jest --reporters=default --reporters=jest-junit
# JEST_JUNIT_OUTPUT_FILE="${RUN_DIR}/tests-iter${ITER_TESTS}.junit.xml"
# coverage output: coverage/coverage-final.json
cp coverage/coverage-final.json "${RUN_DIR}/coverage-final.json"
```

`jest-junit` writes the JUnit XML via the env var `JEST_JUNIT_OUTPUT_FILE`; `c8` provides coverage as `coverage/coverage-final.json`.

### Python (pytest + cov)

```bash
pytest --cov --cov-report=json \
  --junit-xml="${RUN_DIR}/tests-iter${ITER_TESTS}.junit.xml"
# coverage output: coverage.json
cp coverage.json "${RUN_DIR}/coverage-final.json"
```

`pytest` writes the JUnit XML directly via `--junit-xml=…`, coverage as `coverage.json`.

> **JUnit-XML convention:** both `pytest` and `jest-junit` write standard JUnit XML — parsable by `/sprint-review`. If the test runner can't emit JUnit XML (e.g. Mocha without a reporter), test persistence is skipped: `ITER_TESTS` is not incremented, `meta.json.iterations.tests` stays 0 — the coverage run itself proceeds.

---

## Where the reports land

Everything under `journal/reports/local/<run>/`:

| File | Content |
| -- | -- |
| `tests-iter{N}.junit.xml` | Test results per iteration (which tests, pass/fail) |
| `coverage-final.json` | Diff coverage of the new code (final state) |
| `meta.json` | among others `iterations.tests` (test-loop counter), `skipped_gates` |

These files live in **persistence zone C** (local, gitignored) — ephemeral working signal, **not** audit evidence on their own. The load-bearing proof comes from the CI artifacts (zone B) or the coverage trend in the sprint frontmatter (zone A). Details: [`audit-perspective.en.md`](audit-perspective.en.md).

---

## Anti-placeholder check (BOO-177) — real tests, not just coverage

Coverage measures **whether** a line was touched by a test — not **whether the test checks anything**. Trivial tests raise the number without testing anything:

- empty test body,
- `expect(true).toBe(true)` / `assert True`,
- `it.skip` / `xit` / `@pytest.mark.skip` **without** a reason.

The **anti-placeholder check** is therefore a **dedicated, targeted check on test files** (the `anti-placeholder-check.py` hook — AST for Python, heuristics for JS/TS; **not** a linter — linters check style/types, not test meaningfulness). It fires in the same 6a-quart test gate and flags exactly these patterns. This adds the missing dimension to the coverage number: coverage = *"enough tests"*, anti-placeholder = *"real tests"*. Background: the same root problem as BOO-176 (*"agent gamed the gate"*), here at the test level. Source: [`specs/BOO-177.md`](../../specs/BOO-177.md).

**What to do when the check flags:** fill the flagged test with real assertions (input → check the expected output). If a skip is **intentional**, add a reason to the skip — then it's a documented, traceable skip instead of a silent placeholder.

---

## Troubleshooting

| Symptom | Cause | Fix |
| -- | -- | -- |
| Gate blocks with `< 60 %` | New code without a test | Write tests for the added lines, repeat the iteration (max 5). |
| Gate "Warn" (60–80 %) | Partial coverage | Either add tests or accept Warn — reason in the Linear comment. |
| `meta.json.iterations.tests` stays 0 | Runner without a JUnit-XML reporter (e.g. Mocha) | Configure a JUnit reporter (coverage still runs). |
| "Gate skipped — test setup missing" | No `coverage-final.json`/`coverage.json` | Re-run `/bootstrap` for the test setup. |
| Anti-placeholder check flags a real test | Test without an assertion / empty body | Add real assertions; justify skips. |
| 5 iterations without green | Reach too large for one story | STOP → operator: test-reach plan or split the story. |

---

## Further reading

| Topic | Source |
|---|---|
| Operator short version of unit tests | [HANDBUCH chapter 8c-bis](../../HANDBUCH.en.md) |
| Test evidence from the audit view (existence **and** quality) | [`audit-perspective.en.md`](audit-perspective.en.md) |
| Reports convention, `meta.json` schema, persistence zones | [HANDBUCH Appendix E](../../HANDBUCH.en.md) |
| Full gate flow of `/implement` | [`implement/SKILL.en.md`](../../implement/SKILL.en.md) step 6a-quart |
| Look up terms | [`../glossar.en.md`](../glossar.en.md) |

---

> *German version: [`unit-tests.md`](unit-tests.md).*
