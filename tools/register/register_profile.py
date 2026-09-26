#!/usr/bin/env python3
"""register_profile.py: the register deviation list for a native-polish pass. Which
features of the draft fall outside the range of published papers from the same field,
and which way each one should move. Local, no upload. Not a detector.

Why this exists: a native-polish pass needs a yardstick, and "sounds native" is too
vague to check. Here the yardstick is register alignment (Demir & Egbert 2026, Applied
Corpus Linguistics): a draft reads like the field when its features fall inside the
p10-p90 band of real papers in that field. The target is the band, not the median.
Without this list an editor fixes hundreds of surface items (articles, prepositions,
collocations, translationese) and leaves every register deviation where it was, because
nobody told it where the draft is off. Some popular polish rules also point the wrong
way for academic prose: turning every 進行 into a bare verb, splitting long sentences,
banning the semicolon, turning every nominalization into a verb.

What it does:
  1. applies a per-feature policy to the measurements (Chinese: tools/zh-tw/zh_register.py;
     English: tools/en/metadiscourse_en.py plus, if installed, tools/en/biber_diag.py) and
     writes the deviation list the native editor works from;
  2. picks a few paragraphs from corpus papers near the venue median as a feel reference
     (--exemplars). The editor reads them for rhythm and density and never copies them.
tools/register/polish_check.py imports measure() and compare() and checks the whole draft
before and after an edit list, so an edit cannot push a feature the wrong way.

Policies (one per feature):
  band    move back into p10-p90 from either side: reduce when high, restore when low,
          leave alone inside the band.
  cap     may only go down (AI syntax fingerprints and stock metadiscourse: dashes,
          contrast frames, 綜上所述, "in summary").
  locked  a hard rule, never increases (sentence-initial 然而 by default).
  report  stance and claim strength (hedges, boosters, 可能/或許, 認為, self-mention):
          deviations are listed for the author; the editor does not touch them.
Override any policy with --policy-file policy.json:
  {"進行": "report", "transitions": ["band", "how to fix when high", "how to fix when low"]}

Corpus: the same corpora the measuring tools use, and nothing ships with the kit.
  Chinese  --corpus or $ZH_CORPUS_DIR, <corpus>/<venue>/*.txt (see zh_register.py)
  English  --corpus or $CORPUS_DIR,    <corpus>/<venue>/*.txt (see ai_style_diag.py)
  At least 30 published papers by other people; a --venue subset is used only when it
  holds 30 or more, otherwise the whole corpus is used and the list says so. Drafts
  need 1000+ Han characters (Chinese) or 800+ words (English).
  The Biber layer (English grammar features) runs biber_diag.py in its own environment:
  pass --biber-python <path to that venv's python> or set $BIBER_PYTHON. Without it the
  list covers metadiscourse only and says so.

Usage:
  register_profile.py <draft> --lang zh --corpus <dir> [--venue J] [--lines 40-120]
                      [--out deviations.md] [--exemplars 4 --exemplar-out exemplars.md]
  register_profile.py <draft> --lang en --corpus <dir> --venue <folder> [--no-biber] [--json]
  register_profile.py --selftest        # synthetic corpus in a temp dir; no real data needed
"""
import argparse
import json
import math
import os
import re
import subprocess
import sys
import tempfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
TOOLS = HERE.parent
for sub in ("zh-tw", "en", "common"):
    sys.path.insert(0, str(TOOLS / sub))
BIBER_DIAG = TOOLS / "en" / "biber_diag.py"

