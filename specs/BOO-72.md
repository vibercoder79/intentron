# BOO-72 — HANDBUCH Anhang R: Multi-Operator-Koordination (5-20+ Operatoren)

## Summary

HANDBUCH-Anhang R "Multi-Operator-Koordination" (DE+EN): Inspirations-Schicht fuer Teams jenseits Anhang-P-Szenario-4. Anhang P (BOO-70) hat "Team mit Coding-Server" fuer 2-5 Operatoren dokumentiert, aber wenn ein Beratungsmandat mit 10-20 Personen oder ein groesseres Inhouse-Team Code-Crash adoptieren will, fehlen Antworten auf: Branch-Strategie, Code-Owners pro Datei-Bereich, Doku-SSoT-Wahl im Team, Skill-Pool-Governance, Konflikt-Eskalation. Anhang R liefert die drei Layer (Code / Koordination / Doku) mit "was skaliert, was nicht, welche Optionen hat der Operator". **Reine Doku, kein Framework-Code-Change**, kein neuer Skill, keine neue Bootstrap-Frage. Inklusive 1 hochwertigem Excalidraw-Sketch als visuelles Anker-Bild.

## Why

Operator-Frage Tobias (2026-05-27 post-Wave-K): "Wenn 20 Entwickler gleichzeitig im GitHub-Repo arbeiten und sich Daten aus dem Obsidian holen — wie funktioniert das? Stellt das Framework sicher, dass mehrere Leute parallel arbeiten koennen?" Ehrliche Bestandsaufnahme:

- **Code-Layer:** Skaliert nativ via Git (Branch-Protection, PR-Review, Spec-Gate, Sensitive-Paths). Funktioniert in 20er-Teams genauso wie solo.
- **Koordinations-Layer:** Linear/Issue-Tracker mit Workflow-States ist bereits Bootstrap-Frage B.4. Skaliert.
- **Doku-Layer:** Obsidian Vault skaliert nicht in Teams — kein Multi-User-Lock, Sync-Konflikte ueber iCloud/Dropbox. Genau dafuer fragt Bootstrap B.3 die Doku-SSoT ab (Obsidian / Repo-Docs / Confluence / Notion / SharePoint / undecided). Aber: **es fehlt im HANDBUCH die Doku, wie Teams diese Wahl konkret treffen sollen.**

Konsequenzen ohne diese Story:

- "Skaliert das?" bleibt Vertriebs-Hindernis bei Team-Mandaten und Beratungs-Engagements
- Operatoren fallen auf naive Patterns zurueck (jeder cloned, jeder pushed direkt auf `main`, kein CODEOWNERS)
- Doku-Konflikte zwischen Obsidian-Operatoren ohne Lock-Mechanik (Sync-Tool merged binaer, nicht semantisch)
- `privacy-ok` / `review-ok` im Sensitive-Paths-Gate ist heute nicht explizit als "darf nicht der gleiche Operator setzen" dokumentiert — im Solo-Setup egal, im Team kritisch fuer Audit-Trail.

## What

### Fragestellung (1:1 aus Operator-Frage)

> Wenn 20 Entwickler gleichzeitig im selben GitHub-Repo arbeiten und sich Doku aus Obsidian (oder Jira/Confluence/Notion) holen — funktioniert das Framework dann noch? Ist das eine Ueberlegung, die das Framework anstellt, oder muss der Operator das selbst loesen?

### Die drei Layer

Der Anhang strukturiert die Antwort entlang dreier Layer. Jede Layer-Sektion hat dieselbe Struktur: **was skaliert nativ**, **was nicht**, **Operator-Optionen**, **Empfehlung pro Team-Groesse**.

#### Layer 1 — Code-Layer (Git/GitHub)

- **Was skaliert nativ:** Git ist fuer Multi-User-Concurrency gebaut. Branches, PRs, Merge-Konflikt-Resolution, Branch-Protection (BOO-29) — alles team-tauglich ohne Framework-Ergaenzung.
- **Was nicht:** wenn Operatoren direkt auf `main` pushen oder Spec-Gate umgehen, kollabiert die Governance. Aber: das sind keine Framework-Luecken, sondern Team-Disziplin-Themen.
- **Operator-Optionen:**
  - **Trunk-Based Development**: kleine Stories, schnelles Mergen (1-2 Tage pro Branch), Feature-Flags fuer "noch nicht fertig"-Code. Gut fuer hohe Release-Frequenz.
  - **GitFlow**: `develop` + `release/*` Branches zusaetzlich zu `main`. Audit-tauglich, gut fuer regulierte Branchen mit kalendarischen Releases.
  - **Feature-Branches mit PR-Review (Standard heute):** pro Story ein Branch, PR-Review-Gate, Merge in `main`. Einfach, robust, der Code-Crash-Default.
