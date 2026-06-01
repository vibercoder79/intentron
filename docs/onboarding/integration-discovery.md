# Integration-Discovery-Fragebogen

> Zielgruppe: IT-Abteilung des Kunden
> Sprache: Deutsch — englische Fassung siehe [`integration-discovery.en.md`](./integration-discovery.en.md)

## Zweck dieses Dokuments

Das INTENTRON-Framework zusammen mit Claude Code laeuft beim Entwickeln auf einem dedizierten (VPS-)Dev-Setup. Dieses Entwicklungs- und Build-Umfeld ist standardisiert und durch das Framework selbst abgedeckt — dazu muss die Kunden-IT nichts beisteuern.

Dieser Fragebogen erfasst ausschliesslich den **kundenindividuellen Teil**: alles, was die Kunden-IT **vorab** beantworten muss, damit die zu bauende Solution sich anschliessend in die **Live- und Bestandsumgebung des Kunden** integrieren laesst. Es geht also um Continuous Integration und Continuous Deployment **in Ihre Systeme hinein** — nicht um die Entwicklung selbst.

Je vollstaendiger und praeziser die folgenden Cluster beantwortet sind, desto reibungsloser laeuft die spaetere Integration. Unklare oder offene Punkte sind kein Problem: Sie werden als Annahmen markiert und im Projektverlauf gemeinsam geklaert. Bitte beantworten Sie die Fragen so konkret wie moeglich; wo Standards oder bestehende Vorgaben existieren, verweisen Sie gern direkt darauf.

---

## 1. Ziel-Runtime / Hosting der Solution

**Warum wir das fragen:** Wo die Solution am Ende laeuft, bestimmt nahezu alle nachgelagerten Entscheidungen — Deployment-Mechanik, Netzwerk, Secrets, Compliance. Wir muessen frueh wissen, ob wir gegen On-Prem, eine Public Cloud oder ein hybrides Modell bauen, und welche Plattform- und IaC-Standards bei Ihnen gesetzt sind, damit wir uns nicht gegen Ihre bestehenden Konventionen entwickeln.

- Soll die Solution On-Prem, in einer Public Cloud oder hybrid betrieben werden?
- Bei Cloud: welcher Anbieter ist gesetzt (AWS, Azure, GCP, Hetzner, andere)?
- Welche Region bzw. welcher Datenstandort ist vorgeschrieben (z. B. EU, Schweiz, spezifisches Rechenzentrum)?
- Welche Container- bzw. Laufzeit-Plattform ist Standard (Kubernetes, Docker/Compose, reine VMs, Serverless)?
- Falls Kubernetes: gemanagt (EKS/AKS/GKE) oder selbst betrieben? Welche Cluster stehen fuer welche Umgebungen (Dev/Test/Prod) bereit?
- Welcher Infrastructure-as-Code-Standard gilt bei Ihnen (Terraform, Ansible, Helm, Pulumi, CloudFormation)? Gibt es bestehende Module/Repos, an die wir andocken sollen?
- Gibt es Vorgaben zu Betriebssystem, Basis-Images oder gehaerteten Image-Quellen?

---

## 2. Bestehende CI/CD-Systeme des Kunden

**Warum wir das fragen:** Die Solution soll sich in Ihre bestehende Build- und Deploy-Pipeline einfuegen, nicht eine zweite parallele Welt aufmachen. Wir muessen wissen, welches CI/CD-System Sie nutzen, wie Artefakte verwaltet werden und welcher Freigabeprozess vor einem Deployment steht, damit unsere Auslieferung Ihren etablierten Weg geht.

- Welches CI/CD-System ist im Einsatz (Jenkins, GitLab CI, GitHub Actions, Azure DevOps, CircleCI, andere)?
- Wo liegen die Quell-Repositories, und nach welchem Muster werden neue Repos angelegt/verwaltet?
- Welche Artefakt- bzw. Container-Registry wird genutzt (z. B. Artifactory, Nexus, GitLab Registry, ACR/ECR/GCR, Harbor)?
- Welche Branch- und Release-Strategie gilt (Trunk-Based, GitFlow, Release-Branches, Tagging-Konvention)?
- Wie sieht der Freigabe- und Deploy-Prozess aus: automatisiert, manuelle Gates, Vier-Augen-Prinzip?
- Welche Umgebungen existieren (Dev/Integration/Staging/Prod), und wie wird zwischen ihnen promotet?
- Gibt es bestehende Pipeline-Templates, Quality Gates oder Pflicht-Checks (Tests, Linting, Security-Scans), die wir uebernehmen muessen?

