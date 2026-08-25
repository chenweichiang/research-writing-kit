#!/usr/bin/env python3
"""uncited_claims_scan.py — find sentences that make a claim but carry no citation
(deterministic, zero LLM).

Why: citation-verification pipelines walk citation MARKERS (\\cite / [@key] / (Author,
2024)) back to the sentence around them. A sentence with no marker never enters the
pipeline, so it is never checked — yet in design research and RtD the load-bearing
claims are exactly the author's own evidence: "17 student posters showed...",
"improved by 23%", "this is the first...". Those are the sentences most often
hallucinated or overstated, and this scan is the only thing that looks at them.

The tool does NOT judge whether a claim is true. It asks one question per sentence:
  "This sentence makes a claim that needs evidence and contains no citation —
   what do you intend to do about it?"

Three triggers (English + Traditional Chinese):
  quant   numbers / % / p-values / N= / effect sizes / CI / multiples / changes
  causal  causes / leads to / results in / 導致 / 造成 / 使得 / 促使 / 引發
  super   the first / the only / unprecedented / 首次 / 唯一 / 最早 / to our knowledge

Three dispositions per finding:
  (1) add a citation  (2) name your own data source (numbers ledger)  (3) soften the wording

Adjudicated sentences are silenced with a WAIVER so they do not come back next run:
  Markdown / qmd :  <!--uncited-ok: own data analysis/run3.csv-->
  LaTeX          :  % uncited-ok: own data analysis/run3.csv
Put the waiver at the end of the sentence's line, or alone on the next line.
The reason is mandatory; an empty waiver does nothing.

Usage:
  uncited_claims_scan.py --src paper.tex [--json report.json] [--only quant causal]
Exit codes: 0 = no unadjudicated findings; 1 = findings remain (usable as a delivery gate).

Zero-install: Python 3 standard library only.
"""
import argparse
import json
import os
import re
import sys

# ── Citation markers: any one of these means "cited" and the sentence is skipped ──
PARTICLE = r"(?:(?:von|van|der|den|de|du|da|di|dos|del|della|la|le|bin|ibn|ter|ten)\s+){0,2}"
CITE_PATTERNS = [
    r'\\(?:cite|citep|citet|citeauthor|citeyear|autocite|parencite|footcite|textcite)\s*(?:\[[^\]]*\])*\s*\{[^}]*\}',
    r'\[[^\]\n]*@[-\w:.]+[^\]\n]*\]',            # pandoc [@key] / [-@key; @key2]
    r'(?<![\w@])@[-\w:.]{2,}',                    # pandoc inline @key
    r'\[(?:\s*\d+\s*[,;–—-]?)+\]',                # numeric [1] [1,2] [1-3]
    r'\([^)]*[A-Z][^)]*,\s*(?:1[6-9]|20)\d{2}[a-z]?[^)]*\)',          # APA (Chen, 2026)
    # Chicago/Harvard author-year WITHOUT comma: (Dunne and Raby 2013), (Jansen 1990; Esparza 2013).
    # Without this pattern every such citation is reported as an uncited claim.
    # Surnames may carry lowercase particles (von Uexküll / van der Waals / de Certeau).
    r'\((?:' + PARTICLE + r'[A-Z][\w\'’.-]+(?:\s+(?:and|&)\s+' + PARTICLE + r'[A-Z][\w\'’.-]+)?'
    r'(?:\s+et\s+al\.?)?,?\s+(?:1[6-9]|20)\d{2}[a-z]?(?:\s*[;,]\s*)?)+[^)]{0,25}\)',
    r'(?<![@\w])[A-Z][\w\'’-]+(?:\s+(?:and|&)\s+[A-Z][\w\'’-]+|\s+et\s+al\.)?\s*\((?:1[6-9]|20)\d{2}[a-z]?\)',  # Chen et al. (2026)
    r'[（(][^）)]{0,30}[\u4e00-\u9fff]{2,}[^）)]{0,10}[，,]\s*(?:1[6-9]|20)\d{2}[^）)]{0,10}[）)]',  # （陳，2026）
    r'<!--\s*ref:[^>]+-->',
]
CITE_RE = re.compile('|'.join(CITE_PATTERNS))

