#!/usr/bin/env python3
"""pdf_fetch — layered PDF retrieval for reference collection.

**Only download what you are authorized to.** This reaches subscription content
through *your own* institutional access in a real browser session — the same thing
you would do by hand. It does not circumvent access controls. Open access first,
always; anything you are not entitled to is reported as such, not worked around.

Three layers, cheapest first:
  L1 http_get()      curl_cffi (impersonate=chrome) fixes the TLS/JA3 fingerprint;
                     falls back to urllib when not installed
  L2 BrowserSession  patchright + a real Chrome (persistent profile) clears
                     Cloudflare's interactive challenge, then finds the PDF link
                     **on the rendered landing page** (citation_pdf_url meta →
                     anchors → publisher patterns) and fetches it via in-page
                     `fetch(credentials:'include')`, response capture, or a real
                     download event
  L3 cookie handoff  hand the browser-earned cf_clearance back to L1 (optimisation only)

═══ Measured, 2026-08-30 ═══
                urllib      curl_cffi    real Chrome
  ACM             403         403(*)      ok — 1,110,725 b, %PDF
  Wiley           403         403(*)      ok — landing 200
  T&F             403         200         ok — landing 200
  SAGE / AIP      403         403(*)      ok — landing 200
  ScienceDirect   403         403(*)      (Elsevier's own challenge, slower)
  (*) response header `cf-mitigated: challenge`, title "Just a moment..."

⚠️ Three findings that cost real time to learn — none of them are guesses:
 1. **curl_cffi does not clear Cloudflare's interactive challenge.** The blog posts
    claiming otherwise are not testing academic publishers. It fixes the TLS
    fingerprint only. Still worth making the default client (strictly better than
    urllib), but it is not the answer.
 2. **Cookie handoff is not general.** It works for ACM (cf_clearance travels);
    Wiley's pdfdirect re-triggers the challenge. Use it as an optimisation only,
    and **always verify magic bytes**.
 3. **You cannot build the PDF URL from the DOI.** Guessed URLs for T&F and AIP
    return the HTML landing page. The link has to be read off the **rendered**
    page — that is why L2 exists.

❌ Verified dead end, do not retry:
 **Zotero translation-server cannot give you PDF links.** It is the intuitive
 answer — 700+ publisher translators, exactly the "landing page → PDF" knowledge
 you want. Measured against `docker run -p 1969:1969 zotero/translation-server`:
 metadata for ACM / T&F / Springer / APA all resolved **correctly** (it even titles
 ACM pages that curl cannot reach), but `attachments` is **always null**, across
 `format=zotero|csljson`. The cause is in the container's item-export module
 (`src/translation/`): ItemSaver is an object-only stub, so the server has no
 attachment-download capability and the attachment info is gone before output.
 ⇒ It is a **bibliographic metadata service**, not a retrieval service.

⚠️ cf_clearance is bound to **IP + User-Agent**. If you use an institutional VPN,
   warm the profile *while connected*, and do not connect/disconnect mid-run —
   every clearance already earned dies with the IP change.

⚠️ There are two kinds of 403 and they look alike in a log but mean opposite things:
   - `cf-mitigated: challenge` / "Just a moment" = bot block → the browser layer fixes it
   - a real HTML page showing Get Access / Purchase = paywall → only entitlement fixes it
   is_bot_block() is what tells them apart.

Usage (also importable — see fetch_pdf / http_get / extra_oa_urls):
  python3 pdf_fetch.py --out refs-pdf 10.1145/1240624.1240704 10.1002/ece3.5555
  python3 pdf_fetch.py --bib references.bib --out refs-pdf
  python3 pdf_fetch.py --dois dois.txt --out refs-pdf --no-browser
Options: --no-browser (open-access sources only, fast) / --headless (Cloudflare is
  more suspicious of headless; only for machines with no display) / --profile PATH.

Install for the browser layer: `pip install curl_cffi patchright`. patchright drives
your installed Chrome via channel="chrome" — it does not download a second browser.
Without them this degrades to urllib + open-access sources and says so.
"""
import base64, json, os, re, time, urllib.parse, urllib.request

# ---------- L1: HTTP ----------
try:
    from curl_cffi import requests as _cr
    HAVE_CURL_CFFI = True
except Exception:
    HAVE_CURL_CFFI = False

UA = ("Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/124.0 Safari/537.36")

CHALLENGE_RE = re.compile(
    r"just a moment|checking your browser|attention required|"
    r"verify you are human|enable javascript and cookies", re.I)

# Looking only at <title> misses Elsevier: its title is normal and the blocking text
# is in the body. Measured: ScienceDirect serves an "Are you a robot?" human-verification
# page to institutional VPN exit IPs.
CAPTCHA_RE = re.compile(
    r"are you a robot|confirm you are a human|complete the captcha|"
    r"unusual traffic", re.I)

