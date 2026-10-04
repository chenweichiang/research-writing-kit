#!/usr/bin/env python3
"""missing_refs.py: list the reference PDFs you still have to download by hand (stdlib only,
no network).

Why this exists: after pdf_fetch.py has run, some references remain (paywalled, books, no
open-access copy). Before asking you to download them, check what your own PDF library
already holds, otherwise the list contains papers you already own. This tool ties "check the
library first" and "write the list" into one step.

What it does:
  1. Reads the .bib and finds entries with no PDF in <pdfdir>: either <citekey>.pdf (what
     pdf_fetch.py writes) or a hand-filed name such as `NN [Author Year] Title.pdf`
     (matched by year + first-author surname + title similarity; an ambiguous match counts
     as present and is shown for a human to confirm).
  2. If --library DIR is given, matches each missing entry against the PDFs found under DIR
     (recursive) with three gates: same year in the file name, first-author surname in the
     file name, title similarity >= 0.55. One clear match = "confident" (not listed; copied
     into the project with --apply). Several close matches = "ambiguous" (not listed; shown
     for a human to pick). Library files should be named `<Surname> <Year> - <Title>.pdf`
     (inbox_ingest.py --to-library writes that form). Without --library this gate is
     skipped and the report says so.
  3. Writes what is left to <pdfdir>/_missing.md (for you to read: DOI / URL / ISBN links)
     and <pdfdir>/_missing.tsv (machine readable).

Next step: download the PDFs into ~/Downloads and run inbox_ingest.py to file them.

Usage:
  missing_refs.py --bib references.bib [--pdfdir refs-pdf] [--library ~/papers] [--apply]

The default is a dry run for the library copy; only the two list files are written.
"""
import argparse
import csv
import os
import shutil
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import refs_common as rc  # noqa: E402


def classify(missing, library):
    """Split missing entries into (confident, ambiguous, todo) using the library gates."""
    confident, ambiguous, todo = [], [], []
    for e in missing:
        kind, hit = rc.library_match(e, library)
        if kind == "confident":
            confident.append((e, hit))
        elif kind == "ambiguous":
            ambiguous.append((e, hit))
        else:
            todo.append(e)
    return confident, ambiguous, todo


def group_of(e):
    if e.get("doi"):
        return "doi"
    if e.get("isbn"):
        return "isbn"
    if e.get("url"):
        return "url"
    return "none"


def write_outputs(pdfdir, todo):
    groups = {"doi": [], "isbn": [], "url": [], "none": []}
    for e in todo:
        groups[group_of(e)].append(e)
    tsv = os.path.join(pdfdir, "_missing.tsv")
    with open(tsv, "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f, delimiter="\t")
        w.writerow(["key", "type", "author_year", "title", "doi", "isbn", "url"])
        for e in todo:
            w.writerow([e["key"], e.get("type", ""), rc.author_year(e), rc.delatex(e.get("title", "")),
                        e.get("doi", ""), e.get("isbn", ""), e.get("url", "")])
    md = os.path.join(pdfdir, "_missing.md")
    heads = {"doi": "With a DOI", "isbn": "Books (ISBN)", "url": "With a URL only",
             "none": "No DOI, ISBN or URL (search by title)"}
    with open(md, "w", encoding="utf-8") as f:
        f.write("# Full texts still to download (%d)\n\n" % len(todo))
        f.write("Entries already in your library are left out. Download into ~/Downloads, then run "
                "`inbox_ingest.py` to file them.\n\n")
        for g in ("doi", "isbn", "url", "none"):
            if not groups[g]:
                continue
            f.write("## %s (%d)\n\n" % (heads[g], len(groups[g])))
            for i, e in enumerate(groups[g], 1):
                ident = {"doi": "https://doi.org/%s" % e.get("doi", ""),
                         "isbn": "ISBN %s" % e.get("isbn", ""),
                         "url": e.get("url", ""), "none": ""}[g]
                f.write("%d. %s, \"%s\" %s\n" % (i, rc.author_year(e), rc.delatex(e.get("title", "")),
                                                 ident))
            f.write("\n")
    return groups, md, tsv


def main():
    ap = argparse.ArgumentParser(description="List the reference PDFs still to download, after "
                                             "subtracting what your own PDF library already has.")
    ap.add_argument("--bib", required=True, help="BibTeX file")
    ap.add_argument("--pdfdir", default=rc.DEFAULT_PDFDIR,
                    help="project reference-PDF folder, files named <citekey>.pdf "
                         "(default: %s, the pdf_fetch.py default)" % rc.DEFAULT_PDFDIR)
    ap.add_argument("--library", metavar="DIR", default="",
                    help="your personal PDF library (searched recursively); without it the "
                         "library check is skipped")
    ap.add_argument("--apply", action="store_true",
                    help="copy each confident library match into --pdfdir as <citekey>.pdf")
    a = ap.parse_args()
    if not os.path.isfile(a.bib):
        ap.error("bib file not found: %s" % a.bib)
    if a.apply and not a.library:
        ap.error("--apply copies from the library; give --library DIR")
    os.makedirs(a.pdfdir, exist_ok=True)

    entries = rc.parse_bib(a.bib)
    have, present_amb = rc.present_keys(entries, a.pdfdir)
    missing = [e for e in entries if e["key"] not in have]

    library = []
    if not a.library:
        print("Note: no --library given, so the list below was NOT checked against your own PDFs "
              "(it may be longer than needed).")
    elif not os.path.isdir(a.library):
        ap.error("library folder not found: %s" % a.library)
    else:
        library = rc.load_library(a.library)
        if not library:
            print("Warning: no PDFs found under %s; the library check removed nothing." % a.library)
    confident, ambiguous, todo = classify(missing, library)
    if present_amb:
        print("Present but ambiguous in %s (counted as present; confirm by hand):" % a.pdfdir)
        for k, names in sorted(present_amb.items()):
            print("   [%s] %s" % (k, " | ".join(names)))
        print()

    print("bib %d entries | PDF present %d | missing %d | library match %d | library ambiguous %d "
          "| to download by hand %d\n" % (len(entries), len(have), len(missing), len(confident),
                                          len(ambiguous), len(todo)))

    if confident:
        if a.apply:
            for e, L in confident:
                dst = rc.pdf_path(a.pdfdir, e["key"])
                if not os.path.exists(dst):
                    shutil.copy2(L["path"], dst)
            print("Copied %d PDF(s) from the library into %s" % (len(confident), a.pdfdir))
        else:
            print("In your library (%d; add --apply to copy them into the project):" % len(confident))
            for e, L in confident:
                print("   [%s] -> %s" % (e["key"], L["name"]))
    if ambiguous:
        print("\nAmbiguous library matches (pick by hand; not listed for download, not copied):")
        for e, Ls in ambiguous:
            print("   [%s] %s" % (e["key"], rc.delatex(e.get("title", ""))[:50]))
            for L in Ls:
                print("       ? %s" % L["name"])

    groups, md, tsv = write_outputs(a.pdfdir, todo)
    print("\nTo download by hand: DOI %d | books %d | URL only %d | nothing to go on %d" % (
        len(groups["doi"]), len(groups["isbn"]), len(groups["url"]), len(groups["none"])))
    print("List: %s\nTSV:  %s" % (md, tsv))


if __name__ == "__main__":
    main()
