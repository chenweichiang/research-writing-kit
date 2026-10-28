#!/usr/bin/env python3
# /// script
# requires-python = ">=3.9"
# dependencies = []
# ///
"""deadline.py: convert a submission deadline to your own timezone, then show how long is
left and a suggested submit time.

Why it exists: call-for-papers deadlines are given in "AoE", "PST", "23:59 UTC+8" and the
like, and the mental conversion is where people lose a day. "Anywhere on Earth" (UTC-12)
lands on the evening of the NEXT day in East Asia; a "PST" deadline in July is really PDT.
This tool does the arithmetic with real timezone rules (daylight saving by date) and prints
a suggested submit time 24 hours before the deadline, because upload systems fail at the
last minute.

Usage:
  deadline.py "2026-10-26 23:59" --tz AoE [--to Asia/Taipei] [--now "2026-10-25 12:00"]

--tz accepts: AoE (fixed UTC-12); UTC-12 / UTC+8 / GMT+5:30; US abbreviations PST, PDT,
EST, EDT, CST, MST (daylight saving is decided by the date, so PST in July is PDT);
JST, CET, CEST, BST, KST, UTC, TST; or an IANA name (America/New_York).
--to is the timezone to convert into (default: this machine's local timezone; an IANA
name such as Asia/Taipei or Europe/Paris, or any value --tz accepts).
--now is for tests and rehearsals only (read in the --to timezone; default: the real now).

Exit codes: 0 success; 2 unrecognised timezone or time format.
"""
import argparse
import os
import re
import sys
from datetime import datetime, timedelta, timezone

try:
    from zoneinfo import ZoneInfo
except ImportError:  # pragma: no cover
    print("Python 3.9+ with zoneinfo is required", file=sys.stderr)
    sys.exit(2)

# abbreviation -> IANA zone; the US abbreviations resolve by date through zoneinfo
ABBR = {
    "PST": "America/Los_Angeles", "PDT": "America/Los_Angeles",
    "MST": "America/Denver", "MDT": "America/Denver",
    "CST": "America/Chicago", "CDT": "America/Chicago",
    "EST": "America/New_York", "EDT": "America/New_York",
    "CET": "Europe/Paris", "CEST": "Europe/Paris",
    "BST": "Europe/London", "GMT": "UTC",
    "JST": "Asia/Tokyo", "KST": "Asia/Seoul", "TST": "Asia/Taipei", "CCT": "Asia/Taipei",
    "UTC": "UTC", "Z": "UTC",
}
WEEK = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]


def local_tz():
    """The machine's local timezone as an IANA zone when it can be found (so daylight
    saving is right for the deadline's date), else the current fixed offset."""
    tzenv = os.environ.get("TZ", "").lstrip(":")
    if tzenv:
        try:
            return ZoneInfo(tzenv)
        except (KeyError, ValueError, OSError):
            pass
    try:
        link = os.path.realpath("/etc/localtime")
        if "zoneinfo/" in link:
            return ZoneInfo(link.split("zoneinfo/", 1)[1])
    except (KeyError, ValueError, OSError):
        pass
    return datetime.now().astimezone().tzinfo


def parse_tz(name):
    s = name.strip()
    up = s.upper()
    if up == "AOE":
        return timezone(timedelta(hours=-12), "AoE")
    m = re.fullmatch(r"(?:UTC|GMT)\s*([+\-−])\s*(\d{1,2})(?::?(\d{2}))?", up)
    if m:
        sign = -1 if m.group(1) in "-−" else 1
        off = timedelta(hours=int(m.group(2)), minutes=int(m.group(3) or 0)) * sign
        if abs(off) > timedelta(hours=14):
            raise ValueError(f"offset out of range: {name}")
        return timezone(off, f"UTC{m.group(1)}{m.group(2)}")
    if up in ABBR:
        return ZoneInfo(ABBR[up])   # daylight saving follows the date
    try:
        return ZoneInfo(s)
    except Exception:
        raise ValueError(f"unrecognised timezone: {name}")


def parse_time(text, tz):
    for fmt in ("%Y-%m-%d %H:%M", "%Y-%m-%d %H:%M:%S", "%Y-%m-%dT%H:%M", "%Y/%m/%d %H:%M"):
        try:
            return datetime.strptime(text.strip(), fmt).replace(tzinfo=tz)
        except ValueError:
            pass
    raise ValueError(f"unrecognised time format: {text} (use YYYY-MM-DD HH:MM)")


def fmt_local(dt):
    return f"{dt:%Y-%m-%d %H:%M} ({WEEK[dt.weekday()]})"


def fmt_delta(td):
    secs = int(abs(td.total_seconds()))
    d, rem = divmod(secs, 86400)
    h, rem = divmod(rem, 3600)
    m = rem // 60
    return f"{d}d {h}h {m}min"


def main(argv=None):
    ap = argparse.ArgumentParser(description=(__doc__ or "").split("\n")[0])
    ap.add_argument("when", help='e.g. "2026-10-26 23:59"')
    ap.add_argument("--tz", required=True, help="timezone the deadline is stated in")
    ap.add_argument("--to", default=None,
                    help="timezone to convert into (default: this machine's local timezone)")
    ap.add_argument("--now", default=None,
                    help="testing only: pretend this is now (read in the --to timezone)")
    a = ap.parse_args(argv)
    try:
        src_tz = parse_tz(a.tz)
        dst_tz = parse_tz(a.to) if a.to else local_tz()
        dst_label = a.to or (getattr(dst_tz, "key", None) or "local time")
        t = parse_time(a.when, src_tz)
        now = parse_time(a.now, dst_tz) if a.now else datetime.now(timezone.utc)
    except ValueError as e:
        print(f"error: {e}", file=sys.stderr)
        return 2
    local = t.astimezone(dst_tz)
    z = t.strftime("%z")
    print(f"Original: {t:%Y-%m-%d %H:%M} {a.tz} ({t.tzname() or ''}, UTC{z[:3]}:{z[3:]})")
    print(f"Converted: {fmt_local(local)} {dst_label}")
    left = t - now
    if left.total_seconds() >= 0:
        print(f"Remaining: {fmt_delta(left)}")
    else:
        print(f"Expired: {fmt_delta(left)} ago")
    print(f"Suggested submit time: {fmt_local(local - timedelta(hours=24))} {dst_label} "
          "(24 hours before the deadline)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