# ---------- Chinese policy ----------
# key -> (policy, how to fix when high, how to fix when low). Keys match zh_register.FEATURES.
ZH_POLICY = {
    "本研究": ("band", "drop the subject or rephrase",
              "where 本文 or 筆者 pile up, switch some back to 本研究, the default self-reference "
              "in Taiwan journals"),
    "本文": ("band", "switch to 本研究, but keep 本研究 inside its own band for your range; "
                     "drop the subject or rephrase the rest. Replacing every 本文 with 本研究 just "
                     "moves the deviation to the other feature", ""),
    "筆者": ("report", "", ""),
    "我們": ("report", "", ""),
    "被": ("band", "make it active or use 受到/遭; drop passives that add nothing", "(no need to add)"),
    "進行": ("band", "turn 進行 + verb back into the verb",
             "Taiwan journals write 進行分析 and 進行訪談 routinely; if an earlier pass cut every "
             "進行 down to a bare verb, restore it where the sentence now reads clipped"),
    "加以/予以": ("band", "turn back into the verb", "(no need to add)"),
    "對於": ("band", "use 對 or reorder the sentence", "(no need to add)"),
    "關於": ("band", "use 對 or 就, or reorder the sentence", "(no need to add)"),
    "作為": ("band", "use 當作 or 是, or reorder", "(no need to add)"),
    "一個": ("band", "delete 一個 used like an English indefinite article", "(no need to add)"),
    "一種": ("band", "delete 一種 used like an English indefinite article", "(no need to add)"),
    "一項": ("band", "一項研究 and 一項發現 usually lose the 一項", "(no need to add)"),
    "其 (pronoun)": ("band", "replace an unclear 其 with the noun", "(no need to add)"),
    "它/它們": ("band", "replace with the noun or drop it (Chinese rarely uses inanimate pronouns)",
                "(no need to add)"),
    "的": ("band", "break up chains of three or more 的 in one phrase: use 之 or a verb",
           "(no need to add)"),
    "之": ("band", "change back to 的",
           "written 之 (研究之目的, 兩者之間) is more common in Taiwan journals than in the draft; "
           "use 之 where a 的 chain runs long"),
    "具有": ("band", "use 有", "Taiwan journals write 具有…特質/意義; switch a few 有 back to 具有"),
    "針對": ("band", "use 對 or 就", "Taiwan journals write 針對…進行; switch a few 對 back to 針對"),
    "而言": ("band", "", ""),
    "透過/經由": ("band", "", "Taiwan journals use 透過 for means; where 用/以/靠 pile up, switch some "
                              "back to 透過"),
    "藉由/藉以": ("band", "", ""),
    "因此": ("band", "use 故 or 於是, or drop it", "add 因此 where the reader is left to infer the cause"),
    "此外": ("band", "", ""),
    "然而": ("locked", "", ""),
    "但 (not 不但)": ("band", "", ""),
    "而且": ("band", "", ""),
    "同時": ("band", "", ""),
    "以及": ("band", "", "use 以及 before the last item of a long list"),
    "並 (not 並非)": ("band", "", "join two verb phrases with 並 (蒐集資料並分析)"),
    "則": ("band", "", ""),
    "例如": ("band", "", ""),
    "換言之/亦即/也就是說": ("cap", "delete or state it directly", ""),
    "首先": ("cap", "", ""),
    "其次": ("cap", "", ""),
    "綜上所述/總而言之": ("cap", "delete", ""),
    "值得注意/由此可見": ("cap", "delete", ""),
    "研究顯示/研究指出": ("cap", "rewrite as a named citation (某某（年）指出)", ""),
    "不僅": ("cap", "drop the 不僅…更 frame", ""),
    "脈絡下": ("cap", "", ""),
    "可能/或許": ("report", "", ""),
    "顯示": ("report", "", ""),
    "發現": ("report", "", ""),
    "認為": ("report", "", ""),
    "相當": ("report", "", ""),
    "semicolon": ("band", "use 。 or ，",
                  "put 「；」 between long parallel clauses that each have their own subject and "
                  "predicate; Taiwan journal papers use it routinely"),
    "colon": ("band", "", ""),
    "dash": ("cap", "use a comma, parentheses, or split the sentence", ""),
    "contrast (並非/而非/而不是)": ("cap", "state it directly", ""),
    "mean sentence length": ("band", "split the longest few sentences",
                             "merge: when two adjacent sentences share a subject or are linked by "
                             "cause or sequence, join them with a comma. A Taiwan journal sentence "
                             "often carries several comma-separated clauses"),
    "median sentence length": ("band", "", ""),
    "mean clause length": ("band", "", "clauses between commas are too short: fold the "
                                       "fragments into the clause before or after"),
}