# ⚠️ Every phrase here must appear ONLY when you genuinely lack access.
#    Learned the hard way: "add to cart" is a **site-chrome element on every T&F page**
#    (open-access articles included) — using it as evidence makes the tool write off
#    all of T&F as paywalled. "sign in" is too generic for the same reason.
#    ⇒ Keep only phrases that mean "you do not have access to *this* item".
PAYWALL_RE = re.compile(
    r"get access|purchase access|buy article|purchase pdf|rent this article|"
    r"institutional sign ?in|sign in to continue reading|purchase 24 hour|"
    r"access through your institution|purchase this article", re.I)


def is_bot_block(status, ctype, body, headers=None):
    """Bot block (the browser layer can fix it) vs paywall (only entitlement can)."""
    h = {k.lower(): v for k, v in (headers or {}).items()}
    if "cf-mitigated" in h:
        return True
    if status in (403, 503) and body and b"<" in body[:200]:
        head = body[:4000].decode("utf-8", "ignore")
        if CHALLENGE_RE.search(head):
            return True
        # Cloudflare challenge pages are tiny (~6 KB); paywall pages are full layouts
        if status == 403 and len(body) < 20000:
            return True
    return False


def http_get(url, timeout=45, cookies=None, referer=None, impersonate="chrome"):
    """Return (status, ctype, body, headers). Prefers curl_cffi, falls back to urllib.

    Never raises — on failure it returns status <= 0 and lets the caller decide
    whether to escalate to the next layer.
    """
    hdr = {"User-Agent": UA,
           "Accept": "application/pdf,text/html,*/*",
           "Accept-Language": "en-US,en;q=0.9"}
    if referer:
        hdr["Referer"] = referer
    if HAVE_CURL_CFFI:
        try:
            r = _cr.get(url, impersonate=impersonate, headers=hdr,
                        cookies=cookies or {}, timeout=timeout, allow_redirects=True)
            return (r.status_code, r.headers.get("content-type", ""), r.content, dict(r.headers))
        except Exception as ex:
            return (-1, "", b"", {"x-error": "%s: %s" % (type(ex).__name__, ex)})
    try:
        req = urllib.request.Request(url, headers=hdr)
        r = urllib.request.urlopen(req, timeout=timeout)
        return (r.status, r.headers.get("Content-Type", ""), r.read(), dict(r.headers))
    except Exception as ex:
        code = getattr(ex, "code", -1)
        body = b""
        try:
            body = ex.read()
        except Exception:
            pass
        return (code, "", body, {"x-error": "%s: %s" % (type(ex).__name__, ex)})


def looks_pdf(body):
    return bool(body) and body[:5] == b"%PDF-"


# ---------- L2: real browser ----------
try:
    from patchright.sync_api import sync_playwright
    HAVE_PATCHRIGHT = True
except Exception:
    HAVE_PATCHRIGHT = False

# ── Publisher PDF URL patterns ──────────────────────────────────
# ⚠️ These patterns **only work inside a real browser**: the same URLs return 403 to
#    urllib/curl_cffi. An earlier version of this pipeline had similar patterns bolted
#    onto urllib and they looked useless — the patterns were fine, the client was wrong.
# ⚠️ Corrected against live sites:
#    Wiley's /doi/pdf/ returns an **HTML viewer shell** (49 KB); the file is at /doi/pdfdirect/.
#    SAGE's /doi/reader/ and /doi/epub/ are shells too — use /doi/pdf/.
#    T&F's /doi/pdf/ returns the landing page itself: **no constructible PDF URL exists**,
#    it can only be reached by clicking the control (click-download).
def publisher_patterns(final_url, doi):
    host = urllib.parse.urlparse(final_url).netloc.lower()
    root = "https://" + host
    d = doi or ""
    out = []
    if "onlinelibrary.wiley.com" in host and d:
        out += [f"{root}/doi/pdfdirect/{d}?download=true", f"{root}/doi/pdfdirect/{d}"]
    if "journals.sagepub.com" in host and d:
        out += [f"{root}/doi/pdf/{d}", f"{root}/doi/pdf/{d}?download=true"]
    if "link.springer.com" in host and d:
        out += [f"{root}/content/pdf/{d}.pdf"]
    if "dl.acm.org" in host and d:
        out += [f"{root}/doi/pdf/{d}"]
    if "tandfonline.com" in host and d:
        out += [f"{root}/doi/epdf/{d}?needAccess=true"]
    if "pnas.org" in host and d:
        out += [f"{root}/doi/pdf/{d}"]
    if "sciencedirect.com" in host:
        m = re.search(r"/pii/([A-Z0-9]+)", final_url, re.I)
        if m:
            out += [f"{root}/science/article/pii/{m.group(1)}/pdfft?download=true"]
    if "ieeexplore.ieee.org" in host:
        m = re.search(r"/document/(\d+)", final_url)
        if m:
            out += [f"{root}/stamp/stamp.jsp?tp=&arnumber={m.group(1)}"]
    # ⚠️ The generic `/doi/pdf/` pattern **only applies to publishers actually running
    #    the Atypon platform**. An earlier version applied it to any host; against a
    #    national journal portal (not Atypon) it produced a URL that does not exist, and
    #    that site neither answers nor closes the connection → the in-page fetch hung
    #    for 193 seconds. ⇒ Allowlist. When unsure, do not guess a URL — let link
    #    discovery read it off the page.
    ATYPON = ("journals.aps.org", "www.pnas.org", "pubs.acs.org", "www.science.org",
              "royalsocietypublishing.org", "journals.aom.org", "www.emerald.com",
              "asmedigitalcollection.asme.org", "pubs.aip.org", "www.worldscientific.com")
    if d and any(h in host for h in ATYPON) and not any(u.endswith(f"/doi/pdf/{d}") for u in out):
        out += [f"{root}/doi/pdf/{d}"]
    return out


