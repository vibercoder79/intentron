# Release Notes - Wave H Documentation-SSoT & Onboarding

> 🌐 **Sprache:** Deutsch (diese Datei) · [🇬🇧 English](wave-h-documentation-ssot-onboarding.en.md)

Stand: 2026-05-20

## Zweck

Wave H schliesst BOO-64 bis BOO-67. Das Framework macht Projektdokumentation jetzt explizit zum Vertrag: Bootstrap fragt den Documentation-SSoT ab, Developer Onboarding wird als Standard-Artefakt erzeugt, Runtime- und Story-Spec-Preflight verhindern blindes Umsetzen gegen falsche Annahmen.

## Betroffene Stories

- BOO-64
- BOO-65
- BOO-66
- BOO-67

## Was Nutzer mit dem neuen Setup bekommen

- einen klaren Dokumentationsanker pro Projekt statt verstreuter Tool-Notizen,
- ein standardisiertes Developer Onboarding fuer neue Entwickler, fremde Teams und Toolwechsel,
- Preflight-Pruefungen, die vor der Umsetzung Runtime, Story-Spec, relevante SSoTs und Pflegepflichten sichtbar machen,
- Migrationshinweise fuer bestehende Projekte, damit die neuen Artefakte additiv nachgezogen werden koennen.

## Documentation-SSoT Optionen

Bootstrap fuehrt die Entscheidung fuer den fuehrenden Dokumentationsort als Projektvertrag:

- `Obsidian` fuer wissenszentrierte Projektarbeit mit Hub, Governance, ADRs und Daily-Note-Anbindung,
- `Repo docs` fuer code-nahe Projekte, bei denen Markdown im Repository fuehrend ist,
- `External DMS` fuer Organisationen mit bestehendem Dokumentenmanagement, sofern das Framework nur verlinkt und nicht dupliziert,
- `undecided` als expliziter Zwischenstand, der Folgearbeit ausloest statt stillschweigend Annahmen zu treffen.

## Developer Onboarding als Standard-Artefakt

Das Developer Onboarding ist jetzt ein Pflichtartefakt fuer Projekte, in denen neue Entwickler, externe Teams oder andere AI-Coding-Runtimes produktiv arbeiten sollen. Es fuehrt auf:

- Project Hub oder fuehrendes DMS,
- Architektur- und Governance-Dokumente,
- Security- und Secrets-Regeln,
- Backlog- und Story-Spec-Konventionen,
- erste sichere Schritte bis zur ersten Story.

Sprint Review und Implementation muessen das Onboarding pflegen, sobald sich Runtime, SSoT, Security-Regeln, Backlog-Konventionen oder zentrale Artefakte aendern.

## Runtime-/Story-Spec-Preflight

Vor der Umsetzung wird nicht nur gefragt, welche Story umgesetzt wird, sondern ob der lokale Kontext tragfaehig ist:

- Runtime geklaert: Claude, Codex, Cross-Tool oder andere Umgebung,
- Story-Spec vorhanden und zur Arbeit passend,
- Documentation-SSoT bekannt,
- Developer Onboarding vorhanden oder bewusst als Migrationsluecke markiert,
- Sicherheits- und Secrets-Regeln gelesen,
- offene Pflegepunkte fuer Sprint Review oder Implementation erfasst.

## Migration und Handlungsbedarf fuer bestehende Projekte

Bestehende Projekte muessen nicht neu gebootstrappt werden. Der empfohlene Pfad ist additiv:

1. Documentation-SSoT bestimmen und im Projektvertrag festhalten.
2. Developer Onboarding aus bestehenden Hub-, Architektur-, Security- und Backlog-Dokumenten ableiten.
3. Runtime- und Story-Spec-Preflight in die Implementierungsroutine aufnehmen.
4. Sprint-Review-Pflegepflichten fuer Onboarding und SSoT dokumentieren.
5. Externe DMS-Verweise pruefen und tote Links als Blocker markieren.

## Neue Sketch-Artefakte

- `docs/project-documentation-ssot.excalidraw`
- `docs/project-documentation-ssot.en.excalidraw`
- `docs/foreign-developer-onboarding-flow.excalidraw`
- `docs/foreign-developer-onboarding-flow.en.excalidraw`

## Offene Folgearbeit

- Externe DMS werden im Framework nur verlinkt, solange keine konkrete Integration vereinbart ist. Daraus bleiben offene Punkte fuer Link-Validierung, Zugriffsrechte, Owner und Update-Verantwortung.
- Optional: spaeter PNG-Exports erzeugen, wenn die Sketches direkt in README, Handbuch oder Praesentationen eingebettet werden sollen.
- Optional: bestehende Projekt-Templates um projektspezifische Beispiele fuer Obsidian, Repo docs und DMS erweitern.
