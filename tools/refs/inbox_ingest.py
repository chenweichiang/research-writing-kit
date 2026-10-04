#!/usr/bin/env python3
"""inbox_ingest.py: file the reference PDFs you downloaded by hand (stdlib only, no network;
the external `pdftotext` binary is optional).

After missing_refs.py gives you a "please download these" list, you fetch the PDFs yourself
(library proxy, publisher site, author page). They land in ~/Downloads under publisher names
(`1-s2.0-S0142694X...pdf`, `10.1145_3544548.3581234.pdf`, `x (1).pdf`). This tool matches each
one to a missing .bib entry, checks the content, files it under the project's name, and
optionally copies it into your personal library and tidies the Downloads folder.

Flow:
  1. Entries with no PDF in <pdfdir> (<citekey>.pdf, or a hand-filed `NN [Author Year] Title.pdf`
     matched by file name) are the "missing" ones (same definition as missing_refs.py).
  2. PDFs in --inbox (default: the last 72 hours; --all for no limit) are scanned. Files with
     identical content (`x.pdf`, `x (1).pdf`) count once.
  3. For each PDF: compare DOIs first (file name or first two pages), then check the content
     (title phrase match, identity doubts, preview flag). A scanned PDF with no extractable
     text, or any PDF when `pdftotext` is missing, falls back to the file name.
  4. For each missing entry the best candidate wins: verified beats LOW-CONFIDENCE, a DOI match
     beats none, more pages beat fewer. A PDF that looks like two different missing entries
     is not filed; it is listed for you to decide.
  5. Report: filed / LOW-CONFIDENCE (needs your eyes) / DOI matches but content does not /
     files that match nothing / entries still missing.

Default is a preview (writes nothing).
  --apply         copy each match to <pdfdir>/<citekey>.pdf and append a line to
                  <pdfdir>/_inbox_log.tsv (source file, tier, note). CONTENT-MISMATCH and
                  ambiguous matches are never filed.
  --to-library    with --library DIR: also copy each filed PDF into DIR as
                  `<FirstAuthorSurname> <Year> - <Title>.pdf`, skipped when DIR already holds
                  the same content (SHA-256) or the same file name.
  --clean         with --apply: move only the successfully filed source files (and identical
                  duplicates) to the Trash. Nothing is deleted. macOS uses ~/.Trash; elsewhere
                  ~/.local/share/Trash/files must already exist; otherwise --clean is refused.

Usage:
  inbox_ingest.py --bib references.bib [--pdfdir refs-pdf] [--inbox ~/Downloads]
                  [--hours 72 | --all] [--apply] [--library DIR --to-library] [--clean]
"""
import argparse
import csv
import os
import re
import shutil
import sys
import time

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import refs_common as rc  # noqa: E402

TIER_RANK = {"verified": 0, "low": 1, "mismatch": 9}


def trash_dir():
    """The Trash folder to move files into, or "" when there is none."""
    home = os.path.expanduser("~")
    path = (os.path.join(home, ".Trash") if sys.platform == "darwin"
            else os.path.join(home, ".local", "share", "Trash", "files"))
    return path if os.path.isdir(path) else ""


def scan_inbox(inbox, hours=None):
    """[{path, name, sha, dups}] for PDFs in inbox (not recursive). Files with identical content
    are merged; the one with the shortest name is kept and the rest listed in `dups`."""
    now = time.time()
    files = []
    for name in sorted(os.listdir(inbox)):
        p = os.path.join(inbox, name)
        if not (os.path.isfile(p) and name.lower().endswith(".pdf")):
            continue
        if hours is not None and now - os.path.getmtime(p) > hours * 3600:
            continue
        files.append(p)
    groups = {}
    for p in files:
        groups.setdefault(rc.sha256(p), []).append(p)
    out = []
    for h, ps in groups.items():
        ps.sort(key=lambda x: (len(os.path.basename(x)), x))
        out.append({"path": ps[0], "name": os.path.basename(ps[0]), "sha": h, "dups": ps[1:]})
    return sorted(out, key=lambda x: x["name"])


def phrase_of(note):
    m = re.search(r"phrase ([0-9.]+)", note or "")
    return float(m.group(1)) if m else 0.0


def judge(f, e, head):
    """Verdict for one PDF against one missing entry: a dict or None (does not look like it)."""
    doi_hit = bool(e.get("doi")) and rc.norm_doi(e["doi"]) in (rc.dois_in(f["name"]) | rc.dois_in(head))
    ok, n, note = rc.verify(f["path"], e)
    if note.startswith("scanned(no-text)") or note.startswith("saved-UNVERIFIED"):
        # No text to read: only the file name (or a DOI in it) can identify the paper.
        stem = f["name"][:-4]
        sim = rc.title_sim(e.get("title", ""), {"ftoks": set(rc.toks(stem))})
        if doi_hit or sim >= rc.TITLE_GATE:
            tier = "verified" if doi_hit else "low"
            why = ("DOI match" if doi_hit else "file name title similarity %.2f" % sim) + ", " + note
            return {"tier": tier, "doi": doi_hit, "pages": n, "phrase": 0.0,
                    "note": ("LOW-CONFIDENCE " if tier == "low" else "") + why}
        return None
    if not ok:
        if doi_hit:  # right DOI, wrong content: supplement, erratum or wrong download; show it
            return {"tier": "mismatch", "doi": True, "pages": n, "phrase": phrase_of(note), "note": note}
        return None
    tier = "low" if "LOW-CONFIDENCE" in note else "verified"
    return {"tier": tier, "doi": doi_hit, "pages": n, "phrase": phrase_of(note), "note": note}


