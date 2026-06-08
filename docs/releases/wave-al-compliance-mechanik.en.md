# Wave AL — EU AI Act lifecycle + compliance mechanics docs (BOO-106)

> 🌐 **Language:** English (this file) · [🇩🇪 Deutsch](wave-al-compliance-mechanik.md)

**Problem before:** The EU AI Act was only wired into bootstrap (phase 4.4n-bis) + the periodic audit (sprint-review 7c) — **not** into `/ideation`/`/implement` the way Privacy is. And there was no document explaining the compliance mechanics as a whole (gates vs. catalogues, automatic vs. REVIEW-NEEDED) so that a CISO/operator can follow them.

**What is there now:**

- **`docs/compliance/compliance-mechanik.md` (+ `.en.md`)** — end-to-end: two mechanisms (gates = per-code hard stop in `/implement`; catalogues = periodic doc audit in `/sprint-review`), touchpoint table, both lifecycles (Privacy + EU AI Act), clarifications.
- **`/ideation` step 0e-bis** (DE+EN): EU AI Act pre-flight (`ai_act_relevant`), soft, add-on-gated.
- **`/implement` step 5.5c** (DE+EN): soft hint to keep AI_SYSTEM.md current — NO hard stop (the AI Act is governance/docs, not a linter topic).

**Effect:** The EU AI Act is now visible across the whole lifecycle just like Privacy (planning → code → periodic audit), and the mechanics are explained in a CISO-grade document. The binding check remains the catalogue audit (7c) + REVIEW-NEEDED.

Spec: `specs/BOO-106.md`. Release: v0.7.3.
