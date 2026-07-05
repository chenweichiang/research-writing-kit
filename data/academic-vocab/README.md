# Academic vocabulary lists (word/phrase anchoring)

Reference word lists for `paper-review` Layer 3 (wording / academic diction). Three
open academic vocabulary lists, normalized to TSV — grep them locally. They are
**anchors, not auto-replace**: a word not in a list *may* be informal, but the final
call is always Claude reading the context, minimal-edit, with a quote.

Three complementary levels: **phrase templates** (a phrasebank, not bundled) / **ACL**
= collocations / **AVL, AWL** = single words.

## Files

| File | Content | Rows | Columns |
|------|---------|------|---------|
| `acl_collocations.tsv` | Academic **collocations** (phrasing) | 2,474 | `headword`, `collocation` |
| `avl_core_words.tsv` | Academic **core words** (diction), COCA academic sub-corpus | 3,014 | `rank`, `word`, `pos`, `coca_acad_freq`, `acad_ratio` (>1 = over-represented in academic text) |
| `awl_families.tsv` | Academic **word families** (Coxhead) | 570 | `headword`, `sublist` (1 = highest frequency), `related_forms` |

## Usage (paper-review Layer 3)

```bash
AV="$(dirname "$0")/../data/academic-vocab"   # or the repo's data/academic-vocab
# 1) Is a word an academic core word? (AVL) — not in the list + has an academic
#    synonym → possibly informal, suggest upgrading
grep -iP "^\d+\t(utilize|use|get|big)\t" "$AV/avl_core_words.tsv"
# 2) Is a phrase an academic collocation? (ACL) — check contribution/method phrases
grep -i "significant" "$AV/acl_collocations.tsv"
# 3) Which AWL sublist does a word family belong to?
grep -iP "^analyse\t" "$AV/awl_families.tsv"
```

## Sources & licensing

Redistributed here for **private, non-commercial, educational** use, with attribution.
These are third-party lists — not part of the kit's own code.

- **ACL** — Academic Collocation List, Ackermann & Chen (2013), from the Pearson
  International Corpus of Academic English (~25M words). Source: eapfoundation.com /
  Coventry University. Free for research/educational use.
- **AVL** — Academic Vocabulary List (core), Gardner & Davies (2014), COCA academic
  sub-corpus (~120M words). Source: academicvocabulary.info (Mark Davies, BYU). Free
  for research/educational use.
- **AWL** — Academic Word List, Coxhead (2000), Victoria University of Wellington.
  Licensed **CC BY-NC-ND 3.0** — attribution, non-commercial, no derivatives. The TSV
  here is a re-formatting for local grep; treat the word data as the original list and
  cite Coxhead (2000).

If you plan to share this kit beyond a private, non-commercial circle, review these
licenses (especially AWL's ND term) before redistributing the data.
