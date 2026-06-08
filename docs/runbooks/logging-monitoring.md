# Runbook: Logging & Monitoring — `observability.md` füllen

> **Zielgruppe:** Operator:in, die nach dem Bootstrap die Logging-/Monitoring-Vorgaben für ihr Projekt festlegen will — welche Felder geloggt werden, was als Metrik exponiert wird, was alarmiert. In unter 30 Minuten, manuell, mit kopierbaren Beispielen. EN: [`logging-monitoring.en.md`](logging-monitoring.en.md).

## Wann dieses Runbook?

Logging & Monitoring ist ein **nachgelagerter Track** — nicht Teil des Bootstrap-Interviews. Bewusste Design-Entscheidung: **Framework ≠ Architektur-Workshop.** Der Bootstrap legt das **Skelett** `observability.md` im Projekt-Root an (Architektur-Dimension #5, BOO-14) — die fachlichen Vorgaben trägst **du** danach ein. Durchsetzung passiert natürlich: Wer Logging/Monitoring vergisst, fällt bei der Architektur-Review (`/architecture-review` prüft Dimension #5) oder der Konzern-IT-Abnahme durch.

Dieses Runbook zeigt, **wie** man `observability.md` füllt: welche Fragen du vorher klärst und wie konkrete Beispiel-Inhalte für die drei Pflicht-Sektionen aussehen. Ergebnis: `ARCHITECTURE_DESIGN.md §5/§6` nimmt deine Vorgaben auf, weil es `observability.md` referenziert.

**Abgrenzung:** Dieses Runbook beschreibt das **Füllen** der Doku, keine neue Architektur-Mechanik — `observability.md` + Dimension #5 existieren bereits (BOO-14). Dashboards (Grafana) sind ein eigenes Thema → [grafana-Skill](#weiterlesen). Stack-Scope ist **Node.js und Python**; Frontend logged über das Backend oder einen externen Error-Tracker (Sentry o.ä.), nicht als eigene Service-Sektion.

## Was ist `observability.md`?

Vom Bootstrap generiertes **Observability-Skelett im Projekt-Root** (BOO-14, `file-templates` §Gruppe G), eine Sektion pro Service. Es definiert **drei Pflicht-Sektionen**:

1. **Logging-Schema** — strukturiertes JSON-Log-Format mit Pflicht-Feldern (`timestamp`, `level`, `service`, `trace_id`, `message`, `context`), Log-Level und Log-Zielen.
2. **Metrics-Endpoint** — was exponiert wird (`GET /metrics` für Prometheus, Port-Konvention `9090 + N`), Pflicht-Metriken (`{service}_up`, `_requests_total`, `_request_duration_seconds`, `_errors_total`), `lib/metrics`-Konvention.
3. **Alert-Rules** — drei Pflicht-Alerts unter `observability/alerts/<service>.yml` (`{service}_down`, `{service}_error_rate_high`, `{service}_p95_slow`); Routing-Config in `observability/.env.observability` (Telegram/Slack/Email — gitignored, enthält Secrets).

`ARCHITECTURE_DESIGN.md §5/§6` referenziert `observability.md`; `/architecture-review` prüft Dimension #5. **Wer hier Vorgaben einträgt, sorgt dafür, dass Architektur-Doku und Review sie aufnehmen.** Vollständiges Template + Stack-Beispiele: [`bootstrap/references/file-templates.md`](../../bootstrap/references/file-templates.md) §`observability.md`.

## Schritt 1 — Onboarding-Fragen klären

Bevor du `observability.md` füllst, klärst du diese Fragen — am besten mit dem fachlich/IT-Verantwortlichen des Projekts. Jede Antwort landet in einer der drei Pflicht-Sektionen.

| Frage | Klärt | Wirkt auf Sektion |
|---|---|---|
| **Konzern-/Compliance-Vorgaben?** Gibt es zentrale IT-/Audit-Vorgaben (Log-Format, Aufbewahrungsfristen, zentrale Plattform)? | Rahmen, der alles andere überschreibt | alle drei |
| **Log-Ziele?** Wohin gehen Logs — `stdout` (Container-Standard), Datei, zentrale Plattform (ELK, Loki, Datadog, Splunk)? | Wo Logs aggregiert werden | Logging-Schema |
| **Log-File vs. Prometheus/Grafana?** Reicht strukturiertes Logging, oder werden zusätzlich Metriken gescraped und in Dashboards visualisiert? | Ob der Metrics-Endpoint aktiv betrieben wird | Metrics-Endpoint |
| **Metriken / Endpoint?** Welche Metriken über die Pflicht-Vier hinaus? Port-Belegung pro Service? | Inhalt der Metrics-Tabelle | Metrics-Endpoint |
| **Alert-Kanäle?** Wohin gehen Alerts — Telegram, Slack, Email, PagerDuty? `critical` vs. `warning` getrennt routen? | Receiver-Routing in `.env.observability` | Alert-Rules |
| **Retention / Aufbewahrung?** Wie lange Logs/Metriken aufbewahren (Compliance, Speicherkosten)? | Aufbewahrungs-Notiz | Logging-Schema (+ Konzern-Vorgaben) |

> [!note] Kein Interview-Zwang
> Das ist **keine** Bootstrap-Frage und kein erzwungenes Interview (würde ideation aufblähen). Du beantwortest die Fragen, wenn das Projekt produktionsnah wird oder die Konzern-IT-Abnahme ansteht. Solange keine Anforderung existiert, bleibt das Skelett mit den konservativen Defaults stehen.

## Schritt 2 — `observability.md` schreiben (die Pflicht-Sektionen)

Die folgenden zwei Beispiele zeigen vollständige, **kopierbare** Inhalte. Beispiel A ist ein minimaler Web-Service, Beispiel B ergänzt einen zweiten Service. Service-Name in **Logs** ist Kebab-Case (`payment-api`), in **Prometheus-Metrik-Namen** Snake-Case (`payment_api`) — Prometheus erlaubt keine Bindestriche.

### Beispiel A — einfacher Web-Service `payment-api`

**Logging-Schema** (im Skelett bereits als Tabelle vorhanden — hier konkretisiert für den Service):

```json
{
  "timestamp": "2026-06-08T09:15:42.071Z",
  "level": "error",
  "service": "payment-api",
  "trace_id": "7b2e1f90-4c3a-4d11-9a8e-1f2b3c4d5e6f",
  "message": "Payment capture failed: gateway timeout",
  "context": {
    "user_id": "u_1024",
    "request_path": "/api/payments/capture",
    "error_code": "GATEWAY_TIMEOUT",
    "order_id": "o_55021"
  }
}
```

- **Log-Level:** `info` in Production, `debug` lokal (`LOG_LEVEL`-Env).
- **Log-Ziel:** `stdout` als JSON (Container-Standard); Aggregation durch die Plattform (z.B. Loki). Logger: pino (Node) bzw. structlog (Python) mit JSON-Renderer — **kein** `console.log`/`print`.
- **Retention:** 30 Tage in der Log-Plattform (Konzern-Vorgabe), danach Rotation.

**Metrics-Endpoint** — Eintrag in der Service-Tabelle:

| Service | Port | Metrics-URL |
|---|---|---|
| payment-api | `9091` | `http://localhost:9091/metrics` |

Pro-Service-Sektion in `observability.md`:

```markdown
### payment-api

- **Sprache / Stack:** Node.js (TypeScript)
- **Metrics-Endpoint:** `http://localhost:9091/metrics`
- **Alert-Rules:** `observability/alerts/payment-api.yml`
- **Logger:** pino mit JSON-Renderer (`level: 'info'` in Production, `'debug'` lokal)
- **Service-Label für Prometheus:** `payment_api` (snake_case)
- **Bekannte error_type-Werte:** `validation`, `db`, `upstream_timeout`, `gateway`, `internal`
```

Die vier Pflicht-Metriken (`payment_api_up`, `payment_api_requests_total`, `payment_api_request_duration_seconds`, `payment_api_errors_total`) implementierst du nach dem Stack-Beispiel im Template (`src/lib/metrics.ts` / `app/metrics.py`).

**Alert-Rules** — `observability/alerts/payment-api.yml` (aus dem Template, `{{SERVICE_NAME}}` → `payment_api`, Dateiname bleibt Kebab-Case):

```yaml
# observability/alerts/payment-api.yml
# Prometheus Alert Rules für Service payment_api (snake_case für Metrik-Namen).
# Validierung: promtool check rules observability/alerts/*.yml
groups:
  - name: payment_api_alerts
    rules:
      - alert: payment_api_down
        expr: payment_api_up == 0
        for: 2m
        labels:
          severity: critical
          service: payment_api
        annotations:
          summary: "payment_api is down"
          description: |
            Service payment_api reports up == 0 for more than 2 minutes.
            Check process, container or scrape target.

      - alert: payment_api_error_rate_high
        expr: |
          (
            sum(rate(payment_api_errors_total[5m]))
            /
            sum(rate(payment_api_requests_total[5m]))
          ) > 0.05
        for: 5m
        labels:
          severity: warning
          service: payment_api
        annotations:
          summary: "payment_api error rate above 5%"
          description: |
            Error rate (errors_total / requests_total over 5m) is above 5%
            for more than 5 minutes. Inspect recent deploys and upstream
            dependencies.

      - alert: payment_api_p95_slow
        expr: |
          histogram_quantile(
            0.95,
            sum(rate(payment_api_request_duration_seconds_bucket[5m])) by (le)
          ) > 1
        for: 5m
        labels:
          severity: warning
          service: payment_api
        annotations:
          summary: "payment_api p95 latency above 1s"
          description: |
            95th percentile request duration is above 1 second for more
            than 5 minutes. Check DB, upstream calls or recent code changes.
```

**Alert-Routing** — `observability/.env.observability` (gitignored, nie committen):

```bash
# observability/.env.observability — NIEMALS committen (Tokens/Webhooks)
ALERTMANAGER_RECEIVER="default"
ALERTMANAGER_URL="http://localhost:9093"

# critical → Telegram (sofortige Aktion)
TELEGRAM_BOT_TOKEN=""
TELEGRAM_CHAT_ID=""

# warning → Slack (nicht-blockierend)
# SLACK_WEBHOOK_URL=""
```

Routing-Konvention: `critical` (Service down) → Pager/Telegram; `warning` (degradiert: Errors hoch, Latenz hoch) → Slack/Email. Welcher Receiver welche Severity bekommt, entscheidet die Alertmanager-Config — `.env.observability` ist die Single Source of Truth fürs Routing, **kein** Skill.

### Beispiel B — zweiten Service `notification-worker` ergänzen

Beim Hinzufügen eines Services duplizierst du die Pro-Service-Sektion und nimmst den **nächsten freien Port**:

| Service | Port | Metrics-URL |
|---|---|---|
| payment-api | `9091` | `http://localhost:9091/metrics` |
| notification-worker | `9092` | `http://localhost:9092/metrics` |

```markdown
### notification-worker

- **Sprache / Stack:** Python
- **Metrics-Endpoint:** `http://localhost:9092/metrics`
- **Alert-Rules:** `observability/alerts/notification-worker.yml`
- **Logger:** structlog mit JSON-Renderer
- **Service-Label für Prometheus:** `notification_worker` (snake_case)
- **Bekannte error_type-Werte:** `validation`, `db`, `upstream_timeout`, `internal`
```

Dann `observability/alerts/notification-worker.yml` analog zu Beispiel A anlegen (`payment_api` → `notification_worker`), und im Frontmatter von `observability.md` `services: [payment-api, notification-worker]` pflegen.

## Schritt 3 — Validieren

Alert-Rule-Files müssen die Promtool-Validierung bestehen (Pflicht vor Merge):

```bash
promtool check rules observability/alerts/*.yml
```

Falls `promtool` lokal fehlt, per Docker:

```bash
docker run --rm -v "$PWD/observability/alerts:/rules" \
  prom/prometheus promtool check rules /rules
```

Ob der Check im CI-Job oder lokal zuhause ist, ist Operator-Entscheidung — der Bootstrap legt die Rules an, nicht den CI-Hook.

## Schritt 4 — In die Architektur-Doku einspeisen

Sobald `observability.md` gefüllt ist, nimmt `ARCHITECTURE_DESIGN.md §5/§6` die Vorgaben auf (es referenziert `observability.md`). Prüfen via `/architecture-review` — der Skill checkt **Dimension #5 (Observability)** gegen das, was in `observability.md` steht. Leere oder unbeantwortete Pflicht-Sektionen fallen hier (oder spätestens bei der Konzern-IT-Abnahme) auf.

## Anti-Patterns

- **Klartext-Logs** (`console.log`/`print`/unstrukturiert) — Aggregation und Suche brechen zusammen. JSON-Renderer ist Pflicht.
- **Bindestrich in Prometheus-Metrik-Namen** — `payment-api_up` ist ungültig. Logs `payment-api`, Metriken `payment_api`.
- **Pflicht-Alerts löschen** — wer `_down` entfernt, kriegt keinen Alarm, wenn der Service stirbt.
- **Alert-Schwellen weicher stellen ohne Begründung** — `> 0.05` und `> 1s` sind konservative Defaults; Änderung gehört ins Spec dokumentiert.
- **Routing-Detail in der Rule-Datei** (Telegram-Channel-IDs, Slack-Webhooks) — gehört in `.env.observability` / Alertmanager, nicht in die Rule.
- **`.env.observability` committen** — enthält Tokens, ist gitignored. Auch nicht "kurz zum Testen".
- **Frontend als eigene Service-Sektion** — Frontend logged über Backend oder externen Error-Tracker.

---

## Weiterlesen

| Thema | Quelle |
|---|---|
| Operator-Kurzfassung Konzept | HANDBUCH-Kapitel „Logging & Monitoring" ([`HANDBUCH.md`](../../HANDBUCH.md)) |
| Vollständiges `observability.md`-Template + Stack-Beispiele (Node/Python) | [`bootstrap/references/file-templates.md`](../../bootstrap/references/file-templates.md) §`observability.md` |
| Dashboards in Grafana bauen / PromQL-Queries | [`grafana/SKILL.md`](../../grafana/SKILL.md) |
| Observability-Vorgaben als Audit-Beleg | [`audit-perspective.md`](audit-perspective.md) |
| Performance-Gate (P95-Baseline in CI) | [`bootstrap/references/file-templates.md`](../../bootstrap/references/file-templates.md) §Performance-Baseline-Gate |
| Begriffe nachschlagen | [`../glossar.md`](../glossar.md) |

---

> *Englische Fassung: [`logging-monitoring.en.md`](logging-monitoring.en.md).*
