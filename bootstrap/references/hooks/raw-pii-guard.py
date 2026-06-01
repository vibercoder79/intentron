#!/usr/bin/env python3
"""raw-pii-guard — optionaler PII-in-Logs-Guard (BOO-93).

DE: Statischer AST-Check. Meldet, wenn Quellcode ein PII-tragendes Feld in eine
    Log-/Audit-Senke (`log.*()`, `logger.*()`, `audit.*()`, `logging.*()`) gibt —
    als verbotenes Keyword-Argument, Attribut-Lesezugriff oder Variablen-Name
    (`original_value`, `plaintext`, `raw_value` …). AST statt Regex: ignoriert
    Kommentare/Strings und versteht die Aufruf-Struktur (kaum Fehlalarme).
EN: Static AST check. Flags source that passes a PII-bearing field into a log/audit
    sink as a forbidden keyword arg, attribute read, or variable name. AST (not regex)
    ignores comments/strings and understands call structure (few false positives).

Default = Warnung (Exit 0). Mit `--strict` wird ein Treffer zum Fehler (Exit 1) —
konsistent mit dem Layer-0-Bodyguard (BOO-86), der ebenfalls warn-default ist.
Dependency-frei: nur python3-Stdlib (`ast`). Kein Code aus Fremd-Repos uebernommen.

Usage:
    raw-pii-guard.py [--strict] [--config PATH] [FILE ...]
    raw-pii-guard.py --self-test

Ohne FILE-Argumente werden die gestageten *.py-Dateien geprueft (git diff --cached).
Override-Listen: `.claude/raw-pii-guard.local` (eine Eintrag pro Zeile, `#`-Kommentare),
Praefix `sink:` fuer zusaetzliche Senken, sonst zusaetzliches verbotenes Feld.
"""

from __future__ import annotations

import argparse
import ast
import os
import shutil
import subprocess
import sys

# Verbotene Feld-/Argument-Namen (Default). Bewusst spezifische "Roh-/Klartext"-Marker,
# damit die Fehlalarm-Quote niedrig bleibt — generische Namen wie `email` sind NICHT dabei.
DEFAULT_FORBIDDEN = {
    "original_value", "plaintext", "plain_text", "raw_value", "raw_pii",
    "cleartext", "clear_text", "decrypted", "decrypted_value",
    "unmasked", "unmasked_value", "unredacted",
}

# Namen, die als Log-/Audit-Senke gelten (Root-Name oder Attribut-Eigentuemer).
DEFAULT_SINKS = {"log", "logger", "logging", "audit", "audit_log", "auditlog", "audit_logger"}


def load_overlay(config_path: str | None) -> tuple[set[str], set[str]]:
    """Liest optionale Projekt-Overlay-Liste. Gibt (extra_forbidden, extra_sinks) zurueck."""
    forbidden: set[str] = set()
    sinks: set[str] = set()
    path = config_path or ".claude/raw-pii-guard.local"
    if not os.path.isfile(path):
        return forbidden, sinks
    with open(path, encoding="utf-8") as fh:
        for line in fh:
            line = line.split("#", 1)[0].strip()
            if not line:
                continue
            if line.startswith("sink:"):
                sinks.add(line[len("sink:"):].strip())
            else:
                forbidden.add(line)
    return forbidden, sinks


def _sink_token(func: ast.AST) -> str | None:
    """Root-Name der Aufruf-Funktion.

    Beispiele: `logger.info` -> 'logger', `self.log.warn` -> 'log'.
    """
    if isinstance(func, ast.Attribute):
        value = func.value
        if isinstance(value, ast.Name):
            return value.id
        if isinstance(value, ast.Attribute):
            return value.attr
    return None


class _Finder(ast.NodeVisitor):
    def __init__(self, forbidden: set[str], sinks: set[str], filename: str):
        self.forbidden = forbidden
        self.sinks = sinks
        self.filename = filename
        self.findings: list[tuple[int, int, str, str]] = []  # (line, col, sink, field)

    def _record(self, node: ast.Call, sink_name: str, field: str) -> None:
        self.findings.append((node.lineno, node.col_offset, sink_name, field))

    def visit_Call(self, node: ast.Call) -> None:
        token = _sink_token(node.func)
        if token is not None and token in self.sinks:
            sink_name = ast.unparse(node.func) if hasattr(ast, "unparse") else token
            # 1) verbotene Keyword-Argumente: logger.info(..., original_value=x)
            for kw in node.keywords:
                if kw.arg and kw.arg in self.forbidden:
                    self._record(node, sink_name, f"kwarg '{kw.arg}'")
            # 2) verbotene Attribut-Lesezugriffe / Namen in den Argumenten:
            #    logger.info(user.original_value)  bzw.  logger.info(plaintext)
            for arg in list(node.args) + [kw.value for kw in node.keywords]:
                for sub in ast.walk(arg):
                    if isinstance(sub, ast.Attribute) and sub.attr in self.forbidden:
                        self._record(node, sink_name, f"attr '.{sub.attr}'")
                    elif isinstance(sub, ast.Name) and sub.id in self.forbidden:
                        self._record(node, sink_name, f"name '{sub.id}'")
        self.generic_visit(node)


