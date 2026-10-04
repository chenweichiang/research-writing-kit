#!/usr/bin/env python3
"""figure_check.py: pre-flight check of figures and tables in a typeset PDF.

Why: a figure or table error never fails the build; it shows up when a reader opens the
PDF. A figure shrunk to fit a page limit ended up with ~3 pt axis labels and nobody noticed
until the editor did; a figure pasted into body-text styling picked up a first-line indent
and lost its right border; caption numbers drift away from the in-text references after
paragraphs are moved. This checks what a machine can check and crops the rest to PNG for a
human (or a vision model) to look at.

Mechanical checks:
  1. Caption numbering (Figure/Fig./Table, and Chinese 圖/表): gaps and duplicates
  2. A page with a figure caption but no figure (neither raster nor vector)
  3. Body text mentions "Figure N" with no such caption; a caption never mentioned in the body
     (references are matched on page text joined across line breaks; plural forms such as
     "Figures 1, 2, and 5" count; "附錄表 3" is an appendix label, not a reference)
  4. Figure off the page or within 6 pt of the paper edge = red; ink bbox (image white margins
     ignored, clipped vector patterns ignored) wider than the text column by more than 8 pt =
     yellow (the column is estimated from body lines of the whole document; colour boxes often
     add 4-6 pt of padding)
  5. Smallest font inside a vector figure < 6 pt = red; raster effective resolution < 200 dpi
     = yellow (blurry in print)
  6. White-background raster charts with effective dpi > 600 look shrunk (the text inside a
     raster cannot be measured, so the font size is estimated assuming 300 dpi output);
     >= 900 dpi and narrower than 60% of the column = red

Review material: with --out, every figure is cropped to PNG (caption included, 150 dpi)
together with _review_checklist.md for whoever looks at the images (text touching lines or
boxes, clipped text, legends covering data, font size small relative to body text, missing
CJK glyphs rendered as boxes; colour-only distinctions are a job for figure_a11y.py).

Requires: pymupdf.

Usage: figure_check.py paper.pdf [--out figcheck/] [--min-pt 6] [--min-dpi 200] [--json]
Exit code: 0 = no red findings; 1 = at least one red finding; 2 = pymupdf missing
"""
import argparse, json, os, re, statistics, sys

try:
    import pymupdf as fitz
except ImportError:
    try:
        import fitz  # older package name
    except ImportError:
        print("figure_check.py needs PyMuPDF: pip install pymupdf", file=sys.stderr)
        sys.exit(2)

# Caption = number followed by ":" / full-width colon / "." / ideographic space / two spaces / end of line
CAP = re.compile(r"^\s*(圖|表|Figure|Fig\.|Table)\s*([0-9]+(?:[-–][0-9]+)?)(?:[：:．]|\.(?!\d)|\u3000|\s{2,}|$)")
# A number followed by a single ASCII space ("表 3 Title") needs a look at the next word: verbs,
# particles and conjunctions mean body text ("表 5 因此不是…"); English lower case means body text
# ("Table 1 lists"), capitalised means caption.
CAP_LOOSE = re.compile(r"^\s*(圖|表|Figure|Fig\.|Table)\s*([0-9]+(?:[-–][0-9]+)?) (\S+)")
PROSE_HEAD = re.compile(r"^(是|為|列出|列舉|顯示|呈現|所示|中的|中，|可見|可以|將|則|因此|因為|也|即|指出|說明|裡|之中|把|對照|再|還|並|都|就|已|和|及|或|與|跟|的|[，、。；：）)])")  # single 中/各/上 are not listed: "表 3 中文構式" and "表 2 各組平均" are captions


def expand_nums(s):
    """'1, 2, and 5' -> 1 2 5; '2–4' -> 2 3 4."""
    out = []
    for a, b in re.findall(r"(\d+)(?:\s*[–-]\s*(\d+))?", s):
        out += [str(n) for n in range(int(a), int(b) + 1)] if b and int(b) - int(a) < 30 else [a]
    return out


def caption(text):
    """Is this line a caption? If so return (kind, number)."""
    if len(text) >= 160:
        return None
    m = CAP.match(text)
    if m:
        return KIND[m.group(1)], m.group(2)
    m = CAP_LOOSE.match(text)
    if not m or "。" in text:
        return None
    head = m.group(3)
    if m.group(1) in ("圖", "表"):
        return None if PROSE_HEAD.match(head) else (KIND[m.group(1)], m.group(2))
    return (KIND[m.group(1)], m.group(2)) if head[:1].isupper() else None


