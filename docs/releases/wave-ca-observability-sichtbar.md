# Wave CA — Observability sichtbar machen: Doku + Logging/Monitoring-Runbook (BOO-179)

> 🌐 **Sprache:** Deutsch (diese Datei) · [🇬🇧 English](wave-ca-observability-sichtbar.en.md)

**Was jetzt da ist:** Observability ist sichtbar und mit einem Onboarding-Track unterlegt. Die **Substanz** existierte schon (Architektur-Dimension #5 / BOO-14: `observability.md`-Skelett beim Bootstrap, `ARCHITECTURE_DESIGN.md §5/§6`, grafana-Skill) — aber man **sah nicht, wo** Logging/Monitoring-Vorgaben hingehören. Diese Story schliesst die Sichtbarkeits-Lücke. Bewusst **kein** ideation-Interview (würde aufblähen) — Logging/Monitoring ist ein nachgelagerter Track nach dem Bootstrap.

## Änderungen

- **Runbook `docs/runbooks/logging-monitoring.md` (+ `.en`):** Onboarding-Fragen (Konzern-/Compliance-Vorgaben · Log-Ziele · Log-File vs. Prometheus/Grafana · Metriken/Endpoint · Alert-Kanäle · Retention) + **2 kopierbare Beispiele, wie man `observability.md` schreibt** (`payment-api` + `notification-worker`, mit den drei echten Pflicht-Alerts), plus Validierung (`promtool check rules`) und Einspeisung in `ARCHITECTURE_DESIGN.md §5/§6` via `/architecture-review`.
- **HANDBUCH-Kapitel `8d-ter. Logging & Monitoring` (+ `.en`):** Konzept (nachgelagerter Track, Durchsetzung via Architektur-Review/Konzern-IT-Abnahme statt ideation) + die drei Pflicht-Sektionen → verweist aufs Runbook.
- **`observability.md` an drei Stellen erklärt:** HANDBUCH §7 Gruppe G (Callout „hier gehören Logging/Monitoring-Vorgaben hin"), `docs/onboarding/artefakt-landkarte.md` (+ `.en`, war vorher gar nicht gelistet), `docs/runbooks/audit-perspective.md` (+ `.en`, als Audit-Beleg).
- **Bootstrap-Schluss-Checkliste** (`bootstrap/SKILL.md` §7.6 + `.en`): Hinweis „Logging/Monitoring Anforderung? → Vorgaben in `observability.md` eintragen" (reiner Verweis, **kein** Versions-Bump).

## Die drei Pflicht-Sektionen von `observability.md`

Logging-Schema · Metrics-Endpoint · Alert-Rules (`{service}_down` / `_error_rate_high` >5% / `_p95_slow` p95 >1s, Routing via `observability/.env.observability`).

## Abgrenzung

- Keine Änderung an der Observability-Architektur-Dimension selbst (existiert, BOO-14) — nur Sichtbarkeit + Anleitung. **Kein** ideation-Touchpoint. grafana-Skill bleibt standalone.
- Wave-Buchstabe **ca** (bz = Stack-Linter BOO-178).

## Verweise

Spec: `specs/BOO-179.md`. Branch: `tobiaschschmidt/boo-179-docs-observability-sichtbar`. Verwandt: BOO-14 (Observability-Dimension/Skelett), BOO-180 (Doku-DoD), BOO-178 (Stack-Linter, gleiche Form). Operator-Quelle: Tobias, 2026-06-07.
