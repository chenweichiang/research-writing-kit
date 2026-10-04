# Co-authored Manuscripts and Multi-team Proposals

> Applies when a co-author is the lead writer and you rewrite or polish their
> manuscript; when a proposal has a main project plus sub-projects written by
> different people; and whenever you edit someone else's text. A manuscript the author
> leads alone does not need this file.
>
> Where it comes from: an AI rewrite of a co-author's paper added a dozen statements
> the original never made, two of them claims about procedures that were never carried
> out (a three-dimension coding scheme that did not exist; an ethics paragraph
> describing the data as an existing course survey). The text read smoothly and was
> compatible with the original, which is exactly why nobody saw it until the
> co-author compared the two sentence by sentence.

## Three iron rules

1. **Never edit the original; write your changes as an edit layer.** The file a
   co-author sends is archived under its original name (`docs/received/YYYYMMDD-<source>/`,
   see `method/VERSIONING.md`); converted copies go in a build folder. Every change you
   make is one entry `(file, original text, replacement)` kept in an edit-list file and
   applied by a script.
   - The original text must occur **exactly once** in the target file; otherwise that
     entry fails and is listed. The script never guesses a location.
   - When the co-author sends a new version, re-convert and re-apply the edit layer.
     Entries that no longer match are the places they changed; decide each one again.
     Nothing fails silently.
   - The pay-off: at any point you can say who wrote a sentence, what you changed and
     why, and the co-author can read just the edit layer to see what you touched.

   A minimal applier is a few lines:

   ```python
   # edits = [("part2.md", "original sentence", "replacement"), ...]
   failed = []
   for path, old, new in edits:
       text = open(path, encoding="utf-8").read()
       if text.count(old) != 1:
           failed.append((path, old[:40], text.count(old)))
           continue
       open(path, "w", encoding="utf-8").write(text.replace(old, new))
   for f in failed:
       print("NOT APPLIED (found %d times): %s: %s" % (f[2], f[0], f[1]))
   ```

2. **Every sentence must trace back to a source.** Every sentence that states a fact, a
   method or the authors' claim must point back to the original manuscript, the
   co-author's replies, or the proposal. If it cannot, do not write it, or mark it as
   an open question for the co-author. Before handing anything back, run:

   ```bash
   python3 tools/collab/source_trace.py \
       --orig original.docx coauthor-replies.md proposal.pdf [analysis-report.md] \
       --draft new-draft.docx --report docs/source-trace.md --gate
   ```

   Fix every 🔴 (add the source or delete the sentence); send 🟠 (new literature
   claims) through citation verification; look at each 🟡 to confirm it adds no claim.
   Numbers that come from a re-analysis need that analysis report listed under
   `--orig`, or they will count as untraceable. "Traced" means the wording overlaps
   (character bigrams for Chinese, words for English); it is not proof that the meaning
   is the same, so the 🟡 and "rewritten" lines still need a human eye.

3. **Use their meaning; do not write for them.** Site details ("the industry mentor had
   already left"), the co-author's state of mind or design assumptions ("once students
   meet older adults, learning simply happens"), procedures they did not carry out: none
   of these get added. Additions are hard to spot precisely because they fit the
   original. Anything you would like to add becomes a question to the co-author, not a
   sentence in the text.

## The life cycle of an open question

An open question is a marker that someone has to answer before the text is final.
Markers that are not tracked pile up until submission day, when nobody remembers who
was supposed to answer them; markers removed without a record make it impossible to
tell whether the other person answered or you guessed.

| Stage | What to do |
|---|---|
| Open | Mark it visibly in the review copy (a Typst macro such as `#tbc[...]`; in Word, red text on a yellow highlight). Inside the marker write **who is asked, what, and why**, e.g. "to be confirmed by co-PI C: performance length; head count follows the 4 Oct revision notes". Log it in the project's question list (number, who, date) |
| Track | Every review copy reports how many open questions remain and who holds each. Questions for the same person go out as one list, not one at a time |
| Close | When the answer arrives, change the text, remove the marker, and log the closing date and the basis (the reply's file name or the person's words). **Never close one by guessing the answer.** A checkable fact (DOI, page number, statute article) may be closed after you verify it; the basis is the source you checked |
| Submit | The submission build hides markers with a switch, but hiding is not resolving: before submission the count must be 0, or each remaining one must have the author's explicit decision to leave it blank. `tools/regress/regress.py` rule R6 treats "to be confirmed" / 待確認 as a FAIL, so it works as the gate |

## Ownership table: who owns each section, figure and table

A multi-author document keeps one table (in the skeleton file or `docs/ownership.md`),
one row per unit:

| Unit | Lead writer | Your scope | Source file | Status |
|---|---|---|---|---|
| Part 2, sub-project 1 | Co-PI A | polish only (edit layer `edits_part2.py`) | docs/received/20261003-A/part2.docx | abstract awaiting A's confirmation |
| Figure 4-3 costume reference | Co-PI C | none | docs/received/20261004-C/ | final |

- Your scope is one of four: none / polish only / structural integration (moving,
  merging, renumbering) / new writing (only with the lead writer's consent).
- Check this table before touching someone else's unit; anything beyond "polish only"
  needs the lead writer's agreement first.
- Do not redraw someone else's figure unless they ask you to; what you would change
  becomes a question to them.
- The contribution statement at submission and the division-of-labour table in a
  proposal come straight from this table.

## Receiving and merging a version

1. Archive the received file under its original name in
   `docs/received/YYYYMMDD-<source>/`; never edit it there.
2. **Compare structure before wording.** Some co-authors rewrite the whole text instead
   of commenting, so sections and the order of arguments may have changed. Compare the
   structure (sections, figures and tables, list of claims) first, then the sentences.
   Ask early how each co-author works: comments, tracked changes, or full rewrites.
3. Update the ownership table; re-convert, re-apply the edit layer, and handle the
   entries that no longer match.
4. Run `source_trace.py`, the regression rules, and the language and de-AI checks (the
   "full polish" pass in the co-author skill).
5. Bump your own minor version (`method/VERSIONING.md`) and log "merged <source>'s MMDD
   version" in the CHANGELOG.

## Handing back to a co-author

- Bring it to a **submittable state** first; do not hand over a half-finished draft for
  the other person to pick through. A co-author who rewrites everything starts from
  exactly what you send.
- Attach three things: the version number and file names, the list of changes (the edit
  layer or a summary), and the list of open questions addressed to them.
- Never edit their original file directly, and never overwrite their shared cloud
  document.
