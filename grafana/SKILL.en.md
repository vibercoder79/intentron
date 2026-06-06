---
name: grafana
recommended_model: sonnet  # BOO-84 — tier mapping in bootstrap/references/model-tiers.json
description: |
  Grafana dashboard development and metric queries.
  Uses the official Grafana MCP server to create, read and update dashboards directly
  in Grafana Cloud and to run PromQL queries.
  Use when the operator says "Grafana", "dashboard", "panel", "query metric",
  "alert rule", "build grafana" or "/grafana".
version: 1.1.0
language: en
requires_mcp:
  - name: grafana
    description: Grafana MCP server (grafana/mcp-grafana Docker)
metadata:
  hermes:
    category: coding
    tags: [observability, dashboards]
    requires_toolsets: [terminal, grafana-mcp]
    related_skills: [architecture-review, sprint-review]
---

# Grafana Skill — Dashboard Development

Direct access to Grafana Cloud via MCP. Build dashboards, query metrics, create panels — without manual JSON export/import.

## Step 0: Load environment

1. Read `.claude/environment.json` (if present — otherwise fall back to defaults and log a warning).
2. Extract paths from `paths.*` as needed (e.g. `paths.reports_local`, `paths.lessons_l3`, `paths.specs`).
3. Before any tool invocation, check `tools_available.<tool>`. If `false` or missing, the skill skips the call and notes it in the output.
4. Missing-file fallback: assume the schema defaults (`journal/`, `journal/reports/local/`, `specs/`, `ARCHITECTURE_DESIGN.md`) and add a note to the output: "Note: `.claude/environment.json` is missing — defaults active. Recommendation: re-run `/bootstrap` or create the file manually."

## Workflow

### 1. Clarify the goal
- Build panel → which metric? Which visualization type? (Timeseries, Gauge, Table, Stat)
- Run query → which metric? Which time range?
- Find dashboard → `search_dashboards` first

### 2. Understand the metric
```
query_prometheus(expr="<metric_name>", datasourceUid="<uid>")
```
Check result — values plausible? Labels present?

### 3. Create or update dashboard/panel
```
get_dashboard(uid="<uid>")          # Load existing
patch_dashboard(...)                # Targeted update
update_dashboard(...)               # Full replace
```

---

## Conventions

| Convention | Value |
|------------|-------|
| **Grafana Cloud instance** | Primary — all dashboards are built here |
| **Folder** | Project name (all dashboards in one folder) |
| **Panel naming** | `<Group>: <What>` e.g. `Agents: Signal Age`, `Trading: P&L Today` |
| **Refresh** | 30s for live dashboards |
| **Default time range** | Last 1 hour |
| **Colors** | Green = OK, Yellow = Warning, Red = Critical (consistent) |

---

## Panel recipes (examples)

### Agent Health — Signal Age
```promql
signal_age_seconds{agent=~".+"}
```
- Type: Table or Gauge per agent
- Thresholds: <600s=green, <1800s=yellow, >1800s=red

### P&L Today
```promql
pnl_today_usd
```
- Type: Stat (big number), Unit: USD

### Win rate 7 days
```promql
win_rate_7d * 100
```
- Type: Gauge (0–100%)
- Thresholds: >55=green, >45=yellow, <45=red

### Exchange / Service Status
```promql
exchange_up{exchange=~".+"}
```
- Type: Stat per exchange/service
- 1=UP (green), 0=DOWN (red)

---

## Common tasks

> **Before `overwrite=true` — operator confirmation (required):** `update_dashboard(..., overwrite=true)` **replaces** the existing dashboard in Grafana Cloud — remotely, with no local rollback. Before any overwrite, tell the operator the target dashboard (UID/title) + planned change and wait for approval. When in doubt use `overwrite=false` (create new) or `patch_dashboard` (targeted) instead of a full replace. Matches the recommended Claude Code mode `default` (ask before edits) for `/grafana` — see HANDBUCH §6.

### Create a new dashboard
1. `search_dashboards` → check if one already exists
2. Build the dashboard JSON (panels, datasource, folder)
3. `update_dashboard(dashboard=..., overwrite=false)`

### Add a panel to an existing dashboard
1. `get_dashboard(uid=...)` → load the JSON
2. Append a new panel object to the `panels[]` array
3. `update_dashboard(dashboard=..., overwrite=true)`

### Debug PromQL
1. `query_prometheus(expr="...", datasourceUid="...")` directly from Claude
2. Analyze result → adjust panel configuration

### Find the datasource UID
On first call: `search_dashboards` → read the `datasource.uid` from an existing dashboard.

### Metric doesn't exist yet → what to do?

If `query_prometheus(expr="my_metric")` returns no data:

1. **Check whether the metric is defined in the metrics module**
2. **If not:** do NOT build the panel. Instead:
   - Inform the operator: "Metric `my_metric` is missing in `lib/metrics.js`"
   - Describe what the metric should measure
   - Suggestion: `/ideation` for a new story or implement directly
3. **After metric implementation:** Prometheus scrapes it automatically → available in Grafana Cloud

---

## Full data flow (reference)

```
App Agents → lib/metrics.js → GET /metrics endpoint
    → Prometheus (scrape every 15s, Docker-internal)
        ├── Grafana local — dev/debug
        └── remote_write → Grafana Cloud — PROD/MOBILE
                                ↑
                       /grafana skill + MCP plugs in here
```

**Configuration:**
- Prometheus scrape + remote_write: `monitoring/prometheus/prometheus.yml`
- Metric definitions: `lib/metrics.js`
- Kill switch: comment out the `remote_write` block → cloud push stops immediately
