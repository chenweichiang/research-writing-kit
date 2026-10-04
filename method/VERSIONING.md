# Versioning Manuscripts and Deliverables

> Applies to anything that is revised repeatedly and handed to other people: papers,
> grant proposals, applications, review reports, technical reports. Slide decks can
> keep plain SemVer (patch = typo, minor = content, major = overhaul); the meaning is
> compatible with this file.
>
> Why one scheme: left alone, every project grows its own convention, each one taught
> by a different accident ("major = number of submissions", "never print the version
> in the submitted PDF", "keep only one file in the latest folder", "print the version
> in the review copy's footer"). Scattered across project notes, none of them carries
> over to the next project. This file merges them. An existing project may keep its
> own **paths**; the **meaning** of the version number follows this file.
>
> Checker: `tools/versioning/version_check.py` (see the end of this file).

## The number: vX.Y.Z

| Part | Bump when | Example |
|---|---|---|
| X major | **the number of times it has been sent out.** 0 = never submitted; the first submission = 1.0.0; resubmission after review, or submission elsewhere after a rejection = next major | 0.14.1 becomes 1.0.0 on the day the proposal is submitted |
| Y minor | the content changed: argument, structure, sections added or removed, numbers, analysis, figures, references added or removed; a co-author's new version merged in | a new section, a re-run of the statistics, a replaced figure |
| Z patch | the meaning did not change: wording, typos, layout, citation order, formatting, an editor's change list applied line by line | a de-AI pass, citations renumbered by order of appearance |

- If you cannot tell which level a change belongs to, take the larger one.
- While revising after reviews, stay on the current major and bump minor (1.1.0,
  1.2.0, ...). **The version that is sent back** gets the next major (2.0.0).
- A two-part number (1.5) is an older habit; an existing project may keep it. New
  projects use three parts.

## Where the number lives

- **One source: a `VERSION` file** at the project root (or the manuscript folder),
  one line `X.Y.Z`, no `v`. The build script reads it and stamps the footer, the file
  name and the PDF metadata. **Never type the version into the manuscript text by
  hand**: a hand-typed number drifts away from `VERSION`.
- **Order**: decide the number and write the CHANGELOG entry first, then build.
  Writing the changelog after the build is how the delivered file and the record end
  up disagreeing.
- **A delivered number is never reused.** Once a version has been seen by anyone (the
  author, a co-author, a funder, a journal), any further change gets a new number. A
  git tag that has been pushed is not moved unless the author says so.

## CHANGELOG.md

Newest first, one section per version:

```markdown
## 1.2.0 (2026-10-12) Section 4 rewritten after reviews; Table 3 recomputed
- What changed (one line per item; for numbers, give the new and the old value)
- Basis: author's instruction (date, time, quoted) / ADJUDICATED A23 / reviewer point R2.4
- Sent to: co-author B (e-mail attachment)
```

- Heading format `## X.Y.Z (YYYY-MM-DD) one-line summary` (the `v` is optional);
  `version_check.py` reads the topmost section.
- For a version that was sent out, also record the **venue, manuscript ID and how it
  was sent**, and update the duplicate-submission ledger
  (`tools/submissions/check_submissions.py`).
- Every "basis" line points at something that can be found again: the author's words
  with a timestamp, an adjudication-ledger number, a reviewer-point number.

## Deliverables

- **File name** `<short-name>_vX.Y.Z.pdf` / `.docx`. When one version has several
  files, add a suffix: `_review` (with comments and the footer version), `_submission`,
  `_backtranslation`, `_tracked`. The recipient should know which version, and for
  whom, without opening the file.
- **Folders** (default for new projects; an existing project keeps its paths):
  - `latest/`: emptied on every delivery, holds only the current version's files. The
    author and co-authors look only here, so nobody opens the wrong version.
  - `versions/vX.Y.Z/`: a complete snapshot of each version; history lives here.
  - Chinese-language projects may use `最新交付/` and `版本/vX.Y.Z/`; the checker
    accepts either.
- **Word**: if the author or a co-author works in Word, deliver a .docx alongside. The
  PDF is the reference layout; the .docx is for people to edit.
- **Where the number is printed**:
  - the review copy's footer: "Review copy vX.Y.Z (YYYY-MM-DD)", so a reply can say
    which version it is about;
  - **the submitted version's text carries no version number** (a reviewer who sees
    "v0.29.1" assumes a half-finished draft). The number goes only in the file name and
    the PDF metadata (Keywords or Subject).
- **Closing every delivery**: rebuild, report the file paths and the version, and tag a
  version that was sent out with git tag `vX.Y.Z`.

## Receiving versions from others

A version that a co-author or the author sends back is stored under its original name
in `docs/received/YYYYMMDD-<source>/` and never edited there. After merging it, bump
your own minor version and write "merged <source>'s MMDD version" in the CHANGELOG.
The edit-layer and open-question rules for co-authored manuscripts are in
`method/COLLABORATION.md`.

## Check

```bash
python3 tools/versioning/version_check.py <project-or-manuscript-folder> \
    [--latest latest] [--submission manuscript_submission.pdf]
```

What it checks: `VERSION` is valid; the topmost CHANGELOG section has the same number;
`latest/` holds exactly one version and it is the one in `VERSION`; the delivered PDF's
metadata carries the number; the submission PDF's text has no version string; `VERSION`
was already tagged and there are changes after the tag (a delivered number being
reused). Run it before every delivery; fix every FAIL before handing anything over.