# ── Claim triggers (pattern, trigger label) ─────────────────────────────────────
QUANT = [
    (r'\d+(?:\.\d+)?\s*\\?%', 'percentage'),          # tolerates LaTeX 32.5\%
    (r'百分之\s*[\d〇一二三四五六七八九十百]+', 'percentage'),
    (r'\bp\s*[<>=≤≥]\s*\.?\d', 'p-value'),
    (r'\b[Nn]\s*=\s*\d+', 'sample size'),
    (r"\b(?:Cohen'?s\s+d|η²|eta2|ω²|R²|R2|OR|RR|HR)\s*=\s*[-−]?\.?\d", 'effect size'),
    (r'(?<![A-Za-z])(?:d|g|r|β|beta)\s*=\s*[-−]?\s*\.?\d', 'effect size'),
    (r'\d+\s*%\s*CI|信賴區間', 'confidence interval'),
    (r'\d+(?:\.\d+)?\s*(?:倍|×|x)(?![\w])', 'multiple'),
    (r'(?:提升|下降|增加|減少|改善|降低)[^。！？]{0,12}\d+(?:\.\d+)?\s*[%倍]?', 'change magnitude'),
    (r'\b(?:improv|increas|decreas|reduc|outperform)\w*\b[^.!?]{0,25}\d+(?:\.\d+)?\s*%?', 'change magnitude'),
    (r'\d+(?:\.\d+)?\s*(?:ms|s|sec|min|hr)\b', 'measurement'),
    (r'\d+\s*(?:名|位|人|組|件|篇|次|個)(?:參與者|學生|受試者|作品|樣本|案例)?', 'count'),
    (r'\b\d+\s+(?:participants?|students?|subjects?|samples?|cases?|trials?)\b', 'count'),
]
CAUSAL = [
    (r'\b(?:causes?|caused|causing)\b', 'causes'),
    (r'\blead(?:s|ing)?\s+to\b', 'leads to'),
    (r'\bresult(?:s|ed|ing)?\s+in\b', 'results in'),
    (r'\bgives?\s+rise\s+to\b', 'gives rise to'),
    (r'\bbrought?\s+about\b', 'brings about'),
    (r'\b(?:因為|由於)[^。！？]{0,30}(?:導致|造成|使得|致使)', 'causal link (zh)'),
    (r'導致|造成|使得|致使|促使|引發|催生', 'causal verb (zh)'),
]
SUPER = [
    (r'\bthe\s+(?:first|only|largest|smallest|earliest|best|highest|lowest)\b', 'superlative'),
    (r'\bfor\s+the\s+first\s+time\b', 'first time'),
    (r'\bunprecedented\b|\bnever\s+before\b', 'unprecedented'),
    (r'\bto\s+(?:our|the)\s+knowledge\b|\bno\s+prior\s+work\b', 'to our knowledge'),
    (r'首次|首度|首見|最早|唯一|前所未有', 'first/only (zh)'),
    (r'據(?:我們|作者)?所知|尚無(?:相關)?研究|目前(?:仍)?沒有(?:任何)?研究', 'to our knowledge (zh)'),
    (r'(?:最大|最小|最佳|最高|最低|最重要)(?:的)?(?:一|之)?', 'superlative (zh)'),
]
CATEGORIES = [('quant', QUANT), ('causal', CAUSAL), ('super', SUPER)]

WAIVER_RE = re.compile(r'(?:<!--|%)\s*uncited-ok\s*:\s*(?P<reason>[^\n>]*?)\s*(?:-->|$)', re.M)
SKIP_HEADINGS = re.compile(
    r'^\s*(?:#{1,6}\s*)?(?:references?|bibliography|works\s+cited|參考文獻|引用文獻|附錄|acknowledg\w*|致謝)\s*$',
    re.I)


def mask(text, pattern, flags=0):
    """Replace matches with same-length blanks so offsets and line numbers survive."""
    return re.sub(pattern, lambda m: re.sub(r'[^\n]', ' ', m.group(0)), text, flags=flags)


def mask_balanced(text, head_pattern):
    """Mask the brace-balanced argument group after head_pattern (regex cannot nest).
    Needed for \\begin{longtable}[]{>{\\raggedright}p{\\real{0.13}}...} column specs,
    whose decimals would otherwise read as quantitative claims."""
    out, pos = [], 0
    for m in re.finditer(head_pattern, text):
        if m.start() < pos:
            continue
        i = m.end()
        while i < len(text) and text[i] not in '{':
            if text[i] not in ' \t':
                break
            i += 1
        if i >= len(text) or text[i] != '{':
            continue
        depth, j = 0, i
        while j < len(text):
            if text[j] == '{':
                depth += 1
            elif text[j] == '}':
                depth -= 1
                if depth == 0:
                    break
            j += 1
        seg = text[m.start():j + 1]
        out.append(text[pos:m.start()])
        out.append(re.sub(r'[^\n]', ' ', seg))
        pos = j + 1
    out.append(text[pos:])
    return ''.join(out)


