---
name: submit
description: "The last mile before a paper, proposal or application goes out, and the wrap-up after it does. Readiness verdict (re-read the official page, convert the deadline to the author's timezone, scoring by a clean reviewer, never self-scored), Word delivery (build from source, round-trip text comparison, venue-style word count, author to-dos in a separate file), format diff against the official template docx, double-blind anonymization check (author fields, file properties, tracked changes, image EXIF), upload package and field checklist, then after submission: confirmation e-mail, submission record, ledger, calendar dates, major version bump and tag. Use when the author says: can I submit this, is it ready, score it, what is still missing, make the Word version, compare with the official template, does the format match the sample, anonymization check, prepare the upload, what time is the deadline in my timezone, I submitted it, wrap up. Drafting and draft-level checks: co-author (Phase 6); check without editing: paper-review; reviews came back: rebuttal."
---

# submit: readiness, Word delivery, wrap-up after sending

> Generated from the Research Writing Kit; adapt to the author.
> Why this exists: the last mile gets redone from scratch for every submission: each
> project grows its own throw-away script for the Word conversion; "can I submit?" is
> answered by the author of the draft, who scores it generously and measures the word
> limit the wrong way; the Word file goes out with author to-dos still inside it; the
> official sample docx is compared by eye; and after sending, the confirmation, the
> record and the decision date are filed differently each time. This fixes it as one line.
> It starts after the draft is written and the draft-level check is done. `co-author`
> owns "is the manuscript good"; this skill owns "is the file we are handing over correct,
> and is everything filed once it is sent".

Tools live in the kit's `tools/submit/` (the kit path is in the project `CLAUDE.md`).
**Mode:** `full` (tools installed, below) or `lite` (nothing installed; every mechanical
step has a "Lite:" note saying what Claude does by hand). Optional dependencies, all of
which degrade with a clear message instead of failing silently:

| Needs | For | If missing |
|---|---|---|
| `pandoc` | building the docx, `docx_roundtrip.py` | lite round-trip (read both files yourself) |
| `python-docx` | `template_diff.py`, empty-paragraph check | lite template diff |
| `exiftool` | image EXIF in `anon_check.py` | EXIF areas are reported as "not checked" |
| `PyMuPDF` | PDF files in `anon_check.py` | PDFs reported unreadable (exit 2) |
| macOS + Microsoft Word | exact `word_count.sh` | approximate count only (exit 3) |

## Iron rules

1. **Re-read the official page every time; never trust memory or an old copy in
   `venue-notes.md`.** Deadlines, word-count method, file formats, anonymization rules and
   AI-disclosure fields change. Read the official page, compare it with the project's
   `venue-notes.md`, and if anything changed, fix `venue-notes.md` first, then continue,
   and tell the author what changed.
2. **Never self-score.** "Can I submit?" and "what score would it get?" go to the named
   agent `clean-reviewer` (clean context, none of the writing discussion). The person who
   wrote the draft shares its blind spots; a self-given score will be generous and the word
   limit will be measured in the convenient way. Claude only collates.
3. **Count words the venue's way.** First find out what the venue counts: abstract,
   references, captions, tables, appendices, and whether CJK text counts characters or
   words. `word_count.sh` asks Word itself (macOS + Word only). Where Word is unavailable
   the only number available is approximate (exit 3), and it must be reported as
   **approximate**.
4. **Only the author uploads, fills in system fields, presses submit, signs or pays.**
   Claude prepares the files and the field checklist, and does the wrap-up afterwards.
5. **A delivered file carries no author to-dos.** No `【待確認】`, TODO, unresolved
   `[@key]`, or `??` inside it. Anything the author must do goes into a separate
   `author-todo.md`.

## 1. Readiness verdict ("can I submit this?")