def entitlement_block(final_url):
    """Publisher-specific "you are not entitled to this" signal. Returns a string or None.

    ⚠️ These signals are more reliable than page text. Measured:
      with entitlement T&F stays on /doi/full/; without it you are **redirected to
      /doi/abs/**. The "Read this article" link on that page (a.grant-access) is not an
      institutional entry point — it leads to /doi/epdf/?needAccess=true, the purchase
      flow. Fetching /doi/full/ directly also redirects back to /doi/abs/.
      ⇒ Page text alone misjudges this: every T&F page carries "Add to Cart" in the
      header and an "Open access" item in the nav.
    """
    u = (final_url or "").lower()
    if "tandfonline.com" in u and "/doi/abs/" in u:
        return "T&F redirected to /doi/abs/ (no full-text entitlement)"
    return None


DEFAULT_PROFILE = os.path.expanduser("~/.cache/fetch-refs/chrome-profile")

# Find the PDF link on the landing page. Most reliable signal first.
_DISCOVER_JS = r"""(DOI) => {
  const out = [];
  const push = u => { try { if (u) out.push(new URL(u, location.href).href); } catch(e){} };
  document.querySelectorAll('meta[name="citation_pdf_url"]').forEach(m => push(m.content));
  document.querySelectorAll('a[href]').forEach(a => {
    const h = a.href, txt = (a.textContent||'').trim().toLowerCase();
    // ⚠️ All three signals are needed; any one alone has real blind spots:
    //   1. URL shape        — the common case
    //   2. link text        — "Download PDF" and friends
    //   3. **class / aria-label / title** — an icon link has EMPTY textContent!
    //      A national journal portal ships its download control as:
    //        <a href="/submission/api/download?id=..." class="icon pdf"></a>
    //      No text, no ".pdf" in the URL — only "pdf" in the class gives it away.
    //      Checking just the first two signals misses that article 100% of the time.
    const attrs = ((a.className||'')+' '+(a.getAttribute('aria-label')||'')+' '+
                   (a.getAttribute('title')||'')+' '+(a.getAttribute('data-title')||'')).toLowerCase();
    if (/\.pdf($|\?)|\/doi\/pdf|\/doi\/epdf|pdfdirect|\/content\/pdf|article-pdf|\/track\/pdf|\/pdfft/i.test(h)) push(h);
    else if (/^(pdf|download pdf|full text pdf|view pdf|get pdf|epdf)$/.test(txt)) push(h);
    else if (/\bpdf\b/.test(attrs)) push(h);
    else if (/\/(api\/)?download|getfile|fulltext|attachment|\/file\//i.test(h) && /pdf|download/.test(attrs+' '+txt)) push(h);
  });
  // ⚠️ Measured: SAGE reference lists contain .pdf links to *other* papers. Without
  //    scoping you happily download a completely unrelated file. Keep only candidates
  //    on the same host, or whose URL contains this article's DOI.
  const host = location.hostname;
  const uniq = [...new Set(out)];
  const scoped = uniq.filter(u => { try { const x = new URL(u);
      return x.hostname === host || (DOI && u.toLowerCase().includes(DOI.toLowerCase())); } catch(e){ return false; } });
  return scoped.length ? scoped : [];
}"""

