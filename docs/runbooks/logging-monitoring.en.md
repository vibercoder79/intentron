# Runbook: Logging & Monitoring — filling in `observability.md`

> **Audience:** Operators who, after the bootstrap, want to define the logging/monitoring requirements for their project — which fields get logged, what is exposed as a metric, what alerts fire. Under 30 minutes, manual, with copy-paste examples. DE: [`logging-monitoring.md`](logging-monitoring.md).

## When this runbook?

Logging & Monitoring is a **downstream track** — not part of the bootstrap interview. Deliberate design choice: **a framework is not an architecture workshop.** The bootstrap creates the **skeleton** `observability.md` in the project root (architecture dimension #5, BOO-14) — you fill in the substantive requirements afterwards. Enforcement happens naturally: whoever forgets logging/monitoring fails the architecture review (`/architecture-review` checks dimension #5) or the corporate-IT sign-off.

This runbook shows **how** to fill `observability.md`: which questions to clarify first and what concrete example content for the three mandatory sections looks like. Result: `ARCHITECTURE_DESIGN.md §5/§6` picks up your requirements because it references `observability.md`.

**Scope:** this runbook covers **filling in** the docs, not a new architecture mechanism — `observability.md` + dimension #5 already exist (BOO-14). Dashboards (Grafana) are a separate topic → [grafana skill](#further-reading). Stack scope is **Node.js and Python**; frontend logs through the backend or an external error tracker (Sentry or similar), not as its own service section.

## What is `observability.md`?

A bootstrap-generated **observability skeleton in the project root** (BOO-14, `file-templates` §Group G), one section per service. It defines **three mandatory sections**:

1. **Logging schema** — structured JSON log format with mandatory fields (`timestamp`, `level`, `service`, `trace_id`, `message`, `context`), log levels and log targets.
2. **Metrics endpoint** — what is exposed (`GET /metrics` for Prometheus, port convention `9090 + N`), mandatory metrics (`{service}_up`, `_requests_total`, `_request_duration_seconds`, `_errors_total`), `lib/metrics` convention.
3. **Alert rules** — three mandatory alerts under `observability/alerts/<service>.yml` (`{service}_down`, `{service}_error_rate_high`, `{service}_p95_slow`); routing config in `observability/.env.observability` (Telegram/Slack/Email — gitignored, holds secrets).

`ARCHITECTURE_DESIGN.md §5/§6` references `observability.md`; `/architecture-review` checks dimension #5. **Whoever enters requirements here ensures the architecture docs and review pick them up.** Full template + stack examples: [`bootstrap/references/file-templates.en.md`](../../bootstrap/references/file-templates.en.md) §`observability.md`.

## Step 1 — clarify the onboarding questions

Before you fill `observability.md`, clarify these questions — ideally with the project's domain/IT owner. Each answer lands in one of the three mandatory sections.

| Question | Clarifies | Affects section |
|---|---|---|
| **Corporate / compliance requirements?** Are there central IT/audit mandates (log format, retention periods, central platform)? | The frame that overrides everything else | all three |
| **Log targets?** Where do logs go — `stdout` (container default), file, central platform (ELK, Loki, Datadog, Splunk)? | Where logs are aggregated | logging schema |
| **Log file vs. Prometheus/Grafana?** Is structured logging enough, or are metrics also scraped and visualized in dashboards? | Whether the metrics endpoint is actively operated | metrics endpoint |
| **Metrics / endpoint?** Which metrics beyond the mandatory four? Port assignment per service? | Content of the metrics table | metrics endpoint |
| **Alert channels?** Where do alerts go — Telegram, Slack, email, PagerDuty? Route `critical` vs. `warning` separately? | Receiver routing in `.env.observability` | alert rules |
| **Retention?** How long to keep logs/metrics (compliance, storage cost)? | Retention note | logging schema (+ corporate mandates) |

> [!note] No forced interview
> This is **not** a bootstrap question and not a forced interview (it would bloat ideation). You answer these questions when the project nears production or the corporate-IT sign-off is due. As long as no requirement exists, the skeleton stays in place with its conservative defaults.

## Step 2 — write `observability.md` (the mandatory sections)

The two examples below show complete, **copy-paste** content. Example A is a minimal web service, example B adds a second service. The service name in **logs** is kebab-case (`payment-api`), in **Prometheus metric names** it is snake-case (`payment_api`) — Prometheus does not allow hyphens.

### Example A — simple web service `payment-api`

**Logging schema** (already present as a table in the skeleton — here made concrete for the service):

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

- **Log level:** `info` in production, `debug` locally (`LOG_LEVEL` env).
- **Log target:** `stdout` as JSON (container default); aggregation by the platform (e.g. Loki). Logger: pino (Node) or structlog (Python) with a JSON renderer — **no** `console.log`/`print`.
- **Retention:** 30 days in the log platform (corporate mandate), then rotation.

**Metrics endpoint** — entry in the service table:

| Service | Port | Metrics URL |
|---|---|---|
| payment-api | `9091` | `http://localhost:9091/metrics` |

Per-service section in `observability.md`:

```markdown
### payment-api

- **Language / stack:** Node.js (TypeScript)
- **Metrics endpoint:** `http://localhost:9091/metrics`
- **Alert rules:** `observability/alerts/payment-api.yml`
- **Logger:** pino with JSON renderer (`level: 'info'` in production, `'debug'` locally)
- **Prometheus service label:** `payment_api` (snake_case)
- **Known error_type values:** `validation`, `db`, `upstream_timeout`, `gateway`, `internal`
```

Implement the four mandatory metrics (`payment_api_up`, `payment_api_requests_total`, `payment_api_request_duration_seconds`, `payment_api_errors_total`) following the stack example in the template (`src/lib/metrics.ts` / `app/metrics.py`).

**Alert rules** — `observability/alerts/payment-api.yml` (from the template, `{{SERVICE_NAME}}` → `payment_api`, file name stays kebab-case):

```yaml
# observability/alerts/payment-api.yml
# Prometheus alert rules for service payment_api (snake_case for metric names).
# Validation: promtool check rules observability/alerts/*.yml
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

**Alert routing** — `observability/.env.observability` (gitignored, never commit):

```bash
# observability/.env.observability — NEVER commit (tokens/webhooks)
ALERTMANAGER_RECEIVER="default"
ALERTMANAGER_URL="http://localhost:9093"

# critical → Telegram (immediate action)
TELEGRAM_BOT_TOKEN=""
TELEGRAM_CHAT_ID=""

# warning → Slack (non-blocking)
# SLACK_WEBHOOK_URL=""
```

Routing convention: `critical` (service down) → pager/Telegram; `warning` (degraded: high errors, high latency) → Slack/email. Which receiver gets which severity is decided by the Alertmanager config — `.env.observability` is the single source of truth for routing, **not** a skill.

### Example B — add a second service `notification-worker`

When adding a service, duplicate the per-service section and take the **next free port**:

| Service | Port | Metrics URL |
|---|---|---|
| payment-api | `9091` | `http://localhost:9091/metrics` |
| notification-worker | `9092` | `http://localhost:9092/metrics` |

```markdown
### notification-worker

- **Language / stack:** Python
- **Metrics endpoint:** `http://localhost:9092/metrics`
- **Alert rules:** `observability/alerts/notification-worker.yml`
- **Logger:** structlog with JSON renderer
- **Prometheus service label:** `notification_worker` (snake_case)
- **Known error_type values:** `validation`, `db`, `upstream_timeout`, `internal`
```

Then create `observability/alerts/notification-worker.yml` analogous to example A (`payment_api` → `notification_worker`), and maintain `services: [payment-api, notification-worker]` in the `observability.md` frontmatter.

## Step 3 — validate

Alert rule files must pass promtool validation (mandatory before merge):

```bash
promtool check rules observability/alerts/*.yml
```

If `promtool` is missing locally, use Docker:

```bash
docker run --rm -v "$PWD/observability/alerts:/rules" \
  prom/prometheus promtool check rules /rules
```

Whether the check lives in the CI job or locally is an operator decision — the bootstrap creates the rules, not the CI hook.

## Step 4 — feed it into the architecture docs

Once `observability.md` is filled, `ARCHITECTURE_DESIGN.md §5/§6` picks up the requirements (it references `observability.md`). Verify via `/architecture-review` — the skill checks **dimension #5 (observability)** against what `observability.md` says. Empty or unanswered mandatory sections surface here (or at the latest during the corporate-IT sign-off).

## Anti-patterns

- **Plain-text logs** (`console.log`/`print`/unstructured) — aggregation and search break down. A JSON renderer is mandatory.
- **Hyphen in Prometheus metric names** — `payment-api_up` is invalid. Logs `payment-api`, metrics `payment_api`.
- **Deleting mandatory alerts** — removing `_down` means no alarm when the service dies.
- **Loosening alert thresholds without justification** — `> 0.05` and `> 1s` are conservative defaults; a change belongs documented in the spec.
- **Routing detail in the rule file** (Telegram channel IDs, Slack webhooks) — belongs in `.env.observability` / Alertmanager, not in the rule.
- **Committing `.env.observability`** — it holds tokens, it is gitignored. Not even "just to test".
- **Frontend as its own service section** — frontend logs through the backend or an external error tracker.

---

## Further reading

| Topic | Source |
|---|---|
| Operator short version concept | HANDBUCH chapter "Logging & Monitoring" ([`HANDBUCH.en.md`](../../HANDBUCH.en.md)) |
| Full `observability.md` template + stack examples (Node/Python) | [`bootstrap/references/file-templates.en.md`](../../bootstrap/references/file-templates.en.md) §`observability.md` |
| Building dashboards in Grafana / PromQL queries | [`grafana/SKILL.en.md`](../../grafana/SKILL.en.md) |
| Observability requirements as audit evidence | [`audit-perspective.en.md`](audit-perspective.en.md) |
| Performance gate (P95 baseline in CI) | [`bootstrap/references/file-templates.en.md`](../../bootstrap/references/file-templates.en.md) §performance baseline gate |
| Look up terms | [`../glossar.en.md`](../glossar.en.md) |

---

> *German version: [`logging-monitoring.md`](logging-monitoring.md).*
