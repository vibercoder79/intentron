# Wave BB — Multi-User-VPS + Drei-Ebenen-Kollisionsschutz (BOO-151)

**Was jetzt da ist:** Die Doku für **mehrere Menschen an einem Projekt auf einer gemeinsamen VPS** ist geschärft und konsolidiert — plus ein explizites **Drei-Ebenen-Modell**, wie das Framework verhindert, dass sich parallele Arbeit überschreibt. Klare Trennung: Bootstrap-Setup ≠ Entwicklungs-Governance ≠ Git-Best-Practices. DE+EN + Sketch.

## Stories

- **BOO-151** — Multi-User-VPS-Doku-Schärfung, Teammitglied-Checkliste (Runbook), Drei-Ebenen-Kollisionsschutz-Modell, Anhang-P-§3-Begriffsfix, Bootstrap-A.7-Schärfung, `journal/daily`-`.gitignore`-Konvention.

## Die drei Ebenen (neu konsolidiert)

1. **Multi-USER** (mehrere Menschen, ein Projekt) → eigener Klon pro User-Home, Sync über GitHub.
2. **Multi-SESSION** (eine Person, 2 Sessions, ein Klon) → `git worktree` / Session-Hinweis.
3. **Multi-AGENT** (eine Session, mehrere Sub-Agenten) → `EXECUTION_ISOLATION` (existiert bereits, BOO-52).

## Änderungen (DE+EN)

- **Neu:** `docs/kollisionsschutz-drei-ebenen.md` (+ `.en.md`) — das Drei-Ebenen-Modell an einer Stelle.
- **Neu:** `docs/runbooks/multi-user-vps.md` (+ `.en.md`) — Teammitglied-Checkliste (einmal VPS / einmal GitHub / einmal Claude / pro Repo) + Sketch.
- **Neu:** Sketch `docs/assets/multi-user-vps.{excalidraw,png}` (+ `.en.*`) — Multi-User-Klon-Modell, OWLIST, Render-Loop, Read-verifiziert.
- **`HANDBUCH.md` Anhang P §3:** Schritt 7 — „Klon" vs. „git worktree" sauber getrennt + Verweise.
- **`bootstrap/SKILL.md`** (3.38.0 → **3.39.0**): A.7 — Solo-Lock-Hinweis (Ebene 2) + Multi-User-VPS-Runbook-Verweis + `journal/daily`-`.gitignore`-Hinweis.
- **`bootstrap/references/file-templates.md`:** `.gitignore`-Template — kommentierte `journal/daily/`-Zeile (Multi-User aktivierbar; Solo committet).

Alle Änderungen DE+EN-paritätisch.

## Abgrenzung

Multi-AGENT (Ebene 3) ist nicht Teil — schon gebaut (`EXECUTION_ISOLATION`, `implement`-Schritt-0c). Baut auf BOO-138/139/145 auf.

## Verweise

Spec: `specs/BOO-151.md`. Branch: `feat/boo-151-multi-user-vps`. Anknüpfung: HANDBUCH Anhang P §3 / U / Y, `docs/how-we-document.md`. Operator-Quelle: Tobias, 2026-06-04.