# In-page fetch: uses the browser's own session and TLS, so a fingerprint mismatch
# is impossible by construction.
# ⚠️ **The AbortController is mandatory.** The browser's fetch() has no built-in
#    timeout, and playwright's set_default_timeout does not reach a promise inside
#    evaluate. Measured: fetching a non-existent URL on a site that neither answers
#    nor closes the connection hung this single evaluate for **193 seconds** and took
#    the whole batch with it. The per-item budget cannot save you — it is only
#    checked *between* steps.
_GRAB_JS = r"""async (args) => {
  const u = args.url, ms = args.ms || 20000;
  const ac = new AbortController();
  const t = setTimeout(() => ac.abort(), ms);
  try {
    const r = await fetch(u, {credentials:'include', signal: ac.signal});
    const b = await r.arrayBuffer();
    let s = ''; const bytes = new Uint8Array(b);
    const CH = 0x8000;
    for (let i=0; i<bytes.length; i+=CH) s += String.fromCharCode.apply(null, bytes.subarray(i, i+CH));
    return {ok:true, status:r.status, ctype:r.headers.get('content-type')||'', b64: btoa(s)};
  } catch (e) { return {ok:false, err: String(e)}; }
  finally { clearTimeout(t); }
}"""


class BrowserSession:
    """A real Chrome on a persistent profile.

    Use it as a context manager and process the whole batch in one session — that is
    what lets cf_clearance be reused instead of re-earned per item.
    """

    def __init__(self, profile=DEFAULT_PROFILE, headless=False, verbose=True):
        self.profile, self.headless, self.verbose = profile, headless, verbose
        self._pw = self._ctx = self._pg = None

    def __enter__(self):
        if not HAVE_PATCHRIGHT:
            raise RuntimeError("patchright not installed: pip install patchright")
        os.makedirs(self.profile, exist_ok=True)
        self._dl = os.path.join(self.profile, "_downloads")
        os.makedirs(self._dl, exist_ok=True)
        self._pw = sync_playwright().start()
        self._ctx = self._pw.chromium.launch_persistent_context(
            user_data_dir=self.profile, channel="chrome", headless=self.headless,
            no_viewport=True, accept_downloads=True, downloads_path=self._dl)
        self._pg = self._ctx.pages[0] if self._ctx.pages else self._ctx.new_page()
        # ⚠️ Without these two lines a single item can hang for ten minutes or more.
        #    Playwright defaults to 30 s, but if the page keeps loading after goto,
        #    subsequent title()/evaluate() calls queue up behind it indefinitely.
        self._pg.set_default_timeout(15000)
        self._pg.set_default_navigation_timeout(45000)
        self._arm_page(self._pg)
        return self

    def _arm_page(self, pg):
        """Attach page-level guards.

        🔴 **A dialog freezes the entire page.** Measured: a journal portal popped a
           login dialog during retrieval, after which every CDP operation went
           unanswered — the 100 s per-item budget could not save it, because the
           budget is only checked *between* steps and the thread was stuck inside
           the dialog. ⇒ Always attach a dialog handler that dismisses;
           beforeunload goes through the same path.
        Popups (window.open login windows) are closed outright so they cannot steal
        focus or pile up.
        """
        try:
            pg.on("dialog", lambda d: self._dismiss(d))
            pg.on("popup", lambda pop: self._kill_popup(pop))
        except Exception:
            pass

    @staticmethod
    def _dismiss(d):
        try:
            d.dismiss()
        except Exception:
            pass

    @staticmethod
    def _kill_popup(pop):
        try:
            pop.close()
        except Exception:
            pass

    def __exit__(self, *a):
        for close in (getattr(self._ctx, "close", None), getattr(self._pw, "stop", None)):
            try:
                close and close()
            except Exception:
                pass
        return False

    # -- internals --
    def _log(self, *m):
        if self.verbose:
            print("      ", *m, flush=True)

    def page_state(self):
        """Return ('ok'|'challenge'|'captcha'|'paywall', evidence).

        These are three completely different failures needing three different responses.
        """
        try:
            title = self._pg.title() or ""
            body = self._pg.evaluate("() => (document.body ? document.body.innerText : '').slice(0, 4000)") or ""
        except Exception:
            return ("challenge", "page not readable yet")
        # ⚠️ **Check captcha BEFORE challenge.** Measured: ScienceDirect's captcha page
        #    carries Cloudflare's "Just a moment..." <title> while the body says
        #    "Are you a robot?". With the order reversed it is classified as
        #    "challenge in progress" → waits out the full 50 s → then mis-reports as
        #    NO-LINK, telling the author the tool does not support Elsevier when the
        #    truth is "click the captcha once".
        #    The distinction: challenge is **transient** (waiting works), captcha is
        #    **terminal** (only a human clears it).
        m = CAPTCHA_RE.search(body[:1500])
        if m:
            return ("captcha", m.group(0))
        if CHALLENGE_RE.search(title) or CHALLENGE_RE.search(body[:600]):
            return ("challenge", "Cloudflare challenge in progress")
        m = PAYWALL_RE.search(body)
        return ("paywall", m.group(0)) if m else ("ok", "")

    def _clear_challenge(self, timeout=50):
        """Wait out the Cloudflare challenge, clicking the Turnstile checkbox if needed."""
        end = time.time() + timeout
        clicked = False
        state = "challenge"
        while time.time() < end:
            state, _ = self.page_state()
            if state != "challenge":
                return state
            if not clicked:
                try:
                    for fr in self._pg.frames:
                        if "challenges.cloudflare.com" in (fr.url or ""):
                            fr.locator("input[type=checkbox]").first.click(timeout=3000)
                            clicked = True
                            break
                except Exception:
                    pass
            time.sleep(1.5)
        return state

    def _grab(self, url, referer=None):
        """In-page fetch on the main page. Returns bytes or None."""
        return self._grab_on(self._pg, url)

    def _grab_on(self, pg, url, ms=20000):
        try:
            r = pg.evaluate(_GRAB_JS, {"url": url, "ms": ms})
        except Exception as ex:
            self._log("in-page fetch raised:", str(ex)[:70])
            return None
        if not r or not r.get("ok"):
            return None
        data = base64.b64decode(r["b64"])
        return data if looks_pdf(data) else None

    def _download_url(self, url):
        """Navigate to a direct PDF URL and catch the download event.

        For sites where CORS/CSP blocks the in-page fetch (AIP, for one).

        🔴 **This must open its own page.** Measured: doing `location.href = u` on the
           main page makes Chrome close that tab for some URLs. Once the main page dies,
           `self._pg` is permanently invalid and **every remaining item in the batch
           reports "Target page, context or browser has been closed"** — one bad item
           killed fifteen good ones. A throwaway page keeps the blast radius at one.
        """
        tmp = None
        try:
            tmp = self._ctx.new_page()
            tmp.set_default_timeout(15000)
            self._arm_page(tmp)
            with tmp.expect_download(timeout=20000) as dl:
                tmp.evaluate("u => { location.href = u; }", url)
            return self._read_download(dl.value)
        except Exception:
            return None
        finally:
            try:
                if tmp and not tmp.is_closed():
                    tmp.close()
            except Exception:
                pass

    def _navigate_capture(self, url, wait=8):
        """Navigate a throwaway page to url and capture **any** response body whose
        content-type is PDF.

        🔴 Elsevier only works this way. Measured: ScienceDirect's PDF link is
           `/pii/{PII}/pdfft?md5=...&pid=...` where md5 is a one-time per-session token
           (**not constructible** — it can only be read off the rendered page), and that
           URL returns an **HTML interstitial (51 KB)** that hops once more to the file.
           ⇒ An in-page fetch always lands on the interstitial, and a download event may
             never fire either (Chrome can open the PDF in its built-in viewer, which is
             not a download). Capturing the response body handles all three cases.
        """
        tmp = None
        hits = []

        def on_resp(r):
            try:
                if "pdf" in (r.headers or {}).get("content-type", "").lower():
                    hits.append(r)
            except Exception:
                pass

        try:
            tmp = self._ctx.new_page()
            tmp.set_default_timeout(15000)
            self._arm_page(tmp)
            tmp.on("response", on_resp)
            try:
                tmp.goto(url, wait_until="commit", timeout=30000)
            except Exception:
                pass
            end = time.time() + wait
            while time.time() < end and not hits:
                time.sleep(0.5)
            time.sleep(1.0)
            for r in hits:
                try:
                    b = r.body()
                    if looks_pdf(b):
                        return b
                except Exception:
                    continue
            # case: the page itself turned into the PDF viewer
            try:
                if tmp.evaluate("() => document.contentType") == "application/pdf":
                    b = self._grab_on(tmp, tmp.url)
                    if b:
                        return b
            except Exception:
                pass
            return None
        except Exception:
            return None
        finally:
            try:
                if tmp and not tmp.is_closed():
                    tmp.close()
            except Exception:
                pass

    def _click_download(self):
        """Click the real "PDF / Download PDF" control on the landing page.

        ⚠️ T&F needs this path: measured, both /doi/pdf/{doi} and /doi/epdf/{doi} return
           **the landing page itself** (202 KB of HTML). There is no constructible PDF
           URL and no citation_pdf_url meta tag.
        """
        SEL = ("a[href*='/doi/pdf'], a[href*='pdfdirect'], a[href*='pdfft'], "
               "a[href*='stamp.jsp'], a[href*='.pdf'], "
               "a[title*='PDF' i], a[aria-label*='PDF' i], button[aria-label*='PDF' i]")
        try:
            loc = self._pg.locator(SEL)
            n = min(loc.count(), 2)
        except Exception:
            return None
        for i in range(n):
            try:
                with self._pg.expect_download(timeout=8000) as dl:
                    loc.nth(i).click(timeout=4000)
                d = self._read_download(dl.value)
                if d:
                    return d
            except Exception:
                continue
        return None

    def _read_download(self, download):
        try:
            path = download.path()
            data = open(path, "rb").read()
            try:
                os.unlink(path)
            except Exception:
                pass
            return data if looks_pdf(data) else None
        except Exception:
            return None

    def _ensure_page(self):
        """Ensure the main page is usable; reopen it if it was closed.

        One bad item must not take down the batch.
        """
        try:
            if self._pg is not None and not self._pg.is_closed():
                return True
        except Exception:
            pass
        try:
            self._pg = self._ctx.new_page()
            self._pg.set_default_timeout(15000)
            self._pg.set_default_navigation_timeout(45000)
            self._arm_page(self._pg)
            return True
        except Exception:
            return False

    def cookies_for(self, domain):
        try:
            return {c["name"]: c["value"] for c in self._ctx.cookies()
                    if domain in c.get("domain", "")}
        except Exception:
            return {}

    # -- public --
    def fetch_pdf(self, landing_url, doi="", extra_urls=(), budget=100):
        """Open the landing page → clear the challenge → try candidates → fetch.

        Returns (bytes|None, source_url|None, note). The note **starts with a
        classification tag**, and that tag is the point of this whole function:

          OK        got the file
          PAYWALL   no entitlement — no tool fixes this; use ILL, ask the author,
                    or look for an author-hosted copy
          CAPTCHA   a human must clear it once (see warm_profile.py); then re-run
          NO-LINK   the page rendered but no PDF was found — **this is the only
                    bucket where the tool itself can still improve**
          CHALLENGE / TIMEOUT / ERROR   transient; re-running usually helps

        Reporting all of these as one undifferentiated "needs a browser" is what makes
        a reference-collection run useless: the author cannot tell which items are worth
        five more minutes and which are simply not available to them.

        budget = seconds allowed for this item. ⚠️ Non-optional: single items have been
        observed hanging past ten minutes, which kills a batch of dozens. On expiry it
        returns TIMEOUT so the batch moves on.
        """
        deadline = time.time() + budget

        def out_of_time():
            return time.time() > deadline

        if not self._ensure_page():
            return (None, None, "ERROR browser session is dead and unrecoverable")
        try:
            self._pg.goto(landing_url, wait_until="domcontentloaded", timeout=60000)
        except Exception as ex:
            return (None, None, "ERROR goto failed: %s" % str(ex)[:60])
        state = self._clear_challenge(timeout=min(50, max(5, deadline - time.time())))
        if state == "challenge":
            return (None, None, "CHALLENGE Cloudflare challenge not cleared (timeout)")
        if state == "captcha":
            _, ev = self.page_state()
            return (None, None, "CAPTCHA needs a human (%s) — clear it once via warm()" % ev[:40])
        time.sleep(2.0)                      # let JS render the PDF control
        final = self._pg.url

        try:
            if self._pg.evaluate("() => document.contentType") == "application/pdf":
                d = self._grab(final)
                if d:
                    return (d, final, "OK landing-is-pdf")
        except Exception:
            pass

        # ⚠️ Link discovery must **poll**, not scan once. ScienceDirect renders in JS:
        #    at 2 s only one candidate exists; the real pdfft link carrying the one-time
        #    md5 token appears around 8 s. Scanning once makes the tool flaky — the same
        #    DOI gives different results on different runs.
        cands = []
        for _ in range(5):
            try:
                cands = self._pg.evaluate(_DISCOVER_JS, doi) or []
            except Exception:
                cands = []
            if cands or out_of_time():
                break
            time.sleep(2.0)
        cands = list(cands)
        cands += publisher_patterns(final, doi)
        cands += [u for u in extra_urls if u]
        seen = set()
        cands = [u for u in cands if not (u in seen or seen.add(u))]

        # in-page fetch is the cheapest — try every candidate this way first
        for u in cands[:8]:
            if out_of_time():
                return (None, None, "TIMEOUT over %ds budget (in-page fetch stage)" % budget)
            d = self._grab(u)
            if d:
                return (d, u, "OK in-page-fetch")

        # ⚠️ Order matters: decide "paywall" BEFORE the expensive download/click stages.
        #    Before this reordering a single Wiley item cost 224 s and a T&F item 124 s,
        #    all of it spent clicking buttons on a paywall.
        eb = entitlement_block(self._pg.url)
        if eb:
            return (None, None, "PAYWALL %s" % eb)
        state, ev = self.page_state()
        if state == "paywall":
            return (None, None, "PAYWALL no entitlement (page says \"%s\")" % ev[:34])

        for u in cands[:3]:
            if out_of_time():
                return (None, None, "TIMEOUT over %ds budget (navigate-capture stage)" % budget)
            d = self._navigate_capture(u)
            if d:
                return (d, u, "OK navigate-capture")
        for u in cands[:2]:
            if out_of_time():
                return (None, None, "TIMEOUT over %ds budget (download stage)" % budget)
            d = self._download_url(u)
            if d:
                return (d, u, "OK browser-download")
        if not out_of_time():
            d = self._click_download()
            if d:
                return (d, final, "OK click-download")

        # Re-check at the end: the captcha often appears **later** (ScienceDirect only
        # shows it after the redirect settles), so the check at page-open misses it.
        # Without this re-check a CAPTCHA is mis-reported as NO-LINK, telling the author
        # the tool does not support that publisher instead of "click it once".
        state, ev = self.page_state()
        if state == "captcha":
            return (None, None, "CAPTCHA needs a human (%s) — see warm_profile.py" % ev[:30])
        if state == "paywall":
            return (None, None, "PAYWALL no entitlement (page says \"%s\")" % ev[:34])
        return (None, None, "NO-LINK tried %d candidates, none were PDFs" % len(cands))

    def warm(self, url, seconds=6):
        """Warm up: open a site once to earn cf_clearance.

        Also how you sign in to institutional access by hand (headless=False).
        """
        try:
            self._pg.goto(url, wait_until="domcontentloaded", timeout=60000)
        except Exception:
            return False
        ok = self._clear_challenge()
        time.sleep(seconds)
        return ok


