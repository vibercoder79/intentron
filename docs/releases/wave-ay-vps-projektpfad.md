# Wave AY — VPS-Standard-Projektpfad & Daily-Note-Loop (BOO-138/139)

**Was jetzt da ist:** Eine Developer-VPS wird zum reibungsarmen Multi-Projekt-Host. Der Bootstrap erfragt **einmal pro Maschine** einen Standard-Projektpfad (`PROJECTS_ROOT`), hinterlegt ihn in der globalen Operator-`~/.claude/CLAUDE.md` und schlägt ihn danach bei jedem weiteren Projekt als Default vor — Enter genügt, der Override bleibt. Zusätzlich bekommt jedes Projekt einen **Daily-Note-Loop**: die generierte `CLAUDE.md` fragt am Sessionende „Soll ich die Daily Note schreiben?" und legt sie unter `journal/daily/YYYY-MM-DD.md` ab, beim nächsten Start wird sie mitgelesen. Übertragung des Obsidian-Vault-Prinzips (fester Projekt-Ort + Daily Notes) auf die VPS **ohne Obsidian**. Bewusst **kein** Cockpit/Dashboard — leichtgewicht.

## Stories

- **BOO-138** — **VPS-Standard-Projektpfad `PROJECTS_ROOT`**: erstes Bootstrap einer Maschine erfragt den Pfad + schreibt ihn (nach Operator-Bestätigung) in `~/.claude/CLAUDE.md`; Block B Frage 1 liest ihn und schlägt `<PROJECTS_ROOT>/<projektname>` als Default vor (manueller Override bleibt).
- **BOO-139** — **journal/daily/ + Session-Ende-Routine**: die generierte Projekt-`CLAUDE.md` bekommt eine Session-ENDE-Routine („Daily Note schreiben?") + die Konvention `journal/daily/YYYY-MM-DD.md`; die Session-START-Routine liest die letzte Daily Note mit. Nutzt das bestehende `journal/`-Baseline-Artefakt (BOO-61) — kein Parallel-Ordner.

## Änderungen (DE+EN)

- **`bootstrap/SKILL.md`** (Version 3.35.0 → **3.36.0**): Block B — `PROJECTS_ROOT`-Mechanik (lesen/erfragen/schreiben) + Default-Vorschlag an Frage 1; Merken-Block um `PROJECTS_ROOT` ergänzt (BOO-138).
- **`bootstrap/references/global-registry-update.md`**: neue Sektion „3a. Standard-Projektpfad `PROJECTS_ROOT`" — Lese-/Schreib-Regel, Operator-Bestätigung, kein Secret, Override (BOO-138).
- **`bootstrap/references/file-templates.md`** (CLAUDE.md-Template): Session-START-Routine liest zusätzlich die letzte `journal/daily/`-Notiz; neue **Session-ENDE-Routine** „Daily Note schreiben?" + Schreib-Konvention (BOO-139).
- **`bootstrap/references/project-documentation-ssot.md`**: Leichtgewicht-SecondBrain-Loop um `journal/daily/` erweitert (BOO-129/139).
- **`HANDBUCH.md` Anhang U**: Maschinen-Ebene nennt `PROJECTS_ROOT`, Projekt-Ebene nennt `journal/daily/`; Weg 2 Schritt 1 mit Default-Pfad-Vorschlag (BOO-138/139).

Alle Änderungen DE+EN-paritätisch (`.en.md`-Pendants mitgezogen).

## Abgrenzung

Kein projektübergreifendes Cockpit/Dashboard (bewusst verworfen — leichtgewicht): „Wo stehen wir?" entsteht beim Öffnen des jeweiligen Projekts aus PMO-Hub + letzter Daily Note. `repo-docs` bleibt portable Markdown-Basis mit relativen Links (GitHub-/Obsidian-/DMS-spiegelbar); kein Dataview/Wikilink-Zwang.

## Verweise

Specs: `specs/BOO-138.md`, `specs/BOO-139.md`. Branch: `feat/boo-138-139-vps-projektpfad`. Anknüpfung: BOO-129 (Session-Start-Loop), BOO-130 (`docs/how-we-document.md`), Anhang U (Multi-Projekt-Betrieb). Operator-Quelle: Tobias, 2026-06-03 (Ursprung: SecondBrain-Setup → VPS-Übertragung).
