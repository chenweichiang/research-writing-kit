#!/usr/bin/env python3
"""figure_a11y.py — colour-vision accessibility check for figures (CVD + greyscale).

Why: a large share of readers print in black and white, and roughly 8% of men have a
red-green colour vision deficiency. A figure that distinguishes series by hue alone
collapses into mush in either case. This shows up in review as "the figure is hard to
read" without the author ever finding out why — and most venues' figure guidelines
state outright that colour must not be the only carrier of information.

It does two things:
  1. extracts the dominant colours and checks, pairwise, whether they stay
     distinguishable under greyscale and three CVD simulations
  2. writes the simulated images to <figure>_a11y/ so you can LOOK at them

🔴 Honest limits: the simulation is a linear approximation (LMS daltonization), not a
   medical model of vision. "These two collapse" is reliable; "this figure is fine" is
   not a guarantee. **Always open the simulated images.** The numbers are evidence,
   not a verdict.

Requires: numpy, Pillow (+ pymupdf only if you pass a PDF).

Usage:
  figure_a11y.py fig1.png fig2.pdf ...     # check and write simulations
  figure_a11y.py --no-render fig1.png      # numbers only
Exit code 1 if any pair collapses under a CVD simulation.
"""
import argparse, pathlib, sys
import numpy as np

RGB2LMS = np.array([[17.8824, 43.5161, 4.11935],
                    [3.45565, 27.1554, 3.86714],
                    [0.0299566, 0.184309, 1.46709]])
LMS2RGB = np.linalg.inv(RGB2LMS)
SIM = {"protan": np.array([[0, 2.02344, -2.52581], [0, 1, 0], [0, 0, 1]]),
       "deutan": np.array([[1, 0, 0], [0.494207, 0, 1.24827], [0, 0, 1]]),
       "tritan": np.array([[1, 0, 0], [0, 1, 0], [-0.395913, 0.801109, 0]])}
# Far apart in the original (dE>25) but close after simulation (dE<12) = the pair is
# carried by hue alone. That is the real defect.
NEAR, FAR = 12.0, 25.0
# Greyscale uses the WCAG contrast ratio, not a raw luminance difference: a raw
# difference flags the black-vs-grey of an ordinary greyscale figure, where that
# difference IS the encoding. WCAG suggests >=3:1 for graphical objects; 1.4 is a
# conservative "practically indistinguishable" line and the only level reported.
GRAY_CR = 1.4
CHROMA_MIN = 10.0   # both colours near-neutral = deliberate greyscale ramp, not a defect


def simulate(rgb, kind):
    return np.clip(rgb @ RGB2LMS.T @ SIM[kind].T @ LMS2RGB.T, 0, 1)


def _lin(c):
    return np.where(c <= 0.04045, c / 12.92, ((c + 0.055) / 1.055) ** 2.4)


def luminance(rgb):
    return _lin(rgb) @ np.array([0.2126, 0.7152, 0.0722])


def contrast(l1, l2):
    hi, lo = max(l1, l2), min(l1, l2)
    return (hi + 0.05) / (lo + 0.05)


def to_lab(rgb):
    m = np.array([[0.4124, 0.3576, 0.1805], [0.2126, 0.7152, 0.0722],
                  [0.0193, 0.1192, 0.9505]])
    xyz = _lin(rgb) @ m.T / np.array([0.95047, 1.0, 1.08883])
    f = np.where(xyz > 0.008856, np.cbrt(xyz), 7.787 * xyz + 16 / 116)
    return np.stack([116 * f[..., 1] - 16, 500 * (f[..., 0] - f[..., 1]),
                     200 * (f[..., 1] - f[..., 2])], axis=-1)


def load(path):
    from PIL import Image
    p = pathlib.Path(path)
    if p.suffix.lower() == ".pdf":
        import pymupdf
        pix = pymupdf.open(p)[0].get_pixmap(dpi=150)
        img = Image.frombytes("RGB", (pix.width, pix.height), pix.samples)
    else:
        img = Image.open(p).convert("RGB")
    img.thumbnail((900, 900))
    return img


def main_colors(img, k=8):
    """Dominant colours, dropping near-white (usually background) and antialiasing
    speckle, so what is left is what actually encodes information."""
    q = img.quantize(colors=k * 3, method=2).convert("RGB")
    arr = np.asarray(q).reshape(-1, 3) / 255.0
    uniq, cnt = np.unique(arr, axis=0, return_counts=True)
    out = []
    for i in np.argsort(-cnt):
        c, share = uniq[i], cnt[i] / len(arr)
        if share < 0.005 or luminance(c) > 0.92:
            continue
        out.append((c, share))
        if len(out) >= k:
            break
    return out


