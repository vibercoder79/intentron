#!/usr/bin/env python3
"""anti-placeholder-check — Anti-Platzhalter-Check fuer Test-Dateien (BOO-177).

DE: Gezielter, deterministischer Check auf TEST-Dateien (KEIN Linter). Flaggt
    Tests, die die Coverage-Zahl heben, ohne etwas zu testen:
      (1) triviale/leere Assertions: `expect(true).toBe(true)`, `assert True`,
          `assert 1 == 1`, leerer Testkoerper (nur `pass` / `{}`),
      (2) unbegruendete Skips: `it.skip`/`test.skip`/`describe.skip`/`xit`/
          `xdescribe`, `@pytest.mark.skip` / `@pytest.mark.skipif` OHNE `reason=`
          bzw. ohne erklaerenden Begruendungskommentar in derselben Zeile.
    Python: AST (wie raw-pii-guard.py, BOO-93) — ignoriert Kommentare/Strings,
    versteht Aufruf-/Body-Struktur (kaum Fehlalarme). JS/TS: zeilen-basierte
    Heuristik (kein JS-Parser in der Stdlib), bewusst spezifische Muster.
EN: Targeted, deterministic check on TEST files (NOT a linter). Flags tests that
    lift the coverage number without testing anything: trivial/empty assertions,
    empty test bodies, and unjustified skips (no `reason=` / no justifying comment).
    Python via AST (like raw-pii-guard.py); JS/TS via line heuristic.

Default = Warnung (Exit 0). Mit `--strict` bzw. `STRICT=1` wird ein Treffer zum
Fehler (Exit 1) — konsistent mit raw-pii-guard.py (BOO-93) / dem Layer-0-Bodyguard
(BOO-86), die ebenfalls warn-default sind. Dependency-frei: nur python3-Stdlib
(`ast`, `re`). Kein Code aus Fremd-Repos uebernommen.

Usage:
    anti-placeholder-check.py [--strict] [--config PATH] [FILE ...]
    anti-placeholder-check.py --self-test

Ohne FILE-Argumente werden die gestageten Test-Dateien geprueft (git diff --cached),
erkannt an: *.test.{js,ts,jsx,tsx}, *.spec.{js,ts}, test_*.py, *_test.py, tests/**.
Override-Liste: `.claude/anti-placeholder-check.local` (ein Eintrag pro Zeile,
`#`-Kommentare); Praefix `path:` fuer zusaetzliche Test-Pfad-Globs (z.B. `path:spec/`),
sonst ein zusaetzlicher Datei-Glob, der von der Pruefung AUSGENOMMEN wird (Allowlist).
"""

from __future__ import annotations

import argparse
import ast
import fnmatch
import os
import re
import shutil
import subprocess
import sys

# --- Test-Datei-Erkennung (Quelle: Jest/Vitest- und pytest-Konventionen) ---
# Jest/Vitest: *.test.*, *.spec.* ; pytest: test_*.py, *_test.py, tests/**, conftest.py.
TEST_FILE_GLOBS = (
    "*.test.js", "*.test.ts", "*.test.jsx", "*.test.tsx",
    "*.test.mjs", "*.test.cjs",
    "*.spec.js", "*.spec.ts", "*.spec.jsx", "*.spec.tsx",
    "*.spec.mjs", "*.spec.cjs",
    "test_*.py", "*_test.py",
)
# Zusaetzlich gelten Pfade unter tests/ bzw. __tests__/ als Test-Dateien.
TEST_DIR_MARKERS = ("tests/", "/tests/", "__tests__/", "/__tests__/")

_PY_EXT = (".py",)
_JS_EXT = (".js", ".mjs", ".cjs", ".ts", ".jsx", ".tsx")


def is_test_file(path: str, extra_globs: tuple[str, ...] = ()) -> bool:
    base = os.path.basename(path)
    norm = path.replace(os.sep, "/")
    for glob in TEST_FILE_GLOBS + extra_globs:
        if "/" in glob:
            if fnmatch.fnmatch(norm, glob) or fnmatch.fnmatch(norm, "*/" + glob):
                return True
        elif fnmatch.fnmatch(base, glob):
            return True
    if norm.startswith(("tests/", "__tests__/")):
        return True
    return any(m in norm for m in TEST_DIR_MARKERS)


