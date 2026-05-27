# BOO-68 — Token-Effizienz-Policy real validieren (Vor/Nach-Vergleich)

> **Naming-Hinweis (2026-05-27):** In Konzept-Doku und Daily Notes vom 2026-05-24 wurde diese Story als "BOO-74" referenziert (wishful planning, Q3-Roadmap). Tatsaechliche Linear-ID ist **BOO-68**, weil Linear bei Issue-Anlage am 2026-05-27 die naechste freie ID vergab. Die zuvor unter `specs/BOO-68.md` liegende Spec "Non-Code Change-Types" (war nie in Linear) wurde nach `specs/BOO-68-non-code-archive.md` umgezogen.

## Summary

Empirische Validation der in BOO-84 etablierten Token-Effizienz-Policy durch einen kontrollierten Vor/Nach-Vergleich an einer Test-Story. Vor-Lauf simuliert Pre-Policy-Zustand (alle Skills auf Opus, kein Caching) via `/implement --model opus --no-cache`. Nach-Lauf nutzt Default-Policy (per-Skill-Tier-Routing + Caching aktiv). Vergleicht Token-Counts (input/output/cached), Cache-Hit-Rate, USD-Cost und Wall-Clock-Time. Ergebnis: empirischer Beleg fuer die in BOO-84 postulierten 50-70% Token-Reduktion und Faktor-12-Cost-Differenz im Lint-Loop, plus FinOps-Argument fuer Kunden-Pitches.

## Why

BOO-84-Spec verlangt explizit `BOO-68 Test-Lauf mit Routing+Caching dokumentiert (PR-Belege)` als letzten Validation-Punkt (siehe `specs/BOO-84.md` §Decisions Punkt 5 + §Validation). Ohne diesen Beleg bleibt die Policy methodisch unbestaetigt — die postulierten Zahlen (50-70% Reduktion, Faktor 12x) stammen aus Anthropic-Pricing-Rechnung, nicht aus realem Code-Crash-Workflow.

Konsequenzen ohne diese Story:

- Kein realer Beleg dass die Policy in echten /implement-Runs greift (z.B. Cache-Hit-Rate koennte unter Schwelle bleiben wenn Prompt-Strukturen instabil sind).
- Kunden-Pitches stuetzen sich auf Pricing-Rechnung statt auf eigenen Audit-Beleg.
- BOO-84 bleibt unvalidiert in der PMO-Hub-Phasentabelle (Phase 7+ Framework-Validierung).
- Cost-Aggregation im Sprint-Review wurde noch nie an einem echten Sprint getestet.

## What

- **Test-Story-Auswahl** — eine bewusst kleine, reproduzierbare Code-Story mit klarem Lint/Test-Iterationsmuster. Kandidaten:
  - **Variante A (empfohlen):** Eine separate Mini-Story `docs/validation/test-story-token-efficiency.md` mit kuenstlichem Lint-Iterations-Szenario (3-5 ESLint-Fixes auf einem dummy `src/sample.ts`-File). Vorteil: 100% kontrolliert, kein Wettbewerb mit echten Backlog-Stories.
  - **Variante B:** Eine bestehende kleine Story aus dem Backlog (z.B. BOO-69 wenn naechstes Sprint-Item). Vorteil: realer Workflow, Nachteil: nicht wiederholbar.
- **Vor-Lauf** auf separatem Branch `validate/boo-68-pre-policy`:
  - `/implement <story> --model opus --no-cache` (CLI-Override-Flags aus BOO-84)
  - meta.json zeigt `recommended_tier: opus` (override), `cache_hit_rate: 0`
  - Lauf-Daten archivieren nach `journal/reports/local/2026-XX-XX_BOO-68_pre/meta.json`
- **Nach-Lauf** auf separatem Branch `validate/boo-68-post-policy`:
  - `/implement <story>` (Default-Policy: per-Skill-Tier-Routing + Caching aktiv)
  - meta.json zeigt drei-Ebenen-Tracking (iteration/skill/story), per_model-Aufschluesselung, Cache-Hit-Rate
  - Lauf-Daten archivieren nach `journal/reports/local/2026-XX-XX_BOO-68_post/meta.json`
- **Validation-Report** unter `docs/validation/BOO-68-token-efficiency-validation.md` (DE+EN):
  - Vor/Nach-Tabelle: Token-Counts (input/output/cached), Cache-Hit-Rate, USD-Cost, Wall-Clock-Time
  - Pro Skill-Aufruf: alter vs. neuer Tier, Cost-Differenz
  - Root-Cause-Analyse falls Reduktion unter 50% bleibt
- **PR gegen `main`** mit Validation-Report + Verweis in `docs/releases/wave-i-token-efficiency.md` (Sektion "Validation" ergaenzen)
- **Sprint-Review-Aggregation** der `journal/reports/`-Daten im naechsten Sprint-Review testen (BOO-84 Schritt 2b)
- **Update PMO HUB** im SecondBrain: BOO-68 done + Phase 7+ Framework-Validierung naeher an Closeout

## Constraints

