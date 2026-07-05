---
name: build-pdf
description: Turn a finished draft into a properly formatted PDF in the venue's layout. Use when the author says "make the PDF", "format this for submission", "typeset this", "build the paper". The deliverable is always a formatted PDF, never raw markdown (Iron Rule 7).
---

# build-pdf — typeset the deliverable

> Generated from the Research Writing Kit; adapt to the venue and the author's tools.
> Iron Rule 7: **the deliverable is a formatted PDF from version one**, matching the
> venue's official template or the author's past submitted layout. `skeleton.md` and
> draft markdown are internal working files, never handed over.

## Decide the layout source
1. **Official template** for the venue (e.g. an ACM/LaTeX class, a funder's form) →
   use it exactly.
2. **No official template** → measure the layout of the author's previously submitted
   PDFs (margins, font sizes, section styles, table style) and match it.
Record the layout spec in `venue-notes.md`.

## Build path (use what the author has)
- **LaTeX venues:** the official class (e.g. `acmart`), via LaTeX or Quarto.
- **General / Chinese / non-LaTeX:** a lightweight typesetting path (e.g. Typst or
  Quarto) that embeds the correct CJK/Latin fonts and matches the measured spec.
- **Lite / no toolchain installed:** guide the author to a minimal install, or produce
  the cleanest possible export and be explicit that layout still needs a final pass —
  don't pretend a raw markdown export is the submission.

## Check before handing over
Eyeball the PDF against the `venue-notes.md` layout spec: font sizes, margins, section
styles, tables, page/word limits. Layout is a review item — a citation-perfect draft in
the wrong format still fails.

## Second-language papers
Deliver the formatted paper **and** the formatted back-translation as a pair — the
back-translation PDF is the author's sign-off entry point (Iron Rule 3).