def scan_source(source: str, filename: str, forbidden: set[str], sinks: set[str]):
    try:
        tree = ast.parse(source, filename=filename)
    except SyntaxError:
        return None  # unparsebar -> Datei ueberspringen (Signal an Aufrufer)
    finder = _Finder(forbidden, sinks, filename)
    finder.visit(tree)
    # Duplikate (gleiche Zeile/Feld) entfernen, Reihenfolge erhalten
    seen = set()
    unique = []
    for f in finder.findings:
        key = (f[0], f[3])
        if key not in seen:
            seen.add(key)
            unique.append(f)
    return unique


def staged_python_files() -> list[str]:
    git = shutil.which("git")  # absoluter Pfad statt partiellem "git" (vermeidet S607)
    if git is None:
        return []
    try:
        # S603 bewusst unterdrueckt: feste argv-Liste, kein shell=True, kein User-Input.
        out = subprocess.run(  # noqa: S603
            [git, "diff", "--cached", "--name-only", "--diff-filter=ACM"],
            capture_output=True, text=True, check=True,
        ).stdout
    except (subprocess.CalledProcessError, FileNotFoundError):
        return []
    return [p for p in out.splitlines() if p.endswith(".py") and os.path.isfile(p)]


def run(files: list[str], forbidden: set[str], sinks: set[str], strict: bool) -> int:
    total = 0
    for path in files:
        try:
            with open(path, encoding="utf-8") as fh:
                source = fh.read()
        except OSError:
            continue
        findings = scan_source(source, path, forbidden, sinks)
        if findings is None:
            print(f"  ~ {path}: konnte nicht geparst werden (uebersprungen)", file=sys.stderr)
            continue
        for line, col, sink, field in findings:
            total += 1
            print(f"  {path}:{line}:{col}  PII in Log-Senke '{sink}' — verbotenes Feld: {field}")
    if total == 0:
        return 0
    label = "FEHLER" if strict else "WARNUNG"
    print("")
    print(f"raw-pii-guard: {total} potenzielle PII-in-Logs-Stelle(n) [{label}].")
    print("  Roh-/Klartext-PII gehoert nicht in Logs (DSGVO Art. 5/32). "
          "Pseudonymisieren/maskieren.")
    if not strict:
        print("  (Default = Warnung. Mit --strict / STRICT=1 wird dies zum harten Fehler.)")
    return 1 if strict else 0


SELF_TEST_BAD = '''
import logging
logger = logging.getLogger(__name__)
def f(user):
    logger.info("login", original_value=user.email)   # kwarg -> WARN
    log.warning(user.plaintext)                        # attr  -> WARN
    audit.record(raw_value)                            # name  -> WARN
'''

SELF_TEST_GOOD = '''
import logging
logger = logging.getLogger(__name__)
# original_value=... darf im Kommentar stehen
msg = "plaintext ist hier nur ein String"
def f(user):
    logger.info("login", user_id=user.id)              # ok
    increment_counter("logins")                        # keine Senke
    x = user.original_value                             # kein Log-Aufruf
'''


def self_test() -> int:
    bad = scan_source(SELF_TEST_BAD, "<bad>", DEFAULT_FORBIDDEN, DEFAULT_SINKS)
    good = scan_source(SELF_TEST_GOOD, "<good>", DEFAULT_FORBIDDEN, DEFAULT_SINKS)
    ok = True
    if not bad or len(bad) != 3:
        print(f"SELF-TEST FAIL: bad-Snippet erwartet 3 Treffer, hat {len(bad or [])}: {bad}")
        ok = False
    if good:
        print(f"SELF-TEST FAIL: good-Snippet erwartet 0 Treffer, hat {len(good)}: {good}")
        ok = False
    print("SELF-TEST OK" if ok else "SELF-TEST FAILED")
    return 0 if ok else 1


def main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser(description="Optionaler PII-in-Logs-Guard (AST, BOO-93).")
    parser.add_argument("files", nargs="*", help="zu pruefende Dateien (Default: gestagete *.py)")
    parser.add_argument("--strict", action="store_true",
                        help="Treffer = Exit 1 (Default: nur Warnung)")
    parser.add_argument("--config",
                        help="Pfad zur Overlay-Liste (Default: .claude/raw-pii-guard.local)")
    parser.add_argument("--self-test", action="store_true",
                        help="Internen Selbsttest laufen lassen")
    args = parser.parse_args(argv)

    if args.self_test:
        return self_test()

    strict = (
        args.strict
        or os.environ.get("STRICT") == "1"
        or os.environ.get("RAW_PII_STRICT") == "1"
    )
    extra_forbidden, extra_sinks = load_overlay(args.config)
    forbidden = DEFAULT_FORBIDDEN | extra_forbidden
    sinks = DEFAULT_SINKS | extra_sinks

    files = args.files or staged_python_files()
    if not files:
        return 0
    return run(files, forbidden, sinks, strict)


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