def rank(j):
    return (TIER_RANK[j["tier"]], 0 if j["doi"] else 1, -j["phrase"], -j["pages"])


def prefilter(f, e, head):
    """Cheap test to drop obviously unrelated pairs before the full content check."""
    if e.get("doi") and rc.norm_doi(e["doi"]) in (rc.dois_in(f["name"]) | rc.dois_in(head)):
        return True
    blob = (f["name"] + " " + head).lower()
    sur = rc.first_surname(e.get("author", ""))
    tt = rc.verify_toks(e.get("title", ""))
    ov = len([w for w in tt if w in blob]) / len(tt) if tt else 0
    return bool((sur and sur in rc.toks(blob)) or ov >= 0.3 or not head.strip())


def match(files, missing):
    """Returns (assign {key: (file, verdict)}, conflicts [(file, [(entry, verdict)])],
    mismatches [(file, entry, verdict)], unmatched [file])."""
    per_file = {}
    for f in files:
        head = rc.first_pages_text(f["path"])
        hits = []
        for e in missing:
            if not prefilter(f, e, head):
                continue
            j = judge(f, e, head)
            if j:
                hits.append((e, j))
        per_file[f["path"]] = hits
    assign, conflicts, mismatches, unmatched = {}, [], [], []
    for f in files:
        hits = per_file[f["path"]]
        good = [(e, j) for e, j in hits if j["tier"] != "mismatch"]
        for e, j in hits:
            if j["tier"] == "mismatch":
                mismatches.append((f, e, j))
        if not good:
            if not any(j["tier"] == "mismatch" for _, j in hits):
                unmatched.append(f)
            continue
        good.sort(key=lambda x: rank(x[1]))
        # Two equally good candidates for one PDF: do not choose for the author.
        if (len(good) > 1 and rank(good[0][1])[:2] == rank(good[1][1])[:2]
                and abs(good[0][1]["phrase"] - good[1][1]["phrase"]) < 0.1):
            conflicts.append((f, good))
            continue
        e, j = good[0]
        prev = assign.get(e["key"])
        if prev is None or rank(j) < rank(prev[1]):
            assign[e["key"]] = (f, j)
    return assign, conflicts, mismatches, unmatched


def library_name(e):
    """`<FirstAuthorSurname> <Year> - <Title>.pdf`, the form missing_refs.py can match."""
    sur = re.sub(r'[\\/*?"<>|:]', "", rc.surname(e.get("author", ""))).strip() or "Anon"
    head = ("%s %s" % (sur, e.get("year", ""))).strip()
    return "%s - %s.pdf" % (head, rc.clean_title(e.get("title", "")) or e["key"])


def to_library(lib_dir, src, sha, name, hashes):
    """Copy src into the library unless the same content or name is there.
    Returns ("added", name) or ("skipped", reason). `hashes` {sha: path} is updated."""
    if sha in hashes:
        return "skipped", "same content as %s" % os.path.basename(hashes[sha])
    dst = os.path.join(lib_dir, name)
    if os.path.exists(dst):
        return "skipped", "a file named %s already exists" % name
    os.makedirs(lib_dir, exist_ok=True)
    shutil.copy2(src, dst)
    hashes[sha] = dst
    return "added", name


def to_trash(path, trash):
    dst = os.path.join(trash, os.path.basename(path))
    if os.path.exists(dst):
        base, ext = os.path.splitext(os.path.basename(path))
        dst = os.path.join(trash, "%s %s%s" % (base, time.strftime("%H%M%S"), ext))
    shutil.move(path, dst)