def load_overlay(config_path: str | None) -> tuple[tuple[str, ...], tuple[str, ...]]:
    """Liest optionale Projekt-Overlay-Liste. Gibt (allow_globs, extra_test_globs) zurueck.

    allow_globs   -> diese Dateien werden von der Pruefung AUSGENOMMEN (Allowlist).
    extra_globs   -> zusaetzliche Pfade, die ALS Test-Datei gelten (Praefix `path:`).
    """
    allow: list[str] = []
    extra: list[str] = []
    path = config_path or ".claude/anti-placeholder-check.local"
    if not os.path.isfile(path):
        return tuple(allow), tuple(extra)
    with open(path, encoding="utf-8") as fh:
        for line in fh:
            line = line.split("#", 1)[0].strip()
            if not line:
                continue
            if line.startswith("path:"):
                extra.append(line[len("path:"):].strip())
            else:
                allow.append(line)
    return tuple(allow), tuple(extra)


# -----------------------------------------------------------------------------
# Python — AST-basiert
# -----------------------------------------------------------------------------

# Test-Funktion = def, dessen Name mit `test` beginnt (pytest-Konvention)
# oder die innerhalb einer Test-Klasse (`class Test...`) liegt.
_TEST_FN_RE = re.compile(r"^test")


def _is_trivial_compare(node: ast.AST) -> bool:
    """assert 1 == 1, assert True == True, assert 'x' == 'x' (beide Seiten gleiche Konstante)."""
    if isinstance(node, ast.Compare) and len(node.ops) == 1 and isinstance(node.ops[0], ast.Eq):
        left, right = node.left, node.comparators[0]
        if isinstance(left, ast.Constant) and isinstance(right, ast.Constant):
            return left.value == right.value
    return False


def _is_trivial_assert(node: ast.Assert) -> bool:
    test = node.test
    # assert True / assert 1 (truthy Konstante ohne Aussage)
    if isinstance(test, ast.Constant):
        return bool(test.value)
    return _is_trivial_compare(test)


def _has_skip_reason_py(decorator: ast.Call) -> bool:
    """pytest.mark.skip(reason=...) / skipif(condition, reason=...) — reason= vorhanden?"""
    for kw in decorator.keywords:
        if kw.arg == "reason":
            # leere/Whitespace-only reason zaehlt nicht als Begruendung
            if isinstance(kw.value, ast.Constant) and isinstance(kw.value.value, str):
                return bool(kw.value.value.strip())
            return True
    return False


def _decorator_is_skip(dec: ast.AST) -> tuple[bool, ast.Call | None]:
    """Erkennt @pytest.mark.skip / @pytest.mark.skipif (auch ohne Aufruf-Klammern)."""
    target = dec.func if isinstance(dec, ast.Call) else dec
    if isinstance(target, ast.Attribute) and target.attr in ("skip", "skipif"):
        owner = target.value
        if isinstance(owner, ast.Attribute) and owner.attr == "mark":
            call = dec if isinstance(dec, ast.Call) else None
            return True, call
    return False, None


def _body_is_empty(body: list[ast.stmt]) -> bool:
    """Funktionskoerper besteht nur aus pass und/oder einem Docstring-Ausdruck."""
    meaningful = []
    for stmt in body:
        if isinstance(stmt, ast.Pass):
            continue
        if isinstance(stmt, ast.Expr) and isinstance(stmt.value, ast.Constant) \
                and isinstance(stmt.value.value, str):
            continue  # Docstring
        if isinstance(stmt, ast.Expr) and isinstance(stmt.value, ast.Constant) \
                and stmt.value.value is Ellipsis:
            continue  # ...
        meaningful.append(stmt)
    return not meaningful