# ---------- English policy ----------
EN_MD_POLICY = {   # keys match metadiscourse_en.MARKERS names
    "hedges": ("report", "", ""),
    "boosters": ("report", "", ""),
    "attitude markers": ("report", "", ""),
    "self-mention": ("report", "", ""),
    "reader pronouns": ("report", "", ""),
    "directives": ("report", "", ""),
    "questions": ("report", "", ""),
    "shared knowledge": ("report", "", ""),
    "transitions": ("band", "drop the ones that only restate an obvious link",
                    "add however / therefore / thus where the logical link between sentences is "
                    "left for the reader to infer"),
    "frame markers": ("cap", "delete 'in summary', 'to conclude', 'overall,'", ""),
    "code glosses": ("band", "",
                     "add 'for example', 'that is', 'such as', 'namely' where a term or claim needs "
                     "a gloss (never a dash)"),
    "evidentials": ("report", "", ""),
}
# biber_diag column -> (label, policy, fix when high, fix when low). Columns not listed
# here stay out of the deviation list.
EN_BIBER = {
    "f_14_nominalizations": ("nominalizations", "band",
                             "turn nominalizations back into verbs ('the analysis of X' -> 'we analysed X')",
                             "leave them; do not convert more nouns to verbs"),
    "f_25_present_participle": ("present-participial clauses", "band",
                                "split sentence-final -ing clauses into separate sentences", ""),
    "f_29_that_subj": ("that-clauses as subject", "band", "", ""),
    "f_64_phrasal_coordination": ("phrasal coordination", "band",
                                  "reduce 'X and Y' noun pairs that add nothing",
                                  "join two same-class words with 'and' where two clauses now say one "
                                  "thing about two items (Biber counts only adjacent 'X and Y'; serial "
                                  "'X, Y, and Z' lists do not count)"),
    "f_65_clausal_coordination": ("clausal coordination", "band",
                                  "clauses strung together with ', and': subordinate one (because, "
                                  "while, which) or split", ""),
    "f_24_infinitives": ("to-infinitives", "band", "",
                         "use to-infinitives for purpose and complements ('used X to test', 'aims to', "
                         "'serves to') where a gerund or nominalization now sits"),
    "f_20_existential_there": ("existential there", "band", "",
                               "'there is/are' is natural for introducing a new entity"),
    "f_17_agentless_passives": ("agentless passives", "band", "", ""),
    "f_18_by_passives": ("by-passives", "band", "", ""),
    "f_39_prepositions": ("prepositions", "band", "", ""),
    "f_40_adj_attr": ("attributive adjectives", "band", "",
                      "(no action unless a noun phrase is vague without its adjective)"),
    "f_42_adverbs": ("adverbs", "band", "", ""),
    "f_45_conjuncts": ("conjuncts", "band", "",
                       "add conjuncts (however, therefore, thus) where the link is implicit"),
    "f_63_split_auxiliary": ("split auxiliaries (may also be)", "band", "",
                             "an adverb between auxiliary and verb ('can also be', 'has recently been') "
                             "is normal in academic English"),
    "f_11_indefinite_pronouns": ("indefinite pronouns", "band",
                                 "replace something/anything/everything with the specific noun", ""),
    "f_04_place_adverbials": ("place adverbials", "band",
                              "'below', 'above', 'outside' used as text pointers ('as described below'): "
                              "name the section, table or figure instead (Biber's list does not include "
                              "'here'; leave 'here' alone for this feature)", ""),
    "f_05_time_adverbials": ("time adverbials", "band", "", ""),
    "f_10_demonstrative_pronoun": ("bare demonstrative pronouns", "band", "add the noun after a bare 'this'",
                                   "a bare 'this/that' pointing back to the previous sentence is normal; "
                                   "do not add a noun after every 'this'"),
    "f_51_demonstratives": ("demonstratives", "band", "", ""),
    "f_60_that_deletion": ("that-deletion", "band", "restore 'that' after reporting verbs", ""),
    "f_59_contractions": ("contractions", "cap", "expand contractions", ""),
    "f_06_first_person_pronouns": ("first-person pronouns", "report", "", ""),
    "f_07_second_person_pronouns": ("second-person pronouns", "report", "", ""),
    "f_47_hedges": ("hedges (Biber)", "report", "", ""),
    "f_48_amplifiers": ("amplifiers", "report", "", ""),
    "f_49_emphatics": ("emphatics", "report", "", ""),
    "f_52_modal_possibility": ("possibility modals", "report", "", ""),
    "f_53_modal_necessity": ("necessity modals", "report", "", ""),
    "f_54_modal_predictive": ("predictive modals will/would", "report", "", ""),
    "f_01_past_tense": ("past tense", "report", "", ""),
    "f_03_present_tense": ("present tense", "report", "", ""),
}
HIDDEN = {"median sentence length"}   # moves with the mean; checked in compare(), not listed twice
POLICIES = ("band", "cap", "locked", "report")


def load_policy_file(path):
    """Apply a JSON override: {feature: policy} or {feature: [policy, fix_high, fix_low]}.
    A feature key can be a zh_register key, a metadiscourse marker name, or a biber column."""
    if not path:
        return
    cfg = json.loads(Path(path).expanduser().read_text(encoding="utf-8"))
    for key, val in cfg.items():
        if key.startswith("_"):
            continue
        pol, hi, lo = (val, None, None) if isinstance(val, str) else (list(val) + [None, None])[:3]
        if pol not in POLICIES:
            sys.exit(f"--policy-file: {key!r} has policy {pol!r}; use one of {', '.join(POLICIES)}")
        hit = False
        for table in (ZH_POLICY, EN_MD_POLICY):
            if key in table:
                old = table[key]
                table[key] = (pol, old[1] if hi is None else hi, old[2] if lo is None else lo)
                hit = True
        if key in EN_BIBER:
            label, _, ohi, olo = EN_BIBER[key]
            EN_BIBER[key] = (label, pol, ohi if hi is None else hi, olo if lo is None else lo)
            hit = True
        if not hit:
            print(f"(--policy-file: {key!r} is not a known feature; ignored)", file=sys.stderr)


# ---------- measuring ----------
def _read(path):
    p = Path(path)
    if p.suffix.lower() in (".pdf", ".docx"):
        return None
    return p.read_text(encoding="utf-8", errors="ignore")


def measure_zh(raw, corpus, venue=None, tex=False):
    import zh_register as Z
    from md_prose import strip_markup
    corpus = Z.corpus_from_env(corpus)
    if not corpus or not corpus.is_dir():
        return None
    p = Z.profile(strip_markup(raw, tex=tex), corpus, venue)
    if not p:
        return None
    feats = {}
    for k, f in p["feats"].items():
        pol, hi, lo = ZH_POLICY.get(k, ("report", "", ""))
        feats[k] = dict(f, policy=pol, fix_high=hi, fix_low=lo, src="zh_register",
                        count=(round(f["value"] * p["han"] / 1000)
                               if f["group"] != "sentence length" else None))
    return dict(lang="zh", unit="Han chars", size=p["han"], venue=p["venue"], n_docs=p["n_docs"],
                corpus=str(corpus), feats=feats)


