# Worktree-Flow — ein Worktree pro Story

Referenz zu `/sprint-run` Schritt 4.2 / 4.6. Jede Story laeuft in ihrem eigenen `git worktree`
mit eigenem Branch — so isoliert der Sprint die Stories voneinander (Kollisionsschutz Ebene 2,
`docs/kollisionsschutz-drei-ebenen.md`).

## Warum Worktree statt Branch-Wechsel?

- **Isolation:** Jede Story hat einen eigenen Arbeitsbaum — kein `git checkout`-Hin-und-Her,
  kein versehentliches Mischen von Aenderungen.
- **Parallel-faehig:** Bei `parallel_story_limit > 1` koennen mehrere Stories gleichzeitig in
  disjunkten Worktrees laufen (disjunkte `write_scopes` vorausgesetzt).
- **Sauberes `main`:** Der Haupt-Arbeitsbaum bleibt unangetastet, bis gemerged wird.

## Ablauf pro Story

```bash
# 4.2 — anlegen (eigener Branch je Story)
git worktree add ../wt-BOO-<n> -b feat/boo-<n>-<slug>

# 4.3–4.5 — im Worktree: /implement (Daemon) + Remote-CI-Wait
cd ../wt-BOO-<n>
# ... /implement laeuft hier, pusht den Branch, wartet auf gruene CI ...

# 4.6 — Merge NUR bei gruener CI, dann aufraeumen
cd <repo-root>
git merge --no-ff feat/boo-<n>-<slug>      # oder PR-Merge via gh
git worktree remove ../wt-BOO-<n>
git branch -d feat/boo-<n>-<slug>          # nach erfolgreichem Merge
```

## Regeln

- **Branch-Naming:** `feat/boo-<n>-<slug>` (bzw. die von Linear vorgeschlagene `gitBranchName`).
- **Merge-Gate:** kein Merge ohne gruene Remote-CI (BOO-148).
- **Cleanup ist Pflicht:** nach Merge `git worktree remove` + Branch loeschen. Verwaiste
  Worktrees blockieren spaetere Laeufe.
- **Bei Fehler:** Worktree nach `daemon_fail_policy` entfernen (oder fuer Diagnose behalten und
  im Sprint-Report vermerken).
- **Dirty `main`:** niemals mergen, wenn der Haupt-Baum nicht clean ist — STOPP.

## Drei Ebenen des Kollisionsschutzes (Einordnung)

- **Ebene 1 — Multi-User:** eigener Klon pro Person.
- **Ebene 2 — Multi-Session:** `git worktree` pro Session/Story ← *hier wirkt `/sprint-run`*.
- **Ebene 3 — Multi-Agent:** Execution-Isolation + disjunkte Write-Scopes (`/implement` Schritt 0c).

Sketch: `docs/story-breakdown.png` + `docs/github-integration.png` (HANDBUCH Anhang AD).
