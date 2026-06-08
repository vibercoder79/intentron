# Wave AQ — 10 legacy sketches to EN (BOO-111)

> 🌐 **Language:** English (this file) · [🇩🇪 Deutsch](wave-aq-sketch-en-parity.md)

**What is there now:** the last 10 German-only sketches have been brought to English — so all skill/doc sketches are DE+EN parity and the English HANDBUCH shows English diagrams throughout.

## Stories
- **BOO-111** — Bring the 10 legacy sketches (predating the DE+EN rule) to EN.

## Changes
- 10 × `.en.excalidraw` + `.en.png`: `boo-69-privacy-pipeline`, `boo-70-deployment-scenarios`, `boo-71-sovereignty-stack`, `boo-72-multi-operator-3-layer`, `boo-84-token-efficiency`, `codex-onboarding-flow`, `multi-project-onboarding`, `post-install-verification`, `skill-install-locations`, `vault-harvest-solo-vs-team`.
- Generated via index mapping from the DE sources — identical coordinates/colors (OWLIST), only text translated.
- `HANDBUCH.en.md`: 11 embed references (boo-72 has 2) switched from `<sketch>.png` to `<sketch>.en.png`.

## Smoke test
- All 10 rendered; spot-checked visually (boo-72, boo-84, post-install) — no overflow/clipping.
- HANDBUCH.en.md: 0 remaining DE PNG references for the 10 sketches.

## References
Spec: `specs/BOO-111.md`. Release: v0.7.7.