REF = re.compile(r"(?<![附續錄])(圖|表|Figure|Fig\.|Table)\s*([0-9]+(?:\s*[-–]\s*[0-9]+)?)(?!\s*[,，]\s*pp?\.)")  # "Table 1, p. 318" cites another work's table
REF_PL = re.compile(r"\b(Figs\.|Figures|Tables)\s*(\d+(?:(?:\s*(?:,|and|&|–|-)\s*)+\d+)*)")  # "Figs. 1 and 2", "Figures 1, 2, and 5", "Tables 2–4"
KIND = {"圖": "圖", "Figure": "圖", "Fig.": "圖", "表": "表", "Table": "表",
        "Figs.": "圖", "Figures": "圖", "Tables": "表"}
NAME = {"圖": "Figure", "表": "Table"}   # kind key -> word used in messages


def lines_of(page):
    out = []
    for b in page.get_text("dict")["blocks"]:
        for l in b.get("lines", []):
            spans = l["spans"]
            text = "".join(s["text"] for s in spans).strip()
            if text:
                out.append({"text": text, "bbox": fitz.Rect(l["bbox"]),
                            "size": max(s["size"] for s in spans)})
    return out


def body_column(doc, page_lines=None):
    """Left and right edge of the body column, estimated over the whole document: lines at the
    body font size (mode) wider than 40% of the page, taking the mode of their left and right
    edges. Estimating page by page gets pulled off by narrow text (captions beside figures,
    table cells) and flagged a full-width figure as 196 pt too wide."""
    lines = [l for pl in (page_lines or [lines_of(p) for p in doc]) for l in pl]
    if not lines:
        return None
    body = statistics.mode(round(l["size"], 1) for l in lines)
    w = doc[0].rect.width
    wide = [l["bbox"] for l in lines if round(l["size"], 1) == body and l["bbox"].width > w * 0.4]
    if len(wide) < 5:
        return None
    return (statistics.mode(round(r.x0) for r in wide), statistics.mode(round(r.x1) for r in wide), body)


def visible_drawings(page):
    """Visible extent of vector drawings = path bbox intersected with the clip it sits under.
    matplotlib hatching is a set of pattern tiles; get_drawings() reports the unclipped tiles, so
    a bar chart was measured at 94-581 pt and falsely flagged 100 pt over the column. With
    extended=True the clip (scissor rectangle) and the nesting level come back; a clip applies
    to later paths with a larger level."""
    out, stack = [], []          # stack: [(level, scissor or None)]
    for d in page.get_drawings(extended=True):
        lv = d.get("level", 0)
        while stack and stack[-1][0] >= lv:
            stack.pop()
        if d["type"] in ("clip", "group"):
            stack.append((lv, fitz.Rect(d["scissor"]) if d["type"] == "clip" and d.get("scissor") else None))
            continue
        x0, y0, x1, y1 = d["rect"]
        for _, sc in stack:      # intersect by hand: PyMuPDF's & returns zero-height lines (axes, gridlines) unchanged
            if sc is not None:
                x0, y0, x1, y1 = max(x0, sc.x0), max(y0, sc.y0), min(x1, sc.x1), min(y1, sc.y1)
        if x0 <= x1 and y0 <= y1:
            out.append(fitz.Rect(x0, y0, x1, y1))
    return out


def ink_bbox(page, rect, dpi=36, white=245):
    """Extent of actual ink: render the region at low resolution and trim near-white edges.
    When an image file carries its own white margin the frame is wider than the content; every
    photo in one manuscript overshot the column by 11 pt until the margins were trimmed."""
    pix = page.get_pixmap(clip=rect, dpi=dpi, colorspace=fitz.csRGB, alpha=False)
    w, h, buf = pix.width, pix.height, pix.samples
    if not w or not h:
        return rect
    stride = pix.stride
    xs = [x for x in range(w) if any(min(buf[y * stride + 3 * x: y * stride + 3 * x + 3]) < white for y in range(0, h, 2))]
    if not xs:
        return rect
    s = rect.width / w
    return fitz.Rect(rect.x0 + xs[0] * s, rect.y0, rect.x0 + (xs[-1] + 1) * s, rect.y1)


def white_ratio(page, rect, dpi=24, white=245):
    """Share of near-white pixels. Charts (white background, lines, text) are mostly above half;
    photos mostly below."""
    pix = page.get_pixmap(clip=rect, dpi=dpi, colorspace=fitz.csRGB, alpha=False)
    buf, n = pix.samples, pix.width * pix.height
    if not n:
        return 0.0
    return sum(1 for i in range(0, len(buf), 3) if min(buf[i:i + 3]) >= white) / n