def hexs(c):
    return "#" + "".join(f"{int(round(v * 255)):02X}" for v in c)


def check(path, render=True):
    img = load(path)
    cols = main_colors(img)
    findings = []
    if len(cols) < 2:
        return cols, [("OK", "fewer than two dominant colours; nothing encoded by colour", "")], None

    rgbs = np.array([c for c, _ in cols])
    lab0, lum0 = to_lab(rgbs), luminance(rgbs)
    sims = {k: to_lab(simulate(rgbs, k)) for k in SIM}

    for i in range(len(rgbs)):
        for j in range(i + 1, len(rgbs)):
            d0 = float(np.linalg.norm(lab0[i] - lab0[j]))
            if d0 < FAR:
                continue
            for k, lab in sims.items():
                d = float(np.linalg.norm(lab[i] - lab[j]))
                if d < NEAR:
                    findings.append(("FAIL",
                        f"{hexs(rgbs[i])} and {hexs(rgbs[j])} collapse under {k} simulation",
                        f"dE {d0:.0f} -> {d:.0f} (areas {cols[i][1]*100:.0f}%/{cols[j][1]*100:.0f}%)"
                        " - this pair is carried by hue alone; add shape/linestyle/direct"
                        " labels, or switch to a CVD-safe palette"))
            if max(float(np.linalg.norm(lab0[x][1:])) for x in (i, j)) < CHROMA_MIN:
                continue
            cr = contrast(float(lum0[i]), float(lum0[j]))
            if cr < GRAY_CR:
                findings.append(("WARN",
                    f"{hexs(rgbs[i])} and {hexs(rgbs[j])} are nearly identical in print",
                    f"contrast ratio {cr:.2f}:1 (WCAG suggests >=3:1 for graphical objects)"
                    " - journals are mostly printed in black and white; separate the"
                    " lightness or encode with linestyle/fill pattern"))

    if len(rgbs) >= 3 and not findings:
        dmax = max(float(np.linalg.norm(lab0[i] - lab0[j]))
                   for i in range(len(rgbs)) for j in range(i + 1, len(rgbs)))
        if dmax < FAR:
            findings.append(("WARN", "dominant colours are already close together; "
                                     "accessibility cannot be judged",
                             f"largest dE is only {dmax:.0f} (<{FAR:.0f}) - if this figure encodes"
                             " information by colour it is already hard to read; if it does not"
                             " (photo, diagram), ignore this"))

    outdir = None
    if render:
        from PIL import Image
        src = pathlib.Path(path)
        outdir = src.parent / (src.stem + "_a11y")
        outdir.mkdir(exist_ok=True)
        arr = np.asarray(img) / 255.0
        for k in SIM:
            Image.fromarray((simulate(arr, k) * 255).astype(np.uint8)).save(outdir / f"{k}.png")
        g = luminance(arr)
        Image.fromarray((np.stack([g] * 3, -1) * 255).astype(np.uint8)).save(outdir / "grayscale.png")
    return cols, findings, outdir


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("figures", nargs="+")
    ap.add_argument("--no-render", action="store_true")
    a = ap.parse_args()

    n_fail = 0
    for f in a.figures:
        print("=" * 70)
        print(f"  {f}")
        print("=" * 70)
        try:
            cols, findings, outdir = check(f, render=not a.no_render)
        except Exception as e:
            print(f"  [FAIL] cannot read: {type(e).__name__}: {e}")
            n_fail += 1
            continue
        print("  dominant colours: " + "  ".join(f"{hexs(c)}({p*100:.0f}%)" for c, p in cols))
        seen = set()
        for sev, title, why in findings:
            if title in seen:
                continue
            seen.add(title)
            n_fail += sev == "FAIL"
            print(f"  [{sev}] {title}" + (f"\n         {why}" if why else ""))
        if not findings:
            print("  OK - dominant colours stay distinct in greyscale and all three simulations")
        if outdir:
            print(f"  -> simulations in {outdir}/ — LOOK AT THEM; the numbers are evidence,"
                  f" not a verdict")
    sys.exit(1 if n_fail else 0)


if __name__ == "__main__":
    main()
