# Gate assertion — post-story verification against meta.json

Reference for `/sprint-run` step 4.5b. Machine verification that `/implement` executed all
mandatory gates per story (or skipped them only legitimately) — the safeguard against a
**silently** skipped lint/test/security check.

## Source: meta.json (BOO-36/84)

In step 6f-bis `/implement` writes `journal/reports/local/<YYYY-MM-DD_HHMM>_<STORY>/meta.json`.
Relevant fields:

- `change_type` — `code` (default) | `workflow` | `config` | `infrastructure` | `content`
- `skipped_gates` — list of skipped gates (with reason)
- `override_audit` — documented operator overrides (e.g. coverage < 80% with justification)
- `iterations` — iterations per gate

## Legitimacy rule

An entry in `skipped_gates` is **legitimate** exactly when:

1. it is covered by `change_type` — in non-code mode (`/implement` step 5.7) the
   code gates 6a/6a-bis/6a-tris/6a-quart are legitimately skipped; **or**
2. it is documented in `override_audit` with a justification (operator override).

Otherwise → **unjustified skip → story fail**.

Addendum for non-code stories: the gates 6c (architecture quick check),
6d (smoke test), 6e (security findings) that are **hard** in non-code mode must carry evidence —
if it is missing → fail.

If `meta.json` is missing entirely → fail (gate run not provable, no "silently green").

## Pseudocode

```text
meta = read(journal/reports/local/<run>/meta.json)        # missing -> FAIL
for g in meta.skipped_gates:
    if g.gate in CODE_GATES and meta.change_type in {workflow,config,infrastructure,content}: ok
    elif g.gate in meta.override_audit: ok
    else: FAIL(story, gate=g)
if meta.change_type != "code":
    for g in [6c, 6d, 6e]:
        if not has_evidence(meta, g): FAIL(story, gate=g)
PASS   # only then merge (step 4.6)
```

## On fail

- Story back to `Backlog` (In Progress → Backlog).
- Operator notify: story ID + which gate + reason.
- No merge. `daemon_fail_policy` (`stop` | `continue`) determines whether the sprint halts.

## Classifying the three layers

- **Layer 1** — `/implement` gates (step 6): prompt-driven.
- **Layer 2** — remote CI gate before merge (BOO-148): mechanical.
- **4.5b is the machine bridge:** verifies layer 1 against the machine output (`meta.json`),
  **before** layer 2 merges. Does not change `/implement` — only reads its `meta.json`.

Sketch: `docs/sprint-run-flow.png` + `docs/story-breakdown.png` (HANDBUCH Appendix AD).