- **Empfehlung:**
  - 5-10 Operatoren: Feature-Branches reichen.
  - 10-20: Trunk-Based oder Feature-Branches mit verbindlichem PR-Reviewer-Pool.
  - 20+: GitFlow wenn Audit-Pflicht, sonst Trunk-Based mit CODEOWNERS.

#### Layer 2 — Koordinations-Layer (Wer macht was?)

- **Was skaliert nativ:** Linear / Jira / GitHub Issues / Azure DevOps / MS Planner haben Workflow-States ("In Progress" = belegt). Bootstrap-Frage B.4 deckt Backlog-Adapter-Wahl ab (BOO-54).
- **Was nicht:** das Issue-Tracker-Tool selbst loest nicht "wer entscheidet bei Konflikten an `SECURITY.md`?". Auch Zuteilung "welcher Operator arbeitet an welchem Modul?" passiert ausserhalb des Frameworks.
- **Operator-Optionen:**
  - **Squad-Modell**: 3-5 Operatoren pro Modul/Domaene, Squad-Lead entscheidet bei Konflikten.
  - **Pool-Modell**: jeder Operator zieht naechstes Issue aus gemeinsamem Backlog, kein fester Modul-Owner.
  - **Hybrid**: Pool fuer kleine Stories, Squad fuer kritische Pfade (SECURITY/PRIVACY/ARCHITECTURE_DESIGN).
- **Empfehlung:**
  - 5-10: Pool reicht.
  - 10-20: Hybrid mit Squad-Owner pro kritischem Pfad.
  - 20+: Squad-Modell mit Lead-Architekt-Rolle fuer Cross-Squad-Themen.

#### Layer 3 — Doku-Layer (Single Source of Truth)

- **Was skaliert nativ:** Repo-Docs (`docs/project/`) skaliert via Git-Mechanik wie Code. Confluence / Notion / SharePoint haben eigene Multi-User-Permissions und Konflikt-Resolution.
- **Was nicht:** **Obsidian Vault skaliert nicht in Teams.** Kein semantischer Multi-User-Lock, Sync ueber iCloud/Dropbox/Syncthing merged binaer und produziert Konflikt-Files (`note (conflicted copy).md`). Obsidian Sync (kostenpflichtig) hilft technisch, aber nicht beim semantischen Konflikt ("zwei Personen aendern dieselbe Notiz").
- **Operator-Optionen (Doku-SSoT-Matrix):**

  | SSoT | Solo (1) | Klein (2-5) | Mittel (5-10) | Gross (10-20+) | Hauptgrund |
  |---|---|---|---|---|---|
  | Obsidian Vault | ✅ | ⚠ | ❌ | ❌ | Solo-Tool, kein semantischer Lock |
  | Obsidian + Git-Sync auf Vault | ✅ | ⚠ | ❌ | ❌ | Sync-Konflikte werden manuell — bei 5+ Personen zu teuer |
  | `docs/project/` im Repo | ✅ | ✅ | ✅ | ✅ | Selbe Git-Mechanik wie Code; PR-Review fuer Doku |
  | Confluence | ⚠ | ✅ | ✅ | ✅ | Externes Tool mit eigenen Permissions, kein Git-Bezug |
  | Notion | ⚠ | ✅ | ✅ | ✅ | Externes Tool, eigene Multi-User-Logik |
  | SharePoint | ⚠ | ⚠ | ✅ | ✅ | Externes Tool, gut fuer regulierte Enterprises |

- **Empfehlung:**
  - 1 Operator: Obsidian (Workflow + Index)
  - 2-5: Obsidian oder Repo-Docs, abhaengig vom Operator-Profil
  - 5+: Repo-Docs oder externes DMS — Obsidian nur noch als persoenliches Brainstorming-Tool, nicht als Team-SSoT

### Was geht heute (im Framework verankert)

- Bootstrap fragt Doku-SSoT ab (Phase B.3, BOO-58/64). Operator-Wahl wird in `DOCUMENTATION_SSOT.path` fixiert.
- Bootstrap fragt Backlog-Adapter ab (Phase B.4, BOO-54). Linear / GitHub Issues / Jira / Azure DevOps / MS Planner / Markdown-only.
- Branch-Protection-Skript (BOO-29) setzt Required-Status-Checks auf `main`.
- Spec-Gate (BOO-4 + BOO-27) blockiert Code-Aenderungen ohne Spec.
- Sensitive-Paths-Gate (BOO-18) erfordert `review-ok`-Bestaetigung.
- Personal-Data-Paths-Gate (BOO-69) erfordert `privacy-ok`-Bestaetigung.

