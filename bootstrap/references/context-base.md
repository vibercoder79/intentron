# CONTEXT.md — Ubiquitous Language (Framework-Basis · BOO-91)

Kanonisches Vokabular plus Verbotsliste fuer dieses Projekt. Die KI liest `CONTEXT.md`
beim Schreiben und nutzt **konsequent die kanonischen Begriffe** — kein wildes Synonym-
Erfinden (`User` vs. `Customer` vs. `Betroffener`). Jeder Begriff traegt seine **Quelle**
(Audit-Beleg).

**Default = Guidance, kein Hard-Gate.** Die KI wird gefuehrt, nicht blockiert. (Das
optionale Enforcement — Pruefung verbotener Begriffe via dpo-Katalog (BOO-87) bzw.
Layer-0-Bodyguard (BOO-86) — ist eine spaetere, opt-in Ausbaustufe.)

Diese Datei ist die **vorgefuellte Framework-Basis**. Beim `/bootstrap` wird sie in das
Projekt-`CONTEXT.md` geseedet; **projekteigene** Begriffe traegt der Operator in die
Sektion „Projekt-Domaene" ein. Das Projekt-Overlay ueberlebt Framework-Updates.

## Compliance-Vokabular

| kanonisch | verboten | quelle |
| --- | --- | --- |
| `Betroffener` | `User` / `Customer` / `Client` (im PII-Kontext) | DSGVO Art. 4 (betroffene Person) |
| `Bearbeitung` | `Verarbeitung` | nDSG (Schweiz nutzt bewusst „Bearbeitung") |
| `Auftragsverarbeiter` | `Vendor` / `Dienstleister` | DSGVO Art. 28 |
| `Einwilligung` | `Zustimmung` / `OK` | DSGVO Art. 6 / Art. 7 |
| `personenbezogene Daten` | `PII` als Code-Begriff ohne Definition | DSGVO Art. 4 |

## Governance-Vokabular

| kanonisch | verboten | quelle |
| --- | --- | --- |
| `Story` | `Ticket` | INTENTRON-Governance |
| `Spec` | `Anforderung` (lose) | INTENTRON-Governance |
| `Intent` | `Ziel` (vage) | INTENTRON-Governance |
| `Gate` | `Check` (generisch) | INTENTRON Quality-Gate |
| `Layer 0` / `Layer 2` / `Layer 3` | gemischte/uneinheitliche Layer-Benennung | INTENTRON Quality-Gate-Architektur |
| `BOO-<n>` | freie Issue-Bezeichnung | Linear-Issue-Prefix |

<!-- SEED-ENDE — die folgende Sektion wird beim Bootstrap leer in das Projekt-CONTEXT.md uebernommen -->
