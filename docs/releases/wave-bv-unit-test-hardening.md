# Wave BV — Unit-Test-Härtung: echte Tests statt nur Coverage (BOO-177)

> 🌐 **Sprache:** Deutsch (diese Datei) · [🇬🇧 English](wave-bv-unit-test-hardening.en.md)

**Was jetzt da ist:** Platzhalter-Tests zählen nicht mehr als Coverage. Bisher hoben triviale/leere Tests (`expect(true).toBe(true)`, leerer Körper, `assert True`, unbegründete `skip`/`xit`/`@pytest.mark.skip`) die Coverage-Zahl, ohne etwas zu prüfen — niemand fing das. Schwester-Story zu BOO-176: dasselbe Grundproblem „Agent gamed das Gate", hier auf der Test-Ebene. Abgrenzung: nur **Unit-Tests**, nicht Integration/E2E.

## Änderungen

- **Anti-Platzhalter-Check** — neuer, gezielter Check auf Test-Dateien: `bootstrap/references/hooks/anti-placeholder-check.py` (AST für Python, Heuristik für JS/TS, **kein** Linter). Flaggt leere/triviale Testkörper + unbegründete Skips. `--self-test`, Default Warnung, `--strict`/`STRICT=1` → Hard-Fail (analog `raw-pii-guard.py`).
- **Integration ins Test-Gate** — neuer Schritt **6a-quint** in `implement/SKILL.md` (+ `.en`) direkt nach dem Coverage-Lauf 6a-quart: geänderte Test-Dateien (`git diff --cached`) werden geprüft, Funde → Gate-Fail, dokumentiert in `meta.json` (`iterations.anti_placeholder` / `skipped_gates.anti_placeholder`). Operator-Override nur via `override_audit` (BOO-176-Disziplin). Coverage = „genug Tests", Anti-Platzhalter = „echte Tests".
- **Expliziter Test-Block im Story-Template** — neue Sektion 7a (Feature) / 5a (Fix) in `ideation/references/story-template-feature.md` + `.en` und `story-template-fix.md` + `.en`: Testfälle (Happy-Path + Fehlerfall) werden beim Story-Schreiben definiert, mit AC-Bezug und Platzhalter-Verbot.
- **Doku** — neues HANDBUCH-Kapitel `8c-bis. Unit-Tests` (+ `.en`); neues Runbook `docs/runbooks/unit-tests.md` (+ `.en`); Audit-Verlinkung in `docs/runbooks/audit-perspective.md` (+ `.en`): Test-Existenz (JUnit-XML) und Test-Qualität (Anti-Platzhalter) als zwei getrennte Audit-Belege.
- **Migration** — `migrate_boo_177()` in `migrate-to-v2.sh` kopiert den Check idempotent aus der kanonischen Quelle (`cp` + `cmp -s`-Skip, byte-identisch — SSoT-Konvention wie BOO-89, kein Heredoc-Drift). Drift-Guard `check-hook-sources.sh` grün.

## Abgrenzung

- **Unit-Tests ≠ Integration-Tests** — Integration/E2E ist ein eigenes, hier NICHT behandeltes Thema; **kein** Integration-Test-Skill (und es soll keiner gebaut werden).
- Anti-Platzhalter ist **kein** Linter-Thema (Linter prüfen Stil/Typen, nicht Test-Sinnhaftigkeit) und **kein** neuer Skill — `/implement` behält die Tests.
- Gate-Config-Schutz = Schwester-Story **BOO-176** (gemergt, Wave BU).
- Wave-Buchstabe **bv** (bu = Quality-Gate-Integrität BOO-176).

## Verweise

Spec: `specs/BOO-177.md`. Branch: `tobiaschschmidt/boo-177-featdocs-unit-test-hartung`. Verwandt: BOO-176 (Quality-Gate-Integrität, Schwester), BOO-93 (`raw-pii-guard.py`-Präzedenz), BOO-89 (Hook-SSoT/Drift-Guard), BOO-15 (Coverage-Gate). Operator-Quelle: Tobias, Feldeinsatz TYPO3/PHP 2026-06-07.
