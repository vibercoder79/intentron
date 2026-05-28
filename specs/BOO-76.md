# BOO-76 — HANDBUCH Anhang S: Skill-Installations-Strategie (wo gehoeren Skills hin)

## Summary

Neuer HANDBUCH-Anhang S "Skill-Installations-Strategie" (DE+EN) beantwortet die wiederkehrende Operator-Frage "Wo installiere ich die Skills?" an **einer** konsolidierten Stelle. Drei Install-Ebenen (global pro User / pro Projekt / globaler System-Pool), Tradeoff Update-Last vs. Pinning, Decision-Matrix pro Deployment-Szenario (Bezug Anhang P), Cross-Tool-Sicht (Claude Code + Codex + andere via Anhang K). Plus Sketch. Reine Doku, kein Code-Change.

## Why

Wiederkehrende Operator-Frage (Tobias, 2026-05-28). Konkreter Ausloeser: 20-koepfiges Dev-Team auf einer VPS, mehrere System-User, Claude zentral bereitgestellt. Frueher hiess es pauschal "Skills auf Projektebene" — das erzeugt Update-Last (jedes Projekt einzeln nachziehen, wenn sich das Skill-Repo aendert). Die Antwort war bisher verstreut: Bootstrap Phase 5 (pro-Projekt-Install), Anhang P Szenario 3 (global vs. pro-User), Anhang R (Skill-Pool-Governance). Kein Ort beantwortet "wo gehoeren Skills hin?" konsolidiert — und keiner deckt die Cross-Tool-Sicht ab.

## What

- **HANDBUCH Anhang S** (DE+EN):
  - **Drei Install-Ebenen** (Tabelle): global pro User `~/.claude/skills/`, pro Projekt `<projekt>/.claude/skills/` (committed), globaler System-Pool `/opt/claude/skills/` (read-only).
  - **Tradeoff:** global = ein Update, kein Pinning, Bruch-Risiko; pro-Projekt = N Updates, aber reproduzierbar + audit-fest. Faustregel: global Default, pro-Projekt-Pinning nur fuer Audit / externe Uebergabe.
  - **Decision-Matrix pro Deployment-Szenario** (Bezug Anhang P): Solo-Mac/Solo-VPS → global pro User; Multi-User-VPS → System-Pool (Wartungs-Owner); Team-Server → System-Pool oder pro-Projekt.
  - **20-Personen-VPS-Antwort konkret:** ein globaler System-Pool, read-only, ein Wartungs-Owner, ein `git pull` fuer die ganze Maschine. NICHT pro Projekt.
  - **Cross-Tool-Tabelle:** Claude Code (`~/.claude/skills/` + `.claude/skills/`), Codex (`.codex/skills/`), andere via Anhang K. Multi-Tool-Teams → pro-Projekt portabler.
  - **Bootstrap-Bezug:** Phase 5 installiert pro Projekt (`RUNTIME_TARGET`); globaler Pool ist Operator-Sache.
  - Sketch `docs/assets/skill-install-locations.png`.
- **Cross-Verweise:** Anhang P (Szenario 3), Anhang R (Skill-Pool-Governance), Anhang K (Tool-Adapter), Bootstrap Phase 5.

## Constraints

- **Reine Doku.** Konsolidiert bestehende Aussagen, erfindet KEINE neuen Install-Mechaniken.
- Keine erfundenen Pfade/Tools — nur die etablierten (`~/.claude/skills/`, `.claude/skills/`, `/opt/claude/skills/`, `.codex/skills/`).
- DE + EN konsistent. 1 Sketch.

## Decisions

1. **Eigener Anhang statt verstreute Hinweise** — die Frage kommt wiederholt, verdient einen konsolidierten Ort.
2. **Decision-Matrix an Anhang P gekoppelt** — die Install-Ebene haengt am Deployment-Szenario.
3. **Cross-Tool explizit** — nicht nur Claude Code; Multi-Tool-Teams brauchen die portable pro-Projekt-Antwort.
4. **20-Personen-VPS = System-Pool, nicht pro Projekt** — direkte Antwort auf die Operator-Frage, begruendet ueber Update-Last.

## Acceptance Criteria

- [x] HANDBUCH Anhang S (DE) mit 3 Ebenen + Tradeoff + Decision-Matrix + Cross-Tool
- [x] HANDBUCH Anhang S (EN) konsistent
- [x] Sketch `docs/assets/skill-install-locations.png` eingebettet (DE+EN)
- [x] Cross-Verweise Anhang P / R / K / Bootstrap Phase 5
- [x] Footer-Datum aktualisiert
- [x] Release Notes (`docs/releases/wave-n-vault-harvest-and-skill-location.md`) + v0.2.0-overview-Update

## Dependencies

- Soft: BOO-70 (Anhang P Szenarien), BOO-72 (Anhang R Governance), BOO-49 (Anhang K Tool-Adapter), BOO-74 (Bundle-Skills).

## Session-Referenz

Spec + Umsetzung Session 2026-05-28. Wiederkehrende Operator-Frage Tobias. Linear: <https://linear.app/owlist/issue/BOO-76/>
