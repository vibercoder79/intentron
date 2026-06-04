# Wave BC — eslint.config.mjs DE/EN-Basis-Block angeglichen (Linear BOO-146)

**Was jetzt da ist:** Die `eslint.config.mjs`-Vorlage war zwischen DE-SSoT und EN-Spiegel inhaltlich auseinandergelaufen — ein englischsprachiger Operator bekam beim Bootstrap eine andere ESLint-Config (kein `files`-Key, `sourceType: module`, nur 2 Globals) als ein deutschsprachiger (commonjs + 12 Node-Globals + `ignores`). **Deutsch ist kanonisch**; der EN-Basis-Block wurde 1:1 an DE angeglichen. Reine Template-Konsistenz, kein Runtime-Code.

## Story

- **Linear [BOO-146](https://linear.app/owlist/issue/BOO-146)** (Repo-Spec-Slot `specs/BOO-150.md` — siehe Nummern-Hinweis dort) — DE/EN-Basis-Block-Angleichung. Folge aus BOO-141 (Wave BA), wo nur der Frontend-Block vereinheitlicht wurde.

## Änderung

- **`bootstrap/references/file-templates.en.md`** §`eslint.config.mjs`: Basis-Hausregeln-Block an die DE-Variante angeglichen — `files: ['**/*.js','**/*.mjs']`, `sourceType: 'commonjs'`, 12 Node-Globals, 4 Override-Regeln, `ignores`-Block. `diff` gegen DE zeigt jetzt nur noch Kommentar-Unterschiede (deutsch/englisch).
- Bewusst nicht übernommen: der reichere EN-13-Regelsatz (redundant mit `eslint-config-airbnb-base`, das beide Configs ohnehin laden — Leichtgewicht-Prinzip).
- BOO-141-Frontend/TSX-Block (`...globals.browser` + `React: 'readonly'`) unverändert.

## Abgrenzung

Reiner Konsistenz-Fix. **Nicht** Teil dieser Welle: die Normalisierung des Cross-Session-Nummern-/Wave-Drifts (Repo-Specs 146–149 = Linear 147–150; doppelte `wave-ba`/`wave-bb`) — das läuft als eigene Aufräum-Story.

## Verweise

Spec: `specs/BOO-150.md` (= Linear BOO-146). Branch: `feat/boo-146-eslint-config-de-en-align`. Anknüpfung: BOO-141 (Frontend-Globals, Wave BA), BOO-2 (ESLint-Regelsatz).