def _biber(clean_text, corpus, groups, biber_python):
    py = biber_python or os.environ.get("BIBER_PYTHON")
    if not py or not Path(py).expanduser().exists():
        return None, "no Biber environment (pass --biber-python or set BIBER_PYTHON)"
    with tempfile.NamedTemporaryFile("w", suffix=".md", delete=False, encoding="utf-8") as f:
        f.write(clean_text)
        tmp = f.name
    try:
        cmd = [str(Path(py).expanduser()), str(BIBER_DIAG), tmp, "--corpus", str(corpus), "--json"]
        if groups:
            cmd += ["--groups", ",".join(groups)]
        r = subprocess.run(cmd, capture_output=True, text=True, timeout=1800)
        if r.returncode != 0:
            return None, "biber_diag failed: " + (r.stderr.strip().splitlines() or ["?"])[-1]
        return json.loads(r.stdout[r.stdout.index("{"):]), None
    except Exception as e:   # a missing optional layer must not break the list
        return None, f"biber_diag failed: {e}"
    finally:
        os.unlink(tmp)


def measure_en(raw, corpus, venue=None, biber_python=None, biber=True, suffix=".md"):
    import ai_style_diag as A
    import metadiscourse_en as M
    corpus = Path(corpus or os.environ.get("CORPUS_DIR") or "").expanduser()
    if not str(corpus) or str(corpus) == "." or not corpus.is_dir():
        return None
    with tempfile.NamedTemporaryFile("w", suffix=suffix, delete=False, encoding="utf-8") as f:
        f.write(raw)
        tmp = f.name
    try:
        text = A.clean(A.extract_text(Path(tmp)))
    finally:
        os.unlink(tmp)
    groups = [venue] if venue else None
    try:
        p = M.profile(text, corpus, groups)
    except M.BaselineError as e:
        print(f"(metadiscourse baseline: {e})", file=sys.stderr)
        return None
    if not p:
        return None
    feats = {}
    for k, f in p["feats"].items():
        pol, hi, lo = EN_MD_POLICY.get(k, ("report", "", ""))
        feats[k] = dict(f, group=f["cat"], policy=pol, fix_high=hi, fix_low=lo, src="metadiscourse_en")
    note = None
    if biber:
        b, why = _biber(text, corpus, groups, biber_python)
        if b:
            for c, f in b["feats"].items():
                if c in EN_BIBER:
                    label, pol, hi, lo = EN_BIBER[c]
                    feats[f"{label} [{c}]"] = dict(f, group="grammar (Biber)", policy=pol, fix_high=hi,
                                                   fix_low=lo, src="biber_diag", count=None)
        else:
            note = f"grammar layer skipped: {why}"
            print(f"({note})", file=sys.stderr)
    return dict(lang="en", unit="words", size=p["n_words"], venue=p["groups"], n_docs=p["n_docs"],
                corpus=str(corpus), feats=feats, note=note)


def measure(raw, lang, corpus=None, venue=None, biber_python=None, biber=True, tex=False):
    """The draft's register profile with a policy on every feature, or None when the
    corpus or the draft is too small to measure."""
    if lang == "zh":
        return measure_zh(raw, corpus, venue, tex)
    return measure_en(raw, corpus, venue, biber_python, biber, ".tex" if tex else ".md")


# ---------- direction check (used by polish_check) ----------
REL_TOL = 0.015   # rate-only features: deleting words nudges untouched rates up a little


def compare(before, after):
    """(violations, notes) from two whole-draft profiles, before and after the edits.
    band: a high feature may not rise, a low one may not fall, an in-band one may not be
    pushed out; cap: a high one may not rise, an in-band one may not exceed p90;
    locked: may not rise; report: any change is a note for the author."""
    bad, notes = [], []
    for k, fb in before["feats"].items():
        fa = after["feats"].get(k)
        if not fa:
            continue
        pol, vb, va = fb["policy"], fb["value"], fa["value"]
        cb, ca = fb.get("count"), fa.get("count")
        if cb is not None and ca is not None:
            up, down = ca > cb, ca < cb
            delta = f"{cb} -> {ca}"
        else:
            up = va > vb * (1 + REL_TOL) + 1e-9
            down = va < vb * (1 - REL_TOL) - 1e-9
            delta = f"{vb:.2f} -> {va:.2f}"
        where = (f"{k} ({delta}; p{fb['pct']:.0f} -> p{fa['pct']:.0f}; "
                 f"band {fb['p10']:.2f}-{fb['p90']:.2f})")
        if pol == "locked" and up:
            bad.append(f"{where}: hard rule, may not increase")
        elif pol in ("band", "cap") and fb["status"] == "high" and up:
            bad.append(f"{where}: already high, may not increase")
        elif pol == "band" and fb["status"] == "low" and down:
            bad.append(f"{where}: already low, may not decrease")
        elif pol in ("band", "cap") and fb["status"] == "ok" and fa["status"] != "ok":
            if pol == "cap" and fa["status"] == "low":
                continue
            bad.append(f"{where}: was inside the band, pushed out")
        elif pol == "report" and (up or down):
            notes.append(f"{where}: stance or claim strength changed; confirm the author's claim is intact")
        elif pol in ("band", "cap") and fb["status"] != "ok" and fa["status"] == "ok":
            notes.append(f"{where}: back inside the band")
    return bad, notes