def strip_noise(raw, tex=False):
    """Mask regions that must not be scanned (same-length, offsets preserved):
    comments, code, display math, bibliography, figure paths, table column specs."""
    t = raw
    # Waivers are metadata, not manuscript: mask them FIRST or their reason text gets
    # scanned (it can trigger findings of its own and shifts sentence splitting, so line
    # numbers drift by one after each waiver is added).
    t = mask(t, WAIVER_RE.pattern, re.M)
    # Ordinary HTML comments are masked too — comment text is not delivered prose, yet
    # "99%" or "first ever" inside a comment would count. `<!--ref:...-->` is a parsed
    # citation marker (CITE_PATTERNS) and must survive; waivers were handled above.
    t = re.sub(r'<!--(?!\s*(?:ref:|uncited-ok))[\s\S]*?-->',
               lambda m: ''.join('\n' if c == '\n' else ' ' for c in m.group(0)), t)
    t = mask(t, r'(?s)^---\n.*?\n---\n')                                  # YAML frontmatter
    t = mask(t, r'(?s)```.*?```')                                          # fenced code
    t = mask(t, r'(?s)\\begin\{(verbatim|lstlisting|minted|Verbatim)\}.*?\\end\{\1\}')
    t = mask(t, r'(?s)\\begin\{(equation|align|gather|multline|eqnarray)\*?\}.*?\\end\{\1\*?\}')
    t = mask(t, r'(?s)\$\$.*?\$\$')                                        # display math = definitions
    # Inline math must NOT be masked wholesale: in this genre the statistics live inside
    # it ($p < .001$, $N = 40$, $r = 0.86$). Masking it would wave through exactly the
    # claims that most need a source (measured: same paper, .qmd reported 4 findings,
    # the pandoc .tex with \(...\) reported 15 — the lower number was the wrong one).
    # So only the delimiters become blanks; content and offsets stay.
    t = re.sub(r'\\[()\[\]]', '  ', t)                                     # \( \) \[ \] → 2 blanks
    t = re.sub(r'(?<!\\)\$', ' ', t)                                       # $ → 1 blank
    t = mask(t, r'(?s)\\begin\{thebibliography\}.*?\\end\{thebibliography\}')
    if tex:
        # LaTeX comments (\% is not one). Only for .tex: in markdown `%` is literal, and
        # masking to end-of-line there ate every "23%" and glued sentences together.
        t = mask(t, r'(?m)(?<!\\)%.*$')
    t = mask(t, r'\\(?:includegraphics|input|include|label|ref|url|href)\s*(?:\[[^\]]*\])?\{[^}]*\}')
    t = mask(t, r'!?\[[^\]]*\]\([^)]*\)')                                  # markdown images / links
    t = mask_balanced(t, r'\\begin\{(?:longtable|tabular\*?|tabularx|array)\}(?:\[[^\]]*\])?(?:\{[^{}]*\})?')
    t = mask(t, r'>\{[^{}]*(?:\{[^{}]*\}[^{}]*)*\}')                       # leftover >{...} column modifiers
    return t


def section_index(text):
    """[(offset, section name)] so every finding can say which section it is in."""
    out = []
    for m in re.finditer(r'(?m)^\s*(?:#{1,6}\s+(?P<md>.+?)\s*$|\\(?:sub)*section\*?\{(?P<tex>[^}]*)\})', text):
        name = re.sub(r'\s+', ' ', (m.group('md') or m.group('tex') or '')).strip()
        out.append((m.start(), name))
    return out


def section_at(idx, offset):
    name = '(preamble / no section)'
    for off, nm in idx:
        if off <= offset:
            name = nm
        else:
            break
    return name


# Sentence splitting: protect abbreviations and decimal points first
PROTECT = [(r'\b(?:et\s+al|e\.g|i\.e|cf|vs|Fig|Tab|Eq|Dr|Prof|approx|resp)\.', '\x00'),
           (r'(?<=\d)\.(?=\d)', '\x01')]


def split_sentences(text):
    """[(start_offset, sentence)] — works for mixed English / Chinese text."""
    t = text
    for pat, ph in PROTECT:
        t = re.sub(pat, lambda m: m.group(0).replace('.', ph), t)
    spans, start = [], 0
    for m in re.finditer(r'(?:(?<=[.!?])\s+(?=[A-Z\u4e00-\u9fff\\])|(?<=[。！？；])\s*|\n{2,})', t):
        end = m.start()
        if end > start:
            spans.append((start, end))
        start = m.end()
    if start < len(t):
        spans.append((start, len(t)))
    out = []
    for s, e in spans:
        seg = text[s:e]
        if seg.strip():
            out.append((s, seg))
    return out


def waived_lines(raw):
    """{line_no: reason}.

    A waiver that unconditionally covered "the previous line" silenced a whole
    paragraph in one-paragraph-per-line .tex/.md files (measured: a waiver on L13
    silently waived two findings on L12). So:
      - waiver ALONE on a line  -> waives that line and the previous one
      - waiver at END of a line -> waives that line only"""
    lines = raw.split('\n')
    w = {}
    for m in WAIVER_RE.finditer(raw):
        reason = (m.group('reason') or '').strip()
        if not reason:
            continue  # empty waiver is inert
        line = raw.count('\n', 0, m.start()) + 1
        w[line] = reason
        body = WAIVER_RE.sub('', lines[line - 1]).strip() if line - 1 < len(lines) else ''
        if not body:
            w.setdefault(line - 1, reason)
    return w


