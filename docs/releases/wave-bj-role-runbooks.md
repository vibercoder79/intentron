# Wave BJ — Rollenspezifische Runbooks: CISO · DPO · CTO · Geschäftsführung (BOO-158–163)

**Was jetzt da ist:** Vier narrative Einstiegs-Runbooks erklären INTENTRON aus Sicht je einer Führungsrolle — Geschäftsführung, CISO/IT-Leitung, Datenschutzbeauftragte:r, CTO. Jedes liest sich in unter 10 Minuten, beantwortet „was bedeutet das Framework für mich, welche Gatekeeper greifen, wo nehme ich Einfluss" und ist **keine neue Mechanik**, sondern eine Lesebrille auf Bestehendes (analog `audit-perspective.md`). Aus dem README in EN + DE verlinkt, plus eine gemeinsame Rollen-Landkarte als Sketch. Reine Doku. DE+EN.

## Stories
- **BOO-158** — Epic (Dach).
- **BOO-159** — `docs/runbooks/ciso-security.md` (+EN) + Sketch.
- **BOO-160** — `docs/runbooks/dpo-privacy.md` (+EN) + Sketch.
- **BOO-161** — `docs/runbooks/cto-code-quality.md` (+EN); Sketch wiederverwendet (`quality-gate-four-layers`).
- **BOO-162** — `docs/runbooks/ceo-business-case.md` (+EN) + Sketch.
- **BOO-163** — Integration: Rollen-Landkarte-Sketch, README (EN+DE), artefakt-landkarte-Querverweis, diese Wave.

## Änderungen (DE+EN)
- **Neu `docs/runbooks/ciso-security.md` / `.en.md`** — Security-Sicht: Gatekeeper entlang des Lebenszyklus, `security-architect` (4 Modi), Stellschrauben, Grenzen.
- **Neu `docs/runbooks/dpo-privacy.md` / `.en.md`** — Datenschutz-Sicht: `dpo`-Skill (3 Modi), Personal-Data-Paths-Gate, deterministischer Katalog-Audit (`dpo-audit.py`), DSGVO/BDSG/nDSG.
- **Neu `docs/runbooks/cto-code-quality.md` / `.en.md`** — Codequalität/Tech-Debt: Spec-first, 4-Layer-Quality-Gates, doc-version-sync, Audit-Trail, Learning Loop, `governance_mode`.
- **Neu `docs/runbooks/ceo-business-case.md` / `.en.md`** — Investitions-/Business-Sicht: Geschäftsrisiko → Mechanik → Beleg, Entscheidungs-Trigger, Kosten ehrlich.
- **Neu Sketches** `docs/role-runbooks-map.*` (Hero), `docs/ciso-security-runbook.*`, `docs/dpo-privacy-runbook.*`, `docs/ceo-business-case-runbook.*` (je DE+EN, `.excalidraw` + `.png`). CTO nutzt `docs/quality-gate-four-layers.*`.
- **`README.md`** — neuer Abschnitt „Rollenspezifische Runbooks" / „Role-specific runbooks" (EN + DE), nach „Wo anfangen?".
- **`docs/onboarding/artefakt-landkarte.md` / `.en.md`** — Rollen-Einstieg-Hinweis bei den Abnehmer-Rollen.

## Wirkung
Auf die Frage „gibt es eine rollengerechte Einführung ins Framework?" gibt es jetzt vier Lesebrillen statt eines 230-KB-Handbuchs als einzigen Einstieg. Ein CISO, DPO, CTO oder Geschäftsführer versteht in unter 10 Minuten, was das Framework für die eigene Rolle bedeutet.

## Abgrenzung
Reine Doku, kein Code, keine neue Mechanik. Wave-Buchstabe `bj` (bh = knowledge-onboarding-sketches, bg = BOO-156). Projekt-lokale Artefakte im CTO-Runbook als Code-Spans (keine toten Links), Template-Verweis unter „Weiterlesen". Baut auf `artefakt-landkarte` (Abnehmer-Rollen) + `audit-perspective.md` (Stil-Muster) auf.

## Verweise
Spec: `specs/BOO-158.md`. Branch: `tobiaschschmidt/boo-158-rollenspezifische-runbooks-ciso-dpo-cto-geschaftsfuhrung`. Operator-Quelle: Tobias, 2026-06-05.