class _PyFinder(ast.NodeVisitor):
    def __init__(self, filename: str):
        self.filename = filename
        self.findings: list[tuple[int, int, str]] = []  # (line, col, message)
        self._in_test_class = 0

    def _record(self, node: ast.AST, msg: str) -> None:
        self.findings.append((node.lineno, getattr(node, "col_offset", 0), msg))

    def visit_ClassDef(self, node: ast.ClassDef) -> None:
        is_test_class = node.name.startswith("Test")
        if is_test_class:
            self._in_test_class += 1
        self.generic_visit(node)
        if is_test_class:
            self._in_test_class -= 1

    def _visit_func(self, node: ast.FunctionDef | ast.AsyncFunctionDef) -> None:
        is_test = bool(_TEST_FN_RE.match(node.name)) or self._in_test_class > 0
        # Skip-Dekoratoren immer pruefen (auch bei Nicht-Test-Funktionen, da Marker spezifisch)
        for dec in node.decorator_list:
            is_skip, call = _decorator_is_skip(dec)
            if is_skip and not (call is not None and _has_skip_reason_py(call)):
                self._record(dec, f"unbegruendeter Skip-Marker auf '{node.name}' "
                                  f"(@pytest.mark.skip/skipif ohne reason=)")
        if is_test:
            if _body_is_empty(node.body):
                self._record(node, f"leerer Test-Koerper in '{node.name}' (nur pass/.../docstring)")
            for sub in ast.walk(node):
                if isinstance(sub, ast.Assert) and _is_trivial_assert(sub):
                    self._record(sub, f"triviale Assertion in '{node.name}' "
                                      f"(assert True / assert x == x)")
        self.generic_visit(node)

    visit_FunctionDef = _visit_func
    visit_AsyncFunctionDef = _visit_func


def scan_python(source: str, filename: str):
    try:
        tree = ast.parse(source, filename=filename)
    except SyntaxError:
        return None
    finder = _PyFinder(filename)
    finder.visit(tree)
    seen = set()
    unique = []
    for f in finder.findings:
        if (f[0], f[2]) not in seen:
            seen.add((f[0], f[2]))
            unique.append(f)
    return unique


# -----------------------------------------------------------------------------
# JS/TS — zeilen-basierte Heuristik (keine JS-AST in der Stdlib)
# -----------------------------------------------------------------------------

# Triviale Assertions (Jest/Vitest/Chai-Stil). Bewusst spezifisch.
_JS_TRIVIAL = re.compile(
    r"""expect\(\s*(true|1)\s*\)\s*\.\s*(toBe|toEqual|toStrictEqual)\s*\(\s*(true|1)\s*\)"""
    r"""|assert\s*\.\s*(ok|isTrue)\s*\(\s*true\s*\)"""
    r"""|assert\s*\(\s*true\s*\)"""
    r"""|expect\(\s*(true)\s*\)\s*\.\s*toBeTruthy\s*\(\s*\)""",
    re.VERBOSE,
)
# Skip-Marker: it.skip / test.skip / describe.skip / xit / xdescribe / xtest.
_JS_SKIP = re.compile(
    r"""\b(?:it|test|describe)\s*\.\s*skip\s*\("""
    r"""|\b(?:xit|xdescribe|xtest)\s*\(""",
    re.VERBOSE,
)
# Begruendung gilt als vorhanden, wenn in der Zeile ODER der Vorgaengerzeile
# ein Kommentar steht (// ... oder /* ... */).
_JS_COMMENT = re.compile(r"//.+|/\*.+?\*/")


def _strip_js_strings(line: str) -> str:
    """Entfernt simple String-Literale, damit Treffer in Strings nicht falsch flaggen."""
    line = re.sub(r"'(?:\\.|[^'\\])*'", "''", line)
    line = re.sub(r'"(?:\\.|[^"\\])*"', '""', line)
    line = re.sub(r"`(?:\\.|[^`\\])*`", "``", line)
    return line