# ---------- L0: extra open-access sources (far cheaper than touching publishers) ----------
# The usual four are Unpaywall / OpenAlex / Semantic Scholar / arXiv. These three are
# worth adding, and none of them sit behind a publisher paywall so none can block you:
#   Europe PMC — biomedical-leaning but far broader in practice; gives a PDF directly
#                when a PMC full text exists
#   CORE       — the largest OA full-text aggregator (~32.8 M documents) and, crucially,
#                it **hosts its own copies**, so it often still has the file when an
#                institutional repository has moved or been retired. That is the direct
#                answer to "the OA flag was true but the link is dead".
#   OpenAIRE   — EU aggregator, keyless
# CORE needs a free key: https://core.ac.uk/services/api → set CORE_API_KEY

def _jget(url, timeout=20, headers=None):
    try:
        req = urllib.request.Request(url, headers={"User-Agent": UA, **(headers or {})})
        return json.load(urllib.request.urlopen(req, timeout=timeout))
    except Exception:
        return {}


def europepmc_urls(doi):
    """Europe PMC PDF links, read from fullTextUrlList — never constructed.

    An earlier version also appended a guessed REST endpoint
    (`/europepmc/webservices/rest/{PMCID}/fullTextPdf`); it 404s every time.
    Europe PMC already lists the working PDF URL in fullTextUrlList, so guessing
    only bought a guaranteed-failing request. (Note their listed URL can still
    return 500 "Failed to retrieve PDF for pmcid" for individual articles —
    that is their outage, not a wrong URL; just move on to the next source.)
    """
    if not doi:
        return []
    q = urllib.parse.quote('DOI:"%s"' % doi)
    d = _jget("https://www.ebi.ac.uk/europepmc/webservices/rest/search"
              "?query=%s&resultType=core&format=json&pageSize=1" % q)
    out = []
    for r in ((d.get("resultList") or {}).get("result") or []):
        for u in ((r.get("fullTextUrlList") or {}).get("fullTextUrl") or []):
            if u.get("documentStyle") == "pdf" and u.get("url"):
                out.append(u["url"])
    return out


