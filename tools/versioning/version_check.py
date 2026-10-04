#!/usr/bin/env python3
"""version_check.py: pre-delivery version check for a manuscript or deliverable project.

Checks VERSION, CHANGELOG, the delivery folder, PDF metadata, the body text of the
submission copy, and git tag reuse. The rules are in method/VERSIONING.md. Why a
mechanical check: version drift raises no error; it surfaces the day a co-author
asks "which version am I looking at?" or a reviewer sees "v0.29.1" in the body text.

What is checked:
  - VERSION exists and is X.Y.Z (a two-part X.Y is accepted with a warning)
  - the newest CHANGELOG.md section is the same version (write the changelog first, then build)
  - the delivery folder holds exactly one version, and it is VERSION
  - delivered PDFs carry the version in Title / Subject / Keywords (needs pdfinfo)
  - the body text of each submission file has no version string and no review-copy footer
    (needs pdftotext for PDFs)
  - the VERSION tag (vX.Y.Z) has not been changed since it was tagged: a tagged version
    is a delivered one and must not be reused

Delivery folders: `latest/` (also `latest-submission/`) and snapshots in
`versions/vX.Y.Z/`. The Chinese names `最新交付/`、`最新投稿檔/` and `版本/` are
accepted too; whichever exists is used.

Usage:
  version_check.py <project or manuscript dir> [--latest latest] [--submission submission.pdf ...] [--json]
Exit code: 0 = no FAIL; 1 = at least one FAIL
"""
import argparse
import json
import os
import re
import subprocess
import sys

SEMVER = re.compile(r"^(\d+)\.(\d+)\.(\d+)$")
LEGACY = re.compile(r"^(\d+)\.(\d+)$")
VER_IN_TEXT = re.compile(r"(?<![\d.])v?(\d+\.\d+(?:\.\d+)?)(?!\d|\.\d)")  # a version followed by an extension (.docx) still counts
REVIEW_FOOTER = re.compile(r"review copy|審閱稿|draft v\d", re.I)
LATEST_NAMES = ("latest", "latest-submission", "最新交付", "最新投稿檔")
VERSIONS_NAMES = ("versions", "版本")
FAIL, WARN, OK = [], [], []


def find_up(start, name):
    d = os.path.abspath(start)
    for _ in range(4):
        p = os.path.join(d, name)
        if os.path.exists(p):
            return p
        d = os.path.dirname(d)
    return None


def changelog_top(path):
    with open(path, encoding="utf-8") as f:
        for line in f:
            m = re.match(r"^#{2,3}\s+v?(\d+\.\d+(?:\.\d+)?)\b", line)
            if m:
                return m.group(1)
    return None


def pdf_meta(path):
    try:
        out = subprocess.run(["pdfinfo", path], capture_output=True, text=True, timeout=30).stdout
    except Exception:
        return None            # pdfinfo missing: the caller reports it once
    return " ".join(l for l in out.splitlines() if l.split(":")[0] in ("Title", "Subject", "Keywords"))


def pdf_text(path):
    try:
        return subprocess.run(["pdftotext", path, "-"], capture_output=True, text=True, timeout=60).stdout
    except Exception:
        return None


def git(root, *args):
    try:
        r = subprocess.run(["git", "-C", root] + list(args), capture_output=True, text=True)
    except FileNotFoundError:
        return None
    return r.stdout.strip() if r.returncode == 0 else None