def figure_regions(page):
    """Raster images and clustered vector drawings. Returns [(Rect, kind, info)]."""
    regs = []
    for info in page.get_image_info(xrefs=True):
        r = fitz.Rect(info["bbox"])
        if r.width > 20 and r.height > 20:
            w_in = r.width / 72
            dpi = info.get("width", 0) / w_in if w_in else 0
            regs.append((r, "raster", {"dpi": round(dpi)}))
    draws = [r for r in visible_drawings(page) if r.width < page.rect.width * 0.98 and (r.width > 1 or r.height > 1)]
    if len(draws) >= 8:  # a few lines are usually table rules or separators, not a figure
        clusters = []
        for r in sorted(draws, key=lambda x: (x.y0, x.x0)):
            for i, c in enumerate(clusters):
                if (c + (-6, -6, 6, 6)).intersects(r):
                    clusters[i] = c | r      # write back into the list; `c |= r` only changes the loop variable and clusters never grow
                    break
            else:
                clusters.append(fitz.Rect(r))
        merged = True                         # grown clusters may now touch each other; merge until stable
        while merged:
            merged = False
            for i in range(len(clusters)):
                for j in range(i + 1, len(clusters)):
                    if (clusters[i] + (-6, -6, 6, 6)).intersects(clusters[j]):
                        clusters[i] = clusters[i] | clusters.pop(j)
                        merged = True
                        break
                if merged:
                    break
        for c in clusters:
            if c.width > 60 and c.height > 40:
                regs.append((c, "vector", {}))
    return regs