---

## 3. Schnittstellen / Zielsysteme / Datenquellen

**Warum wir das fragen:** Die Solution liefert ihren Wert ueber die Anbindung an Ihre Bestandssysteme. Wir muessen die konkreten Zielsysteme, ihre Schnittstellentypen und das Authentifizierungsmodell kennen, um Adapter, Datenflusse und Migrationen sauber zu planen — und um frueh zu erkennen, wo Schema- oder Protokoll-Bruchstellen liegen.

- Welche Bestandssysteme sollen angebunden werden (ERP, CRM, Datenbanken, Fachverfahren, Drittdienste)? Bitte je System mit Version, falls bekannt.
- Welche Schnittstellentypen liegen vor (REST, SOAP, gRPC, Event/Streaming wie Kafka, Message Queues, Datei-/Batch-Transfer)?
- Existiert ein API-Gateway oder Integration-Layer (z. B. Kong, Apigee, Azure API Management, MuleSoft), ueber den wir gehen sollen/muessen?
- Wie funktioniert die Authentifizierung gegenueber diesen Systemen (SSO, OIDC, SAML, LDAP/AD, API-Keys, mTLS, technische Service-Accounts)? Gibt es eine zentrale Identity-Foederation?
- Welche Daten-Schemas/Datenmodelle sind relevant, und gibt es dafuer eine verbindliche Dokumentation?
- Sind Datenmigrationen oder initiale Datenuebernahmen Teil des Vorhabens? Wenn ja, in welchem Umfang und mit welchen Quellen?
- Gibt es Vorgaben zu Datenformaten, Versionierung von Schnittstellen oder Rueckwaertskompatibilitaet?

---

## 4. Netzwerk / Zugang

**Warum wir das fragen:** Auch die beste Solution funktioniert nur, wenn sie die noetigen Endpunkte erreicht und umgekehrt erreichbar ist. Netzwerkfreigaben und Zugangswege haben bei Kunden oft lange Vorlaufzeiten — deshalb klaeren wir sie so frueh wie moeglich, damit sie nicht zum Blocker beim ersten Deployment werden.

- Welche Endpunkte muss die Solution erreichen (interne Systeme, externe Dienste), und sind diese aus der Ziel-Runtime erreichbar?
- Wird ein VPN oder eine dedizierte Verbindung benoetigt, und wer stellt diese bereit?
- Welche Firewall-Freigaben sind erforderlich (Quellen, Ziele, Ports, Protokolle)? Wie ist der Antragsprozess und die typische Vorlaufzeit?
- Gibt es IP-Whitelisting oder Allow-Lists, in die unsere Komponenten aufgenommen werden muessen?
- Erfolgt der Zugang ueber einen Bastion-/Jump-Host? Wie wird dieser Zugriff bereitgestellt und protokolliert?
- Welche Egress-Regeln gelten (ausgehender Traffic, Proxy-Pflicht, gesperrte Ziele)?
- Gibt es Netzwerksegmentierung/Zonen (DMZ, interne Zonen), die das Solution-Design beeinflussen?

---

## 5. Secrets-Management des Kunden

**Warum wir das fragen:** Die Solution braucht Zugangsdaten, Zertifikate und Schluessel, um mit Ihren Systemen zu sprechen. Diese duerfen nie im Code, in Pipelines oder in Konfigurationsdateien landen. Wir muessen Ihr Secrets-Management kennen, um Solution-Secrets von Anfang an ueber den von Ihnen vorgesehenen, sicheren Weg in die Zielumgebung zu bringen.

