# Pitch — Code-Crash Framework

`code-crash-pitch.html` — eine **30-Minuten-Pitch-Präsentation** im OWLIST-Layout. Ziel: jemanden in einer Sitzung vom Framework überzeugen, sodass er es einsetzen will. Zielpublikum gemischt (Business-Hook vorne, technische Gamechanger in der Mitte, Architektur-Tiefe als Backup-Slide).

## Öffnen & präsentieren

Datei einfach im Browser öffnen (Doppelklick) — standalone HTML, kein Build, keine Dependencies.

| Taste | Aktion |
|-------|--------|
| `→` / `←` / Leertaste / Klick | Slide vor / zurück |
| `F` | Vollbild ein/aus |
| `P` | drucken → **PDF exportieren** (jede Slide eine Seite) |
| `Home` / `End` | erste / letzte Slide |

Die Sketches werden relativ aus `../schrader-sketches/` und `../assets/` geladen — daher die Datei **im Repo belassen** (nicht isoliert verschieben), sonst fehlen die Bilder.

## Aufbau (17 Slides)

1. Titel · 2. Problem (Vibe-Coding-Chaos) · 3. Warum jetzt (Jevons/Intent) · 4. Was ist Code-Crash (OS) · 5–9. Gamechanger (Intent · 4P · Quality-Gates · Token-Sprint · tool-agnostisch) · 10. Was wir besser machen · 11. Key-Komponenten · 12. Privacy & Security · 13. Skaliert · 14. Beweis (verify/E2E) · 15. Start · 16. Call to Action · 17. Backup (Pipeline-Detail).

## Inhalts-Quellen

HANDBUCH Anhang M (Schrader-Decoder), README „Why Code-Crash" / „Not one-size-fits-all", Anhang L (4P), Anhang N–T. Farben/Fonts: OWLIST Design System (Beige `#f9f6f1`, Orange `#d77f11`, Poppins).

## Anpassen

Inhalt + Styles stecken in der einen `.html` (CSS im `<head>`, Slides als `<section class="slide">`). Neue Slide = neues `<section>`; der Zähler aktualisiert sich automatisch.