### Was heute nicht geht (Anhang R fuellt die Luecken)

- **CODEOWNERS-Pattern fuer Datei-Bereiche pro Sub-Team** ist nicht im Bootstrap-Setup. Manuelle Operator-Aufgabe.
- **Konflikt-Eskalations-Konvention** fuer SECURITY.md / PRIVACY.md / ARCHITECTURE_DESIGN.md fehlt. Wer entscheidet, wenn zwei Operatoren widerspruechliche Aenderungen mergen wollen?
- **Skill-Pool-Governance** im 20er-Team ist heute nur in Anhang P (Szenario 3) angerissen (global vs. pro User), nicht ausgefuehrt fuer "Wartungs-Owner-Rolle".
- **`privacy-ok` / `review-ok` = Vier-Augen-Prinzip:** im Solo-Setup setzt der Operator das selbst, im 20er-Team muss das ein **anderer** Operator sein. Heute nicht explizit dokumentiert.
- **Doku-SSoT-Wahl pro Team-Groesse** als Decision-Matrix fehlt — die Matrix-Tabelle oben ist genau das, was hier rein muss.

### Wie setzt man das Framework in einem 20-koepfigen Entwicklungsteam auf?

Aus Anhang P Szenario 3 (Multi-User-VPS-Coding-Factory) erweitert, plus Anhang R Disziplinen:

1. **VPS-Setup** (siehe Anhang P Szenario 3): VPS mit 1 System-User pro Operator, Skill-Pool global unter `/opt/claude/skills/` (read-only, Wartungs-Owner-Rolle), Repository-Worktrees pro User in `~/projects/<projekt>/`.
2. **Bootstrap einmalig vom Lead-Architekt:** Frage B.3 = Repo-Docs (`docs/project/`) **oder** Confluence/Notion. Frage B.4 = Linear oder Jira. Frage A.5 = "heavy" Governance.
3. **CODEOWNERS-Datei pflegen:** `.github/CODEOWNERS` mit Datei-Pattern → Sub-Team-Mapping. Beispiel:

   ```text
   /SECURITY.md         @owlist/sec-team
   /PRIVACY.md          @owlist/legal-team
   /ARCHITECTURE_DESIGN.md  @owlist/arch-leads
   /docs/api/**         @owlist/backend
   /docs/ui/**          @owlist/frontend
   ```

4. **Branch-Protection erweitert:** Required-Reviewer-Pool pro kritischem Pfad (mind. 1 Reviewer aus dem CODEOWNERS-Sub-Team).
5. **Vier-Augen-Konvention fuer Gates:** `privacy-ok` / `review-ok` darf NICHT der gleiche Operator setzen, der die Aenderung gemacht hat. Operator-Disziplin, im Audit-Log via `git blame` nachvollziehbar.
6. **Konflikt-Eskalation:** Lead-Architekt + Domain-Owner aus CODEOWNERS entscheiden gemeinsam bei Merge-Konflikten an SECURITY / PRIVACY / ARCHITECTURE_DESIGN.
7. **Squad-Modell:** 3-5 Operatoren pro Modul, Squad-Lead arbeitet Cross-Squad-Themen mit Lead-Architekt aus.
8. **Daily/Weekly-Sync:** kurzer Stand-up (15 Min) zur Backlog-Koordination — kein Framework-Schritt, aber bewaehrte Praxis bei 10+ Operatoren.

### Optionen / Inspirations-Bausteine (nicht-praeskriptiv)

Anhang R praesentiert pro Layer 2-3 Optionen als Auswahl-Matrix, nicht als Empfehlung. Operator waehlt aus.

- Branch-Strategie: Trunk-Based vs. GitFlow vs. Feature-Branches
- Doku-SSoT: Repo-Docs vs. Confluence vs. Notion vs. SharePoint (Matrix oben)
- Skill-Pool: global read-only vs. pro User vs. Hybrid
- Konflikt-Eskalation: CODEOWNERS-basiert vs. Squad-Lead vs. Lead-Architekt-Veto
- Squad-Struktur: Pool vs. Squad vs. Hybrid

### Visualisierung

