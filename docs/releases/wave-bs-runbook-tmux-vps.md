# Wave BS — Runbook: Sprint unbeaufsichtigt auf der VPS per tmux (BOO-172)

**Was jetzt da ist:** Ein neues Runbook erklärt, wie man `/sprint-run` (oder jede langlaufende Claude-Arbeit) auf der VPS in **`tmux`** startet, sodass sie das **Zuklappen des Laptops / einen SSH-Abbruch überlebt**. Bewusst **statt** eines vollausführbaren VPS-Daemons (zu großer Umbau für den Nutzen) — Bordmittel reichen.

## Stories
- **BOO-172** — Runbook „Sprint unbeaufsichtigt per tmux" (DE+EN + Sketch).

## Änderungen
- **Neu `docs/runbooks/sprint-unattended-tmux.md` (+ `.en.md`):** Problem (Sitzung hängt an SSH → Laptop zu = Agent tot) → Lösung (tmux) → 5 Schritte → Cheatsheet → „wann nötig" → bewusste Grenze (kein Daemon).
- **Neu Sketch `sprint-unattended-tmux.{excalidraw,png}` (+ `.en.*`):** „ohne tmux (stirbt) vs. mit tmux (läuft weiter)", im Render-Loop erstellt + eingebettet.
- **Verlinkt:** aus `docs/runbooks/sprint-run.{md,en.md}` (Verweise) + `docs/onboarding/artefakt-landkarte.{md,en.md}` (Runbook-Liste).

## Scope-Entscheidungen
- **Nur die einfache tmux-Empfehlung** — die SSH-Host-Alias-/Auto-tmux-Konfiguration wurde bewusst weggelassen (zu fummelig, bricht VS Code Remote-SSH).
- Mac-Terminal **oder** VS-Code-Terminal gleichwertig; gilt für jede langlaufende Remote-Arbeit, nicht nur Sprints.

## Wirkung
Klare, verlinkte Anleitung für „starte den Sprint, klapp den Mac zu, er läuft weiter" — ohne Daemon, ohne Konfig-Fummelei.

## Abgrenzung
Reine Doku. Der vollausführbare VPS-Daemon (Variante B, cron/systemd: zeitgesteuerter Auto-Start, Selbstheilung, Reboot-Persistenz) bleibt **bewusst ungebaut** — nur bei echtem Bedarf. Wave-Buchstabe **bs** (br = implement-Haiku-Loops BOO-171).

## Verweise
Spec: `specs/BOO-172.md`. Branch: `feat/boo-172-runbook-tmux-vps`. Verwandt: BOO-170/171 (Modell-Routing-Kette), BOO-157 (sprint-run), `hostinger-vps-setup`/`multi-user-vps` (VPS-Grundlagen). Operator-Quelle: Tobias, 2026-06-07.
