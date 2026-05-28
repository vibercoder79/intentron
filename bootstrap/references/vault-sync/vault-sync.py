#!/usr/bin/env python3
"""vault-sync.py — Framework-native Vault-Harvest-Engine (BOO-77).

Einseitiger Sync: GitHub-Repo -> persoenlicher Obsidian-Vault. NIE zurueck.
Liest .vault-sync/tracked-paths.json (versionierter Team-Vertrag) und
.vault-sync/local.json (pro Mitarbeiter, gitignored). Spiegelt ausgewaehlte
docs/-Dateien in den persoenlichen Vault, ergaenzt vault_sync_*-Frontmatter.

Designprinzipien (HANDBUCH Anhang R Layer 3 / vault-sync-pattern.md):
- Einseitig: schreibt NUR in den Vault, NIE ins Repo.
- Pfad-Containment: jedes Vault-Ziel muss innerhalb von vault_path liegen.
- Idempotent, kein Netzwerk, keine Secrets, nur Python-Stdlib.
- Fehlt local.json oder enabled=false: still exit 0 (null Reibung).

Aufruf: python3 scripts/vault-sync.py [--dry-run]
Wird normal vom .git/hooks/post-merge-Wrapper nach jedem git pull getriggert.
"""

from __future__ import annotations

import datetime as _dt
import json
import os
import sys
from pathlib import Path

VAULT_SYNC_DIR = ".vault-sync"
CONTRACT_FILE = "tracked-paths.json"
LOCAL_FILE = "local.json"
NS = "vault_sync_"  # Frontmatter-Namespace


def _log(msg: str) -> None:
    print(f"[vault-sync] {msg}")


def _repo_root() -> Path:
    """Repo-Root = Verzeichnis, in dem .vault-sync/ liegt (vom CWD aufwaerts)."""
    cur = Path.cwd().resolve()
    for cand in [cur, *cur.parents]:
        if (cand / VAULT_SYNC_DIR / CONTRACT_FILE).exists():
            return cand
    return cur


def _load_json(path: Path) -> dict | None:
    try:
        with path.open(encoding="utf-8") as fh:
            return json.load(fh)
    except FileNotFoundError:
        return None
    except json.JSONDecodeError as exc:
        _log(f"WARN: {path} ist kein gueltiges JSON ({exc}). Uebersprungen.")
        return None


def _git_head(repo: Path) -> str:
    """Aktueller Commit-SHA ohne Subprozess-Pflicht — liest .git direkt."""
    head = repo / ".git" / "HEAD"
    try:
        ref = head.read_text(encoding="utf-8").strip()
    except OSError:
        return "unknown"
    if ref.startswith("ref:"):
        ref_path = repo / ".git" / ref.split(" ", 1)[1].strip()
        try:
            return ref_path.read_text(encoding="utf-8").strip()[:12]
        except OSError:
            return "unknown"
    return ref[:12]


def _split_frontmatter(text: str) -> tuple[list[str], str]:
    """Trennt YAML-Frontmatter (--- ... ---) vom Body. Sehr einfacher Parser
    (zeilenbasiert) — kein YAML-Dependency, reicht fuer flache Properties."""
    lines = text.splitlines()
    if lines and lines[0].strip() == "---":
        for i in range(1, len(lines)):
            if lines[i].strip() == "---":
                return lines[1:i], "\n".join(lines[i + 1:])
    return [], text


def _has_key(fm_lines: list[str], key: str) -> bool:
    return any(ln.lstrip().startswith(f"{key}:") for ln in fm_lines)