def check(pdf, out=None, min_pt=6.0, min_dpi=200):
    doc = fitz.open(pdf)
    red, warn, caps, refs, crops = [], [], {}, {}, []
    all_lines = [lines_of(p) for p in doc]       # text extraction is the slowest step; do it once
    col = body_column(doc, all_lines)
    for pno in range(doc.page_count):
        page = doc[pno]
        lines = all_lines[pno]
        regs = figure_regions(page)
        prose = []
        for ln in lines:
            key = caption(ln["text"])
            if key:
                caps.setdefault(key, []).append((pno + 1, ln))
            else:
                prose.append(ln["text"])
        text = " ".join(prose)       # join the page before matching: "(Figure" ends one line and "5)" starts the next
        for m2 in REF.finditer(text):   # "表 1-" at a line end and "1" on the next joins to "表 1- 1"
            refs.setdefault((KIND[m2.group(1)], re.sub(r"\s+", "", m2.group(2)).replace("–", "-")), []).append(pno + 1)
        for m3 in REF_PL.finditer(text):
            for n in expand_nums(m3.group(2)):
                refs.setdefault((KIND[m3.group(1)], n), []).append(pno + 1)
        page_caps = [(c[0], l) for l in lines for c in [caption(l["text"])] if c]
        for kind, ln in page_caps:
            if kind != "圖":
                continue
            near = regs or (ln["bbox"].y0 < page.rect.height / 3 and pno > 0 and figure_regions(doc[pno - 1]))
            if not near:
                red.append(f"p.{pno + 1} \"{ln['text'][:20]}\" has a figure caption but no figure was found nearby (neither raster nor vector)")
        for r, kind, info in regs:
            tag = f"{'raster' if kind == 'raster' else 'vector'} figure on p.{pno + 1} (y {r.y0:.0f}-{r.y1:.0f})"
            over = max(col[0] - r.x0, r.x1 - col[1]) if col else 0
            if over > 8:                     # frame overshoots: measure the actual ink, white margins do not count
                ink = ink_bbox(page, r & page.rect)
                over = max(col[0] - ink.x0, ink.x1 - col[1])
            if not (page.rect + (6, 6, -6, -6)).contains(r):
                red.append(f"{tag} runs off the page or within 6 pt of the paper edge: it will be clipped")
            elif over > 8:   # inside the page nothing is clipped; this is only a ragged text block (a frame border clipped by a box is for the visual review)
                warn.append(f"{tag} is {over:.1f} pt ({over / 72 * 2.54:.2f} cm) beyond the text column: check whether full-bleed is intended or the width is wrong")
            if kind == "raster" and info["dpi"] and info["dpi"] < min_dpi:
                warn.append(f"{tag} has effective resolution about {info['dpi']} dpi, below {min_dpi}: it will print blurry")
            if kind == "raster" and info["dpi"] > 600 and white_ratio(page, r & page.rect) > 0.5:
                # Text inside a raster cannot be measured, so look at how much it was shrunk: charts are
                # usually exported at 300 dpi, so a higher equivalent dpi means a smaller figure.
                # A chart at 1310 dpi equivalent and 40% of the column width left axis text at ~3 pt;
                # at full column width the same chart is 426 dpi.
                est = 10 * 300 / info["dpi"]
                narrow = col and r.width < (col[1] - col[0]) * 0.6
                msg = (f"{tag} is a white-background chart at {info['dpi']} dpi equivalent: if exported at 300 dpi, 10 pt text inside shrinks to about {est:.1f} pt"
                       + (f", and it spans only {r.width / (col[1] - col[0]):.0%} of the column width" if narrow else "") + "; check it visually")
                (red if info["dpi"] >= 900 and narrow else warn).append(msg)
            if kind == "vector":
                inside = [l["size"] for l in lines if r.contains(l["bbox"].tl) and r.contains(l["bbox"].br)]
                if inside and min(inside) < min_pt:
                    body = col[2] if col else None
                    red.append(f"{tag} has smallest font {min(inside):.1f} pt (< {min_pt})"
                               + (f", body text is {body} pt" if body else "") + ": the figure was shrunk too far; change the layout instead of shrinking")
            if out:
                cap = next((l for k, l in page_caps
                            if l["bbox"].y0 >= r.y1 - 2 and l["bbox"].y0 - r.y1 < 80), None)
                clip = fitz.Rect(r) | cap["bbox"] if cap else fitz.Rect(r)
                clip = (clip + (-12, -12, 12, 12)) & page.rect
                fn = os.path.join(out, f"p{pno + 1:03d}_y{int(r.y0):04d}.png")
                page.get_pixmap(clip=clip, dpi=150).save(fn)
                crops.append((fn, cap["text"] if cap else "(caption not found)"))
    for kind in ("圖", "表"):
        nm = NAME[kind]
        nums = sorted({k[1] for k in caps if k[0] == kind}, key=lambda x: [int(t) for t in re.split(r"[-–.]", x)])
        simple = [int(n) for n in nums if n.isdigit()]
        if simple:
            gaps = sorted(set(range(1, max(simple) + 1)) - set(simple))
            if gaps:
                red.append(f"{nm} numbering gap: missing {', '.join(map(str, gaps))}")
        for k, occ in caps.items():
            if k[0] == kind and len(occ) > 1:
                pages = [p for p, _ in occ]
                msg = f"{nm} {k[1]} caption appears {len(occ)} times (p.{', '.join(map(str, pages))})"
                if max(pages) - min(pages) <= len(occ) - 1 or any("續" in l["text"] or "continued" in l["text"].lower() for _, l in occ):
                    warn.append(msg + ": adjacent pages, probably a table split across pages or a continuation; check")
                else:
                    red.append(msg)
        for k, pages in refs.items():
            if k[0] == kind and k not in caps:
                red.append(f"text mentions {nm} {k[1]} (p.{pages[0]}) but there is no such caption")
        for k in caps:
            if k[0] == kind and k not in refs:
                warn.append(f"{nm} {k[1]} has a caption but is never referenced in the text")
    if out and crops:
        with open(os.path.join(out, "_review_checklist.md"), "w", encoding="utf-8") as f:
            f.write(f"# Figure review checklist: {os.path.basename(pdf)}\n\nOpen each PNG and report for each: no problem, or the problem and where.\n\n"
                    "Check: text touching lines or boxes, text or frame lines clipped, legend covering data, "
                    "axis labels and ticks readable, font size clearly smaller than body text, CJK glyphs "
                    "rendered as boxes, caption matches the figure content, font size consistent across figures.\n\n")
            for fn, cap in crops:
                f.write(f"- `{os.path.basename(fn)}`: {cap[:60]}\n")
    return red, warn, crops


def main():
    ap = argparse.ArgumentParser(description=(__doc__ or "").split("\n")[0])
    ap.add_argument("pdf", help="typeset PDF to check")
    ap.add_argument("--out", default="", help="directory for per-figure PNG crops and the review checklist")
    ap.add_argument("--min-pt", type=float, default=6.0, help="smallest allowed font size inside a vector figure (default 6)")
    ap.add_argument("--min-dpi", type=int, default=200, help="lowest allowed effective raster resolution (default 200)")
    ap.add_argument("--json", action="store_true", help="print findings as JSON")
    a = ap.parse_args()
    if a.out:
        os.makedirs(a.out, exist_ok=True)
    red, warn, crops = check(a.pdf, a.out or None, a.min_pt, a.min_dpi)
    if a.json:
        print(json.dumps({"red": red, "warn": warn, "crops": [c[0] for c in crops]}, ensure_ascii=False, indent=1))
    else:
        for x in red:
            print("  🔴 " + x)
        for x in warn:
            print("  🟡 " + x)
        print(f"-- 🔴 {len(red)} | 🟡 {len(warn)}" + (f" | {len(crops)} crops -> {a.out} (checklist: _review_checklist.md)" if a.out else "") + " --")
    return 1 if red else 0


if __name__ == "__main__":
    sys.exit(main())
