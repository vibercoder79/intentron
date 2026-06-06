#!/usr/bin/env python3
"""resolve-model.py — BOO-170

Loest fuer einen Skill das Claude-Code `--model`-Flag deterministisch auf.

Kette (nutzt bestehende SSoT, kein neuer Doppel-Owner):
  1. <repo>/<skill>/SKILL.md  Frontmatter `recommended_model:`  -> Tier (haiku|sonnet|opus)
  2. bootstrap/references/model-tiers.json  tiers[tier].current_version  -> Modell-Version

Genutzt vom /sprint-run-Daemon (Schritt 4.3), um /implement pro Story mit dem
empfohlenen Modell als Subprozess zu starten:

    claude -p "/implement <ISSUE>" \\
      --model "$(python3 sprint-run/scripts/resolve-model.py implement)" \\
      --permission-mode dontAsk

Dependency-frei (kein PyYAML — Frontmatter wird zeilenweise geparst), analog
dpo-audit.py / docs_drift_check.py. Faellt im Zweifel auf das 'sonnet'-Tier
zurueck (sicherer Default laut model-tiers.json) und meldet nach stderr.

Operator-Override: Dieses Skript liefert nur den Skill-Default. Die Override-
Hierarchie (`--model`-CLI > CLAUDE.md model_overrides > Skill-Default) bleibt
gewahrt — wer dem Daemon ein explizites Modell vorgibt, ueberschreibt diesen Wert.

Usage:
  resolve-model.py <skill-name> [--tier] [--repo-root PATH]
    --tier        gibt das Tier (haiku|sonnet|opus) statt der Version aus
    --repo-root   Repo-Wurzel explizit setzen (sonst Auto-Discovery)
"""
import json
import os
import re
import sys

DEFAULT_TIER = "sonnet"
TIERS_REL = os.path.join("bootstrap", "references", "model-tiers.json")


def find_repo_root(start):
    d = os.path.abspath(start)
    while True:
        if os.path.exists(os.path.join(d, TIERS_REL)):
            return d
        parent = os.path.dirname(d)
        if parent == d:
            return None
        d = parent


def read_recommended_tier(skill_dir):
    """Liest `recommended_model:` aus dem YAML-Frontmatter der SKILL.md (zeilenweise)."""
    skill_md = os.path.join(skill_dir, "SKILL.md")
    if not os.path.isfile(skill_md):
        return None
    in_frontmatter = False
    with open(skill_md, encoding="utf-8") as fh:
        for idx, raw in enumerate(fh):
            line = raw.rstrip("\n")
            if idx == 0 and line.strip() == "---":
                in_frontmatter = True
                continue
            if in_frontmatter and line.strip() == "---":
                break
            if in_frontmatter:
                m = re.match(r"\s*recommended_model:\s*([A-Za-z0-9_.-]+)", line)
                if m:
                    return m.group(1)
    return None


def main(argv):
    args = list(argv)
    want_tier = "--tier" in args
    args = [a for a in args if a != "--tier"]

    repo_root = None
    if "--repo-root" in args:
        i = args.index("--repo-root")
        if i + 1 >= len(args):
            sys.stderr.write("resolve-model: --repo-root erwartet einen Pfad\n")
            return 2
        repo_root = args[i + 1]
        del args[i:i + 2]

    if not args:
        sys.stderr.write(
            "usage: resolve-model.py <skill-name> [--tier] [--repo-root PATH]\n")
        return 2
    skill = args[0]

    root = (repo_root
            or find_repo_root(os.getcwd())
            or find_repo_root(os.path.dirname(os.path.abspath(__file__))))
    if not root:
        sys.stderr.write(
            "resolve-model: model-tiers.json nicht gefunden -> Fallback-Tier '%s'\n"
            % DEFAULT_TIER)
        print(DEFAULT_TIER)
        return 0

    tier = read_recommended_tier(os.path.join(root, skill))
    if not tier:
        sys.stderr.write(
            "resolve-model: kein recommended_model fuer '%s' -> Fallback '%s'\n"
            % (skill, DEFAULT_TIER))
        tier = DEFAULT_TIER

    with open(os.path.join(root, TIERS_REL), encoding="utf-8") as fh:
        tiers = json.load(fh).get("tiers", {})

    if tier not in tiers:
        sys.stderr.write(
            "resolve-model: Tier '%s' nicht in model-tiers.json -> Fallback '%s'\n"
            % (tier, DEFAULT_TIER))
        tier = DEFAULT_TIER if DEFAULT_TIER in tiers else tier

    if want_tier:
        print(tier)
        return 0

    version = tiers.get(tier, {}).get("current_version")
    if not version:
        sys.stderr.write(
            "resolve-model: keine current_version fuer Tier '%s' -> gebe Tier-Alias aus\n"
            % tier)
        print(tier)
        return 0
    print(version)
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
