# Wave BX — PR- & Merge-Hygiene: Guard gegen doppelte PRs (BOO-175)

> 🌐 **Sprache:** Deutsch (diese Datei) · [🇬🇧 English](wave-bx-pr-merge-hygiene.en.md)

**Was jetzt da ist:** Eine Konvention, die den Doppel-Merge von BOO-172 künftig verhindert. Beim Release-Audit (BOO-173) war aufgefallen, dass **BOO-172 über zwei PRs nach `main` gemergt** wurde. Diese Story klärt die Ursache und etabliert zwei Guards.

## Analyse (read-only)

- **#69** (2026-06-07 08:32, Titel *„docs: Runbook … (BOO-172)"* — saubere BOO-Nummer) und **#70** (09:32, generischer Titel *„Feat/boo 172 runbook tmux vps"*) kamen vom **selben** Branch `feat/boo-172-runbook-tmux-vps`.
- **Root-Cause:** Nach dem Merge von #69 wurden weitere Commits (u.a. `sprint-run/README.md`/`.en`) auf **denselben** Branch gepusht und als zweiter PR #70 gemergt. #70 war ein Superset von #69.
- **`main` ist vollständig** — beide PRs sind gemergt, kein Inhalt verloren (verifiziert: die nur in #70 enthaltenen `sprint-run/README`-Änderungen liegen auf `main`). Das Problem war reine PR-Hygiene, kein inhaltlicher Defekt. **Kein** History-Rewrite.

## Änderungen

- **Konvention „PR- & Merge-Hygiene" in `CONVENTIONS.md` §3** (EN- + DE-Block): *Ein Issue → ein PR → ein Merge.* Zwei Guards:
  1. **Vor `gh pr create` auf bestehenden PR prüfen** (`gh pr list --head <branch> --state all`) — kein zweiter PR pro Branch; bei bereits gemergtem PR frisch von `main` branchen.
  2. **PR-Titel muss die Issue-Nummer (`BOO-NNN`) enthalten** — generische Branch-Titel können beim Merge das falsche/kein Linear-Issue verknüpfen (Linear-first, BOO-154).
  Plus Hinweis: Feature-Branch nach Merge löschen.
- **Branch-Cleanup:** der verwaiste, voll gemergte Branch `feat/boo-172-runbook-tmux-vps` auf dem Remote gelöscht.

## Abgrenzung

- **Read-only-Analyse zuerst, kein Revert, kein History-Rewrite** auf `main` — beide Inhalte sind korrekt vorhanden.
- Reine Doku/Konvention + Branch-Cleanup. Ein erzwingender Wrapper-Skript (`gh pr create`-Guard) bleibt optionale Folge-Idee — die Konvention ist Operator-Disziplin.
- Wave-Buchstabe **bx** (bw = Doku-DoD BOO-180).

## Verweise

Spec: `specs/BOO-175.md`. Branch: `tobiaschschmidt/boo-175-chore-doppel-merge-guard`. Verwandt: BOO-172 (Doppel-Merge), BOO-173 (Release-Audit, fand es), BOO-154 (Linear-first), BOO-180 (Doku-DoD — diese Story folgt ihr). Operator-Quelle: Tobias, 2026-06-07.
