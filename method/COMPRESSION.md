# Cutting a Manuscript Down to a Page or Word Limit

> Applies when a paper, proposal or application is over its page or word limit, or has
> zero slack and still needs new text.
>
> Compression rarely fails by cutting too little. It fails by cutting in the wrong
> place: shrinking a figure until its labels are 3 pt, trading away evidence for a
> page, or deleting a few words here and there that the end-of-paragraph white space
> simply absorbs.

## 0. Read how the limit is counted, then measure the real overrun

Every venue counts differently. **Read the call or the author guidelines in the
original**, and write the counting rule and the date you read it into the venue notes
(`templates/venue-notes.template.md`). Rules that have been misread in practice:

| Kind of rule | Example (as read in 2026-10; re-read the current version) | The misreading |
|---|---|---|
| A page limit that includes parts you might assume are exempt | A national teaching-research grant: 25 pages excluding the cover, **including** the PI's own section, references and appendices | Assuming the PI section did not count |
| A total page limit with fixed typography | A national research grant: 12 pt, single line spacing, 2 cm margins, 60 pages including references | None, but the typography is part of the limit |
| A printed-page limit that differs from the submission length | A design journal: 24 printed pages is the hard ceiling; the submitted file is counted differently | Cutting evidence to hit a number the editor would have accepted with a one-line note in the cover letter |
| An all-inclusive word count where figures count by area | Intellect journals: abstract, notes, references and bio all count; a figure counts by the space it takes, 400 words for a full page and 200 for a half page | Counting every figure as 400 words, which nearly doubled the apparent overrun |
| An all-inclusive word count | RPTEL: 10,000 words including everything | None |
| No hard limit | Taylor & Francis (some journals): no ceiling, but state the word count | None |

The formatting rules (font size, line spacing, margins) are part of the limit: **never
go below the required size or spacing to gain a page.** Adjust only inside what the
rules allow.

## 1. Measure, and find the pinned boundaries

- Total pages, how many lines are left on the last page, pages per section, word or
  character counts. One command shows where the large empty areas are:
  ```bash
  n=$(pdfinfo draft.pdf | awk '/^Pages/{print $2}'); for i in $(seq 1 $n); do printf "p.%s %s\n" $i "$(pdftotext -f $i -l $i draft.pdf - | wc -m)"; done
  ```
- **Find what is pinned**: a table that cannot break across pages, a full-page figure,
  a Gantt chart, a forced page break before a section. Savings before such a boundary
  only enlarge the gap on the page before it; they never reach the pages after it. In
  one proposal, splitting figures and tables still left 6 lines over; changing the body
  line spacing and the table font size did **nothing**, because a full-page figure, an
  unsplittable Gantt chart and the start of the references were all pinned. What
  finally absorbed it was the references-and-appendix font size, within the allowed
  range.
- In another manuscript the bottom of one page was a single table row that could not
  break; saving one line before it was absorbed, and only saving two or more pulled the
  next row up. So first compute **how much has to go for one page to actually
  disappear**, not "as much as possible".

## 2. A budget per section

Give the author one table and compress against it:

| Section | Now | Budget | Difference | Basis |
|---|---|---|---|---|
| PI's own section | 1.5 pp | 3 pp | +1.5 | worth 20 points in the scoring; the best return per page |
| Literature review | 5 pp | 4 pp | -1 | venue norm; two paragraphs unrelated to the research question |

- Allocate by **scoring weight** (proposals) or **venue expectation** (papers: look at
  the share of methods and results in published papers from the same venue), not
  evenly.
- Some sections should **grow** (heavily weighted, currently squeezed). Compression is
  reallocation, not only deletion.

## 3. Cut by level of impact (light first; use up a level before the next)

| Level | What | Example |
|---|---|---|
| 0 Layout only (no text change) | short last lines of paragraphs holding one or two words, wrapped table cells, reference and appendix font size within the rules, figure and table placement | the usual first pass on a zero-slack manuscript |
| 1 Repetition and scaffolding | things said twice, preview and transition sentences, "this study / this paper" metadiscourse, parenthetical asides, lists that can be merged | |
| 2 Move to supplementary material or an appendix | secondary tables, item-by-item detail, robustness-check details (the text keeps one sentence of result and a pointer) | a secondary table moved to the supplement, one sentence left in the text |
| 3 Secondary points and secondary references | the argument furthest from the research question; the third and later citations for one claim | only with the author's agreement |

**Never cut:**

- The core claim, load-bearing evidence and load-bearing numbers, the methods detail
  the design needs, ethics and AI-use statements, wording the author has already ruled
  on (check `ADJUDICATED.md`). Explaining the length in the cover letter is better than
  trading evidence for a page.
- 🔴 **Do not shrink figures.** A figure shrunk to 40 % of the column to save a page
  ended up with roughly 3 pt axis labels; the author's reaction was "I can't read
  figure 1 any more", and it had to be redrawn. Text inside a figure stays at 6 pt or
  the venue's minimum; run `tools/figures/figure_check.py` after every compression.
- Never go below the required font size, line spacing or margins.

**Cut in blocks.** A few words deleted here and there are swallowed by the white space
at the end of each paragraph. Delete a whole paragraph, or enough of one that it loses
a line, or the saving is not real.

## 4. Report every cut

One row per cut; the whole table goes to the author with the delivery:

| # | Where | What was cut or moved | Level | Saved | Running total |
|---|---|---|---|---|---|
| 1 | 3.2, second paragraph | two sentences repeating the definition from 2.1 | 1 | 2 lines | 2 lines |
| 2 | Table 6 | whole table moved to supplement S-15, one sentence left | 2 | 0.6 pp | 0.7 pp |

"Saved" is measured on the rebuilt file, in actual lines or pages, never estimated.

## 5. Rebuild and verify

1. Rebuild; check the total pages and the lines on the last page; confirm the pinned
   boundary actually moved.
2. Run the project's gates and regression rules (`tools/regress/regress.py`, the
   doc-regress rules); every pointer to moved content must resolve.
3. Run `tools/figures/figure_check.py` for shrunk figures and broken references.
4. Recount every field with its own limit (an abstract at 498 of 500 characters is
   one edit away from failing).
5. Content deleted: bump the minor version. Layout only: bump the patch version
   (`method/VERSIONING.md`). Attach the table from section 4 to the CHANGELOG entry.

## 6. When it will not fit

Give the author the remaining difference and the options: which section to cut, what
to move to an appendix, a note in the cover letter, or a different venue. **Never cut
the core claim or evidence on your own.**

## Adding text to a manuscript with zero slack

Some manuscripts sit exactly at the limit: 135 added characters pushed a page over, and
more than about eight characters before one figure moved it to the next page. On such
a manuscript every addition needs **an equal cut**, and the file is rebuilt right after
each addition to check the page count. An abstract placed at the end (a second-language
abstract, for example) is the part most often forgotten when a number changes, and the
part most likely to change the last page.
