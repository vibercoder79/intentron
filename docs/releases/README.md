# Release Notes — Konvention

Dieser Ordner ist die **Quelle der Release Notes**. Sie werden zusaetzlich als **GitHub Releases** veroeffentlicht:
<https://github.com/vibercoder79/code-crash-framework/releases>

## Zwei Ebenen

| Ebene | Datei | Zweck |
|-------|-------|-------|
| **Granular (pro Welle)** | `wave-<x>-<thema>.md` | Eine Datei pro Wave/Update — der einzelne Change mit Stories, Aenderungen, Migration, Smoke-Test. Im Repo, dauerhaft. |
| **Sammel (pro Version)** | `v<MAJOR.MINOR.PATCH>-overview.md` | Fasst alle Wellen einer Version zusammen (Big-Picture-Tabelle + Detail-Sektionen + Anhang-/Versions-Tabellen). Wird der **Body des GitHub Release**. |

## Konvention: GitHub Release pro Version

**Bei jedem Version-Tag** wird ein GitHub Release angelegt — Granularitaet ist **pro Version** (nicht pro Wave). Die einzelnen `wave-*.md` bleiben die granulare Quelle im Repo und sind im Release-Body verlinkt/zusammengefasst.

So wird ein Release angelegt (Beispiel v0.2.0):

```bash
# 1. Tag auf dem fertigen Stand (alle Wellen der Version done, Doku DE/EN paritaetisch)
git tag -a v0.2.0 -m "v0.2.0 — <Kurzbeschreibung>"
git push origin v0.2.0

# 2. GitHub Release mit dem Overview als Body
gh release create v0.2.0 \
  --title "v0.2.0 — <Titel>" \
  --notes-file docs/releases/v0.2.0-overview.md
```

Ein bestehendes Release nachtraeglich aktualisieren: `gh release edit v0.2.0 --notes-file docs/releases/v0.2.0-overview.md`.

## Regeln

1. **Jede Wave bekommt eine `wave-*.md`** im selben Stil (Zweck, Stories, Aenderungen, Migration, Verweise) — das ist Teil des Doku-Touchpoint-Quartetts (HANDBUCH, Release Notes, Spec, Linear).
2. **Die `v<version>-overview.md` wird pro Wave mitgepflegt** (Tabellenzeile + ggf. Detail-Sektion), damit sie beim Version-Release komplett ist.
3. **Vor dem Tag**: Doku DE/EN paritaetisch, alle Linear-Issues der Version Done, `verify-setup.sh` gruen.
4. **Tag = Stand**: erst taggen, wenn der Release-Stand wirklich fertig ist (kein Tag auf halbem EN-Stand).
5. **Release-Body = overview**: kein separates Copy-Paste pflegen — `--notes-file` zeigt direkt auf die `v<version>-overview.md`.

## Vorgaenger

- `v0.1.0` — GAP-Hardening (Wellen A–I), getaggt 2026-05-22.
- `v0.2.0` — Governance-OS (Wellen J–T): Privacy, Deployment, Souveraenitaet, Multi-Operator, Verifikation, Multi-Projekt, Vault-Harvest, Codex-Onboarding.
