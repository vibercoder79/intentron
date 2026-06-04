# Wave BC — eslint.config.mjs DE/EN base block aligned (Linear BOO-146)

**What's now in place:** The `eslint.config.mjs` template had drifted in content between the DE SSoT and the EN mirror — an English-speaking operator got a different ESLint config on bootstrap (no `files` key, `sourceType: module`, only 2 globals) than a German-speaking one (commonjs + 12 Node globals + `ignores`). **German is canonical**; the EN base block was aligned 1:1 to DE. Pure template consistency, no runtime code.

## Story

- **Linear [BOO-146](https://linear.app/owlist/issue/BOO-146)** (repo spec slot `specs/BOO-150.md` — see the numbering note there) — DE/EN base-block alignment. Follow-up from BOO-141 (Wave BA), where only the frontend block was unified.

## Change

- **`bootstrap/references/file-templates.en.md`** §`eslint.config.mjs`: base house-rules block aligned to the DE variant — `files: ['**/*.js','**/*.mjs']`, `sourceType: 'commonjs'`, 12 Node globals, 4 override rules, `ignores` block. `diff` against DE now shows only comment differences (German/English).
- Deliberately not adopted: the richer EN 13-rule set (redundant with `eslint-config-airbnb-base`, which both configs already load — lightweight principle).
- BOO-141 frontend/TSX block (`...globals.browser` + `React: 'readonly'`) unchanged.

## Scope boundary

Pure consistency fix. **Not** part of this wave: normalising the cross-session number/wave drift (repo specs 146–149 = Linear 147–150; duplicate `wave-ba`/`wave-bb`) — handled as a separate cleanup story.

## References

Spec: `specs/BOO-150.md` (= Linear BOO-146). Branch: `feat/boo-146-eslint-config-de-en-align`. Related: BOO-141 (frontend globals, Wave BA), BOO-2 (ESLint ruleset).
