# Vorab-Fragebogen: bevor wir euer Projekt aufsetzen

> **Worum geht's?** Wir richten für euer Vorhaben eine moderne, KI-gestützte Entwicklungs-Umgebung ein (intern „INTENTRON"-Framework). Bevor wir loslegen, führen wir ein kurzes Setup-Gespräch (~15 Min). Damit das schnell und zielgerichtet läuft, schicken wir euch vorab diese Fragen.
>
> **Was ihr tun müsst:** nichts installieren, nichts vorbereiten — nur diese Fragen lesen und, wo möglich, Antworten parat haben. Es geht allein darum, dass wir verstehen **was ihr bauen wollt** und **in welcher Umgebung**. Je klarer die Antworten, desto besser passt das Setup von Anfang an.
>
> **Unsicher bei einer Frage?** Völlig okay — markiert sie mit „weiß ich noch nicht / klären wir gemeinsam". Niemand muss alles wissen: manche Fragen beantwortet eure IT, andere die Fachseite oder das Management.

## Teil 1 — Was wollt ihr bauen?

**1. Worum geht es in dem Projekt?**
Beschreibt in 2–3 Sätzen, was die Software können soll und für wen.
- *Warum wir das fragen:* Wir müssen den Zweck verstehen, um sinnvolle Qualitäts- und Sicherheitsregeln zu setzen.
- *Beispielantwort:* „Ein internes Web-Portal, über das unser Außendienst Aufträge erfasst und den Status sieht."

**2. Welche Technologie ist geplant?**
Wisst ihr schon, womit gebaut wird? Programmiersprache (z. B. Java, .NET, Node.js, Python) — und gibt es eine Web-Oberfläche (z. B. React/Angular)? Falls noch offen, ist auch das eine gültige Antwort.
- *Warum:* Davon hängt ab, welche Test- und Prüf-Werkzeuge wir einbauen.
- *Beispielantwort:* „Backend in Java (Spring Boot), Web-Frontend in Angular." — oder: „Noch offen, bitte beraten."

**3. Hat die Software eine Web-Oberfläche, bei der Geschwindigkeit wichtig ist?**
Z. B. ein Kundenportal, das schnell laden muss.
- *Warum:* Dann bauen wir eine automatische Performance-Messung ein, die bei jeder Änderung Ladezeit und Bedienbarkeit prüft.
- *Beispielantwort:* „Ja, öffentliches Kundenportal — Ladezeit ist geschäftskritisch." / „Nein, nur ein internes Tool."

**4. Arbeitet euer Team mit einem KI-Programmier-Assistenten?**
Z. B. Claude, GitHub Copilot/Codex, Cursor — oder noch keiner?
- *Warum:* Das Framework richtet sich auf das KI-Tool aus, das eure Entwickler tatsächlich nutzen.
- *Beispielantwort:* „Wir nutzen Claude; einzelne Entwickler zusätzlich Cursor."

**5. Projekt-Eckdaten.**
Wie soll das Projekt heißen? Ein Satz dazu, was es tut. Gibt es schon eine Start-Versionsnummer (sonst nehmen wir 0.1.0)?
- *Beispielantwort:* „Projekt ‚AußendienstPortal', Auftragserfassung für den Außendienst, Start 0.1.0."

**6. Womit plant ihr Aufgaben und Tickets?**
Jira, Azure DevOps, GitHub Issues, Linear — oder noch gar nichts?
- *Warum:* Wir verbinden das Framework mit eurem bestehenden Tool, damit Aufgaben dort sichtbar bleiben, wo ihr eh arbeitet.
- *Beispielantwort:* „Jira, Projekt-Kürzel AP." / „Noch nichts — bitte Vorschlag."

**7. Gibt es besondere Anforderungen an Datenschutz, Regulierung oder KI?**
Trifft etwas davon zu? (Mehrfaches möglich.)
- Die Software verarbeitet **personenbezogene / Kundendaten** → Thema **Datenschutz (DSGVO)**
- Die Software enthält einen **KI-Bestandteil, der (Kunden-)Daten verarbeitet** → Thema **EU AI Act** (KI-Verordnung mit Dokumentationspflichten)
- Ihr seid in einer **regulierten Branche** (Finanzen, Gesundheit, Versicherung, Recht)
- Hohe **Kostenrelevanz** (viele KI-/Cloud-/SaaS-Kosten)
- *Warum:* Je nach Antwort schalten wir automatisch passende Schutz- und Nachweis-Mechanismen dazu (z. B. Datenschutz-Prüfungen, KI-Dokumentation). Trifft nichts zu, bleibt es schlank.
- *Beispielantwort:* „Ja — verarbeitet Kundendaten, Finanzbranche, KI-Komponente zur Betrugserkennung."

