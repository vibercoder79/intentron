# Wave CB — EN catch-up for the 43 legacy wave release notes: DE+EN parity, retroactively (BOO-174)

> 🌐 **Language:** English (this file) · [🇩🇪 Deutsch](wave-cb-en-parity-altwaves.md)

**What is now in place:** All 43 wave release notes that predate the DE+EN parity rule (docs DoD, BOO-180) and were German-only now have a faithful English mirror. The release index is regenerated in DE and EN — no more *(DE only)* markers. Pure docs, no code change.

## Problem before

Found during the release-notes audit (BOO-173): 43 `wave-*.md` (from `wave-a` to `wave-as`, incl. `wave-b`…`wave-z`) had no `.en.md` mirror. They were marked as *(DE only)* in the index. The DE+EN parity rule therefore only applied to new waves — the existing stock stayed half-German.

## Changes

- **43 EN mirrors NEW** — one `wave-*.en.md` per legacy wave: same structure, headings, tables, ordering; code identifiers, BOO numbers, paths, links, wave letters and versions carried over verbatim (anti-fabrication).
- **Language switcher added to all 43 DE sources** — `🌐` line directly under the H1, otherwise unchanged in content (+2 lines each, 0 deletions).
- **Release index regenerated** — `README.md` (DE): EN link added per entry. `README.en.md` (EN): English title from each EN mirror's H1 + `· [DE]` link, `*(DE only)*` removed. Wave counter 81 → 82.

## Approach

Agentic in 8 small, size-balanced batches across disjoint file clusters (memory: long DE+EN sub-agents time out → batch small). Per batch: read the DE source → write the EN mirror → add the switcher. Then lead cross-check: BOO numbers, URLs, backtick identifiers and link targets compared DE↔EN.

## References

- Spec: `specs/BOO-174.md`
- Docs Definition of Done: `docs/releases/wave-bw-doku-definition-of-done.md` (BOO-180)
- Release index convention: `docs/releases/wave-bt-release-index.md` (BOO-173)
- Previous wave: `docs/releases/wave-ca-observability-sichtbar.md`
