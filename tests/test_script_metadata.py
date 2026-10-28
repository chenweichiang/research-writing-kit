"""Every runnable tool declares its Python floor and packages inline (PEP 723), so
`uv run tools/<dir>/<tool>.py` installs what it needs. A package imported at module
level without a fallback must be in that list."""
import ast
import re

import pytest
from conftest import TOOLS

# Shared modules and tools that need their own environment (see setup/TOOLS.md).
NO_HEADER = {
    "common/md_prose.py",
    "refs/refs_common.py",
    "zh-tw/zh_tw_terms.py",
    "en/biber_diag.py",
    "method/tea_second_opinion.py",
}
# import name -> distribution name
DIST = {
    "numpy": "numpy",
    "PIL": "pillow",
    "fitz": "pymupdf",
    "pymupdf": "pymupdf",
    "docx": "python-docx",
    "lxml": "lxml",
    "yaml": "pyyaml",
}
BLOCK = re.compile(r"(?m)^# /// script$\s(?P<content>(^#(| .*)$\s)+)^# ///$")
SCRIPTS = sorted(p for p in TOOLS.rglob("*.py") if "__pycache__" not in p.parts)


def rel(p):
    return p.relative_to(TOOLS).as_posix()


def metadata(text):
    blocks = list(BLOCK.finditer(text))
    if not blocks:
        return None
    assert len(blocks) == 1, "more than one script block"
    fields = {}
    for line in blocks[0].group("content").splitlines():
        key, _, value = line[2:].partition("=")
        if key.strip():
            fields[key.strip()] = ast.literal_eval(value.strip())
    return fields


def unguarded_imports(tree):
    """Top-level imports that are not inside a try block."""
    names = set()
    for node in tree.body:
        if isinstance(node, ast.Import):
            names.update(a.name.split(".")[0] for a in node.names)
        elif isinstance(node, ast.ImportFrom) and node.module and not node.level:
            names.add(node.module.split(".")[0])
    return names


@pytest.mark.parametrize("path", SCRIPTS, ids=rel)
def test_script_metadata(path):
    text = path.read_text(encoding="utf-8")
    meta = metadata(text)
    if rel(path) in NO_HEADER:
        assert meta is None
        return
    assert meta is not None, "missing a PEP 723 block (# /// script)"
    assert meta.get("requires-python") == ">=3.9"
    deps = meta.get("dependencies")
    assert isinstance(deps, list)
    needed = {DIST[n] for n in unguarded_imports(ast.parse(text)) if n in DIST}
    assert needed <= set(deps), f"imported without a fallback but not declared: {sorted(needed - set(deps))}"
    assert set(deps) <= set(DIST.values()), f"unknown package name: {sorted(set(deps) - set(DIST.values()))}"