- Test-Story muss **reproduzierbar** sein: gleicher Code-Stand, gleiches Modell-Version (Anthropic-Cutoff), gleiche Tool-Versionen (eslint, ruff). Sonst sind Vor/Nach-Vergleiche nicht aussagekraeftig.
- **Keine Secrets** im Cost-Report (kein API-Key, kein Token, kein Customer-Daten — auch nicht in den /implement-Conversation-Logs).
- **Aufwand-Grenze:** maximal 3 SP (Sprint-Sizing-Mechanik). Wenn ueberschritten: Test-Story-Scope verkleinern, nicht Validation-Tiefe reduzieren.
- **Kein Hard-Block auf Cost-Reduktion:** falls reale Reduktion < 50% bleibt, Story trotzdem mergen aber mit Root-Cause-Sektion im Report. Policy-Anpassung erfolgt in eigener Folge-Story, nicht hier.
- DE + EN Validation-Report konsistent (Memory `feedback_subagent_long_heredoc_timeout`: nicht in einem Sub-Agent-Heredoc, lieber 2 separate Sub-Agents oder Lead schreibt EN-Pass).

## Decisions

1. **Variante A (kuenstliche Test-Story) gewaehlt** statt echte Backlog-Story. Begruendung: 100% Reproduzierbarkeit, klare Lint-Iterations-Zahl, keine Vermischung mit echten Story-Risiken. Wenn spaeter eine echte Story gleichzeitig validieren soll: separates Issue.
2. **CLI-Override-Flags `--model opus --no-cache`** statt Skill-File-Edit fuer den Vor-Lauf. Vermeidet Skill-Pollution (Reverts notwendig sonst).
3. **Branch-Pattern `validate/boo-68-*`** statt feature/boo-68-*. Signalisiert dass das Branches reine Mess-Setups sind, nicht Feature-Code. Werden nach PR-Merge geloescht.
4. **Validation-Report-Pfad `docs/validation/`** als neuer Sub-Ordner. Erste Validation-Story → erste Konvention. Folge-Validations (z.B. Security-Policy-Validation) wuerden dort hin.
5. **Acceptance-Schwelle Cache-Hit-Rate ≥ 60%** als Soft-Gate. Wenn unter Schwelle: kein Block, aber Root-Cause-Pflicht im Report.

## Agent-Pattern

**Gewaehltes Pattern:** linear (Operator-Lead, kein Sub-Agent).

**Begruendung:** Die Story hat zwei sequenzielle Mess-Laeufe + einen Report-Schritt. Sub-Agent-Overhead waere groesser als Nutzen. Lead fuehrt beide Laeufe persoenlich aus (sieht meta.json live), schreibt Report manuell, EN-Pass durch Lead nicht durch Sub-Agent (Heredoc-Timeout-Risiko bei langen Vergleichs-Tabellen).

## Validation

- meta.json beider Laeufe zeigt drei-Ebenen-Tracking aktiv (iteration/skill/story)
- Nach-Lauf Cache-Hit-Rate ≥ 60% (Soft-Gate)
- Vor/Nach-Cost-Differenz konsistent mit BOO-84 Policy-Erwartung (50-70% Reduktion) ODER Root-Cause-Sektion im Report
- PR-Body enthaelt die Vor/Nach-Tabelle
- `docs/validation/BOO-68-token-efficiency-validation.md` DE+EN existiert
- `docs/releases/wave-i-token-efficiency.md` hat ergaenzten Validation-Verweis
- `git diff --check` clean

## Acceptance Criteria

- [ ] Test-Story (Variante A) als `docs/validation/test-story-token-efficiency.md` definiert
- [ ] Vor-Lauf abgeschlossen, `journal/reports/local/<date>_BOO-68_pre/meta.json` archiviert
- [ ] Nach-Lauf abgeschlossen, `journal/reports/local/<date>_BOO-68_post/meta.json` archiviert
- [ ] Validation-Report `docs/validation/BOO-68-token-efficiency-validation.md` (DE+EN) geschrieben mit Vor/Nach-Tabelle
- [ ] `docs/releases/wave-i-token-efficiency.md` um Validation-Verweis ergaenzt
- [ ] PR gegen `main` mit Vor/Nach-Tabelle im Body
- [ ] Sprint-Review-Aggregation gegen die `journal/reports/`-Daten testweise gelaufen (manueller Smoke-Test)
- [ ] PMO HUB im SecondBrain: BOO-68 done eingetragen
- [ ] Cache-Hit-Rate ≥ 60% beim Nach-Lauf ODER Root-Cause-Sektion im Report begruendet warum nicht erreicht

## Dependencies

- **Erfuellt (Voraussetzung fuer Lauf):** BOO-84 (Token-Effizienz-Policy implementiert, in main, Tag v0.1.0)
- **Soft-Dependency:** keine — die Story kann jederzeit gestartet werden

## Session-Referenz

Initiale Spec-Erstellung: SecondBrain Daily Note 2026-05-27, Session "Code-Crash Framework — BOO-84 Closeout + HANDBUCH-Split". Bezugs-ADR: keiner gesondert, Policy-Begruendung liegt in `02 Projekte/Code-Crash Framework/Token-Effizienz-Policy.md`.

## Rollout

Kein Feature-Flag noetig — die Story ist reine Validation, kein produktives Feature. Branches `validate/boo-68-*` nach PR-Merge loeschen.