# ---------- deviation list ----------
def _lines_arg(s):
    if not s:
        return None
    out = []
    for part in s.split(","):
        a, _, b = part.partition("-")
        out.append((int(a), int(b or a)))
    return out


def _scope_text(raw, lines):
    return "\n".join(l for i, l in enumerate(raw.split("\n"), 1) if any(a <= i <= b for a, b in lines))


def _scope_size(raw, lang, lines):
    if not lines:
        return None
    sel = _scope_text(raw, lines)
    return (len(re.findall(r"[一-鿿]", sel)) if lang == "zh"
            else len(re.findall(r"[A-Za-z][A-Za-z'-]*", sel)))


def _scope_count(raw, lang, key, lines):
    """How often one feature occurs inside the editor's line range (after stripping
    layout and quotations); None when it cannot be counted."""
    sel = _scope_text(raw, lines)
    if lang == "zh":
        import zh_register as Z
        from md_prose import strip_markup
        rx = Z.RX.get(key)
        return len(rx.findall(Z.prose(strip_markup(sel)))) if rx else None
    import ai_style_diag as A
    import metadiscourse_en as M
    mk = next((m for m in M.MARKERS if m[1] == key), None)
    if not mk:
        return None
    return len(re.findall(M.MARKERS[mk], A.clean(sel), 0 if mk in M.CASE_SENSITIVE else re.I))


def _examples_zh(raw, key, lines, status):
    import zh_register as Z
    if key == "mean sentence length" and status == "high":
        return [f"L{i} ({n} chars) 「{s}…」" for i, n, s in Z.long_sentences(raw, lines)]
    if key == "mean sentence length" and status == "low":
        return [f"L{i} (two sentences, {n} chars) 「{s}」" for i, n, s in Z.short_runs(raw, lines)]
    if status == "high":
        return [f"L{i} 「…{c}…」" for i, c in Z.locate(raw, key, lines, limit=6)]
    return []


def _examples_en(raw, name, lines):
    import metadiscourse_en as M
    key = next((k for k in M.MARKERS if k[1] == name), None)
    if not key:
        return []
    flags = 0 if key in M.CASE_SENSITIVE else re.I
    out = []
    for i, line in enumerate(raw.split("\n"), 1):
        if lines and not any(a <= i <= b for a, b in lines):
            continue
        for m in re.finditer(M.MARKERS[key], line, flags):
            out.append(f"L{i} \"…{line[max(0, m.start() - 30):m.end() + 30].strip()}…\"")
            if len(out) >= 6:
                return out
    return out


# Where a Biber feature can be found (high: instances; low: sentence shapes that could be
# rewritten into the feature). Only features with a clear surface pattern are listed.
BIBER_SITES = {
    ("f_04_place_adverbials", "high"): r"\b(?:below|above|outside|beneath)\b",
    ("f_11_indefinite_pronouns", "high"):
        r"\b(?:something|anything|everything|nothing|someone|anyone|everyone|nobody)\b",
    ("f_65_clausal_coordination", "high"): r", and (?:the|it|this|these|they|we|he|she|its|their)\b",
    ("f_14_nominalizations", "high"): r"\b(?:the|an?) \w+(?:tion|ment|ance|ence|ity) of\b",
    ("f_25_present_participle", "high"): r", \w+ing\b[^.]*\.",
    ("f_24_infinitives", "low"):
        r"\bfor (?:the )?\w+ing\b|\b(?:aim|aims|aimed|goal|purpose|attempt|intention)s? (?:at|of) \w+ing\b"
        r"|\bwith the (?:aim|purpose|goal) of\b",
    ("f_45_conjuncts", "low"): r"(?:^|\. )(?:But|And|So|Also) ",
}


def _examples_biber(raw, col, status, lines, limit=6):
    rx = BIBER_SITES.get((col, status))
    if not rx:
        return []
    out = []
    for i, line in enumerate(raw.split("\n"), 1):
        if lines and not any(a <= i <= b for a, b in lines):
            continue
        if line.lstrip().startswith(("|", "#", "!", "<!--")):
            continue
        for m in re.finditer(rx, line, re.I if col != "f_45_conjuncts" else 0):
            out.append(f"L{i} \"…{line[max(0, m.start() - 30):m.end() + 30].strip()}…\"")
            if len(out) >= limit:
                return out
    return out