1 Excalidraw-Sketch "Multi-Operator-Koordination — 3-Layer-Modell" zeigt das Layer-Modell mit Operator-Topologie und Skalierungs-Indikatoren pro Layer. Liegt unter `docs/assets/boo-72-multi-operator-3-layer.excalidraw` + `.png`, eingebettet im HANDBUCH-Anhang R.

## Constraints

- **KEIN neuer Skill, KEINE neue Bootstrap-Frage.** Reine Inspirations-Doku. Bestehende Skills/Gates aus Wave A-K bleiben Quelle der Wahrheit.
- **KEINE Empfehlungs-Festlegung "Trunk-Based ist besser als GitFlow".** Operator waehlt aus, Anhang liefert Tradeoffs.
- **Alle Patterns muessen real existieren** (CODEOWNERS-Datei, Trunk-Based-Development, GitFlow, Confluence-Permissions sind etablierte Konzepte) — keine Erfindungen.
- **DE + EN konsistent.**
- **1 Sketch** als visuelles Anker-Bild, nicht 5. Schraege Versuchung "noch ein Sketch fuer X" widerstehen.

## Decisions

1. **Anhang statt eigenes Buch-Kapitel** — Konsistenz mit Anhang P/Q (Inspirations-Schicht im HANDBUCH).
2. **Reine Doku-Story, kein Framework-Code-Change** — Multi-Operator-Koordination ist Operator-Disziplin, nicht Framework-Garantie. Vier-Augen-Prinzip beim Setzen von `privacy-ok` / `review-ok` koennte man theoretisch im Sensitive-Paths-Gate prueffen (Author des Gate-Commits != Author der Aenderung), aber das wird absichtlich NICHT in diese Story gepackt — wuerde Framework-Komplexitaet erhoehen.
3. **Sketch als Inspirations-Bild** — Layer-Modell + Pattern-Optionen pro Layer schneller erfasst als 5 Seiten Text.
4. **Soft-Dependency auf Anhang P** — Anhang R erweitert P Szenario 3+4, ersetzt sie nicht. Quellen-Hinweis im Anhang R.
5. **Story-Points 5** — 3 Punkte fuer Doku DE+EN, 2 Punkte fuer hochwertigen Sketch mit Render-Loop.

## Agent-Pattern

**Gewaehltes Pattern:** sub-agents (sequentiell). 1 Sub-Agent fuer Anhang R DE+EN (analog Wave-K-Pattern), 1 Sub-Agent fuer Excalidraw-Sketch mit Render-Loop. Lead haengt an, macht Migration-Hinweis-Block falls noetig, schreibt Release Notes.

## Acceptance Criteria

- [ ] HANDBUCH-Anhang R (DE) mit 3-Layer-Modell, Decision-Matrix, Code-Owners-Pattern, Doku-SSoT-Matrix, Skill-Pool-Governance, Konflikt-Eskalation
- [ ] HANDBUCH-Anhang R (EN) konsistent
- [ ] Excalidraw-Sketch "Multi-Operator-3-Layer-Modell" als `.excalidraw` + `.png` im Repo, eingebettet im HANDBUCH-Anhang R (Spec-Anlage liefert bereits eine erste Version, Story-Umsetzung verfeinert wenn noetig)
- [ ] HANDBUCH-Footer aktualisiert
- [ ] Release Notes als Bestandteil einer naechsten Wave (Wave L oder spaeter, je nach Story-Mix)

## Dependencies

- **Anhang P (BOO-70) als Voraussetzung** — Szenario 3+4 sind die Basis, Anhang R erweitert sie.
- **Soft-Dependencies:** BOO-29 (Branch-Protection), BOO-18 (Sensitive-Paths-Gate), BOO-69 (Personal-Data-Paths-Gate), BOO-54 (Backlog-Adapter), BOO-58/64 (Doku-SSoT-Pflicht). Anhang R zeigt, wie diese im Team diszipliniert gelebt werden.
- **Keine Hard-Dependencies.**

## Session-Referenz

Spec geschrieben in Session 2026-05-27 nach Wave-K-Release (Commit `3f3dc92`). Operator-Frage Tobias post-Wave-K: "Wie funktioniert das Framework wenn 20 Entwickler gleichzeitig arbeiten?". Daily Note: SecondBrain `05 Daily Notes/2026-05-27.md`. Linear: <https://linear.app/owlist/issue/BOO-72/>

## Rollout

Kein Feature-Flag noetig — reine Doku-Story. Bestands-Projekte unveraendert. Anhang R ist Lese-Material, kein Skill-Verhaltens-Change.
