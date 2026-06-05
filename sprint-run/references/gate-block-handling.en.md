# Gate-Block Handling — pause/resume protocol

Reference for `/sprint-run` step 4.4. Security-critical: the daemon must
**never** bridge governance gates automatically.

## Which gates pause the daemon?

| Gate | Source (`/implement`) | Trigger | Approval token |
|---|---|---|---|
| Sensitive-Paths | step 5.5 (BOO-18) | changed file matches `.claude/sensitive-paths.json` | `review-ok: <name> - <comment>` |
| Personal-Data | step 5.5b (BOO-69) | `personal_data: true` + match in `.claude/personal-data-paths.json` | `privacy-ok: <name> - <comment>` (GDPR Art. 25) |

Both can strike at the same time — then first `review-ok` (technical), then `privacy-ok`
(legal). No confirmation replaces the other.

## Protocol

1. **Pause.** `/implement` stops at its gate. `/sprint-run` does **not** continue —
   no merge, no worktree cleanup, no next story.
2. **Notify.** Operator hint with **story ID**, **gate type** and **concrete path/reason**.
   In daemon mode: persistent note (e.g. Linear comment) instead of just console output.
3. **Wait.** The daemon stays blocked until the operator delivers the matching approval
   token. **No** timeout resume.
4. **Resume.** After approval `/implement` records the block in the spec file (`## Human Review`
   or `## Privacy Review`) and continues; `/sprint-run` resumes the loop.
5. **Abort (optional).** If the operator does not want to approve: story back to `Backlog`,
   remove worktree, next story per `daemon_fail_policy`.

## Prohibitions

- ❌ No automatic bypass of a gate — not even in `--auto` mode.
- ❌ No timeout-based auto-resume.
- ❌ No approval "in advance" for upcoming stories — each approval applies to exactly one block.

## State machine

```
running ──(gate hit)──▶ paused ──(review-ok / privacy-ok)──▶ resumed ──▶ running
                          │
                          └──(operator rejects)──▶ aborted (story → Backlog)
```

Sketch: `docs/gate-block-handling.png` (HANDBUCH Appendix AD).
