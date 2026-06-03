# Wave AV — Doku/Runbooks, Leichtgewicht-SecondBrain & Design-Story-Entscheidung (BOO-118/119/126/128/129)

**Was jetzt da ist:** das GitHub-Runbook deckt HTTPS→SSH ab, SonarCloud hat ein eigenes Zwei-Szenarien-Setup-Runbook, der Operator kann sein Setup jederzeit selbst prüfen, `repo-docs` wird zum nutzbaren Leichtgewicht-SecondBrain (Session-Start-Routine), und das Design-Story-Handling ist als Entscheidung festgehalten. Drittes und letztes Bündel der Probelauf-Folge-Stories (BKO, 2026-06-02).

## Stories
- **BOO-118** — SSH-Runbook: `git remote set-url` HTTPS→SSH als Schritt 5 + Verbindungstest.
- **BOO-128** — Phase 7.6: `verify-setup.sh`-Re-Run-Hinweis (`--strict`, read-only) + fertiger Operator-Prompt.
- **BOO-119** — **HANDBUCH Anhang AA**: SonarCloud-Setup-Runbook (Szenario A: Account existiert / B: von 0); Bootstrap D.5 + Provider-Postflight (BOO-58) deeplinken darauf.
- **BOO-129** — `repo-docs` **Leichtgewicht-SecondBrain**: Session-Start-Routine in der generierten `CLAUDE.md` (PMO-Hub + meetings/decisions lesen, zurückschreiben) + DE/EN-Sketch.
- **BOO-126** — **Design-Story-Entscheidung** ratifiziert: „implement gegen Referenz", kein `change_type:design` (ADR + Abgrenzung, Karpathy-Verifizierbarkeit).

## Änderungen (DE+EN)
- **`HANDBUCH.md`:** §3 SSH-Schritt 5 (BOO-118); neuer **Anhang AA** SonarCloud-Runbook (BOO-119); §6 Design-Story-Abgrenzung (BOO-126).
- **`bootstrap/SKILL.md`:** Phase 7.6 verify-setup-Re-Run + Prompt (BOO-128); D.5 Anhang-AA-Deeplink (BOO-119).
- **`references/file-templates.md`:** CLAUDE.md-Template Session-Start-Routine (BOO-129).
- **`references/project-documentation-ssot.md`:** Leichtgewicht-SecondBrain-Loop + Sketch-Embed (BOO-129).
- **`references/provider-postflight.md`:** SonarCloud-Runbook-Deeplink (BOO-119).
- **Neu:** ADRs `docs/domain/adrs/design-story-handling(.en).md` (BOO-126); Sketch `docs/assets/boo-129-leichtgewicht-secondbrain.{excalidraw,png}` (+`.en`).

## Verweise
Specs: `specs/BOO-118.md`, `BOO-119.md`, `BOO-126.md`, `BOO-128.md`, `BOO-129.md`. Branch: `feat/boo-docs-secondbrain` (auf der Bündel-2-Spitze).