def core_urls(doi, api_key=None):
    key = api_key or os.environ.get("CORE_API_KEY")
    if not (doi and key):
        return []
    d = _jget("https://api.core.ac.uk/v3/search/works?q=%s&limit=3"
              % urllib.parse.quote('doi:"%s"' % doi),
              headers={"Authorization": "Bearer " + key})
    out = []
    for w in (d.get("results") or []):
        if (w.get("doi") or "").lower().rstrip(".") != doi.lower().rstrip("."):
            continue     # CORE matches loosely; without pinning the DOI you get other papers
        if w.get("downloadUrl"):
            out.append(w["downloadUrl"])
        for l in (w.get("links") or []):
            if l.get("type") == "download" and l.get("url"):
                out.append(l["url"])
    return out


def openaire_urls(doi):
    if not doi:
        return []
    try:
        req = urllib.request.Request(
            "https://api.openaire.eu/search/publications?doi=%s&format=json&size=1"
            % urllib.parse.quote(doi), headers={"User-Agent": UA})
        raw = urllib.request.urlopen(req, timeout=20).read().decode("utf-8", "ignore")
    except Exception:
        return ""
    return [u for u in re.findall(r'https?://[^"\'<>\s]+?\.pdf', raw)][:3]


def extra_oa_urls(doi):
    """Union of the three extra OA sources (deduped, order preserved).

    Any one of them failing does not affect the others.
    """
    out = []
    for fn in (europepmc_urls, core_urls, openaire_urls):
        try:
            out += fn(doi) or []
        except Exception:
            pass
    seen = set()
    return [u for u in out if u and not (u in seen or seen.add(u))]


