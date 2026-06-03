# Glossar für Nicht-Entwickler (Klartext)

> Schulungs-Glossar (BOO-131): die wichtigsten Framework-Begriffe in 1–2 Sätzen, mit Alltagsanalogie — für Fachseite, Management und Kunden. Die technische Kurzfassung steht in **HANDBUCH Anhang C**. EN: [`glossar.en.md`](glossar.en.md).

## Grundbegriffe

- **Repository (Repo)** — der zentrale Ordner, in dem der gesamte Code + die Doku eines Projekts liegen, inkl. voller Änderungs-Historie. *Analogie:* der Aktenschrank des Projekts, in dem jede Version archiviert ist.
- **Commit** — ein gespeicherter Änderungs-Stand mit kurzer Beschreibung. *Analogie:* ein „Speichern + Notiz, was ich geändert habe".
- **Branch** — eine parallele Arbeitskopie, auf der man gefahrlos arbeitet, ohne den Hauptstand zu stören. *Analogie:* ein Entwurf neben dem Original.
- **`main`** — der Hauptstand, der immer funktionieren soll. *Analogie:* die freigegebene Reinschrift.
- **Pull Request (PR) / Merge** — der Antrag, eine Branch-Änderung in `main` zu übernehmen — erst nach Prüfung. *Analogie:* „Bitte um Freigabe", bevor der Entwurf in die Reinschrift einfließt.

## Qualität & Automatik

- **Gate** — eine automatische Prüfung, die durchlaufen sein muss, bevor es weitergeht. *Analogie:* die Schranke, die nur bei grün öffnet.
- **Hook** — ein kleines Skript, das bei einem bestimmten Ereignis (z. B. vor dem Speichern) automatisch losläuft. *Analogie:* ein Bewegungsmelder, der bei Auslösung etwas anstößt.
- **Linter** — ein Werkzeug, das den Code automatisch auf Stil- und Flüchtigkeitsfehler prüft. *Analogie:* die Rechtschreibprüfung für Code.
- **SAST** (Static Application Security Testing) — automatische Suche nach Sicherheitslücken im Code, ohne ihn auszuführen. *Analogie:* der TÜV liest die Baupläne, statt das Auto zu fahren.
- **Runner** — der Computer (oft in der Cloud), der die automatischen Prüfungen ausführt. *Analogie:* der Prüfstand, auf dem die Tests laufen.
- **CI** (Continuous Integration) — die Automatik, die bei jeder Änderung alle Prüfungen auf dem Runner startet. *Analogie:* die Endkontrolle am Fließband, die bei jedem Stück anspringt.
- **Branch-Protection** — die Regel, die direktes Ändern von `main` verbietet und PR + grüne Gates erzwingt. *Analogie:* „Nur über die Qualitätskontrolle, kein Schleichweg in die Reinschrift."

## Doku & Steuerung

- **Spec** (Specification) — die kurze Vorgabe, *was* eine Aufgabe genau leisten soll, bevor Code entsteht. *Analogie:* der Bauauftrag mit Abnahmekriterien.
- **ADR** (Architecture Decision Record) — ein kurzes Dokument, das eine wichtige Entscheidung samt Begründung festhält. *Analogie:* das Protokoll „Wir haben X entschieden, weil Y".
- **Bootstrap** — der einmalige Einrichtungs-Lauf, der ein Projekt mit allen Regeln, Vorlagen und Prüfungen aufsetzt. *Analogie:* die Werkseinrichtung, bevor produziert wird.
- **Skill** — ein wiederholbarer KI-Arbeitsablauf, den man mit `/name` aufruft (z. B. `/ideation`, `/implement`). *Analogie:* ein eingespieltes Standard-Verfahren auf Knopfdruck.
- **Scaffold** — das automatische Anlegen der Grundgerüst-Dateien (leere Vorlagen). *Analogie:* das Baugerüst + Rohbau, das später gefüllt wird.

## KI-Anbindung

- **MCP** (Model Context Protocol) — der genormte „Stecker", über den die KI sichere Verbindungen zu Tools/Daten bekommt (z. B. Linear, GitHub). *Analogie:* die USB-Norm für KI-Werkzeuge.
- **Agent / Sub-Agent** — eine KI-Instanz, die eine abgegrenzte Aufgabe eigenständig erledigt. *Analogie:* eine Fachkraft mit klarem Auftrag.

## Verweise

Technische Kurz-Definitionen: HANDBUCH **Anhang C**. Wie das alles zusammen dokumentiert wird: [`how-we-document.md`](how-we-document.md).
