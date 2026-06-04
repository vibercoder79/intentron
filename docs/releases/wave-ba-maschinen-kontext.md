# Wave BA — Maschinen-Kontext beim Bootstrap (BOO-145)

**Was jetzt da ist:** Der Bootstrap schreibt am Ende von **Block A** automatisch einen `## Maschinen-Kontext`-Abschnitt in die globale `~/.claude/CLAUDE.md` — **idempotent** und **ohne separaten Operator-Schritt**. Jede KI-Session auf der Maschine hat damit sofort Orientierung: OS-Typ, Framework-Version, bevorzugter Stack und verfuegbare Skills. Zweiter Maschinen-Ebene-Baustein neben `PROJECTS_ROOT` (BOO-138). DE+EN.

## Stories

- **BOO-145** — Block A schreibt `## Maschinen-Kontext` (Typ via `uname -s`, Framework `intentron <VERSION>`, Stack-Praeferenz aus A.1, Skills via `ls ~/.claude/skills/`), idempotent.

## Änderungen (DE+EN)

- **`bootstrap/SKILL.md`** (3.36.0 → **3.37.0**): neuer Schritt **A.8 Maschinen-Kontext** vor dem Phase-1-Checkpoint — idempotenter Schreibvorgang in `~/.claude/CLAUDE.md`, OS/Version/Stack/Skills-Ermittlung, Abschnitts-Template.
- **`bootstrap/references/global-registry-update.md`**: neue Sektion „3b. Maschinen-Kontext" — Lese-/Schreib-Regel, Idempotenz, kein Secret, Beispiel.

Alle Änderungen DE+EN-paritätisch.

## Abgrenzung

Reine Bootstrap-Ergänzung (Block A) + Doku, kein Sketch. Baut auf BOO-138 (`PROJECTS_ROOT`, `v0.8.0`) auf.

## Verweise

Spec: `specs/BOO-145.md`. Branch: `feat/boo-145-maschinen-kontext`. Anknüpfung: BOO-138 (`PROJECTS_ROOT`), `global-registry-update.md`. Operator-Quelle: Tobias, 2026-06-04.
