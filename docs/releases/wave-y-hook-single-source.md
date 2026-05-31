# Wave Y — coverage-check.sh Single-Source + Drift-Guard (BOO-89)

**Linear:** [BOO-89](https://linear.app/owlist/issue/BOO-89/) · Folge-Story aus BOO-88

## Problem

`coverage-check.sh` wurde **dreifach** gepflegt: als Inline-Body im `file-templates.md` (DE),
im `file-templates.en.md` (EN) und als eingebetteter Heredoc in `migrate-to-v2.sh`
(`migrate_boo_15`). Der BOO-88-Bugfix brauchte deshalb drei synchrone Edits — Drift ist nur
eine Frage der Zeit. Gilt potenziell fuer alle gescaffoldeten Hooks.

## Was sich aendert

- **Kanonische Quelle:** `bootstrap/references/hooks/coverage-check.sh` (v2, inkl. BOO-88-Fix) —
  **eine** Datei statt drei Kopien.
- **Migration kopiert statt einzubetten:** `migrate_boo_15` macht `cp` aus der kanonischen
  Datei (kein `COVCHECK_EOF`-Heredoc mehr). v1→v2-Replace mit `.bak` bleibt unveraendert.
- **Templates zeigen auf die Quelle:** `file-templates.md` + `.en.md` enthalten statt des
  Inline-Skripts einen Pointer auf `references/hooks/coverage-check.sh` (Bootstrap rendert
  verbatim daraus).
- **Drift-Guard:** `bootstrap/scripts/check-hook-sources.sh` prueft die Single-Source-Konvention
  (kanonisch valide; nicht zusaetzlich eingebettet; frisch migriert == kanonisch) und listet
  die noch eingebetteten Hooks als Folge-Kandidaten. Laeuft lokal **und in CI**
  (`.github/workflows/hook-sources.yml`).

## Verifiziert

- Fresh-Install + v1-Replace + Idempotenz: installierte `coverage-check.sh` ist byte-identisch
  zur kanonischen Quelle.
- Drift-Guard exit 0 auf aktuellem Stand; `bash -n` auf allen betroffenen Skripten.

## Designentscheid

„Beides" (Operator-Wahl): echtes Single-Source **plus** Drift-Guard als Sicherheitsnetz.
Erst-Migration auf `coverage-check.sh` (die Story, die uns gebissen hat); die uebrigen
gescaffoldeten Hooks (spec-gate, dependency-check, pre-edit-bodyguard, …) sind als
Folge-Kandidaten gelistet und werden inkrementell nachgezogen.

## Hinweis

`coverage-check.sh` benoetigt weiterhin bash 4+ (`declare -A`, vorbestehend seit BOO-15).
bootstrap 3.33.0 → 3.34.0.
