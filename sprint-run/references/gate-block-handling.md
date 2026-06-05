# Gate-Block-Handling — Pause/Resume-Protokoll

Referenz zu `/sprint-run` Schritt 4.4. Sicherheitskritisch: Der Daemon darf Governance-Gates
**niemals** automatisch ueberbruecken.

## Welche Gates pausieren den Daemon?

| Gate | Quelle (`/implement`) | Ausloeser | Freigabe-Token |
|---|---|---|---|
| Sensitive-Paths | Schritt 5.5 (BOO-18) | geaenderte Datei matcht `.claude/sensitive-paths.json` | `review-ok: <name> - <kommentar>` |
| Personal-Data | Schritt 5.5b (BOO-69) | `personal_data: true` + Match in `.claude/personal-data-paths.json` | `privacy-ok: <name> - <kommentar>` (DSGVO Art. 25) |

Beide koennen gleichzeitig zuschlagen — dann erst `review-ok` (technisch), dann `privacy-ok`
(rechtlich). Keine Bestaetigung ersetzt die andere.

## Protokoll

1. **Pause.** `/implement` stoppt an seinem Gate. `/sprint-run` faehrt **nicht** fort —
   kein Merge, kein Worktree-Cleanup, keine naechste Story.
2. **Notify.** Operator-Hinweis mit **Story-ID**, **Gate-Typ** und **konkretem Pfad/Grund**.
   Im Daemon-Modus: persistente Notiz (z.B. Linear-Kommentar) statt nur Konsolen-Ausgabe.
3. **Warten.** Der Daemon bleibt blockiert, bis der Operator das passende Freigabe-Token
   liefert. **Kein** Timeout-Resume.
4. **Resume.** Nach Freigabe traegt `/implement` den Block ins Spec-File (`## Human Review`
   bzw. `## Privacy Review`) und faehrt fort; `/sprint-run` nimmt den Loop wieder auf.
5. **Abbruch (optional).** Will der Operator nicht freigeben: Story zurueck auf `Backlog`,
   Worktree entfernen, naechste Story nach `daemon_fail_policy`.

## Verbote

- ❌ Kein automatischer Bypass eines Gates — auch nicht im `--auto`-Modus.
- ❌ Kein Timeout-basiertes Auto-Resume.
- ❌ Keine Freigabe „im Voraus" fuer kommende Stories — jede Freigabe gilt fuer genau einen Block.

## Zustandsmaschine

```
laufend ──(Gate-Treffer)──▶ pausiert ──(review-ok / privacy-ok)──▶ resumed ──▶ laufend
                              │
                              └──(Operator lehnt ab)──▶ abgebrochen (Story → Backlog)
```

Sketch: `docs/gate-block-handling.png` (HANDBUCH Anhang AD).