def main():
    ap = argparse.ArgumentParser(description=(__doc__ or "").split("\n")[0])
    ap.add_argument("root", help="project or manuscript directory")
    ap.add_argument("--latest", default="",
                    help="the folder holding only the current version (default: latest/ or latest-submission/, "
                         "or the Chinese names, in the directory or its parent)")
    ap.add_argument("--submission", nargs="*", default=[],
                    help="submission copies: the body text must not carry a version")
    ap.add_argument("--json", action="store_true")
    a = ap.parse_args()
    root = os.path.realpath(a.root)   # macOS /var is /private/var: without normalising both sides, relative paths come out wrong

    vf = find_up(root, "VERSION")
    ver = None
    if not vf:
        FAIL.append("no VERSION file (the single source of the version, see method/VERSIONING.md)")
    else:
        with open(vf, encoding="utf-8") as f:
            ver = f.read().strip().lstrip("v")
        if SEMVER.match(ver):
            OK.append(f"VERSION = {ver} ({os.path.relpath(vf, root)})")
        elif LEGACY.match(ver):
            WARN.append(f"VERSION = {ver} is the old two-part convention; use X.Y.Z for new projects")
        else:
            FAIL.append(f"VERSION content \"{ver}\" is not a version")
            ver = None

    cl = find_up(root, "CHANGELOG.md")
    if ver and cl:
        top = changelog_top(cl)
        if top is None:
            FAIL.append("CHANGELOG.md has no \"## X.Y.Z (date)\" version heading")
        elif top != ver:
            FAIL.append(f"CHANGELOG top section is {top} but VERSION is {ver}: write the CHANGELOG first, then build")
        else:
            OK.append("CHANGELOG top section = VERSION")
    elif ver:
        WARN.append("no CHANGELOG.md (every version needs a record of what changed, on what basis, for whom)")

    latest = a.latest or next((os.path.join(d, n) for d in (root, os.path.dirname(root))
                               for n in LATEST_NAMES if os.path.isdir(os.path.join(d, n))), "")
    if latest and ver:
        files = [f for f in os.listdir(latest) if not f.startswith(".")]
        seen = set()
        for f in files:
            for m in VER_IN_TEXT.finditer(f):
                if "." in m.group(1) and not re.fullmatch(r"(19|20)\d{2}\.\d+", m.group(1)):
                    seen.add(m.group(1))
        rel = os.path.relpath(latest, root)
        vdir = next((n for n in VERSIONS_NAMES if os.path.isdir(os.path.join(os.path.dirname(latest), n))),
                    "版本" if re.search(r"[一-鿿]", os.path.basename(latest)) else "versions")
        if not files:
            WARN.append(f"{rel} is empty")
        elif seen - {ver}:
            FAIL.append(f"{rel} mixes in other versions: {', '.join(sorted(seen - {ver}))} "
                        f"(it holds only the current version; move old ones to {vdir}/)")
        elif ver not in seen:
            FAIL.append(f"no file name in {rel} carries {ver}: has the deliverable been rebuilt?")
        else:
            OK.append(f"{rel} has only {ver}")
        no_meta_tool = False
        for f in files:
            if f.lower().endswith(".pdf"):
                meta = pdf_meta(os.path.join(latest, f))
                if meta is None:
                    no_meta_tool = True
                elif ver not in meta:
                    WARN.append(f"PDF metadata (Title / Subject / Keywords) of {f} has no version")
        if no_meta_tool:
            WARN.append("pdfinfo (poppler) not found: PDF metadata was not checked")

    for s in a.submission:
        if s.lower().endswith(".pdf"):
            txt = pdf_text(s)
            if txt is None:
                WARN.append(f"pdftotext (poppler) not found: body text of {os.path.basename(s)} was not checked")
                continue
        else:
            with open(s, encoding="utf-8", errors="ignore") as f:
                txt = f.read()
        hits = {m.group(0) for m in VER_IN_TEXT.finditer(txt) if ver and m.group(1) == ver}
        if hits or (ver and REVIEW_FOOTER.search(txt)):
            FAIL.append(f"body text of submission copy {os.path.basename(s)} shows a version or a review-copy marker: "
                        "a submission copy carries the version only in its file name and metadata")
        else:
            OK.append(f"submission copy {os.path.basename(s)} has no version in its body")

    gr = git(root, "rev-parse", "--show-toplevel")
    if ver and gr:
        gr = os.path.realpath(gr)
        tag = "v" + ver
        if git(gr, "rev-parse", "-q", "--verify", f"refs/tags/{tag}") is not None:
            rel = os.path.relpath(root, gr)
            changed = git(gr, "diff", "--name-only", tag, "HEAD", "--", rel)
            dirty = git(gr, "status", "--porcelain", "--", rel)
            if changed is None or dirty is None:
                FAIL.append(f"git failed to list changes since {tag}: the tag-reuse check did not run")  # a failure must not read as "no changes"
            elif changed or dirty:
                FAIL.append(f"{tag} is tagged (= delivered) and has changed since: bump the version, do not reuse {ver}")
            else:
                OK.append(f"{tag} is tagged, no changes since")

    if a.json:
        print(json.dumps({"version": ver, "fail": FAIL, "warn": WARN, "ok": OK}, ensure_ascii=False, indent=1))
    else:
        for x in OK:
            print("  ✓ " + x)
        for x in WARN:
            print("  🟡 " + x)
        for x in FAIL:
            print("  🔴 " + x)
        print(f"-- version {ver or '?'} | FAIL {len(FAIL)} | WARN {len(WARN)} --")
    return 1 if FAIL else 0


if __name__ == "__main__":
    sys.exit(main())