def _build_frontmatter(
    fm_lines: list[str], *, project: str, rel_path: str, commit: str,
    inject_type: str | None,
) -> str:
    """Ergaenzt vault_sync_*-Felder (idempotent: ueberschreibt eigene Keys) und
    optional 'type:' (nur wenn Quelle keinen hat). Quell-Properties bleiben."""
    now = _dt.datetime.now(_dt.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    managed = {
        f"{NS}project": project,
        f"{NS}path": rel_path,
        f"{NS}commit": commit,
        f"{NS}at": now,
    }
    kept = [ln for ln in fm_lines if not ln.lstrip().startswith(NS)]
    if inject_type and not _has_key(kept, "type"):
        kept.append(f"type: {inject_type}")
    out = ["---"]
    out.extend(kept)
    for key, val in managed.items():
        out.append(f"{key}: {val}")
    out.append("---")
    return "\n".join(out)


def _is_contained(target: Path, base: Path) -> bool:
    """True wenn target (nach realpath) innerhalb base liegt. Schutz gegen
    Pfad-Traversal und Symlink-Ausbruch aus dem Vault."""
    try:
        target_r = target.resolve()
        base_r = base.resolve()
    except OSError:
        return False
    return base_r == target_r or base_r in target_r.parents


def _map_target(rel_path: str, mappings: dict, slug: str, vault: Path) -> Path | None:
    """Mappt einen Repo-relativen Pfad auf einen Vault-Pfad ueber das laengste
    passende path_mappings-Praefix. {slug} wird ersetzt."""
    best_prefix = ""
    best_dest = None
    for prefix, dest in mappings.items():
        norm = prefix.rstrip("/")
        if (rel_path == norm or rel_path.startswith(norm + "/")) and len(norm) > len(best_prefix):
            best_prefix = norm
            best_dest = dest
    if best_dest is None:
        return None
    remainder = rel_path[len(best_prefix):].lstrip("/")
    dest_dir = best_dest.replace("{slug}", slug)
    return vault / dest_dir / remainder


def _iter_tracked(repo: Path, tracked: list[dict]):
    """Liefert (abs_path, rel_path, inject_type) fuer jede getrackte Quelldatei.
    Ueberspringt .notes.md-Sidecars (Annotationen, nie angefasst)."""
    for entry in tracked:
        glob = entry.get("glob")
        if not glob:
            continue
        inject_type = entry.get("type")
        for match in sorted(repo.glob(glob)):
            if not match.is_file():
                continue
            if match.name.endswith(".notes.md"):
                continue
            yield match, match.relative_to(repo).as_posix(), inject_type


def main(argv: list[str]) -> int:
    cli_dry_run = "--dry-run" in argv
    repo = _repo_root()
    sync_dir = repo / VAULT_SYNC_DIR

    contract = _load_json(sync_dir / CONTRACT_FILE)
    local = _load_json(sync_dir / LOCAL_FILE)

    # Null-Reibung: keine local.json oder deaktiviert -> still exit 0.
    if local is None:
        return 0
    if not local.get("enabled", False):
        _log("local.json vorhanden, aber enabled=false — Sync uebersprungen.")
        return 0
    if not contract or not contract.get("tracked_paths"):
        _log("Kein tracked-paths.json / keine tracked_paths — nichts zu tun.")
        return 0

    vault_raw = (local.get("vault_path") or "").strip()
    slug = (local.get("project_slug") or "").strip()
    mappings = local.get("path_mappings") or {}
    mode = "dry-run" if cli_dry_run else (local.get("mode") or "dry-run")

    if not vault_raw:
        _log("WARN: vault_path leer in local.json — abgebrochen.")
        return 1
    vault = Path(os.path.expanduser(vault_raw))
    if not vault.is_dir():
        _log(f"WARN: vault_path existiert nicht: {vault} — abgebrochen.")
        return 1

    commit = _git_head(repo)
    written = skipped = blocked = 0

    for abs_path, rel_path, inject_type in _iter_tracked(repo, contract["tracked_paths"]):
        target = _map_target(rel_path, mappings, slug, vault)
        if target is None:
            _log(f"SKIP {rel_path}: kein path_mapping passt.")
            skipped += 1
            continue
        # Sicherheits-Gate: Ziel MUSS innerhalb des Vaults liegen.
        if not _is_contained(target, vault):
            _log(f"BLOCK {rel_path}: Ziel {target} liegt ausserhalb des Vaults — uebersprungen.")
            blocked += 1
            continue

        src_text = abs_path.read_text(encoding="utf-8")
        fm_lines, body = _split_frontmatter(src_text)
        new_fm = _build_frontmatter(
            fm_lines, project=slug, rel_path=rel_path, commit=commit,
            inject_type=inject_type,
        )
        body = body.rstrip("\n")
        new_text = f"{new_fm}\n{body}\n" if body else f"{new_fm}\n"

        if mode == "dry-run":
            _log(f"[dry-run] wuerde schreiben: {target}")
            written += 1
            continue
        if mode == "ask":
            ans = input(f"[vault-sync] {rel_path} -> {target} schreiben? [y/N] ").strip().lower()
            if ans not in ("y", "yes", "j", "ja"):
                skipped += 1
                continue
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(new_text, encoding="utf-8")
        written += 1

    # last_sync_commit aktualisieren (nur bei echtem Schreiben, idempotent)
    if mode not in ("dry-run",) and written:
        local["last_sync_commit"] = commit
        (sync_dir / LOCAL_FILE).write_text(
            json.dumps(local, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
        )

    _log(
        f"Fertig (mode={mode}, commit={commit}): {written} geschrieben/geplant, "
        f"{skipped} uebersprungen, {blocked} blockiert."
    )
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
