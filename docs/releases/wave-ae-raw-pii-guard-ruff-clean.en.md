# Wave AE — raw-pii-guard ruff-clean + Hook-Lint-Gate (BOO-95)

> 🌐 **Language:** English (this file) · [🇩🇪 Deutsch](wave-ae-raw-pii-guard-ruff-clean.md)

**Linear:** [BOO-95](https://linear.app/owlist/issue/BOO-95/) · Source: upstream field feedback privacy-proxy / 2XT (Martin), 2026-06-01

## Problem

The `bootstrap/references/hooks/raw-pii-guard.py` shipped in Wave AC (BOO-93) did **not** pass a
common strict Ruff profile (`line-length 100`, flake8-bandit `S`) — **9× E501**
(German docstrings/f-strings/argparse help texts) + **1× S607** (`subprocess.run(["git", …])`
with a partial executable path). The file is copied byte-identically into user projects via
`migrate_boo_93()`; during field installation (project with `max-line-length 100`) it blocked the
**pre-commit gate** — the field had to build a local `per-file-ignore` exception. The irony: the
security guard fails the security linter. Root cause behind the symptom: the framework so far does
**not** lint its **own** shipped Python hooks — no repo-wide Ruff profile, no CI stage.

## Stories

| Story | Content | Status |
|-------|--------|--------|
| **BOO-95** | Make raw-pii-guard.py ruff-clean (smooth the source) + framework-owned hook-lint gate | ✅ done |

## What changes

- **Part A — source smoothed (no behavioral change):**
  - **S607:** `git` resolved to an absolute path at runtime via `shutil.which("git")`
    (`None` → empty list, existing `FileNotFoundError` handling stays). The remaining
    **S603** (advisory, not autofixable) is suppressed via a targeted `# noqa: S603` with a rationale
    at the call site — fixed argv list, no `shell=True`, no user input.
  - **9× E501 wrapped:** `_sink_token` docstring made multi-line; three `findings.append(…)` lines
    shortened via a new helper method `_record(node, sink_name, field)` (which also removes
    duplication); long `print` via implicit string concatenation; three argparse `help=`
    texts onto continuation lines; `strict` assignment bracketed across multiple lines. `--self-test` still green.
- **Part B — hook-lint gate (root-cause fix):**
  - `bootstrap/references/hooks/ruff.toml` (single-source profile: `line-length = 100`,
    `select = ["E", "F", "S"]`, local + CI).
  - CI workflow `.github/workflows/ruff-hooks.yml` (pinned Ruff `0.15.11`) that lints the
    canonical hooks on every hook/profile touch. Future `*.py` hooks are captured automatically.

## Design decision

- **Genuinely fix S607** (`shutil.which`) instead of suppressing — an absolute path is
  in fact more secure.
- **Suppress S603 via a targeted `# noqa`** instead of a blanket ignore — the opposite of the
  downstream stopgap. The rationale sits at the code.
- **Gate as its own workflow** (`ruff-hooks.yml`) instead of extending `hook-sources.yml`
  — separate responsibilities (drift guard vs. lint), its own `paths` trigger.
- **Profile as `ruff.toml` in the hooks folder** (not repo-wide) — local + CI use the same
  source, no assumption about the lint strategy of the rest of the (non-Python) repo.
- **Target profile `line-length 100`** (field requirement), deliberately not 88 (would tear the German
  docstrings apart more strongly).

## Verified

- `ruff check bootstrap/references/hooks/` (E,F,S @100) → **0 findings**.
- `python3 raw-pii-guard.py --self-test` → `SELF-TEST OK`; `py_compile` without error.
- Negative probe: a built-in `*.py` violation makes `ruff-hooks` fail (throwaway file).
- No change to detection logic/CLI/exit codes of `raw-pii-guard.py`.

## Effect

The shipped guard now passes a strict Bandit profile itself; downstream no longer needs a
`per-file-ignore` exception and can roll it back. Self-dogfooding via CI prevents
recurrence.

## References / Release

- Branch `feat/boo-95-ruff-clean`. Release: **v0.6.0 (Wave AE)** — see
  `docs/releases/v0.6.0-overview.md`, detail spec `specs/BOO-95.md`.