def _js_skip_finding(lines: list[str], idx: int, raw: str, code: str):
    """Liefert (col, msg) wenn ein unbegruendeter Skip in der Zeile steht, sonst None."""
    s = _JS_SKIP.search(code)
    if not s:
        return None
    has_reason = bool(_JS_COMMENT.search(raw))
    if not has_reason and idx > 0:
        has_reason = bool(_JS_COMMENT.search(lines[idx - 1]))
    if has_reason:
        return None
    return (s.start(), "unbegruendeter Skip "
            "(it.skip/test.skip/describe.skip/xit ohne Begruendungskommentar)")


def scan_js(source: str, _filename: str):
    findings: list[tuple[int, int, str]] = []
    lines = source.splitlines()
    for idx, raw in enumerate(lines):
        # Kommentar-only-Zeile ueberspringen (kein Code).
        if raw.strip().startswith(("//", "*", "/*")):
            continue
        code = _strip_js_strings(raw)
        m = _JS_TRIVIAL.search(code)
        if m:
            findings.append((idx + 1, m.start(), "triviale Assertion "
                             "(expect(true).toBe(true) / assert(true))"))
        skip = _js_skip_finding(lines, idx, raw, code)
        if skip:
            findings.append((idx + 1, skip[0], skip[1]))
    return findings


# -----------------------------------------------------------------------------
# Dispatch + Runner
# -----------------------------------------------------------------------------

def scan_file(path: str, source: str):
    if path.endswith(_PY_EXT):
        return scan_python(source, path)
    if path.endswith(_JS_EXT):
        return scan_js(source, path)
    return []  # nicht abgedeckte Endung -> nichts zu pruefen


def staged_test_files(extra_globs: tuple[str, ...], allow_globs: tuple[str, ...]) -> list[str]:
    git = shutil.which("git")
    if git is None:
        return []
    try:
        out = subprocess.run(  # noqa: S603
            [git, "diff", "--cached", "--name-only", "--diff-filter=ACM"],
            capture_output=True, text=True, check=True,
        ).stdout
    except (subprocess.CalledProcessError, FileNotFoundError):
        return []
    files = []
    for p in out.splitlines():
        if not os.path.isfile(p):
            continue
        if any(fnmatch.fnmatch(p, g) or fnmatch.fnmatch(os.path.basename(p), g)
               for g in allow_globs):
            continue
        if is_test_file(p, extra_globs):
            files.append(p)
    return files


def run(files: list[str], strict: bool, extra_globs: tuple[str, ...],
        allow_globs: tuple[str, ...]) -> int:
    total = 0
    for path in files:
        if any(fnmatch.fnmatch(path, g) or fnmatch.fnmatch(os.path.basename(path), g)
               for g in allow_globs):
            continue
        if not is_test_file(path, extra_globs):
            continue
        try:
            with open(path, encoding="utf-8") as fh:
                source = fh.read()
        except OSError:
            continue
        findings = scan_file(path, source)
        if findings is None:
            print(f"  ~ {path}: konnte nicht geparst werden (uebersprungen)", file=sys.stderr)
            continue
        for line, col, msg in findings:
            total += 1
            print(f"  {path}:{line}:{col}  Platzhalter-Test — {msg}")
    if total == 0:
        return 0
    label = "FEHLER" if strict else "WARNUNG"
    print("")
    print(f"anti-placeholder-check: {total} Platzhalter-Test-Stelle(n) [{label}].")
    print("  Platzhalter-Tests heben die Coverage, ohne etwas zu testen (BOO-177). "
          "Echte Assertion schreiben oder Skip begruenden (reason= / Kommentar).")
    if not strict:
        print("  (Default = Warnung. Mit --strict / STRICT=1 wird dies zum harten Fehler.)")
    return 1 if strict else 0


# -----------------------------------------------------------------------------
# Selbsttest
# -----------------------------------------------------------------------------

SELF_TEST_PY_BAD = '''
import pytest

def test_trivial_true():
    assert True                      # triviale Assertion -> FLAG

def test_trivial_eq():
    assert 1 == 1                    # triviale Assertion -> FLAG

def test_empty():
    pass                             # leerer Koerper -> FLAG

@pytest.mark.skip
def test_skipped_no_reason():
    assert add(1, 2) == 3            # unbegruendeter Skip -> FLAG
'''