# ---------- CLI ----------
def _parse_bib_dois(path):
    out = []
    txt = open(path, encoding="utf-8", errors="ignore").read()
    for m in re.finditer(r"@\w+\s*\{\s*([^,]+),(.*?)(?=\n@\w+\s*\{|\Z)", txt, re.S):
        key, body = m.group(1).strip(), m.group(2)
        d = re.search(r'10\.\d{4,9}/[^\s,}"]+', body)
        if d:
            out.append((key, d.group(0).rstrip(".")))
    return out


def _safe(name):
    return re.sub(r"[^\w.\-]+", "_", name)[:120] or "ref"


def main():
    import argparse
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("dois", nargs="*", help="DOIs given directly")
    ap.add_argument("--bib", help="BibTeX file; DOIs read from doi fields")
    ap.add_argument("--dois", dest="doi_file", help="text file, one DOI per line")
    ap.add_argument("--out", default="refs-pdf", help="output directory (default: refs-pdf)")
    ap.add_argument("--no-browser", action="store_true",
                    help="open-access sources only; fast, but Cloudflare publishers will all miss")
    ap.add_argument("--headless", action="store_true",
                    help="no browser window (Cloudflare is more suspicious of headless)")
    ap.add_argument("--profile", default=DEFAULT_PROFILE, help="persistent Chrome profile path")
    a = ap.parse_args()

    entries = []
    if a.bib:
        entries += _parse_bib_dois(a.bib)
    if a.doi_file:
        for ln in open(a.doi_file, encoding="utf-8"):
            ln = re.sub(r"^(?:https?://)?(?:dx\.)?doi\.org/", "", ln.strip())
            if ln and not ln.startswith("#"):
                entries.append((ln, ln))
    for d in a.dois:
        d = re.sub(r"^(?:https?://)?(?:dx\.)?doi\.org/", "", d)
        entries.append((d, d))
    if not entries:
        ap.error("nothing to fetch: give --bib, --dois, or DOIs on the command line")

    os.makedirs(a.out, exist_ok=True)
    print("engine: curl_cffi=%s | browser=%s" %
          (HAVE_CURL_CFFI, "off" if a.no_browser else HAVE_PATCHRIGHT), flush=True)

    pending, got = [], 0
    for key, doi in entries:                       # L0/L1: open access first
        data = b""
        for u in extra_oa_urls(doi):
            st, ct, body, _h = http_get(u)
            if 200 <= st < 300 and looks_pdf(body):
                data = body
                break
        if data:
            open(os.path.join(a.out, _safe(key) + ".pdf"), "wb").write(data)
            print("  [OK]   %-34s open-access (%d b)" % (key[:34], len(data)), flush=True)
            got += 1
        else:
            pending.append((key, doi))

    if pending and not a.no_browser and HAVE_PATCHRIGHT:   # L2: real browser
        print("\nbrowser layer: %d item(s) - a Chrome window will open; leave it alone"
              % len(pending), flush=True)
        with BrowserSession(profile=a.profile, headless=a.headless, verbose=False) as bs:
            for key, doi in pending:
                data, src, how = bs.fetch_pdf("https://doi.org/" + doi, doi=doi)
                if data:
                    open(os.path.join(a.out, _safe(key) + ".pdf"), "wb").write(data)
                    print("  [OK]   %-34s %s (%d b)" % (key[:34], how, len(data)), flush=True)
                    got += 1
                else:
                    print("  [MISS] %-34s %s" % (key[:34], how[:60]), flush=True)
    elif pending and not a.no_browser:
        print("\nbrowser layer unavailable (pip install patchright); %d item(s) left"
              % len(pending), flush=True)

    print("\n%d/%d obtained -> %s" % (got, len(entries), a.out))
    print("Verify every file's content against its citation before trusting it - "
          "see skills/fetch-refs (right link, wrong file is common).")


if __name__ == "__main__":
    main()