def main():
    ap = argparse.ArgumentParser(description="File hand-downloaded reference PDFs: match them to "
                                             "missing .bib entries, verify the content, name them "
                                             "<citekey>.pdf, optionally add to your library and "
                                             "tidy the inbox.")
    ap.add_argument("--bib", required=True, help="BibTeX file")
    ap.add_argument("--pdfdir", default=rc.DEFAULT_PDFDIR,
                    help="project reference-PDF folder, files named <citekey>.pdf "
                         "(default: %s, the pdf_fetch.py default)" % rc.DEFAULT_PDFDIR)
    ap.add_argument("--inbox", default=os.path.join("~", "Downloads"),
                    help="folder where the PDFs were downloaded (default: ~/Downloads)")
    ap.add_argument("--hours", type=float, default=72, help="only files changed in the last N hours "
                                                            "(default: 72)")
    ap.add_argument("--all", action="store_true", help="no time limit")
    ap.add_argument("--apply", action="store_true", help="file the matches (default: preview only)")
    ap.add_argument("--library", metavar="DIR", default="", help="your personal PDF library")
    ap.add_argument("--to-library", action="store_true",
                    help="with --apply and --library: also copy each filed PDF into the library")
    ap.add_argument("--clean", action="store_true",
                    help="with --apply: move the filed source files (and identical duplicates) "
                         "to the Trash; nothing is deleted")
    a = ap.parse_args()
    if not os.path.isfile(a.bib):
        ap.error("bib file not found: %s" % a.bib)
    if a.clean and not a.apply:
        ap.error("--clean needs --apply (only successfully filed files are moved)")
    if a.to_library and not a.library:
        ap.error("--to-library needs --library DIR")
    if a.to_library and not a.apply:
        ap.error("--to-library needs --apply")
    trash = ""
    if a.clean:
        trash = trash_dir()
        if not trash:
            print("Refusing --clean: no Trash folder found (macOS: ~/.Trash; elsewhere: "
                  "~/.local/share/Trash/files). Nothing was changed; this tool never deletes files.")
            return 2
    inbox = os.path.expanduser(a.inbox)
    if not os.path.isdir(inbox):
        print("Inbox folder not found: %s" % inbox)
        return 2
    if not rc.have_pdftotext():
        print("Note: `pdftotext` (poppler) not found, so content checking is off: matches rely on "
              "DOIs and file names only and are marked accordingly.")
    os.makedirs(a.pdfdir, exist_ok=True)

    entries = rc.parse_bib(a.bib)
    have, _amb = rc.present_keys(entries, a.pdfdir)
    missing = [e for e in entries if e["key"] not in have]
    files = scan_inbox(inbox, None if a.all else a.hours)
    span = "all" if a.all else "last %g hours" % a.hours
    print("Missing %d | PDFs in %s (%s): %d (identical copies merged)\n" % (len(missing), inbox, span,
                                                                           len(files)))
    if not missing or not files:
        return 0

    assign, conflicts, mismatches, unmatched = match(files, missing)
    bykey = {e["key"]: e for e in entries}

    print("== Matched (%d) ==" % len(assign))
    for key, (f, j) in sorted(assign.items()):
        mark = "OK  " if j["tier"] == "verified" else "WARN"
        print("  [%s] %-26s <- %s | %s%s" % (mark, key[:26], f["name"][:50], j["note"][:70],
                                             " | DOI match" if j["doi"] else ""))
    if conflicts:
        print("\n== One file looks like several entries; not filed, you decide ==")
        for f, good in conflicts:
            print("  ? %s -> %s" % (f["name"][:50], ", ".join(e["key"] for e, _ in good[:3])))
    if mismatches:
        print("\n== DOI matches but the content does not (supplement, erratum, wrong file?); not filed ==")
        for f, e, j in mismatches:
            print("  x %s <-> %s | %s" % (f["name"][:50], e["key"], j["note"][:60]))
    if unmatched:
        print("\n== PDFs in the inbox that match no missing entry (%d, left alone) ==" % len(unmatched))
        for f in unmatched[:20]:
            print("  . %s" % f["name"][:70])
    still = [e["key"] for e in missing if e["key"] not in assign]
    print("\nStill missing after this run: %d%s" % (
        len(still), (": " + ", ".join(still[:12]) + (" ..." if len(still) > 12 else "")) if still else ""))

    if not a.apply:
        print("\n(Preview only. Add --apply to file%s.)" % (
            "; --library DIR --to-library to add them to your library; --clean to tidy the inbox"
            if assign else ""))
        return 0

    log = os.path.join(a.pdfdir, "_inbox_log.tsv")
    new_log = not os.path.exists(log)
    filed, lib_added, lib_skipped = [], [], []
    hashes = {}
    if a.to_library and os.path.isdir(a.library):
        hashes = {rc.sha256(p): p for p in rc.list_pdfs(a.library)}
    with open(log, "a", newline="", encoding="utf-8") as lf:
        lw = csv.writer(lf, delimiter="\t")
        if new_log:
            lw.writerow(["key", "source", "tier", "note"])
        for key in sorted(assign):
            f, j = assign[key]
            e = bykey[key]
            shutil.copy2(f["path"], rc.pdf_path(a.pdfdir, key))
            lw.writerow([key, f["name"], j["tier"], j["note"]])
            filed.append(f)
            if a.to_library:
                status, what = to_library(a.library, f["path"], f["sha"], library_name(e), hashes)
                (lib_added if status == "added" else lib_skipped).append((key, what))
    print("\nFiled %d PDF(s) into %s (log: %s)" % (len(filed), a.pdfdir, log))
    if a.to_library:
        print("Library: %d added, %d skipped" % (len(lib_added), len(lib_skipped)))
        for k, why in lib_skipped:
            print("   = %s skipped, already in library: %s" % (k, why[:60]))
    if a.clean:
        moved = 0
        for f in filed:
            for p in [f["path"]] + f["dups"]:
                if os.path.exists(p):
                    to_trash(p, trash)
                    moved += 1
        print("Moved %d file(s) from the inbox to the Trash (including identical copies; "
              "everything else untouched)" % moved)
    return 0


if __name__ == "__main__":
    sys.exit(main())