def scan(path, only=None):
    raw = open(path, encoding='utf-8').read()
    clean = strip_noise(raw, tex=path.lower().endswith(('.tex', '.latex')))
    secs = section_index(clean)
    # Headings are not claims but glue onto the next sentence (single newline after
    # them). Index sections first, then mask headings same-length.
    clean = mask(clean, r'(?m)^\s*#{1,6}\s+.*$')
    clean = mask_balanced(clean, r'\\(?:sub)*section\*?')
    waivers = waived_lines(raw)
    wanted = set(only) if only else {c[0] for c in CATEGORIES}

    findings, stats = [], {'sentences': 0, 'cited': 0, 'triggered': 0, 'waived': 0}
    for off, sent in split_sentences(clean):
        off += len(sent) - len(sent.lstrip())   # line number of the first real char
        s = sent.strip()
        if len(s) < 8 or SKIP_HEADINGS.match(s):
            continue
        stats['sentences'] += 1
        if CITE_RE.search(sent):
            stats['cited'] += 1
            continue  # cited: the citation-verification line owns it
        hits = []
        for key, pats in CATEGORIES:
            if key not in wanted:
                continue
            for pat, tname in pats:
                m = re.search(pat, sent, re.I)
                if m:
                    hits.append({'category': key, 'trigger': tname, 'match': m.group(0).strip(),
                                 'span': [off + m.start(), off + m.end()]})
                    break  # first trigger per category; avoids flooding one sentence
        if not hits:
            continue
        stats['triggered'] += 1
        line = clean.count('\n', 0, off) + 1
        waiver = waivers.get(line)
        if waiver:
            stats['waived'] += 1
        findings.append({
            'id': f'UC{len(findings) + 1:03d}', 'line': line,
            'section': section_at(secs, off),
            'categories': sorted({h['category'] for h in hits}),
            'triggers': hits,
            'text': re.sub(r'\s+', ' ', s)[:400],
            'waived': bool(waiver), 'waiver_reason': waiver,
        })
    return {'source': os.path.abspath(path), 'stats': stats, 'findings': findings}


def report(res):
    st, fs = res['stats'], res['findings']
    open_f = [f for f in fs if not f['waived']]
    print(f"# Uncited-claim scan: {os.path.basename(res['source'])}")
    print(f"sentences {st['sentences']} | cited {st['cited']} | triggered {st['triggered']} "
          f"| waived {st['waived']} | OPEN {len(open_f)}\n")
    waived_f = [f for f in fs if f['waived']]
    if waived_f:
        # List waivers one by one: a single waiver silencing several findings must stay visible.
        print("## Waived (listed so no waiver silently covers a whole paragraph)")
        for f in waived_f:
            print(f"  [{f['id']}] L{f['line']} \"{f['waiver_reason']}\" <- {f['text'][:70]}")
        print()
    if not open_f:
        print("[OK] no unadjudicated uncited claims.\n")
        return
    cur = None
    for f in open_f:
        if f['section'] != cur:
            cur = f['section']
            print(f"\n## {cur}")
        cats = ' '.join(f"[{c}]" for c in f['categories'])
        trig = ', '.join(f"{h['trigger']} \"{h['match']}\"" for h in f['triggers'])
        print(f"\n[WARN] {f['id']} L{f['line']} {cats}  trigger: {trig}")
        print(f"  {f['text']}")
    print("\n---\nDisposition, one per finding: (1) add a citation  (2) name your own data "
          "source (numbers ledger)  (3) soften the wording")
    print("Then waive the line (reason mandatory):")
    print("  Markdown/qmd  <!--uncited-ok: own data analysis/run3.csv-->")
    print("  LaTeX         % uncited-ok: own data analysis/run3.csv\n")


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('--src', required=True, help='manuscript: .tex / .qmd / .md / .txt')
    ap.add_argument('--json', help='write the JSON report here')
    ap.add_argument('--only', nargs='*', choices=['quant', 'causal', 'super'],
                    help='report only these categories (default: all)')
    ap.add_argument('--quiet', action='store_true', help='no text report (JSON only)')
    a = ap.parse_args()

    res = scan(a.src, a.only)
    if not a.quiet:
        report(res)
    if a.json:
        with open(a.json, 'w', encoding='utf-8') as fh:
            json.dump(res, fh, ensure_ascii=False, indent=2)
        print(f"JSON -> {a.json}")
    return 1 if any(not f['waived'] for f in res['findings']) else 0


if __name__ == '__main__':
    sys.exit(main())
