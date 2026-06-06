# Wave BK — /sprint-run: post-story gate assertion (BOO-165)

**What's now in place:** After every story run, `/sprint-run` **machine-verifies** against the `meta.json` that no mandatory gate was silently skipped — a new **step 4.5b** between remote-CI wait and merge. Hardens the previously prompt-driven gate enforcement. `sprint-run` v1.0.0 → v1.1.0. DE+EN.

## Stories
- **BOO-165** — step 4.5b post-story gate assertion + docs/sketch follow-up.

## Changes (DE+EN)
- **`sprint-run/SKILL.md` (+EN)**: new step 4.5b (table row + section + legitimacy matrix); daemon-mode note; **v1.0.0 → 1.1.0**.
- **New `sprint-run/references/gate-assertion.md` (+EN)**: assertion logic, legitimacy rule, pseudocode.
- **`sprint-run/README.md` (+EN)**: gate-assertion section + step table; v1.1.0.
- **HANDBUCH Anhang/Appendix AD (DE+EN)**: 4.5b in the daemon-loop table, "gate assertion" section, error handling extended.
- **`docs/runbooks/sprint-run.md` (+EN)**: failure scenario "unjustified gate skip → story back".
- **Sketches updated (DE+EN)**: `sprint-run-flow` + `story-breakdown` — assertion node between CI and merge.

## Impact
A silently skipped lint/test/security check can no longer pass the sprint unnoticed: alongside the prompt-driven gate execution (layer 1) and the remote-CI gate (BOO-148, layer 2), there is now machine verification against `meta.json` as a backstop for layer 1.

## Scope
Pure orchestrator addition; `/implement`, `/backlog`, `/sprint-review` unchanged (only `meta.json` is read). `change_type: tooling`. Non-code skips stay legitimate (change_type-aware). Wave letter **bk** (bi = sprint-run BOO-157, bj = role-runbooks BOO-158, bh = knowledge-onboarding-sketches). Also contains the hotfix `wave bi→bj` for role-runbooks (resolving the cross-session collision with the already-released `wave-bi-sprint-run`).

## References
Spec: `specs/BOO-165.md`. Branch: `feat/boo-165-gate-assertion`. Skill: `sprint-run/SKILL.md` (4.5b) + `references/gate-assertion.md`. HANDBUCH Appendix AD. Related: BOO-157 (`/sprint-run`), BOO-148 (remote-CI loop), BOO-36/84 (`meta.json`). Operator source: Tobias, 2026-06-06.
