# Wave AI — Enterprise-Readiness (BOO-100…103)

Vier zusammenhaengende Bausteine aus der Konzern-Vorbereitung 2026-06-01. Reine Doku + ein modularer opt-in Compliance-Katalog. Kein Eingriff in die Kern-Pipeline.

## BOO-100 — Value-Prop-Frame
README „Why INTENTRON" + HANDBUCH §1 (DE+EN) um den Frame „schneller UND compliant — Verstoesse werden im Commit gefangen, nicht im nachgelagerten Audit" ergaenzt. Benennt CISO/Auditor als Problemfigur; belegt durch Gates (sensitive-paths/personal-data, Layer-0-Bodyguard), Spec-Linkage, audit-trace.sh, heavy-Modus.

## BOO-101 — EU AI Act modular
Neuer dpo-Kontrollkatalog `dpo/controls/eu-ai-act.yml` (gleiches Schema, vom AUDIT-Runner automatisch mitgeladen) + `dpo/references/ai-system-template.md` (`AI_SYSTEM.md`-Vorlage). Bootstrap-Add-on `[ ] EU AI Act` (strikt opt-in, setzt Privacy voraus). Deckt KI-VO-Dokumentationspflichten (Risikoklasse, Transparenz, Human Oversight, Logging, GPAI) ab — Urteils-Checks als REVIEW-NEEDED, KEINE Rechtsberatung. Kein neuer Skill/Runner/Dependency.

## BOO-102 — Integration-Discovery-Fragebogen
`docs/onboarding/integration-discovery.md` (+ .en): 7 Frage-Cluster fuer den kundenindividuellen Integrations-/CI-Teil (Hosting, CI/CD, Schnittstellen, Netz, Secrets, Compliance, RACI/Go-Live) — was die Kunden-IT vorab klaeren muss, damit die Solution in die Live-Umgebung integriert.

## BOO-103 — Audit-/CISO-Runbook
`docs/runbooks/audit-perspective.md` (+ .en): „Audit-Frage → Beleg → Ort"-Tabelle + Pruef-Schritte + Caveats. Aggregiert vorhandene Evidenz (Spec-Gate, audit-trace.sh, journal/reports, Branch-Protection, dpo-audit.py, verify-setup, Vier-Augen). Plus: toter `GOVERNANCE.md`-Verweis in `audit-trace.sh` gefixt.

Specs: `specs/BOO-100.md`…`BOO-103.md`. Release: v0.7.0.