1. Read the official page (rule 1). Convert the deadline to the author's timezone:
   ```bash
   python3 tools/submit/deadline.py "2026-10-26 23:59" --tz AoE [--to Europe/Paris]
   ```
   Prints the deadline in the target timezone (default: this machine's local timezone;
   `--to` takes an IANA name), the time remaining, and a suggested submit time 24 hours
   before the deadline. It accepts AoE, PST/PDT/EST/..., `UTC+8`, and IANA names. AoE is
   UTC-12, so in East Asia the deadline falls on the evening of the next day.
   *Lite:* do the arithmetic by hand and say so; state both the original and the converted
   time, check whether daylight saving applied on that date, and propose a submit time at
   least 24 hours earlier.
2. Run the mechanical checks that apply (sections 2 to 4): word count, Word round-trip,
   template diff, anonymization.
3. Hand `clean-reviewer` the manuscript path, `venue-notes.md`, the venue's scoring
   criteria (the official rubric or review form; if there is none, the venue's published
   review focus) and the project's `ADJUDICATED.md` (settled points are not re-raised).
   Ask for item-by-item scores against the rubric, each with a location in the manuscript.
4. Report in four fixed sections, no commentary:

   | Section | Content |
   |---|---|
   | **Hard requirements, one by one** | Every rule on the official page (word count, pages, format, file types, anonymization, declarations, attachments): meets / does not meet / could not find, with the measured value and how it was measured |
   | **Blockers** | What prevents submission if not fixed (over the limit, anonymity leak, missing mandatory declaration, template mismatch); write "none" if none |
   | **Only the author can do** | Signatures, payment, system fields, co-author consent, ethics approval number, membership proof ... itemized |
   | **Timeline** | Deadline (original timezone and the author's), suggested submit time, how long each item takes, by when the author must reply |

   Put `clean-reviewer`'s score and main weaknesses after the four sections, labelled as a
   simulated review, not the venue's result.

## 2. Word delivery

- **Build from the source, never hand-edit the docx.** The source (md / typ) is the single
  truth; change the source and rebuild, or the next version overwrites the hand edit. With
  pandoc, pass the venue template as `--reference-doc` when there is one, and use
  `--citeproc` with the venue's CSL for citations.
- **Round-trip comparison:**
  ```bash
  python3 tools/submit/docx_roundtrip.py source.md built.docx
  ```
  Both sides are converted to plain text and compared sentence by sentence ("in source,
  missing from docx" and "in docx, not in source"), then scanned for leftovers (`[@key]`,
  `??`, `【待確認】`, TODO, unreplaced `{{`, Word reference errors, runs of empty
  paragraphs). Deliver only on exit 0.
  *Lite:* convert the docx to text (any converter) and read it against the source
  section by section; grep the text for `[@`, `??`, `TODO`, `{{`, `【待確認】`.
- **Word count:** `bash tools/submit/word_count.sh built.docx [--pdf out.pdf]`.
  **macOS + Microsoft Word only**; it drives Word through osascript (the PDF option also
  goes through Word, saving inside Word's sandbox first, because saving straight outside
  hangs Word). Elsewhere it falls back to `wordcount_approx.py`, prints an approximate
  count and exits 3: report that number as approximate and tell the author to count in
  Word (or by the venue's own tool) before submitting.
  *Lite:* count by hand with the venue's rule and name the method; never present a rough
  estimate as the count.
- **Author to-dos go in a separate file**: `latest/author-todo.md`, each item giving where
  in the manuscript (section name plus the first few words of the sentence) and what the
  author has to do.
- File names follow `method/VERSIONING.md`: `<short-name>_vX.Y.Z_submission.docx`.

## 3. Template diff ("does the format match the sample?")

```bash
python3 tools/submit/template_diff.py manuscript.docx official-template.docx [--only-diff]
```

Compares paper size, margins, header and footer distance, default fonts (ascii and
eastAsia separately), font size, line spacing, space before and after, first-line indent,
alignment, and styles the manuscript uses that the template lacks. Limit: it compares
style definitions, not direct formatting on paragraphs; paragraphs formatted by hand need
a visual check. For each difference report "manuscript value / template value", fix the
source or the reference-doc, rebuild, and compare again until only deliberate differences
remain (write the reason for each). Exit 0 consistent, 1 differences.
*Lite:* open both in Word (or unzip and read `word/styles.xml` and `sectPr`), and compare
those same properties by hand; say which properties you did not check.

## 4. Anonymization (double-blind review only)

```bash
python3 tools/submit/anon_check.py review-copy.docx review-copy.pdf figures/ \
  --names "Jane Doe,Doe, J." \
  --affil "Example University,EU" \
  --extra "janedoe,example.org"
```

Checks the docx creator and lastModifiedBy, authors of tracked changes and comments, names
and affiliations in the body and in headers and footers, hyperlinks, PDF Author and XMP,
and the EXIF (author, GPS) of embedded images and image files. Add co-authors' names and
affiliations to the lists. The tool also reports a 🟢 list of what it actually checked and
says so loudly when it checked nothing (an "empty run" is not evidence of a clean file).
🔴 findings must all be cleared before delivery; 🟠 self-disclosure phrasing ("our previous
work (Doe, 2024)") is for the author to decide whether to rewrite in the third person.
Exit 0 no red, 1 red findings, 2 a file could not be read.
*Lite:* check by hand: File > Info > Inspect Document in Word (author fields, comments,
revisions), PDF properties, the text for names and affiliations, and the images' properties;
state that image EXIF was not machine-checked.

## 5. Upload package

Before sending, assemble in the project's `latest/` folder and report the full paths:

- Every file to be uploaded (names per the venue, or per VERSIONING), each with the first
  16 characters of its SHA-1 so they can be matched after submission.
- `submission-fields.md`: every field the system asks for (title, abstract, keywords,
  category, author data, declaration ticks, cover letter), written out field by field with
  the character limits beside them, for the author to paste.
- `author-todo.md` (section 2).
- Finally run the version check: `python3 tools/versioning/version_check.py <project>
  --submission <submission file>` (see `method/VERSIONING.md`).
*Lite:* compute hashes with `shasum`, and check the version rules in `method/VERSIONING.md`
by hand.

## 6. After submission (the author says "I submitted it")

1. **Find and file the confirmation e-mail.** Search every mailbox the system could have
   used, spam folder included; note sender, time, subject and manuscript ID. **If it
   cannot be found, tell the author and do not treat the paper as submitted.**
2. **Write a submission record**, `versions/v<new major>.0.0/submission-record.md` (next to
   that version's snapshot, `method/VERSIONING.md`), with:
   time of submission and who submitted; system URL and the login account (never the
   password); manuscript ID; track and keywords; uploaded file names with SHA-1; the author
   list as the system shows it, with the e-mail addresses used; the confirmation e-mail
   (sender, time, subject, receiving mailbox); whether the submission can still be edited
   before the deadline; the decision date.
3. **Version:** bump the major version as `method/VERSIONING.md` says (0.x becomes 1.0.0;
   a resubmission after review, 1.x becomes 2.0.0); if the content did not change, do not
   rebuild the PDF, write "content = vX.Y.Z" in the record; then `git tag vN.0.0` and push
   the tag.
4. **Submissions ledger:** set the entry to `submitted` with the date, then
   `python3 tools/submissions/check_submissions.py --ledger SUBMISSIONS.tsv` must show no
   🔴 (this is the duplicate-submission guard).
5. **Calendar:** put the decision date, the revision deadline and the registration deadline
   in the author's calendar, in the timezone of where the event takes place; write the
   manuscript ID and the announcement's original timezone in the description; read the
   events back after creating them.
6. **Project notes:** mark the project "submitted" in its notes (manuscript ID, decision
   date, "not to be sent elsewhere while under review").
7. Report: manuscript ID, which mailbox holds the confirmation, that the ledger and calendar
   are updated, the tag name, and the next date the author should watch.
*Lite:* every step here is manual anyway; Claude drafts the record from what the author
pastes in, and edits the ledger as text.

## Out of scope

- Writing and revising, the draft-level full check, AI-use and ethics declarations (their
  content) → `co-author` and `method/AI_DISCLOSURE.md`.
- Version numbers and the delivery folder rules → `method/VERSIONING.md`.
- Proofreading, reporting guidelines, statistical consistency → `paper-review`.
- Reviews came back, revision table → `rebuttal`; proofs and copyright after acceptance
  → `co-author` Phase 8.