**8. Wie streng müssen die Regeln sein?**
Wie kritisch oder reguliert ist das Projekt?
- **locker** — internes Hilfstool, wenig Risiko
- **normal** — produktive Software, übliche Sorgfalt
- **streng** — regulierte/kritische Software mit Audit-Pflicht und Vier-Augen-Prinzip
- *Warum:* Das bestimmt, wie viele automatische Kontrollen und Freigabe-Schritte eingebaut werden. Mehr Strenge = mehr Nachweise (aber auch etwas mehr Aufwand) — wir wählen es passend zu eurem Risiko.
- *Beispielantwort:* „Streng — unterliegt der Finanzaufsicht."

**9. Arbeiten mehrere Personen gleichzeitig am selben Code?**
- *Warum:* Bei paralleler Arbeit richten wir getrennte Arbeitsbereiche ein, damit sich Änderungen nicht gegenseitig überschreiben.
- *Beispielantwort:* „Ja, 4 Entwickler parallel." / „Nein, im Moment eine Person."

**10. Wo wird entwickelt?**
Wo arbeitet das Team konkret mit der Umgebung?
- jeder **lokal auf seinem eigenen Rechner/Laptop**
- auf einem **gemeinsamen Entwicklungs-Server** (z. B. ein Linux-Server in der Cloud)
- ein **größeres Team auf einem zentralen Server**
- *Warum:* Davon hängt ab, ob wir die Umgebung einmal zentral oder pro Rechner einrichten.
- *Beispielantwort:* „Gemeinsamer Linux-Server, 5 Entwickler greifen darauf zu."

## Teil 2 — Was ist schon vorhanden?

**11. Gibt es das Projekt schon, oder fangen wir neu an?**
Falls es existiert: wo liegt es (Server/Pfad)? Falls neu: wo soll es liegen?

**12. Habt ihr ein Code-Repository?**
Z. B. GitHub, GitLab, Azure Repos — mit Adresse (URL)? Oder soll eines angelegt werden? Oder gar keins?
- *Warum:* Dort lebt der Code samt Versions-Historie und den automatischen Prüfungen.

**13. Wo soll die Projekt-Dokumentation leben?**
Habt ihr ein Wiki / Confluence / SharePoint / Notion — oder soll die Doku direkt beim Code liegen?
- *Warum:* Damit Entscheidungen und Wissen auffindbar bleiben, auch noch in Monaten.
- *Beispielantwort:* „Confluence-Bereich ‚AP'." / „Beim Code reicht uns."

**14. Womit verwaltet ihr Tickets — konkret inkl. Zugang?**
(Anschluss an Frage 6.) Welches Tool genau, und das Projekt-/Team-Kürzel, damit wir es anbinden können.

**15. Gibt es schon Zugangsschlüssel / Zugangsdaten, die die Software braucht?**
Z. B. API-Schlüssel zu anderen Systemen.
- *Warum:* Wir behandeln Zugangsdaten sicher und legen sie nie offen im Code ab.
- *Beispielantwort:* „Ja, liegen bereits gesammelt vor." / „Noch keine."

**16. Sollen wir eine Einarbeitungs-Doku für neue Teammitglieder anlegen?**
- *Warum:* Damit neue Entwickler — oder ein anderes Tool — das Projekt schnell übernehmen können, ohne euch löchern zu müssen.

**Zusatz — habt ihr das schon?**
- **Monitoring/Überwachung** (z. B. Grafana, ein Logging-System): vorhanden und nutzen, neu aufbauen, oder noch offen?
- Braucht ihr im Setup **Recherche- oder Diagramm-Funktionen** (optional)?

## Teil 3 — klären wir gemeinsam im Gespräch

- **Doku-Struktur:** Wer bei euch entscheidet über Ablage und Struktur der Dokumentation (gibt es Vorgaben, ein bestehendes Wiki, Namens-Konventionen)?
- **Optionale Automatismen:** Möchtet ihr Zusatzfunktionen wie automatische Selbst-Checks, Doku-Synchronisierung oder eine Lernschleife? Gibt es betriebliche Einwände gegen Automatismen, die in eure Umgebung schreiben? — das entscheiden wir gemeinsam.

## Falls die Software später in eure Live-Umgebung integriert wird

Wenn das fertige Ergebnis in eure bestehenden Systeme eingebunden werden soll (Hosting, eure Deploy-Abläufe, Schnittstellen zu anderen Systemen, Netzwerk, Zugangsdaten, Freigabe-Prozesse), gibt es dafür einen ergänzenden Bogen (`integration-discovery.md`) — den schicken wir separat, sobald es so weit ist.

> **Nur für die, die die Umgebung technisch aufsetzen** (eure IT): aktuelle Node.js-Version, Git und ein KI-Coding-Tool sollten verfügbar sein, plus Zugänge zu KI-Tool / Repository / Ticket-Tool. Die genauen Schritte liefern wir mit.