SELF_TEST_PY_GOOD = '''
import pytest

def test_real():
    assert add(2, 3) == 5            # echte Assertion -> ok

@pytest.mark.skip(reason="Backend noch nicht deployt")
def test_skipped_with_reason():
    assert call_backend() == 200     # begruendeter Skip -> ok

@pytest.mark.skipif(SLOW, reason="nur im Nightly")
def test_slow():
    assert heavy() is not None       # begruendeter skipif -> ok
'''

SELF_TEST_JS_BAD = '''
describe("suite", () => {
  it("trivial", () => {
    expect(true).toBe(true);
  });
  it.skip("no reason", () => {
    expect(add(1, 2)).toBe(3);
  });
  xit("also skipped", () => {
    expect(sub(2, 1)).toBe(1);
  });
});
'''

SELF_TEST_JS_GOOD = '''
describe("suite", () => {
  it("real", () => {
    expect(add(2, 3)).toBe(5);
  });
  // Backend nicht verfuegbar in CI
  it.skip("skipped with reason above", () => {
    expect(call()).toBe(200);
  });
  const msg = "expect(true).toBe(true) ist hier nur ein String";
});
'''


def self_test() -> int:
    ok = True

    py_bad = scan_python(SELF_TEST_PY_BAD, "<py-bad>")
    if not py_bad or len(py_bad) != 4:
        print(f"SELF-TEST FAIL: py-bad erwartet 4 Treffer, hat {len(py_bad or [])}: {py_bad}")
        ok = False
    py_good = scan_python(SELF_TEST_PY_GOOD, "<py-good>")
    if py_good:
        print(f"SELF-TEST FAIL: py-good erwartet 0 Treffer, hat {len(py_good)}: {py_good}")
        ok = False

    # JS-bad: trivial (1) + it.skip ohne Kommentar (1) + xit ohne Kommentar (1) = 3 Treffer.
    js_bad = scan_js(SELF_TEST_JS_BAD, "<js-bad>")
    if not js_bad or len(js_bad) != 3:
        print(f"SELF-TEST FAIL: js-bad erwartet 3 Treffer, hat {len(js_bad or [])}: {js_bad}")
        ok = False
    js_good = scan_js(SELF_TEST_JS_GOOD, "<js-good>")
    if js_good:
        print(f"SELF-TEST FAIL: js-good erwartet 0 Treffer, hat {len(js_good)}: {js_good}")
        ok = False

    # Test-Datei-Erkennung
    detect_cases = {
        "src/foo.test.ts": True, "a/b.spec.js": True, "tests/x.py": True,
        "test_thing.py": True, "thing_test.py": True, "pkg/__tests__/c.jsx": True,
        "src/foo.ts": False, "lib/util.py": False, "README.md": False,
    }
    for path, expected in detect_cases.items():
        if is_test_file(path) != expected:
            print(f"SELF-TEST FAIL: is_test_file({path!r}) != {expected}")
            ok = False

    print("SELF-TEST OK" if ok else "SELF-TEST FAILED")
    return 0 if ok else 1


def main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser(
        description="Anti-Platzhalter-Check fuer Test-Dateien (BOO-177).")
    parser.add_argument("files", nargs="*",
                        help="zu pruefende Dateien (Default: gestagete Test-Dateien)")
    parser.add_argument("--strict", action="store_true",
                        help="Treffer = Exit 1 (Default: nur Warnung)")
    parser.add_argument("--config",
                        help="Pfad zur Overlay-Liste "
                             "(Default: .claude/anti-placeholder-check.local)")
    parser.add_argument("--self-test", action="store_true",
                        help="Internen Selbsttest laufen lassen")
    args = parser.parse_args(argv)

    if args.self_test:
        return self_test()

    strict = (
        args.strict
        or os.environ.get("STRICT") == "1"
        or os.environ.get("ANTI_PLACEHOLDER_STRICT") == "1"
    )
    allow_globs, extra_globs = load_overlay(args.config)

    files = args.files or staged_test_files(extra_globs, allow_globs)
    if not files:
        return 0
    return run(files, strict, extra_globs, allow_globs)


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
