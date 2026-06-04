#!/usr/bin/env python3
"""docs-drift-check — repo-internes Doku-Drift-Gate fuer das intentron-Repo.

NICHT Teil des ausgelieferten Frameworks: liegt bewusst unter `.github/`, wird
nicht gebootstrappt und steht in keinem HANDBUCH-Anhang. Es huetet die
Doku-Hygiene DIESES Repos und failt, wenn die Doku vom realen Stand driftet —
analog zu den bestehenden repo-internen CI-Gates (hook-sources, ruff-hooks).

Checks (alle deterministisch, nur python3-Stdlib):
  1) Tote `references/*.md`-Links in SKILL*.md / README*.md
  2) Versions-Gleichstand SKILL.md (`version:`) <-> README.md (`**Version:**`)
  3) DE/EN-Paritaet: zu SKILL.md/README.md existiert .en.md; v*-overview.md hat EN-Spiegel
  4) Skills-Tabelle: jeder Skill-Ordner (mit SKILL.md) ist in README.md verlinkt
  5) Wave-Dopplungen: kein neuer Release-Wave-Buchstabe doppelt belegt
     (BOO-153 Cross-Session-Drift-Guard; Alt-Dopplungen ba/bb/bc als Allowlist)
"""
from __future__ import annotations

import glob
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
errors: list[str] = []


def rel(p: str) -> str:
    return os.path.relpath(p, ROOT)


def read(p: str) -> str:
    with open(p, encoding="utf-8") as fh:
        return fh.read()


skill_dirs = sorted(
    d for d in os.listdir(ROOT)
    if os.path.isfile(os.path.join(ROOT, d, "SKILL.md"))
)

# --- 1) Tote references/-Links ---
link_re = re.compile(r"\]\((references/[^)]+\.md)\)")
for d in skill_dirs:
    for fname in ("SKILL.md", "SKILL.en.md", "README.md", "README.en.md"):
        p = os.path.join(ROOT, d, fname)
        if not os.path.isfile(p):
            continue
        for m in link_re.finditer(read(p)):
            if not os.path.isfile(os.path.join(ROOT, d, m.group(1))):
                errors.append(f"[dead-ref] {rel(p)} -> {m.group(1)} (Zieldatei fehlt)")

# --- 2) Versions-Gleichstand SKILL <-> README ---
ver_fm = re.compile(r"^version:\s*v?([0-9]+\.[0-9]+\.[0-9]+)", re.M)
ver_rd = re.compile(r"\*\*Version:\*\*\s*v?([0-9]+\.[0-9]+\.[0-9]+)")
for d in skill_dirs:
    sp, rp = os.path.join(ROOT, d, "SKILL.md"), os.path.join(ROOT, d, "README.md")
    if not os.path.isfile(rp):
        continue
    sv, rv = ver_fm.search(read(sp)), ver_rd.search(read(rp))
    if sv and rv and sv.group(1) != rv.group(1):
        errors.append(f"[version-drift] {d}: SKILL.md {sv.group(1)} != README.md {rv.group(1)}")

# --- 3) DE/EN-Paritaet ---
for d in skill_dirs:
    for base in ("SKILL.md", "README.md"):
        p = os.path.join(ROOT, d, base)
        en = os.path.join(ROOT, d, base[:-3] + ".en.md")
        if os.path.isfile(p) and not os.path.isfile(en):
            # Ausnahme: bilinguale Single-File-README (EN+DE-Anker in einer Datei,
            # wie security-architect/README.md bzw. CONVENTIONS.md) — kein .en.md noetig.
            if base == "README.md" and re.search(
                r'name="english"|English Version|English\]\(#english\)', read(p), re.I
            ):
                continue
            errors.append(f"[de-en] {d}/{base} ohne {base[:-3]}.en.md")
for ov in sorted(glob.glob(os.path.join(ROOT, "docs/releases/v*-overview.md"))):
    if "English Version" not in read(ov):
        errors.append(f"[de-en] {rel(ov)} ohne EN-Spiegel ('# ... English Version')")

# --- 4) Skills-Tabelle vollstaendig ---
readme = read(os.path.join(ROOT, "README.md"))
for d in skill_dirs:
    if f"({d}/)" not in readme:
        errors.append(f"[skills-table] Skill '{d}' fehlt in README.md (kein Link ({d}/))")

# --- 5) Doppelte Release-Wave-Buchstaben (BOO-153 — Cross-Session-Drift-Guard) ---
# Vor dem Guard entstandene Alt-Dopplungen (im ADR cross-session-drift dokumentiert):
WAVE_DUP_ALLOW = {"ba", "bb", "bc"}
wave_re = re.compile(r"^wave-([a-z]+)-(.+)\.md$")
wave_map: dict[str, set[str]] = {}
for wf in glob.glob(os.path.join(ROOT, "docs/releases/wave-*.md")):
    name = os.path.basename(wf)
    if name.endswith(".en.md"):
        continue
    m = wave_re.match(name)
    if m:
        wave_map.setdefault(m.group(1), set()).add(m.group(2))
for letter, slugs in sorted(wave_map.items()):
    if len(slugs) > 1 and letter not in WAVE_DUP_ALLOW:
        errors.append(
            f"[wave-dup] Wave-Buchstabe '{letter}' doppelt belegt: {sorted(slugs)} "
            f"— vor Vergabe naechsten freien Buchstaben gegen docs/releases/ pruefen (ADR cross-session-drift)"
        )

print(f"docs-drift-check: {len(skill_dirs)} Skills geprueft, {len(errors)} Drift-Befund(e).")
for e in errors:
    print("FAIL " + e)
if not errors:
    print("OK — keine Doku-Drift.")
sys.exit(1 if errors else 0)
