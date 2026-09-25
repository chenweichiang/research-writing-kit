"""Shared helpers for the tools/ smoke tests. Nothing here touches the network:
the autouse fixture below makes any socket connection in the test process fail."""
import importlib.util
import os
import random
import socket
import subprocess
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
TOOLS = ROOT / "tools"


@pytest.fixture(autouse=True)
def no_network(monkeypatch):
    def refuse(*_a, **_k):
        raise OSError("network disabled in tests")
    monkeypatch.setattr(socket.socket, "connect", refuse)
    monkeypatch.setattr(socket, "create_connection", refuse)


def run_tool(rel, *args, home=None, env=None, stdin=None, cwd=None):
    """Run tools/<rel> as a subprocess. HOME points at a temp dir so baseline caches
    never land in the real home directory."""
    e = dict(os.environ)
    if home is not None:
        e["HOME"] = str(home)
    e.update(env or {})
    for k in ("HTTP_PROXY", "HTTPS_PROXY", "http_proxy", "https_proxy"):
        e[k] = "http://127.0.0.1:9"   # a subprocess that tries the network fails fast
    cmd = ["bash"] if rel.endswith(".sh") else [sys.executable]
    return subprocess.run(cmd + [str(TOOLS / rel), *map(str, args)], capture_output=True,
                          text=True, encoding="utf-8", env=e, input=stdin,
                          cwd=cwd or ROOT, timeout=120)


_loaded = {}


def load_tool(rel):
    """Import tools/<rel> as a module (the folders are not packages)."""
    if rel not in _loaded:
        path = TOOLS / rel
        sys.path.insert(0, str(path.parent))
        name = "kit_" + rel.replace("/", "_").replace("-", "_").removesuffix(".py")
        spec = importlib.util.spec_from_file_location(name, path)
        mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mod)
        _loaded[rel] = mod
    return _loaded[rel]


WORDS = ("design study participants data method results analysis model system users "
         "interface evaluation findings approach research context practice design task "
         "measure effect sample interview theory framework process outcome feedback").split()


def english_text(seed, n_words=900):
    """Deterministic filler prose: capitalised sentences of 8 to 20 words."""
    rnd = random.Random(seed)
    out, total = [], 0
    while total < n_words:
        k = rnd.randint(8, 20)
        words = [rnd.choice(WORDS) for _ in range(k)]
        if rnd.random() < 0.3:
            words[k // 2] += ","
        out.append(" ".join(words).capitalize() + ".")
        total += k
    return " ".join(out)


def make_corpus(root, n=30, venue="venue"):
    d = Path(root) / venue
    d.mkdir(parents=True, exist_ok=True)
    for i in range(n):
        (d / f"paper{i:02d}.txt").write_text(english_text(i), encoding="utf-8")
    return Path(root)
