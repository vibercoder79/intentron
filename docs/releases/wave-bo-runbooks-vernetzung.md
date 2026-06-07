# Wave BO — Runbooks & Doku-Vernetzung: Auditor-Runbook, Belege verlinken, INDEX + Elevator-Pitch (BOO-167)

> 🌐 **Sprache:** Deutsch (diese Datei) · [🇬🇧 English](wave-bo-runbooks-vernetzung.en.md)

**Was jetzt da ist:** Die Rollen-Runbooks (Wave BJ) werden vom losen Bestand zu einem vernetzten Ganzen. Das Auditor-Runbook ist jetzt vollwertig (mit Audit-Prompt + Persistenz-Zonen + Sketch), alle Beleg-Spalten der Runbooks sind klickbar, ein neuer rollenbasierter Wegweiser steht ganz oben im README, eine alphabetische INDEX-Datei gibt den Gesamtüberblick über alle Dokumente, das HANDBUCH nimmt die Runbooks namentlich auf, und ein laienverständlicher 60-Sekunden-Elevator-Pitch erklärt das Framework am Whiteboard. Reine Doku. DE+EN.

## Stories
- **BOO-167** — Doku-Vernetzungs-Story (7 Arbeitspakete A–G).

## Änderungen (DE+EN)
- **`docs/runbooks/audit-perspective.md` / `.en.md`** — von 156 auf ~311 Zeilen ausgebaut: Zielgruppe Auditor (Cyber-Security UND Code-Quality) direkt adressiert, „In einem Satz"/„Big Picture"(+Sketch)/„Weiterlesen", die drei **Persistenz-Zonen** (committet/dauerhaft · CI-Artifact/30 Tage · lokal-gitignored), Doppel-Zielgruppe-Tabelle, und ein **Audit-Prompt** als zweisprachiger Copy-Paste-Block (8-Schritt-Scan, read-only, zwei Modi).
- **`docs/runbooks/ceo-business-case` · `ciso-security` · `cto-code-quality` · `dpo-privacy` (je `.md`/`.en.md`)** — `> **Für wen.**` → `> **Zielgruppe:**` (reine Leserrolle) + separater Zeit-/Kernfrage-Satz; Beleg-/Artefakt-Spalten von Klartext auf Markdown-Links umgestellt (nur reale Repo-Ziele; projekt-lokale Artefakte bleiben Code-Spans); Header-/Intro-Drift harmonisiert. DPO war Verlinkungs-Vorbild.
- **Neu `docs/INDEX.md` / `.en.md`** — alphabetische Tabelle aller 32 Dokumente (Dokument | Beschreibung | Zielgruppe | Sprachen) plus separater Block „Skill-Dokumentation" (15 Skill-READMEs). Aus README verlinkt.
- **Neu `docs/pitch/elevator-pitch.md` / `.en.md`** — 60-Sekunden-Pitch (~205/210 Wörter), jargonfrei, mit Whiteboard-Skript + eingebettetem Sketch; ergänzt die bestehende 30-Min-Präsentation.
- **Neu Sketches (DE+EN, `.excalidraw` + `.png`):** `docs/audit-perspective-runbook.*` (Frage→Beleg→Ort mit 3 Persistenz-Zonen), `docs/pitch/elevator-pitch.*` (Whiteboard-Skript). **Aktualisiert:** `docs/role-runbooks-map.*` — von „Vier Brillen" auf **„Fünf Brillen"** (Auditor als nachgelagerte Querschnitts-Brille).
- **`README.md`** — neuer schlanker Rollen-Wegweiser „Wer bist du? / Who are you?" ganz oben (DE+EN) mit Links auf CEO/CISO/CTO/DPO/Auditor-Runbooks + Verweis auf INDEX und Elevator-Pitch. Bestehende Langtabelle bleibt.
- **`HANDBUCH.md` / `.en.md`** — Kapitel 13 nimmt die 5 Rollen-Runbooks + `framework-update`/`sonarcloud-setup` namentlich auf; TOC „Anhänge A bis AB" → „A bis AD"; Anhänge-Wegweiser um AC/AD ergänzt.
- **`docs/glossar.md` / `.en.md`** — neue Einträge „Auditor", „Audit-Trail", „Audit-Artefakt" mit Alltagsanalogie.

## Wirkung
Auf die Frage „Ich bin neu — wo fange ich an?" gibt es jetzt einen rollenbasierten Einstieg in der ersten Bildschirmseite, einen Gesamtindex und einen 60-Sekunden-Pitch. Der Auditor hat ein eigenständiges, handlungsfähiges Runbook samt Copy-Paste-Prompt. Belege sind durchklickbar statt nur benannt.

## Abgrenzung
Reine Doku, kein Code, keine neue Mechanik. Wave-Buchstabe `bo` (bn zuletzt belegt). Projekt-lokal entstehende Artefakte (`specs/`, `.claude/*`, `journal/*`, `ARCHITECTURE_DESIGN.md`) bleiben Code-Spans (keine toten Links). Kein CIO/CDO-Runbook (existiert nicht). `docs-drift` grün, alle neuen relativen Links/Embeds gegen das Dateisystem verifiziert.

## Verweise
Linear: BOO-167. Branch: `tobiaschschmidt/boo-167-docs-runbooks-doku-vernetzung-auditor-runbook-ausbauen`. Baut auf Wave BJ (BOO-158–163, Rollen-Runbooks) auf. Operator-Quelle: Tobias, 2026-06-06.
