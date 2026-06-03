# ADR: Design-Story-Handling — implement gegen Referenz, kein change_type:design (BOO-126)

- **Status:** akzeptiert (2026-06-03)
- **Typ:** Discovery-/Decision-Story (bewusst strukturiert entschieden, nicht Sofort-Impl)
- **Kontext-Quelle:** Probelauf-Folgefrage (BKO, 2026-06-02)

## Kontext
Wie behandelt das Framework design-lastige Stories? Zur Entscheidung stand: reicht „Design-Story =
implement gegen eine Design-Referenz" (Default-These des Operators), oder braucht es einen eigenen
`change_type: design`, ein Template und/oder eine Auto-Erkennung in `/ideation`?

Befund (v0.7.9): Es gibt **keinen** design-spezifischen Story-Typ; `change_type`-Typen (non-code/prototype)
waren bisher nur Vorschläge, nicht implementiert. `ARCHITECTURE_DESIGN.md` kann via §9-Auto-Linking auf
eine Design-Datei verweisen — die Mechanik „Code gegen Design-Referenz" existiert also bereits.

## Entscheidung
**Default ratifiziert:** Eine Design-Story = **„implement gegen eine Design-Referenz"** über die normale
Pipeline (`/ideation` → `/implement`). **Kein** `change_type: design`, **kein** neues Template, **keine**
Auto-Erkennung in `/ideation`. Die Design-Referenz (z.B. `DESIGN.md`, Figma-Export, Screenshot) wird in
`ARCHITECTURE_DESIGN.md §9` verlinkt; `/implement` verifiziert gegen die Referenz **plus** a11y- und
Lighthouse-Gates (BOO-45).

## Begründung (Verifizierbarkeit, Karpathy)
- **Code-Output hat Ground Truth** (Tests, Lighthouse-Budget, a11y-Checks) → automatisch verifizierbar →
  framework-tauglich. Eine Design-*Umsetzung* lässt sich so gegen messbare Gates prüfen.
- **Design-Geschmack hat keinen Auto-Check** → kein Gate möglich → gehört **nicht** in die Pflicht-Pipeline.
- Ein eigener `change_type: design` + Template + Auto-Erkennung wäre Maschinerie für einen Einzelfall ohne
  Ground Truth — Verstoß gegen das Leichtgewicht-Prinzip.

## Abgrenzung (was wohin gehört)
- **Coding-Framework (Pflicht-Pipeline):** *setzt Design um* — implementiert gegen eine Referenz, mit
  messbaren Gates (a11y, Lighthouse, Tests).
- **Reine Gestaltung (Geschmack, Brand, Visual Identity):** **opt-in externe Skills** — `design-md-generator`,
  die `lumen-*`-Brand-Skills, Pencil-/Webflow-MCP. **Keine** Pflicht-Pipeline, kein Gate.

## Konsequenzen
- Keine Code-/Skill-Änderung nötig — `/ideation` und `change_type` bleiben unverändert.
- Falls später doch ein `change_type: design` gewünscht wird (mit Akzeptanzkriterien Referenz-Match +
  a11y/Performance), ist das ein **neuer ADR**, der diesen ablöst.
- Doku-Abgrenzung im HANDBUCH §6 (DE+EN) verankert.
