# Orchestration-Checklist — Sprint-Pre-Flight + Loop-Checks

Referenz zu `/sprint-run` Schritt 1 (Sprint-Pre-Flight, HARD GATE) und Schritt 4 (Daemon-Loop).
Der Sprint darf erst starten, wenn **alle** Pre-Flight-Punkte gruen sind.

## Sprint-Pre-Flight (Schritt 1) ⛔

| Check | Pass-Kriterium | Bei Verstoss |
|---|---|---|
| Backlog priorisiert | `/backlog` liefert geordnete Kandidaten (`Todo`/`Backlog`, Reihenfolge) | STOPP — erst `/backlog` fahren |
| Spec pro Story | `specs/<ISSUE>.md` existiert (Spec-Gate) | Story aus Sprint nehmen / STOPP |
| Schrader-vollstaendig | Insight, Constraints, Erfolgskriterien, Gewuenschtes Ergebnis je ≥20 Zeichen | Story aus Sprint nehmen |
| Execution-Isolation-Block | Spec traegt `execution_mode`, `worktree_strategy`, `write_scopes` | Story aus Sprint nehmen |
| Governance-Gates | `governance_mode` aus CONVENTIONS; sensitive-paths/personal-data konfiguriert | Pause-Verhalten klaeren |
| Werkzeug | `git worktree` da, `gh` authentifiziert, `main` clean | STOPP |

> Der Pre-Flight ist die Bedingung dafuer, dass der Loop danach ohne Rueckfragen laeuft.
> Im Daemon-Modus (`--auto`) werden Stories, die einen Pre-Flight-Punkt verletzen,
> **uebersprungen und protokolliert** — sie blockieren nicht den ganzen Sprint.

## Loop-Checks pro Story (Schritt 4)

Vor `/implement` (4.1–4.3):
- [ ] Linear-Status auf `In Progress` gesetzt
- [ ] Worktree angelegt: `git worktree add ../wt-<ISSUE> -b feat/boo-<n>-<slug>`
- [ ] Arbeitsbaum im Worktree clean

Nach `/implement` (4.5–4.7):
- [ ] Remote-CI gruen (`gh run watch --exit-status`) — sonst max 3 Fix-Iterationen
- [ ] Merge **nur** bei gruener CI
- [ ] Worktree entfernt: `git worktree remove ../wt-<ISSUE>`
- [ ] Linear-Status `Done` mit AC-Evidenz-Kommentar

Pro Iteration:
- [ ] Token-Verbrauch gegen 80%-Boundary geprueft (Schritt 4.8)

## Anti-Pattern

- **Story ohne Spec in den Sprint nehmen** — Spec-Gate haelt `/implement` ohnehin an, kostet
  aber einen halben Loop. Im Pre-Flight abfangen.
- **Mehrere Stories im selben Worktree** — Kollisionsgefahr; je Story ein Worktree (Ebene 2,
  siehe `docs/kollisionsschutz-drei-ebenen.md`).
- **Merge bei roter CI** — verboten (BOO-148). Kein Merge ohne gruenen Remote-Lauf.