def deviation_md(prof, raw, lines=None, draft_name="draft"):
    lang, unit, size = prof["lang"], prof["unit"], prof["size"]
    scope = _scope_size(raw, lang, lines)
    L = ["# Register deviation list (register_profile)",
         f"Draft: {draft_name} | {size} {unit} | baseline = {prof['venue']}, "
         f"{prof['n_docs']} published papers from the corpus",
         (f"Your range: lines {', '.join(f'{a}-{b}' for a, b in lines)} (about {scope} {unit})"
          if lines else "Range: whole draft"),
         ""]
    if prof.get("note"):
        L += [f"Note: {prof['note']}", ""]
    L += ["\"Band\" = p10-p90 of same-field published papers. Move features that sit outside the "
          "band toward it; the target is the band, not the median. Each edit has to make that spot "
          "read better on its own; do not force an edit to hit a number. Leave in-band features alone.",
          ""]
    fix, author, locked, inband = [], [], [], []
    for k, f in prof["feats"].items():
        pol, st = f["policy"], f["status"]
        rng = f"{f['p10']:.2f}-{f['p90']:.2f}, median {f['p50']:.2f}"
        mild = 5 <= f["pct"] <= 95
        head = (f"{'▲ HIGH' if st == 'high' else '▼ LOW'} **{k}** {f['value']:.2f} "
                f"(p{f['pct']:.0f}; band {rng})"
                + (" | mild: fix only the one or two most natural spots" if mild else ""))
        if pol == "locked":
            locked.append(f"- {k}: may not increase (hard rule)")
            continue
        if st == "ok":
            inband.append(k)
            continue
        if k in HIDDEN:
            continue
        if pol == "report":
            author.append(f"- {head}")
            continue
        if pol == "cap" and st == "low":
            inband.append(k)
            continue
        how = f["fix_high"] if st == "high" else f["fix_low"]
        line = f"- {head}\n  - How to fix: {how or 'judge from the instances'}"
        if f.get("count") is not None:
            bound = f["p90"] if st == "high" else f["p10"]
            line += (f"\n  - Whole draft: {f['count']} now; back inside the band needs about "
                     f"{'<=' if st == 'high' else '>='}{round(bound * size / 1000)}")
            sc = _scope_count(raw, lang, k, lines) if scope else None
            if sc is not None:
                # Give both ends for the editor's own range. Told only "reduce X" or "add Y",
                # an editor working on one section tends to overshoot into the other end.
                lo_s, hi_s = round(f["p10"] * scope / 1000), round(f["p90"] * scope / 1000)
                line += (f"\n  - Your range: {sc} now; scaled from the field's band, {lo_s}-{hi_s} is "
                         f"reasonable here. Move toward the band and **do not cross the other end** "
                         f"(for example, restoring a low feature past {hi_s})")
        if lang == "zh":
            ex = _examples_zh(raw, k, lines, st)
        elif f["src"] == "metadiscourse_en":
            ex = _examples_en(raw, k, lines) if st == "high" else []
        else:
            ex = _examples_biber(raw, k.split("[")[-1].rstrip("]"), st, lines)
        if ex:
            line += ("\n  - Instances in range: " if st == "high"
                     else "\n  - Candidates in range: ") + "; ".join(ex)
        fix.append(line)
    L.append("## To fix (inside your range)")
    L += fix or ["- None: every feature the editor may touch is inside the band. Fix the surface only "
                 "(typos, collocations, articles and prepositions, local usage); leave register alone."]
    L += ["", "## Locked (may not increase)"] + (locked or ["- None"])
    if lang == "zh":
        L += ["- Also never add: sentence-initial 然而, 這一/此一 pointing, dashes, contrast frames "
              "(AI syntax fingerprints and default voice_lint hard rules)"]
    else:
        L += ["- Also never add: dashes, contrast frames ('not X but Y', ', not', 'rather than'), "
              "opener cliches (AI syntax fingerprints; polish_check blocks them)"]
    L += ["", "## For the author (you do not edit these; the \"needs the author\" section of your "
              "change list may point at specific sentences)"] + (author or ["- None"])
    L += ["", "## Inside the band (leave alone)", ", ".join(inband) if inband else "(none)"]
    return "\n".join(L)