- Welches Secrets-Management ist im Einsatz (HashiCorp Vault, Azure Key Vault, AWS Secrets Manager, GCP Secret Manager, CyberArk, anderes)?
- Wie werden Secrets zur Laufzeit an Anwendungen ausgeliefert (Injection, Sidecar, Mount, Umgebungsvariablen via Plattform)?
- Wer legt Secrets an und rotiert sie — und wie sollen die Secrets der Solution beantragt/bereitgestellt werden?
- Gibt es Vorgaben zu Rotation, Gueltigkeitsdauer und Verschluesselung?
- Wie werden TLS-/Client-Zertifikate verwaltet und ausgerollt?
- Wie kommen Secrets in die CI/CD-Pipeline, ohne dort im Klartext zu erscheinen?
- Gibt es einen definierten Prozess fuer den Umgang mit kompromittierten Secrets?

---

## 6. Compliance-/Audit-Vorgaben des Kunden

**Warum wir das fragen:** Compliance-Anforderungen sind keine nachgelagerte Pruefung, sondern Designvorgabe. Wir muessen Ihre branchen- und unternehmensspezifischen Pflichten frueh kennen, damit Architektur, Datenhaltung und Auslieferungsprozess von Anfang an konform sind und keine spaeten, teuren Umbauten noetig werden.

- Welche branchen- oder unternehmensspezifischen Pflichten gelten (z. B. ISO 27001, SOC 2, BAIT/VAIT, KRITIS, HIPAA, PCI-DSS, regulatorische Vorgaben Ihrer Branche)?
- Wie werden Daten klassifiziert (oeffentlich, intern, vertraulich, streng vertraulich), und welche der verarbeiteten Daten fallen in welche Klasse?
- Sind Penetrationstests, Code-Audits oder externe Freigaben vor Go-Live vorgeschrieben? Durch wen, mit welchem Vorlauf?
- Wie sieht der Change-Approval-Prozess aus (Change Advisory Board, Ticketpflicht, Freigabe-Instanzen)?
- Welche Audit-/Logging-Anforderungen bestehen (Nachvollziehbarkeit, Aufbewahrungsfristen, revisionssichere Protokolle)?
- Gibt es Vorgaben zu Datenresidenz, Auftragsverarbeitung oder Unterauftragnehmern?

> **Querverweis:** Enthaelt die Solution einen KI-Anteil, kommen zusaetzliche regulatorische Anforderungen hinzu — insbesondere der EU AI Act sowie der Datenschutz (DSGVO/BDSG/nDSG). Diese werden gesondert ueber den `dpo`-Skill (Data Protection Officer) erfasst und bewertet; bitte halten Sie etwaige KI-Komponenten und die dabei verarbeiteten personenbezogenen Daten bereit.

---

## 7. Verantwortlichkeiten / Go-Live

**Warum wir das fragen:** Ein technisch sauberer Deploy nuetzt nichts, wenn beim Go-Live unklar ist, wer entscheidet, wer freigibt und wer im Fehlerfall handelt. Klare Verantwortlichkeiten, ein abgestimmter Cutover-Plan und ein definierter Rollback machen den Uebergang in den Live-Betrieb planbar und reduzieren das Risiko erheblich.

- Wer sind die Ansprechpartner auf Seiten der Kunden-IT (fachlich, technisch, Betrieb)? Bitte mit Rolle und Erreichbarkeit.
- Wie ist die RACI-Verteilung fuer Aufbau, Betrieb und Wartung der Solution?
- Wie sieht der Eskalationsweg aus (Stufen, Ansprechpartner, Reaktionszeiten)?
- Welche Wartungsfenster stehen fuer Deployments und Aenderungen zur Verfuegung?
- Welche SLAs gelten fuer Verfuegbarkeit, Reaktions- und Wiederherstellungszeiten?
- Wie soll der Cutover/Go-Live ablaufen (Big Bang, schrittweise, parallel)? Gibt es einen festen Termin?
- Wie ist die Rollback-Strategie definiert (Kriterien, Verantwortliche, technische Umsetzung)?
- Wer uebernimmt nach Go-Live Betrieb und Wartung — Kunde, wir, geteilt?

---

## Hinweis

Auf Basis Ihrer Antworten entsteht der **individuelle Integrations- und CI-Teil des Projekt-Setups**: die konkrete Anbindung der Solution an Ihre Pipelines, Zielsysteme, Netzwerk- und Secrets-Infrastruktur sowie der abgestimmte Go-Live- und Rollback-Plan. Offene Punkte werden als Annahmen dokumentiert und gemeinsam geschaerft, bevor sie in die Umsetzung einfliessen.