# ---------- feel-reference paragraphs ----------
def _nearest(docs, keys, k):
    med, sd = {}, {}
    for key in keys:
        vals = sorted(d["v"][key] for d in docs)
        med[key] = vals[len(vals) // 2]
        m = sum(vals) / len(vals)
        sd[key] = math.sqrt(sum((v - m) ** 2 for v in vals) / len(vals)) or 1.0
    return sorted(docs, key=lambda d: sum(((d["v"][x] - med[x]) / sd[x]) ** 2 for x in keys))[:k]


def _chunks_zh(text, lo=150, hi=380):
    text = re.split(r"參考文獻|參考書目|References", text)[0]
    out, cur = [], ""
    for s in re.split(r"(?<=[。！？])", text):
        cur += s
        n = len(re.findall(r"[一-鿿]", cur))
        if n >= lo:
            if n <= hi:
                out.append(cur.strip())
            cur = ""
    return out


def _clean_score(chunk):
    """A good feel reference has few digits, citation brackets and Latin words."""
    return (len(re.findall(r"\d", chunk)) + 5 * len(re.findall(r"（[^）]*\d{4}", chunk))
            + len(re.findall(r"[A-Za-z]{3,}", chunk)))


def exemplars_zh(corpus, venue, n=4):
    import zh_register as Z
    corpus = Z.corpus_from_env(corpus)
    b = Z.baseline(corpus) if corpus else None
    if not b:
        return []
    docs = [d for d in b["docs"] if not venue or d["venue"] == venue] or b["docs"]
    keys = [key for key, (pol, _, _) in ZH_POLICY.items() if pol == "band" and key in docs[0]["v"]]
    out = []
    for d in _nearest(docs, keys, n * 2):
        cs = _chunks_zh((corpus / d["file"]).read_text(encoding="utf-8", errors="ignore"))
        mid = cs[len(cs) // 3: 2 * len(cs) // 3] or cs
        if mid:
            out.append((d["file"], min(mid, key=_clean_score)))
        if len(out) >= n:
            break
    return out


def exemplars_en(corpus, venue, n=4):
    import metadiscourse_en as M
    corpus = Path(corpus or os.environ.get("CORPUS_DIR") or "").expanduser()
    try:
        b = M.baseline(corpus)
    except (M.BaselineError, OSError):
        return []
    docs = [d for d in b["docs"] if not venue or d["name"].split("/")[0] == venue] or b["docs"]
    keys = [k for k, (pol, _, _) in EN_MD_POLICY.items() if pol == "band"] + ["hedges"]
    out = []
    for d in _nearest(docs, keys, n * 2):
        f = corpus / d["name"]
        raw = f.read_text(encoding="utf-8", errors="ignore") if f.exists() else ""
        paras = [re.sub(r"\s+", " ", p).strip() for p in re.split(r"\n\s*\n", raw)]
        paras = [p for p in paras if 90 <= len(p.split()) <= 220 and not re.match(r"(Figure|Table|Fig\.)", p)]
        mid = paras[len(paras) // 3: 2 * len(paras) // 3] or paras
        if mid:
            out.append((d["name"], min(mid, key=lambda p: len(re.findall(r"\d", p)) + 3 * p.count("("))))
        if len(out) >= n:
            break
    return out


def exemplars_md(lang, corpus, venue, n):
    ex = exemplars_zh(corpus, venue, n) if lang == "zh" else exemplars_en(corpus, venue, n)
    L = ["# Feel reference (same-field published papers whose register features sit closest to "
         "the venue median)",
         "Read a few paragraphs for sentence length, how clauses are joined, self-reference and "
         "formal density. **Never copy a sentence or phrase** and do not imitate the content; they "
         "only show how people in this field usually write.", ""]
    if not ex:
        L.append("(No paragraphs found: the corpus is missing, too small, or its files have no "
                 "paragraph breaks.)")
    for name, text in ex:
        L += [f"## {name}", "", text, ""]
    return "\n".join(L)


# ---------- self-test ----------
def _en_synthetic(root, n=30, venue="VA", seed=3):
    """A throwaway English corpus: word-list prose, clearly not real writing."""
    import random
    words = ("design study participants data method results analysis model system users interface "
             "evaluation findings approach research context practice task measure effect sample "
             "interview theory framework process outcome feedback").split()
    extra = ["however", "therefore", "for example", "may", "suggests", "and", "we"]
    d = root / venue
    d.mkdir(parents=True, exist_ok=True)
    for i in range(n):
        rnd = random.Random(seed + i)
        paras = []
        for _ in range(8):
            sents = []
            for _ in range(8):
                k = rnd.randint(8, 18)
                w = [rnd.choice(words) for _ in range(k)]
                if rnd.random() < 0.3:
                    w[k // 2] = rnd.choice(extra)
                sents.append(" ".join(w).capitalize() + ".")
            paras.append(" ".join(sents))
        (d / f"paper{i:02d}.txt").write_text("\n\n".join(paras), encoding="utf-8")
    return root


def selftest():
    good = True

    def t(name, cond):
        nonlocal good
        good &= bool(cond)
        print(("PASS " if cond else "FAIL ") + name)

    mk = lambda st, v, c=None, pol="band": {"policy": pol, "status": st, "value": v, "count": c,
                                            "pct": 50, "p10": 1.0, "p90": 2.0}
    B = {"feats": {"a": mk("high", 3.0, 30), "b": mk("low", 0.5, 5), "c": mk("ok", 1.5, 15),
                   "d": mk("ok", 1.0, 10, "locked"), "e": mk("ok", 1.5, 15, "report")}}
    A2 = {"feats": {"a": mk("high", 3.1, 31), "b": mk("low", 0.4, 4), "c": mk("high", 2.5, 25),
                    "d": mk("ok", 1.1, 11, "locked"), "e": mk("ok", 1.2, 12, "report")}}
    bad, notes = compare(B, A2)
    t("high rises, low falls, pushed out of band, locked rises: all four blocked", len(bad) == 4)
    t("a stance count that changed is only a note", len(notes) == 1 and "author" in notes[0])
    A3 = {"feats": {"a": mk("ok", 1.9, 19), "b": mk("ok", 1.1, 11), "c": mk("ok", 1.5, 15),
                    "d": mk("ok", 0.9, 9, "locked"), "e": mk("ok", 1.5, 15, "report")}}
    bad, notes = compare(B, A3)
    t("moving toward the band passes and is noted", not bad and sum("back inside" in x for x in notes) == 2)
    t("rate drift within 1.5% is not blocked",
      not compare({"feats": {"a": {**mk("high", 3.0), "count": None}}},
                  {"feats": {"a": {**mk("high", 3.03), "count": None}}})[0])
    t("cap: an in-band feature falling below p10 is fine",
      not compare({"feats": {"a": mk("ok", 1.5, 15, "cap")}},
                  {"feats": {"a": mk("low", 0.2, 2, "cap")}})[0])
    t("然而 is locked by default", ZH_POLICY["然而"][0] == "locked")
    t("stance features go to the author",
      all(ZH_POLICY[k][0] == "report" for k in ("可能/或許", "認為", "顯示")))
    import zh_register as Z
    t("every zh_register feature has a policy", set(Z.ALL_KEYS) <= set(ZH_POLICY))
    import metadiscourse_en as M
    t("every metadiscourse marker has a policy", {n for _, n in M.MARKERS} <= set(EN_MD_POLICY))
    with tempfile.TemporaryDirectory() as tmp:
        zc = Z.synthetic_corpus(Path(tmp) / "zh")
        raw = ("本文以問卷蒐集資料。本文分析結果。本文討論意義。" * 40 + "\n") * 2
        p = measure(raw, "zh", zc, "JX")
        md = deviation_md(p, raw, [(1, 1)]) if p else ""
        t("zh: 本文 is listed to fix, with instances in range", "**本文**" in md and "L1 「" in md)
        t("zh: per-range bounds are given", "Your range:" in md and "do not cross the other end" in md)
        t("zh: feel-reference paragraphs are found", len(exemplars_zh(zc, "JX", 2)) == 2)
        ec = _en_synthetic(Path(tmp) / "en")
        saved, M.CACHE = M.CACHE, Path(tmp) / "md_cache.json"   # keep the real cache untouched
        try:
            draft = "# Draft\n\n" + ("In summary, we show the design. " * 60 + "\n\n") * 3
            pe = measure(draft, "en", ec, "VA", biber=False)
            t("en: metadiscourse layer measures against the synthetic corpus",
              pe and pe["n_docs"] == 30 and "frame markers" in pe["feats"])
            t("en: frame markers flagged high and listed to fix",
              pe and pe["feats"]["frame markers"]["status"] == "high"
              and "**frame markers**" in deviation_md(pe, draft))
        finally:
            M.CACHE = saved
    print("\nselftest: all passed" if good else "\nselftest: FAILED")
    return 0 if good else 1


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("draft", nargs="?", help="draft (.md/.txt/.tex); convert .docx/.pdf to text first")
    ap.add_argument("--lang", choices=["zh", "en"])
    ap.add_argument("--corpus", help="baseline corpus dir (default: $ZH_CORPUS_DIR for zh, $CORPUS_DIR for en)")
    ap.add_argument("--venue", help="compare against this venue folder only (falls back to the whole "
                                    "corpus under 30 papers)")
    ap.add_argument("--lines", help="the editor's line range, e.g. 40-120,130-150 (instances and "
                                    "per-range targets are computed for it)")
    ap.add_argument("--out", help="write the deviation list here (default: print)")
    ap.add_argument("--exemplars", type=int, default=0, help="also pick N same-field paragraphs as a "
                                                             "feel reference")
    ap.add_argument("--exemplar-out", help="write the feel reference here")
    ap.add_argument("--biber-python", help="python of the environment that has pybiber and spaCy "
                                           "(default: $BIBER_PYTHON)")
    ap.add_argument("--no-biber", action="store_true", help="English: skip the Biber grammar layer")
    ap.add_argument("--policy-file", help="JSON overrides: {feature: policy or [policy, fix_high, fix_low]}")
    ap.add_argument("--json", action="store_true", help="print the measured profile as JSON")
    ap.add_argument("--selftest", action="store_true")
    a = ap.parse_args()
    if a.selftest:
        return selftest()
    if not (a.draft and a.lang):
        ap.error("needs a draft and --lang (or --selftest)")
    load_policy_file(a.policy_file)
    raw = _read(a.draft)
    if raw is None:
        sys.exit("Convert .docx/.pdf to .md or .txt first; the deviation list cites line numbers.")
    prof = measure(raw, a.lang, a.corpus, a.venue, a.biber_python, not a.no_biber,
                   a.draft.endswith(".tex"))
    if not prof:
        sys.exit("Cannot measure: no corpus (pass --corpus), fewer than 30 usable papers in it, or the "
                 "draft is too short (under 1000 Han characters / 800 words).")
    if a.json:
        print(json.dumps(prof, ensure_ascii=False, indent=1))
    else:
        md = deviation_md(prof, raw, _lines_arg(a.lines), Path(a.draft).name)
        if a.out:
            Path(a.out).write_text(md + "\n", encoding="utf-8")
            print(f"Deviation list -> {a.out}")
        else:
            print(md)
    if a.exemplars:
        ex = exemplars_md(a.lang, a.corpus, a.venue, a.exemplars)
        if a.exemplar_out:
            Path(a.exemplar_out).write_text(ex + "\n", encoding="utf-8")
            print(f"Feel reference -> {a.exemplar_out}")
        else:
            print("\n" + ex)
    return 0


if __name__ == "__main__":
    sys.exit(main())
